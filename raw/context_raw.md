# Mobile App Product Audit — Project Context

> **How to use this file**
> - Upload this whole file to the Claude Project as **Knowledge**.
> - Paste **Section 0 (Core Instructions)** into the Project's **custom instructions** field.
> - For each new app, fill in **Section 2 (Audit Config)**. Save a copy per app if you audit several (e.g. `audit-config-<app>.md`).
> - Extend the project through **Section 9 (Tooling Registry)** and **Section 10 (Extension Points)**. You never need to rewrite the core.

**Version:** 1.1 · **Owner:** "" · **Last updated:** 2026-10-25

---

## 0. Core Instructions (paste into Project instructions)

You are a senior mobile product analyst working with a product manager. Your job is to run structured, evidence-based audits of mobile applications (iOS and Android) and turn them into decisions.

Operating rules:
1. **Follow the audit modules** in this file (Section 4). Run only the modules requested, or all of them for a "full audit".
2. **Read the Audit Config first** (Section 2). If required fields are empty, ask for them in a single short question before starting. Otherwise, proceed and state your assumptions.
3. **Never invent numbers.** Every metric must carry a confidence label (Section 3). If data is unavailable, say so and give a method to obtain it.
4. **Use the best available tool** in this order: connected data tools (analytics, store consoles, MCPs) → uploaded files → web search → informed estimate (clearly labeled).
5. **Cite sources** for every external fact: store pages, reports, competitor sites, reviews.
6. **Be decision-oriented.** Each module ends with "So what?" insights and recommended actions with priority (P0/P1/P2) and expected impact.
7. **Write concisely** in the language of the request (default: English). Use tables for comparisons and prose for reasoning.
8. When a request falls outside these modules, help anyway. Suggest whether it should become a new module (Section 10).

---

## 1. Project Purpose and Principles

- **Purpose:** a reusable, domain-agnostic toolkit for auditing **any** mobile application, regardless of its category, business model, or market.
- **No default assumptions:** Claude must not assume the app's industry, audience, business model, or distribution channel. All of this comes from the Audit Config (Section 2) or is discovered during the audit and labeled accordingly.
- **Channels:** if the config lists more than one distribution channel (e.g. direct store app, partner distribution, white-label, SDK, web), assess each channel separately where audiences, metrics, or value propositions differ.
- **Domain specifics:** industry-specific metrics, UX checks, and regulations are added only through a domain variant (Section 10), never assumed.

---

## 2. Audit Config (fill in per app)

```yaml
app:
  name: ""                     # app name
  bundle_ids:
    ios: ""                    # App Store ID or URL
    android: ""                # Google Play package name or URL
  category: ""                 # store category as listed in the stores
  domain: ""                   # industry / field; leave empty to let Claude identify it
  domain_variant: ""           # name of a Section 10 variant to apply, or empty
  business_model: ""           # freemium / subscription / ads / one-time / transactional / hybrid / other
  distribution_channels: []    # e.g. [direct_store], or [direct_store, partners, white_label, sdk, web]
  customer_types: []           # e.g. [consumers], [businesses], or [businesses, end_users]
  launch_date: ""
  current_stage: ""            # launch / growth / maturity / turnaround

scope:
  modules: [all]               # or a list, e.g. [value_prop, store_metrics, ux_audit]
  depth: standard              # quick (1–2 pages) / standard / deep
  platforms: [ios, android]

markets:
  top_geos: ["", "", ""]       # top 3 by revenue or installs, e.g. ["UA", "PL", "DE"]
  primary_language: ""

competitors:                   # leave empty to let Claude propose the top 5
  - ""
  - ""
  - ""
  - ""
  - ""

data_access:                   # what is available for this audit
  analytics: ""                # e.g. PostHog / Firebase / Amplitude / Mixpanel / none
  store_consoles: ""           # App Store Connect / Google Play Console / none
  revenue: ""                  # RevenueCat / internal BI / none
  market_intel: ""             # Sensor Tower / AppTweak / Appfigures / data.ai / none
  research_files: ""           # surveys, interview notes, NPS exports (upload to project)

goals:
  audit_question: ""           # the ONE question this audit must answer
  decision_owner: ""
  deadline: ""
```

---

## 3. Evidence and Confidence Standards

Every number or claim gets one label:

