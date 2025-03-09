import os
from pathlib import Path

PYADR_DEBUG = os.getenv('PYADR_DEBUG', "False").lower() == 'true'

PYADR_PROJECT_ROOT = Path.cwd()
PYADR_DEFAULT_TEMPLATE_DIR = Path(__file__).parent / 'templates'

PYADR_TEMPLATE_DIR = Path(os.getenv('PYADR_TEMPLATE_DIR', PYADR_DEFAULT_TEMPLATE_DIR))

PYADR_FILE_PATTERN = r"^\d{4}-.+\.md$"
