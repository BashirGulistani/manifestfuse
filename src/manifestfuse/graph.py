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



def build_manifest(root: str, scan_include: list[str], scan_exclude: list[str], asset_dirs: list[str]) -> dict:
    root = str(Path(root).resolve())
    scan_files = discover_files(root, scan_include, scan_exclude)
    assets = discover_assets(root, asset_dirs)

    asset_rel = {_rel(root, a) for a in assets}
    asset_hash = {ar: file_sha256(str(Path(root) / ar)) for ar in asset_rel}

    graph = {}
    all_refs: Set[str] = set()
    resolved_used: Set[str] = set()
    unresolved_refs: Set[str] = set()



    for f in scan_files:
        relf = _rel(root, f)
        text = _read_text(f)
        refs = extract_refs_from_text(text)
        all_refs |= refs

        resolved = []
        unresolved = []
        for r in refs:
            m = _best_match_asset(asset_rel, r)
            if m:
                resolved.append(m)
                resolved_used.add(m)
            else:
                unresolved.append(r)
                unresolved_refs.add(r)

        graph[relf] = {
            "refs": sorted(refs),
            "resolved_assets": sorted(set(resolved)),
            "unresolved_refs": sorted(set(unresolved)),
        }

