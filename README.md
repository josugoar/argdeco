<p align="center">
  <img src="assets/argdeco.png" alt="argdeco" width="640" height="320" />
</p>

<h1></h1>

> Opinionated **argparse** wrapper

* API breaking change in later versions due to major refactor!!

* Follows the same decorating order as regular **argparse**

* Recommended to install the development version directly from the repository

# Why argdeco?

There are so many libraries out there for writing command line utilities; why does **argdeco** exist?

This question is easy to answer: because there is not a single command line utility for Python out there which ticks the following boxes: ([sound familiar?](https://click.palletsprojects.com/en/7.x/why/))

* is fully typed using official **typeshed** **argparse** stubs

* supports class callback method decoration and method instance binding with class instance forwarding

* supports callback callable instance binding with **argparse** context or parser instance forwarding

* shares the EXACT same API as **argparse** using decorators

# Installation

You can get the library directly from PyPI:

```sh
$ python -m pip install argdeco-josugoar
```

The installation into a [virtualenv](https://github.com/pypa/virtualenv) (or [pipenv](https://github.com/pypa/pipenv)) is heavily recommended.

# API reference

* **argdeco.argument_parser**(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, prefix_chars="-", fromfile_prefix_chars=None, argument_default=None, conflict_handler="error", add_help=True, allow_abbrev=True, exit_on_error=True)

  * Create a new ArgumentParser object. All parameters should be passed as keyword arguments. Each parameter has its own more detailed description below, but in short they are:

      * prog - The name of the program (default: sys.argv[0])

      * usage - The string describing the program usage (default: generated from arguments added to parser)

      * description - Text to display before the argument help (default: __doc__)

      * epilog - Text to display after the argument help (default: none)

      * parents - A list of ArgumentParser objects whose arguments should also be included

      * formatter_class - A class for customizing the help output

      * prefix_chars - The set of characters that prefix optional arguments (default: "-")

      * fromfile_prefix_chars - The set of characters that prefix files from which additional arguments should be read (default: None)

      * argument_default - The global default value for arguments (default: None)

      * conflict_handler - The strategy for resolving conflicting optionals (usually unnecessary)

      * add_help - Add a -h/--help option to the parser (default: True)

      * allow_abbrev - Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)

      * exit_on_error - Determines whether or not ArgumentParser exits with error info when an error occurs. (default: True)

```py
>>> import argdeco
>>> @argdeco.add_argument("--foo", help="foo help")
... @argdeco.argument_parser()
... def parser(foo):
...     pass
...
```

```py
>>> parser(["--help"])
usage: myprogram.py [-h] [--foo FOO]

optional arguments:
 -h, --help  show this help message and exit
 --foo FOO   foo help
```

* **argdeco.add_argument**(name or flags..., group=None, [, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])

  * Define how a single command-line argument should be parsed. Each parameter has its own more detailed description below, but in short they are:

    * name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.

    * group - The group to add the argument. (default: None)

    * action - The basic type of action to be taken when this argument is encountered at the command line.

    * nargs - The number of command-line arguments that should be consumed.

    * const - A constant value required by some action and nargs selections.

    * default - The value produced if the argument is absent from the command line.

    * type - The type to which the command-line argument should be converted.

    * choices - A container of the allowable values for the argument.

    * required - Whether or not the command-line option may be omitted (optionals only).

    * help - A brief description of what the argument does.

    * metavar - A name for the argument in usage messages.

    * dest - The name of the attribute to be added to the object returned by parse_args().

* **argdeco.add_subparsers**([title][, description][, prog][, parser_class][, action][, option_string][, dest][, required][, help][, metavar])

  * Many programs split up their functionality into a number of sub-commands, for example, the svn program can invoke sub-commands like svn checkout, svn update, and svn commit. Splitting up functionality this way can be a particularly good idea when a program performs several different functions which require different kinds of command-line arguments. ArgumentParser supports the creation of such sub-commands with the add_subparsers() method. The add_subparsers() method is normally called with no arguments and returns a special action object. This object has a single method, add_parser(), which takes a command name and any ArgumentParser constructor arguments, and returns an ArgumentParser object that can be modified as usual.

  * Description of parameters:

    * title - title for the sub-parser group in help output; by default “subcommands” if description is provided, otherwise uses title for positional arguments

    * description - description for the sub-parser group in help output, by default None

    * prog - usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument

    * parser_class - class which will be used to create sub-parser instances, by default the class of the current parser (e.g. ArgumentParser)

    * action - the basic type of action to be taken when this argument is encountered at the command line

    * dest - name of the attribute under which sub-command name will be stored; by default None and no value is stored

    * required - Whether or not a subcommand must be provided, by default False (added in 3.7)

    * help - help for sub-parser group in help output, by default None

    * metavar - string presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ..}

```py
>>> # create the top-level parser
>>> @argdeco.add_subparsers(help="sub-command help")
... @argdeco.add_argument("--foo", action="store_true", help="foo help")
... @argdeco.argument_parser(prog="PROG")
... def parser(**kwargs):
...     print("parser")
...     print(kwargs)
...
```

```py
>>> # create the parser for the "a" command
>>> @argdeco.add_argument("bar", type=int, help="bar help")
... @argdeco.add_parser(parser, "a", help="a help")
... def parser_a(**kwargs):
...     print("parser_a")
...     print(kwargs)
...
```

```py
>>> # create the parser for the "b" command
>>> @argdeco.add_argument("--baz", choices="XYZ", help="baz help")
... @argdeco.add_parser(parser, "b", help="b help")
... def parser_b(**kwargs):
...     print("parser_b")
...     print(kwargs)
...
```

```py
>>> # parse some argument lists
>>> parser(["a", "12"])
parser_a
{"foo": False, "bar": 12}
>>> parser(["--foo", "b", "--baz", "Z"])
parser_b
{"foo": True, "baz": "Z"}
```

* **argdeco.add_argument_group**(title=None, description=None)

  * By default, ArgumentParser groups command-line arguments into “positional arguments” and “optional arguments” when displaying help messages. When there is a better conceptual grouping of arguments than this default one, appropriate groups can be created using the add_argument_group() method. The last added argument group in the decorator chain will be the one receiving the subsequently added arguments.

```py
>>> @argdeco.add_argument("bar", help="bar help")
... @argdeco.add_argument("--foo", help="foo help")
... @argdeco.add_argument_group(title="group")
... @argdeco.argument_parser(prog="PROG", add_help=False)
... def parser(**kwargs):
...     pass
...
>>> parser.print_help()
usage: PROG [--foo FOO] bar

group:
  bar    bar help
  --foo FOO  foo help
```

  * Group are defined in order and arguments are added to the last group in the chain.

```py
>>> @argdeco.add_argument("bar2", help="bar help")
... @argdeco.add_argument("--foo2", help="foo help")
... @argdeco.add_argument_group(title="group2")
... @argdeco.add_argument("bar1", help="bar help")
... @argdeco.add_argument("--foo1", help="foo help")
... @argdeco.add_argument_group(title="group1")
... @argdeco.argument_parser(prog="PROG", add_help=False)
... def parser(**kwargs):
...     pass
...
>>> parser.print_help()
usage: PROG [--foo1 FOO1] [--foo2 FOO2] bar1 bar2

group1:
  --foo1 FOO1  foo help
  bar1         bar help

group2:
  --foo2 FOO2  foo help
  bar2         bar help
```

* **ardeco.add_mutually_exclusive_group**(required=False)

```py
>>> @argdeco.add_argument("--bar", action="store_false")
... @argdeco.add_argument("--foo", action="store_true")
... @argdeco.add_mutually_exclusive_group()
... @argdeco.argument_parser(prog="PROG")
... def parser(**kwargs):
...     print(kwargs)
...
>>> parser(["--foo"])
{"foo": True, "bar": True}
>>> parser(["--bar"])
{"foo": False, "bar": False}
>>> parser(["--foo", "--bar"])
usage: PROG [-h] [--foo | --bar]
PROG: error: argument --bar: not allowed with argument --foo
```

# Advanced usage

## Accessing attributes

**argdeco** makes it so that each decorated function is converted to an **argparse** parser, so that further customization can be achieved by calling the proper original methods.

```py
>>> @argdeco.argument_parser()
... def prog(self):
...     pass
...
>>> prog.__wrapped__
<function prog at 0x0000029BCBFABF70>
>>> prog
_ArgumentParser(prog="argdeco.py", usage=None, description=None, formatter_class=<class "argparse.HelpFormatter">, conflict_handler="error", add_help=True)
```

## Class method decoration

argdeco supports class callback method decoration, unlike the big majority of CLI decorator libraries, without any difference as regular callback callable decoration.

```py
>>> class Prog:
...
...     @argdeco.argument_parser()
...     def parser(self):
...         pass
...
```

Decorating a class will forward the arguments to the *\_\_init__* method (usually not the desired behaviour), as decorated callbacks will ALWAYS be treated as callables.

```py
>>> @argdeco.argument_parser()
... class Prog:
...     pass
...
```

Decorating the *\_\_call__* method will forward the arguments to the class itself.

```py
>>> class Prog:
...
...     @argdeco.argument_parser()
...     def __call__(self):
...         pass
...
```

## Context forwarding

Decorated callback callables can get access to the **argparse** context or parser instance.

```py
>>> @argdeco.argument_parser(prog="PROG")
... def parser():
...     parser.print_help()
...
>>> parser([])
usage: PROG [-h]

optional arguments:
  -h, --help  show this help message and exit
```

Class callback method context or parser instance forwarding is still respected on decorated class methods.

```py
>>> class Prog:
...
...     @argdeco.argument_parser(prog="PROG")
...     def __call__(self):
...         Prog.__call__.print_help()
...
>>> prog = Prog()
>>> prog([])
usage: PROG [-h]

optional arguments:
  -h, --help  show this help message and exit
```
