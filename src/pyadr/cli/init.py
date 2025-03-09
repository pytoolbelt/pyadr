from argparse import Namespace

def configure_parser(subparser) -> None:
    new_parser = subparser.add_parser("init", help="Init the ADR project in this directory")
    new_parser.set_defaults(entrypoint=entrypoint)


def entrypoint(cliargs: Namespace) -> int:
    print("init", cliargs)
    return 0
