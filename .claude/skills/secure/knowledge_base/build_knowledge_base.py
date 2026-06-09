"""
Construtor da Base de Conhecimento - Orquestrador

Executa o pipeline completo: download do XML CWE -> parse -> chunking -> ingestão no ChromaDB.

Uso:
    conda run -n securecontext python -m knowledge_base.build_knowledge_base [OPTIONS]

Opções:
    --source    Fonte a ingerir: "top25", "nvd_mapping", "owasp", "full",
                "m3" (= top25 ∪ nvd_mapping, o KB usado pela avaliação M3)
                ou "all" (padrão: m3)
    --reset     Limpa a coleção existente antes de ingerir
    --skip-download  Pula o download (usa arquivos XML existentes em raw_data)
"""

import logging
import time
from pathlib import Path

from knowledge_base.pipelines.cwe_downloader import download_and_extract, DEFAULT_OUTPUT_DIR
from knowledge_base.pipelines.cwe_parser import parse_cwe_xml
from knowledge_base.pipelines.chunker import chunk_all
from knowledge_base.store.vector_store import SecurityKnowledgeStore

logger = logging.getLogger(__name__)

SOURCE_MAP = {
    "top25": "cwe_top25_2025",
    "nvd_mapping": "nvd_mapping_1003",
    "owasp": "owasp_top10_2025",
    "full": "cwec_latest",
}

# Meta-fontes: combinam várias views; chunks duplicados são deduplicados
# pelo upsert do ChromaDB (ids determinísticos por chunk).
META_SOURCES = {
    # KB usado pela avaliação M3.
    # 133 CWEs (130 do View 1003 + 3 exclusivos do Top 25:
    # CWE-121, CWE-122, CWE-284). ~2250 chunks.
    "m3": ["nvd_mapping", "top25"],
}


def build(
    sources: list[str],
    reset: bool = False,
    skip_download: bool = False,
) -> dict:
    """Executa o pipeline completo para as fontes indicadas.

    Retorna dict com estatísticas do que foi ingerido.
    """
    store = SecurityKnowledgeStore()

    if reset:
        logger.info("Resetando coleção")
        store.reset()

    total_chunks = 0
    total_weaknesses = 0

    for source in sources:
        download_key = SOURCE_MAP[source]
        xml_path = DEFAULT_OUTPUT_DIR / f"{download_key}.xml"

        # Etapa 1: Download
        if not skip_download or not xml_path.exists():
            logger.info("Etapa 1: Baixando %s", source)
            xml_path = download_and_extract(download_key, DEFAULT_OUTPUT_DIR)
        else:
            logger.info("Etapa 1: Pulando download, usando %s", xml_path)

        # Etapa 2: Parse
        logger.info("Etapa 2: Parseando XML")
        weaknesses = parse_cwe_xml(xml_path)
        total_weaknesses += len(weaknesses)

        # Etapa 3: Chunking
        logger.info("Etapa 3: Gerando chunks")
        chunks = chunk_all(weaknesses)
        total_chunks += len(chunks)

        # Etapa 4: Ingestão
        logger.info("Etapa 4: Ingerindo no ChromaDB")
        store.add_documents(chunks)

    stats = store.get_collection_stats()
    return {
        "sources": sources,
        "weaknesses_parsed": total_weaknesses,
        "chunks_generated": total_chunks,
        "collection_total": stats["total_documents"],
        "unique_cwes": stats["unique_cwes"],
        "chunk_types": stats["chunk_types"],
    }


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Constrói a base de conhecimento de segurança")
    parser.add_argument(
        "--source",
        choices=["top25", "nvd_mapping", "owasp", "full", "m3", "all"],
        default="m3",
        help="Fonte de dados a ingerir (padrão: m3 = top25 ∪ nvd_mapping).",
    )
    parser.add_argument("--reset", action="store_true", help="Limpa a coleção antes de ingerir")
    parser.add_argument("--skip-download", action="store_true", help="Usa arquivos XML existentes")
    args = parser.parse_args()

    if args.source == "all":
        sources = ["top25", "owasp", "full"]
    elif args.source in META_SOURCES:
        sources = META_SOURCES[args.source]
    else:
        sources = [args.source]

    start = time.time()
    result = build(sources, reset=args.reset, skip_download=args.skip_download)
    elapsed = time.time() - start

    print(f"\nBase de conhecimento construída em {elapsed:.1f}s")
    print(f"  Fontes: {', '.join(result['sources'])}")
    print(f"  Vulnerabilidades parseadas: {result['weaknesses_parsed']}")
    print(f"  Chunks gerados: {result['chunks_generated']}")
    print(f"  Total na coleção: {result['collection_total']}")
    print(f"  CWEs distintos: {result['unique_cwes']}")
    print(f"  Tipos de chunk: {', '.join(result['chunk_types'])}")
