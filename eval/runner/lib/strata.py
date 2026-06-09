#!/usr/bin/env python3
"""Classificador de estrato de cobertura do KB para os prompts SALLM.

Classifica cada CWE-alvo em um de três estratos com base na cobertura da
base de conhecimento c_know (View 1003 U Top 25, 133 CWEs):

    A — CWE diretamente no KB
    B — CWE tem um parente hierárquico a 1 salto no KB
        (ChildOf / PeerOf via grafo completo MITRE)
    C — CWE sem representação no KB nem parentes a 1 salto

Os estratos são pré-computados uma vez para alimentar o
``build_treated_dataset.py``.  O grafo completo de hierarquia é lido de
``cwec_latest.xml`` (baixado automaticamente para ``raw_data/`` se ausente);
o conjunto KB é extraído dos dois XMLs da KB (View 1003 e Top 25).

Valores esperados para os 100 prompts SALLM (45 CWEs distintos):
    A=75 prompts / B=20 prompts / C=5 prompts
    Grupo C = 1x CWE-176, 1x CWE-379, 3x CWE-730

Uso::

    python3 eval/runner/lib/strata.py

Espera-se ``A=75 B=20 C=5`` e a lista de ids do Grupo C.
"""

from __future__ import annotations

import json
import logging
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = REPO_ROOT / "eval" / "SALLM" / "Dataset" / "dataset.jsonl"
RAW_DATA_DIR = (
    REPO_ROOT / ".claude" / "skills" / "secure" / "knowledge_base" / "raw_data"
)
KB_XML_NAMES = ["nvd_mapping_1003.xml", "cwe_top25_2025.xml"]
FULL_XML_NAME = "cwec_latest.xml"
FULL_XML_URL = "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"

NS = {"cwe": "http://cwe.mitre.org/cwe-7"}

# Natures que definem parentesco hierárquico a 1 salto (sem CanPrecede, Requires, etc.)
HIERARCHY_NATURES = {"ChildOf", "PeerOf", "ParentOf"}

Stratum = Literal["A", "B", "C"]


# ---------------------------------------------------------------------------
# Download do catálogo completo (lazy, idempotente)
# ---------------------------------------------------------------------------

def _ensure_full_xml(raw_dir: Path = RAW_DATA_DIR) -> Path:
    """Garante que ``cwec_latest.xml`` está presente em ``raw_dir``.

    Faz o download (2 MB ZIP) somente se o arquivo ainda não existir.
    """
    target = raw_dir / FULL_XML_NAME
    if target.exists():
        logger.debug("Catálogo completo já presente: %s", target)
        return target

    logger.info("Baixando catálogo completo CWE de %s …", FULL_XML_URL)
    import io
    import zipfile

    import requests  # já usado pelo cwe_downloader.py da skill

    resp = requests.get(FULL_XML_URL, timeout=60)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        xml_names = [n for n in zf.namelist() if n.endswith(".xml")]
        if not xml_names:
            raise RuntimeError(f"Nenhum XML no ZIP de {FULL_XML_URL}")
        target.write_bytes(zf.read(xml_names[0]))

    logger.info("Catálogo salvo em %s", target)
    return target


# ---------------------------------------------------------------------------
# Construção dos conjuntos KB e do grafo de hierarquia
# ---------------------------------------------------------------------------

def _load_kb_set(raw_dir: Path = RAW_DATA_DIR) -> frozenset[int]:
    """Retorna o conjunto de IDs inteiros (sem prefixo CWE-) dos CWEs no KB.

    Usa os mesmos XMLs que o build_knowledge_base.py ingere (View 1003 + Top 25).
    """
    ids: set[int] = set()
    for fname in KB_XML_NAMES:
        path = raw_dir / fname
        tree = ET.parse(path)
        for w in tree.getroot().findall(".//cwe:Weakness", NS):
            ids.add(int(w.get("ID")))
    logger.debug("KB: %d CWEs diretos", len(ids))
    return frozenset(ids)


def _build_neighbor_map(full_xml: Path) -> dict[int, set[int]]:
    """Constrói mapa de vizinhos a 1 salto para cada CWE no catálogo completo.

    Para cada Weakness no XML:
      - Lê Related_Weaknesses com natures em HIERARCHY_NATURES (ChildOf/PeerOf).
      - Registra edge bidirecional: tanto X→Y quanto Y→X.
        (O XML só declara ChildOf/PeerOf a partir do filho/par; a relação
        inversa ParentOf é implícita e adicionada aqui para cobertura
        completa a 1 salto.)

    Args:
        full_xml: Caminho para cwec_latest.xml.

    Returns:
        Dict ``{cwe_id: {neighbor_id, …}}``.
    """
    tree = ET.parse(full_xml)
    neighbors: dict[int, set[int]] = {}

    for w in tree.getroot().findall(".//cwe:Weakness", NS):
        src = int(w.get("ID"))
        if src not in neighbors:
            neighbors[src] = set()

        rels = w.find("cwe:Related_Weaknesses", NS)
        if rels is None:
            continue
        for r in rels.findall("cwe:Related_Weakness", NS):
            if r.get("Nature") not in HIERARCHY_NATURES:
                continue
            tgt = int(r.get("CWE_ID"))
            neighbors[src].add(tgt)
            # relação inversa (ParentOf implícito)
            if tgt not in neighbors:
                neighbors[tgt] = set()
            neighbors[tgt].add(src)

    logger.debug("Grafo de hierarquia: %d nós", len(neighbors))
    return neighbors


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

