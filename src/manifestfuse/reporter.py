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


