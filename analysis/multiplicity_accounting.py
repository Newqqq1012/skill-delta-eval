#!/usr/bin/env python3
"""Multiplicity accounting for the SkillsBench pilot (post-results analysis).

Read-only re-analysis of the same runs_*.jsonl; NOT a change to the
pre-registered driver (v1.1). All dimension operators replicate the driver's
exact semantics (dimension_deltas in run_first_measurement.py):
  traj/tool: per-task mean over all (b,s) pairs, then mean over tasks
  eff_c:     rel_change(mean(all skill runs), mean(all base runs))  [pooled]

Computes:
  1. number of implicit qualification tests (unit x dimension);
  2. per-test empirical one-sided p-values from each configuration's own
     null-delta distribution;
  3. BH (FDR) at q=0.05 / 0.10 and Bonferroni verdicts;
  4. sensitivity of the single qualifying case (band quantiles 90/95/97.5,
     band bootstrap CI, leave-one-task-out, base rates).

Output: multiplicity_report.json + stdout summary.
"""
import json
from collections import defaultdict

from run_first_measurement import (
    load_runs, action_type_seq, tool_event_seq, mean,
    norm_levenshtein, rel_change, percentile, bootstrap_ci,
)
from metrics import EFFICIENCY_COMPONENTS

HERE = os.path.dirname(os.path.abspath(__file__)) if (os := __import__("os")) else None
import os
CONFIGS = {
    "gemini-3.5-flash": os.path.join(HERE, "runs_gemini-3.5-flash.jsonl"),
    "minimax-MiniMax-M3": os.path.join(HERE, "runs_minimax-MiniMax-M3.jsonl"),
}
DIMS = ["traj", "tool"] + [f"eff_{c}" for c in EFFICIENCY_COMPONENTS]  # saf excluded: degenerate


def dim_value(a, b, dim):
    """Null-side per-pair delta (mirrors null_bands' dim_key_fn)."""
    if dim == "traj":
        return norm_levenshtein(action_type_seq(a), action_type_seq(b))
    if dim == "tool":
        return norm_levenshtein(tool_event_seq(a), tool_event_seq(b))
    if dim.startswith("eff_"):
        return rel_change(b.get(dim[4:]), a.get(dim[4:]))
    raise ValueError(dim)


def unit_delta(base_lists, skill_lists, common, dim, drop_task=None):
    """Driver-exact unit delta. drop_task: leave-one-task-out override."""
    tasks = [t for t in common if t != drop_task]
    if not tasks:
        return None
    if dim in ("traj", "tool"):
        per_task = []
        for t in tasks:
            vals = [dim_value(b, s, dim) for b in base_lists[t] for s in skill_lists[t]]
            vals = [v for v in vals if v is not None]
            if vals:
                per_task.append(mean(vals))
        return mean(per_task) if per_task else None
    comp = dim[4:]
    rb = mean([b.get(comp) for t in tasks for b in base_lists[t]])
    ra = mean([s.get(comp) for t in tasks for s in skill_lists[t]])
    return rel_change(ra, rb) if (rb is not None and ra is not None) else None


