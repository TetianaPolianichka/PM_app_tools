# Guardrails for A/B test analyses

Read this when choosing guardrails for a test plan, setting their tolerances, monitoring a running test, or judging guardrails in a readout.

A guardrail is a metric the change is not trying to move but must not hurt. The primary metric decides whether the variant is better; guardrails decide whether it is safe to ship. A primary-metric win with a breached guardrail is not a win.

## Contents
1. Catalog: which guardrails for which test
2. Setting tolerances
3. Analysing a guardrail: non-inferiority, not "not significant"
4. Monitoring and stopping for harm
5. Reporting
6. Common mistakes

## 1. Catalog

Pick 3–5 guardrails per test. More guardrails mean more false alarms and slower decisions; choose the ones the change could plausibly hurt.

### Always on (any test that ships in the app)

| Guardrail | Definition | Window | Why |
|---|---|---|---|
| Crash-free users | Share of exposed users with no crash | Test duration | A variant that crashes more is broken regardless of conversion |
| Sample ratio (SRM) | Chi-square of actual vs planned split | Daily + end | Not a metric but a validity gate: fails → no conclusion |
| Exposure event integrity | Exposure events per assigned user, by arm | Daily | Missing or double-fired events in one arm bias everything |

### Monetization: paywall, pricing, trial, plan tests

| Guardrail | Definition | Window | Harmful direction |
|---|---|---|---|
| Refund rate | Refunds / purchases, per arm | 14–30 days after purchase | Up |
| Trial cancellation rate | Trials cancelled before conversion / trial starts | Within trial length + 1 day | Up |
| Trial-to-paid rate | Paid conversions / trial starts | After every trial in the cohort has ended | Down |
| Revenue per exposed user | Net revenue / users who saw the paywall | Fixed cohort window | Down (guardrail when the primary is conversion) |
| Plan mix | Share of annual vs monthly vs weekly | Fixed window | Shift toward lower-LTV plans |
| Billing support contacts | Tickets tagged billing / exposed users | Test duration | Up |
| Early churn / first renewal | Cancellations before first renewal | ~5 weeks for monthly (slow; often via holdout) | Up |

### Engagement and retention: onboarding, core flow, notifications

| Guardrail | Definition | Window | Harmful direction |
|---|---|---|---|
| D1 / D7 retention | Users active on day 1 / day 7 after assignment | Day 1 / day 7 | Down |
| Core action rate | Share of users who complete the product's key action (e.g. connect in a VPN app) | 7 days | Down |
| Onboarding completion | Users finishing onboarding / users starting it | Session | Down |
| Uninstalls / notification opt-outs | Per exposed user | 7 days | Up |

### Store and reputation

