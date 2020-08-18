import argparse
import functools

import wrapt


# ======================
# Registration functions
# ======================

def register(func, /):

    def wrapper(wrapped=None, /, **kwargs):
        return functools.partial(func, **kwargs) if wrapped is None else func(wrapped, **kwargs)

    return wrapper


def _argument_decorator(parser, /):

    def wrapper(wrapped, /):
        parser._groups = {}
        parser.__call__ = wrapped
        return _parse_args(parser)

    return wrapper


# =======================
# Adding argument actions
# =======================

def add_argument(*args, group=None, **kwargs):
    """
    add_argument(dest, ..., name=value, ...)
    add_argument(option_string, option_string, ..., name=value, ...)
    """

    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args, **kwargs,
                                  parent=group)


def add_argument_group(name, /, *args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_argument_group,
                                  *args, **kwargs,
                                  parent=group, child=name)


def add_mutually_exclusive_group(name, /, *args, group=None, **kwargs):
    return _add_container_actions(argparse._ActionsContainer.add_mutually_exclusive_group,
                                  *args, **kwargs,
                                  parent=group, child=name)


def _add_container_actions(add_action, /, *args, parent=None, child=None, **kwargs):

    def wrapper(wrapped, /):
        container = add_action(wrapped if parent is None
                               else wrapped._groups[parent],
                               *args, **kwargs)
        if child is not None:
            wrapped._groups[child] = container
        return wrapped

    return wrapper


@register
def argument_parser(wrapped, /, *, parser_class=argparse.ArgumentParser, description=None, **kwargs):
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - prog -- The name of the program (default: sys.argv[0])
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
    """

    return _argument_decorator(parser_class(description=wrapped.__doc__ if description is None else description, **kwargs))(wrapped)


# ====================================
# Optional/Positional adding functions
# ====================================

@register
def add_subparsers(wrapped, /, **kwargs):
    wrapped.add_subparsers(**kwargs)
    return wrapped


def add_parser(parent, /, name=None, description=None, **kwargs):

    def wrapper(wrapped, /):
        child = next(_argument_decorator(action.add_parser(wrapped.__name__ if name is None else name,
                                                           description=wrapped.__doc__ if description is None else description,
                                                           **kwargs)(wrapped))
                     for action in parent._subparsers._actions
                     if isinstance(action, argparse._SubParsersAction))
        child.set_defaults(callback=wrapped)
        return child

    return wrapper


# =======================================
# Command line argument parsing functions
# =======================================

@wrapt.decorator
def _parse_args(wrapped, instance, args, kwargs, /):

    def wrapper(args=None, namespace=None):
        return wrapped.parse_args(args=args, namespace=namespace)

    namespace = vars(wrapper(*args, **kwargs))
    if (callback := namespace.pop("callback", None)) is None:
        return wrapped(**namespace)
    return callback(**namespace) if instance is None else callback(instance, **namespace)
