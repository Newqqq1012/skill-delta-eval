# Skill Delta Evaluation — Anonymous Analysis Package

This package contains the complete analysis pipeline for the paper
*"From Task Completion to Behavioral Shift: Rethinking Agent Skill Evaluation"*.

It reproduces, from public data alone:

- the first measurement on 1,014 paired SkillsBench trajectories
  (Section "A First Measurement on Public Paired Traces", Table 3, Figure 2);
- the null-band construction, qualification, and adoption logic;
- the post-hoc multiplicity accounting and sensitivity analyses;
- the task-level reanalysis (171 task units, 855 implicit tests).

## Layout

```
analysis/                     core pipeline (pure Python 3 stdlib; no dependencies)
  metrics.py                  operators: normalized Levenshtein, JSD, rel. change,
                              bootstrap CI, percentile (all with fixed seeds)
  run_first_measurement.py    pre-registered driver v1.1: unit-level deltas,
                              rerun-null bands, z-scores, qualification,
                              Pareto adoption, cosmetic-churn flag
  multiplicity_accounting.py  post-hoc: 80 implicit tests, empirical p-values,
                              BH/Bonferroni, sensitivity (band quantiles,
                              band CI, leave-one-task-out)
  task_level_analysis.py      post-hoc: task-granularity deltas + label-permutation
  build_skillsbench_runs_jsonl.py   archive -> runs.jsonl converter
  download_skillsbench_runs.py      fetches the public SkillsBench per-run archive
  runs_gemini-3.5-flash.jsonl       518 runs (261 skill / 257 baseline)
  runs_minimax-MiniMax-M3.jsonl     496 runs (247 skill / 249 baseline)
  results_gemini/ results_minimax/  driver outputs behind Table 3 (results.json,
                                    report.md — machine- and human-readable)
  multiplicity_report.json          full multiplicity + sensitivity output
  task_level_report.json            full task-level output
figures/
  make_figure2.py             Figure 1 (schematic, Appendix A worked example)
  make_figure2_pilot.py       Figure 2 (reads analysis/results_*/results.json)
  *.pdf                       compiled figures used in the paper
```

## Reproduction

```bash
cd analysis
# 1. unit-level analysis (Table 3, Figure 2 data)
python3 run_first_measurement.py runs_gemini-3.5-flash.jsonl --out results_gemini/
python3 run_first_measurement.py runs_minimax-MiniMax-M3.jsonl --out results_minimax/

# 2. multiplicity accounting + sensitivity of the qualifying case
python3 multiplicity_accounting.py

# 3. task-level reanalysis
python3 task_level_analysis.py

# 4. figures
cd ../figures && python3 make_figure2_pilot.py
```

All bootstrap seeds are fixed in-code; every number in the paper's Table 3,
the multiplicity paragraph, and the task-level paragraph is reproduced
deterministically by these runs.

## Data provenance

The 1,014 paired trajectories are the publicly released per-run records of
SkillsBench (cited in the paper). `download_skillsbench_runs.py` documents the
fetch; the archived runs are used unmodified. No new benchmark episodes were
executed for any analysis in the paper.

## Honesty boundaries

- The driver was frozen **pre-results** (v1.1 changelog in the file header
  declares the only post-freeze changes, made before any real data existed).
- The multiplicity and task-level analyses are **post-hoc** and are reported
  as such in the paper; no synthetic or smoke-test output enters any paper number.
