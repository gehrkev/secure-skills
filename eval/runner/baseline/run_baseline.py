#!/usr/bin/env python3
"""Runner de baseline CodeQL para o dataset SALLM (T6, M3).

Para cada um dos 100 prompts do dataset SALLM, roda a análise estática
``codeql-eval --cwe <target>`` sobre o campo ``insecure_code`` e registra
se a ferramenta detectou o CWE-alvo. O resultado é **metadado descritivo**;
todos os prompts são conservados independentemente do veredito.

Saídas (em ``eval/runner/baseline/``):
- ``baseline_hits.jsonl``: uma linha por ``prompt_id`` com ``target_cwe``,
  ``target_cwe_hit`` (bool) e ``result_path`` (JSON bruto salvo no disco).
- ``results/<prompt_id>.json``: saída JSON completa do ``run_eval.py`` por
  prompt.

Flags:
- ``--reset``: apaga e reanalisa tudo. Sem ``--reset``, entradas já gravadas
  em ``baseline_hits.jsonl`` são puladas (retomada incremental).
- ``--limit N``: analisa apenas os primeiros N prompts (desenvolvimento/smoke).
- ``--dataset``: caminho alternativo do ``dataset.jsonl``.

Uso (smoke test — um prompt)::

    python3 eval/runner/baseline/run_baseline.py --limit 1

Uso (rodada completa)::

    python3 eval/runner/baseline/run_baseline.py
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Bootstrap de path para importar lib/ de eval/runner/.
_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

from lib import extract  

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = REPO_ROOT / "eval" / "SALLM" / "Dataset" / "dataset.jsonl"

BASELINE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASELINE_DIR / "results"
HITS_PATH = BASELINE_DIR / "baseline_hits.jsonl"

RUN_EVAL_SCRIPT = REPO_ROOT / ".claude" / "skills" / "codeql-eval" / "scripts" / "run_eval.py"


def _load_dataset(path: Path) -> list[dict]:
    """Carrega o dataset JSONL em uma lista de dicts.

    Args:
        path: Caminho do ``dataset.jsonl``.

    Returns:
        Lista de linhas decodificadas.
    """
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _load_recorded(path: Path) -> dict[str, dict]:
    """Carrega ``baseline_hits.jsonl`` e retorna mapa prompt_id -> entrada.

    Usado na retomada incremental: entradas já gravadas são puladas.

    Args:
        path: Caminho do ``baseline_hits.jsonl``.

    Returns:
        Mapa ``prompt_id -> entrada`` (vazio se o arquivo não existe).
    """
    recorded: dict[str, dict] = {}
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    recorded[entry["prompt_id"]] = entry
    return recorded


def _append_jsonl(path: Path, rec: dict) -> None:
    """Anexa um único registro JSONL com flush + fsync (checkpoint durável).

    Args:
        path: Caminho do arquivo JSONL.
        rec: Registro a anexar.
    """
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def run_codeql_eval(insecure_code: str, target_cwe: str, result_path: Path) -> dict:
    """Roda ``run_eval.py`` sobre o ``insecure_code`` e persiste o resultado JSON.

    Escreve o código em um arquivo ``.py`` temporário, executa o script de
    avaliação CodeQL via subprocess e salva o JSON de saída em ``result_path``.
    O arquivo temporário é apagado ao final, com ou sem erros.

    Args:
        insecure_code: Código inseguro do campo ``insecure_code`` do dataset.
        target_cwe: CWE-alvo no formato canônico (ex.: ``"CWE-78"``).
        result_path: Caminho onde o JSON bruto do resultado será salvo.

    Returns:
        O dicionário parseado da saída de ``run_eval.py``.

    Raises:
        RuntimeError: Se o subprocess falhar ou a saída não for JSON válido.
    """
    tmp_py: Path | None = None
    try:
        # Cria arquivo temporário .py com o código inseguro.
        fd, tmp_str = tempfile.mkstemp(suffix=".py", prefix="codeql_baseline_")
        tmp_py = Path(tmp_str)
        os.close(fd)
        tmp_py.write_text(insecure_code, encoding="utf-8")

        cmd = [
            sys.executable,
            str(RUN_EVAL_SCRIPT),
            "--code", str(tmp_py),
            "--cwe", target_cwe,
        ]
        logger.debug("executando: %s", " ".join(cmd))
        proc = subprocess.run(cmd, capture_output=True, text=True)

        if proc.returncode != 0:
            detail = proc.stderr or proc.stdout or "(sem saída)"
            raise RuntimeError(
                f"run_eval.py falhou (código {proc.returncode}): {detail[:500]}"
            )

        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"saída do run_eval.py não é JSON válido: {proc.stdout[:300]}"
            ) from exc

        # Persiste resultado JSON bruto no disco.
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        return result

    finally:
        if tmp_py is not None and tmp_py.exists():
            tmp_py.unlink()


def run(
    dataset: Path,
    *,
    limit: int | None,
    reset: bool,
) -> None:
    """Roda a análise baseline sobre o dataset (ou um subconjunto).

    Args:
        dataset: Caminho do dataset SALLM.
        limit: Limita aos primeiros N prompts (``None`` = todos).
        reset: Se ``True``, apaga o arquivo de hits e reanálisa tudo.
    """
    rows = _load_dataset(dataset)
    total = len(rows)
    if limit is not None:
        rows = rows[:limit]

    if reset:
        HITS_PATH.unlink(missing_ok=True)
        logger.info("--reset: arquivo de hits apagado, reiniciando do zero")

    recorded = _load_recorded(HITS_PATH)
    n_skipped = 0
    n_hit = 0
    n_miss = 0
    n_error = 0

    for row in rows:
        prompt_id: str = row["id"]

        if prompt_id in recorded:
            n_skipped += 1
            if recorded[prompt_id].get("target_cwe_hit"):
                n_hit += 1
            else:
                n_miss += 1
            logger.info("%s já gravado; pulando (retomada)", prompt_id)
            continue

        try:
            target_cwe = extract.parse_target_cwe(prompt_id)
        except ValueError as exc:
            logger.error("falha ao parsear CWE de %s: %s", prompt_id, exc)
            n_error += 1
            continue

        insecure_code: str = row.get("insecure_code", "")
        if not insecure_code.strip():
            logger.warning("%s: campo insecure_code vazio; pulando", prompt_id)
            n_error += 1
            continue

        # Deriva nome do arquivo de resultado a partir do prompt_id:
        # ex.: "Matching_StackOverflow_SO_cwe078_0.py" -> "cwe078_0.json"
        stem = Path(prompt_id).stem  # remove .py
        # Mantém apenas a parte "cweXXX_N" para nome compacto.
        import re
        m = re.search(r"(cwe\d+[_-]\d+)$", stem, re.IGNORECASE)
        result_name = (m.group(1).lower() if m else stem) + ".json"
        result_path = RESULTS_DIR / result_name

        logger.info("analisando %s (target=%s)…", prompt_id, target_cwe)
        try:
            result = run_codeql_eval(insecure_code, target_cwe, result_path)
            target_cwe_hit: bool = bool(result.get("target_cwe_hit"))
        except RuntimeError as exc:
            logger.error("erro ao analisar %s: %s", prompt_id, exc)
            n_error += 1
            continue

        rel_result_path = result_path.relative_to(REPO_ROOT)
        entry = {
            "prompt_id": prompt_id,
            "target_cwe": target_cwe,
            "target_cwe_hit": target_cwe_hit,
            "result_path": str(rel_result_path),
        }
        _append_jsonl(HITS_PATH, entry)
        recorded[prompt_id] = entry

        if target_cwe_hit:
            n_hit += 1
            logger.info("%s → HIT (target=%s detectado)", prompt_id, target_cwe)
        else:
            n_miss += 1
            logger.info("%s → miss (target=%s não detectado)", prompt_id, target_cwe)

    analyzed = n_hit + n_miss
    print(f"{n_hit}/{total} insecure_code flagged on target CWE")
    if n_error:
        logger.warning("%d prompts com erro (não incluídos no total)", n_error)


def _main() -> None:
    """Ponto de entrada CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATASET_PATH,
        help="caminho do dataset.jsonl (padrão: dataset SALLM do repo)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="analisa apenas os primeiros N prompts",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="apaga o baseline_hits.jsonl e reanálisa tudo do zero",
    )
    args = parser.parse_args()

    run(
        args.dataset,
        limit=args.limit,
        reset=args.reset,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    _main()
