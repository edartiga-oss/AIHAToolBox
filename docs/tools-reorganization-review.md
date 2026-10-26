# Tools Main Page — review of Andy Becker's reorganization proposal

**Source:** `Tools_Main_Page_AJB_072926.docx` (Andy Becker, "first cut").
**Reviewed:** 2026-10-26. **Status of this document:** working roadmap, not yet a committed spec.

Andy's document proposes turning the Tools & Apps area into a single consolidated
landing page **organized by tool/application category and sub-category**, with several
new top-level sections, some removals/relocations, and a number of open questions. He is
explicit that it is a *first cut* and that "some tools may be referenced under more than
one category."

This review maps every item in the proposal to a concrete status so AIHA can decide what
to build next. The current website is a **filterable directory of 25 exposure-assessment
tools**; much of Andy's proposal expands well beyond that scope (phone apps, reference
documents, EPA links, a legal/ownership notice), and several items need content or product
decisions that are not in the source documents.

**Legend:** ✅ done in this change · ◐ recommended, buildable now · ⚠ needs content from
AIHA · ❓ needs a product decision · ↗ belongs elsewhere on aiha.org, not this directory.

---

## Done in this change

- ✅ **Added the FR Assessment Tool** (full page + directory entry), from
  `Tool_Specific_Page_FR_Assessment_Tool.docx`. Listed under *Refined Exposure
  Assessment*, matching Andy's "Refined Assessments" grouping.
- ✅ **Added the NPT-ODT Estimator** (full page + directory entry), from
  `Tool_Specific_Page_NPT_ODT_Estimator`. Listed under *Basic Characterization*, matching
  Andy's "Basic Categorization" grouping.
- ✅ **Category filter now reads in assessment-workflow order** — Data Collection →
  Basic Characterization → Preliminary / Initial → Refined → Validating → Product Exposure
  Modeling → Environmental — instead of alphabetically. This is the directory-level
  expression of Andy's "organized by category" intent and of his ordered list under
  "Computer based Tools and Resources (Filterable by Category)."

---

## Proposed top-level landing-page structure

Andy's main landing page would show five sections. The current site is section 3 only.

| # | Proposed section | Status | Notes |
|---|------------------|--------|-------|
| 1 | AIHA Policy on Application Ownership (legal notice + info re "Marcos") | ⚠ | Needs the actual notice/ownership text and the "Marcos" reference from AIHA — not in any source doc. |
| 2 | Phone / Calculator Apps | ⚠❓ | New section; needs the app list, links, and icons (see below). None are in the current data. |
| 3 | Access to Computer-Based Tools (~42, incl. Product Safety) | ◐ | This is today's directory (25 tools). ~17 more are implied by Andy's lists — see the gap analysis. |
| 4 | Background / Reference Documents | ⚠ | New section; documents (not tools) with links — see below. |
| 5 | Questions re tool use / submission of new tools | ◐ | Can be a short page or a panel with a contact/submission link once AIHA provides the destination. |

**Recommendation:** keep the current filterable directory as section 3 and add the other
four as sibling sections on a consolidated landing page. Each needs content AIHA holds; the
scaffolding is straightforward once that content exists.

---

## Removals / relocations Andy calls out

| Item | Andy's instruction | Status |
|------|--------------------|--------|
| NIOSH Apps and Tools | Relocate content under "Exposure / Control Banding Tools" or "Phone Apps" | ❓ not in current data |
| AIHA Heat Stress App | Move under a new "Heat / Thermal Stress Tools" category | ⚠ not in current data |
| Safety Climate Assessment Tool (under Job Safety & Health Programs) | Out of scope — relocate elsewhere on aiha.org | ↗ never in this directory |
| AIHA Ergo Assessment Tool Kit | Remove; instead add the *Ergonomic Assessment Tool Selection Guide* as a reference document | ⚠ not in current data |
| IH Hazards by Market Segment | Remove from tools; add under Background / Reference Documents | ◐ **currently a tool in our directory** — see recommendation |

**IH Hazards by Market Segment** is the one item already in our data (category *Data
Collection*). Andy is right that it is a reference resource, not a tool. **Recommendation:**
once a "Background / Reference Documents" section exists, move it there and remove it from
the tool table. Until that section exists, leaving it in place avoids a dangling link.
Andy also notes the underlying AIHA content buries 26 industry-specific exposure documents
behind a long SIC-code overview and could be streamlined for direct access — that is an
aiha.org content change, outside this repo.

---

## Phone / Calculator Apps (new) — ⚠ needs content

- **IH Calculator Apps** — in-site calculations (Andy notes none appear to be downloadable as
  phone apps, which is why they are listed separately from the Phone Apps below), with
  sub-categories: Basic Sciences, Heat Stress, Noise, Statistics, Ventilation, Radiation,
  Conversions.
- **Phone Apps:** NIOSH Lifting Equation, Ergomine, OSHA/NIOSH Heat Safety Tool, Home Care
  Safety, SLM.

None are in the current data. To build this we need, per app: name, one-line description,
platform (iOS/Android/web), and a link. Andy also asks whether the **UNIFAC Calculator**
(currently a Refined-Assessment tool here) belongs under IH Calculator Apps instead — ❓ a
re-categorization decision.

---

## New tool categories Andy proposes

