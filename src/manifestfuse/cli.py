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


