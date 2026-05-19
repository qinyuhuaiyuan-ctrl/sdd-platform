import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("SDD_DATA_DIR", Path.home() / ".sdd-platform"))
PROJECT_REPO_PATH = Path(os.environ.get("SDD_PROJECT_REPO", os.getcwd()))
DATABASE_PATH = DATA_DIR / "sdd.db"
SKILLS_DIR = DATA_DIR / "skills"
TEMPLATES_DIR = DATA_DIR / "templates"
