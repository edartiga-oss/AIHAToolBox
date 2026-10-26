# Candidate tools — researched, pending verification

**Purpose:** drafts for five tools named in (or adjacent to) Andy Becker's proposal, prepared so
each can be published to the directory as soon as the facts are confirmed.

**Important — read before publishing:** this session's network could not reach `aiha.org`,
`cdc.gov`, `irsst.qc.ca`, or `cov-irt.org` (the egress proxy blocked them), so **every fact below
came from web-search summaries, not from the live authoritative pages.** Nothing here has been
published to the site. Confidence and the specific items to confirm are listed per tool. The two
tools already added to the site (FR Assessment Tool, NPT-ODT Estimator) were built from the
authoritative Word docs you supplied — that is the standard these five should meet before they go
live.

**Fastest path to publish:** paste the text of each tool's AIHA/NIOSH/IRSST page (or hand me a doc,
as you did for FR and NPT), or just confirm the fields below, and I will add each one immediately.

### Taxonomy decisions these raise
- **New category "OEL Adjustment"** (Andy proposes it) for the two OEL tools below. Recommended.
- **New category "Pandemic Assessment"** (Andy proposes it) for CEAT, or map CEAT to the existing
  "Preliminary / Initial Exposure Assessment." CEAT would also be the **first Biological-hazard
  tool**, which makes the Biological hazard filter meaningful.
- NIOSH OEB → existing "Preliminary / Initial Exposure Assessment." IHDA-AIHA → existing
  "Validating Exposure Assessments."

---

## 1. NIOSH Occupational Exposure Banding e-Tool — confidence: MEDIUM

- **Proposed category:** Preliminary / Initial Exposure Assessment · **Hazard:** Chemical ·
  **Route:** Inhalation · **Tool type:** Worker Exposure
- **Developer:** NIOSH (CDC) · **URL (confirm live):** https://wwwn.cdc.gov/NIOSH-OEB/
- **Draft description:** "A free NIOSH web application that assigns a chemical an occupational
  exposure band (A–E) from its toxicological/hazard data, for chemicals that lack an authoritative
  occupational exposure limit (OEL). Supports Tier 1 (GHS-based) and Tier 2 (point-of-departure)
  banding."
- **Inputs:** hazard data across nine health endpoints (carcinogenicity, reproductive toxicity,
  STOT, genotoxicity, respiratory/skin sensitization, acute toxicity, skin corrosion/irritation,
  eye damage) — GHS categories (Tier 1) or point-of-departure data (Tier 2).
- **Output:** one band A–E (the most protective band across endpoints with data); each band is an
  order-of-magnitude airborne-concentration range.
- **Confirm before publishing:** exact Band A/B boundaries; current version/date (reported v1.1,
  updated 2021-09-21); that it is web-only and Tier 1/2 only.
- **Sources:** cdc.gov/NIOSH-OEB, its About page and Tier 1 criteria PDF, the 2019 NIOSH
  technical report (stacks.cdc.gov/view/cdc/79841), AIHA publications.

## 2. Toxico-kinetic Extended Shift OEL Adjustment — confidence: HIGH

- **Proposed category:** OEL Adjustment (new) · **Hazard:** Chemical · **Route:** Inhalation ·
  **Tool type:** Worker Exposure
- **Developer:** AIHA (implements Hickey & Reist 1977, per Armstrong et al.)
- **URL (confirm live):** aiha.org → Apps and Tools → AIHA Risk Assessment Tools →
  "toxico-kinetic-extended-shift-oel-adjustment"
- **Draft description:** "A free AIHA Excel workbook that adjusts a standard 8-hour occupational
  exposure limit for extended or nonstandard work shifts using the Hickey & Reist toxicokinetic
  (biological half-life) approach. Four tabs cover known half-life, unknown half-life,
  documentation, and examples; no macros."
- **Inputs:** 8-hr TWA OEL; shift schedule (hours/day, days/week); the substance's biological
  half-life (separate tab for unknown half-life).
- **Output:** a shift-adjusted (generally reduced) OEL preserving the standard limit's margin of
  safety.
- **Limitations:** only for OELs driven by accumulated systemic body burden — not for
  odor/irritant/acute-effect limits; needs a half-life; least conservative of the common methods.
- **Confirm before publishing:** version/date; direct download link and file type; whether the
  author credit includes the Brescia collaboration (Stefana, Marciano, Armstrong, Drolet) or only
  Armstrong et al.; whether STEL/ceiling values are handled.
- **Sources:** AIHA tool page; AIHA Apps-and-Tools index; Armstrong EPA slide deck; eLCOSH.

## 3. IRSST OEL Adjustment for Unusual Work Schedules — confidence: MEDIUM

- **Proposed category:** OEL Adjustment (new) · **Hazard:** Chemical · **Route:** Inhalation ·
  **Tool type:** Worker Exposure
- **Developer:** IRSST (Institut de recherche Robert-Sauvé en santé et en sécurité du travail,
  Québec). Guide T-22/T-21 authored by Daniel Drolet.
- **URL (confirm live):** https://www.irsst.qc.ca/en/_outil_100011.html
- **Draft description:** "A computer-based IRSST utility that computes the adjusted average exposure
  value (AAEV) for work schedules other than 8 h/day, 5 days/week, implementing IRSST Technical
  Guide T-22. Built for Québec's RSST permissible exposure values; adaptable to other limit
  systems."
- **Inputs:** the substance (with its IRSST adjustment category and 8-hr TWA PEV/VEMP) and the
  unusual schedule (hours/day, days/week).
- **Output:** the adjusted average exposure value (AAEV) and the substance's adjustment category.
- **Limitations:** only 8-hr TWA values adjusted (not ceiling/STEV); categories/values are specific
  to the Québec RSST list; other jurisdictions require adaptation.
