import argparse

import wrapt


@wrapt.decorator
def _callback(wrapped, instance, args, kwargs, /):

    def wrapper(*, parse_func=argparse.ArgumentParser.parse_args):
        return parse_func

    # CHECK IF _NAMESPACE EXISTS
    namespace = vars(wrapper(**kwargs)(wrapped._namespace.parser, *args))
    if (callback := namespace.pop("callback", None)) is None:
        return wrapped(**namespace)
    if instance is None:
        return callback(**namespace)
    return callback(instance, **namespace)


def argument_parser(wrapped=None, /, *, cls=argparse.ArgumentParser, **kwargs):
    if wrapped is None:
        return functools.partial(argument_parser, cls=cls, **kwargs)
    wrapped._namespace = argparse.Namespace(parser=cls(**kwargs), title_group_map={})
    return _callback(wrapped)


def _add_container(add_func, /, *args, name=None, group=None, **kwargs):

    def wrapper(wrapped, /):
        # CHECK IF _NAMESPACE EXISTS
        if (container := wrapped._namespace.parser if group is None
                         else wrapped._namespace.title_group_map.get(group, None)) is None:
            raise ValueError(f"unknown group {group}")
        container = add_func(container, *args, **kwargs)
        if name is not None:
            wrapped._namespace.title_group_map[name] = container
        return wrapped

    return wrapper


def add_argument(*args, group=None, **kwargs):
    return _add_container(argparse._ActionsContainer.add_argument,
                          *args, **kwargs,
                          group=group)


def add_argument_group(name, /, *args, group=None, **kwargs):
    return _add_container(argparse._ActionsContainer.add_argument_group,
                          *args, **kwargs,
                          name=name,
                          group=group)


def add_mutually_exclusive_group(name, /, *args, group=None, **kwargs):
    return _add_container(argparse._ActionsContainer.add_mutually_exclusive_group,
                          *args, **kwargs,
                          name=name,
                          group=group)


def add_subparsers(wrapped=None, /, **kwargs):
    if wrapped is None:
        return functools.partial(add_subparsers, **kwargs)
    # CHECK IF _NAMESPACE EXISTS
    wrapped._namespace.parser.add_subparsers(**kwargs)
    return wrapped


def add_parser(callback, /, *args, **kwargs):

    def wrapper(wrapped, /):
        for action in callback._namespace.parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                wrapped._namespace = argparse.Namespace(parser=action.add_parser(*args, **kwargs), title_group_map={})
                callback._namespace.parser.set_defaults(callback=wrapped)
                return _callback(wrapped)

    # CHECK IF _NAMESPACE EXISTS
    if callback._namespace.parser._subparsers is None:
        callback._namespace.parser.error("unknown subparser arguments")
    return wrapper
