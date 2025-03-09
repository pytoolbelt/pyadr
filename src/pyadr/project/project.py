import re
from pathlib import Path
from typing import Optional, List, Iterator

from pyadr import config


class FileIndex:

    def __init__(self, index: int) -> None:
        self._index = index

    @classmethod
    def from_name(cls, name: str) -> 'FileIndex':
        return cls(int(name.split("-")[0]))

    @property
    def index_as_int(self) -> int:
        return self._index

    @property
    def index_as_str(self) -> str:
        return str(self._index).zfill(4)

    def increment(self) -> None:
        self._index += 1


class Project:

    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = root or config.PYADR_PROJECT_ROOT

    @property
    def docs_dir(self) -> Path:
        return self.root / 'docs'

    @property
    def adr_dir(self) -> Path:
        return self.docs_dir / 'adr'

    def init(self) -> None:
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.adr_dir.mkdir(parents=True, exist_ok=True)

    def adrs(self) -> Iterator[Path]:
        for path in self.adr_dir.glob('*.md'):
            if re.match(config.PYADR_FILE_PATTERN, path.name):
                yield path

    def list_adrs(self, reverse: bool = False) -> List[Path]:
        l = list(self.adrs())
        return sorted(l, reverse=reverse)

    def list_indexes(self) -> List[FileIndex]:
        l = [FileIndex.from_name(p.name) for p in self.list_adrs()]
        return sorted(l, key=lambda p: p.index_as_int)

    def get_next_index(self) -> FileIndex:
        try:
            i = self.list_indexes()[-1]
            i.increment()
        except IndexError:
            i = FileIndex(1)
        return i

    def get_next_adr(self, title: str) -> Path:
        return self.adr_dir / f"{self.get_next_index().index_as_str}-{title}.md"
