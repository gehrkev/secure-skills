#!/usr/bin/env python3
"""Constrói o dataset tratado canônico para a pipeline de avaliação M3 (T7).

Mescla as quatro saídas pré-runner em um único JSONL de 100 linhas que ambos
os modos de execução (NL e stub) consomem:

    - T1 (extract.py): ``extract_docstring``, ``parse_target_cwe``
    - T2 (strata.py):  ``classify_cwe(cwe) -> "A"|"B"|"C"``
    - T5 (paraphrases.jsonl): ``nl_paraphrase``, ``nl_provenance``
    - T6 (baseline_hits.jsonl): ``baseline_target_cwe_hit``
    - Fonte: ``eval/SALLM/Dataset/dataset.jsonl`` (campos ``id``, ``prompt``,
      ``insecure_code``)

Mapeamento para os runners:
    ``nl_input   = nl_paraphrase``
    ``stub_input = stub``  (i.e. o campo ``prompt`` verbatim do SALLM)

Schema de saída (9 campos obrigatórios):
    prompt_id               str   — campo ``id`` do dataset SALLM
    target_cwe              str   — ex.: "CWE-78"
    stratum                 str   — "A", "B" ou "C"
    docstring               str   — primeira docstring extraída do ``prompt``
    nl_paraphrase           str   — paráfrase cega gerada em T5
    nl_provenance           str   — deve ser "blind-paraphrase-v1"
    stub                    str   — ``prompt`` SALLM verbatim
    insecure_code           str   — referência SALLM
    baseline_target_cwe_hit bool  — resultado do baseline (T6)

Arquivo de saída: ``eval/runner/dataset/treated_dataset.jsonl`` (100 linhas)

Uso::

    # construir (idempotente — não reconstrói se saída válida já existir)
    python3 build_treated_dataset.py

    # forçar reconstrução
    python3 build_treated_dataset.py --reset

    # validar sem reconstruir
    python3 build_treated_dataset.py --validate
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ajuste do sys.path para importar lib/ (runner root)
# ---------------------------------------------------------------------------

_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

from lib import extract as extract_mod  
from lib.strata import classify_cwe  

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------

_DATASET_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _DATASET_DIR.parents[2]

DATASET_PATH = _REPO_ROOT / "eval" / "SALLM" / "Dataset" / "dataset.jsonl"
PARAPHRASES_PATH = _RUNNER_ROOT / "paraphrase" / "paraphrases.jsonl"
BASELINE_HITS_PATH = _RUNNER_ROOT / "baseline" / "baseline_hits.jsonl"
OUTPUT_PATH = _DATASET_DIR / "treated_dataset.jsonl"

# Campos obrigatórios e seus tipos esperados para validação
_REQUIRED_FIELDS: dict[str, type | tuple[type, ...]] = {
    "prompt_id": str,
    "target_cwe": str,
    "stratum": str,
    "docstring": str,
    "nl_paraphrase": str,
    "nl_provenance": str,
    "stub": str,
    "insecure_code": str,
    "baseline_target_cwe_hit": bool,
}

EXPECTED_ROWS = 100
VALID_STRATA = frozenset({"A", "B", "C"})
EXPECTED_NL_PROVENANCE = "blind-paraphrase-v1"


# ---------------------------------------------------------------------------
# Carregamento dos arquivos auxiliares
# ---------------------------------------------------------------------------


def _load_jsonl(path: Path) -> list[dict]:
    """Carrega um arquivo JSONL em uma lista de dicts.

    Args:
        path: Caminho do arquivo ``.jsonl``.

    Returns:
        Lista de dicts decodificados (linhas vazias ignoradas).

    Raises:
        FileNotFoundError: Se ``path`` não existir.
    """
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _load_paraphrases(path: Path) -> dict[str, dict]:
    """Indexa o arquivo de paráfrases por ``prompt_id``.

    Args:
        path: Caminho de ``paraphrases.jsonl``.

    Returns:
        Dict ``{prompt_id: {nl_paraphrase, nl_provenance, …}}``.
    """
    index: dict[str, dict] = {}
    for row in _load_jsonl(path):
        pid = row["prompt_id"]
        index[pid] = row
    return index


def _load_baseline_hits(path: Path) -> dict[str, bool]:
    """Indexa baseline_hits.jsonl por ``prompt_id``, retornando o bool do hit.

    Args:
        path: Caminho de ``baseline_hits.jsonl``.

    Returns:
        Dict ``{prompt_id: target_cwe_hit}``.
    """
    index: dict[str, bool] = {}
    for row in _load_jsonl(path):
        pid = row["prompt_id"]
        index[pid] = bool(row["target_cwe_hit"])
    return index


# ---------------------------------------------------------------------------
# Construção do dataset tratado
# ---------------------------------------------------------------------------


def build_treated_dataset(
    dataset_path: Path = DATASET_PATH,
    paraphrases_path: Path = PARAPHRASES_PATH,
    baseline_hits_path: Path = BASELINE_HITS_PATH,
    output_path: Path = OUTPUT_PATH,
) -> list[dict]:
    """Mescla as fontes e produz o dataset tratado canônico.

    Args:
        dataset_path: Caminho do dataset SALLM.
        paraphrases_path: Caminho das paráfrases (T5).
        baseline_hits_path: Caminho dos hits do baseline (T6).
        output_path: Onde escrever o JSONL de saída.

    Returns:
        Lista com os 100 dicts resultantes.

    Raises:
        ValueError: Se alguma linha não puder ser mesclada (prompt_id ausente
            nas tabelas auxiliares).
    """
    source_rows = _load_jsonl(dataset_path)
    paraphrases = _load_paraphrases(paraphrases_path)
    baseline_hits = _load_baseline_hits(baseline_hits_path)

    logger.info(
        "Fonte: %d linhas | Paráfrases: %d | Baseline hits: %d",
        len(source_rows),
        len(paraphrases),
        len(baseline_hits),
    )

    output_rows: list[dict] = []
    errors: list[str] = []

    for row in source_rows:
        prompt_id: str = row["id"]

        # T1: extrações da AST
        target_cwe = extract_mod.parse_target_cwe(prompt_id)
        docstring = extract_mod.extract_docstring(row["prompt"])
        if docstring is None:
            logger.warning("sem docstring: %s", prompt_id)
            docstring = ""

        # T2: estrato de cobertura
        stratum = classify_cwe(target_cwe)

        # T5: paráfrase cega
        if prompt_id not in paraphrases:
            errors.append(f"paráfrase ausente: {prompt_id}")
            continue
        para_row = paraphrases[prompt_id]
        nl_paraphrase: str = para_row["nl_paraphrase"]
        nl_provenance: str = para_row["nl_provenance"]

        # T6: baseline hit
        if prompt_id not in baseline_hits:
            errors.append(f"baseline hit ausente: {prompt_id}")
            continue
        baseline_hit: bool = baseline_hits[prompt_id]

        output_rows.append(
            {
                "prompt_id": prompt_id,
                "target_cwe": target_cwe,
                "stratum": stratum,
                "docstring": docstring,
                "nl_paraphrase": nl_paraphrase,
                "nl_provenance": nl_provenance,
                "stub": row["prompt"],
                "insecure_code": row["insecure_code"],
                "baseline_target_cwe_hit": baseline_hit,
            }
        )

    if errors:
        raise ValueError(
            f"{len(errors)} erros de mesclagem:\n" + "\n".join(errors)
        )

    # Escrever saída
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        for out_row in output_rows:
            fh.write(json.dumps(out_row, ensure_ascii=False) + "\n")

    logger.info("Escrito: %s (%d linhas)", output_path, len(output_rows))
    return output_rows


# ---------------------------------------------------------------------------
# Validação
# ---------------------------------------------------------------------------


def validate_output(output_path: Path = OUTPUT_PATH) -> None:
    """Valida o dataset tratado existente.

    Verifica:
    - 100 linhas
    - 9 campos obrigatórios presentes em cada linha
    - Tipos corretos (``baseline_target_cwe_hit`` é bool)
    - ``stratum`` ∈ {A, B, C}
    - ``nl_provenance`` == "blind-paraphrase-v1"

    Args:
        output_path: Caminho do arquivo a validar.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se qualquer violação de esquema for encontrada.
    """
    if not output_path.exists():
        raise FileNotFoundError(f"Arquivo de saída não encontrado: {output_path}")

    rows = _load_jsonl(output_path)
    violations: list[str] = []

    if len(rows) != EXPECTED_ROWS:
        violations.append(
            f"contagem de linhas: esperado {EXPECTED_ROWS}, obtido {len(rows)}"
        )

    for i, row in enumerate(rows):
        row_id = row.get("prompt_id", f"<linha {i}>")

        # Todos os campos presentes
        for field in _REQUIRED_FIELDS:
            if field not in row:
                violations.append(f"{row_id}: campo ausente '{field}'")

        # Tipos
        for field, expected_type in _REQUIRED_FIELDS.items():
            if field in row and not isinstance(row[field], expected_type):
                violations.append(
                    f"{row_id}: campo '{field}' tem tipo {type(row[field]).__name__},"
                    f" esperado {expected_type.__name__ if isinstance(expected_type, type) else str(expected_type)}"
                )

        # baseline_target_cwe_hit deve ser bool estrito (não int)
        if "baseline_target_cwe_hit" in row:
            val = row["baseline_target_cwe_hit"]
            if type(val) is not bool:  # noqa: E721
                violations.append(
                    f"{row_id}: baseline_target_cwe_hit não é bool estrito: {val!r}"
                )

        # stratum ∈ {A, B, C}
        if "stratum" in row and row["stratum"] not in VALID_STRATA:
            violations.append(
                f"{row_id}: stratum inválido '{row['stratum']}'"
            )

        # nl_provenance fixo
        if "nl_provenance" in row and row["nl_provenance"] != EXPECTED_NL_PROVENANCE:
            violations.append(
                f"{row_id}: nl_provenance inesperado '{row['nl_provenance']}'"
            )

    if violations:
        raise ValueError(
            f"{len(violations)} violações de esquema:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


# ---------------------------------------------------------------------------
# Estatísticas auxiliares (usadas no __main__)
# ---------------------------------------------------------------------------


def _compute_stats(rows: list[dict]) -> dict:
    """Computa distribuição de estratos e contagem de baseline hits.

    Args:
        rows: Lista de dicts do dataset tratado.

    Returns:
        Dict com chaves ``strata`` (dict A/B/C -> int) e ``baseline_hits`` (int).
    """
    strata: dict[str, int] = {"A": 0, "B": 0, "C": 0}
    baseline_hits = 0
    for row in rows:
        strata[row["stratum"]] = strata.get(row["stratum"], 0) + 1
        if row["baseline_target_cwe_hit"]:
            baseline_hits += 1
    return {"strata": strata, "baseline_hits": baseline_hits}


# ---------------------------------------------------------------------------
# Entrada principal
# ---------------------------------------------------------------------------


def _main() -> None:
    """Ponto de entrada CLI para construir e/ou validar o dataset tratado."""
    parser = argparse.ArgumentParser(
        description="Constrói o dataset tratado canônico para M3 (T7)."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reconstrói o dataset mesmo que a saída já exista e seja válida.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Apenas valida o dataset existente, sem reconstruir.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")

    if args.validate:
        # Modo somente-validação
        validate_output(OUTPUT_PATH)
        print("100 rows, schema OK")
        return

    # Verificar idempotência: se saída existe e é válida, pular
    if not args.reset and OUTPUT_PATH.exists():
        try:
            validate_output(OUTPUT_PATH)
            rows = _load_jsonl(OUTPUT_PATH)
            stats = _compute_stats(rows)
            print("100 rows, schema OK")
            s = stats["strata"]
            print(
                f"Estratos: A={s['A']} B={s['B']} C={s['C']}"
            )
            print(
                f"Baseline hits: {stats['baseline_hits']}/100"
            )
            print("(saída já existente e válida — use --reset para forçar reconstrução)")
            return
        except (ValueError, FileNotFoundError):
            logger.info("Saída existente inválida; reconstruindo…")

    # Construir
    rows = build_treated_dataset(
        dataset_path=DATASET_PATH,
        paraphrases_path=PARAPHRASES_PATH,
        baseline_hits_path=BASELINE_HITS_PATH,
        output_path=OUTPUT_PATH,
    )

    # Validar resultado
    validate_output(OUTPUT_PATH)

    stats = _compute_stats(rows)
    s = stats["strata"]
    print("100 rows, schema OK")
    print(f"Estratos: A={s['A']} B={s['B']} C={s['C']}")
    print(f"Baseline hits: {stats['baseline_hits']}/100")


if __name__ == "__main__":
    _main()
