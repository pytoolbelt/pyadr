import re
from enum import Enum
from pathlib import Path
from typing import Optional, List, Iterator
from pyadr import config
from pyadr.error_handling.exceptions import PyadrError


class AdrStatus(Enum):
    PROPOSED = "Proposed"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    SUPERSEDED = "Superseded"


class FileNumber:
    def __init__(self, i: int) -> None:
        self._i = i

    @classmethod
    def from_filename(cls, name: str) -> "FileNumber":
        return cls(int(name.split("-")[0]))

    @property
    def index(self) -> int:
        return self._i

    @property
    def number(self) -> str:
        return str(self.index).zfill(4)

    def increment(self) -> None:
        self._i += 1


class Adr:
    def __init__(
        self,
        number: FileNumber,
        title: str,
        status: AdrStatus,
        content: str = "",
        superseded_adr: Optional["Adr"] = None,
        supersedes_adr: Optional["Adr"] = None,
    ) -> None:
        self._number = number
        self.title = title
        self.status = status
        self.content = content
        self.superseded_adr = superseded_adr
        self.supersedes_adr = supersedes_adr

    @classmethod
    def from_path(cls, path: Path) -> "Adr":
        content = path.read_text()
        return cls.from_content(content)

    @classmethod
    def from_content(cls, content: str) -> "Adr":
        number_match = re.search(r"# ADR (\d+): (.+)", content)
        status_match = re.search(r"Status: (Proposed|Accepted|Deprecated|Superseded)", content)
        content_section = re.search(r"## Context(.*)", content, re.DOTALL)

        if not (number_match and status_match):
            raise ValueError("ADR content is not in the expected format")

        number = int(number_match.group(1))
        title = number_match.group(2).strip()
        status = AdrStatus[status_match.group(1).upper()]

        if content_section:
            content_section = content_section.group(1).strip()
            return Adr(FileNumber(number), title, AdrStatus(status), content_section)
        return Adr(FileNumber(number), title, AdrStatus(status))

    @property
    def number(self) -> FileNumber:
        return self._number

    @property
    def filename(self) -> str:
        return f"{self.number.number}-{self.title}.md"


class Project:
    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = root or config.PYADR_PROJECT_ROOT

    @property
    def docs_dir(self) -> Path:
        return self.root / "docs"

    @property
    def adr_dir(self) -> Path:
        return self.docs_dir / "adr"

    def init(self) -> None:
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.adr_dir.mkdir(parents=True, exist_ok=True)

    def adr_paths(self) -> Iterator[Path]:
        for path in self.adr_dir.glob("*.md"):
            if re.match(config.PYADR_FILE_PATTERN, path.name):
                yield path

    def list_adrs_paths(self, reverse: bool = False) -> List[Path]:
        l = list(self.adr_paths())
        return sorted(l, reverse=reverse)

    def list_adrs(self, reverse: bool = False) -> List[Adr]:
        l = [Adr.from_path(p) for p in self.adr_paths()]
        return sorted(l, key=lambda p: p.number.index, reverse=reverse)

    def list_indexes(self) -> List[FileNumber]:
        return [adr.number for adr in self.list_adrs()]

    def next_number(self) -> FileNumber:
        try:
            i = self.list_indexes()[-1]
            i.increment()
        except IndexError:
            i = FileNumber(1)
        return i

    def get_adr(self, number: str) -> Adr:
        for adr in self.list_adrs():
            if adr.number.number == number:
                return adr
        raise PyadrError(f"No adr found for {number}")


class TemplateLoader:
    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or config.PYADR_TEMPLATE_DIR

    def load(self, name: str, **params) -> str:
        path = self.template_dir / f"{name}.md"
        content = path.read_text()
        if params:
            return content.format(**params)
        return content


def write(adr: Adr, project: Project, content: str) -> None:
    path = project.adr_dir / adr.filename
    path.touch(exist_ok=True)
    path.write_text(content)
