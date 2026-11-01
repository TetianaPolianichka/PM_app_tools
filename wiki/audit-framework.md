# Mobile App Audit Framework

Sources: raw/context_raw.md (v1.1)

A reusable, **domain-agnostic** toolkit for evidence-based audits of any iOS or Android app, whatever its category, business model or market (source: context_raw.md). Version 1.1, owner field left empty in the source (source: context_raw.md).

## Principles
- **No default assumptions:** industry, audience, business model and channel come only from the Audit Config, or are discovered during the audit and labeled (source: context_raw.md)
- **Channels:** if the config lists several distribution channels, assess each separately where audiences, metrics or value props differ (source: context_raw.md)
- **Domain specifics** enter only through a domain variant, never assumed (source: context_raw.md)

## Operating rules
- Read the Audit Config first; if required fields are empty, ask one short question (source: context_raw.md)
- Never invent numbers; tool order: connected data tools → uploaded files → web search → labeled estimate (source: context_raw.md)
- Cite sources for every external fact; each module ends with "So what?" and P0/P1/P2 actions (source: context_raw.md)

## Audit Config fields
- **app:** name, bundle_ids (ios, android), category, domain, domain_variant, business_model (freemium / subscription / ads / one-time / transactional / hybrid / other), distribution_channels, customer_types, launch_date, current_stage (source: context_raw.md)
- **scope:** modules, depth (quick / standard / deep), platforms (source: context_raw.md)
- **markets:** top_geos (3), primary_language (source: context_raw.md)
- **competitors:** up to 5, or empty so Claude proposes them (source: context_raw.md)
- **data_access:** analytics, store_consoles, revenue, market_intel, research_files (source: context_raw.md)
- **goals:** audit_question, decision_owner, deadline (source: context_raw.md)

## Evidence labels
| Label | Meaning |
|---|---|
| [Verified] | First-party data or official source |
| [Third-party] | Market-intelligence tool or published report |
| [Estimated] | Calculated from proxies, formula shown |
| [Assumption] | Hypothesis to validate |

Estimates show formulas, metrics carry date ranges, conflicting sources are shown side by side (source: context_raw.md)

## Modules (Inputs → Method → Output → So what?)
| # | Module | Core method / output |
|---|---|---|
| 4.1 | Value Proposition | Value Proposition Canvas; stated vs perceived gap; separate prop per customer type or channel if the config lists several |
| 4.2 | Market | TAM/SAM/SOM top-down and bottom-up, trends, regulation |
| 4.3 | Audience | 3–5 segments by needs and behavior first |
| 4.4 | Personas | 2–3 max, marked evidence-based or proto-persona |
| 4.5 | JTBD | 1 core job + 3–5 related; job map; opportunity score = importance + max(importance − satisfaction, 0) |
| 4.6 | Metrics | NSM → input → feature metrics; dashboard with 🟢🟡🔴; channel metrics if several channels; domain metrics if a variant is set |
| 4.7 | Store / ASO | Per top-3 geo × platform scorecard; review theme clustering; ASO quick wins |
| 4.8 | Competitors | Top 5 (direct + 1 indirect), matrix, positioning map |
| 4.9 | UX audit | Nielsen heuristics (severity 0–4), HIG / Material, accessibility, trust cues |
| 4.10 | Surveys | NPS, CSAT, CES, Sean Ellis PMF, Van Westendorp |
| 4.11 | Flow analytics | Funnels, drop-offs, experiments; tracking plan if no data |
| 4.12 | Synthesis | Exec summary, SWOT, RICE backlog, 30/60/90 roadmap (always last) |

All rows (source: context_raw.md)

## Commands
`full audit`, `quick audit`, `module: <name>`, `compare: A vs B`, `review mining: <geo>`, `survey: design <goal>`, `update: <module>` (source: context_raw.md)

## Outputs
Chat with tables (default), report, presentation, spreadsheet, visuals. Every report ends with: Data sources used · Confidence summary · Data gaps (source: context_raw.md)

## Benchmarks (general mobile apps, verify before use)
- Crash-free users ≥ 99.5%; store rating ≥ 4.3; Android ANR below Google Play bad-behavior threshold (source: context_raw.md)
- D1/D30 retention and trial → paid: category-dependent (source: context_raw.md)

## Domain variants
- Fill the template and reference it by name in `domain_variant` (source: context_raw.md)
- Template fields: name, applies_to, extra_metrics (→ 4.6), extra_ux_checks (→ 4.9), regulations, competitor_criteria (→ 4.8), research_questions (→ 4.10), benchmarks_source (source: context_raw.md)
- If no variant is set, Claude may propose one as [Assumption] and must ask before applying it (source: context_raw.md)
- No variants are defined yet. v1.0 had a security / fintech example; it was removed in v1.1 (source: context_raw.md)

## Related
- [Tooling](tooling.md)
