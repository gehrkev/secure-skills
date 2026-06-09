#!/usr/bin/env python3
"""Orquestrador da pipeline de paráfrase cega.

Para cada prompt do dataset SALLM: extrai docstring + deriva assinatura
-> autora a paráfrase NL -> audita neutralidade + fidelidade -> em
caso de reprovação, regenera até ``--max-attempts`` vezes -> **congela** o
resultado.

Saídas (em ``eval/runner/paraphrase/``):
- ``paraphrases.jsonl``: arquivo canônico congelado, uma linha por
  ``prompt_id`` com ``nl_paraphrase``, ``nl_provenance="blind-paraphrase-v1"``,
  ``source_docstring`` e ``attempts``.
- ``paraphrase_audit.jsonl``: resultado de auditoria por ``prompt_id``.

Flags:
- ``--dry-run --limit N``: autora+audita N prompts, imprime os resultados e
  grava em ``*.dryrun.jsonl`` — NÃO congela o arquivo canônico (VERIFY-4).
- ``--reset``: re-autora tudo. Sem ``--reset``, o arquivo congelado é
  autoritativo e entradas já existentes NÃO são re-autoradas (a
  não-determinância fica congelada).

**Checkpoint incremental + retomada:** cada entrada aprovada é anexada ao
canônico assim que passa (``fsync``), e a auditoria é anexada por tentativa.
Se a rodada for interrompida (ex.: limite de janela de 5h faz o ``claude -p``
falhar), todo o progresso já concluído está em disco — basta rodar de novo
(sem ``--reset``) para retomar de onde parou. Prompts reprovados NÃO são
congelados, então são re-tentados na próxima rodada.

Uso (gate VERIFY-4)::

    python3 eval/runner/paraphrase/run_paraphrase.py --dry-run --limit 5
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Bootstrap de path para importar lib/ e os módulos irmãos. 
_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

from lib import cc, extract  
from paraphrase import audit as audit_mod  
from paraphrase import author as author_mod  

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = REPO_ROOT / "eval" / "SALLM" / "Dataset" / "dataset.jsonl"
PARAPHRASE_DIR = Path(__file__).resolve().parent
PARAPHRASES_PATH = PARAPHRASE_DIR / "paraphrases.jsonl"
AUDIT_PATH = PARAPHRASE_DIR / "paraphrase_audit.jsonl"

NL_PROVENANCE = "blind-paraphrase-v1"
DEFAULT_MAX_ATTEMPTS = 3


def _load_dataset(path: Path) -> list[dict]:
    """Carrega o dataset JSONL.

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


def _load_frozen(path: Path) -> dict[str, dict]:
    """Carrega o arquivo congelado existente, indexado por ``prompt_id``.

    Args:
        path: Caminho do ``paraphrases.jsonl``.

    Returns:
        Mapa ``prompt_id -> entrada`` (vazio se o arquivo não existe).
    """
    frozen: dict[str, dict] = {}
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    frozen[entry["prompt_id"]] = entry
    return frozen


def process_prompt(row: dict, max_attempts: int) -> tuple[dict, dict]:
    """Autora + audita um prompt, regenerando até passar ou esgotar tentativas.

    Args:
        row: Linha do dataset (``id``, ``prompt``, ...).
        max_attempts: Número máximo de tentativas de autoria.

    Returns:
        ``(entry, audit_record)``:
            - ``entry``: dict congelável (paráfrase + proveniência + attempts).
            - ``audit_record``: dict com o veredito da última tentativa e o
              histórico de tentativas.

    Raises:
        ValueError: Se a docstring não puder ser extraída do stub.
    """
    prompt_id = row["id"]
    stub = row["prompt"]
    docstring = extract.extract_docstring(stub)
    if not docstring:
        raise ValueError(f"docstring ausente para {prompt_id}")

    history: list[dict] = []
    paraphrase = ""
    result: dict = {}
    for attempt in range(1, max_attempts + 1):
        paraphrase = author_mod.author_paraphrase(stub)
        result = audit_mod.audit(paraphrase, stub)
        history.append(
            {
                "attempt": attempt,
                "paraphrase": paraphrase,
                "passed": result["passed"],
                "lexicon_hits": result["lexicon_hits"],
                "semantic_ok": result["semantic_ok"],
                "reasons": result["reasons"],
            }
        )
        if result["passed"]:
            break
        logger.warning(
            "%s tentativa %d reprovada: %s",
            prompt_id,
            attempt,
            result["reasons"],
        )

    attempts = len(history)
    entry = {
        "prompt_id": prompt_id,
        "nl_paraphrase": paraphrase,
        "nl_provenance": NL_PROVENANCE,
        "source_docstring": docstring,
        "attempts": attempts,
    }
    audit_record = {
        "prompt_id": prompt_id,
        "passed": result["passed"],
        "attempts": attempts,
        "final": {
            "lexicon_hits": result["lexicon_hits"],
            "semantic_ok": result["semantic_ok"],
            "reasons": result["reasons"],
        },
        "history": history,
    }
    return entry, audit_record


