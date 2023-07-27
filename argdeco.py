import argparse


def argument_parser(prog=None,
                    usage=None,
                    description=None,
                    epilog=None,
                    parents=[],
                    formatter_class=argparse.HelpFormatter,
                    prefix_chars='-',
                    fromfile_prefix_chars=None,
                    argument_default=None,
                    conflict_handler='error',
                    add_help=True,
                    allow_abbrev=True,
                    exit_on_error=True):

    def wrapper(wrapped):
        return _ArgumentParser(wrapped=wrapped,
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

    def wrapper(wrapped):
        kwargs.setdefault("description", wrapped.__doc__)
        wrapped._container.add_argument(*args, **kwargs)
        return wrapped

    return wrapper


def add_argument_group(*args, **kwargs):

    def wrapper(wrapped):
        wrapped._container = wrapped.add_argument_group(*args, **kwargs)
        return wrapped

    return wrapper


def add_mutully_exclusive_argument_group(**kwargs):

    def wrapper(wrapped):
        wrapped._container = wrapped.add_mutully_exclusive_argument_group(
            **kwargs)
        return wrapped

    return wrapper


def add_subparsers(**kwargs):

    def wrapper(wrapped):
        wrapped._subparser = wrapped.add_subparsers(**kwargs)
        return wrapped

    return wrapper


def add_parser(parser, name, **kwargs):

    def wrapper(wrapped):
        return parser._subparser.add_parser(name, wrapped=wrapped, **kwargs)

    return wrapper


class _ArgumentParser(argparse.ArgumentParser):

    def __init__(self,
                 *,
                 wrapped,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
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

        self._wrapped = wrapped

        self._actions_container = self
        self._subparsers_action = None

    def __call__(self, args=None, namespace=None):
        return self._wrapped(**vars(self.parse_args(args=args, namespace=namespace)))
