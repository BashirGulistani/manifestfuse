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


    html_text = f"""<!doctype html>
<html><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>ManifestFuse Report</title>
<style>
  body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;margin:24px;background:#0b0b0b;color:#eee}}
  .card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:14px;margin:12px 0}}
  h1{{margin:0 0 6px;font-size:22px}}
  h2{{margin:0 0 10px;font-size:16px}}
  .muted{{color:#b9b9b9;font-size:13px}}
  code,pre{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}
  details{{margin-top:8px}}
  summary{{cursor:pointer}}
  ul{{margin:8px 0 0 18px}}
</style>
</head>
<body>
<h1>ManifestFuse Report</h1>
<div class="muted">Root: {h(payload.get("root"))}</div>

<div class="card">
  <h2>Overview</h2>
  <div class="muted">
    files scanned: {h(payload.get("files_scanned"))}<br/>
    assets total: {h(payload.get("assets_total"))}<br/>
    assets used: {h(payload.get("assets_used"))}<br/>
    assets unused: {h(payload.get("assets_unused"))}
  </div>
</div>

<div class="card">
  <h2>Unused assets ({len(unused)})</h2>
  <details open>
    <summary>Show list</summary>
    <ul>{"".join(f"<li><code>{h(x)}</code></li>" for x in unused[:2000])}</ul>
  </details>
</div>

<div class="card">
  <h2>Unresolved references ({len(unresolved)})</h2>
  <div class="muted">These were referenced but didn’t match a local asset (CDN URLs, external links, etc.).</div>
  <details>
    <summary>Show list</summary>
    <ul>{"".join(f"<li><code>{h(x)}</code></li>" for x in unresolved[:2000])}</ul>
  </details>
</div>

<div class="card">
  <h2>Duplicates ({len(dups)})</h2>
  <div class="muted">Files that are byte-identical (SHA256 match).</div>
  <details>
    <summary>Show groups</summary>
    {"".join("<div style='margin:10px 0'><div class='muted'>hash: "+h(k)+"</div><ul>"+ "".join(f"<li><code>{h(v)}</code></li>" for v in vals) + "</ul></div>" for k, vals in list(dups.items())[:200])}
  </details>
</div>

</body></html>
"""
    p.write_text(html_text, encoding="utf-8")

    
