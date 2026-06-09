#!/usr/bin/env python3
"""Utilitários puros de extração de prompts SALLM.

Fornece duas funções puras usadas pela pipeline de paráfrase cega (M3):

- ``extract_docstring``: faz um walk na AST (módulo -> classe -> função) e
  devolve a PRIMEIRA docstring encontrada. Importante: ``ast.get_docstring``
  aplicado só ao módulo devolve ``None`` para docstrings em nível de função
  (caso ``cwe078_0``); por isso o walk recursivo é obrigatório.
- ``parse_target_cwe``: extrai o CWE-alvo canônico a partir do ``id`` do
  prompt (ex.: ``...cwe078_0.py`` -> ``CWE-78``).

Uso (sanity check sobre as 100 linhas do dataset)::

    python3 eval/runner/lib/extract.py

Espera-se ``docstrings: 100/100`` e ``cwe-parse failures: 0``.
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Caminho do dataset SALLM relativo à raiz do repositório.
REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = REPO_ROOT / "eval" / "SALLM" / "Dataset" / "dataset.jsonl"

# Regex do token CWE no id (case-insensitive), ex.: "cwe078", "cwe78".
_CWE_RE = re.compile(r"cwe[_-]?(\d+)", re.IGNORECASE)


def extract_docstring(src: str) -> str | None:
    """Devolve a primeira docstring do código-fonte (módulo->classe->função).

    Percorre a AST em ordem de precedência módulo -> classe -> função,
    descendo recursivamente, e devolve a primeira docstring não-vazia.
    Diferente de ``ast.get_docstring(ast.parse(src))``, que só inspeciona o
    nível de módulo e devolve ``None`` quando a docstring está dentro de uma
    função (padrão dominante nos stubs SALLM).

    Args:
        src: Código-fonte Python (o campo ``prompt`` do dataset).

    Returns:
        A primeira docstring encontrada (já com ``inspect.cleandoc``
        aplicado por ``ast.get_docstring``), ou ``None`` se o código não
        parsear ou não houver docstring alguma.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        logger.warning("fonte não parseável; sem docstring extraível")
        return None

    return _first_docstring(tree)


def _first_docstring(node: ast.AST) -> str | None:
    """Walk recursivo em pré-ordem buscando a primeira docstring.

    Inspeciona o próprio nó (se for módulo/classe/função) e, não havendo
    docstring, desce pelos filhos na ordem em que aparecem no código-fonte.
    A pré-ordem garante a precedência módulo -> classe -> função e respeita
    a ordem textual em níveis irmãos.

    Args:
        node: Nó da AST a inspecionar.

    Returns:
        A docstring encontrada ou ``None``.
    """
    if isinstance(
        node,
        (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
    ):
        doc = ast.get_docstring(node)
        if doc:
            return doc

    for child in ast.iter_child_nodes(node):
        found = _first_docstring(child)
        if found:
            return found

    return None


def extract_signature(src: str) -> str | None:
    """Devolve a assinatura textual da primeira função/método com docstring.

    Localiza o mesmo nó função que ``extract_docstring`` selecionaria (a
    primeira função em pré-ordem que possui docstring) e reconstrói sua
    assinatura: ``nome(args) -> retorno``. A assinatura alimenta a autoria
    cega (T3) junto da docstring, sem expor corpo/CWE/id.

    Args:
        src: Código-fonte Python (o campo ``prompt`` do dataset).

    Returns:
        A assinatura como string (ex.: ``execute_bash()``), ou ``None`` se
        não houver função com docstring (caso raro: docstring de classe pura).
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None

    func = _first_doc_function(tree)
    if func is None:
        return None
    return _format_signature(func)


def _first_doc_function(node: ast.AST) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Acha a primeira função (pré-ordem) que possui docstring.

    Args:
        node: Nó raiz da AST.

    Returns:
        O nó da função, ou ``None``.
    """
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(
        node
    ):
        return node
    for child in ast.iter_child_nodes(node):
        found = _first_doc_function(child)
        if found:
            return found
    return None


def _format_signature(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Reconstrói a assinatura textual de um nó função, sem o corpo.

    Args:
        func: Nó de definição de função.

    Returns:
        ``"nome(args) -> retorno"`` (anotações preservadas quando presentes).
    """
    params: list[str] = []
    a = func.args

    posonly = getattr(a, "posonlyargs", [])
    for arg in posonly:
        params.append(_format_arg(arg))
    if posonly:
        params.append("/")

    for arg in a.args:
        params.append(_format_arg(arg))

    if a.vararg:
        params.append("*" + _format_arg(a.vararg))
    elif a.kwonlyargs:
        params.append("*")
    for arg in a.kwonlyargs:
        params.append(_format_arg(arg))
    if a.kwarg:
        params.append("**" + _format_arg(a.kwarg))

    sig = f"{func.name}({', '.join(params)})"
    if func.returns is not None:
        sig += f" -> {ast.unparse(func.returns)}"
    return sig


def _format_arg(arg: ast.arg) -> str:
    """Formata um único argumento, com anotação quando houver.

    Args:
        arg: Nó de argumento.

    Returns:
        ``"nome"`` ou ``"nome: tipo"``.
    """
    if arg.annotation is not None:
        return f"{arg.arg}: {ast.unparse(arg.annotation)}"
    return arg.arg


def parse_target_cwe(prompt_id: str) -> str:
    """Extrai o CWE-alvo canônico do ``id`` do prompt.

    Ex.: ``"Matching_StackOverflow_SO_cwe078_0.py"`` -> ``"CWE-78"``. Zeros à
    esquerda no número são removidos para a forma canônica do MITRE.

    Args:
        prompt_id: O campo ``id`` da linha do dataset.

    Returns:
        Identificador canônico ``"CWE-<n>"``.

    Raises:
        ValueError: Se nenhum token ``cwe<dígitos>`` for encontrado no id.
    """
    match = _CWE_RE.search(prompt_id)
    if not match:
        raise ValueError(f"id sem token CWE reconhecível: {prompt_id!r}")
    number = int(match.group(1))
    return f"CWE-{number}"


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


def _main() -> None:
    """Sanity check: roda ambas as funções sobre as 100 linhas do dataset."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATASET_PATH,
        help="caminho do dataset.jsonl (padrão: dataset SALLM do repo)",
    )
    args = parser.parse_args()

    rows = _load_dataset(args.dataset)
    total = len(rows)

    with_docstring = 0
    cwe_failures = 0
    for row in rows:
        if extract_docstring(row["prompt"]):
            with_docstring += 1
        else:
            logger.warning("sem docstring: %s", row.get("id"))
        try:
            parse_target_cwe(row["id"])
        except ValueError:
            cwe_failures += 1
            logger.warning("falha de parse CWE: %s", row.get("id"))

    print(f"docstrings: {with_docstring}/{total}")
    print(f"cwe-parse failures: {cwe_failures}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    _main()
