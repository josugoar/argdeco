import argparse
import functools

import wrapt


def _callback(wrapped, /, *, func):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs, /):

        def parse_args(args=None, namespace=None):
            return wrapped.parse_args(
                args=args,
                namespace=namespace
            )

        namespace = vars(parse_args(*args, **kwargs))
        subcommand = namespace.pop("subcommand", None)
        if subcommand is None:
            return func(**namespace)
        return subcommand(**namespace) if instance is None \
            else subcommand(instance, **namespace)

    wrapped.func = func
    wrapped._groups = {}
    return wrapper(wrapped)


def add_argument(*args, group=None, **kwargs):
    return _add_container_actions(
        argparse._ActionsContainer.add_argument,
        *args,
        parent=group,
        **kwargs
    )


def add_argument_group(name, /, *args, group=None, **kwargs):
    return _add_container_actions(
        argparse._ActionsContainer.add_argument_group,
        *args,
        parent=group,
        child=name,
        title=kwargs.pop("title", name),
        **kwargs
    )


def add_mutually_exclusive_group(name, /, *, group=None, **kwargs):
    return _add_container_actions(
        argparse._ActionsContainer.add_mutually_exclusive_group,
        parent=group,
        child=name,
        **kwargs
    )


def _add_container_actions(func, /, *args, parent=None, child=None, **kwargs):

    def wrapper(wrapped, /):
        container = func(
            wrapped if parent is None else wrapped._groups[parent],
            *args, **kwargs
        )
        if child is not None:
            wrapped._groups[child] = container
        return wrapped

    return wrapper


def argument_parser(wrapped=None, /, *, parser_class=argparse.ArgumentParser, **kwargs):
    if wrapped is None:
        return functools.partial(
            argument_parser,
            parser_class=parser_class,
            **kwargs
        )
    parser = parser_class(
        description=kwargs.pop("description", wrapped.__doc__),
        **kwargs
    )
    return _callback(parser, func=wrapped)


def add_subparsers(wrapped=None, /, **kwargs):
    wrapper = _add_container_actions(
        argparse.ArgumentParser.add_subparsers,
        parser_class=kwargs.pop("parser_class", wrapped.__class__),
        **kwargs
    )
    return wrapper if wrapped is None else wrapper(wrapped)


def add_parser(parent, /, name=None, **kwargs):

    def wrapper(wrapped, /):
        for action in parent._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                parser = action.add_parser(
                    wrapped.__name__ if name is None else name,
                    description=kwargs.pop("description", wrapped.__doc__),
                    **kwargs
                )
                child = _callback(parser, func=wrapper)
                child.set_defaults(subcommand=wrapped)
                return child

    return wrapper