- **Confirm before publishing:** exact tool title and input fields; web-based vs downloadable;
  current guide edition (T-22 3rd ed. 2008, with a ~2015 revision referenced elsewhere); whether
  biological agents are in scope.
- **Sources:** irsst.qc.ca tool page, Guide T-22 publication page, project pages, report R-168 PDF.

## 4. IHDA-AIHA (IH Data Analyst) — confidence: MEDIUM · _not in Andy's proposal_

From the earlier AIHA update list, not Andy's doc — include only if you want it.

- **Proposed category:** Validating Exposure Assessments · **Hazard:** Chemical · **Route:**
  Inhalation · **Tool type:** Worker Exposure
- **Developer:** Exposure Assessment Solutions, Inc. (EASi) — Paul Hewett, Ph.D., CIH
- **URL (confirm live):** aiha.org → AIHA Risk Assessment Tools → "ihda-aiha" (developer site:
  easinc.co)
- **Draft description:** "Windows statistical software for interpreting occupational exposure
  monitoring data: descriptive and compliance statistics, upper tolerance limits, non-detect
  (censored-data) methods, and Bayesian Decision Charts that assign the AIHA exposure control
  category (0–4). The AIHA-hosted edition is a free/limited edition for students and course
  participants."
- **Inputs:** small similar-exposure-group sampling datasets (airborne concentrations vs an OEL),
  including non-detects.
- **Output:** descriptive/decision statistics (e.g. UTL 95,95), goodness-of-fit, and Bayesian
  decision charts (probability of each AIHA category).
- **Confirm before publishing:** current version; exact outputs and the free vs commercial feature
  split; canonical URL (AIHA page vs easinc.co); whether to broaden beyond chemical/inhalation
  (the stats are agent-agnostic).
- **Sources:** AIHA IHDA-AIHA page and download page, AIHA apps index, Synergist, EASi site.

## 5. COVID-19 Exposure Assessment Tool (CEAT) — confidence: MEDIUM

- **Naming correction:** Andy's doc lists "COV-IRT LLC Exposure Assessment Tool." The authoritative
  name is **COVID-19 Exposure Assessment Tool (CEAT)**, developed by **Signature Science, LLC** (an
  SwRI subsidiary) with the COVID-19 International Research Team (COV-IRT).
- **Proposed category:** Pandemic Assessment (new) _or_ Preliminary / Initial · **Hazard:**
  Biological · **Route:** Inhalation · **Tool type:** Worker Exposure
- **URL (confirm live):** https://www.cov-irt.org/exposure-assessment-tool/
- **Draft description (based on AIHA's own wording):** "A free Beta tool that estimates a group's
  *relative* exposure to SARS-CoV-2 across activities, to show the relative importance of the
  factors that drive exposure. It combines mechanistic and epidemiological factors; distributed as
  an editable PDF with embedded JavaScript."
- **Inputs:** ~14 factors — emission/aerosol generation, aerosol decay and removal, ventilation,
  room volume, filtration, mask use/effectiveness, distance, group size, duration, and community
  epidemiology (prevalence, vaccination, testing).
- **Output:** a group-wide *relative* exposure/risk value vs a high-risk baseline — relative, not
  absolute, risk.
- **Confirm before publishing:** exact name/developer wording; current hosted version and whether
  still available; factor count (12 vs 14); the Science Advances citation.
- **Sources:** AIHA publications, cov-irt.org, PMC article, Signature Science press, SwRI podcast.

---

## Ready-to-insert directory entries (fill the blanks on confirmation)

```json
[
  {"name":"NIOSH Occupational Exposure Banding e-Tool","slug":"niosh-occupational-exposure-banding",
   "urls":["https://wwwn.cdc.gov/NIOSH-OEB/"],"description":"...","exposure_routes":"Inhalation",
   "agency":"NIOSH (CDC)","output":"...","category":"Preliminary / Initial Exposure Assessment",
   "hazard_type":["Chemical"],"tool_type":["Worker Exposure"]},
  {"name":"Toxico-kinetic Extended Shift OEL Adjustment","slug":"oel-adjustment-toxico-kinetic",
   "urls":[""],"description":"...","exposure_routes":"Inhalation","agency":"AIHA","output":"...",
   "category":"OEL Adjustment","hazard_type":["Chemical"],"tool_type":["Worker Exposure"]},
  {"name":"IRSST OEL Adjustment for Unusual Work Schedules","slug":"oel-adjustment-irsst",
   "urls":["https://www.irsst.qc.ca/en/_outil_100011.html"],"description":"...",
   "exposure_routes":"Inhalation","agency":"IRSST","output":"...","category":"OEL Adjustment",
   "hazard_type":["Chemical"],"tool_type":["Worker Exposure"]},
  {"name":"IHDA-AIHA (IH Data Analyst)","slug":"ihda-aiha","urls":[""],"description":"...",
   "exposure_routes":"Inhalation","agency":"Exposure Assessment Solutions, Inc. (Paul Hewett)",
   "output":"...","category":"Validating Exposure Assessments","hazard_type":["Chemical"],
   "tool_type":["Worker Exposure"]},
  {"name":"COVID-19 Exposure Assessment Tool (CEAT)","slug":"covid-19-exposure-assessment-tool-ceat",
   "urls":["https://www.cov-irt.org/exposure-assessment-tool/"],"description":"...",
   "exposure_routes":"Inhalation","agency":"Signature Science, LLC with COV-IRT","output":"...",
   "category":"Pandemic Assessment","hazard_type":["Biological"],"tool_type":["Worker Exposure"]}
]
```
