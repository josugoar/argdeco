# Author: josugoar.

"""Command-line parsing library

This module is an argparse-inspired command-line parsing library that:

    - handles both optional and positional arguments
    - produces highly informative usage messages
    - supports parsers that dispatch to sub-parsers

The following is a simple usage example that sums integers from the
command-line and writes the result to a file::

    @argdeco.add_argument(
        "--log", default=sys.stdout, type=argparse.FileType("w"),
        help="the file where the sum should be written")
    @argdeco.add_argument(
        "integers", metavar="int", nargs="+", type=int,
        help="an integer to be summed")
    @argdeco.argument_parser(
        description="sum the integers at the command line")
    def parser(integers, log):
        log.write("%s" % sum(args.integers))
        log.close()
"""

__version__ = "1.6"
__all__ = [
    "ArgumentParser",
    "argument_parser",
    "add_argument",
    "add_argument_group",
    "add_mutually_exclusive_group",
    "add_subparsers",
    "add_parser",
]


import argparse
import types


class ArgumentParser(argparse.ArgumentParser):

    def __init__(self,
                 wrapped,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars="-",
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler="error",
                 add_help=True,
                 allow_abbrev=True,
                 exit_on_error=True):
        super().__init__(prog=prog,
                         usage=usage,
                         description=description,
                         epilog=epilog,
                         parents=parents,
                         formatter_class=formatter_class,
                         prefix_chars=prefix_chars,
                         fromfile_prefix_chars=fromfile_prefix_chars,
                         argument_default=argument_default,
                         conflict_handler=conflict_handler,
                         add_help=add_help,
                         allow_abbrev=allow_abbrev,
                         exit_on_error=exit_on_error)
        self.__wrapped__ = wrapped
        self.container = self
        self.subparsers = None

    def __call__(self, args=None, namespace=None):
        return self.__wrapped__(**vars(self.parse_args(args=args, namespace=namespace)))

    def __get__(self, instance, _):
        if instance is not None:
            self.__wrapped__ = types.MethodType(self.__wrapped__, instance)
        return self


def argument_parser(prog=None,
                    usage=None,
                    description=None,
                    epilog=None,
                    parents=[],
                    formatter_class=argparse.HelpFormatter,
                    prefix_chars="-",
                    fromfile_prefix_chars=None,
                    argument_default=None,
                    conflict_handler="error",
                    add_help=True,
                    allow_abbrev=True,
                    exit_on_error=True):
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
        - exit_on_error -- Determines whether or not ArgumentParser exits with
            error info when an error occurs
    """

    def wrapper(wrapped):
        nonlocal description
        if description is None:
            description = wrapped.__doc__
        return ArgumentParser(wrapped,
                              prog=prog,
                              usage=usage,
                              description=description,
                              epilog=epilog,
                              parents=parents,
                              formatter_class=formatter_class,
                              prefix_chars=prefix_chars,
                              fromfile_prefix_chars=fromfile_prefix_chars,
                              argument_default=argument_default,
                              conflict_handler=conflict_handler,
                              add_help=add_help,
                              allow_abbrev=allow_abbrev,
                              exit_on_error=exit_on_error)

    return wrapper


def add_argument(*args, **kwargs):
    """
    add_argument(dest, ..., name=value, ...)
    add_argument(option_string, option_string, ..., name=value, ...)
    """

    def wrapper(wrapped):
        wrapped.container.add_argument(*args, **kwargs)
        return wrapped

    return wrapper


def add_argument_group(*args, **kwargs):

    def wrapper(wrapped):
        wrapped.container = wrapped.add_argument_group(*args, **kwargs)
        return wrapped

    return wrapper


def add_mutually_exclusive_group(**kwargs):

    def wrapper(wrapped):
        wrapped.container = wrapped.add_mutually_exclusive_group(**kwargs)
        return wrapped

    return wrapper


def add_subparsers(**kwargs):

    def wrapper(wrapped):
        wrapped.subparsers = wrapped.add_subparsers(**kwargs)
        return wrapped

    return wrapper


def add_parser(parser, name=None, **kwargs):

    def wrapper(wrapped):
        nonlocal name
        if name is None:
            name = wrapped.__name__
        kwargs.setdefault("description", wrapped.__doc__)
        return parser.subparsers.add_parser(name, wrapped=wrapped, **kwargs)

    return wrapper
