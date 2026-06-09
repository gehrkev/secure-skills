# Rerun metrics from saved generations

This reproduces aggregation + statistics from already-generated candidates without re-running any Claude Code sessions.

## Command

```bash
python3 eval/runner/aggregate/aggregate.py --run-id m3_20260601_150010 [--runs-dir eval/runs/]
```

## What it reads

- `codeql_progress_<modality>_<arm>.jsonl` — CodeQL security signal
- `functional_results.jsonl` — Functional signal
- `eval/runner/dataset/treated_dataset.jsonl` — Strata + metadata

## What it writes

- `metrics/per_prompt.csv`, `per_stratum.csv`, `pooled.json`
- `metrics/plots/*.png`

## CodeQL tool label

All security metrics are qualified by CodeQL image tag recorded in `manifest.json`.
