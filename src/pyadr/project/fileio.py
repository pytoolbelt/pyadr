from pathlib import Path
from typing import Optional

from pyadr import config


class TemplateLoader:

    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or config.PYADR_TEMPLATE_DIR

    def load(self, name: str, **params) -> str:
        path = self.template_dir / f"{name}.md"
        content = path.read_text()
        if params:
            return content.format(**params)
        return content
