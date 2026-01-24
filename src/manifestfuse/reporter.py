from __future__ import annotations
import html
import json
from pathlib import Path


def write_json(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")






def write_delete_plan(path: str, root: str, unused_assets: list[str]) -> None:

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("#!/usr/bin/env bash")
    lines.append("set -euo pipefail")
    lines.append("")
    lines.append('echo "ManifestFuse delete plan (interactive) — review before running."')
    lines.append('echo "Root: ' + root.replace('"', '\\"') + '"')
    lines.append("")

    for rel in unused_assets:
        lines.append(f'rm -i "{rel.replace(\'"\', \'\\\\"\')}"')

    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        p.chmod(0o755)
    except Exception:
        pass


def write_html(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    def h(s): return html.escape(str(s))

    unused = payload.get("unused_assets", [])
    used = payload.get("used_assets", [])
    unresolved = payload.get("unresolved_refs", [])
    dups = payload.get("duplicates", {})




    
