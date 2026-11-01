# PM App Tools

A workspace for product managers auditing and growing mobile apps (iOS and Android), for Claude Code, Cursor and Codex. It bundles agents, skills and a Markdown wiki so the AI runs UX audits, competitor analysis, user feedback analysis, A/B test planning and App Store monitoring the same way every time, with a source for every fact.

The toolkit is **domain-agnostic**: industry, audience and business model come from an audit config or from the sources you add. The AI does not assume them.

## What it can do

| Task | How to start | Powered by |
|---|---|---|
| Onboarding audit: friction points, top-3 competitor benchmark, 10+ low-code improvements | "onboarding audit of X", a Figma link, or screenshots in `pending_audit/` | `onboarding-auditor` agent + `audit-sources`, `audit-scoring`, `audit-benchmarks` skills |
| UX audit outside onboarding: paywall, settings, key flow, empty and error states | "UX audit" + Figma link or screenshots | `ux-auditor` skill |
| User feedback analysis: themes, sentiment, trends, prioritized problems and hypotheses | "analyze reviews", "feedback analysis", or exports in `feedback/` | `feedback-analyst` agent |
| Competitor analysis from public App Store and Google Play data | `/competitor-analysis`, "go!" or "погнали!" | `competitor-analysis` skill |
| A/B tests: hypothesis, sample size, duration, SRM, significance, guardrails | Paste test numbers or ask about an experiment | `ab-testing` skill + `stats.py` |
| Weekly App Store monitoring vs competitors | "weekly App Store report" | `app-store-collector` agent (data collection only) |
| Knowledge base upkeep | `ingest`, `lint`, "update wiki" | Rules in `AGENTS.md` |

## Getting started

**Requirements:** one of [Claude Code](https://claude.com/claude-code), Cursor or Codex, plus Python 3.9+ for the two scripts. Both use only the standard library, so there's nothing to install.

1. Clone the repo and open the folder in your tool.
2. Add a source file to `raw/` and say `ingest`. The AI shows the key points and writes to the wiki only after your OK.
3. Run any task from the table above.

### Optional connectors

Agents use whatever MCP connectors are attached in your tool and work without them. Useful ones: Figma (read-only, for audits), Mobbin (UX references), PostHog, Tableau, AppTweak, Zendesk and Jira (feedback analysis), Purchasely (experiments), Google Sheets and Gmail (weekly monitoring). Status is tracked in [wiki/tooling.md](wiki/tooling.md).

## Project structure

```
.
├── AGENTS.md               # Project rules for every tool: role, folders, wiki rules, language
├── CLAUDE.md               # One line: imports AGENTS.md for Claude Code
├── raw/                    # Source materials you add. Read-only for the AI
├── wiki/                   # Curated facts with sources, maintained by the AI
│   ├── index.md            # Table of contents
│   ├── log.md              # Change log: source, what changed
│   ├── audit-framework.md  # Audit framework v1.1: 12 modules, config, evidence labels
│   ├── tooling.md          # Connectors, skills, agents and their status
│   └── competitors/        # Competitor reports
├── knowledge/
│   └── experiments.md      # Shared log of A/B tests and hypotheses (append-only)
├── memory/
│   └── onboarding-audits.md # Agents' run logs, one file per agent (append-only)
├── artifacts/              # Outputs for people: reports, one-pagers, dashboards
├── scripts/
│   └── sync_agents.py      # Generates the Cursor and Codex copies from .claude/
├── .claude/                # Source of truth for agents and skills
│   ├── settings.json       # Permissions (raw/ is write-protected)
│   ├── agents/
│   └── skills/             # Skills with references and scripts (incl. stats.py)
├── .cursor/agents/         # Generated: agents for Cursor
├── .codex/agents/          # Generated: agents for Codex (TOML)
└── .agents/skills/         # Generated: skills for Codex
```

## Claude Code, Cursor and Codex

| | Claude Code | Cursor | Codex |
|---|---|---|---|
| Project rules | `CLAUDE.md` → `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| Agents | `.claude/agents/*.md` | `.cursor/agents/*.md` | `.codex/agents/*.toml` |
| Skills | `.claude/skills/` | `.claude/skills/` (read natively) | `.agents/skills/` |

Edit agents and skills only in `.claude/`, then regenerate the other copies:

```bash
python3 scripts/sync_agents.py
```

## Audit framework

The core method lives in [wiki/audit-framework.md](wiki/audit-framework.md). It has 12 modules, each going Inputs → Method → Output → "So what?":

4.1 Value Proposition · 4.2 Market · 4.3 Audience · 4.4 Personas · 4.5 JTBD · 4.6 Metrics · 4.7 Store / ASO · 4.8 Competitors · 4.9 UX audit · 4.10 Surveys · 4.11 Flow analytics · 4.12 Synthesis

Rules that apply to every module:

- No invented numbers. Data comes from connected tools first, then uploaded files, then web search, then a labeled estimate.
- Every fact is labeled by evidence type (`[Verified]`, `[Third-party]`, etc.) and cites its source.
- Every report ends with: data sources used, confidence summary, data gaps.

## A/B test calculator

```bash
# Sample size per arm: 5% baseline, +10% relative lift
python3 .claude/skills/ab-testing/scripts/stats.py size 0.05 0.10

# Sample ratio mismatch check
python3 .claude/skills/ab-testing/scripts/stats.py srm 10120 9880

# Compare conversion: control A vs variant B
python3 .claude/skills/ab-testing/scripts/stats.py prop 500 10000 560 10000

# Test duration: users per arm, number of arms, daily users
python3 .claude/skills/ab-testing/scripts/stats.py duration 31000 2 4000

# Guardrail (non-inferiority) check
python3 .claude/skills/ab-testing/scripts/stats.py guardrail 120 10000 130 10000 --margin 0.005 --harm up
```

## Wiki conventions

- Each page starts with a title and a `Sources:` line (source files). Pages and log entries carry no edit dates.
- Each fact cites its source; unverified facts are marked "(needs verification)".
- Conflicts between sources are flagged, not resolved silently.
- After any wiki change, `index.md` and `log.md` are updated.
- File names: lowercase Latin, hyphen-separated.

## Language

Instructions, skills, agents and wiki pages are written in English. The AI replies in English and keeps technical terms (CTR, ROAS, MCP) and brand names as they are.
