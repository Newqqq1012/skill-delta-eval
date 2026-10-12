#!/usr/bin/env python3
"""Task-level analysis (post-results, read-only): per (config, task) deltas
under the same operators and config-level null bands. Answers: is the 1/16
domain-layer qualification frequency an artifact of aggregation, or does the
task layer show more/fewer qualifications than chance?

Reports: task-level qualification counts, rate vs the 5% per-test chance
rate, and which tasks qualify where.
"""
import json
from collections import defaultdict

from run_first_measurement import (
    load_runs, action_type_seq, tool_event_seq, mean,
    norm_levenshtein, rel_change, percentile,
)
from metrics import EFFICIENCY_COMPONENTS
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIGS = {
    "gemini-3.5-flash": os.path.join(HERE, "runs_gemini-3.5-flash.jsonl"),
    "minimax-MiniMax-M3": os.path.join(HERE, "runs_minimax-MiniMax-M3.jsonl"),
}
DIMS = ["traj", "tool"] + [f"eff_{c}" for c in EFFICIENCY_COMPONENTS]

def dim_value(a, b, dim):
    if dim == "traj":
        return norm_levenshtein(action_type_seq(a), action_type_seq(b))
    if dim == "tool":
        return norm_levenshtein(tool_event_seq(a), tool_event_seq(b))
    if dim.startswith("eff_"):
        return rel_change(b.get(dim[4:]), a.get(dim[4:]))
    raise ValueError(dim)

report = {}
total_tests, total_qual = 0, 0
qual_detail = []

for cfg, path in CONFIGS.items():
    runs = load_runs(path)
    base_runs = [r for r in runs if r.get("condition") == "baseline"]
    null_runs = [r for r in runs if r.get("condition") == "null"]
    base_by_task = defaultdict(list)
    for r in base_runs:
        base_by_task[r["task_id"]].append(r)
    null_pairs = [(b, r) for r in null_runs for b in base_by_task.get(r["task_id"], [])]
    bands = {}
    for dim in DIMS:
        nd = sorted(v for v in (dim_value(p[0], p[1], dim) for p in null_pairs) if v is not None)
        bands[dim] = percentile(nd, 95) if nd else None

    skill_by_task = defaultdict(list)
    for r in runs:
        if r.get("condition") == "skill":
            skill_by_task[r["task_id"]].append(r)

    cfg_out = {"n_tasks": 0, "qualifications": 0, "detail": []}
    for tid in sorted(set(base_by_task) & set(skill_by_task)):
        bs, ss = base_by_task[tid], skill_by_task[tid]
        if not bs or not ss:
            continue
        cfg_out["n_tasks"] += 1
        task_qual = []
        for dim in DIMS:
            if dim in ("traj", "tool"):
                vals = [dim_value(b, s, dim) for b in bs for s in ss]
                vals = [v for v in vals if v is not None]
                obs = mean(vals) if vals else None
            else:
                comp = dim[4:]
                rb = mean([b.get(comp) for b in bs])
                ra = mean([s.get(comp) for s in ss])
                obs = rel_change(ra, rb) if (rb is not None and ra is not None) else None
            band = bands[dim]
            z = (obs / band) if (obs is not None and band) else None
            if z is not None and z > 1.0:
                task_qual.append((dim, round(z, 2), round(obs, 3)))
                total_qual += 1
                qual_detail.append({"config": cfg, "task": tid, "dim": dim,
                                    "z": round(z, 2), "delta": round(obs, 3)})
            total_tests += 1
        if task_qual:
            cfg_out["qualifications"] += len(task_qual)
            cfg_out["detail"].append({"task": tid, "qual": task_qual})
    report[cfg] = cfg_out

n_tasks_total = sum(v["n_tasks"] for v in report.values())
obs_rate = total_qual / total_tests if total_tests else None
summary = {
    "n_task_units": n_tasks_total,
    "n_tests": total_tests,
    "n_qualifications": total_qual,
    "observed_rate": obs_rate,
    "chance_rate": 0.05,
    "expected_by_chance": round(0.05 * total_tests, 1),
    "detail": qual_detail,
}
with open(os.path.join(HERE, "task_level_report.json"), "w") as fh:
    json.dump({"per_config": report, "summary": summary}, fh, indent=2, ensure_ascii=False)

print(f"task units: {n_tasks_total}  tests: {total_tests}  qualifications: {total_qual}")
print(f"observed rate: {obs_rate:.3f} vs chance 0.050  (expected by chance: {0.05*total_tests:.0f})")
print(f"configs: " + ", ".join(f"{c}: {v['n_tasks']} tasks, {v['qualifications']} quals" for c, v in report.items()))
print("\nqualifying (config, task, dim, z):")
for d in qual_detail:
    print(f"  {d['config']}/{d['task']}/{d['dim']}: z={d['z']} delta={d['delta']}")
