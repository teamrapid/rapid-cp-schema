"""Data model package for rapid-cp-schema."""

from pathlib import Path
from .rapid_cp_schema import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "rapid_cp_schema.yaml"
