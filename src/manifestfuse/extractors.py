from __future__ import annotations
import re
from typing import Iterable, Set, Tuple


LIQUID_ASSET_RE = re.compile(r"""\{\{\s*['"]([^'"]+\.(?:css|js|png|jpg|jpeg|webp|gif|svg|json|woff2?|ttf|eot|mp4|mov))['"]\s*\|\s*(?:asset_url|file_url|img_url|image_url)[^}]*\}\}""", re.IGNORECASE)



CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""", re.IGNORECASE)

HTML_SRC_RE = re.compile(r"""\s(?:src|href)\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE)
HTML_SRCSET_RE = re.compile(r"""srcset\s*=\s*['"]([^'"]+)['"]""", re.IGNORECASE)

JS_IMPORT_RE = re.compile(r"""import\s+[^;]*?['"]([^'"]+)['"]""", re.IGNORECASE)
JS_FETCH_RE = re.compile(r"""fetch\(\s*['"]([^'"]+)['"]""", re.IGNORECASE)

LIQUID_STYLESHEET_TAG_RE = re.compile(r"""['"]([^'"]+\.css(?:\.liquid)?)['"]\s*\|\s*asset_url\s*\|\s*stylesheet_tag""", re.IGNORECASE)




def _normalize_ref(ref: str) -> str:
    ref = (ref or "").strip()
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    return ref


def extract_refs_from_text(text: str) -> Set[str]:
    refs: Set[str] = set()

    for m in LIQUID_ASSET_RE.finditer(text):
        refs.add(_normalize_ref(m.group(1)))

    for m in LIQUID_STYLESHEET_TAG_RE.finditer(text):
        refs.add(_normalize_ref(m.group(1)))




