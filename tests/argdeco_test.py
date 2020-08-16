import argparse
import argdeco


# @argdeco.add_subparsers
# @argdeco.argument_parser
# class Uci:

#     @argdeco.add_argument("--value")
#     @argdeco.add_argument("--name", required=True)
#     @argdeco.add_argument(Uci, "setoption")
#     def setoption(self, name, value):
#         print(name, value)


# if __name__ == "__main__":
#     Uci()("--name JoshGoA --value HelloWorld".split())


@argdeco.add_subparsers(title="my_title")
@argdeco.argument_parser
def cli():
    pass


@argdeco.add_argument("--hello")
@argdeco.add_parser(cli, "subcommand")
def subcommand(hello):
    print(hello)


# cli._namespace.parser.print_help()
cli(["subcommand", "--hello", "world"])
