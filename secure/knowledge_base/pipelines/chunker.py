"""
Chunker Semântico para Ingestão RAG

Converte dicts parseados do CWE/OWASP em chunks de documentos autocontidos
com metadata para ingestão no vector store.

Tipos de chunk por CWE:
  - overview:         Descrição + descrição estendida + contexto de severidade
  - mitigation:       Um chunk por estratégia de mitigação (com fase/efetividade)
  - example_insecure: Exemplo de código inseguro com explicação
  - example_secure:   Exemplo de código seguro com explicação
  - detection:        Métodos de detecção e sua efetividade
  - consequences:     Informações de impacto/escopo
  - relationships:    CWEs relacionados e padrões de ataque

Cada chunk é autocontido: inclui o ID e nome do CWE como cabeçalho,
sendo compreensível mesmo fora do contexto original.

Uso:
    python -m knowledge_base.pipelines.chunker [--input PATH] [--stats]
"""

import logging
from pathlib import Path

from knowledge_base.pipelines.cwe_parser import parse_cwe_xml

logger = logging.getLogger(__name__)

DEFAULT_RAW_DIR = Path(__file__).resolve().parent.parent / "raw_data"


def _cwe_header(cwe: dict) -> str:
    """Linha de cabeçalho padrão para todo chunk, garantindo autocontência."""
    return f"{cwe['cwe_id']}: {cwe['name']}"


def _chunk(
    cwe: dict,
    chunk_type: str,
    content: str,
    *,
    extra_metadata: dict | None = None,
) -> dict:
    """Cria um dict de chunk único com conteúdo e metadata."""
    metadata = {
        "cwe_id": cwe["cwe_id"],
        "cwe_name": cwe["name"],
        "chunk_type": chunk_type,
        "abstraction": cwe.get("abstraction", ""),
        "likelihood": cwe.get("likelihood_of_exploit", ""),
    }
    if extra_metadata:
        metadata.update(extra_metadata)

    # ID único para deduplicação
    chunk_id = f"{cwe['cwe_id']}_{chunk_type}"
    if extra_metadata and "index" in extra_metadata:
        chunk_id += f"_{extra_metadata['index']}"

    return {
        "id": chunk_id,
        "content": content,
        "metadata": metadata,
    }


def chunk_overview(cwe: dict) -> list[dict]:
    """Cria chunk de visão geral: descrição + plataformas + probabilidade de exploração."""
    header = _cwe_header(cwe)

    parts = [header, "", cwe["description"]]

    if cwe["extended_description"]:
        parts.extend(["", cwe["extended_description"]])

    if cwe["likelihood_of_exploit"]:
        parts.extend(["", f"Likelihood of Exploit: {cwe['likelihood_of_exploit']}"])

    platforms = cwe.get("applicable_platforms", {})
    langs = platforms.get("languages", [])
    if langs:
        lang_str = ", ".join(
            f"{l['name']} ({l['prevalence']})" if l["prevalence"] else l["name"]
            for l in langs
        )
        parts.extend(["", f"Applicable Languages: {lang_str}"])

    techs = platforms.get("technologies", [])
    if techs:
        tech_str = ", ".join(
            f"{t['name']} ({t['prevalence']})" if t["prevalence"] else t["name"]
            for t in techs
        )
        parts.extend(["", f"Applicable Technologies: {tech_str}"])

    return [_chunk(cwe, "overview", "\n".join(parts))]


def chunk_consequences(cwe: dict) -> list[dict]:
    """Cria um único chunk de consequências resumindo todos os impactos."""
    if not cwe["common_consequences"]:
        return []

    header = _cwe_header(cwe)
    parts = [header, "", "Common Consequences:"]

    for cons in cwe["common_consequences"]:
        scopes = ", ".join(cons["scopes"])
        impacts = ", ".join(cons["impacts"])
        parts.append(f"- Scope: {scopes} | Impact: {impacts}")
        if cons["note"]:
            parts.append(f"  Note: {cons['note']}")

    return [_chunk(cwe, "consequences", "\n".join(parts))]


def chunk_mitigations(cwe: dict) -> list[dict]:
    """Cria um chunk por estratégia de mitigação."""
    chunks = []
    header = _cwe_header(cwe)

    for i, mit in enumerate(cwe["potential_mitigations"]):
        if not mit["description"]:
            continue

        parts = [header, "", "Mitigation:"]

        if mit["phase"]:
            parts.append(f"Phase: {', '.join(mit['phase'])}")
        if mit["strategy"]:
            parts.append(f"Strategy: {mit['strategy']}")
        if mit["effectiveness"]:
            parts.append(f"Effectiveness: {mit['effectiveness']}")

        parts.extend(["", mit["description"]])

        extra = {"index": i}
        if mit["phase"]:
            extra["phase"] = ", ".join(mit["phase"])
        if mit["strategy"]:
            extra["strategy"] = mit["strategy"]

        chunks.append(_chunk(cwe, "mitigation", "\n".join(parts), extra_metadata=extra))

    return chunks


