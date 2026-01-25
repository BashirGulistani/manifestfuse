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



def write_html(path: str, payload: Payload) -> None:
    p = Path(path)
    ensure_parent(p)

    root = payload.get("root", "Unknown")
    stats = {
        "files_scanned": payload.get("files_scanned", 0),
        "assets_total": payload.get("assets_total", 0),
        "assets_used": payload.get("assets_used", 0),
        "assets_unused": payload.get("assets_unused", 0),
    }
    

    def render_list(items: List[str], limit: int = 2000) -> str:
        return "".join(f"<li><code>{html.escape(str(x))}</code></li>" for x in items[:limit])

    css = textwrap.dedent("""
        body{font-family:system-ui,-apple-system,sans-serif;margin:24px;background:#0b0b0b;color:#eee}
        .card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:14px;margin:12px 0}
        h1{margin:0 0 6px;font-size:22px} h2{margin:0 0 10px;font-size:16px}
        .muted{color:#b9b9b9;font-size:13px}
        code{font-family:ui-monospace,monospace}
        details{margin-top:8px} summary{cursor:pointer} ul{margin:8px 0 0 18px}
    """).strip()

    body_content = f"""
    <h1>ManifestFuse Report</h1>
    <div class="muted">Root: {html.escape(root)}</div>

    <div class="card">
      <h2>Overview</h2>
      <div class="muted">
        files scanned: {stats['files_scanned']}<br/>
        assets total: {stats['assets_total']}<br/>
        assets used: {stats['assets_used']}<br/>
        assets unused: {stats['assets_unused']}
      </div>
    </div>

    <div class="card">
      <h2>Unused assets ({len(payload.get("unused_assets", []))})</h2>
      <details open>
        <summary>Show list</summary>
        <ul>{render_list(payload.get("unused_assets", []))}</ul>
      </details>
    </div>

    <div class="card">
      <h2>Unresolved references ({len(payload.get("unresolved_refs", []))})</h2>
      <div class="muted">References not matching local assets.</div>
      <details>
        <summary>Show list</summary>
        <ul>{render_list(payload.get("unresolved_refs", []))}</ul>
      </details>
    </div>
    """
    dups = payload.get("duplicates", {})
    dup_items = []
    for k, vals in list(dups.items())[:200]:
        dup_items.append(
            f"<div style='margin:10px 0'><div class='muted'>hash: {html.escape(k)}</div>"
            f"<ul>{render_list(vals)}</ul></div>"
        )
    
    dup_section = f"""
    <div class="card">
      <h2>Duplicates ({len(dups)})</h2>
      <div class="muted">Byte-identical files.</div>
      <details>
        <summary>Show groups</summary>
        {"".join(dup_items)}
      </details>
    </div>
    """

    final_html = f"<!doctype html><html><head><meta charset='utf-8'/><style>{css}</style></head><body>{body_content}{dup_section}</body></html>"
    p.write_text(final_html, encoding="utf-8")