def main():
    report = {"per_config": {}, "combined": {}}
    all_tests = []

    for cfg, path in CONFIGS.items():
        runs = load_runs(path)
        base_runs = [r for r in runs if r.get("condition") == "baseline"]
        null_runs = [r for r in runs if r.get("condition") == "null"]
        skill_units = sorted({r["skill_id"] for r in runs if r.get("condition") == "skill"})

        base_by_task = defaultdict(list)
        for r in base_runs:
            base_by_task[r["task_id"]].append(r)
        null_pairs = [(b, r) for r in null_runs for b in base_by_task.get(r["task_id"], [])]

        nulls = {}
        for dim in DIMS:
            nulls[dim] = sorted(v for v in (dim_value(p[0], p[1], dim) for p in null_pairs) if v is not None)

        cfg_out = {"n_null_runs": len(null_runs), "n_null_pairs": len(null_pairs),
                   "bands_q": {}, "tests": []}
        for dim in DIMS:
            cfg_out["bands_q"][dim] = {str(q): percentile(nulls[dim], q) for q in (90, 95, 97.5)}

        for sid in skill_units:
            s_runs = [r for r in runs if r.get("condition") == "skill" and r["skill_id"] == sid]
            base_lists, skill_lists = defaultdict(list), defaultdict(list)
            for b in base_runs:
                base_lists[b["task_id"]].append(b)
            for s in s_runs:
                skill_lists[s["task_id"]].append(s)
            common = sorted(set(base_lists) & set(skill_lists))
            for dim in DIMS:
                obs = unit_delta(base_lists, skill_lists, common, dim)
                nd = nulls[dim]
                if obs is None or not nd:
                    continue
                n_ge = sum(1 for v in nd if v >= obs)
                p = (n_ge + 1) / (len(nd) + 1)
                b95 = percentile(nd, 95)
                all_tests.append((cfg, sid, dim, obs, p, len(nd)))
                cfg_out["tests"].append({"unit": sid, "dim": dim, "obs": obs,
                                          "p_emp": p, "n_null": len(nd),
                                          "z95": (obs / b95) if b95 else None})
        report["per_config"][cfg] = cfg_out

    m = len(all_tests)
    ranked = sorted(all_tests, key=lambda t: t[4])

    def bh(q):
        thresh, k = None, 0
        for i, t in enumerate(ranked, 1):
            if t[4] <= (i / m) * q:
                thresh, k = t[4], i
        return thresh, k

    bh05, bh10 = bh(0.05), bh(0.10)
    bonf = 0.05 / m
    n_obs_qual = sum(1 for t in all_tests
                     if t[5] and report["per_config"][t[0]]["bands_q"][t[2]]["95"]
                     and t[3] / report["per_config"][t[0]]["bands_q"][t[2]]["95"] > 1.0)

    report["combined"] = {
        "m_tests": m,
        "expected_chance_qualifications": 0.05 * m,
        "observed_qualifications_z95": n_obs_qual,
        "bh05": {"threshold_p": bh05[0], "n_reject": bh05[1]},
        "bh10": {"threshold_p": bh10[0], "n_reject": bh10[1]},
        "bonferroni_p": bonf,
        "surviving_bonferroni": [t for t in all_tests if t[4] <= bonf],
        "top10_by_p": [{"config": t[0], "unit": t[1], "dim": t[2],
                        "obs": round(t[3], 4), "p": round(t[4], 5), "n_null": t[5]}
                       for t in ranked[:10]],
    }
    with open("multiplicity_report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print(f"implicit tests m = {m}  (16 units x {len(DIMS)} dims; saf excluded: degenerate)")
    print(f"chance-level expected qualifications at per-test 5%: {0.05*m:.1f}")
    print(f"observed z95>1 qualifications: {n_obs_qual}")
    print(f"BH q=0.05: threshold p={bh05[0]}, rejects={bh05[1]} | BH q=0.10: p={bh10[0]}, rejects={bh10[1]}")
    print(f"Bonferroni threshold p={bonf:.6f}; surviving={len(report['combined']['surviving_bonferroni'])}")
    print("\ntop-10 smallest empirical p:")
    for t in report["combined"]["top10_by_p"]:
        print(f"  {t['config']}/{t['unit']}/{t['dim']}: obs={t['obs']} p={t['p']} (n_null={t['n_null']})")

    # ---- sensitivity: the qualifying case ----
    print("\n=== sensitivity: gemini / industrial-physical / eff_failed_actions ===")
    runs = load_runs(CONFIGS["gemini-3.5-flash"])
    base_runs = [r for r in runs if r.get("condition") == "baseline"]
    s_runs = [r for r in runs if r.get("condition") == "skill" and "industrial" in r["skill_id"]]
    base_lists, skill_lists = defaultdict(list), defaultdict(list)
    for b in base_runs:
        base_lists[b["task_id"]].append(b)
    for s in s_runs:
        skill_lists[s["task_id"]].append(s)
    common = sorted(set(base_lists) & set(skill_lists))
    obs = unit_delta(base_lists, skill_lists, common, "eff_failed_actions")
    nd = sorted(v for v in (dim_value(p[0], p[1], "eff_failed_actions")
              for p in [(b, r) for r in [x for x in runs if x.get("condition") == "null"]
                        for b in base_by_task_null(r, base_runs)]) if v is not None)
    band95 = percentile(nd, 95)
    print(f"unit delta={obs:.4f}  band95={band95:.4f}  z={obs/band95:.3f}  (driver: 1.424)")
    for q in (90, 97.5):
        bq = percentile(nd, q)
        print(f"  band q={q}: {bq:.4f} -> z={obs/bq:.3f}  {'QUALIFIES' if obs/bq>1 else 'not qualified'}")
    lo, hi = bootstrap_ci(nd, stat_fn=lambda v: percentile(v, 95), iterations=1000, seed=1)
    print(f"  band95 CI [{lo:.4f},{hi:.4f}] -> z range [{obs/hi:.3f},{obs/lo:.3f}]"
          f"  {'robust' if obs/hi>1 else 'NOT robust (upper CI kills z>1)'}")
    loos = sorted(unit_delta(base_lists, skill_lists, common, "eff_failed_actions", drop_task=t)
                  for t in common)
    print(f"  LOO ({len(common)} tasks): delta range [{loos[0]:.4f},{loos[-1]:.4f}]"
          f" -> z range [{loos[0]/band95:.3f},{loos[-1]/band95:.3f}]"
          f"  {'all>1 robust' if loos[0]/band95>1 else 'NOT robust: some task drops kill it'}")
    rb = mean([b.get("failed_actions") for t in common for b in base_lists[t]])
    ra = mean([s.get("failed_actions") for t in common for s in skill_lists[t]])
    n0b = sum(1 for t in common for b in base_lists[t] if not b.get("failed_actions"))
    n0a = sum(1 for t in common for s in skill_lists[t] if not s.get("failed_actions"))
    print(f"  base rates: before={rb:.4f}/run after={ra:.4f}/run over {len(common)} tasks "
          f"(zero-fail runs: {n0b} base, {n0a} skill)")


def base_by_task_null(r, base_runs):
    return [b for b in base_runs if b["task_id"] == r["task_id"]]


if __name__ == "__main__":
    main()
