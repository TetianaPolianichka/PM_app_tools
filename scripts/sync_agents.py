#!/usr/bin/env python3
"""Generate Cursor and Codex copies of the agents and skills in .claude/.

.claude/ is the source of truth. Run this after changing any agent or skill:

    python3 scripts/sync_agents.py

It rewrites .cursor/agents/, .codex/agents/ and .agents/skills/ from scratch.
Standard library only (Python 3.9+).
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_AGENTS = ROOT / ".claude/agents"
SRC_SKILLS = ROOT / ".claude/skills"
CURSOR_AGENTS = ROOT / ".cursor/agents"
CODEX_AGENTS = ROOT / ".codex/agents"
CODEX_SKILLS = ROOT / ".agents/skills"

# Claude-only tool names, reworded so the same text works in Cursor and Codex.
NEUTRAL = [
    ("Call them via Skill only when you reach the matching step:", "Use them only when you reach the matching step:"),
    ("| Read; use Bash with Python for counting.", "| Read them; use Python in the terminal for counting."),
    ("| WebFetch `", "| Fetch `"),
    ("Open each `url` with WebFetch.", "Open each `url` with web fetch."),
    ('run WebSearch "', 'run a web search for "'),
]
CLAUDE_ONLY = re.compile(r"\b(WebFetch|WebSearch|via Skill|Bash)\b")

# Per-agent settings that only exist in one tool. Model choice is left to each tool.
CURSOR_EXTRA = {"app-store-collector": "readonly: true\n"}
CODEX_EXTRA = {"app-store-collector": "\n[features]\nshell_tool = false\n"}

# Skill frontmatter fields Codex doesn't document.
CODEX_SKIP_FIELDS = re.compile(r"^(user-invocable|model): .*\n", re.M)


def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n\n?(.*)", text, re.S)
    if not m:
        raise ValueError("missing frontmatter")
    fields = dict(re.findall(r"^([\w-]+): (.*)$", m.group(1), re.M))
    return fields, m.group(2)


def neutral(body, name):
    for old, new in NEUTRAL:
        body = body.replace(old, new)
    leftover = CLAUDE_ONLY.search(body)
    if leftover:
        raise SystemExit(f"{name}: Claude-only term '{leftover.group(0)}' left; add a rewrite to NEUTRAL")
    return body.rstrip() + "\n"


def toml_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def reset(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def sync_agents():
    reset(CURSOR_AGENTS)
    reset(CODEX_AGENTS)
    for src in sorted(SRC_AGENTS.glob("*.md")):
        fields, body = split_frontmatter(src.read_text())
        name, description = fields["name"], fields["description"]
        body = neutral(body, name)
        if "'''" in body:
            raise SystemExit(f"{name}: body contains ''' and can't be a TOML literal string")

        (CURSOR_AGENTS / f"{name}.md").write_text(
            f"---\nname: {name}\ndescription: {description}\nmodel: inherit\n"
            f"{CURSOR_EXTRA.get(name, '')}---\n\n{body}"
        )
        (CODEX_AGENTS / f"{name}.toml").write_text(
            f"name = {toml_string(name)}\ndescription = {toml_string(description)}\n"
            f"developer_instructions = '''\n{body}'''\n{CODEX_EXTRA.get(name, '')}"
        )
        print(f"agent  {name}")


def sync_skills():
    if CODEX_SKILLS.exists():
        shutil.rmtree(CODEX_SKILLS)
    shutil.copytree(SRC_SKILLS, CODEX_SKILLS, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    for path in CODEX_SKILLS.rglob("*.md"):
        text = path.read_text().replace(".claude/skills/", ".agents/skills/")
        if path.name == "SKILL.md":
            text = CODEX_SKIP_FIELDS.sub("", text)
            print(f"skill  {path.parent.name}")
        path.write_text(text)


if __name__ == "__main__":
    sync_agents()
    sync_skills()
    print("Done. Cursor reads skills from .claude/skills/ directly.")