| Category | Tools named | Status |
|----------|-------------|--------|
| Exposure / Control Banding | NIOSH Exposure Banding, Stoffenmanager 8.2 (already here), "Other? (not COSHH)" | ◐ Stoffenmanager present; NIOSH Exposure Banding ⚠ to add |
| Heat / Thermal Stress | AIHA tool + IRSST tools; links to heat-stress calcs and ergo apps | ⚠ not in current data |
| Ergonomic Assessment | NIOSH Ergomine, NIOSH Lifting Equation, AIHA Ergo kit (tool or reference?) | ⚠❓ |
| Pandemic Assessment | COV-IRT LLC Exposure Assessment Tool (CEAT) — full description supplied in the doc | ◐ content exists in the proposal; can add if AIHA wants a Pandemic category and a link |
| Business Case | AIHA Business Case Tool | ⚠ needs link/description |
| OEL Adjustment | Toxico-kinetic Extended Shift adjustment; IRSST method (link + doc); IH calc for B&S method | ◐ overlaps the two OEL tools flagged in the original UPDATE_SUMMARY |
| EPA Risk & Exposure Assessment Tools | 10 EPA links (Air Quality, Ecological Risk, the six ExpoBox families, TSCA, pesticides, human health) | ◐ links are in the proposal; would be a reference/links block, possibly cross-listed under Product Assessment |

The **Product Exposure Modeling** group in Andy's doc lists ~15 tools, several of which we
currently file under *other* categories (e.g. IH-MOD 2.0, SDM 2.0, DRAM, ChemSTEER). This
reflects his note that a tool may appear under more than one category. Our directory
currently assigns each tool a single category. ❓ **Decision needed:** should tools support
multiple categories (a tool could then show under both "Refined" and "Product Exposure
Modeling")? That is a small data-model change (category → list) we can make if wanted.

---

## Background / Reference Documents (new) — ⚠ needs content

- Functional Requirements for IH/OEHS Systems → **remove**, replace with "Best Practices
  for IH-related document management" (new).
- Ergonomic Assessment Tool Selection Guide.
- IH Hazards by Market Segment (moved here from tools — see above).
- Information Resources for Users of Statistical Tools.
- Model Exposure Assessment and Management Written Program.
- NIOSH Pocket Guide (formerly under "NIOSH").

Each needs a title and a link. These are documents, not tools, so they belong in a separate
reference-documents list rather than the filterable tool table.

---

## Gap analysis — tools named by Andy vs. the current directory

**Already in the directory (match Andy's lists):** IH/OEHS Exposure Scenario Tool, Basic
Exposure Assessment & Sampling Spreadsheet, NPT-ODT Estimator, SDM 2.0, IH-MOD 2.0,
IH SkinPerm, ODHMOD, DRAM, FR Assessment Tool, RF Exposure Assessment Tool, UNIFAC
Calculator, SIHM, CB Nanotool 2.0, Precautionary Matrix, Stoffenmanager Nano,
Stoffenmanager 8.2, NanoSafer, ECETOC TRA (integrated + consumer), Advanced REACH Tool,
ConsExpo Web, Consumer Exposure Model, EAS-E / RAIDAR-ICE, ChemSTEER.

**Named by Andy but not yet in the directory (candidates to add):** NIOSH Exposure Banding;
AIHA Heat Stress App + IRSST heat tools; NIOSH Ergomine; NIOSH Lifting Equation; AIHA Ergo
Assessment Tool Kit; COV-IRT CEAT (pandemic); AIHA Business Case Tool; OEL Adjustment
(Toxico-kinetic) and IRSST OEL method; the 10 EPA ExpoBox/risk tools; and the phone/calculator
apps. Not from Andy's proposal but still outstanding from the earlier UPDATE_SUMMARY and worth
folding into the same effort: **OEL Adjustment — IRSST method** (which Andy also names) and
**IHDA-AIHA** (Bayesian decision analysis, Paul Hewett — not mentioned by Andy).

Each new entry needs the same fields the directory already uses: name, link, one-line
description, exposure routes, developer, output, category, hazard type, tool type. Give me
the source material (or point me at the AIHA pages) and each is a quick add.

---

## Open questions for AIHA (from Andy's doc)

1. Should a tool be allowed to appear under **more than one category** (e.g. IH-MOD under
   both Refined and Product Exposure Modeling)?
2. Does the **UNIFAC Calculator** belong under Refined Assessment or IH Calculator Apps?
3. Where should the **Safety Climate Assessment Tool** live (Andy: out of scope here)?
4. Is the **AIHA Ergo Assessment Tool Kit** a tool or a reference document?
5. What is the **Application Ownership / legal notice** text, and the "Marcos" reference?
6. What is the destination for **"Submit a new tool"** (form, email, page)?
7. The FR Assessment Tool source **contradicts itself on macros** — "Tool Type: Macro-enabled
   tool – No" vs. "System requirements: Macros must be enabled for full functionality." The
   published page currently shows "Macro-enabled: No." Please confirm which is correct.

---

## Suggested build order

1. ✅ Add the two tools and the workflow-ordered category filter (this change).
2. Add the remaining named tools for which AIHA can supply source material (fastest wins:
   NIOSH Exposure Banding, the OEL Adjustment tools, IHDA-AIHA, COV-IRT CEAT).
3. Decide the multi-category question (#1). If yes, change the data model once, early.
4. Add the consolidated landing page shell with the five top-level sections, filling the
   reference-documents and phone-apps lists as AIHA provides content.
5. Add the legal/ownership notice and the "submit a tool" destination.
