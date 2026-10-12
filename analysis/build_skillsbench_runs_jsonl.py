#!/usr/bin/env python3
"""Build first-measurement runs.jsonl from downloaded SkillsBench trials.

One output file per model configuration. Condition assignment is
deterministic and declared ex ante:

  - with-skills trials            -> condition "skill"   (skill_id "<config>__curated-skills")
  - no-skill trials, sorted by    -> condition "null"    (the first trial per task,
    trial hash, first per task          null_kind "rerun": a same-condition matched
                                        rerun measuring natural run-to-run variance,
                                        the closed-API regime's null intervention)
  - remaining no-skill trials     -> condition "baseline"

Action sequences are extracted from trajectory/acp_trajectory.jsonl:
  - every {"type": "tool_call"} event becomes one action
  - action type  = event "kind" (read / edit / execute / ...)
  - tool         = underlying tool name parsed from the result text
                   ("Tool: terminal" / "Tool: file_editor"), fallback to kind
  - arg_schema   = for terminal executions, the head of the shell command
                   (python3 / curl / grep / ...); otherwise the event kind

Safety events are NOT instrumented by the SkillsBench harness, so the field
is omitted entirely (the driver reports the dimension as uninformative
rather than silently zero). Confidence values are likewise absent -> deltaECE
is declared omitted.

Usage:
  python3 build_skillsbench_runs_jsonl.py --config gemini-3.5-flash
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS_ROOT = os.path.join(HERE, "data", "runs")

TOOL_RE = re.compile(r"^Tool:\s*(\w+)", re.M)
CMD_RE = re.compile(r"\$\s*(\S+)")


def parse_actions(traj_path):
    actions = []
    n_failed = 0
    with open(traj_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "tool_call":
                continue
            kind = ev.get("kind") or "?"
            status = ev.get("status")
            if status and status != "completed":
                n_failed += 1
            tool = None
            texts = []
            for c in ev.get("content") or []:
                inner = (c or {}).get("content") or {}
                t = inner.get("text")
                if t:
                    texts.append(t)
            blob = "\n".join(texts)
            m = TOOL_RE.search(blob)
            if m:
                tool = m.group(1)
            title = ev.get("title") or ""
            arg_schema = kind
            cm = CMD_RE.search(title)
            if tool == "terminal" and cm:
                arg_schema = os.path.basename(cm.group(1))
            if tool is None:
                tool = kind
            actions.append({"type": kind, "tool": tool, "arg_schema": arg_schema})
    return actions, n_failed


def extract_tokens(result):
    ar = result.get("agent_result") or {}
    if ar.get("total_tokens"):
        return ar["total_tokens"]
    fm = result.get("final_metrics") or {}
    tot = (fm.get("total_prompt_tokens") or 0) + (fm.get("total_completion_tokens") or 0)
    return tot or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="agent_group substring")
    args = ap.parse_args()

    groups = sorted(
        d for d in os.listdir(RUNS_ROOT)
        if args.config in d and os.path.isdir(os.path.join(RUNS_ROOT, d))
    )
    if not groups:
        sys.exit(f"FAIL: no downloaded group matches {args.config!r}")
    with_group = next((g for g in groups if g.startswith("openhands-with-skills")), None)
    without_group = next((g for g in groups if g.startswith("openhands-no-skills")), None)
    if not (with_group and without_group):
        sys.exit(f"FAIL: need both with-skills and no-skills groups, found {groups}")

    dom_path = os.path.join(HERE, "data", "task_domains.json")
    with open(dom_path, encoding="utf-8") as fh:
        domains = json.load(fh)

    out_path = os.path.join(HERE, f"runs_{args.config}.jsonl")
    n_written = 0
    n_skipped = 0
    records = []

    def load_trials(group, mode):
        trials = {}  # task -> [trial_dir]
        gdir = os.path.join(RUNS_ROOT, group)
        for task in sorted(os.listdir(gdir)):
            tdir = os.path.join(gdir, task)
            if not os.path.isdir(tdir):
                continue
            for trial in sorted(os.listdir(tdir)):
                p = os.path.join(tdir, trial)
                if os.path.isdir(p):
                    trials.setdefault(task, []).append(p)
        return trials

    without_trials = load_trials(without_group, "without")
    with_trials = load_trials(with_group, "with")

    def emit(trial_dir, condition, task, skill_id, null_kind=None):
        nonlocal n_written, n_skipped
        res_p = os.path.join(trial_dir, "result.json")
        traj_p = os.path.join(trial_dir, "trajectory", "acp_trajectory.jsonl")
        if not (os.path.exists(res_p) and os.path.exists(traj_p)):
            n_skipped += 1
            return
        with open(res_p, encoding="utf-8") as fh:
            result = json.load(fh)
        # FAIL-fast guard: the artifact's own declared skill_mode must match
        # the condition we assign from the directory group. A mismatch means
        # the grouping logic is wrong; refuse rather than silently degrade.
        declared = result.get("skill_mode")
        expected = "with-skill" if condition == "skill" else "no-skill"
        if declared != expected:
            sys.exit(
                f"FAIL: {trial_dir} declares skill_mode={declared!r} but is "
                f"assigned condition={condition!r} (expected {expected!r})"
            )
        actions, n_failed = parse_actions(traj_p)
        steps = (result.get("trajectory_summary") or {}).get("steps") or len(actions)
        rec = {
            "run_id": f"{task}__{os.path.basename(trial_dir)}",
            "skill_id": skill_id,
            "condition": condition,
            "null_kind": null_kind,
            "task_id": task,
            "stratum": "benign",
            "outcome": float((result.get("rewards") or {}).get("reward") or 0.0),
            "actions": actions,
            "tokens": extract_tokens(result),
            "steps": steps,
            "failed_actions": n_failed,
        }
        records.append(rec)
        n_written += 1

    for task, dirs in sorted(without_trials.items()):
        for i, d in enumerate(dirs):
            if i == 0 and len(dirs) > 1:
                emit(d, "null", task, "__null__", null_kind="rerun")
            else:
                emit(d, "baseline", task, "__baseline__")
    for task, dirs in sorted(with_trials.items()):
        dom = domains.get(task, "unknown")
        sid = f"{args.config}__{dom}"
        for d in dirs:
            emit(d, "skill", task, sid)

    n_null = sum(1 for r in records if r["condition"] == "null")
    n_base = sum(1 for r in records if r["condition"] == "baseline")
    n_skill = sum(1 for r in records if r["condition"] == "skill")
    with open(out_path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}: {n_written} runs "
          f"(baseline={n_base}, null={n_null}, skill={n_skill}), skipped {n_skipped}")
    if n_null < 30:
        sys.exit(f"FAIL: only {n_null} null runs (<30); protocol minimum unmet")


if __name__ == "__main__":
    main()
