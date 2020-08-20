import argparse
import functools
import types

import wrapt


class ArgumentDecorator(wrapt.ObjectProxy):

    def __init__(self,
                 callback, /, *,
                 wrapped=argparse.ArgumentParser(),
                 ctx=False):
        super().__init__(wrapped)
        self.callback = callback
        self._self_ctx = ctx
        self._self_groups = {}

    @property
    def _groups(self, /):
        return self._self_groups

    @wrapt.decorator
    def wrapper(self, wrapped, instance, args, kwargs, /):
        namespace = vars(self.parse_args(*args, **kwargs))
        subcommand = namespace.pop("subcommand", None)
        if subcommand is None:
            callback = wrapped
        else:
            callback = types.MethodType(subcommand, instance)
        if self._self_ctx:
            callback = types.MethodType(callback, self.__wrapped__)
        return callback(**namespace)

    def __get__(self, instance, owner=None, /):
        if instance is not None:
            self.callback = types.MethodType(self.callback, instance)
        return self

    def __call__(self, /, *args, **kwargs):
        return self.wrapper(self.callback)(*args, *kwargs)


def add_argument(*args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args,
                                  parent=group,
                                  **kwargs)


def add_argument_group(name, /, *args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument_group,
                                  *args,
                                  parent=group,
                                  child=name,
                                  title=kwargs.pop("title", name),
                                  **kwargs)


def add_mutually_exclusive_group(name, /, *, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group,
                                  parent=group,
                                  child=name,
                                  **kwargs)


def _add_container_actions(func, /, *args, parent=None, child=None, **kwargs):

    def wrapper(wrapped, /):
        instance = wrapped if parent is None else wrapped._groups[parent]
        container = func(instance, *args, **kwargs)
        if child is not None:
            wrapped._groups[child] = container
        return wrapped

    return wrapper


def argument_parser(wrapped=None, /, *,
                    parser_class=argparse.ArgumentParser,
                    ctx=False,
                    **kwargs):
    if wrapped is None:
        return functools.partial(argument_parser,
                                 parser_class=parser_class,
                                 ctx=ctx,
                                 **kwargs)
    kwargs.setdefault("description", wrapped.__doc__)
    parser = parser_class(**kwargs)
    return ArgumentDecorator(wrapped, wrapped=parser, ctx=ctx)


def add_subparsers(wrapped=None, /, **kwargs):
    kwargs.setdefault("parser_class", wrapped.__class__)
    wrapper = _add_container_actions(argparse.ArgumentParser.add_subparsers,
                                     **kwargs)
    return wrapper if wrapped is None else wrapper(wrapped)


def add_parser(parent, /, name=None, ctx=False, **kwargs):

    def wrapper(wrapped, /):
        name_ = wrapped.__name__ if name is None else name
        kwargs.setdefault("description", wrapped.__doc__)
        for action in parent._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                parser = action.add_parser(name_, **kwargs)
                child = ArgumentDecorator(wrapped, wrapped=parser, ctx=ctx)
                child.set_defaults(subcommand=wrapped)
                return child

    return wrapper
