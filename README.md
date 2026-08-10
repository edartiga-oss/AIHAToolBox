# AIHA Industrial Hygienist Toolbox

A static website cataloguing exposure assessment tools for industrial hygiene and occupational
health professionals. Every tool has a directory entry and a detail page describing what it does,
what it needs, what it produces, and where to get it.

Live site: **https://edartiga-oss.github.io/AIHAToolBox/**

## How the site is put together

The published pages are generated from data and content files, so the shared layout, navigation,
and styling live in exactly one place instead of being copied into every page.

```
data/tools.json              one record per tool — drives the directory and every tool page
data/categories.json         assessment category names and descriptions
content/tools/<slug>.html    the written documentation for one tool (body sections only)
content/pages/*.html         standalone prose pages
templates/base.html          the page shell: <head>, header, nav, footer
templates/home.html          the directory page body
assets/css/site.css          the entire design system
assets/js/directory.js       search and filtering on the directory page
scripts/build.py             renders everything below into the repo root
scripts/check_links.py       fails on broken internal links or unrendered templates
```

Generated output — **do not edit these by hand**, they are overwritten on every build:

```
index.html  documentation.html  404.html  tools/<slug>.html  sitemap.xml  robots.txt
```

The generated files are committed to the repository. That keeps GitHub Pages working with no build
step and makes changes visible in pull request diffs.

## Working locally

Requires Python 3.9 or newer. There are no third-party dependencies.

```bash
python3 scripts/build.py       # regenerate every page
python3 scripts/check_links.py # verify internal links and anchors
python3 -m http.server 8000    # then open http://localhost:8000
```

Always run `scripts/build.py` after editing anything in `data/`, `content/`, or `templates/`, and
commit the regenerated pages along with your source change. CI runs `build.py --check` and fails
the build if the committed pages are out of date.

## Editing content

**Fix a description, developer, or category** — edit `data/tools.json` and rebuild. This file is
the single source of truth for the directory table, the filter chips and their counts, the badges,
and the sidebar on each tool page.

**Write or extend a tool's documentation** — edit `content/tools/<slug>.html`. Each file is a list
of `<section class="panel">` blocks; the build wraps them in the site shell. Useful building blocks:

```html
<section class="panel" id="overview">
  <h2>Overview</h2>
  <p>Plain prose.</p>
  <ul class="bullets"><li>A list</li></ul>
  <dl class="facts"><div><dt>Platform</dt><dd>Excel</dd></div></dl>
  <div class="callout callout--warn"><p>A limitation worth flagging.</p></div>
</section>
```

A section titled `Assessment Phase(s)` is lifted into the sidebar automatically rather than
rendered as its own panel.

**Add a new tool** — add a record to `data/tools.json`, create
`content/tools/<slug>.html` with at least an Overview section, then rebuild:

```json
{
  "name": "Tool name",
  "slug": "tool-name",
  "urls": ["https://example.org/tool"],
  "description": "One or two sentences for the directory table.",
  "exposure_routes": "Inhalation and dermal",
  "agency": "Developing organisation",
  "output": "What the tool produces.",
  "category": "Refined Exposure Assessment",
  "hazard_type": ["Chemical"],
  "tool_type": ["Worker Exposure"]
}
```

`category` must be one of the keys in `data/categories.json` — the build fails otherwise. Leave
`description` empty for a tool that has not been written up yet; it will be shown as
“write-up in progress” instead of being hidden.

## Deployment

`.github/workflows/pages.yml` runs on every push to `main`: it verifies the committed pages match
the sources, checks internal links, assembles the publishable files into `_site`, and deploys to
GitHub Pages.

To publish from a branch instead of Actions, point GitHub Pages at the repository root — the site
works as-is, with the source directories simply going unused.

### Moving to a custom domain

The site is served from the project URL, so pages live under `/AIHAToolBox/`. `SITE_URL` in
`scripts/build.py` is the only place that knows this — it drives canonical URLs, Open Graph tags,
`sitemap.xml`, `robots.txt`, and the absolute paths on `404.html`. To move to a domain:

1. Register the domain and point DNS at GitHub — a `CNAME` record on `www` to
   `<owner>.github.io.`, plus A records on the apex to `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`.
2. Set `SITE_URL = "https://www.example.com"` in `scripts/build.py` and rebuild. `SITE_PATH`
   becomes `/` on its own, so the absolute links on `404.html` follow automatically.
3. Add a `CNAME` file at the repo root containing just that hostname, and copy it into `_site` in
   `.github/workflows/pages.yml` (there is a comment marking the spot).
4. Enter the same domain under Settings → Pages, wait for the DNS check to pass, then enable
   **Enforce HTTPS**.
