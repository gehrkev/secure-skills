"""
Vector Store - Wrapper ChromaDB

Fornece uma interface para ingestão de conhecimento de segurança
em chunks e consulta via busca por similaridade semântica.

Uso:
    store = SecurityKnowledgeStore(persist_dir="path/to/chroma_db")
    store.add_documents(chunks)
    results = store.query("SQL injection prevention", top_k=5)
"""

import logging
from pathlib import Path

import chromadb

logger = logging.getLogger(__name__)

DEFAULT_PERSIST_DIR = Path(__file__).resolve().parent / "chroma_db"
COLLECTION_NAME = "cwe_security_knowledge"


class SecurityKnowledgeStore:
    """Vector store com ChromaDB para conhecimento de segurança CWE/OWASP."""

    def __init__(self, persist_dir: Path | str | None = None):
        self.persist_dir = Path(persist_dir or DEFAULT_PERSIST_DIR)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "CWE/OWASP security knowledge for RAG retrieval"},
        )
        logger.info(
            "Store inicializado em %s (coleção: %s, %d documentos)",
            self.persist_dir,
            COLLECTION_NAME,
            self.collection.count(),
        )

    def add_documents(self, chunks: list[dict], batch_size: int = 200) -> int:
        """Ingere chunks de documentos no vector store.

        Args:
            chunks: Lista de dicts com chaves 'id', 'content' e 'metadata'.
            batch_size: Número de documentos por batch de upsert.

        Returns:
            Número de documentos adicionados.
        """
        total = len(chunks)
        added = 0

        for i in range(0, total, batch_size):
            batch = chunks[i : i + batch_size]

            ids = [c["id"] for c in batch]
            documents = [c["content"] for c in batch]

            # Valores de metadata no ChromaDB devem ser str, int, float ou bool
            metadatas = []
            for c in batch:
                meta = {}
                for k, v in c["metadata"].items():
                    if isinstance(v, (str, int, float, bool)):
                        meta[k] = v
                    elif isinstance(v, list):
                        meta[k] = ", ".join(str(x) for x in v)
                    else:
                        meta[k] = str(v)
                metadatas.append(meta)

            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )
            added += len(batch)
            logger.info("Ingeridos %d/%d documentos", added, total)

        return added

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        where: dict | None = None,
        where_document: dict | None = None,
    ) -> list[dict]:
        """Consulta o vector store por conhecimento de segurança relevante.

        Args:
            query_text: A query de busca (ex: prompt do usuário ou descrição de CWE).
            top_k: Número de resultados a retornar.
            where: Filtro de metadata (ex: {"cwe_id": "CWE-89"}).
            where_document: Filtro no conteúdo do documento.

        Returns:
            Lista de dicts com 'id', 'content', 'metadata', 'distance'.
        """
        kwargs = {
            "query_texts": [query_text],
            "n_results": min(top_k, self.collection.count() or top_k),
        }
        if where:
            kwargs["where"] = where
        if where_document:
            kwargs["where_document"] = where_document

        if self.collection.count() == 0:
            logger.warning("Coleção vazia, retornando sem resultados")
            return []

        results = self.collection.query(**kwargs)

        documents = []
        for i in range(len(results["ids"][0])):
            documents.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return documents

    def query_by_cwe(self, cwe_id: str, chunk_type: str | None = None, top_k: int = 10) -> list[dict]:
        """Recupera todos os chunks de um CWE específico.

        Args:
            cwe_id: ex. "CWE-89"
            chunk_type: Filtro opcional (ex: "mitigation", "example_insecure")
            top_k: Máximo de resultados.
        """
        where = {"cwe_id": cwe_id}
        if chunk_type:
            where = {"$and": [{"cwe_id": cwe_id}, {"chunk_type": chunk_type}]}

        # Usa query genérica pois o filtro principal é por metadata
        return self.query(f"{cwe_id} security vulnerability", top_k=top_k, where=where)

    def get_collection_stats(self) -> dict:
        """Retorna estatísticas resumidas da coleção."""
        count = self.collection.count()
        if count == 0:
            return {"total_documents": 0}

        # Lê todos os metadados para extrair valores únicos
        sample = self.collection.get(limit=count, include=["metadatas"])
        metadatas = sample["metadatas"]

        cwe_ids = set()
        chunk_types = set()
        for m in metadatas:
            if "cwe_id" in m:
                cwe_ids.add(m["cwe_id"])
            if "chunk_type" in m:
                chunk_types.add(m["chunk_type"])

        return {
            "total_documents": count,
            "unique_cwes": len(cwe_ids),
            "cwe_ids": sorted(cwe_ids),
            "chunk_types": sorted(chunk_types),
        }

    def reset(self):
        """Deleta e recria a coleção."""
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "CWE/OWASP security knowledge for RAG retrieval"},
        )
        logger.info("Coleção resetada")


if __name__ == "__main__":
    # Sanity check: abre o store padrão e mostra contagem de documentos.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    store = SecurityKnowledgeStore()
    print(f"{store.collection.count()} documentos em {store.persist_dir}")