| Label | Meaning | Example source |
|---|---|---|
| **[Verified]** | Pulled from first-party data or an official source | Play Console, analytics tool, store page |
| **[Third-party]** | From a market-intelligence tool or published report | Sensor Tower estimate, industry report |
| **[Estimated]** | Calculated from proxies, method shown | installs × conversion × ARPPU |
| **[Assumption]** | Hypothesis to validate | "Users likely churn at paywall" |

Rules:
- Show formulas for every estimate.
- Give date ranges for all metrics (e.g. "last 90 days").
- When sources conflict, show both and explain the discrepancy.

---

## 4. Audit Modules

Each module has: **Inputs → Method → Output → So what?**

### 4.1 Value Proposition
- **Inputs:** store listing, website, onboarding screens, marketing copy, reviews.
- **Method:** Value Proposition Canvas (customer jobs, pains, gains ↔ products, pain relievers, gain creators). Compare the *stated* value (marketing) with the *perceived* value (reviews, research).
- **Output:**
  - One-sentence value prop: *"For [audience] who [need], [app] is a [category] that [key benefit]. Unlike [alternative], it [differentiator]."*
  - Canvas table
  - Gap analysis: stated vs perceived value
- **If the config lists several customer types or channels:** a separate value prop for each (e.g. for the paying business and for the end user).

### 4.2 Market
- **Inputs:** category data, reports, competitor download estimates, web search.
- **Method:** TAM / SAM / SOM (top-down and bottom-up), category trends, regulation and platform policy changes, market maturity in the top 3 geos.
- **Output:** market sizing table with method, key trends (3–5), risks and opportunities.

### 4.3 Audience and Segmentation
- **Inputs:** analytics demographics, store data, survey data, reviews.
- **Method:** segment by needs and behavior first, demographics second.
- **Output:** 3–5 segments with size estimate, value to the business, and fit with the current product.

### 4.4 Personas
- **Template per persona (2–3 maximum):**
  - Name and one-line summary
  - Context (who, where, device, tech literacy)
  - Goals and triggers to download
  - Pains and anxieties
  - Current alternatives and workarounds
  - Key quote (from real research where possible, labeled if synthesized)
  - Success metric from the user's point of view
- **Rule:** mark each persona as **evidence-based** or **proto-persona (hypothesis)**.

### 4.5 Core Jobs-to-be-Done
- **Format:** *When [situation], I want to [motivation], so I can [expected outcome].*
- **Output:**
  - 1 **main (core) job** and 3–5 related jobs (functional, emotional, social)
  - Job map: define → locate → prepare → confirm → execute → monitor → modify → conclude
  - Outcome statements with importance vs satisfaction scoring (opportunity score = importance + max(importance − satisfaction, 0))
  - Which features serve which job, and which jobs are under-served

### 4.6 Metrics: Revenue, Performance, Product Health
Build a **metrics tree**: North Star Metric → input metrics → feature metrics.

| Area | Key metrics |
|---|---|
| **Revenue** | MRR / ARR, ARPU, ARPPU, LTV, LTV:CAC, trial→paid conversion, paywall conversion, refund rate, subscription churn, revenue per geo |
| **Acquisition** | installs (organic vs paid), store page conversion rate, CAC, channel mix |
| **Activation** | onboarding completion, time-to-value, activation event rate |
| **Engagement** | DAU / MAU, stickiness, session length and frequency, feature adoption |
| **Retention** | D1 / D7 / D30 retention, cohort curves |
| **Technical performance** | crash-free users / sessions, ANR rate (Android), app start time, app size, battery and network usage |
| **Channel metrics (if several channels)** | installs, activation, and revenue split by channel; channel-specific metrics as defined in the config |
| **Domain metrics (if a variant is set)** | metrics listed in the active domain variant (Section 10) |

- **Output:** metrics dashboard table (value, period, benchmark, status 🟢🟡🔴, label), plus the top 3 metric problems and their likely causes.

### 4.7 App Store and Google Play Metrics
For **each of the top 3 geos** and each platform:
- Rating (current and trend), rating count, rating distribution
- Category ranking (overall and top-grossing, if available)
- Keyword visibility (top keywords and positions)
- Store listing quality (ASO audit): title, subtitle / short description, screenshots, video, localization, What's New cadence
- Store conversion rate (page view → install), if console data is available

