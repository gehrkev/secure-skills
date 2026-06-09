#!/usr/bin/env python3
"""Batch runner de avaliação CodeQL para um arm x modality.

Para cada ``candidate.py`` gerado, invoca ``codeql-eval/scripts/run_eval.py``
fora de banda, captura o JSON de resultado, checkpointa por candidato e suporta
4-way parallel sharding para manter o uso de memória/Docker viável.

Layout de entrada::

    eval/runs/<run_id>/gen/<modality>/<arm>/<prompt_id>/s<k>/candidate.py

Layout de saída::

    eval/runs/<run_id>/codeql/<modality>/<arm>/<prompt_id>/s<k>/result.json
    eval/runs/<run_id>/codeql_progress_<modality>_<arm>.jsonl

Uso típico::

    # Rodar avaliação CodeQL para treatment x nl, 4 shards paralelos
    python3 eval/runner/eval/eval_batch.py \\
        --run-id m3_20260601_143022 --arm treatment --modality nl

    # Smoke test (2 prompts, requer T10 smoke slice já existente)
    python3 eval/runner/eval/eval_batch.py \\
        --run-id m3_20260601_143022 --arm treatment --modality nl --smoke

    # Re-rodar tudo para este arm x modality
    python3 eval/runner/eval/eval_batch.py \\
        --run-id m3_20260601_143022 --arm treatment --modality nl --reset-arm
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Ajuste de sys.path — permite importar lib/ como pacote irmão.
# ---------------------------------------------------------------------------
_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

from lib import extract as extract_mod  

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATASET = REPO_ROOT / "eval" / "runner" / "dataset" / "treated_dataset.jsonl"
DEFAULT_RUNS_DIR = REPO_ROOT / "eval" / "runs"

# Caminho do script run_eval.py relativo à raiz do repo.
RUN_EVAL_SCRIPT = REPO_ROOT / ".claude" / "skills" / "codeql-eval" / "scripts" / "run_eval.py"

# Tag da imagem CodeQL usada nesta rodada (R10) — gravada em cada resultado.
CODEQL_IMAGE_TAG = "securecontext-codeql-eval:2.25.4"

# Número padrão de shards paralelos.
DEFAULT_WORKERS = 4


# ---------------------------------------------------------------------------
# Helpers de I/O
# ---------------------------------------------------------------------------

def _load_dataset(path: Path) -> dict[str, dict]:
    """Carrega o dataset tratado, indexado por ``prompt_id``.

    Args:
        path: Caminho do ``treated_dataset.jsonl``.

    Returns:
        Mapa ``prompt_id -> linha`` (vazio se o arquivo não existir).
    """
    dataset: dict[str, dict] = {}
    if not path.exists():
        logger.warning(
            "Dataset não encontrado em %s — CWE será inferido do prompt_id.", path
        )
        return dataset
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                row = json.loads(line)
                pid = row.get("prompt_id") or row.get("id")
                if pid:
                    dataset[pid] = row
    return dataset


def _get_target_cwe(prompt_id: str, dataset: dict[str, dict]) -> str:
    """Obtém o CWE-alvo para um prompt_id.

    Tenta primeiro o dataset tratado; em fallback, faz parse do prompt_id.

    Args:
        prompt_id: Identificador do prompt.
        dataset: Mapa ``prompt_id -> linha`` do dataset tratado.

    Returns:
        CWE canônico, ex.: ``"CWE-78"``.

    Raises:
        ValueError: Se não for possível inferir o CWE.
    """
    row = dataset.get(prompt_id)
    if row:
        cwe = row.get("target_cwe")
        if cwe:
            return cwe
    return extract_mod.parse_target_cwe(prompt_id)


def _load_progress(progress_path: Path) -> set[tuple[str, int]]:
    """Carrega o conjunto de ``(prompt_id, k)`` já avaliados do progress JSONL.

    Args:
        progress_path: Caminho do ``codeql_progress_<modality>_<arm>.jsonl``.

    Returns:
        Conjunto de tuplas ``(prompt_id, k)`` com resultado **conclusivo**
        (``target_cwe_hit`` em ``{true, false}``). Registros com
        ``target_cwe_hit=null`` (falha transitória do CodeQL/Docker) são
        deliberadamente *omitidos* para que o resume os **re-tente** — caso
        contrário uma falha transitória viraria dado faltante permanente.
        A última linha por ``(prompt_id, k)`` vence (re-tentativas anexam).
    """
    done: set[tuple[str, int]] = set()
    if not progress_path.exists():
        return done
    with progress_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                key = (rec["prompt_id"], int(rec["k"]))
            except (json.JSONDecodeError, KeyError):
                logger.warning("Linha de progresso malformada ignorada: %r", line)
                continue
            if rec.get("target_cwe_hit") is None:
                # Falha transitória — re-tentar no próximo resume.
                done.discard(key)
            else:
                done.add(key)
    return done


def _append_progress(path: Path, rec: dict, lock: threading.Lock) -> None:
    """Anexa um registro ao progress JSONL com fsync (checkpoint durável).

    Args:
        path: Caminho do JSONL de progresso.
        rec: Registro a anexar.
        lock: Lock de threading para escrita concorrente segura.
    """
    with lock:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())


# ---------------------------------------------------------------------------
# Scan de candidatos
# ---------------------------------------------------------------------------

def _scan_candidates(gen_root: Path) -> list[tuple[str, int, Path]]:
    """Varre ``gen/<modality>/<arm>/`` recursivamente por ``candidate.py``.

    Args:
        gen_root: Diretório raiz de geração para este arm x modality
                  (``eval/runs/<run_id>/gen/<modality>/<arm>/``).

    Returns:
        Lista de ``(prompt_id, k, candidate_path)`` ordenada.
    """
    candidates: list[tuple[str, int, Path]] = []
    if not gen_root.exists():
        return candidates

    for candidate_path in sorted(gen_root.rglob("candidate.py")):
        # Estrutura esperada: .../<prompt_id>/s<k>/candidate.py
        try:
            sample_dir = candidate_path.parent      # s<k>/
            prompt_dir = sample_dir.parent           # <prompt_id>/
            prompt_id = prompt_dir.name
            k_str = sample_dir.name
            if not k_str.startswith("s"):
                logger.warning("Diretório de sample inesperado: %s", sample_dir)
                continue
            k = int(k_str[1:])
            candidates.append((prompt_id, k, candidate_path))
        except (ValueError, IndexError) as exc:
            logger.warning("Caminho de candidato inesperado %s: %s", candidate_path, exc)

    return candidates


# ---------------------------------------------------------------------------
# Avaliação de um único candidato
# ---------------------------------------------------------------------------

def _evaluate_candidate(
    candidate_path: Path,
    target_cwe: str,
    result_path: Path,
) -> tuple[Optional[bool], Optional[str]]:
    """Invoca ``run_eval.py`` em um candidato e persiste o resultado JSON.

    Nota: o SARIF bruto é gerado internamente pelo ``run_eval.py`` mas não é
    exposto externamente — é um gap conhecido aceito para M3. Apenas o JSON
    resumido (que inclui ``target_cwe_hit``) é preservado aqui.

    Args:
        candidate_path: Caminho do ``candidate.py``.
        target_cwe: CWE-alvo (ex.: ``"CWE-78"``).
        result_path: Onde gravar o ``result.json``.

    Returns:
        Tupla ``(hit, error)``: ``hit`` é ``True``/``False`` conforme
        ``target_cwe_hit``, ou ``None`` em falha (transitória ou não); ``error``
        é uma string curta descrevendo a falha (``None`` em sucesso). O motivo
        é persistido no progresso para que nulos transitórios sejam diagnosticáveis.
    """
    result_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(RUN_EVAL_SCRIPT),
        "--code", str(candidate_path),
        "--cwe", target_cwe,
    ]

    logger.info(
        "CodeQL avaliando %s (cwe=%s)", candidate_path.relative_to(candidate_path.parents[5]),
        target_cwe,
    )

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        logger.error("Timeout ao avaliar %s", candidate_path)
        return None, "timeout"

    if proc.returncode != 0:
        tail = proc.stderr[-2000:]
        logger.error(
            "run_eval.py falhou (rc=%d) para %s:\n%s",
            proc.returncode, candidate_path, tail,
        )
        return None, f"rc={proc.returncode}: {tail[-300:].strip()}"

    try:
        summary = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        logger.error(
            "JSON inválido de run_eval.py para %s: %s\nstdout=%r",
            candidate_path, exc, proc.stdout[:500],
        )
        return None, f"json_decode: {exc}"

    # Adiciona metadados de rastreabilidade ao resultado salvo.
    summary["codeql_image_tag"] = CODEQL_IMAGE_TAG
    result_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary.get("target_cwe_hit"), None


# ---------------------------------------------------------------------------
# Worker de shard
# ---------------------------------------------------------------------------

def _run_shard(
    shard: list[tuple[str, int, Path]],
    arm: str,
    modality: str,
    run_dir: Path,
    dataset: dict[str, dict],
    done_set: set[tuple[str, int]],
    done_lock: threading.Lock,
    progress_path: Path,
    progress_lock: threading.Lock,
    counters: dict,
    counters_lock: threading.Lock,
) -> None:
    """Processa sequencialmente um shard de candidatos dentro de uma thread.

    Args:
        shard: Lista de ``(prompt_id, k, candidate_path)`` a avaliar.
        arm: Braço do experimento.
        modality: Modalidade de entrada.
        run_dir: Diretório raiz da execução.
        dataset: Mapa de dataset tratado (pode estar vazio).
        done_set: Conjunto de ``(prompt_id, k)`` já avaliados (compartilhado).
        done_lock: Lock para leitura/escrita de ``done_set``.
        progress_path: Caminho do JSONL de progresso.
        progress_lock: Lock para escrita no arquivo de progresso.
        counters: Dicionário mutável com contadores ``evaluated`` e ``hits``.
        counters_lock: Lock para os contadores.
    """
    for prompt_id, k, candidate_path in shard:
        cell_key = (prompt_id, k)

        # Verificar se já foi avaliado (checkpoint/resume).
        with done_lock:
            already_done = cell_key in done_set

        if already_done:
            logger.info(
                "arm=%s modality=%s prompt_id=%s k=%d — já avaliado; pulando",
                arm, modality, prompt_id, k,
            )
            continue

        # Determinar CWE-alvo.
        try:
            target_cwe = _get_target_cwe(prompt_id, dataset)
        except ValueError as exc:
            logger.error("Não foi possível determinar CWE para %s: %s", prompt_id, exc)
            target_cwe = "CWE-0"

        # Caminho de saída.
        result_path = (
            run_dir / "codeql" / modality / arm / prompt_id / f"s{k}" / "result.json"
        )

        # Avaliar.
        hit, error = _evaluate_candidate(candidate_path, target_cwe, result_path)

        # Registrar progresso.
        progress_rec: dict = {
            "prompt_id": prompt_id,
            "modality": modality,
            "arm": arm,
            "k": k,
            "target_cwe_hit": hit,  # bool ou None se falha
            "error": error,  # motivo da falha (None se sucesso) — diagnóstico de nulos transitórios
            "result_path": str(result_path),
            "codeql_image_tag": CODEQL_IMAGE_TAG,
        }
        _append_progress(progress_path, progress_rec, progress_lock)

        with done_lock:
            done_set.add(cell_key)

        with counters_lock:
            counters["evaluated"] += 1
            if hit is True:
                counters["hits"] += 1

        logger.info(
            "arm=%s modality=%s prompt_id=%s k=%d — target_cwe_hit=%s",
            arm, modality, prompt_id, k, hit,
        )


# ---------------------------------------------------------------------------
# Orquestrador principal
# ---------------------------------------------------------------------------

def run_eval_batch(
    run_id: str,
    arm: str,
    modality: str,
    dataset_path: Path,
    runs_dir: Path,
    workers: int,
    limit: Optional[int],
    smoke: bool,
    reset_arm: bool,
) -> int:
    """Executa o batch de avaliação CodeQL para um arm x modality.

    Args:
        run_id: Identificador da execução.
        arm: Braço do experimento (``"treatment"`` ou ``"control"``).
        modality: Modalidade de entrada (``"nl"`` ou ``"stub"``).
        dataset_path: Caminho do ``treated_dataset.jsonl``.
        runs_dir: Diretório raiz das execuções.
        workers: Número de shards paralelos.
        limit: Limita aos primeiros N prompts distintos (``None`` = todos).
        smoke: Se ``True``, usa ``limit=2``.
        reset_arm: Se ``True``, apaga o progress deste arm x modality e reavalia tudo.

    Returns:
        Código de saída (0 = sucesso, 1 = erro crítico).
    """
    if smoke:
        limit = 2

    run_dir = runs_dir / run_id
    if not run_dir.exists():
        print(
            f"No run dir found — run generate_batch.py --smoke first "
            f"(expected: {run_dir})"
        )
        return 1

    # Diretório de geração deste arm x modality.
    gen_root = run_dir / "gen" / modality / arm

    # Arquivo de progresso.
    progress_path = run_dir / f"codeql_progress_{modality}_{arm}.jsonl"

    # --reset-arm: apagar progresso e forçar reavaliação.
    if reset_arm:
        if progress_path.exists():
            progress_path.unlink()
            logger.info("--reset-arm: progresso removido (%s)", progress_path.name)

    # Carregar dataset para lookup de CWE.
    dataset = _load_dataset(dataset_path)

    # Carregar progresso existente.
    done_set = _load_progress(progress_path)
    n_already_done = len(done_set)
    logger.info(
        "Progresso carregado: %d candidatos já avaliados (serão pulados).", n_already_done
    )

    # Varrer candidatos.
    all_candidates = _scan_candidates(gen_root)

    if not all_candidates:
        print(
            f"Nenhum candidate.py encontrado em {gen_root}\n"
            f"No run dir found — run generate_batch.py --smoke first"
        )
        return 1

    # Aplicar limit por prompt_id distinto.
    if limit is not None:
        prompt_ids_seen: list[str] = []
        limited: list[tuple[str, int, Path]] = []
        for pid, k, cp in all_candidates:
            if pid not in prompt_ids_seen:
                prompt_ids_seen.append(pid)
            if prompt_ids_seen.index(pid) < limit:
                limited.append((pid, k, cp))
        all_candidates = limited

    total = len(all_candidates)

    # Sharding: dividir em ``workers`` fatias.
    n_workers = max(1, workers)
    shards: list[list[tuple[str, int, Path]]] = [[] for _ in range(n_workers)]
    for i, candidate in enumerate(all_candidates):
        shards[i % n_workers].append(candidate)

    # Contadores compartilhados entre threads.
    counters: dict = {"evaluated": 0, "hits": 0}
    counters_lock = threading.Lock()
    done_lock = threading.Lock()
    progress_lock = threading.Lock()

    if n_workers == 1:
        # Sequencial — mais simples.
        _run_shard(
            shard=shards[0],
            arm=arm,
            modality=modality,
            run_dir=run_dir,
            dataset=dataset,
            done_set=done_set,
            done_lock=done_lock,
            progress_path=progress_path,
            progress_lock=progress_lock,
            counters=counters,
            counters_lock=counters_lock,
        )
    else:
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = [
                executor.submit(
                    _run_shard,
                    shard=shard,
                    arm=arm,
                    modality=modality,
                    run_dir=run_dir,
                    dataset=dataset,
                    done_set=done_set,
                    done_lock=done_lock,
                    progress_path=progress_path,
                    progress_lock=progress_lock,
                    counters=counters,
                    counters_lock=counters_lock,
                )
                for shard in shards
                if shard  # pular shards vazios (quando total < n_workers)
            ]
            for future in as_completed(futures):
                exc = future.exception()
                if exc:
                    logger.error("Shard falhou com exceção: %s", exc)

    evaluated = counters["evaluated"]
    hits = counters["hits"]

    # Incluir candidatos pulados (já avaliados) no total de "avaliados" para
    # relatório de progresso acumulado.
    total_evaluated = evaluated + n_already_done
    print(
        f"{evaluated}/{total} candidates evaluated, {hits} hits "
        f"(total acumulado: {total_evaluated} avaliados, progresso em {progress_path.name})"
    )
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parseia os argumentos da linha de comando.

    Args:
        argv: Lista de argumentos (``None`` usa ``sys.argv``).

    Returns:
        Namespace com os argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--run-id",
        required=True,
        metavar="ID",
        help="Identificador da execução (ex.: m3_20260601_143022).",
    )
    parser.add_argument(
        "--arm",
        required=True,
        choices=["treatment", "control"],
        help="Braço do experimento.",
    )
    parser.add_argument(
        "--modality",
        required=True,
        choices=["nl", "stub"],
        help="Modalidade de entrada.",
    )
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=DEFAULT_RUNS_DIR,
        metavar="PATH",
        help=f"Diretório raiz das execuções (padrão: {DEFAULT_RUNS_DIR}).",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        metavar="PATH",
        help=f"Dataset tratado (padrão: {DEFAULT_DATASET}).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        metavar="N",
        help=f"Shards paralelos (padrão: {DEFAULT_WORKERS}, mín. 1).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Executar apenas os primeiros N prompts distintos (dev/teste).",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Alias para --limit 2 (teste E2E rápido).",
    )
    parser.add_argument(
        "--reset-arm",
        action="store_true",
        help="Apagar o progresso deste arm x modality e reavalar tudo.",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada principal.

    Args:
        argv: Argumentos da linha de comando (``None`` usa ``sys.argv``).

    Returns:
        Código de saída.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    args = _parse_args(argv)
    workers = max(1, args.workers)

    return run_eval_batch(
        run_id=args.run_id,
        arm=args.arm,
        modality=args.modality,
        dataset_path=args.dataset,
        runs_dir=args.runs_dir,
        workers=workers,
        limit=args.limit,
        smoke=args.smoke,
        reset_arm=args.reset_arm,
    )


if __name__ == "__main__":
    sys.exit(main())
