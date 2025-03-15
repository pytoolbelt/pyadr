import re
from argparse import Namespace, Action
from pyadr import adr
from pyadr.error_handling.exceptions import PyadrError

class FormatSupersede(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pattern = re.compile(r"^\d{4}$")
        if not pattern.match(values):
            raise PyadrError("Supersede must be a 4 digit number")
        setattr(namespace, "supersede", values.zfill(4))



def configure_parser(subparser) -> None:
    new_parser = subparser.add_parser("new", help="Create a new ADR")
    new_parser.add_argument("--supersede", "-s", type=str, action=FormatSupersede, help="Supersede the ADR")
    new_parser.add_argument("title", help="Title of the ADR", nargs="+")
    new_parser.set_defaults(entrypoint=entrypoint)


def entrypoint(cliargs: Namespace) -> int:
    project = adr.Project()
    number = project.next_number()
    title = " ".join(cliargs.title)
    new_adr = adr.Adr(number, title, adr.AdrStatus.PROPOSED)
    template_loader = adr.TemplateLoader()

    if cliargs.supersede:
        old_adr = project.get_adr(cliargs.supersede)
        old_adr.superseded_adr = new_adr
        old_adr.status = adr.AdrStatus.SUPERSEDED
        new_adr.supersedes_adr = old_adr
        old_content = template_loader.load("superseded", adr=old_adr)
        new_content = template_loader.load("supersedes", adr=new_adr)
        adr.write(old_adr, project, old_content)
        adr.write(new_adr, project, new_content)
        return 0

    new_content = template_loader.load("new", adr=new_adr)
    adr.write(new_adr, project, new_content)
    return 0
