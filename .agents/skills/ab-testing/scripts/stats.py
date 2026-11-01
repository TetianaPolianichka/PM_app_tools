#!/usr/bin/env python3
"""A/B test statistics with the standard library only.

Usage:
  stats.py size BASELINE REL_LIFT [--alpha 0.05] [--power 0.8]
      n per arm for a two-sided two-proportion test (e.g. size 0.05 0.10)
  stats.py srm COUNT_A COUNT_B [COUNT_C ...] [--shares 0.5,0.5]
      sample ratio mismatch: chi-square goodness of fit vs planned shares
  stats.py prop CONV_A N_A CONV_B N_B [--alpha 0.05]
      control A vs variant B: abs/rel difference, CI, two-sided p-value
  stats.py duration N_PER_ARM ARMS USERS_PER_DAY [--share 1.0] [--maturation 0]
      days to enroll, rounded up to whole weeks, plus maturation window
  stats.py guardrail EVENTS_A N_A EVENTS_B N_B --margin 0.005 --harm up|down [--alpha 0.05]
      non-inferiority check of variant B vs control A against an absolute tolerance
"""
import argparse
import math
from statistics import NormalDist

Z = NormalDist()


def n_per_arm(p1, rel_lift, alpha=0.05, power=0.8):
    p2 = p1 * (1 + rel_lift)
    pb = (p1 + p2) / 2
    a, b = Z.inv_cdf(1 - alpha / 2), Z.inv_cdf(power)
    num = a * math.sqrt(2 * pb * (1 - pb)) + b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num ** 2 / (p2 - p1) ** 2)


def _gammq(a, x):
    # Regularized upper incomplete gamma Q(a, x) (Numerical Recipes).
    if x <= 0:
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-15:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - gln)
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        h *= d * c
        if abs(d * c - 1) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def srm(counts, shares):
    total = sum(counts)
    chi2 = sum((o - s * total) ** 2 / (s * total) for o, s in zip(counts, shares))
    return chi2, _gammq((len(counts) - 1) / 2, chi2 / 2)


def prop_test(ca, na, cb, nb, alpha=0.05):
    pa, pb = ca / na, cb / nb
    diff = pb - pa
    pooled = (ca + cb) / (na + nb)
    se0 = math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb))
    p = 2 * (1 - Z.cdf(abs(diff) / se0)) if se0 > 0 else 1.0
    z = Z.inv_cdf(1 - alpha / 2)
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    # Relative CI via log of the ratio (delta method).
    rel_ci = None
    if ca > 0 and cb > 0:
        se_log = math.sqrt((1 - pa) / ca + (1 - pb) / cb)
        lr = math.log(pb / pa)
        rel_ci = (math.exp(lr - z * se_log) - 1, math.exp(lr + z * se_log) - 1)
    return pa, pb, diff, (diff - z * se, diff + z * se), diff / pa if pa else float("nan"), rel_ci, p


def guardrail(ea, na, eb, nb, margin, harm, alpha=0.05):
    # One-sided non-inferiority: is harm beyond `margin` ruled out?
    pa, pb = ea / na, eb / nb
    diff = pb - pa
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    z = Z.inv_cdf(1 - alpha)
    sign = 1 if harm == "up" else -1
    harm_est = sign * diff
    bound = harm_est + z * se
    if harm_est > margin:
        verdict = "BREACH: estimated harm exceeds the tolerance"
    elif bound <= margin:
        verdict = "PASS: harm beyond the tolerance is ruled out"
    else:
        verdict = "INCONCLUSIVE: cannot rule out harm beyond the tolerance"
    return pa, pb, diff, sign * bound, verdict


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("size")
    s.add_argument("baseline", type=float)
    s.add_argument("rel_lift", type=float)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    r = sub.add_parser("srm")
    r.add_argument("counts", type=int, nargs="+")
    r.add_argument("--shares")
    pr = sub.add_parser("prop")
    for name in ("conv_a", "n_a", "conv_b", "n_b"):
        pr.add_argument(name, type=int)
    pr.add_argument("--alpha", type=float, default=0.05)
    d = sub.add_parser("duration")
    d.add_argument("n_per_arm", type=int)
    d.add_argument("arms", type=int)
    d.add_argument("users_per_day", type=float)
    d.add_argument("--share", type=float, default=1.0)
    d.add_argument("--maturation", type=int, default=0)
    g = sub.add_parser("guardrail")
    for name in ("events_a", "n_a", "events_b", "n_b"):
        g.add_argument(name, type=int)
    g.add_argument("--margin", type=float, required=True, help="absolute tolerance, e.g. 0.005 = 0.5 pp")
    g.add_argument("--harm", choices=["up", "down"], required=True, help="direction that is harmful")
    g.add_argument("--alpha", type=float, default=0.05, help="one-sided")
    args = ap.parse_args()

    if args.cmd == "size":
        n = n_per_arm(args.baseline, args.rel_lift, args.alpha, args.power)
        print(f"n per arm: {n:,}  (baseline {args.baseline:.2%}, +{args.rel_lift:.0%} relative, "
              f"alpha {args.alpha}, power {args.power:.0%})")
    elif args.cmd == "srm":
        k = len(args.counts)
        shares = [float(x) for x in args.shares.split(",")] if args.shares else [1 / k] * k
        if len(shares) != k or abs(sum(shares) - 1) > 1e-6:
            ap.error("--shares must have one value per arm and sum to 1")
        chi2, p = srm(args.counts, shares)
        total = sum(args.counts)
        actual = ", ".join(f"{c / total:.2%}" for c in args.counts)
        verdict = "SRM: do not trust results until the cause is found" if p < 0.001 else "no SRM detected"
        print(f"actual split: {actual}\nchi2 = {chi2:.3f}, p = {p:.4g} -> {verdict}")
    elif args.cmd == "prop":
        pa, pb, diff, ci, rel, rel_ci, p = prop_test(args.conv_a, args.n_a, args.conv_b, args.n_b, args.alpha)
        conf = f"{1 - args.alpha:.0%}"
        print(f"control A: {pa:.3%}   variant B: {pb:.3%}")
        print(f"absolute diff: {diff * 100:+.3f} pp  ({conf} CI {ci[0] * 100:+.3f} to {ci[1] * 100:+.3f} pp)")
        if rel_ci:
            print(f"relative diff: {rel:+.2%}  ({conf} CI {rel_ci[0]:+.2%} to {rel_ci[1]:+.2%})")
        print(f"two-sided p = {p:.4g}")
    elif args.cmd == "duration":
        days = math.ceil(args.n_per_arm * args.arms / (args.users_per_day * args.share))
        weeks = math.ceil(max(days, 7) / 7)
        print(f"enrollment: {days} days -> {weeks} week(s) ({weeks * 7} days)"
              f"\nreadout after maturation: day {weeks * 7 + args.maturation}")
    elif args.cmd == "guardrail":
        pa, pb, diff, bound, verdict = guardrail(args.events_a, args.n_a, args.events_b, args.n_b,
                                                 args.margin, args.harm, args.alpha)
        side = "upper" if args.harm == "up" else "lower"
        tol = args.margin if args.harm == "up" else -args.margin
        print(f"control A: {pa:.3%}   variant B: {pb:.3%}   change: {diff * 100:+.3f} pp")
        print(f"one-sided {1 - args.alpha:.0%} {side} bound: {bound * 100:+.3f} pp   tolerance: {tol * 100:+.3f} pp")
        print(verdict)


if __name__ == "__main__":
    main()