class StratumClassifier:
    """Classifica CWEs em estratos A/B/C com base na cobertura do KB.

    Inicialização faz o download do cwec_latest.xml se necessário (idempotente).
    """

    def __init__(self, raw_dir: Path = RAW_DATA_DIR) -> None:
        self._kb = _load_kb_set(raw_dir)
        full_xml = _ensure_full_xml(raw_dir)
        self._neighbors = _build_neighbor_map(full_xml)

    @property
    def kb_size(self) -> int:
        return len(self._kb)

    def classify(self, cwe: str) -> Stratum:
        """Classifica um CWE canônico (ex.: ``'CWE-78'``) em A, B ou C.

        Args:
            cwe: Identificador canônico ``CWE-<n>``.

        Returns:
            ``'A'`` se direto no KB, ``'B'`` se 1-hop, ``'C'`` caso contrário.

        Raises:
            ValueError: Se o argumento não for ``CWE-<n>``.
        """
        if not cwe.upper().startswith("CWE-"):
            raise ValueError(f"CWE inválido: {cwe!r}; esperado 'CWE-<n>'")
        cid = int(cwe.split("-", 1)[1])

        if cid in self._kb:
            return "A"

        for neighbor in self._neighbors.get(cid, set()):
            if neighbor in self._kb:
                return "B"

        return "C"


# Instância global lazy (criada na primeira chamada a classify_cwe)
_classifier: StratumClassifier | None = None


def classify_cwe(cwe: str) -> Stratum:
    """Classifica um CWE usando o classificador global (singleton).

    Inicializa o classificador na primeira chamada.

    Args:
        cwe: Identificador canônico ``CWE-<n>``.

    Returns:
        ``'A'``, ``'B'`` ou ``'C'``.
    """
    global _classifier
    if _classifier is None:
        _classifier = StratumClassifier()
    return _classifier.classify(cwe)


# ---------------------------------------------------------------------------
# CLI / sanity check
# ---------------------------------------------------------------------------

def _main() -> None:
    """Sanity check: classifica todos os 100 prompts SALLM e reporta A/B/C."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    classifier = StratumClassifier()
    logger.info("KB: %d CWEs diretos", classifier.kb_size)

    rows: list[dict] = []
    with DATASET_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    counts: dict[Stratum, int] = {"A": 0, "B": 0, "C": 0}
    group_c: list[str] = []

    for row in rows:
        # parse_target_cwe já testado em T1; reimplementamos inline para evitar
        # dependência circular (ambos são em lib/ sem __init__)
        import re
        m = re.search(r"cwe[_-]?(\d+)", row["id"], re.IGNORECASE)
        if not m:
            logger.error("id sem CWE: %s", row["id"])
            sys.exit(1)
        cwe = f"CWE-{int(m.group(1))}"
        stratum = classifier.classify(cwe)
        counts[stratum] += 1
        if stratum == "C":
            group_c.append(row["id"])

    print(f"A={counts['A']} B={counts['B']} C={counts['C']}")
    if group_c:
        print("Grupo C:")
        for pid in sorted(group_c):
            print(f"  {pid}")

    # Verificação das contagens esperadas
    expected = {"A": 75, "B": 20, "C": 5}
    ok = True
    for s, exp in expected.items():
        if counts[s] != exp:
            logger.error("FALHA: esperado %s=%d, obtido %d", s, exp, counts[s])
            ok = False

    expected_c_cwes = {"CWE-176", "CWE-379", "CWE-730"}
    _cwe_re2 = re.compile(r"cwe[_-]?(\d+)", re.IGNORECASE)
    actual_c_cwes = {
        f"CWE-{int(_cwe_re2.search(pid).group(1))}"
        for pid in group_c
    }
    if actual_c_cwes != expected_c_cwes:
        logger.error("FALHA Grupo C: esperado %s, obtido %s", expected_c_cwes, actual_c_cwes)
        ok = False

    if ok:
        print("OK — contagens e Grupo C conferem.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    _main()