| Guardrail | Definition | Window | Harmful direction |
|---|---|---|---|
| Rating prompt outcome | Share of 1–2★ among in-app ratings, per arm | Test duration | Up |
| Review complaints | Reviews mentioning the changed area (directional; can't be split by arm) | Test duration | Up |
| App Store / Google Play ranking | Category chart position and positions for the top target keywords, per store and country (directional; can't be split by arm) | Test duration vs the 2–4 weeks before launch | Down (a higher rank number) |

Ranking is a store-wide signal, so it can't pass or fail a test on its own. Use it when the change can reach the store: ratings and reviews (rating prompt, paywall, onboarding friction), uninstalls, or retention. Compare against the pre-launch baseline and against the usual weekly swings. Read it alongside a calendar of releases, featuring, seasonality and paid UA changes, since those move rank more than most tests. A drop beyond the normal range while the test runs is a prompt to look at the arm-level guardrails (rating prompt outcome, uninstalls, D1 retention), not a result. For tests on 100% of traffic or store listing experiments with a large traffic share, check it every week.

### Technical

| Guardrail | Definition | Harmful direction |
|---|---|---|
| Screen load time (p75/p95) | Time to interactive on the changed screen | Up |
| Paywall / product load failures | Failed StoreKit / Play Billing product fetches per paywall view | Up |
| Purchase errors | Failed purchase attempts / attempts | Up |

## 2. Setting tolerances

The tolerance (non-inferiority margin) is the largest harm you would accept for the expected gain. Write it down before launch, as an absolute change where possible.

Ask the user, for each guardrail: "If the primary metric wins as hoped, how much worse could this get before you'd refuse to ship?" Use the business context (wiki/overview.md) and past tests if they exist. If the user has no view, propose starting points and label them as assumptions to confirm:

| Guardrail type | Starting-point tolerance (assumption, confirm with the team) |
|---|---|
| Crash-free users, purchase errors, product load failures | Effectively zero: any clear increase is a stop |
| Refund rate, trial cancellation | +0.5 to +1 pp absolute |
| Trial-to-paid, retention, core action | −1 pp absolute or −2% to −5% relative |
| Revenue per exposed user (as guardrail) | −2% to −3% relative |
| Load time | +10% at p75 |

Check that the tolerance is detectable: a guardrail with a tolerance far below what the test's sample can resolve will almost never pass. Estimate the CI width up front (`stats.py size` with the tolerance as the effect gives the n needed to rule it out at 80% power). If the test can't resolve it, either widen the tolerance consciously, extend the test, or say in the plan that this guardrail is monitored only for large harm.

## 3. Analysing a guardrail: non-inferiority

The question for a guardrail is "can we rule out harm larger than the tolerance?", not "is there a significant difference?".

- **Pass**: the confidence bound on the harmful side is inside the tolerance. Example: refund rate tolerance +0.5 pp; observed +0.1 pp, 95% one-sided upper bound +0.35 pp → pass.
- **Breach**: the point estimate itself is worse than the tolerance, or harm is statistically significant and practically meaningful. Example: observed +0.8 pp → breach.
- **Inconclusive**: the bound crosses the tolerance but the estimate is inside it. Example: observed +0.2 pp, upper bound +0.9 pp → the test can't rule out unacceptable harm. Say so; this is not a pass.

Use a one-sided test at α = 0.05 (equivalently, the harmful-side bound of a 90% two-sided CI). Don't apply multiple-comparison corrections to guardrails: correcting would make it easier to miss real harm, which is the opposite of what a guardrail is for. Accept that with several guardrails one may look inconclusive by chance, and investigate rather than auto-reject.

Run it with the bundled script:

```
# refund rate: control 120/4000, variant 131/4010, harm = increase, tolerance +0.5 pp
python3 .agents/skills/ab-testing/scripts/stats.py guardrail 120 4000 131 4010 --margin 0.005 --harm up

# trial-to-paid: harm = decrease, tolerance 1 pp
python3 .agents/skills/ab-testing/scripts/stats.py guardrail 800 2000 790 2010 --margin 0.01 --harm down
```

For continuous guardrails (load time, revenue per user), bootstrap the difference at the user level and apply the same pass / breach / inconclusive rule to the harmful-side bound.

Apply the guardrail's own window. A refund-rate guardrail read before its 14–30 day window has matured is incomplete; report it as "not yet mature", not as a pass.

## 4. Monitoring and stopping for harm

Check guardrails at the weekly review (see the cadence in SKILL.md), not on every dashboard refresh.

| Situation | Action |
|---|---|
| Crash spike, broken purchase flow, billing errors, wrong prices shown | Stop immediately. No statistics needed. |
| Guardrail breaches the pre-set harm boundary at a planned look | Pause the variant, investigate, decide with the team |
| Guardrail looks worse on a daily dip, inside tolerance | Note it, keep running. Daily dips are mostly noise |
| Guardrail inconclusive at the end | Report it; decide explicitly: accept the risk, extend, or rerun with more traffic |

If the plan includes interim harm checks, set the boundary in advance and make it stricter than the final tolerance (e.g. stop if the harmful-side bound at α = 0.01 already exceeds the tolerance), so repeated looks don't trigger false stops.

## 5. Reporting

In every readout, give each guardrail a row (the readout table in [test-templates.md](test-templates.md)) with: control value, variant value, absolute change, harmful-side bound, tolerance, and verdict (pass / breach / inconclusive / not yet mature). Then a one-line overall call:

- All pass → "Guardrails OK."
- Any breach → "Not shippable as is: [guardrail] got worse by [x], beyond the [tolerance] agreed." Offer the trade-off explicitly if the primary win is large, but let the team decide.
- Any inconclusive → name it and what it would take to resolve (more users, longer window, holdout).

## 6. Common mistakes

- Calling a guardrail "fine" because the difference isn't significant.
- No tolerance agreed before launch, then picking one after seeing the number.
- Reading refund or renewal guardrails before their window has matured.
- Too many guardrails, then dismissing the one that fails as "probably noise" without checking.
- Using trial starts as a guardrail for revenue: it can rise while revenue falls.
- Correcting guardrails for multiple comparisons, which hides harm.
- Treating a review-complaint spike as proof of harm in one arm: store reviews can't be split by arm, so it's a prompt to investigate, not a result.
- Blaming a test for a store ranking drop without checking releases, featuring, seasonality and UA spend over the same weeks.
