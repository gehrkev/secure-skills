"""
Parser XML do CWE

Parseia arquivos XML do CWE (baixados pelo cwe_downloader) em dicts Python
estruturados, prontos para chunking e ingestão RAG.

Função principal: parse_cwe_xml(xml_path) -> list[dict]
"""

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path

logger = logging.getLogger(__name__)

# Namespaces declarados na raiz do XML do CWE (<Weakness_Catalog xmlns="..." xmlns:xhtml="...">).
# Todo tag sem prefixo no arquivo (ex: <Weakness>, <Description>) pertence ao namespace "cwe".
# O "xhtml" aparece dentro de campos de descrição que embbutem HTML.
# Sem esse mapeamento, o ElementTree exigiria o URI completo em cada busca:
#   root.findall(".//{http://cwe.mitre.org/cwe-7}Weakness")
# Com ele, escrevemos simplesmente:
#   root.findall(".//cwe:Weakness", NS)
NS = {"cwe": "http://cwe.mitre.org/cwe-7", "xhtml": "http://www.w3.org/1999/xhtml"}

DEFAULT_RAW_DIR = Path(__file__).resolve().parent.parent / "raw_data"


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def parse_cwe_xml(xml_path: Path) -> list[dict]:
    """Parseia um arquivo XML do CWE e retorna lista de dicts estruturados."""
    logger.info("Parseando %s", xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    weaknesses = []
    for weakness in root.findall(".//cwe:Weakness", NS):
        parsed = parse_weakness(weakness)
        weaknesses.append(parsed)
        logger.debug("Parseado %s: %s", parsed["cwe_id"], parsed["name"])

    logger.info("Parseadas %d vulnerabilidades de %s", len(weaknesses), xml_path.name)
    return weaknesses


# ---------------------------------------------------------------------------
# Parser de vulnerabilidade individual
# ---------------------------------------------------------------------------

def parse_weakness(weakness: ET.Element) -> dict:
    """Parseia um único elemento <Weakness> em um dict estruturado."""
    cwe_id = weakness.get("ID", "")
    name = weakness.get("Name", "")

    desc_el = weakness.find("cwe:Description", NS)
    description = _text_content(desc_el) if desc_el is not None else ""

    ext_desc_el = weakness.find("cwe:Extended_Description", NS)
    extended_description = _text_content(ext_desc_el) if ext_desc_el is not None else ""

    likelihood = weakness.find("cwe:Likelihood_Of_Exploit", NS)
    likelihood_text = likelihood.text.strip() if likelihood is not None and likelihood.text else ""

    return {
        "cwe_id": f"CWE-{cwe_id}",
        "name": name,
        "abstraction": weakness.get("Abstraction", ""),
        "status": weakness.get("Status", ""),
        "description": description,
        "extended_description": extended_description,
        "likelihood_of_exploit": likelihood_text,
        "applicable_platforms": _parse_platforms(weakness),
        "common_consequences": _parse_consequences(weakness),
        "potential_mitigations": _parse_mitigations(weakness),
        "demonstrative_examples": _parse_examples(weakness),
        "detection_methods": _parse_detection_methods(weakness),
        "related_weaknesses": _parse_related_weaknesses(weakness),
    }


# ---------------------------------------------------------------------------
# Parsers de subseções (chamados por parse_weakness)
# ---------------------------------------------------------------------------

def _parse_platforms(weakness: ET.Element) -> dict:
    """Parseia a seção Applicable_Platforms."""
    platforms = {"languages": [], "technologies": []}
    container = weakness.find("cwe:Applicable_Platforms", NS)
    if container is None:
        return platforms

    for lang in container.findall("cwe:Language", NS):
        name = lang.get("Name", lang.get("Class", "Unknown"))
        platforms["languages"].append({
            "name": name,
            "prevalence": lang.get("Prevalence", ""),
        })

    for tech in container.findall("cwe:Technology", NS):
        name = tech.get("Name", tech.get("Class", "Unknown"))
        platforms["technologies"].append({
            "name": name,
            "prevalence": tech.get("Prevalence", ""),
        })

    return platforms


def _parse_consequences(weakness: ET.Element) -> list[dict]:
    """Parseia a seção Common_Consequences."""
    consequences = []
    container = weakness.find("cwe:Common_Consequences", NS)
    if container is None:
        return consequences

    for cons in container.findall("cwe:Consequence", NS):
        entry = {
            "scopes": [],
            "impacts": [],
            "note": "",
        }
        for scope in cons.findall("cwe:Scope", NS):
            if scope.text:
                entry["scopes"].append(scope.text.strip())
        for impact in cons.findall("cwe:Impact", NS):
            if impact.text:
                entry["impacts"].append(impact.text.strip())
        note = cons.find("cwe:Note", NS)
        if note is not None:
            entry["note"] = _text_content(note)
        consequences.append(entry)

    return consequences


def _parse_mitigations(weakness: ET.Element) -> list[dict]:
    """Parseia a seção Potential_Mitigations."""
    mitigations = []
    container = weakness.find("cwe:Potential_Mitigations", NS)
    if container is None:
        return mitigations

    for mit in container.findall("cwe:Mitigation", NS):
        entry = {
            "phase": [],
            "strategy": "",
            "description": "",
            "effectiveness": "",
        }

        for phase in mit.findall("cwe:Phase", NS):
            if phase.text:
                entry["phase"].append(phase.text.strip())

        strategy = mit.find("cwe:Strategy", NS)
        if strategy is not None and strategy.text:
            entry["strategy"] = strategy.text.strip()

        desc = mit.find("cwe:Description", NS)
        entry["description"] = _text_content(desc)

        eff = mit.find("cwe:Effectiveness", NS)
        if eff is not None and eff.text:
            entry["effectiveness"] = eff.text.strip()

        mitigations.append(entry)

    return mitigations


def _parse_examples(weakness: ET.Element) -> list[dict]:
    """Parseia a seção Demonstrative_Examples."""
    examples = []
    container = weakness.find("cwe:Demonstrative_Examples", NS)
    if container is None:
        return examples

    for ex in container.findall("cwe:Demonstrative_Example", NS):
        entry = {"blocks": []}

        for child in ex:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

            if tag == "Intro_Text":
                entry["blocks"].append({
                    "type": "intro",
                    "content": _text_content(child),
                })
            elif tag == "Body_Text":
                entry["blocks"].append({
                    "type": "body",
                    "content": _text_content(child),
                })
            elif tag == "Example_Code":
                nature = child.get("Nature", "unknown")
                entry["blocks"].append({
                    "type": "code",
                    "nature": nature.lower(),  # "bad", "good", "attack", etc.
                    "language": child.get("Language", ""),
                    "content": _text_content(child),
                })

        if entry["blocks"]:
            examples.append(entry)

    return examples


def _parse_detection_methods(weakness: ET.Element) -> list[dict]:
    """Parseia a seção Detection_Methods."""
    methods = []
    container = weakness.find("cwe:Detection_Methods", NS)
    if container is None:
        return methods

    for det in container.findall("cwe:Detection_Method", NS):
        entry = {
            "method": "",
            "description": "",
            "effectiveness": "",
        }

        method = det.find("cwe:Method", NS)
        if method is not None and method.text:
            entry["method"] = method.text.strip()

        desc = det.find("cwe:Description", NS)
        entry["description"] = _text_content(desc)

        eff = det.find("cwe:Effectiveness", NS)
        if eff is not None and eff.text:
            entry["effectiveness"] = eff.text.strip()

        methods.append(entry)

    return methods


def _parse_related_weaknesses(weakness: ET.Element) -> list[dict]:
    """Parseia a seção Related_Weaknesses."""
    related = []
    container = weakness.find("cwe:Related_Weaknesses", NS)
    if container is None:
        return related

    for rel in container.findall("cwe:Related_Weakness", NS):
        related.append({
            "nature": rel.get("Nature", ""),
            "cwe_id": rel.get("CWE_ID", ""),
            "view_id": rel.get("View_ID", ""),
        })

    return related


# ---------------------------------------------------------------------------
# Helper de extração de texto
# ---------------------------------------------------------------------------

def _text_content(element: ET.Element | None) -> str:
    """Extrai recursivamente todo o texto de um elemento, incluindo filhos xhtml.

    Campos de descrição do CWE embbutem tags xhtml (<p>, <code>, <b> etc.) misturadas
    com texto puro. Chamar apenas .text pegaria somente o trecho antes do primeiro filho.
    Esta função percorre a árvore inteira e concatena todos os fragmentos de texto.
    """
    if element is None:
        return ""
    parts = []
    if element.text:
        parts.append(element.text)
    for child in element:
        parts.append(_text_content(child))
        if child.tail:
            parts.append(child.tail)
    text = " ".join(parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Sanity check: parseia o XML padrão e mostra contagem + primeiro CWE.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    weaknesses = parse_cwe_xml(DEFAULT_RAW_DIR / "cwe_top25_2025.xml")
    print(f"{len(weaknesses)} CWEs parseados")
    if weaknesses:
        print(f"primeiro: {weaknesses[0]['cwe_id']} - {weaknesses[0]['name']}")
