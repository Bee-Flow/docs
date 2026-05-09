"""
Resolve folder-style image references at build time.

Convention:
    ![alt text](../img/screenshots/<topic>/)        ← path ends with /

The hook looks inside that folder and rewrites the reference to point at
the first image file found (alphabetically). Filename doesn't matter —
contributors just drop a screenshot into the right topical folder.

If the folder is missing or empty, a placeholder reference is emitted so
the build still succeeds (broken-image icon at runtime).

Supported extensions: .png .jpg .jpeg .webp .gif .svg
Hidden files (leading .) and `README.md` are ignored.
"""

from pathlib import Path
import os
import re
import logging

log = logging.getLogger("mkdocs.hooks.screenshots")

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}

# Match: ![alt](optional ../ prefix + img/screenshots/<topic>/<more?>/ )
# The trailing "/" before ")" is the trigger — explicit file references are left alone.
PATTERN = re.compile(
    r'!\[([^\]]*)\]\(((?:\.\./)*img/screenshots/[^()\s]+/)\)'
)


def _first_image(folder: Path):
    if not folder.is_dir():
        return None
    candidates = sorted(
        f for f in folder.iterdir()
        if f.is_file()
        and f.suffix.lower() in IMG_EXTS
        and not f.name.startswith(".")
    )
    return candidates[0] if candidates else None


def on_page_markdown(markdown, page, config, files, **kwargs):
    docs_dir = Path(config["docs_dir"]).resolve()
    page_dir = (docs_dir / page.file.src_path).parent

    def replace(match):
        alt = match.group(1)
        folder_path = match.group(2)
        folder_abs = (page_dir / folder_path).resolve()
        img = _first_image(folder_abs)
        if img is None:
            log.info(
                f"[screenshots] no image yet in {folder_abs.relative_to(docs_dir)}"
            )
            # Keep the folder ref as-is so an explicit broken-image icon
            # renders. Helpful visual cue to "drop a screenshot here".
            return match.group(0)
        # Pages can sit deeper than the screenshots tree (e.g. studio/foo.md
        # referencing img/screenshots/...). Path.relative_to insists on a
        # subpath relationship; os.path.relpath handles "../" segments.
        rel = os.path.relpath(img, page_dir).replace(os.sep, "/")
        return f"![{alt}]({rel})"

    return PATTERN.sub(replace, markdown)
