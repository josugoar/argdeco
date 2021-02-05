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
    """Define how a single command-line argument should be parsed.

    Args:
        name or flags: Either a name or a list of option strings, e.g. foo or -f, --foo.
        group (optional): The group to add the argument. Defaults to None.
        action (optional): The basic type of action to be taken when this argument is encountered at the command line.
        nargs (optional): The number of command-line arguments that should be consumed.
        const (optional): A constant value required by some action and nargs selections.
        default (optional): The value produced if the argument is absent from the command line.
        type (optional): The type to which the command-line argument should be converted.
        choices (optional): A container of the allowable values for the argument.
        required (optional): Whether or not the command-line option may be omitted (optionals only).
        help (optional): A brief description of what the argument does.
        metavar (optional): A name for the argument in usage messages.
        dest (optional): The name of the attribute to be added to the object returned by parse_args().
    """
    return _add_container_actions(argparse._ActionsContainer.add_argument,
                                  *args, parent=group, **kwargs)


def add_argument_group(name, /, *args, group=None, **kwargs):
    """
    By default, ArgumentParser groups command-line arguments into “positional
    arguments” and “optional arguments” when displaying help messages. When there
    is a better conceptual grouping of arguments than this default one, appropriate
    groups can be created using the add_argument_group() method.
    """
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
    """Create a new ArgumentParser object. All parameters should be passed as keyword arguments.

    Args:
        wrapped: The callback callable. Defaults to None.
        parser_class (optional): The class to instantiate the parser. Defaults to argparse.ArgumentParser.
        ctx (optional): Pass the **argparse** context or parser instance to the callback callable. Defaults to False
        prog (optional): The name of the program. Defaults to sys.argv[0].
        usage (optional): The string describing the program usage. Generated from arguments added to parser.
        description (optional): Text to display before the argument help. Defaults to __doc__.
        epilog (optional): Text to display after the argument help. Defaults to none.
        parents (optional): A list of ArgumentParser objects whose arguments should also be included
        formatter_class (optional): A class for customizing the help output
        prefix_chars (optional): The set of characters that prefix optional arguments. Defaults to "-".
        fromfile_prefix_chars (optional): The set of characters that prefix files from which additional arguments should be read. Defaults to None.
        argument_default (optional): The global default value for arguments. Defaults to None.
        conflict_handler (optional): The strategy for resolving conflicting optionals (usually unnecessary)
        add_help (optional): Add a -h/--help option to the parser. Defaults to True.
        allow_abbrev (optional): Allows long options to be abbreviated if the abbreviation is unambiguous. Defaults to True.
    """
    if wrapped is None:
        return functools.partial(argument_parser, parser_class=parser_class,
                                 ctx=ctx, **kwargs)
    kwargs.setdefault("description", wrapped.__doc__)
    parser = parser_class(**kwargs)
    return ArgumentDecorator(wrapped, parser=parser, ctx=ctx)


def add_subparsers(wrapped=None, /, **kwargs):
    """
    Many programs split up their functionality into a number of sub-commands,
    for example, the svn program can invoke sub-commands like svn checkout,
    svn update, and svn commit. Splitting up functionality this way can be a
    particularly good idea when a program performs several different functions
    which require different kinds of command-line arguments. ArgumentParser
    supports the creation of such sub-commands with the add_subparsers() method.
    The add_subparsers() method is normally called with no arguments and returns
    a special action object. This object has a single method, add_parser(), which
    takes a command name and any ArgumentParser constructor arguments, and
    returns an ArgumentParser object that can be modified as usual.

    Args:
        wrapped: The callback callable. Defaults to None.
        title (optional): title for the sub-parser group in help output; by default “subcommands” if description is provided, otherwise uses title for positional arguments.
        description (optional): description for the sub-parser group in help output, by default None.
        prog (optional): usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument.
        parser_class (optional): class which will be used to create sub-parser instances, by default the class of the current parser (e.g. ArgumentParser).
        action (optional): the basic type of action to be taken when this argument is encountered at the command line.
        dest (optional): name of the attribute under which sub-command name will be stored; by default None and no value is stored.
        required (optional): Whether or not a subcommand must be provided, by default False (added in 3.7).
        help (optional): help for sub-parser group in help output, by default None.
        metavar (optional): string presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ..}.
    """
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
