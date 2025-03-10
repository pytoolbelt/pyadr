from argparse import Namespace
from pyadr import project


def configure_parser(subparser) -> None:
    new_parser = subparser.add_parser("new", help="Create a new ADR")
    new_parser.add_argument("--supersede", "-s", type=int, help="Supersede the ADR")
    new_parser.add_argument("title", help="Title of the ADR")
    new_parser.set_defaults(entrypoint=entrypoint)


def entrypoint(cliargs: Namespace) -> int:
    proj = project.Project()

    ard = proj.get_next_adr(cliargs.title)
    template = project.TemplateLoader().load(name="new", number=ard.index.index_as_str, title=ard.title)
    with ard.path.open("w") as f:
        f.write(template)
    return 0
