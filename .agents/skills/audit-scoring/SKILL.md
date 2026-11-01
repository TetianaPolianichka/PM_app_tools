---
name: audit-scoring
description: Scoring for UX audits. Shared base for onboarding-auditor and ux-auditor — Nielsen heuristics table H1–H10 and the 0–4 severity scale. For onboarding also — HIG/Material, accessibility, checklist, friction points, High/Medium criteria, low-code, improvement format and ICE. Call during any UX audit when scoring screens, logging issues or friction points, or building a list of improvements.
---

# UX audit scoring

## 0. Shared base (for all audits)

### Nielsen heuristics

| # | Heuristic | What to check |
|---|---|---|
| H1 | Visibility of system status | Progress, loading, onboarding step ("2 of 4"), action confirmations |
| H2 | Match with the real world | User's language, clear icons, logical order |
| H3 | User control and freedom | "Back", "Skip", "Close", undo |
| H4 | Consistency and standards | Same patterns on all screens, platform conventions, design system |
| H5 | Error prevention | Confirmation of destructive actions, validation before submit, safe defaults |
| H6 | Recognition rather than recall | Visible options, hints, context isn't lost between steps |
| H7 | Flexibility and efficiency | Minimum steps to value, autofill, shortcuts |
| H8 | Aesthetic and minimalist design | Visual hierarchy, one primary CTA, no excess copy |
| H9 | Help users recognize and recover from errors | Clear messages with a way to fix |
| H10 | Help and documentation | Access to support, FAQ, in-context explanations |

### Severity scale (Nielsen)

| Score | Level | Meaning |
|---|---|---|
| 0 | Not a problem | No agreement that it's a problem |
| 1 | Cosmetic | Fix if there's time |
| 2 | Minor | Low priority |
| 3 | Major | High priority |
| 4 | Catastrophe | Fix before release; blocks the task or creates business or moderation risk |

Set severity by the problem's frequency, impact and persistence.

Sections 1–3 below apply to onboarding audits only.

## 1. Scoring each screen
- Nielsen's 10 heuristics;
- Apple HIG and Material Design;
- accessibility: contrast (in Figma — measured per WCAG; on screenshots — visual estimate labeled "estimate"), tap targets 44×44 pt (iOS) and 48×48 dp (Android), readability.

**Onboarding checklist:**
- [ ] value is clear on the first screen;
- [ ] optional steps can be skipped;
- [ ] permissions are explained before the system dialog (pre-permission);
- [ ] sign-up isn't required too early;
- [ ] there's a progress indicator;
- [ ] there's personalization;
- [ ] paywall terms are transparent: price, trial, price after trial, auto-renewal, close, "Restore purchases";
- [ ] no dark patterns.

## 2. Friction points
For each:
- screen, element and friction type: cognitive, mechanical, emotional (distrust, pressure) or technical;
- severity on Nielsen's 0–4 scale;
- evidence: what exactly is visible on the screen, or a measured value from Figma;
- likely funnel impact (hypothesis): at which step and why the user may drop off.

## 3. Improvements: at least 10 low-code

**Low-code** — changes that can ship in 1–2 days without new backend: copy, screen order, removing or merging a step, adding skip or progress, moving a permission request, changing the CTA, visual hierarchy, existing components, remote config or feature flag. Anything that needs new logic, backend or new features goes into a separate "Not low-code (for later)" list.

**Selection by confidence.** The main list holds **High** only. High requires all four conditions:
- (a) a heuristic or standard violation with severity ≥ 3;
- (b) at least 2 of 3 competitors do it better, or there's a positive result from a similar test in `knowledge/experiments.md`;
- (c) no failed test of a similar change in the knowledge base;
- (d) the change matches widely accepted onboarding best practice.

If there are fewer than 10 High improvements, don't pad the list. Show as many as there are, and list Medium candidates separately, explaining which condition is missing for High.

**Numeric probability.** Never give a numeric probability of success or a lift forecast (like "90%" or "+15% conversion").

**Format of each improvement:**
- №, screen, the friction point it removes;
- change: what exactly and how, concretely (new CTA copy — verbatim);
- rationale: heuristic, practice, competitor precedent, knowledge base data;
- metric: a specific funnel step (onboarding completion, permission grant rate, trial start, etc.);
- hypothesis: "If …, then …, because …";
- confidence: High, listing the conditions a–d that are met;
- effort (S or M) and risk (what could get worse);
- ICE: Impact (1–10) × Confidence (1–10) × Ease (1–10) = score.

Sort improvements by ICE, descending.
