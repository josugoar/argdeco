import argparse
import functools
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Protocol, Sequence, Tuple, Type, TypeVar, Union, cast, overload

import wrapt

_TFunc = TypeVar("_TFunc", bound=Callable)


class _ArgumentDecorator(Protocol[_TFunc]):
    parser: argparse.ArgumentParser
    _groups: Dict[str, argparse._ArgumentGroup]
    __call__: _TFunc


class _ContainerAction(Protocol):

    @staticmethod
    def __call__(container: argparse._ActionsContainer,
                 *args, **kwargs) -> Any: ...


_TFuncArgumentDecorator = _ArgumentDecorator[_TFunc]

_TFuncArgumentDecoratorWrapper = Callable[[_TFuncArgumentDecorator],
                                          _TFuncArgumentDecorator]

_OptionalDecorator = Union[_TFuncArgumentDecorator,
                           functools.partial[_TFuncArgumentDecorator]]


@wrapt.decorator
def _callback(wrapped: _TFuncArgumentDecorator,
              instance: object,
              args, kwargs, /) -> Any:

    _TArgs = TypeVar("_TArgs", bound=Sequence[str])
    _TNamespace = TypeVar("_TNamespace", bound=argparse.Namespace)

    # TODO: overload parse_func
    def wrapper(args: Optional[_TArgs] = None,
                namespace: Optional[_TNamespace] = None, *,
                parse_func: Callable = argparse.ArgumentParser.parse_args) -> Tuple[Optional[_TArgs],
                                                                                    Optional[_TNamespace],
                                                                                    Callable]:
        return args, namespace, parse_func

    *params, parse_func = wrapper(*args, **kwargs)
    namespace, *extras = parse_func(wrapped.parser, *params)
    if (callback := (attrs := vars(namespace)).pop("callback", None)) is None:
        return wrapped(**attrs)
    return callback(**attrs) if instance is None else callback(instance, **attrs)


# def _optional_decorator(wrapped: Callable, **kwargs) -> _OptionalDecorator:
#     if wrapped is None:
#         return functools.partial(_optional_decorator, **kwargs)
#     ...
#     return


def argument_parser(wrapped: Optional[_TFunc] = None, /, *,
                    cls: Type[argparse.ArgumentParser] = argparse.ArgumentParser,
                    **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(
            cast(Callable[[_TFunc], _TFuncArgumentDecorator],
                 argument_parser),
            cls=cls, **kwargs
        )
    argument_decorator = cast(_TFuncArgumentDecorator, wrapped)
    argument_decorator.parser = cls(**kwargs)
    argument_decorator._groups = {}  # TODO: improve implementation detail
    return _callback(argument_decorator)


def set_defaults(wrapped: Optional[_TFuncArgumentDecorator] = None, **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(cast(_TFuncArgumentDecoratorWrapper, set_defaults), **kwargs)
    wrapped.parser.set_defaults(**kwargs)
    return wrapped


def _add_container_actions(add_func: Callable, /,
                           *args,
                           name: Optional[str] = None,
                           group: Optional[str] = None,
                           **kwargs):

    def wrapper(wrapped: _TFuncArgumentDecorator, /) -> _TFuncArgumentDecorator:
        if (container := wrapped.parser if group is None
                else wrapped._groups.get(group, None)) is None:  # type: ignore
            raise ValueError(f"unknown group {group}")
        action = add_func(container, *args, **kwargs)
        if name is not None:
            wrapped._groups[name] = action
        return wrapped

    return wrapper


def add_argument(*args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args, group=group, **kwargs)


def add_argument_group(name: str, /, *args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument_group,
                                  *args, name=name, group=group, **kwargs)


def add_mutually_exclusive_group(name: str, /, *args, group: str = None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group,
                                  *args, name=name, group=group, **kwargs)


def add_subparsers(wrapped: Optional[_TFuncArgumentDecorator] = None, /, **kwargs) -> _OptionalDecorator:
    if wrapped is None:
        return functools.partial(cast(_TFuncArgumentDecoratorWrapper, add_subparsers), **kwargs)
    wrapped.parser.add_subparsers(**kwargs)
    return wrapped


def add_parser(argument_decorator: _TFuncArgumentDecorator, /, *args, **kwargs):

    def wrapper(wrapped: _TFunc, /):
        if subparsers is None:
            parser.error("unknown subparser")
        for action in subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                callback = cast(_TFuncArgumentDecorator, wrapped)
                callback.parser = action.add_parser(*args, **kwargs)
                callback._groups = {}  # TODO: improve implementation detail
                set_defaults(callback, callback=callback)
                return _callback(callback)

    parser = argument_decorator.parser
    subparsers = parser._subparsers
    return wrapper
