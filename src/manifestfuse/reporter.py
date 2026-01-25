from __future__ import annotations
import html
import json
import shlex
import textwrap
from pathlib import Path
from typing import Any, Dict, List

Payload = Dict[str, Any]

def ensure_parent(path: Path) -> None:
    """Helper to ensure parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)



def write_json(path: str, payload: Payload) -> None:
    p = Path(path)
    ensure_parent(p)
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

def write_delete_plan(path: str, root: str, unused_assets: List[str]) -> None:
    p = Path(path)
    ensure_parent(p)

    safe_root = shlex.quote(root)
    
    script_content = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        'echo "ManifestFuse delete plan (interactive) — review before running."',
        f'echo "Root: {safe_root}"',
        "",
    ]

    for rel in unused_assets:
        script_content.append(f"rm -i {shlex.quote(rel)}")

    p.write_text("\n".join(script_content) + "\n", encoding="utf-8")
    
    try:
        p.chmod(0o755)
    except OSError:
        pass  





