# Sample size and duration guide

Read this when you need an exact sample size, a non-default α or power, a multi-arm or continuous-metric calculation, or a duration estimate.

## Contents
1. Binary metrics: formula
2. Tables (80% and 90% power, multi-arm)
3. Continuous metrics
4. Unequal splits
5. Variance reduction
6. Sequential designs
7. Duration worked examples
8. Script

## 1. Binary metrics: formula

Two-sided test of two proportions, baseline p1, treatment p2 = p1 × (1 + relative lift):

```
p̄ = (p1 + p2) / 2
n per arm = [ z(1−α/2) · √(2·p̄(1−p̄)) + z(1−β) · √(p1(1−p1) + p2(1−p2)) ]² / (p2 − p1)²
```

z values: α = 0.05 → 1.960; α = 0.0167 → 2.394; α = 0.01 → 2.576. Power 80% → 0.842; 90% → 1.282.

Shortcut (80% power, α = 0.05): n ≈ 16 · p(1−p) / δ². For 90% power use 21 instead of 16.

## 2. Tables (per arm, two-sided α = 0.05, relative lift)

**80% power**

| Baseline | 5% | 10% | 20% | 50% |
|---|---|---|---|---|
| 1% | 637k | 163k | 43k | 7.8k |
| 3% | 208k | 53k | 14k | 2.5k |
| 5% | 122k | 31k | 8.2k | 1.5k |
| 10% | 58k | 15k | 3.8k | 690 |
| 20% | 26k | 6.5k | 1.7k | 290 |

**90% power**

| Baseline | 5% | 10% | 20% | 50% |
|---|---|---|---|---|
| 1% | 853k | 218k | 57k | 10.4k |
| 3% | 278k | 71k | 19k | 3.4k |
| 5% | 163k | 42k | 11k | 2.0k |
| 10% | 77k | 20k | 5.1k | 920 |
| 20% | 34k | 8.7k | 2.3k | 390 |

**A/B/C (two treatments vs control, Bonferroni α = 0.05/2 = 0.025 per comparison), 80% power, per arm**

| Baseline | 10% | 20% |
|---|---|---|
| 3% | 64k | 17k |
| 5% | 38k | 9.9k |
| 10% | 18k | 4.7k |

With three treatments vs control (α ≈ 0.0167): 3% → 71k / 19k, 5% → 42k / 11k, 10% → 20k / 5.1k.

Multiply per-arm n by the number of arms for total traffic.

## 3. Continuous metrics (revenue, ARPU, sessions)

```
n per arm = 2 · (z(1−α/2) + z(1−β))² · σ² / δ²      (≈ 15.7 · σ² / δ² at 80%, α = 0.05)
```

σ is the standard deviation of the metric per randomization unit, taken from pre-period data on the same population. δ is the absolute difference you want to detect.

Revenue per user is mostly zeros plus a long right tail, so σ is often 3–10× the mean. Example: ARPU $0.40, σ $3.00, want +10% (δ = $0.04) → n ≈ 15.7 × 9 / 0.0016 ≈ 88k per arm. Cap at a pre-specified percentile (e.g. 99th) before computing σ and in the analysis.

## 4. Unequal splits

For allocation share k in treatment (control 1 − k), total N needed ≈ N(50/50) / (4·k·(1−k)).
- 80/20 → 1.56× the total traffic of 50/50
- 90/10 → 2.78×

## 5. Variance reduction

- **CUPED / regression adjustment**: use the same metric from a pre-period as a covariate. Required n scales with (1 − ρ²), where ρ is the pre/post correlation. ρ = 0.5 → 25% fewer users; ρ = 0.7 → ~50% fewer. Works poorly for new users with no pre-period.
- **Winsorizing** heavy-tailed metrics.
- **Triggered analysis** on users who reach the change (see SKILL.md).
- **Stratification** by platform or country when baselines differ a lot.

## 6. Sequential designs

Max sample inflation versus a fixed test (two-sided α = 0.05, 80–90% power), approximately:
- O'Brien–Fleming, 2–5 looks: +1–3%
- Pocock, 5 looks: +15–20%
- Always-valid (mSPRT): depends on the mixing parameter; expect a larger max n, but earlier stops on big effects.

Expected sample size under a real, large effect is usually well below the fixed-horizon n.

## 7. Duration worked examples

**Paywall test.** 3,000 new users/day reach the paywall, 100% of them in the test, 2 arms, baseline paid conversion 5%, MDE 10% relative → 31k per arm → 62k total / 3,000 ≈ 21 days → round to 3 weeks, then add the 14-day conversion window → readout at ~5 weeks.

**Underpowered case.** 400 users/day reach the paywall, baseline 3%, MDE 10% → 53k per arm → 266 days. Don't run it. Options: MDE 30% (~6.4k per arm, ~32 days), a higher-funnel metric, or ship on judgement.

## 8. Script

Use the bundled script instead of interpolating tables (standard library only):

```
python3 .claude/skills/ab-testing/scripts/stats.py size 0.03 0.20 --power 0.9
python3 .claude/skills/ab-testing/scripts/stats.py size 0.05 0.10 --alpha 0.025   # A/B/C, Bonferroni
python3 .claude/skills/ab-testing/scripts/stats.py duration 31234 2 3000 --share 0.5 --maturation 14
```
