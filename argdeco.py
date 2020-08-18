import argparse
import functools

import wrapt


def with_optional_arguments(func, /):

    def wrapper(wrapped=None, /, **kwargs):
        return functools.partial(func, **kwargs) if wrapped is None else func(wrapped, **kwargs)

    return wrapper


def _argument_decorator(parser, /):

    def wrapper(wrapped, /):
        parser._groups = {}
        parser.__call__ = wrapped
        return _parse_args(parser)  # pylint: disable=E1120

    return wrapper


def add_argument(*args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument, *args, parent=group, **kwargs)


def add_argument_group(name, /, *args, group=None, title=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument_group, *args, parent=group, child=name, title=name if title is None else title, **kwargs)


def add_mutually_exclusive_group(name, /, *args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group, *args, parent=group, child=name, **kwargs)


def _add_container_actions(add_action, /, *args, parent=None, child=None, **kwargs):

    def wrapper(wrapped, /):
        container = add_action(wrapped if parent is None else wrapped._groups[parent],
                               *args, **kwargs)
        if child is not None:
            wrapped._groups[child] = container
        return wrapped

    return wrapper


@with_optional_arguments
def argument_parser(wrapped, /, *, parser_class=argparse.ArgumentParser, description=None, **kwargs):
    return _argument_decorator(parser_class(description=wrapped.__doc__ if description is None else description, **kwargs))(wrapped)


@with_optional_arguments
def add_subparsers(wrapped, /, **kwargs):
    wrapped.add_subparsers(**kwargs)
    return wrapped


def add_parser(parent, /, name=None, description=None, **kwargs):

    def wrapper(wrapped, /):
        (child := next(_argument_decorator(action.add_parser(wrapped.__name__ if name is None else name, description=wrapped.__doc__ if description is None else description, **kwargs))(wrapped)
                       for action in parent._subparsers._actions if isinstance(action, argparse._SubParsersAction))).set_defaults(callback=wrapped)
        return child

    return wrapper


@wrapt.decorator
def _parse_args(wrapped, instance, args, kwargs, /):

    def wrapper(args=None, namespace=None):
        return wrapped.parse_args(args=args, namespace=namespace)

    namespace = vars(wrapper(*args, **kwargs))
    if (callback := namespace.pop("callback", None)) is None:
        return wrapped(**namespace)
    return callback(**namespace) if instance is None else callback(instance, **namespace)
