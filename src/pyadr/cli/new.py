from argparse import Namespace
from pyadr import project

def configure_parser(subparser) -> None:
    new_parser = subparser.add_parser("new", help="Create a new ADR")
    new_parser.add_argument("--supersede", "-s", type=int, help="Supersede the ADR")
    new_parser.set_defaults(entrypoint=entrypoint)


def entrypoint(cliargs: Namespace) -> int:
    p = project.Project()
    a = p.get_next_adr("New ADR")
    a.touch()
    return 0
