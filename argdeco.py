import argparse
import functools
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Protocol, Sequence, Tuple, Type, TypeVar, Union, cast, overload

import wrapt

_T = TypeVar("_T")
_TFunc = TypeVar("_TFunc", bound=Callable[..., _T])
_N = TypeVar("_N")

_Decorator = Callable[[_T], ArgumentDecorator[_TFunc]]
_OptionalDecorator = Union[ArgumentDecorator[_TFunc],
                           functools.partial[ArgumentDecorator[_TFunc]]]


class ArgumentDecorator(Protocol[_TFunc]):

    parser: argparse.ArgumentParser

    _title_group_map: Dict[str, argparse._ArgumentGroup]

    __call__: _TFunc


class ContainerAction(Protocol):

    @staticmethod
    def __call__(container: argparse._ActionsContainer,
                 *args, **kwargs) -> Optional[argparse._ActionsContainer]: ...


@wrapt.decorator
def _callback(wrapped: ArgumentDecorator[_TFunc],
              instance: object,
              args, kwargs, /) -> Any:

    def wrapper(args: Optional[Sequence[str]] = None,
                namespace: Optional[argparse.Namespace] = None, *,
                parse_func=argparse.ArgumentParser.parse_args) -> Tuple[Optional[Sequence[str]],
                                                                        Optional[argparse.Namespace],
                                                                        Callable]:
        return args, namespace, parse_func

    *params, parse_func = wrapper(*args, **kwargs)
    namespace, *extras = parse_func(wrapped.parser, *params)
    if (callback := (attrs := vars(namespace)).pop("callback", None)) is None:
        return wrapped(**attrs)
    return callback(**attrs) if instance is None else callback(instance, **attrs)


def argument_parser(wrapped: Optional[_TFunc] = None, /, *,
                    cls: Type[argparse.ArgumentParser] = argparse.ArgumentParser,
                    **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(cast(Callable[[_TFunc], ArgumentDecorator[_TFunc]], argument_parser), cls=cls, **kwargs)
    argument_decorator = cast(ArgumentDecorator[_TFunc], wrapped)
    argument_decorator.parser = cls(**kwargs)
    argument_decorator._title_group_map = {}  # TODO: improve implementation detail
    return _callback(argument_decorator)


def set_defaults(wrapped: Optional[ArgumentDecorator[_TFunc]] = None,
                 **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(cast(Callable[..., ArgumentDecorator[_TFunc]], set_defaults), **kwargs)
    wrapped.parser.set_defaults(**kwargs)
    return wrapped


def _add_container_actions(action: ContainerAction, /,
                           *args,
                           name: Optional[str] = None,
                           group: Optional[str] = None,
                           **kwargs):

    def wrapper(wrapped: ArgumentDecorator[_TFunc], /) -> ArgumentDecorator[_TFunc]:
        if (container := wrapped.parser if group is None
                else wrapped._title_group_map.get(group, None)) is None:
            raise ValueError(f"unknown group {group}")
        container = action(container, *args, **kwargs)
        if name is not None:
            wrapped._title_group_map[name] = container
        return wrapped

    return wrapper


def add_argument(*args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args,
                                  group=group,
                                  **kwargs)


def add_argument_group(name: str, /, *args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument_group,
                                  *args,
                                  name=name,
                                  group=group,
                                  **kwargs,)


def add_mutually_exclusive_group(name: str, /, *args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group,
                                  *args,
                                  name=name,
                                  group=group,
                                  **kwargs,)


def add_subparsers(wrapped: Optional[ArgumentDecorator[_TFunc]] = None, /,
                   **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(cast(Callable[[ArgumentDecorator[_TFunc]], ArgumentDecorator[_TFunc]], add_subparsers),
                                 **kwargs)
    wrapped.parser.add_subparsers(**kwargs)
    return wrapped


def add_parser(callback: ArgumentDecorator[_TFunc], /,
               *args, **kwargs):

    def wrapper(wrapped: _TFunc, /):
        if (subparsers := callback.parser._subparsers) is None:
            raise ValueError
        for action in subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                argument_decorator = cast(ArgumentDecorator[_TFunc], wrapped)
                argument_decorator.parser = action.add_parser(*args, **kwargs)
                argument_decorator._title_group_map = {}
                callback.parser.set_defaults(callback=argument_decorator)
                return _callback(argument_decorator)

    if callback.parser._subparsers is None:
        callback.parser.error("unknown subparser arguments")
    return wrapper
