#!/usr/bin/env python3
"""Fail if a change to the published site does not bump VERSION.

    python3 scripts/check_version.py <base-ref>      e.g. origin/main

Compares the committed HEAD with <base-ref>. When any published file differs —
the pages, the tool pages, or the assets — VERSION in scripts/build.py must
differ too, and when both values have the form vN the number must go up.
Changes confined to files the site does not serve (docs/, README, data or
content sources without a rebuild, scripts) need no bump.
"""

import re
import subprocess
import sys

# What the deploy publishes, per "Assemble the publishable site" in
# .github/workflows/pages.yml. sitemap.xml and robots.txt are left out: the
# sitemap's lastmod dates change whenever the site is rebuilt on a new day,
# with or without an edit, and robots.txt only changes alongside the pages.
PUBLISHED = ("index.html", "documentation.html", "404.html", "tools/", "assets/")

VERSION_RE = re.compile(r'^VERSION = "([^"]+)"', re.M)
NUMBERED_RE = re.compile(r"v(\d+)")


def git(*args):
    return subprocess.run(("git",) + args, check=True, capture_output=True, text=True).stdout


def version_at(ref):
    match = VERSION_RE.search(git("show", "%s:scripts/build.py" % ref))
    if not match:
        raise SystemExit("no VERSION line found in scripts/build.py at %s" % ref)
    return match.group(1)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    base = sys.argv[1]

    changed = git("diff", "--name-only", "%s...HEAD" % base).split()
    published = [path for path in changed if path.startswith(PUBLISHED)]
    if not published:
        print("No published files changed; no version bump needed.")
        return 0

    old, new = version_at(base), version_at("HEAD")
    if old == new:
        print("The published site changed (%d file%s) but VERSION is still %s."
              % (len(published), "" if len(published) == 1 else "s", old), file=sys.stderr)
        print("Bump VERSION in scripts/build.py, then run python3 scripts/build.py.",
              file=sys.stderr)
        for path in published[:10]:
            print("  changed: " + path, file=sys.stderr)
        if len(published) > 10:
            print("  ... and %d more" % (len(published) - 10), file=sys.stderr)
        return 1

    old_n, new_n = NUMBERED_RE.fullmatch(old), NUMBERED_RE.fullmatch(new)
    if old_n and new_n and int(new_n.group(1)) <= int(old_n.group(1)):
        print("VERSION went from %s to %s; it should go up." % (old, new), file=sys.stderr)
        return 1

    print("Version bumped %s -> %s for %d published file%s."
          % (old, new, len(published), "" if len(published) == 1 else "s"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
