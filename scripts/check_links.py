#!/usr/bin/env python3
"""Check the built site for broken internal links, missing assets, and dead anchors.

    python3 scripts/check_links.py

Exits non-zero if anything is wrong. External (http) links are not requested.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import ROOT, SITE_PATH  # noqa: E402  (single source of truth for both)

PAGES = ["index.html", "documentation.html", "404.html"] + \
        sorted(str(p.relative_to(ROOT)) for p in (ROOT / "tools").glob("*.html"))

LINK = re.compile(r'(?:href|src)="([^"]+)"')
ANCHOR_ID = re.compile(r'\sid="([^"]+)"')


def main() -> int:
    problems = []

    ids = {}
    for page in PAGES:
        ids[page] = set(ANCHOR_ID.findall((ROOT / page).read_text(encoding="utf-8")))

    for page in PAGES:
        source = ROOT / page
        markup = source.read_text(encoding="utf-8")

        for href in LINK.findall(markup):
            if href.startswith(("http://", "https://", "mailto:", "data:", "//")):
                continue
            path, _, fragment = href.partition("#")
            if not path:
                if fragment and fragment not in ids[page]:
                    problems.append("%s: anchor #%s does not exist" % (page, fragment))
                continue
            path = path.split("?")[0]
            if path.startswith("/"):
                # Absolute links carry the publish prefix (e.g. /AIHAToolBox/);
                # strip it to get back to a repo-relative path.
                if SITE_PATH != "/" and not path.startswith(SITE_PATH):
                    problems.append("%s: %s -> absolute link missing the %s prefix"
                                    % (page, href, SITE_PATH))
                    continue
                base, path = ROOT, path[len(SITE_PATH):]
            else:
                base = source.parent
            target = (base / path).resolve()
            if not target.exists():
                problems.append("%s: %s -> missing file" % (page, href))
                continue
            rel = str(target.relative_to(ROOT))
            if fragment and rel in ids and fragment not in ids[rel]:
                problems.append("%s: %s -> anchor #%s does not exist" % (page, href, fragment))

        if "{{" in markup:
            problems.append("%s: unrendered template placeholder" % page)
        for tag in ("<html", "<title", "</body>"):
            if tag not in markup:
                problems.append("%s: missing %s" % (page, tag))

    if problems:
        print("Link check failed:", file=sys.stderr)
        for problem in problems:
            print("  " + problem, file=sys.stderr)
        return 1

    print("Link check passed: %d pages, no broken internal links." % len(PAGES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
