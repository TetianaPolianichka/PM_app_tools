# Tooling Registry

Sources: raw/context_raw.md (v1.1), .claude/skills/competitor-analysis/SKILL.md, .claude/agents/feedback-analyst.md

Status as of v1.1 of the framework (source: context_raw.md). Used by the [audit framework](audit-framework.md).

## Connectors / MCP
| Tool | Modules | Status |
|---|---|---|
| Web search | 4.1, 4.2, 4.7, 4.8 | ✅ connected |
| PostHog | 4.6, 4.11 | 🟡 planned |
| Firebase / Crashlytics | 4.6 | 🟡 planned |
| Amplitude / Mixpanel | 4.6, 4.11 | 🟡 planned |
| App Store Connect / Google Play Console | 4.7 | 🟡 planned |
| RevenueCat | 4.6 | 🟡 planned |
| Sensor Tower / AppTweak / Appfigures | 4.2, 4.7, 4.8 | 🟡 planned |
| Typeform / Google Forms | 4.10 | 🟡 planned |
| Figma | 4.9 | 🟡 planned |
| Jira / Linear / Notion | 4.12 | 🟡 planned |
| Gmail / Slack | outputs | 🟡 planned |

All rows (source: context_raw.md)

## Skills
| Skill | Modules | Status |
|---|---|---|
| competitor-analysis: competitor analysis from App Store and Google Play data, report in `wiki/competitors/`; trigger: "go!", «погнали!» or `/competitor-analysis` | 4.7, 4.8 | ✅ created, not tested yet (source: .claude/skills/competitor-analysis/SKILL.md) |
| Review mining | 4.7 | 🟡 planned |
| ASO audit checklist | 4.7 | 🟡 planned |
| UX heuristic audit | 4.9 | 🟡 planned |
| Report in company style | outputs | 🟡 planned |

Planned rows (source: context_raw.md)

## Agents
Store Analyst, Competitor Scout, Data Analyst, UX Reviewer, Research Synthesizer, Orchestrator (runs modules and writes synthesis) (source: context_raw.md)

| Agent | Modules | Status |
|---|---|---|
| feedback-analyst: themes, frequency, sentiment and trends from store reviews, surveys (NPS, CSAT, PostHog) and tickets; uses PostHog, Tableau, AppTweak, Zendesk and Jira (issue status), all read-only, when those MCPs are connected; report in `artifacts/feedback/`; trigger: "analyze reviews", "review mining", "feedback analysis" | 4.7, 4.10 | ✅ created, not tested yet (source: .claude/agents/feedback-analyst.md) |

All agents also have Cursor versions (`.cursor/agents/`) and Codex versions (`.codex/agents/`); all skills have Codex copies in `.agents/skills/`, and Cursor reads `.claude/skills/` directly (source: README.md).
