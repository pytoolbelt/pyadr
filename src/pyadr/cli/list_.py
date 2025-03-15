from argparse import Namespace
from pyadr import adr

def configure_parser(subparser) -> None:
    list_parser = subparser.add_parser("list", help="List all the adrs in the project")
    list_parser.add_argument("--reverse", "-r", action="store_true", help="Reverse the order of the list", default=False)
    list_parser.set_defaults(entrypoint=entrypoint)


def entrypoint(cliargs: Namespace) -> int:
    project = adr.Project()
    for adr_ in project.list_adrs(cliargs.reverse):
        print(adr_.filename)
    return 0
