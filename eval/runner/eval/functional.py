#!/usr/bin/env python3
"""Verificador de sinal funcional pass@k por candidato.

Para cada ``candidate.py`` verifica três critérios — um **piso de sanidade**
("o código roda?"), deliberadamente mínimo:

1. ``parses`` — ``ast.parse`` não lança SyntaxError (equivale ao
   ``is_compilable`` do SALLM).
2. ``defines_symbol`` — define **pelo menos um** símbolo chamável de nível de
   módulo (função/classe). É uma checagem de *liveness* neutra à modalidade,
   **não** um casamento de nome exato. Casamento exato foi rejeitado porque
   confunde 1:1 com a modalidade: no ``stub`` o modelo herda a assinatura (nome
   ≈ sempre presente), no ``nl`` o modelo escolhe o próprio nome (≈ sempre
   ausente) — penalizando o NL por liberdade de nomeação, não por incorreção.
3. ``imports_clean`` — o módulo pode ser importado sem levantar exceção
   (subprocess com timeout de 10 s), usando um venv com as dependências
   *pinned* do SALLM (Flask/Flask-SQLAlchemy/pycryptodome). Sem o venv, qualquer
   candidato que importe Flask falharia por dependência ausente, não por defeito.

**Caveat / trabalho futuro (TCC):** este é um sinal de *funciona/compila*, não
de **corretude comportamental**. O SALLM define corretude via testes por prompt
(``test_<id>.py::test_correctness``, entrada->saída). Reproduzir esse pass@k
comportamental (ou outras suítes de avaliação funcional) está fora do escopo do
M3 e é registrado como melhoria futura — aqui, "se roda, está ok".

Uso típico::

    # Varrer todos os candidatos de uma execução
    python3 eval/runner/eval/functional.py --run m3_20260601_143022

    # Smoke test (candidatos da execução m3_* mais recente)
    python3 eval/runner/eval/functional.py --smoke
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
import subprocess
import sys
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

IMPORT_TIMEOUT = 10  # segundos

# Venv com as dependências pinned do SALLM para a checagem de import.
# Construído uma vez por ``functional_requirements.txt`` (ver setup_env.sh).
# Fallback para ``sys.executable`` se o venv não existir (degrada para
# "stdlib-only", com aviso).
_FUNCTIONAL_VENV_PY = Path(__file__).resolve().parent / "functional_venv" / "bin" / "python"


def _check_python() -> str:
    """Retorna o interpretador para a checagem de import.

    Prefere o venv com dependências SALLM; cai para ``sys.executable`` (e avisa)
    se o venv ainda não foi construído.
    """
    if _FUNCTIONAL_VENV_PY.exists():
        return str(_FUNCTIONAL_VENV_PY)
    logger.warning(
        "functional_venv ausente em %s — imports_clean rodará só com stdlib "
        "(candidatos que importam Flask etc. falharão por dependência ausente). "
        "Construa o venv: bash eval/runner/eval/setup_env.sh",
        _FUNCTIONAL_VENV_PY.parent,
    )
    return sys.executable


# ---------------------------------------------------------------------------
# Função principal de verificação funcional
# ---------------------------------------------------------------------------

def functional_ok(
    candidate_path: Path,
) -> dict[str, bool]:
    """Verifica o sinal funcional de um candidato para pass@k.

    Realiza três verificações independentes (piso de sanidade — ver docstring
    do módulo):

    - ``parses``: o arquivo é Python sintaticamente válido.
    - ``defines_symbol``: define ≥1 símbolo chamável de nível de módulo
      (função/classe). Liveness neutra à modalidade, **não** casamento de nome.
    - ``imports_clean``: o módulo importa sem exceção (venv com deps SALLM).

    Args:
        candidate_path: Caminho absoluto do ``candidate.py``.

    Returns:
        Dicionário ``{"parses": bool, "defines_symbol": bool, "imports_clean": bool}``.
    """
    try:
        src = candidate_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("Não foi possível ler %s: %s", candidate_path, exc)
        return {"parses": False, "defines_symbol": False, "imports_clean": False}

    # 1. parses
    try:
        tree = ast.parse(src)
        parses = True
    except SyntaxError:
        parses = False
        tree = None

    # 2. defines_symbol — liveness: ≥1 função/classe de nível de módulo.
    if not parses or tree is None:
        defines_symbol = False
    else:
        defines_symbol = any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            for node in tree.body
        )

    # 3. imports_clean — executa o módulo via importlib em subprocesso isolado
    import_snippet = (
        "import importlib.util, sys; "
        f"spec = importlib.util.spec_from_file_location('_c', {str(candidate_path)!r}); "
        "m = importlib.util.module_from_spec(spec); "
        "spec.loader.exec_module(m)"
    )
    try:
        result = subprocess.run(
            [_check_python(), "-c", import_snippet],
            capture_output=True,
            text=True,
            timeout=IMPORT_TIMEOUT,
        )
        imports_clean = result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.warning("Timeout ao importar %s", candidate_path)
        imports_clean = False
    except OSError as exc:
        logger.warning("Erro ao importar %s: %s", candidate_path, exc)
        imports_clean = False

    return {
        "parses": parses,
        "defines_symbol": defines_symbol,
        "imports_clean": imports_clean,
    }


# ---------------------------------------------------------------------------
# Helpers de I/O
# ---------------------------------------------------------------------------

def _load_dataset(path: Path) -> dict[str, dict]:
    """Carrega o dataset tratado, indexado por ``prompt_id``.

    Args:
        path: Caminho do ``treated_dataset.jsonl``.

    Returns:
        Mapa ``prompt_id -> linha`` (vazio se não existir).
    """
    dataset: dict[str, dict] = {}
    if not path.exists():
        logger.warning("Dataset não encontrado em %s.", path)
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


def _get_expected_symbol(
    prompt_id: str,
    modality: str,
    dataset: dict[str, dict],
    candidate_path: Path,
) -> Optional[str]:
    """Infere o símbolo esperado para um candidato.

    Tenta obter o stub/nl_paraphrase do dataset e extrair a assinatura. Em
    fallback, extrai a assinatura diretamente do ``candidate.py``.

    Args:
        prompt_id: Identificador do prompt.
        modality: Modalidade (``"nl"`` ou ``"stub"``).
        dataset: Mapa do dataset tratado.
        candidate_path: Caminho do ``candidate.py`` (fallback).

    Returns:
        Nome do símbolo esperado, ou ``None`` se não for possível inferir.
    """
    row = dataset.get(prompt_id)
    stub_src: Optional[str] = None

    if row:
        if modality == "stub":
            stub_src = row.get("stub") or row.get("nl_paraphrase")
        else:
            stub_src = row.get("nl_paraphrase") or row.get("stub")

    if not stub_src:
        # Fallback: extrair do próprio candidato.
        try:
            stub_src = candidate_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    sig = extract_mod.extract_signature(stub_src)
    if not sig:
        return None
    return sig.split("(")[0]


# ---------------------------------------------------------------------------
# Varredura de candidatos (todos os arms/modalities de uma execução)
# ---------------------------------------------------------------------------

def _scan_all_candidates(run_dir: Path) -> list[tuple[str, str, str, int, Path]]:
    """Varre todos os ``candidate.py`` sob ``gen/*/`` de uma execução.

    Args:
        run_dir: Diretório raiz da execução.

    Returns:
        Lista de ``(prompt_id, arm, modality, k, candidate_path)`` ordenada.
    """
    gen_root = run_dir / "gen"
    candidates: list[tuple[str, str, str, int, Path]] = []

    if not gen_root.exists():
        return candidates

    for candidate_path in sorted(gen_root.rglob("candidate.py")):
        # Estrutura: gen/<modality>/<arm>/<prompt_id>/s<k>/candidate.py
        try:
            sample_dir = candidate_path.parent       # s<k>
            prompt_dir = sample_dir.parent            # <prompt_id>
            arm_dir = prompt_dir.parent               # <arm>
            modality_dir = arm_dir.parent             # <modality>

            prompt_id = prompt_dir.name
            arm = arm_dir.name
            modality = modality_dir.name
            k_str = sample_dir.name

            if not k_str.startswith("s"):
                logger.warning("Diretório de sample inesperado: %s", sample_dir)
                continue
            k = int(k_str[1:])
            candidates.append((prompt_id, arm, modality, k, candidate_path))
        except (ValueError, IndexError) as exc:
            logger.warning("Caminho inesperado %s: %s", candidate_path, exc)

    return candidates


# ---------------------------------------------------------------------------
# Modo --run: varrer execução e imprimir tabela
# ---------------------------------------------------------------------------

def run_functional_check(
    run_id: str,
    runs_dir: Path,
    dataset_path: Path,
) -> int:
    """Verifica todos os candidatos de uma execução e imprime tabela + JSONL.

    Args:
        run_id: Identificador da execução.
        runs_dir: Diretório raiz das execuções.
        dataset_path: Caminho do ``treated_dataset.jsonl``.

    Returns:
        Código de saída (0 = ok, 1 = diretório não encontrado).
    """
    run_dir = runs_dir / run_id
    if not run_dir.exists():
        print(f"No run dir found — run generate_batch.py --smoke first (expected: {run_dir})")
        return 1

    dataset = _load_dataset(dataset_path)
    candidates = _scan_all_candidates(run_dir)

    if not candidates:
        print(f"Nenhum candidate.py encontrado em {run_dir / 'gen'}")
        return 1

    results: list[dict] = []
    n_parses = n_defines = n_imports = 0

    # Cabeçalho da tabela.
    header = f"{'prompt_id':<40} {'arm':<12} {'modality':<10} {'k':>3}  {'parses':<8} {'defines_symbol':<16} {'imports_clean'}"
    print(header)
    print("-" * len(header))

    for prompt_id, arm, modality, k, candidate_path in candidates:
        # Informativo apenas — NÃO usado no booleano defines_symbol (liveness).
        expected_symbol = _get_expected_symbol(prompt_id, modality, dataset, candidate_path)
        result = functional_ok(candidate_path)

        parses = result["parses"]
        defines = result["defines_symbol"]
        imports = result["imports_clean"]

        if parses:
            n_parses += 1
        if defines:
            n_defines += 1
        if imports:
            n_imports += 1

        print(
            f"{prompt_id:<40} {arm:<12} {modality:<10} {k:>3}  "
            f"{str(parses):<8} {str(defines):<16} {str(imports)}"
        )

        results.append({
            "prompt_id": prompt_id,
            "arm": arm,
            "modality": modality,
            "k": k,
            "candidate_path": str(candidate_path),
            "expected_symbol": expected_symbol,
            "parses": parses,
            "defines_symbol": defines,
            "imports_clean": imports,
        })

    total = len(results)
    print()
    print(
        f"TOTAL: {total} candidates, "
        f"{n_parses} parses, "
        f"{n_defines} defines_symbol, "
        f"{n_imports} imports_clean"
    )

    # Gravar JSONL de resultados.
    out_path = run_dir / "functional_results.jsonl"
    with out_path.open("w", encoding="utf-8") as fh:
        for rec in results:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\nResultados gravados em {out_path}")

    return 0


# ---------------------------------------------------------------------------
# Modo --smoke: execução m3_* mais recente
# ---------------------------------------------------------------------------

def _find_latest_run(runs_dir: Path) -> Optional[Path]:
    """Encontra o diretório de execução m3_* mais recente.

    Args:
        runs_dir: Diretório raiz das execuções.

    Returns:
        Caminho do diretório mais recente, ou ``None`` se não houver nenhum.
    """
    if not runs_dir.exists():
        return None
    candidates = sorted(runs_dir.glob("m3_*"))
    return candidates[-1] if candidates else None


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

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--run",
        metavar="ID",
        help="Identificador da execução a verificar.",
    )
    mode_group.add_argument(
        "--smoke",
        action="store_true",
        help="Auto-seleciona a execução m3_* mais recente (T10 smoke slice).",
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

    if args.smoke:
        run_dir = _find_latest_run(args.runs_dir)
        if run_dir is None:
            print(
                f"No run dir found — run generate_batch.py --smoke first "
                f"(expected: {args.runs_dir}/m3_*)"
            )
            return 1
        run_id = run_dir.name
        print(f"[smoke] Usando execução mais recente: {run_id}")
    else:
        run_id = args.run

    return run_functional_check(
        run_id=run_id,
        runs_dir=args.runs_dir,
        dataset_path=args.dataset,
    )


if __name__ == "__main__":
    sys.exit(main())
