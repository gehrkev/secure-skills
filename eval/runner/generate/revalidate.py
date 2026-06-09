#!/usr/bin/env python3
"""Re-valida as células de uma execução de geração **sem regenerar** (R2a fix).

Motivação: a asserção R2a (``assemble.py --prompt`` argv ==
task) estava sendo verificada com um extrator que não reproduzia o
*unescaping* de aspas-duplas do bash — então células em que o modelo escapou
crases (`` \\` ``) eram marcadas ``invalid`` mesmo tendo passado os bytes
corretos a ``assemble.py``. As gerações estão **congeladas** (regenerar seria
viés de seleção/priming); o bug é do *verificador*, não da geração. Este script
re-executa as asserções sobre os artefatos salvos (trace + candidate) com o
verificador corrigido e atualiza ``progress.jsonl`` in-place.

Determinístico e idempotente: lê ``session.jsonl``/``result``/``candidate.py`` do
disco, recomputa status, e reescreve o progresso (backup em
``progress.jsonl.bak``). Nunca chama ``claude``.

Uso::

    python3 eval/runner/generate/revalidate.py --run-id m3_20260601_150010
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

from generate import session as session_mod  
from verify1 import verify1_assert as va  

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / "eval" / "runs"
DEFAULT_DATASET = REPO_ROOT / "eval" / "runner" / "dataset" / "treated_dataset.jsonl"


def _load_dataset(path: Path) -> dict[str, dict]:
    """Indexa o dataset tratado por ``prompt_id``."""
    ds: dict[str, dict] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                row = json.loads(line)
                ds[row["prompt_id"]] = row
    return ds


def _task_for(row: dict, modality: str) -> str:
    """Retorna o input de task da modalidade (nl_paraphrase ou stub verbatim)."""
    return row["nl_paraphrase"] if modality == "nl" else row["stub"]


def _model_from_manifest(run_dir: Path) -> str | None:
    """Lê o model id fixado do manifest da execução, se houver."""
    mani = run_dir / "manifest.json"
    if not mani.exists():
        return None
    data = json.loads(mani.read_text(encoding="utf-8"))
    # tolerante a layout: procura uma chave que contenha o id pinado
    for key in ("model", "model_id", "pinned_model"):
        if isinstance(data.get(key), str):
            return data[key]
    blob = json.dumps(data)
    if "claude-haiku-4-5-20251001" in blob:
        return "claude-haiku-4-5-20251001"
    return None


def revalidate_run(run_id: str, runs_dir: Path, dataset_path: Path) -> int:
    """Re-valida todas as células de ``run_id`` a partir dos artefatos salvos."""
    run_dir = runs_dir / run_id
    progress_path = run_dir / "progress.jsonl"
    if not progress_path.exists():
        print(f"progress.jsonl não encontrado em {run_dir}")
        return 1

    dataset = _load_dataset(dataset_path)
    model = _model_from_manifest(run_dir)
    if model is None:
        logger.warning("model id não encontrado no manifest — R3 pode reprovar")
        model = "claude-haiku-4-5-20251001"

    # Última linha vence por célula (resume pode ter anexado).
    by_cell: dict[tuple, dict] = {}
    for line in progress_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        by_cell[(rec["prompt_id"], rec["modality"], rec["arm"], rec["k"])] = rec

    flipped = 0          # invalid -> valid
    regressed = 0        # valid -> invalid (não deveria acontecer)
    still_invalid = 0
    skipped = 0
    byte_exact = Counter()  # True/False/None
    new_records: list[dict] = []

    for cell, rec in by_cell.items():
        prompt_id, modality, arm, k = cell
        trace_path = rec.get("trace_path")
        if not trace_path or not Path(trace_path).exists():
            skipped += 1
            new_records.append(rec)
            continue

        events = [
            json.loads(l)
            for l in Path(trace_path).read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        result_obj = va.final_result(events)
        candidate_py = Path(rec["candidate_path"]) if rec.get("candidate_path") else (
            run_dir / "gen" / modality / arm / prompt_id / f"s{k}" / "candidate.py"
        )
        row = dataset.get(prompt_id)
        if row is None:
            skipped += 1
            new_records.append(rec)
            continue
        task = _task_for(row, modality)

        assertions, meta = session_mod._run_assertions(
            events=events,
            result_obj=result_obj,
            arm=arm,
            task=task,
            model=model,
            candidate_py=Path(candidate_py),
        )
        all_pass = session_mod._all_assertions_pass(assertions, arm)
        new_status = "valid" if all_pass else "invalid"
        old_status = rec.get("status")

        if old_status != "valid" and new_status == "valid":
            flipped += 1
        elif old_status == "valid" and new_status != "valid":
            regressed += 1
        elif new_status != "valid":
            still_invalid += 1

        byte_exact[meta["r2a_byte_exact"]] += 1

        rec = dict(rec)
        rec["status"] = new_status
        rec["invalid_reason"] = (
            None if all_pass
            else f"asserções falhas: {[k2 for k2, v in assertions.items() if v is False]}"
        )
        rec["r2a_byte_exact"] = meta["r2a_byte_exact"]
        rec["revalidated"] = True
        new_records.append(rec)

    # Backup + reescrita atômica.
    backup = progress_path.with_suffix(".jsonl.bak")
    if not backup.exists():
        backup.write_text(progress_path.read_text(encoding="utf-8"), encoding="utf-8")
    tmp = progress_path.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for rec in new_records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    tmp.replace(progress_path)

    n_valid = sum(1 for r in new_records if r.get("status") == "valid")
    total = len(new_records)
    print(f"=== revalidate {run_id} ===")
    print(f"total células        : {total}")
    print(f"válidas (após fix)   : {n_valid}")
    print(f"invalid->valid       : {flipped}")
    print(f"ainda invalid        : {still_invalid}")
    print(f"valid->invalid (!)   : {regressed}")
    print(f"puladas (sem trace)  : {skipped}")
    print(f"R2a byte-exato       : true={byte_exact[True]} "
          f"false={byte_exact[False]} n/a-control={byte_exact[None]}")
    print(f"backup               : {backup}")
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--run-id", required=True, help="Execução a re-validar.")
    ap.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = ap.parse_args(argv)
    return revalidate_run(args.run_id, args.runs_dir, args.dataset)


if __name__ == "__main__":
    sys.exit(main())
