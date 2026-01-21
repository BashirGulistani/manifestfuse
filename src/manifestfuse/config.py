from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class FuseConfig:
    project_root: str = "."
    scan_include: list[str] = field(default_factory=lambda: ["**/*.liquid", "**/*.html", "**/*.css", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.json"])
    scan_exclude: list[str] = field(default_factory=lambda: ["**/node_modules/**", "**/.git/**", "**/dist/**", "**/build/**"])

    asset_dirs: list[str] = field(default_factory=lambda: ["assets", "snippets", "sections", "templates", "layout"])

    output_dir: str = ".manifestfuse-out"

    write_delete_plan: bool = True





def _coerce_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]




def load_config(path: str | None) -> FuseConfig:
    if not path:
        return FuseConfig()

    p = Path(path)
    if not p.exists():
        return FuseConfig()

    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    cfg = FuseConfig()

    cfg.project_root = str(raw.get("project_root", cfg.project_root))
    cfg.scan_include = _coerce_list(raw.get("scan_include", cfg.scan_include))
    cfg.scan_exclude = _coerce_list(raw.get("scan_exclude", cfg.scan_exclude))
    cfg.asset_dirs = _coerce_list(raw.get("asset_dirs", cfg.asset_dirs))
    cfg.output_dir = str(raw.get("output_dir", cfg.output_dir))
    cfg.write_delete_plan = bool(raw.get("write_delete_plan", cfg.write_delete_plan))
    return cfg



