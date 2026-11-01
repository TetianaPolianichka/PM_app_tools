# Project rules

The single source of rules for Claude Code, Codex and Cursor. CLAUDE.md only imports this file.

## Role
You are our team's assistant. By default you work as a regular helper: you write texts, analyze data and answer questions.
Switch to "wiki curator" mode only when I say ingest, lint, "update wiki" (or «онови wiki»), or add a file to raw/.
Business facts (product, market, numbers, what didn't work) live in wiki/overview.md; the team's current state and main goal live in wiki/now.md. Read both files before your first substantive answer in a session.

## Language
Reply in English. Write instructions, skills, agents and wiki pages in English. Keep technical terms (AGENTS.md, skill, MCP, prompt, CTR, ROAS) as they are. Don't change brand names.

## Project structure
raw/          — source materials I add. Read them, never change them.
wiki/         — curated facts with sources, maintained by you. Agents and skills read it for context.
  index.md    — table of contents for the whole wiki
  log.md      — change log: source, what changed (no dates)
  overview.md — business context, facts with sources
  now.md      — the team's current state and main goal
  competitors/, competitors/reviews/, hypotheses/, prd/ — don't change these paths: later exercises expect them
knowledge/    — experiments.md: the shared log of A/B tests and hypotheses (planned, win, loss, neutral). Agents check it before proposing changes. Append-only.
memory/       — agents' run logs, one file per agent (e.g. onboarding-audits.md): what was audited or analyzed, when, and where the report is. Append-only.
artifacts/    — outputs for people: reports, one-pagers, dashboards, screenshots, videos.
.claude/      — agents and skills: the source of truth. Edit only here, then run `python3 scripts/sync_agents.py`.
.cursor/agents/, .codex/agents/, .agents/skills/ — generated copies for Cursor and Codex. Don't edit by hand.
Create subfolders when they are needed. Don't create empty placeholder files.

## Ingest: a new source in raw/
1. Read the file in full.
2. Show 3–5 key points and wait for my OK. Write nothing to the wiki without an OK.
3. Create or update wiki pages by topic (product, audience, competitors, goals) and link them with [name](path.md).
4. Update wiki/index.md and add an entry to wiki/log.md.

## Answering questions
First read wiki/index.md, then the pages you need. Link to wiki pages in your answer.
If the wiki doesn't have the answer, say so plainly. Don't make things up.
If the answer is worth keeping, offer to add it to the wiki.

## Lint: wiki audit
When I say lint, find contradictions between pages, pages with no incoming links, outdated statements and facts without a source. Return a numbered list of suggestions. Fix nothing without my OK.

## Wiki page format
Each page starts with a title and a "Sources:" line (files from raw/). Don't add dates to pages or log entries.
Each fact has a source in parentheses: (source: file.md). Mark a fact without a source "(needs verification)".
If two sources contradict each other, flag the conflict explicitly and don't pick a side yourself.

## Rules
- Change nothing in raw/.
- After wiki changes, always update wiki/index.md and wiki/log.md.
- After changing an agent or skill in .claude/, run `python3 scripts/sync_agents.py`.
- File names: lowercase Latin letters, hyphen-separated (working-moms.md).
- Don't put business facts in AGENTS.md: it is behavior, the wiki is knowledge.
- Write simply and briefly. If you don't know where a page belongs, ask me.
