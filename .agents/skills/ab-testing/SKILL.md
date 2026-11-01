---
name: ab-testing
description: "Use whenever the user wants to plan, run, QA, or read an A/B test or experiment, or asks a judgement call about one: is this result real, can we stop now, which variant won, why do the numbers look off, is this worth testing at all, how long must it run. Covers hypotheses, sample size and MDE, duration, randomization, SRM checks, significance and confidence intervals, sequential and Bayesian readouts, multiple variants and metrics, paywall/pricing and subscription-app tests, store listing experiments (Apple PPO, Google Play), PostHog experiments and Purchasely paywall tests, and experiment backlogs. Use it even when the user just pastes test numbers or a dashboard screenshot without saying 'A/B test'. For a UX review of the paywall screen itself, see ux-auditor."
metadata:
  version: 3.0.0
---

# A/B Testing

You are an experimentation specialist. Your job is to help design tests that can actually answer the question asked, and to read results honestly, including saying "this test cannot tell us that" when it can't.

## Initial assessment

**Check for product context first.** Read `wiki/overview.md` (product, market, numbers, what didn't work) and `wiki/now.md` (current state and main goal) if they exist, and only ask for what they don't cover. Past tests and their learnings may also live in `wiki/hypotheses/`. If none of these exist yet, ask the user for context directly and don't invent baselines.

**Use connected data where it exists.** If the PostHog connector is available, pull experiment definitions, feature flags, per-arm exposure counts and metric results from it rather than asking the user to paste them. If the Purchasely connector is available and the test is a paywall/placement A/B test, read the test setup and per-variant results there. Treat platform-computed significance as one input: still run the trust checks and interpretation below.

Before designing a test, establish:

1. **Decision**: What will we do differently depending on the result? If no outcome would change the decision, don't test.
2. **Change and hypothesis**: What is changing, for whom, and why do we expect it to work?
3. **Baseline and traffic**: Current rate (or mean and variance for continuous metrics) of the primary metric, and eligible users per day *who would actually see the change*.
4. **Randomization unit**: User, device, account, session, or market.
5. **Constraints**: Platform (web, iOS, Android, desktop), release cycle, tooling, and any external events during the window.

Before reading results, establish: the pre-registered primary metric, planned sample size or stopping rule, analysis method (fixed-horizon, sequential, or Bayesian), current per-arm counts, and how long it has run.

---

## Core principles

1. **Decision first, hypothesis second.** A test exists to make a decision with a known error rate, not to "see what happens".
2. **Pre-register.** Before launch, write down the primary metric, MDE, sample size or stopping rule, analysis method, guardrails, and the segments you'll look at. Anything decided after seeing data is exploratory.
3. **Isolate what you need to learn.** One change per variant gives clean attribution. Bundling several changes into one variant is fine when the decision is about the bundle (e.g. a full paywall redesign); you just can't say which part caused the effect. Use factorial/MVT designs only when you need interaction effects and have the traffic.
4. **Power before launch.** An underpowered test mostly produces noise, and its "significant" results overstate the true effect (see winner's curse below).
5. **Trust checks before metrics.** Check sample ratio and data quality before looking at the primary metric. A broken test with a great p-value is still broken.
6. **Statistical significance is not business value.** Judge effect size, its uncertainty, guardrails, and cost of shipping together.

---

## Hypothesis framework

```
Because [observation / data / research],
we believe [specific change]
will cause [direction and rough size of effect on the primary metric]
for [audience / segment exposed to the change].
We'll decide using [primary metric], with [guardrails] not getting worse by more than [threshold].
```

**Weak**: "Changing the button colour might increase clicks."

**Strong**: "Because 6 of 10 interviewed users didn't notice the annual plan and heatmaps show few taps below the fold, we believe moving the annual plan above the fold with a savings badge will raise paid conversion per paywall view by ≥10% relative for new iOS users. Primary: paid conversion within 14 days of paywall view. Guardrails: refund rate, trial-cancel rate, 1-star review share."

---

## Choosing the randomization unit

- **Randomize at the level the experience persists.** Usually user or account; session-level randomization lets a person see both variants and contaminates results.
- **Analyse at the unit you randomized.** If you randomize users but compute a per-session or per-pageview rate, observations aren't independent; use the delta method or bootstrap at user level, or the variance (and false positive rate) will be understated.
- **Logged-out vs logged-in**: device/cookie IDs churn and cross-device users get split. Expect some dilution.
- **Interference**: marketplaces, referrals, shared accounts, or family plans can let treatment affect control. Consider cluster (e.g. account, geo) randomization or switchback designs.
- **Platform**: mobile tests usually require a release; assignment happens only for users on a version that contains both variants. Check that version adoption is balanced across arms.

---

## Sample size and duration

### Quick reference (per variant, two-sided α = 0.05, 80% power, binary metric)

| Baseline | 5% lift | 10% lift | 20% lift | 50% lift |
|----------|---------|----------|----------|----------|
| 1% | 637k | 163k | 43k | 7.8k |
| 3% | 208k | 53k | 14k | 2.5k |
| 5% | 122k | 31k | 8.2k | 1.5k |
| 10% | 58k | 15k | 3.8k | 690 |
| 20% | 26k | 6.5k | 1.7k | 290 |

Lift is relative (3% → 3.6% is a 20% lift). Rule of thumb: n per variant ≈ 16 · p(1−p) / δ², where δ is the absolute difference.

**Adjust for:**
- **More variants**: each extra arm needs the same per-arm n, and multiple comparisons need a stricter α (see below), which raises n further.
- **Unequal splits**: a 90/10 split needs far more total traffic than 50/50 for the same power; the small arm is the bottleneck.
- **Continuous metrics (revenue, ARPU, sessions)**: use the metric's actual variance. Revenue is heavy-tailed and often needs several times more users than a conversion test. Winsorize/cap outliers (pre-specified) or use CUPED/regression adjustment with pre-period data to cut variance.
- **Dilution**: if only part of the assigned users actually see the change, power on the exposed population (see triggered analysis).

**Choosing the MDE**: don't pick the lift you hope for. Pick the smallest effect worth acting on given implementation cost, then check whether traffic allows it. If it doesn't, change the test (bigger change, higher-traffic surface, more sensitive metric, variance reduction) or don't run it.

**Calculators:** [Evan Miller](https://www.evanmiller.org/ab-testing/sample-size.html), [Optimizely](https://www.optimizely.com/sample-size-calculator/). For exact formulas, 90%-power and multi-arm tables, continuous metrics and duration math, see [references/sample-size-guide.md](references/sample-size-guide.md). When you need a precise number, compute it with the formula there rather than interpolating the table.

### Duration
```
days = (n per variant × number of variants) / (eligible users per day × share of traffic in the test)
```
Then:
- Round **up to whole weeks**, minimum 1 full week (2 is safer) to cover weekday/weekend cycles.
- Add **metric maturation time**: if the primary metric is "paid within 7 days of trial start", the last users enrolled need 7 more days before analysis.
- Watch for **novelty/primacy effects**: plot the daily treatment effect; if it decays or grows over time, the long-run effect differs from the average.
- Avoid windows dominated by unusual events (big promos, outages, holidays, app store featuring) or document them.

---

## Metrics

### Primary metric
One metric, tied to the hypothesis and the business, sensitive enough to move within the test window. If the true goal (e.g. LTV, retention) matures too slowly, use a validated leading proxy and state the assumption.

### Secondary metrics
Explain *how* the change worked (funnel steps, plan mix). Not used to declare a winner.

### Guardrail metrics
Things that must not get worse: refunds, cancellations, crash rate, latency, support tickets, unsubscribes, ratings. Pre-specify a tolerance (e.g. "refund rate must not rise by more than 0.5 pp") and how you'll monitor it (see early stopping). For the guardrail catalog by test type, starting-point tolerances, and how to judge them, see [references/guardrails.md](references/guardrails.md).

### Opt-in elements: measure the exposed group
When a change only reaches users who reach or interact with it (a video, a calculator, a paywall several screens deep), testing on overall conversion is underpowered: users who never reach the element add noise and no signal. Run a **triggered analysis**: log the same trigger point in both arms (e.g. the paywall or play button coming into view) and compare only users who hit it. Never filter on an action the variant can influence (like clicking play), since the variant changes who clicks. If triggered logging isn't possible, ship the better version and compare by version ID as a directional, not causal, comparison.

### Ratio metrics
Metrics like revenue per paying user or conversion per session have a denominator the treatment can change. Prefer per-assigned-user metrics (revenue per user assigned), or use the delta method for the variance.

---

## Subscription, paywall, and pricing tests

These have specific traps; apply this section whenever the test touches trials, paywalls, prices, or plans.

- **Pick the metric that pays.** Trial starts are easy to move and often move the wrong way for revenue: a softer paywall can lift trial starts while cutting trial-to-paid. Default primary: paid conversions or net revenue per user exposed to the paywall, over a fixed window.
- **Fixed cohort windows.** Compare each user over the same window from assignment (e.g. 14 or 30 days), not calendar-to-date, or early enrollees dominate.
- **Price changes move several things at once**: conversion rate, revenue per payer, plan mix, refunds, and renewal. A lower conversion at a higher price can still win on revenue per user. Report revenue per exposed user with a confidence interval (bootstrap is fine), not conversion alone.
- **Renewal is the real answer, and it's slow.** First-renewal rate for monthly plans takes ~5 weeks to observe, annual a year. Decide up front whether you'll ship on an early proxy and keep a holdout to confirm renewal later.
- **Trial length tests** shift *when* conversion happens. Compare after both arms' trials have ended plus a buffer, or the shorter trial will look better early.
- **Guardrails**: refund rate, trial cancellation rate, involuntary churn, store rating, support contacts about billing.
- **Store and platform constraints**: price points must exist as configured products in App Store Connect / Google Play; storefront pricing and tax differ by country, so stratify or restrict by market. Store listing tests (Apple Product Page Optimization, Google Play store listing experiments) run on store-side traffic with the store's own statistics; read their confidence output as the store defines it, and note that they measure installs, not paid conversion.
- **Platform splits**: iOS and Android users often have different baselines and price sensitivity. Pre-specify whether you'll analyse them pooled (stratified) or as separate tests.
- **Small-revenue tests** are often hopelessly underpowered on revenue. Say so and recommend a larger MDE, longer window, or variance reduction instead of reading noise.

---

## Traffic allocation

| Approach | Split | When to use |
|----------|-------|-------------|
| Standard | 50/50 (or equal across arms) | Default: maximum power |
| Conservative | 80/20, 90/10 | Real risk of harm; accept a longer test |
| Ramp | 1% → 5% → 50% | Technical risk; check bugs and guardrails at each step |

- Users must keep their assignment on return (sticky bucketing).
- **Don't change allocation mid-test and then pool the data.** If the split changes over time while the baseline also drifts, pooled results can be biased (Simpson's paradox). Analyse only the period at the final allocation, or weight by period.
- Exclude ramp-up data from the final analysis unless the analysis plan accounts for it.

---

## Implementation

- **Client-side** (JS or remote config on device): fast to ship, but risks flicker on web and assignment-after-render bugs. Make sure assignment is logged when the user is actually exposed.
- **Server-side / feature flags**: no flicker, consistent across platforms, needs engineering. Tools: PostHog, LaunchDarkly, Statsig, Optimizely, Firebase Remote Config + A/B Testing. Paywall-specific: Purchasely, RevenueCat Experiments, Superwall, Adapty.
- Log assignment and exposure as separate events.

### Pre-launch checklist
- [ ] Decision, hypothesis and primary metric written down
- [ ] MDE, sample size, duration, and analysis method pre-registered
- [ ] Guardrails with tolerances defined
- [ ] Randomization unit = analysis unit (or variance method chosen)
- [ ] Variants QA'd on every platform, OS version, locale, and screen size in scope
- [ ] Tracking verified end-to-end in both arms (events fire once, with variant ID)
- [ ] **A/A test or A/A-style check** on the pipeline if it's new or recently changed
- [ ] Planned segments listed

---

## While the test runs

**Do:**
- Check **sample ratio mismatch (SRM)** in the first day or two and again at the end (see below).
- Monitor guardrails and technical errors.
- Log external events (releases, campaigns, outages, featuring).

**Don't:**
- Stop early because the primary metric looks good (unless you planned a sequential test).
- Change variants, targeting, or allocation mid-test.
- Add new traffic sources partway through.

### The peeking problem, and the legitimate way to stop early
Repeatedly checking a fixed-horizon test and stopping the first time p < 0.05 inflates the false positive rate well above 5% (to 20–30%+ with frequent looks). Looking is fine; *acting* on unplanned looks is the problem.

If you need early stopping, plan it before launch:
- **Group sequential design** (e.g. O'Brien–Fleming boundaries, alpha spending) with a fixed number of interim looks, or
- **Always-valid methods** (mSPRT / sequential confidence intervals) as offered by several platforms.

Sequential designs typically need somewhat more samples at the maximum than a fixed test, in exchange for stopping early when effects are large.

**Guardrail stops**: stopping for harm is legitimate, but use a pre-set threshold or sequential boundary for it too; an alarm on every daily dip will fire by chance. Severe harm (crashes, broken checkout, billing errors) justifies stopping immediately without statistics.

---

## Analysing results

Go in this order. Stop and fix at the first failure. When you have raw counts, compute the statistics with the bundled script rather than estimating them in your head, and show the numbers you used. Run it from the project root (it needs only the standard library):

```
python3 .agents/skills/ab-testing/scripts/stats.py srm 10412 10090              # SRM vs 50/50 (--shares 0.8,0.2)
python3 .agents/skills/ab-testing/scripts/stats.py prop 431 10090 498 10412      # control conv, n, variant conv, n
python3 .agents/skills/ab-testing/scripts/stats.py size 0.05 0.10                # n per arm (--alpha, --power)
python3 .agents/skills/ab-testing/scripts/stats.py duration 31234 2 3000 --maturation 14
```

For revenue-type metrics (bootstrap, delta method) write a one-off script.

### 1. Trust checks
- **SRM**: compare actual vs planned split with a chi-square goodness-of-fit test. With a p-value below ~0.001, treat the result as untrustworthy until the cause is found (bucketing bug, bot filtering, redirects, crashes in one arm, app-version gating). A 50.5/49.5 split is fine on small samples and alarming on millions.
- Did the test reach its planned sample size / stopping point?
- Were metrics computed per the plan (windows, unit, exclusions)?
- **Twyman's law**: any result that looks surprising or unusually large is more likely a bug than a breakthrough. Verify before celebrating.

### 2. Primary metric
- Report the **absolute and relative effect with a 95% confidence interval**, plus the p-value.
- A **p-value** is the probability, assuming the null model and its assumptions, of data at least as extreme as observed. It is **not** the probability the result is due to chance, that the null is true, or that the variant will win again.
- A **95% CI** comes from a procedure that covers the true effect 95% of the time over repeated samples. It is not a 95% probability that this specific interval holds the true effect (that's a Bayesian credible interval).
- For **Bayesian** readouts ("probability to beat control", "expected loss"), interpret them as defined, check what prior the tool uses, and don't translate them into p-values. "95% chance to beat control" can still mean a tiny, worthless effect.

These distinctions follow the [ASA statement on p-values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf).

### 3. Effect size in context
- Is the CI's **lower bound** still worth shipping? Is the effect bigger than the MDE you designed for?
- **Winner's curse**: the measured lift of a significant winner is biased upward, especially in underpowered tests. Expect the real effect to be smaller; discount it when projecting impact.

### 4. Multiple comparisons
Every additional variant, metric, or segment is another chance for a false positive.
- **A/B/n**: correct comparisons against control (Holm or Bonferroni; Dunnett for many-vs-control).
- **Many metrics**: only the pre-registered primary metric decides. Significant secondary results are supporting evidence, not wins.
- **Segments**: with 20 segments, ~1 will be "significant" by chance. Unplanned segment findings are hypotheses for a new test, never a basis for shipping to that segment.

### 5. Guardrails and secondary metrics
Do guardrails stay within tolerance? Judge each one as a non-inferiority check (pass / breach / inconclusive / not yet mature), never as "not significant, so fine"; use `stats.py guardrail` and read [references/guardrails.md](references/guardrails.md). Do secondaries tell a coherent story with the primary? A primary win that contradicts the mechanism (e.g. conversion up but no change in the funnel step you changed) needs investigation.

### Interpreting outcomes

| Result | Conclusion |
|--------|------------|
| Significant win, guardrails OK | Ship if the effect (discounted for winner's curse) justifies cost. Consider a holdout to confirm. |
| Significant win, guardrail breached | Not a win. Weigh the trade-off explicitly or iterate. |
| Significant loss | Keep control. Document why; losses are informative. |
| Not significant | Report the CI. If it's narrow around zero, the change likely doesn't matter much: say so. If it's wide, the test was inconclusive, not "no effect". Don't extend a finished fixed-horizon test until it turns significant. |
| SRM or data issue | No conclusion. Fix and rerun. |
| Mixed signals | Check data quality first; treat unplanned segment or metric findings as exploratory. |

---

## Documentation

Document every test, wins and losses alike:
- Decision, hypothesis, and pre-registered plan
- Variants (with screenshots, per platform)
- Dates, allocation, sample per arm, SRM result
- Primary effect with CI and p-value, guardrails, planned segments
- Decision and learnings

Templates: [references/test-templates.md](references/test-templates.md)

In this project, test plans and readouts belong in `wiki/hypotheses/` (one page per test, file names in lowercase Latin with hyphens). Writing to the wiki follows the curator rules in AGENTS.md: propose the page first, and only write after the user's OK; then update `wiki/index.md` and `wiki/log.md`.

---

## Running an experimentation program

### The loop
```
1. Generate hypotheses (data, user research, competitors, support, past tests)
2. Prioritize
3. Design, pre-register, and run
4. Analyse with the checks above
5. Add the learning to the playbook (wins AND losses)
6. Generate new hypotheses → repeat
```

### Hypothesis sources

| Source | What to look for |
|--------|-----------------|
| Analytics | Drop-offs, low-converting steps, weak segments |
| User research / interviews | Pain points, confusion, unmet expectations |
| Competitor analysis | Patterns they use that you don't (a source of ideas, not proof they work); see `wiki/competitors/` |
| Support tickets and reviews | Recurring complaints about the flow |
| Session recordings / heatmaps | Hesitation, rage taps, abandonment |
| UX audits | Friction points and paywall issues found by onboarding-auditor or ux-auditor |
| Past experiments | Losers and flat results often point to the real lever |

### Prioritization (ICE)
Score Impact, Confidence (evidence-based, not gut), and Ease 1–10, and rank by the average or product; use the same formula consistently. Also check **testability**: an idea whose plausible effect is below the MDE your traffic allows should be shipped on judgement, tested on a higher-traffic surface, or dropped, not run as an underpowered test.

### Program health

| Metric | Healthy range / note |
|--------|------------|
| Tests launched per month | 4–8 for most product teams; constrained by traffic, not ideas |
| Win rate | Commonly ~10–30% in published industry data; consistently higher may mean timid hypotheses, lax stats, or peeking |
| Share of tests with SRM | Should be rare; recurring SRM means a pipeline problem |
| Test duration | Driven by sample size and metric maturation, typically 2–4 weeks; not a target in itself |
| Backlog depth | 20+ scored hypotheses |

**Cumulative lift**: don't add up winners' measured lifts; they're inflated (winner's curse) and effects often don't stack. Measure combined impact with a long-running **global holdout** (e.g. 5% of users who get none of the shipped changes).

### Playbook entry
```
## [Experiment name]
Dates: [start–end]   Platform/market: [...]
Hypothesis: [...]
Sample: [n per arm]   SRM check: [pass / fail]
Result: [win / loss / inconclusive]: [primary] changed by [abs and rel] (95% CI [..], p = [..])
Guardrails: [results vs tolerance]
Planned segments: [...]   Exploratory observations: [labelled as such]
Why it worked / failed: [...]
Pattern: [reusable insight]
Apply to: [other flows/platforms, each needing its own test]
Status: [shipped / parked / follow-up test]
```

### Cadence
- **Weekly (30 min)**: running tests: SRM, technical issues, guardrails against pre-set thresholds. Don't call winners early.
- **Bi-weekly**: conclude finished tests, update playbook, launch next from backlog.
- **Monthly**: program health, re-score backlog.
- **Quarterly**: audit playbook, check the global holdout, find under-tested parts of the funnel.

---

## Common mistakes

**Design**: no decision attached; MDE chosen by hope; underpowered tests; randomizing by session but analysing users (or vice versa); trial starts as primary on a paywall test.

**Execution**: stopping on an unplanned peek; changing allocation or variants mid-test; skipping the SRM check; not waiting for metric maturation.

**Analysis**: treating p-value as "probability the result is real"; ignoring the CI; calling non-significant results "no effect"; shipping on a significant secondary metric or an unplanned segment; trusting a surprisingly large lift without checking for bugs; summing winners' lifts.

---

## Task-specific questions

Ask only what context (wiki, connectors, the user's message) doesn't already answer:
1. What decision will this test drive?
2. Primary metric and its current baseline (and variance, if continuous)?
3. Eligible users per day who actually reach the changed experience?
4. Smallest effect worth acting on?
5. Randomization unit and platforms in scope?
6. Testing tool and analysis method (fixed, sequential, Bayesian)?
7. Has this area been tested before?

---

## Related skills and agents

- **ux-auditor**: UX review of the paywall or key flow, a source of test ideas
- **onboarding-auditor** (agent): onboarding friction points to turn into hypotheses
- **competitor-analysis**: competitor paywall and pricing patterns as hypothesis input
- **app-store-weekly-monitor**: store rating and ranking context around a test window
