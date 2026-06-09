"""
Downloader de Dados CWE

Baixa dados xml do CWE das fontes oficiais da MITRE:
- Base completa do CWE (cwec_latest.xml.zip)
- CWE Top 25 (2025) — view 1435
- OWASP Top Ten RC1 (2025) — view 1450

Função principal: download_and_extract(key, output_dir) -> Path
"""

import io
import logging
import zipfile
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://cwe.mitre.org/data/xml"

DOWNLOADS = {
    "cwec_latest": {
        "url": f"{BASE_URL}/cwec_latest.xml.zip",
        "description": "Full CWE database",
    },
    "cwe_top25_2025": {
        "url": f"{BASE_URL}/views/1435.xml.zip",
        "description": "CWE Top 25 (2025)",
    },
    "nvd_mapping_1003": {
        "url": f"{BASE_URL}/views/1003.xml.zip",
        "description": "View 1003 — NVD CVE-mapping weaknesses (130 CWEs)",
    },
    "owasp_top10_2025": {
        "url": f"{BASE_URL}/views/1450.xml.zip",
        "description": "OWASP Top Ten RC1 (2025) CWE mapping",
    },
}

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw_data"


def download_and_extract(key: str, output_dir: Path) -> Path:
    """Baixa um zip do CWE e extrai o xml para output_dir.

    Retorna o caminho para o arquivo extraído.
    """
    entry = DOWNLOADS[key]
    url = entry["url"]
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Baixando %s de %s", entry["description"], url)
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        xml_names = [n for n in zf.namelist() if n.endswith(".xml")]
        if not xml_names:
            raise ValueError(f"Nenhum arquivo XML encontrado em {url}")

        xml_name = xml_names[0]
        extracted_path = output_dir / f"{key}.xml"
        extracted_path.write_bytes(zf.read(xml_name))
        logger.info("Extraído %s -> %s", xml_name, extracted_path)

    return extracted_path


if __name__ == "__main__":
    # Sanity check: baixa o CWE Top 25 no diretório padrão.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    path = download_and_extract("cwe_top25_2025", DEFAULT_OUTPUT_DIR)
    print(f"baixado: {path}")
