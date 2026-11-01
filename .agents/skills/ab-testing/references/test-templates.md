# Test templates

Read this when writing a test plan, a readout, or a backlog entry. In this project a filled template becomes a page in `wiki/hypotheses/` (after the user's OK), with the wiki "Sources:" header line added at the top.

## Contents
1. Pre-registration (test plan)
2. Mid-test check
3. Readout
4. Backlog entry

## 1. Pre-registration (test plan)

Fill this in before launch. Anything added after launch goes under "Changes after launch" with a date.

```markdown
# [Test name]

Owner: [...]   Status: draft / approved / running / concluded
Platform / market: [iOS, Android, web; countries]   Tool: [PostHog / Purchasely / Firebase / ...]

## Decision
If [variant wins by ≥ MDE with guardrails OK] → [action].
If [flat or loss] → [action].

## Hypothesis
Because [evidence], we believe [change] will cause [direction, rough size] in [primary metric] for [audience].

## Variants
- Control: [description, screenshot link]
- B: [description, screenshot link]

## Design
- Randomization unit: [user / device / account]   Analysis unit: [same, or variance method]
- Allocation: [50/50]   Ramp plan: [if any]
- Trigger / exposure event: [event logged identically in all arms]
- Eligibility: [new users, app version ≥ x, markets]

## Metrics
- Primary: [definition, window, e.g. paid conversion within 14 days of first paywall view]
- Secondary: [...]
- Guardrails and tolerance: [metric: max allowed change]

## Power
- Baseline: [value, source, date range]
- MDE: [relative and absolute] (why this is the smallest effect worth acting on)
- α / power: [0.05 / 80%]   Correction: [none / Holm / Bonferroni]
- n per arm: [...]   Eligible users/day: [...]
- Duration: [enrollment days] + [maturation window] = readout on [date]

## Analysis method
[Fixed-horizon / group sequential with N looks on dates ... / always-valid / Bayesian with prior ...]
Stopping rules: [harm thresholds; efficacy boundary if sequential]

## Planned segments
[platform, country, new vs returning], each labelled as secondary.

## Known risks / external events
[releases, promos, holidays]

## Changes after launch
[date: change, reason]
```

## 2. Mid-test check

```markdown
## Check [date], day [n] of [N]
- Per-arm assigned / exposed: [A: ..., B: ...]   SRM p-value: [...]  → pass / investigate
- Guardrails vs tolerance: [...]
- Technical issues: [crashes, missing events, version gating]
- External events: [...]
- Action: continue / pause / stop for harm (not for a promising primary)
```

## 3. Readout

```markdown
# [Test name]: readout

Dates: [start–end]   Platform/market: [...]   Tool: [...]
Result: win / loss / inconclusive / invalid

## Trust checks
- SRM: [counts, expected split, p-value]
- Planned n reached: yes / no   Maturation window complete: yes / no
- Data issues: [none / ...]

## Primary metric
| Arm | n | Value | Abs. diff vs control | Rel. diff | 95% CI (rel.) | p |
|---|---|---|---|---|---|---|
| Control | | | — | — | — | — |
| B | | | | | | |

Interpretation: [what the CI does and doesn't rule out; winner's-curse discount if significant]

## Guardrails
| Metric | Window mature? | Control | B | Change | Harmful-side bound | Tolerance | Verdict (pass / breach / inconclusive / not yet mature) |
|---|---|---|---|---|---|---|---|

Overall: [Guardrails OK / Not shippable as is: ... / Inconclusive: ...]. See guardrails.md.

## Secondary metrics
[mechanism story: do funnel steps move the way the hypothesis predicts?]

## Planned segments
[results, labelled secondary]

## Exploratory observations
[unplanned cuts, clearly labelled as hypotheses for future tests]

## Decision
[ship / keep control / iterate / rerun], because [...]
Expected impact (discounted): [...]   Holdout: [yes/no, size, review date]

## Learnings
Pattern: [reusable insight]   Apply to: [other surfaces, each needing its own test]
```

## 4. Backlog entry

```markdown
| ID | Hypothesis (one line) | Source / evidence | Surface | Primary metric | Plausible effect | Testable at current traffic? | I | C | E | Score | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

Testable at current traffic: compare the plausible effect with the MDE the surface's traffic allows in ≤ 4 weeks. If it's below, mark "ship on judgement", "move to higher-traffic surface", or "drop".
