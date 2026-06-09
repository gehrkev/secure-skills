#!/usr/bin/env python3
"""Helper compartilhado para chamadas headless ao Claude Code.

Encapsula a invocação validada de ``claude -p`` no caminho OAuth/assinatura
desta máquina (ver ``eval/runner/verify1/verify1_smoke.sh``). Reutilizado por
T3 (autoria) e T4 (auditoria) — UM único módulo, sem duplicação.

Fatos da recipe que este módulo honra (NÃO reinventar):
- Auth Pro/OAuth: **sem** ``--bare`` e **sem** ``ANTHROPIC_API_KEY``.
- Modelo fixo ``claude-haiku-4-5-20251001``.
- ``--mcp-config`` deve ser ``'{"mcpServers":{}}'`` (não ``'{}'``).
- ``--allowedTools`` é variádico e engole o positional final -> o prompt vai
  PRIMEIRO (logo após ``-p``) e ``--allowedTools`` por ÚLTIMO.
- ``--output-format json``: o texto fica em ``result.result``; o id de modelo
  fixado fica em ``result.modelUsage`` (o ``model`` de topo é ``null``).
- Cada chamada roda em um cwd scratch novo (sem CLAUDE.md) para isolamento.

Uso::

    from eval.runner.lib import cc
    texto = cc.complete("Diga olá em uma palavra.")
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
import time

logger = logging.getLogger(__name__)

MODEL = "claude-haiku-4-5-20251001"
EMPTY_MCP_CONFIG = '{"mcpServers":{}}'


class ClaudeError(RuntimeError):
    """Erro ao invocar ou interpretar a resposta do ``claude -p``."""


def complete(
    prompt: str,
    system_prompt: str | None = None,
    allowed_tools: str = "",
    *,
    model: str = MODEL,
    max_turns: int = 1,
    timeout: int = 180,
    retries: int = 3,
) -> str:
    """Roda uma chamada headless ``claude -p`` e devolve o texto da resposta.

    Para geração só-texto (autoria/auditoria), nenhuma ferramenta é
    necessária, então ``allowed_tools`` é vazio por padrão.

    Args:
        prompt: O prompt do usuário (passado PRIMEIRO, logo após ``-p``).
        system_prompt: Prompt de sistema opcional (anexado via
            ``--append-system-prompt``). ``None`` omite a flag.
        allowed_tools: Valor variádico de ``--allowedTools`` (ex.: ``""`` ou
            ``"Bash Read"``). Passado por ÚLTIMO.
        model: Id do modelo a fixar (padrão: Haiku da recipe).
        max_turns: Limite de turnos do agente.
        timeout: Timeout em segundos para o subprocesso.
        retries: Tentativas totais com backoff exponencial (5s, 10s, …, cap
            60s) para falhas transitórias. Não recupera limite de janela 5h.

    Returns:
        O texto de ``result.result`` (com ``strip`` aplicado).

    Raises:
        ClaudeError: Em auth via API key, falha do subprocesso, JSON
            inesperado, ou ``subtype`` diferente de ``success``.
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        raise ClaudeError(
            "ANTHROPIC_API_KEY definido; as chamadas M3 rodam só em OAuth."
        )

    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        model,
        "--disable-slash-commands",
        "--no-session-persistence",
        "--strict-mcp-config",
        "--mcp-config",
        EMPTY_MCP_CONFIG,
        "--setting-sources",
        "",
        "--output-format",
        "json",
        "--max-turns",
        str(max_turns),
    ]
    if system_prompt is not None:
        cmd += ["--append-system-prompt", system_prompt]
    # allowedTools por último: é variádico e engoliria o positional do prompt.
    cmd += ["--allowedTools", allowed_tools]

    # cwd scratch novo, sem CLAUDE.md, para isolamento entre chamadas.
    # Retry com backoff exponencial para falhas transitórias (overload,
    # blips de rede). NÃO recupera de um limite de janela de 5h esgotado —
    # nesse caso as tentativas se esgotam e a exceção sobe, e o chamador
    # (run_paraphrase) para de forma graciosa com o progresso já checkpointado.
    last_err: ClaudeError | None = None
    for attempt in range(1, retries + 1):
        try:
            return _run_once(cmd, timeout)
        except ClaudeError as exc:
            last_err = exc
            if attempt < retries:
                wait = min(5 * 2 ** (attempt - 1), 60)
                logger.warning(
                    "claude -p falhou (tentativa %d/%d): %s — retry em %ds",
                    attempt,
                    retries,
                    exc,
                    wait,
                )
                time.sleep(wait)
    assert last_err is not None
    raise last_err


def _run_once(cmd: list[str], timeout: int) -> str:
    """Uma única tentativa de ``claude -p``: roda, parseia e devolve o texto.

    Args:
        cmd: Comando já montado.
        timeout: Timeout do subprocesso em segundos.

    Returns:
        Texto de ``result.result`` (com ``strip`` aplicado).

    Raises:
        ClaudeError: timeout, ``returncode != 0``, JSON inesperado,
            ``subtype`` diferente de ``success``, ou campo ``result`` ausente.
    """
    with tempfile.TemporaryDirectory() as scratch:
        try:
            proc = subprocess.run(
                cmd,
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise ClaudeError(f"timeout após {timeout}s") from exc

    if proc.returncode != 0:
        raise ClaudeError(
            f"claude -p saiu com código {proc.returncode}: {proc.stderr.strip()}"
        )

    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ClaudeError(
            f"saída não-JSON do claude -p: {proc.stdout[:300]!r}"
        ) from exc

    subtype = result.get("subtype")
    if subtype and subtype != "success":
        raise ClaudeError(f"sessão não bem-sucedida (subtype={subtype})")

    text = result.get("result")
    if not isinstance(text, str):
        raise ClaudeError(f"campo 'result' ausente ou inesperado: {result!r}")

    logger.info(
        "claude -p ok (model_usage=%s)",
        list((result.get("modelUsage") or {}).keys()) or "n/a",
    )
    return text.strip()


def _main() -> None:
    """Sanity check: faz uma chamada só-texto trivial e imprime a resposta."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prompt",
        default="Responda apenas com a palavra: ok",
        help="prompt de teste",
    )
    args = parser.parse_args()
    print(complete(args.prompt))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    _main()
