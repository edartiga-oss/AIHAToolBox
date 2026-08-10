#!/usr/bin/env python3
"""Build the AIHA Industrial Hygienist Toolbox static site.

Sources of truth
    data/tools.json            one record per tool (drives the directory + every tool page)
    data/categories.json       assessment category descriptions
    content/tools/<slug>.html  the written documentation for each tool
    content/pages/*.html       standalone prose pages
    templates/*.html           page shells

Output (committed to the repo so GitHub Pages needs no build step)
    index.html, documentation.html, 404.html, tools/<slug>.html, sitemap.xml, robots.txt

Usage
    python3 scripts/build.py [--check]

    --check  build into memory and fail if the committed output is stale
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# Where the site is published. Canonical URLs, Open Graph tags, the sitemap, and
# robots.txt are all derived from this, so it is the only line to change when the
# site moves. To serve it from a custom domain instead, set this to the domain
# (e.g. "https://www.aihatoolbox.com"), add a CNAME file holding that hostname,
# and set the same domain under Settings -> Pages.
SITE_URL = "https://edartiga-oss.github.io/AIHAToolBox"

# The path GitHub Pages serves the site under ("/AIHAToolBox/" for a project site,
# "/" at a domain root). Only absolute links need it — everything else is relative.
SITE_PATH = (urlparse(SITE_URL).path.rstrip("/") or "") + "/"

SITE_NAME = "AIHA Industrial Hygienist Toolbox"
YEAR = 2025  # footer copyright year; bump when the site content is next revised

ROUTES = [("inhalation", "Inhalation"), ("dermal", "Dermal"), ("oral", "Oral")]


# --------------------------------------------------------------------------- helpers
def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def fill(template: str, values: dict) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{%s}}" % key, value)
    leftover = re.findall(r"\{\{([A-Z_]+)\}\}", out)
    if leftover:
        raise SystemExit("unfilled template placeholders: %s" % sorted(set(leftover)))
    return out


def strip_tags(markup: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", markup)).strip()


def summarise(text: str, limit: int = 155) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def routes_of(tool: dict) -> list:
    text = (tool.get("exposure_routes") or "").lower()
    return [key for key, _ in ROUTES if key in text]


def is_stub(tool: dict) -> bool:
    """A tool whose directory entry has not been written up yet."""
    return not tool.get("description")


# --------------------------------------------------------------------------- page shell
def page(*, title, description, canonical_path, main, hero="", active="",
         base="", head_extra="", scripts="") -> str:
    return fill(read("templates/base.html"), {
        "TITLE": esc(title),
        "OG_TITLE": esc(title),
        "DESCRIPTION": esc(description),
        "CANONICAL": SITE_URL + canonical_path,
        "BASE": base,
        "HEAD_EXTRA": head_extra,
        "HERO": hero,
        "MAIN": main,
        "SCRIPTS": scripts,
        "YEAR": str(YEAR),
        "NAV_TOOLS": ' aria-current="page"' if active == "tools" else "",
        "NAV_DOCS": ' aria-current="page"' if active == "docs" else "",
    })


# --------------------------------------------------------------------------- home page
def filter_group(label: str, name: str, options: list) -> str:
    """options: list of (value, label, count); value "" means "all"."""
    chips = [
        '        <button type="button" class="chip" data-filter="%s" data-value="%s" '
        'aria-pressed="%s">%s</button>' % (name, esc(value), "true" if value == "" else "false", esc(text))
        for value, text, _count in options
    ]
    return (
        '      <div class="filter-group" role="group" aria-label="Filter by %s">\n'
        '        <span class="filter-group__label">%s</span>\n%s\n      </div>'
        % (esc(label.lower()), esc(label), "\n".join(chips))
    )


def build_home(tools: list) -> str:
    def counted(values, key):
        counts = {}
        for tool in tools:
            for value in key(tool):
                counts[value] = counts.get(value, 0) + 1
        return [(v, "%s (%d)" % (v, counts[v]), counts[v]) for v in values if counts.get(v)]

    tool_types = sorted({t for tool in tools for t in tool["tool_type"]})
    hazards = sorted({h for tool in tools for h in tool["hazard_type"]})
    categories = sorted({tool["category"] for tool in tools})

    route_counts = [
        (key, "%s (%d)" % (label, sum(1 for t in tools if key in routes_of(t))),
         sum(1 for t in tools if key in routes_of(t)))
        for key, label in ROUTES
    ]

    groups = [
        filter_group("Tool type", "type", [("", "All types", 0)] + counted(tool_types, lambda t: t["tool_type"])),
        filter_group("Hazard", "hazard", [("", "All hazards", 0)] + counted(hazards, lambda t: t["hazard_type"])),
        filter_group("Exposure route", "route", [("", "All routes", 0)] + [r for r in route_counts if r[2]]),
        filter_group("Category", "category", [("", "All categories", 0)] + counted(categories, lambda t: [t["category"]])),
    ]

    rows = []
    for tool in tools:
        haystack = " ".join(filter(None, [
            tool["name"], tool["description"], tool["agency"], tool["output"],
            tool["category"], tool["exposure_routes"],
            " ".join(tool["hazard_type"]), " ".join(tool["tool_type"]),
        ])).lower()
        route_badges = "".join(
            '<span class="badge badge--route">%s</span>' % label
            for key, label in ROUTES if key in routes_of(tool)
        )
        description = (
            '<span class="pending">Write-up in progress</span>' if is_stub(tool)
            else esc(tool["description"])
        )
        rows.append(
            '        <tr data-type="%s" data-hazard="%s" data-route="%s" data-category="%s" data-search="%s">\n'
            '          <td class="cell-name" data-label="Tool">\n'
            '            <a href="tools/%s.html">%s</a>\n'
            '            %s\n'
            '          </td>\n'
            '          <td class="cell-desc" data-label="What it does"><div class="clamp">%s</div></td>\n'
            '          <td data-label="Category"><span class="badge badge--category">%s</span></td>\n'
            '          <td class="cell-developer" data-label="Developer">%s</td>\n'
            '          <td class="cell-output" data-label="Output"><div class="clamp">%s</div></td>\n'
            '        </tr>' % (
                esc("|".join(tool["tool_type"]).lower()),
                esc("|".join(tool["hazard_type"]).lower()),
                esc("|".join(routes_of(tool))),
                esc(tool["category"].lower()),
                esc(haystack),
                tool["slug"], esc(tool["name"]),
                '<div class="meta-line">%s</div>' % route_badges if route_badges else "",
                description,
                esc(tool["category"]),
                esc(tool["agency"]) or '<span class="pending">Not documented yet</span>',
                esc(tool["output"]) or '<span class="pending">Not documented yet</span>',
            )
        )

    body = fill(read("templates/home.html"), {
        "FILTERS": "\n".join(groups),
        "ROWS": "\n".join(rows),
        "TOOL_COUNT": str(len(tools)),
    })

    hero = (
        '<div class="hero">\n'
        '  <div class="wrap">\n'
        '    <h1>Exposure assessment tools, in one place</h1>\n'
        '    <p class="hero__lead">A curated directory of validated models and instruments for occupational, '
        'consumer, and environmental exposure assessment — what each tool does, what it needs, what it '
        'produces, and where to get it.</p>\n'
        '    <div class="stats">\n'
        '      <div class="stat"><span class="stat__value">%d</span><span class="stat__label">Assessment tools</span></div>\n'
        '      <div class="stat"><span class="stat__value">%d</span><span class="stat__label">Exposure routes</span></div>\n'
        '      <div class="stat"><span class="stat__value">%d</span><span class="stat__label">Assessment categories</span></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>' % (len(tools), len([r for r in route_counts if r[2]]), len(categories))
    )

    return page(
        title="Assessment Tools | " + SITE_NAME,
        description="A searchable directory of %d exposure assessment tools for industrial hygiene — "
                    "filter by tool type, hazard, exposure route, and assessment category." % len(tools),
        canonical_path="/",
        hero=hero,
        main=body,
        active="tools",
        scripts='<script src="assets/js/directory.js" defer></script>',
    )


# --------------------------------------------------------------------------- tool pages
def build_tool(tool: dict, tools: list, index: int) -> str:
    slug = tool["slug"]
    content = read("content/tools/%s.html" % slug).strip()

    # A one-line section reads better as a sidebar fact than as its own panel.
    assessment_phase = ""
    phase_section = re.search(
        r'<section class="panel" id="assessment-phase-s">.*?</section>\n*', content, re.S)
    if phase_section:
        assessment_phase = strip_tags(re.sub(r"<h2>.*?</h2>", "", phase_section.group(0), flags=re.S))
        content = content.replace(phase_section.group(0), "").strip()

    badges = ['<span class="badge badge--hero">%s</span>' % esc(tool["category"])]
    badges += ['<span class="badge badge--hero">%s</span>' % esc(t) for t in tool["tool_type"]]
    badges += ['<span class="badge badge--hero">%s hazard</span>' % esc(h) for h in tool["hazard_type"]]

    hero = (
        '<div class="hero hero--compact">\n'
        '  <div class="wrap">\n'
        '    <nav class="breadcrumb" aria-label="Breadcrumb">\n'
        '      <a href="../index.html">Assessment Tools</a> <span aria-hidden="true">/</span> %s\n'
        '    </nav>\n'
        '    <h1>%s</h1>\n'
        '    <div class="badge-row">%s</div>\n'
        '  </div>\n'
        '</div>' % (esc(tool["name"]), esc(tool["name"]), "".join(badges))
    )

    main_parts = []
    if is_stub(tool):
        main_parts.append(
            '<div class="callout callout--info panel">\n'
            '<p><strong>Write-up in progress.</strong> This tool is part of the toolbox, but its '
            'detailed documentation has not been published yet. The reference links below go '
            'straight to the developer&rsquo;s own material.</p>\n'
            '</div>' if tool["urls"] else
            '<div class="callout callout--info panel">\n'
            '<p><strong>Write-up in progress.</strong> This tool is part of the toolbox, but its '
            'detailed documentation and access link have not been published yet.</p>\n'
            '</div>'
        )
    if content:
        main_parts.append(content)

    # Sidebar: access links
    aside = []
    if tool["urls"]:
        links = "\n".join(
            '      <a class="btn %s" href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
            % ("btn--primary" if i == 0 else "btn--ghost", esc(url),
               "Access the tool &rarr;" if i == 0 else "Alternative link %d &rarr;" % (i + 1))
            for i, url in enumerate(tool["urls"])
        )
        aside.append(
            '<section class="panel">\n<h2>Get the tool</h2>\n'
            '  <div class="tool-links">\n%s\n  </div>\n</section>' % links
        )

    facts = []
    if assessment_phase:
        facts.append(("Assessment phase", esc(assessment_phase)))
    if tool["exposure_routes"]:
        facts.append(("Exposure routes", esc(tool["exposure_routes"])))
    if tool["hazard_type"]:
        facts.append(("Hazard types", esc(", ".join(tool["hazard_type"]))))
    if tool["tool_type"]:
        facts.append(("Applies to", esc(", ".join(tool["tool_type"]))))
    facts.append(("Assessment category", esc(tool["category"])))
    if tool["agency"]:
        facts.append(("Developer", esc(tool["agency"])))
    aside.append(
        '<section class="panel">\n<h2>At a glance</h2>\n'
        '  <ul class="aside-list">\n%s\n  </ul>\n</section>'
        % "\n".join('    <li><div class="aside-label">%s</div><div>%s</div></li>' % (label, value)
                    for label, value in facts)
    )

    related = [t for t in tools if t["slug"] != slug and t["category"] == tool["category"]][:5]
    if related:
        aside.append(
            '<section class="panel">\n<h2>Same category</h2>\n'
            '  <ul class="aside-list">\n%s\n  </ul>\n</section>'
            % "\n".join('    <li><a href="%s.html">%s</a></li>' % (t["slug"], esc(t["name"]))
                        for t in related)
        )

    prev_tool = tools[index - 1] if index > 0 else None
    next_tool = tools[index + 1] if index + 1 < len(tools) else None
    nav_links = []
    if prev_tool:
        nav_links.append('  <a href="%s.html"><span>Previous</span><strong>%s</strong></a>'
                         % (prev_tool["slug"], esc(prev_tool["name"])))
    if next_tool:
        nav_links.append('  <a href="%s.html"><span>Next</span><strong>%s</strong></a>'
                         % (next_tool["slug"], esc(next_tool["name"])))
    page_nav = '<nav class="page-nav" aria-label="Tool">\n%s\n</nav>' % "\n".join(nav_links) if nav_links else ""

    main = (
        '<div class="wrap">\n'
        '  <div class="tool-layout">\n'
        '    <div>\n%s\n%s\n    </div>\n'
        '    <aside class="tool-aside" aria-label="Tool summary">\n%s\n    </aside>\n'
        '  </div>\n'
        '</div>' % ("\n\n".join(main_parts), page_nav, "\n".join(aside))
    )

    overview = re.search(r'id="overview">\s*<h2>Overview</h2>\s*<p>(.*?)</p>', content, re.S)
    description = summarise(strip_tags(overview.group(1)) if overview else
                            (tool["description"] or "%s — part of the %s." % (tool["name"], SITE_NAME)))

    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool["name"],
        "applicationCategory": "Exposure assessment tool",
        "description": description,
        "url": "%s/tools/%s.html" % (SITE_URL, slug),
    }
    if tool["agency"]:
        ld["author"] = {"@type": "Organization", "name": tool["agency"]}
    if tool["urls"]:
        ld["installUrl"] = tool["urls"][0]

    return page(
        title="%s | %s" % (tool["name"], SITE_NAME),
        description=description,
        canonical_path="/tools/%s.html" % slug,
        hero=hero,
        main=main,
        active="tools",
        base="../",
        head_extra='<script type="application/ld+json">%s</script>'
                   % json.dumps(ld, ensure_ascii=False, indent=2),
    )


# --------------------------------------------------------------------------- other pages
def build_documentation(categories: dict, tools: list) -> str:
    counts = {}
    for tool in tools:
        counts[tool["category"]] = counts.get(tool["category"], 0) + 1
    items = []
    for name, blurb in categories.items():
        count = counts.get(name, 0)
        items.append(
            '  <li><strong>%s</strong> (%d tool%s) — %s</li>'
            % (esc(name), count, "" if count == 1 else "s", esc(blurb))
        )
    body = read("content/pages/documentation.html").replace(
        "{{CATEGORY_LIST}}", '<ul class="bullets">\n%s\n</ul>' % "\n".join(items))

    hero = (
        '<div class="hero hero--compact">\n'
        '  <div class="wrap">\n'
        '    <h1>Supporting documentation</h1>\n'
        '    <p class="hero__lead">How the toolbox is organised, how to pick a tool for the decision '
        'in front of you, and what to check before you trust an output.</p>\n'
        '  </div>\n'
        '</div>'
    )
    return page(
        title="Supporting Documentation | " + SITE_NAME,
        description="Guidance on selecting exposure assessment tools, what each assessment category "
                    "means, and good practice for modelling and interpreting results.",
        canonical_path="/documentation.html",
        hero=hero,
        main='<div class="wrap wrap--narrow prose">\n%s\n</div>' % body,
        active="docs",
    )


def build_404() -> str:
    # Pages serves this for a missing path at any depth, so its links must be
    # absolute — relative ones would resolve against whatever URL was mistyped.
    main = (
        '<div class="wrap wrap--narrow">\n'
        '  <div class="empty-state">\n'
        '    <h3>Page not found</h3>\n'
        '    <p>That page does not exist, or it has moved.</p>\n'
        '    <p style="margin-top:1.5rem"><a class="btn btn--primary" href="%sindex.html">Browse all tools</a></p>\n'
        '  </div>\n'
        '</div>' % SITE_PATH
    )
    return page(title="Page not found | " + SITE_NAME,
                description="The requested page could not be found.",
                canonical_path="/404.html", main=main, base=SITE_PATH)


def build_sitemap(tools: list) -> str:
    today = dt.date.today().isoformat()
    urls = ["/", "/documentation.html"] + ["/tools/%s.html" % t["slug"] for t in tools]
    entries = "\n".join(
        "  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n  </url>" % (SITE_URL, u, today)
        for u in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % entries)


def build_robots() -> str:
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL


# --------------------------------------------------------------------------- entry point
def render_all() -> dict:
    tools = json.loads(read("data/tools.json"))
    tools.sort(key=lambda t: t["name"].lower())
    categories = json.loads(read("data/categories.json"))

    unknown = {t["category"] for t in tools} - set(categories)
    if unknown:
        raise SystemExit("categories missing from data/categories.json: %s" % sorted(unknown))
    for tool in tools:
        if not (ROOT / ("content/tools/%s.html" % tool["slug"])).exists():
            raise SystemExit("missing content/tools/%s.html" % tool["slug"])

    files = {
        "index.html": build_home(tools),
        "documentation.html": build_documentation(categories, tools),
        "404.html": build_404(),
        "sitemap.xml": build_sitemap(tools),
        "robots.txt": build_robots(),
    }
    for i, tool in enumerate(tools):
        files["tools/%s.html" % tool["slug"]] = build_tool(tool, tools, i)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail if the committed output differs from a fresh build")
    args = parser.parse_args()

    files = render_all()
    if args.check:
        stale = []
        for name, content in files.items():
            path = ROOT / name
            if name == "sitemap.xml":
                continue  # lastmod changes daily by design
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        if stale:
            print("Stale output — run `python3 scripts/build.py`:", file=sys.stderr)
            for name in stale:
                print("  " + name, file=sys.stderr)
            return 1
        print("Output is up to date (%d files)." % len(files))
        return 0

    for name, content in files.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print("Built %d files: %d tool pages, index, documentation, 404, sitemap, robots."
          % (len(files), len(files) - 5))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
