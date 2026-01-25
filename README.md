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
