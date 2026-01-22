from __future__ import annotations
import re
from typing import Iterable, Set, Tuple


LIQUID_ASSET_RE = re.compile(r"""\{\{\s*['"]([^'"]+\.(?:css|js|png|jpg|jpeg|webp|gif|svg|json|woff2?|ttf|eot|mp4|mov))['"]\s*\|\s*(?:asset_url|file_url|img_url|image_url)[^}]*\}\}""", re.IGNORECASE)






