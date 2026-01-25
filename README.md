# ManifestFuse

ManifestFuse builds a “what’s actually used?” manifest for messy web projects — especially Shopify themes.


If you’ve ever opened a theme’s `assets/` folder and thought:
> “Can I delete any of this without breaking production?”
…this tool is for that exact moment.

It scans your Liquid/HTML/CSS/JS files, finds asset references, and then compares them against what exists in the repo.

You get:
- a manifest file (references graph)
- a list of used assets
- a list of unused assets
- duplicate detection (byte-identical files)
- a simple HTML report you can hand to someone else
- an optional interactive delete plan script

This is static analysis, not browser coverage. The point is to get you 80–90% of the way there fast, with a clear audit trail.

---

## Install

From source:

```bash
pip install -e .