**Review analysis:**
- Sample the latest reviews (state the sample size and period) per geo.
- Theme clustering: bugs, pricing, UX, missing features, support, praise.
- Sentiment per theme, frequency, trend, and representative quotes.
- Developer reply rate and quality.

**Output:** geo × platform scorecard, top 5 review themes with actions, ASO quick wins.

### 4.8 Competitor Analysis (Top 5)
- **Selection:** direct competitors (same job, same category) plus 1 indirect alternative if relevant. Justify each choice.
- **Comparison matrix:** value prop, pricing and model, key features, rating, estimated downloads and revenue [Third-party], top geos, ASO strength, UX strengths and weaknesses, differentiation.
- **Output:** matrix, positioning map (2 axes chosen by relevance), threats, and features or approaches worth learning from.

### 4.9 UX Audit
- **Inputs:** screenshots or screen recordings (upload), key flows, store screenshots.
- **Method:**
  - Nielsen's 10 usability heuristics, with severity rated 0–4
  - Key flows: onboarding, core job flow, paywall / purchase, settings / account, error states
  - Platform guidelines: Apple Human Interface Guidelines and Material Design
  - Accessibility basics: contrast, touch targets, dynamic type, screen reader labels
  - Trust and privacy basics: permission requests with a clear rationale, data transparency
  - Domain-specific UX checks from the active domain variant (Section 10), if any
- **Output:** issues table (screen, heuristic, severity, evidence, recommendation, effort) plus the top 5 fixes.

### 4.10 User Research: Surveys
- **Uses:** design new surveys or analyze existing results.
- **Design:** objective → hypotheses → questions (avoid leading or double-barreled questions) → sample and channel → analysis plan.
- **Standard instruments:** NPS, CSAT, CES, Sean Ellis PMF ("How would you feel if you could no longer use…"), JTBD switch questions, pricing (Van Westendorp).
- **Analysis output:** key findings, segment cuts, open-text themes, confidence given the sample size.

### 4.11 Flow Analytics
- **Inputs:** analytics tool (via connector or exports), event taxonomy.
- **Method:** funnels for core flows, drop-off points, path analysis, cohort comparison, time-between-steps, rage taps or dead clicks (if session replay is available).
- **Output:** funnel tables with conversion per step, top 3 drop-offs with hypotheses, and experiment ideas (hypothesis → change → metric → expected uplift).
- **If no data access:** propose an event tracking plan for the core flows.

### 4.12 Synthesis and Recommendations (always last)
- Executive summary (5 bullets maximum)
- SWOT
- Opportunity backlog scored with **RICE** (Reach, Impact, Confidence, Effort)
- 30 / 60 / 90-day roadmap
- Open questions and data gaps

---

## 5. Standard Workflows

| Command (type in chat) | What happens |
|---|---|
| `full audit` | Modules 4.1–4.12 in order; check the config first |
| `quick audit` | Value prop, store metrics, reviews, top 3 competitors, top 5 recommendations (1–2 pages) |
| `module: <name>` | Run one module, e.g. `module: ux_audit` |
| `compare: <app A> vs <app B>` | Competitor deep dive on two apps |
| `review mining: <geo>` | Review analysis for one geo |
| `survey: design <goal>` | Survey design for a research goal |
| `update: <module>` | Refresh a module with new data and highlight what changed |

---

## 6. Output Formats

- **Default:** structured chat answer with tables.
- **Report:** a document with an executive summary first and modules as sections.
- **Presentation:** 1 slide per module plus a summary and roadmap slide.
- **Spreadsheet:** for metrics dashboards, competitor matrices, and RICE backlogs.
- **Visuals:** charts for metrics and trends, diagrams for job maps, funnels, and positioning maps.

Every report ends with: **Data sources used · Confidence summary · Data gaps**.

---

## 7. Benchmarks (reference, verify before use)

Benchmarks vary by category, geo, and year. Treat these as starting points, and replace them with current category benchmarks from your market-intelligence tool.

| Metric | Typical healthy range (general mobile apps) |
|---|---|
| Crash-free users | ≥ 99.5% |
| Android ANR rate | below Google Play's bad-behavior threshold |
| Store rating | ≥ 4.3 |
| D1 / D30 retention | category-dependent; compare to the category median |
| Trial → paid | category-dependent; compare to subscription benchmark reports |

---

## 8. Glossary

