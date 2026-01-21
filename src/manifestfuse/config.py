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








