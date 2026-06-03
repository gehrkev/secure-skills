"""
c_know - Componente de Conhecimento Externo de Segurança

Camada de recuperação que recebe um prompt de tarefa de codificação, identifica
vulnerabilidades de segurança relevantes via busca semântica e formata o
conhecimento para injeção no contexto do LLM.

O desenvolvedor escreve um prompt normal de codificação. O c_know identifica o
que pode dar errado (em termos de segurança) e fornece ao LLM o conhecimento
necessário para evitar esses erros.

Exemplo:
    prompt = "write a function that takes an username and looks up their profile in the database"
    knowledge = c_know.retrieve_for_prompt(prompt)
    # -> Retorna conhecimento sobre SQL Injection (CWE-89):
    #    mitigações, exemplos de código seguro, anti-padrões a evitar

Uso:
    c_know = SecurityKnowledge()
    context = c_know.retrieve_for_prompt(user_prompt, top_k=5)
"""

import logging
from pathlib import Path

from knowledge_base.store.vector_store import SecurityKnowledgeStore

logger = logging.getLogger(__name__)


class SecurityKnowledge:
    """Recupera e formata conhecimento de segurança relevante para uma tarefa de codificação."""

    def __init__(self, store: SecurityKnowledgeStore | None = None):
        self.store = store or SecurityKnowledgeStore()

    def retrieve_for_prompt(
        self,
        prompt: str,
        top_k: int = 5,
        include_types: list[str] | None = None,
        max_chars: int = 6000,
    ) -> str:
        """Dado um prompt de tarefa de codificação, recupera conhecimento de segurança relevante.

        Args:
            prompt: Descrição da tarefa de codificação do usuário.
            top_k: Número de chunks a recuperar do vector store.
            include_types: Filtro para tipos específicos de chunk (ex: ["mitigation",
                "example_secure"]). Se None, recupera todos os tipos.
            max_chars: Máximo de caracteres no output formatado.
                Trunca os chunks menos relevantes para respeitar o limite.

        Returns:
            String formatada pronta para injeção no contexto do LLM.
        """
        where = None
        if include_types:
            if len(include_types) == 1:
                where = {"chunk_type": include_types[0]}
            else:
                where = {"chunk_type": {"$in": include_types}}

        results = self.store.query(prompt, top_k=top_k, where=where)

        if not results:
            logger.info("Nenhum conhecimento de segurança encontrado para o prompt")
            return ""

        return self._format_results(results, max_chars)

    def retrieve_raw(
        self,
        prompt: str,
        top_k: int = 5,
        include_types: list[str] | None = None,
    ) -> list[dict]:
        """Recupera resultados brutos (para c_mem ou assembly processarem).

        Retorna lista de dicts com 'id', 'content', 'metadata', 'distance'.
        """
        where = None
        if include_types:
            if len(include_types) == 1:
                where = {"chunk_type": include_types[0]}
            else:
                where = {"chunk_type": {"$in": include_types}}

        return self.store.query(prompt, top_k=top_k, where=where)

    def _format_results(self, results: list[dict], max_chars: int) -> str:
        """Formata os chunks recuperados em contexto estruturado para o LLM.

        Agrupa por CWE e ordena: overview -> mitigações -> exemplos seguros
        -> exemplos inseguros (anti-padrões).
        """
        # Agrupa chunks por CWE
        by_cwe: dict[str, list[dict]] = {}
        for r in results:
            cwe_id = r["metadata"].get("cwe_id", "unknown")
            by_cwe.setdefault(cwe_id, []).append(r)

        # Ordenação por tipo: mais acionável primeiro
        type_order = {
            "overview": 0,
            "mitigation": 1,
            "example_secure": 2,
            "example_insecure": 3,
            "consequences": 4,
            "detection": 5,
            "example_attack": 6,
            "example": 7,
            "relationships": 8,
        }

        sections = []
        total_chars = 0

        for cwe_id, chunks in by_cwe.items():
            # Ordena chunks por prioridade de tipo, depois por relevância (distância)
            chunks.sort(key=lambda c: (
                type_order.get(c["metadata"].get("chunk_type", ""), 99),
                c["distance"],
            ))

            cwe_name = chunks[0]["metadata"].get("cwe_name", "")
            section_header = f"### {cwe_id}: {cwe_name}"
            section_parts = [section_header]

            for chunk in chunks:
                chunk_type = chunk["metadata"].get("chunk_type", "")
                content = chunk["content"]

                # Remove a linha de cabeçalho do CWE no conteúdo (já temos section_header)
                lines = content.split("\n")
                if lines and lines[0].startswith("CWE-"):
                    content = "\n".join(lines[1:]).strip()

                entry = f"\n**[{chunk_type}]**\n{content}"

                if total_chars + len(entry) > max_chars:
                    break
                section_parts.append(entry)
                total_chars += len(entry)

            sections.append("\n".join(section_parts))

            if total_chars >= max_chars:
                break

        header = (
            "## Security Knowledge (retrieved by c_know)\n"
            "The following security patterns are relevant to this coding task. "
            "Use this knowledge to write secure code that avoids these vulnerabilities.\n"
        )

        return header + "\n\n".join(sections)


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="c_know — Recuperação de Conhecimento de Segurança")
    parser.add_argument("prompt", type=str, help="Prompt de tarefa de codificação")
    parser.add_argument("--top-k", type=int, default=5, help="Número de chunks a recuperar")
    parser.add_argument(
        "--types",
        nargs="+",
        choices=[
            "overview", "mitigation", "example_secure", "example_insecure",
            "consequences", "detection", "example_attack", "example", "relationships",
        ],
        help="Filtrar por tipos de chunk",
    )
    parser.add_argument("--max-chars", type=int, default=6000)
    args = parser.parse_args()

    c_know = SecurityKnowledge()
    result = c_know.retrieve_for_prompt(
        args.prompt,
        top_k=args.top_k,
        include_types=args.types,
        max_chars=args.max_chars,
    )
    print(result)
