from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

from .discover import discover_files, discover_assets
from .extractors import extract_refs_from_text
from .fingerprints import file_sha256




def _read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Path(path).read_text(encoding="latin-1")