def chunk_examples(cwe: dict) -> list[dict]:
    """Cria chunks dos exemplos demonstrativos, separando código inseguro/seguro."""
    chunks = []
    header = _cwe_header(cwe)

    for i, example in enumerate(cwe["demonstrative_examples"]):
        # Coleta blocos de texto e código do exemplo
        intro_parts = []
        code_blocks = []

        for block in example["blocks"]:
            if block["type"] in ("intro", "body"):
                intro_parts.append(block["content"])
            elif block["type"] == "code":
                code_blocks.append(block)

        context_text = " ".join(intro_parts).strip()

        if not code_blocks:
            # Exemplo apenas de texto — ainda é útil
            if context_text:
                parts = [header, "", f"Example {i + 1}:", "", context_text]
                chunks.append(_chunk(
                    cwe, "example", "\n".join(parts),
                    extra_metadata={"index": i},
                ))
            continue

        # Cria chunks separados para código inseguro e seguro
        for j, code_block in enumerate(code_blocks):
            nature = code_block["nature"]  # "bad", "good", "attack", etc.
            language = code_block["language"]

            if nature == "bad":
                chunk_type = "example_insecure"
                label = "Insecure Code Example"
            elif nature == "good":
                chunk_type = "example_secure"
                label = "Secure Code Example"
            elif nature == "attack":
                chunk_type = "example_attack"
                label = "Attack Example"
            else:
                chunk_type = "example"
                label = "Code Example"

            parts = [header, "", f"{label}:"]
            if language:
                parts.append(f"Language: {language}")
            if context_text:
                parts.extend(["", context_text])
            parts.extend(["", code_block["content"]])

            extra = {"index": f"{i}_{j}", "code_nature": nature}
            if language:
                extra["language"] = language

            chunks.append(_chunk(cwe, chunk_type, "\n".join(parts), extra_metadata=extra))

    return chunks


def chunk_detection(cwe: dict) -> list[dict]:
    """Cria um único chunk de detecção combinando todos os métodos."""
    if not cwe["detection_methods"]:
        return []

    header = _cwe_header(cwe)
    parts = [header, "", "Detection Methods:"]

    for det in cwe["detection_methods"]:
        parts.append(f"\n- Method: {det['method']}")
        if det["effectiveness"]:
            parts.append(f"  Effectiveness: {det['effectiveness']}")
        if det["description"]:
            parts.append(f"  {det['description']}")

    return [_chunk(cwe, "detection", "\n".join(parts))]


def chunk_relationships(cwe: dict) -> list[dict]:
    """Cria chunk de relacionamentos linkando CWEs pai/filho."""
    if not cwe["related_weaknesses"]:
        return []

    header = _cwe_header(cwe)
    parts = [header, "", "Related Weaknesses:"]

    for rel in cwe["related_weaknesses"]:
        parts.append(f"- {rel['nature']}: CWE-{rel['cwe_id']}")

    return [_chunk(cwe, "relationships", "\n".join(parts))]


def chunk_cwe(cwe: dict) -> list[dict]:
    """Gera todos os chunks para uma entrada CWE."""
    chunks = []
    chunks.extend(chunk_overview(cwe))
    chunks.extend(chunk_consequences(cwe))
    chunks.extend(chunk_mitigations(cwe))
    chunks.extend(chunk_examples(cwe))
    chunks.extend(chunk_detection(cwe))
    chunks.extend(chunk_relationships(cwe))
    return chunks


def chunk_all(weaknesses: list[dict]) -> list[dict]:
    """Gera todos os chunks para uma lista de vulnerabilidades CWE parseadas."""
    all_chunks = []
    for cwe in weaknesses:
        cwe_chunks = chunk_cwe(cwe)
        all_chunks.extend(cwe_chunks)
        logger.debug("%s: %d chunks", cwe["cwe_id"], len(cwe_chunks))

    logger.info("Gerados %d chunks no total de %d vulnerabilidades", len(all_chunks), len(weaknesses))
    return all_chunks


if __name__ == "__main__":
    # Sanity check: parseia o XML padrão, gera chunks e mostra contagem.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    weaknesses = parse_cwe_xml(DEFAULT_RAW_DIR / "cwe_top25_2025.xml")
    chunks = chunk_all(weaknesses)
    print(f"{len(chunks)} chunks gerados de {len(weaknesses)} CWEs")
