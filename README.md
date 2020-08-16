# argdeco

> Stylish Decorator Syntax For Argparse

**argdeco** is just another **argparse** decorator syntactic sugar. It is heavily inspired by [**argparse-deco**](https://github.com/zaehlwerk/argparse-deco), but tries to solve the problems of many CLI libraries.

## API

```py
>>> import argdeco
```

* **argdeco.argument_parser**

Add necessary parser metadata to given callable.

```py
>>> @argdeco.argument_parser
... def cli():
...     pass
```

The parser class and instance can be modified via the optional *cls* and *kwargs* parameters.

```py
>>> @argdeco.argument_parser(cls=argparse.ArgumentParser, prog="cli")
... def cli():
...     pass
```

Calling the decorated function will start the parsing process, depending on the given optional *parse_func*.
```py
>>> cli(["--cli"], parse_func=argparse.ArgumentParser.parse_args)
usage: cli [-h]
cli: error: unrecognized arguments: --cli
```

* **argdeco.add_argument**

Add given argument to **argdeco** decorated callable.

```py
>>> @argdeco.add_argument("--cli", action="store_true")
... @argdeco.argument_parser
... def cli(cli):
...     print(cli)
```

Arguments are passed via *kwargs* to the callback callable.

```py
>>> cli(["--cli"])
True
```

Arguments belonging to a group must be specified using the *group* optional parameter.

* **argdeco.add_argument_group**

Add given argument group to **argdeco** decorated callable.

```py
>>> @argdeco.add_argument("--cli", group="prog", action="store_true")
... @argdeco.add_argument("--hello", group="prog")
... @argdeco.add_argument_group("prog", title="prog")
... @argdeco.argument_parser
... def cli(cli, hello):
...     print(cli, hello)
```

* **argdeco.add_mutually_exclusive_group**

Add given mutually exclusive group to **argdeco** decorated callable.

```py
>>> @argdeco.add_argument("--cli", group="prog", action="store_true")
... @argdeco.add_argument("--hello", group="prog")
... @argdeco.add_mutually_exclusive_group("prog")
... @argdeco.argument_parser
... def cli(cli, hello):
...     print(cli, hello)
```

```py
>>> cli(["--cli", "--hello", "world"])
usage: argdeco_test.py [-h] [--hello HELLO | --cli]
argdeco_test.py: error: argument --hello: not allowed with argument --cli
```

* **argdeco.add_subparsers**

Register subparsers of **argdeco** decorated callable.

```py
>>> @argdeco.add_subparsers
... @argdeco.argument_parser
... def cli(cli, hello):
...     print(cli, hello)
```

The parser instance can be modified via the optional *kwargs* parameters.

```py
>>> @argdeco.add_subparsers(title="my_title")
... @argdeco.argument_parser
... def cli(cli, hello):
...     print(cli, hello)
```

* **argdeco.add_parser**

Add parser to registered callback subparsers and make decorated callable a parser callback.

```py
>>> @argdeco.add_subparsers(title="my_title")
... @argdeco.argument_parser
... def cli():
...     pass
```

```py
>>> @argdeco.add_argument("--hello")
... @argdeco.add_parser(cli, "subcommand")
... def subcommand(hello):
...     print(hello)
```

```py
>>> cli(["subcommand", "--hello", "world"])
world
```
