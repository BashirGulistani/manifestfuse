from __future__ import annotations
import argparse
from pathlib import Path

from .config import load_config
from .graph import build_manifest
from .reporter import write_json, write_html, write_delete_plan





def main() -> None:
    ap = argparse.ArgumentParser(
        prog="manifestfuse",
        description="Build an asset reference manifest for Liquid/HTML/CSS/JS projects (unused + duplicates).",
    )
    ap.add_argument("project_root", nargs="?", default=".", help="Project root (default: .)")
    ap.add_argument("--config", default=".manifestfuse.yml", help="Config file (default: .manifestfuse.yml)")
    ap.add_argument("--out", default=None, help="Override output dir")
    args = ap.parse_args()


    cfg = load_config(args.config)
    cfg.project_root = args.project_root
    root = str(Path(cfg.project_root).resolve())
    outdir = Path(root) / (args.out or cfg.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    payload = build_manifest(
        root=root,
        scan_include=cfg.scan_include,
        scan_exclude=cfg.scan_exclude,
        asset_dirs=cfg.asset_dirs,
    )

    write_json(str(outdir / "manifest.json"), payload)
    write_html(str(outdir / "report.html"), payload)

    if cfg.write_delete_plan and payload.get("unused_assets"):
        write_delete_plan(str(outdir / "delete_plan.sh"), payload["root"], payload["unused_assets"])

    print("Done.")
    print(f"- manifest: {outdir / 'manifest.json'}")
    print(f"- report:   {outdir / 'report.html'}")
    if cfg.write_delete_plan:
        print(f"- plan:     {outdir / 'delete_plan.sh'}")
