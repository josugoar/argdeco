import argparse
import functools
import types

import wrapt


class ArgumentDecorator(wrapt.FunctionWrapper):

    def __init__(self, /, wrapped, enabled=None, *,
                 parser=argparse.ArgumentParser(), ctx=False):
        super().__init__(wrapped, self.wrapper, enabled)
        self.parser = parser
        self._containers = {}
        self._self_ctx = ctx

    def wrapper(self, wrapped, instance, args, kwargs, /):
        namespace = vars(self.parser.parse_args(*args, **kwargs))
        default = namespace.pop("default", None)
        if default is not None:
            wrapped = types.MethodType(default, instance)
        if self._self_ctx:
            wrapped = types.MethodType(wrapped, self.parser)
        return wrapped(**namespace)


def add_argument(*args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args, parent=group, **kwargs)


def add_argument_group(name, /, *args, group=None, **kwargs):
    kwargs.setdefault("title", name)
    return _add_container_actions(argparse._ActionsContainer.add_argument_group,
                                  *args, parent=group, child=name, **kwargs)


def add_mutually_exclusive_group(name, /, *, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group,
                                  parent=group, child=name, **kwargs)


def _add_container_actions(add, /, *args, parent=None, child=None, **kwargs):

    def wrapper(wrapped, /):
        instance = wrapped.parser if parent is None else wrapped._containers[parent]
        container = add(instance, *args, **kwargs)
        if child is not None:
            wrapped._containers[child] = container
        return wrapped

    return wrapper


def argument_parser(wrapped=None, /, *, parser_class=argparse.ArgumentParser,
                    ctx=False, **kwargs):
    if wrapped is None:
        return functools.partial(argument_parser, parser_class=parser_class,
                                 ctx=ctx, **kwargs)
    kwargs.setdefault("description", wrapped.__doc__)
    parser = parser_class(**kwargs)
    return ArgumentDecorator(wrapped, parser=parser, ctx=ctx)


def add_subparsers(wrapped=None, /, **kwargs):
    if wrapped is None:
        return functools.partial(add_subparsers, **kwargs)
    kwargs.setdefault("parser_class", wrapped.parser.__class__)
    wrapper = _add_container_actions(argparse.ArgumentParser.add_subparsers,
                                     **kwargs)
    return wrapper(wrapped)


def add_parser(parent, /, name=None, ctx=False, **kwargs):

    def wrapper(wrapped, /):
        subcommand = wrapped.__name__ if name is None else name
        kwargs.setdefault("description", wrapped.__doc__)
        for action in parent.parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                parser = action.add_parser(subcommand, **kwargs)
                child = ArgumentDecorator(wrapped, ctx=ctx, parser=parser)
                parser.set_defaults(default=wrapped)
                return child

    return wrapper
