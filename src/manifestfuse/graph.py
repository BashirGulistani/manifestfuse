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


def _rel(root: str, path: str) -> str:
    r = Path(root).resolve()
    p = Path(path).resolve()
    return str(p.relative_to(r)).replace("\\", "/")



def _best_match_asset(asset_rel_paths: Set[str], ref: str) -> str | None:

    ref = (ref or "").lstrip("/")
    if not ref:
        return None

    if ref in asset_rel_paths:
        return ref

    if "assets/" in ref:
        idx = ref.find("assets/")
        candidate = ref[idx:]
        if candidate in asset_rel_paths:
            return candidate

    fn = ref.split("/")[-1]
    if not fn:
        return None

    hits = [a for a in asset_rel_paths if a.endswith("/" + fn) or a == fn]
    if len(hits) == 1:
        return hits[0]

    return None