def _write_jsonl(path: Path, records: list[dict]) -> None:
    """Grava uma lista de dicts como JSONL (uma linha por registro).

    Args:
        path: Caminho de saída.
        records: Registros a gravar.
    """
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _append_jsonl(path: Path, rec: dict) -> None:
    """Anexa um único registro JSONL e força a escrita em disco.

    Checkpoint durável a crash: abre em modo append, grava uma linha e faz
    ``flush`` + ``fsync`` antes de fechar, para que uma interrupção abrupta
    (ex.: limite de janela de 5h) preserve todo o progresso já concluído.

    Args:
        path: Caminho do JSONL.
        rec: Registro a anexar.
    """
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def run(
    dataset: Path,
    *,
    dry_run: bool,
    limit: int | None,
    reset: bool,
    max_attempts: int,
) -> None:
    """Roda a pipeline sobre o dataset (ou um subconjunto).

    Args:
        dataset: Caminho do dataset SALLM.
        dry_run: Se ``True``, imprime e grava em ``*.dryrun.jsonl`` sem congelar.
        limit: Limita aos primeiros N prompts (``None`` = todos).
        reset: Re-autora tudo, ignorando o arquivo congelado.
        max_attempts: Tentativas máximas de autoria por prompt.
    """
    rows = _load_dataset(dataset)
    if limit is not None:
        rows = rows[:limit]

    # --- Dry-run: acumula em memória e grava nos *.dryrun.jsonl (não congela).
    if dry_run:
        entries: list[dict] = []
        audits: list[dict] = []
        n_failed = 0
        for row in rows:
            entry, audit_record = process_prompt(row, max_attempts)
            entries.append(entry)
            audits.append(audit_record)
            if not audit_record["passed"]:
                n_failed += 1
            print(f"\n=== {row['id']} (attempts={entry['attempts']}) ===")
            print(f"--- source docstring ---\n{entry['source_docstring']}")
            print(f"--- paraphrase ---\n{entry['nl_paraphrase']}")
            print(
                "--- audit --- passed="
                f"{audit_record['passed']} "
                f"lexicon_hits={audit_record['final']['lexicon_hits']} "
                f"semantic_ok={audit_record['final']['semantic_ok']}"
            )
        para_out = PARAPHRASE_DIR / "paraphrases.dryrun.jsonl"
        audit_out = PARAPHRASE_DIR / "paraphrase_audit.dryrun.jsonl"
        _write_jsonl(para_out, entries)
        _write_jsonl(audit_out, audits)
        print(
            f"\n[dry-run] {len(entries)} parafraseados, "
            f"{n_failed} ainda reprovando após {max_attempts} tentativas. "
            f"Gravado em {para_out.name} / {audit_out.name} (canônico NÃO congelado)."
        )
        return

    # --- Rodada real: checkpoint incremental por entrada + retomada.
    if reset:
        PARAPHRASES_PATH.unlink(missing_ok=True)
        AUDIT_PATH.unlink(missing_ok=True)

    frozen = _load_frozen(PARAPHRASES_PATH)
    n_reused = n_new = n_failed = 0
    interrupted = False

    for row in rows:
        prompt_id = row["id"]
        if prompt_id in frozen:
            n_reused += 1
            logger.info("%s já congelado; pulando (retomada)", prompt_id)
            continue

        try:
            entry, audit_record = process_prompt(row, max_attempts)
        except cc.ClaudeError as exc:
            # Falha persistente do claude -p (provável limite de janela 5h):
            # para de forma graciosa — o progresso já está checkpointado.
            logger.error(
                "INTERROMPIDO em %s (provável limite de sessão): %s",
                prompt_id,
                exc,
            )
            interrupted = True
            break

        # Auditoria sempre anexada (inclui tentativas reprovadas); só
        # entradas aprovadas vão ao canônico (reprovadas serão re-tentadas).
        _append_jsonl(AUDIT_PATH, audit_record)
        if audit_record["passed"]:
            _append_jsonl(PARAPHRASES_PATH, entry)
            frozen[prompt_id] = entry
            n_new += 1
        else:
            n_failed += 1
            logger.warning(
                "%s reprovado após %d tentativas; NÃO congelado (será re-tentado)",
                prompt_id,
                max_attempts,
            )

    remaining = sum(1 for r in rows if r["id"] not in frozen)
    status = "INTERROMPIDO" if interrupted else "concluído"
    tail = (
        f", {remaining} restantes — rode de novo (sem --reset) para retomar"
        if remaining
        else ""
    )
    print(
        f"[{status}] {len(frozen)}/{len(rows)} congelados em "
        f"{PARAPHRASES_PATH.name} ({n_reused} reusados, {n_new} novos, "
        f"{n_failed} reprovados nesta rodada{tail})."
    )


def _main() -> None:
    """Ponto de entrada CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="autora+audita e imprime, grava em *.dryrun.jsonl, não congela",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="limita aos primeiros N prompts"
    )
    parser.add_argument(
        "--reset", action="store_true", help="re-autora tudo, ignora o congelado"
    )
    parser.add_argument(
        "--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS
    )
    args = parser.parse_args()

    run(
        args.dataset,
        dry_run=args.dry_run,
        limit=args.limit,
        reset=args.reset,
        max_attempts=args.max_attempts,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    _main()