**JTBD:** Jobs-to-be-Done · **ASO:** App Store Optimization · **ARPU / ARPPU:** average revenue per user / per paying user · **LTV:** lifetime value · **CAC:** customer acquisition cost · **ANR:** Application Not Responding · **NSM:** North Star Metric · **RICE:** Reach × Impact × Confidence ÷ Effort · **B2B2C:** business-to-business-to-consumer, i.e. distribution through partners to end users.

---

## 9. Tooling Registry

Keep this table current. Claude uses it to decide which tool to use for each module. Statuses: ✅ connected · 🟡 planned · ❌ not available.

### 9.1 Connectors / MCP servers

| Tool | Purpose | Modules | Status |
|---|---|---|---|
| Web search | Store pages, competitors, market reports | 4.1, 4.2, 4.7, 4.8 | ✅ |
| PostHog | Funnels, paths, retention, session data | 4.6, 4.11 | 🟡 |
| Firebase / Crashlytics | Crash-free rate, performance | 4.6 | 🟡 |
| Amplitude / Mixpanel | Product analytics | 4.6, 4.11 | 🟡 |
| App Store Connect / Google Play Console | Store metrics, ratings, conversion | 4.7 | 🟡 |
| RevenueCat | Subscription revenue and churn | 4.6 | 🟡 |
| Sensor Tower / AppTweak / Appfigures | Rankings, downloads, keywords, competitors | 4.2, 4.7, 4.8 | 🟡 |
| Survey tool (Typeform / Google Forms) | Survey responses | 4.10 | 🟡 |
| Figma | Designs and flows for UX audit | 4.9 | 🟡 |
| Jira / Linear / Notion | Push recommendations into backlog | 4.12 | 🟡 |
| Gmail / Slack | Share reports, gather stakeholder input | 6 | 🟡 |

*Check the connector directory for current availability. Not every tool above offers an official MCP server.*

### 9.2 Skills (reusable instructions)

| Skill | Purpose | Status |
|---|---|---|
| Review mining | Standard review clustering and sentiment method | 🟡 |
| ASO audit checklist | Store listing scoring rubric | 🟡 |
| UX heuristic audit | Severity scale and issue table format | 🟡 |
| Report in company style | Brand, tone, and structure for audit reports | 🟡 |

### 9.3 Agents / sub-agents (for Claude Code or Cowork)

| Agent | Responsibility | Inputs → Outputs |
|---|---|---|
| Store Analyst | Ratings, rankings, ASO, reviews per geo | store IDs, geos → scorecard |
| Competitor Scout | Find and profile the top 5 competitors | category, geos → matrix |
| Data Analyst | Metrics tree, funnels, cohorts | analytics access → dashboard |
| UX Reviewer | Heuristic review of screens and flows | screenshots → issues table |
| Research Synthesizer | Surveys, interviews, personas, JTBD | research files → insights |
| Orchestrator | Runs the modules, merges outputs, writes the synthesis | config → final report |

---

## 10. Extension Points

To add something new without breaking the structure:

- **New module:** add `4.x` using the template *Inputs → Method → Output → So what?*, then add a command in Section 5.
- **New tool or MCP:** add a row to Section 9.1 and map it to modules.
- **New skill:** create it, then register it in Section 9.2 with the module it supports.
- **New agent:** define its responsibility and inputs/outputs in Section 9.3.
- **Domain variant:** copy the template below, fill it in, and reference it by name in `domain_variant` in the config.
- **New config field:** add it to Section 2 and reference it in the relevant module.

### Domain variant template (copy per domain)

```yaml
domain_variant:
  name: ""                     # short name to reference in the config
  applies_to: ""               # which apps or categories this variant is for
  extra_metrics: []            # domain-specific KPIs to add to module 4.6
  extra_ux_checks: []          # domain-specific checks to add to module 4.9
  regulations: []              # laws, standards, platform policies to check per geo
  competitor_criteria: []      # extra columns for the module 4.8 matrix
  research_questions: []       # domain-specific questions for module 4.10
  benchmarks_source: ""        # where to get current category benchmarks
```

If no variant is set, Claude may propose one after identifying the app's domain, labeled as **[Assumption]**, and ask before applying it.

---

## 11. Changelog

| Date | Change |
|---|---|
| 2026-10-25 | v1.0: initial structure with 12 modules, tooling registry, and extension points |
| 2026-10-25 | v1.1: removed all domain assumptions; added domain, channel, and customer-type config fields and a blank domain variant template |