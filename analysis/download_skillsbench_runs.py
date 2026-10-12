#!/usr/bin/env python3
"""Download SkillsBench v1.1 official-selected trial artifacts.

Fetches result.json + trajectory/acp_trajectory.jsonl for the runs listed in
data/selected_runs.jsonl (official-selected snapshot, HF dataset
benchflow/skillsbench-leaderboard), restricted to the model configurations
given on the command line. Files are served via Git LFS, so the /resolve/
endpoint is required (/raw/ returns LFS pointers).

Resume-capable: existing non-empty files are skipped. Stdlib only.

Usage:
  python3 download_skillsbench_runs.py --config gemini-3.5-flash --config minimax-MiniMax-M3
"""

import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

RESOLVE = "https://hf-mirror.com/datasets/benchflow/skillsbench-leaderboard/resolve/main"
RAW = "https://hf-mirror.com/datasets/benchflow/skillsbench-leaderboard/raw/main"
HERE = os.path.dirname(os.path.abspath(__file__))
SELECTED = os.path.join(HERE, "data", "selected_runs.jsonl")
OUT_ROOT = os.path.join(HERE, "data", "runs")
FILES = ("result.json", "trajectory/acp_trajectory.jsonl")


def fetch(path, dest, retries=3, lfs=True):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "skip"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = f"{RESOLVE if lfs else RAW}/{path}"
    for attempt in range(retries):
        if attempt:
            import time; time.sleep(2 * attempt)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; skillsbench-reanalysis)"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            if data.startswith(b"version https://git-lfs.github.com"):
                raise RuntimeError("LFS pointer instead of content")
            with open(dest, "wb") as fh:
                fh.write(data)
            return "ok"
        except Exception as exc:  # noqa: BLE001 - log and retry
            if attempt == retries - 1:
                return f"fail: {exc}"
    return "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", action="append", required=True,
                    help="substring of agent_group, e.g. gemini-3.5-flash")
    args = ap.parse_args()

    runs = []
    with open(SELECTED, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if any(c in r["agent_group"] for c in args.config):
                runs.append(r)
    print(f"selected runs matching {args.config}: {len(runs)}")

    jobs = []
    for r in runs:
        for rel in FILES:
            src = f"{r['path']}/{rel}"
            dest = os.path.join(OUT_ROOT, r["agent_group"], r["task"],
                                os.path.basename(r["path"]), rel)
            jobs.append((src, dest, rel.endswith(".jsonl")))

    n_ok = n_skip = n_fail = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(fetch, s, d, 3, lfs): (s, d) for s, d, lfs in jobs}
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            if res == "ok":
                n_ok += 1
            elif res == "skip":
                n_skip += 1
            else:
                n_fail += 1
                print(f"FAIL {futs[fut][0]}: {res}", file=sys.stderr)
            if i % 200 == 0:
                print(f"  progress {i}/{len(jobs)} (ok={n_ok} skip={n_skip} fail={n_fail})")
    print(f"done: ok={n_ok} skip={n_skip} fail={n_fail} of {len(jobs)} files")
    if n_fail:
        sys.exit(2)


if __name__ == "__main__":
    main()
