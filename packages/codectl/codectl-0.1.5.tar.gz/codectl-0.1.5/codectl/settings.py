"""Built-in configurations."""

from pathlib import Path

BASE_DIR = Path.home() / ".codectl"

TEMPLATE_DIR = BASE_DIR / "templates"

CONFIG_PATH = BASE_DIR / "config.json"
