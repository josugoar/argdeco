from argparse import (_N, _SUPPRESS_T, _T, Action, ArgumentParser, FileType,
                      Namespace, _ActionsContainer, _ActionStr,
                      _ArgumentParserT, _FormatterClass, _NArgsStr,
                      _SubParsersAction)
from collections.abc import Sequence
from typing import Any, Callable, Iterable, Sequence, overload


def argument_parser(
    prog: str | None = None,
    usage: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
    parents: Sequence[ArgumentParser] = [],
    formatter_class: _FormatterClass = ...,
    prefix_chars: str = "-",
    fromfile_prefix_chars: str | None = None,
    argument_default: Any = None,
    conflict_handler: str = "error",
    add_help: bool = True,
    allow_abbrev: bool = True,
    exit_on_error: bool = True,
) -> Callable[[Callable], _ArgumentParser]: ...


def add_argument(
    *name_or_flags: str,
    action: _ActionStr | type[Action] = ...,
    nargs: int | _NArgsStr | _SUPPRESS_T = ...,
    const: Any = ...,
    default: Any = ...,
    type: Callable[[str], _T] | FileType = ...,
    choices: Iterable[_T] | None = ...,
    required: bool = ...,
    help: str | None = ...,
    metavar: str | tuple[str, ...] | None = ...,
    dest: str | None = ...,
    version: str = ...,
    **kwargs: Any,
) -> Callable[[Callable], _ArgumentParser]: ...


def add_argument_group(
    title: str | None = None,
    description: str | None = None,
    *,
    prefix_chars: str = ...,
    argument_default: Any = ...,
    conflict_handler: str = ...,
) -> Callable[[Callable], _ArgumentParser]: ...


def add_mutually_exclusive_group(
    *,
    required: bool = False
) -> Callable[[Callable], _ArgumentParser]: ...


@overload
def add_subparsers(
    *,
    title: str = ...,
    description: str | None = ...,
    prog: str = ...,
    action: type[Action] = ...,
    option_string: str = ...,
    dest: str | None = ...,
    required: bool = ...,
    help: str | None = ...,
    metavar: str | None = ...,
) -> Callable[[Callable], _ArgumentParser]: ...


@overload
def add_subparsers(
    *,
    title: str = ...,
    description: str | None = ...,
    prog: str = ...,
    parser_class: type[_ArgumentParserT],
    action: type[Action] = ...,
    option_string: str = ...,
    dest: str | None = ...,
    required: bool = ...,
    help: str | None = ...,
    metavar: str | None = ...,
) -> Callable[[Callable], _ArgumentParser]: ...


def add_parser(
    parser,
    name: str,
    *,
    help: str | None = ...,
    aliases: Sequence[str] = ...,
    prog: str | None = ...,
    usage: str | None = ...,
    description: str | None = ...,
    epilog: str | None = ...,
    parents: Sequence[_ArgumentParserT] = ...,
    formatter_class: _FormatterClass = ...,
    prefix_chars: str = ...,
    fromfile_prefix_chars: str | None = ...,
    argument_default: Any = ...,
    conflict_handler: str = ...,
    add_help: bool = ...,
    allow_abbrev: bool = ...,
    exit_on_error: bool = ...,
) -> Callable[[Callable], _ArgumentParser]: ...


class _ArgumentParser(ArgumentParser):

    _wrapped: Callable
    _actions_container: _ActionsContainer
    _subparsers_action: _SubParsersAction | None

    def __init__(
        self,
        *,
        wrapped: Callable,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = [],
        formatter_class: _FormatterClass = ...,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: Any = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
    ) -> None: ...

    @overload
    def __call__(
        self,
        args: Sequence[str] | None = None,
        namespace: Namespace | None = None
    ): ...

    @overload
    def __call__(
        self,
        args: Sequence[str] | None,
        namespace: _N
    ): ...

    @overload
    def __call__(
        self,
        *,
        namespace: _N
    ): ...
