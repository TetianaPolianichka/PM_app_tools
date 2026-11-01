---
name: audit-sources
description: Sources and connectors for an onboarding UX audit. How to detect the source (Figma MCP, pending_audit/, Figma + screenshots), which Figma tools to call read-only, where to get competitor screenshots. Call at the start of an onboarding audit, before reading any screens.
user-invocable: false
---

# Audit sources

Detect the source automatically.

- **Figma.** If the request has a Figma link, work through the Figma MCP, read-only:
  - `get_metadata` — onboarding frames and their order;
  - `get_screenshot` — an image of each screen;
  - `get_design_context` — exact copy, sizes, components;
  - `get_variable_defs` — colors for exact contrast calculation.
  - Never change the Figma file. Don't call tools that write to Figma (`use_figma`, `upload_assets`, `send_code_to_figma`, etc.).
  - If the Figma MCP is unavailable, say so in one sentence and offer screenshots instead.
- **`pending_audit/`.** If there's no link, take screenshots from there. Screen order follows file names (`01-...png`, `02-...png`).
- **Figma + screenshots.** Analyze both sources and add a "Design vs implementation differences" section to the report.
- **No source at all.** Ask one short question. Don't invent anything.
- **Competitors.** `competitors_screens/<name>/01-...png`, one subfolder per competitor.
  - More than three — ask which three to use.
  - Fewer than three — work with what's there and state this limitation explicitly (it affects condition (b) for High in the `audit-scoring` skill).

Only read screenshots in `pending_audit/` and `competitors_screens/`.
