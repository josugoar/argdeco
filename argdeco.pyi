import argparse
from argparse import (_N, _SUPPRESS_T, _T, Action, FileType, Namespace,
                      _ActionsContainer, _ArgumentParserT, _FormatterClass,
                      _NArgsStr, _SubParsersAction)
from typing import Any, Callable, Iterable, Sequence, TypeVar, overload

_R = TypeVar("_R")


class ArgumentParser(argparse.ArgumentParser):

    __wrapped__: Callable[..., _R]
    container: _ActionsContainer
    subparsers: _SubParsersAction | None

    def __init__(
        self,
        wrapped: Callable,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[_ArgumentParserT] = [],
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
    ) -> _R: ...

    @overload
    def __call__(
        self,
        args: Sequence[str] | None,
        namespace: _N
    ) -> _R: ...

    @overload
    def __call__(
        self,
        *,
        namespace: _N
    ) -> _R: ...


def argument_parser(
    prog: str | None = None,
    usage: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
    parents: Sequence[_ArgumentParserT] = [],
    formatter_class: _FormatterClass = ...,
    prefix_chars: str = "-",
    fromfile_prefix_chars: str | None = None,
    argument_default: Any = None,
    conflict_handler: str = "error",
    add_help: bool = True,
    allow_abbrev: bool = True,
    exit_on_error: bool = True,
) -> Callable[[Callable], ArgumentParser]: ...


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
) -> Callable[[ArgumentParser], ArgumentParser]: ...


def add_argument_group(
    title: str | None = None,
    description: str | None = None,
    *,
    prefix_chars: str = ...,
    argument_default: Any = ...,
    conflict_handler: str = ...,
) -> Callable[[ArgumentParser], ArgumentParser]: ...


def add_mutually_exclusive_group(
    *,
    required: bool = False
) -> Callable[[ArgumentParser], ArgumentParser]: ...


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
) -> Callable[[ArgumentParser], ArgumentParser]: ...


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
) -> Callable[[ArgumentParser], ArgumentParser]: ...


def add_parser(
    parser,
    name: str | None,
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
) -> Callable[[ArgumentParser], ArgumentParser]: ...
