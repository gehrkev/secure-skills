#!/usr/bin/env python3
"""Asserções do gate VERIFY-1 sobre os traces stream-json capturados.

Consome os traces de sessão produzidos por verify1_smoke.sh e verifica os
quatro critérios de aceitação de design:

  (a) Isolamento : a sessão de sonda responde A FRIO (sem vazamento de
                   projeto/tese/conversa anterior).
  (b) Treatment  : um tool_use Bash invocando assemble.py + um candidate.py
                   parseável.
  (c) R2a + R4   : o argv de assemble.py --prompt é byte-igual ao <TASK>
                   templatizado, e NENHUM braço tem chamada codeql/codeql-eval
                   no trace.
  (d) Model/ok   : o result final de cada sessão reporta o model id fixado e
                   subtype == "success".

Código de saída 0 sse todos os gates passam.

Uso:
    verify1_assert.py --out-dir <dir> --task-file <file> --model <id>
"""

import argparse
import ast
import json
import re
import sys
import unicodedata
from pathlib import Path

LEAK_TERMS = [
    "securecontext",
    "secure context",
    "thesis",
    "tcc",
    "c_know",
    "codeql",
    "claude.md",
    "state.md",
    "memory.md",
    "udesc",
    "knowledge base",
    "knowledge_base",
    "sallm",
    "cwe",
    "prior conversation",
    "earlier conversation",
    "we discussed",
    "we talked",
    "as we",
]


def load_events(path: Path) -> list[dict]:
    """Parseia um arquivo stream-json (um objeto JSON por linha)."""
    events = []
    if not path.exists():
        return events
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            # tolera qualquer linha espúria não-JSON
            continue
    return events


def final_result(events: list[dict]) -> dict | None:
    for ev in reversed(events):
        if ev.get("type") == "result":
            return ev
    return None


def iter_tool_uses(events: list[dict]):
    """Gera (name, input_dict) para cada bloco de conteúdo tool_use."""
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name", ""), block.get("input", {}) or {}


def assistant_text(events: list[dict]) -> str:
    """Concatena todos os blocos de texto do assistant (para o scan de sonda a frio)."""
    chunks = []
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict):
            continue
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content")
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    # também a string `result` do objeto de resultado final, se houver
    fr = final_result(events)
    if fr and isinstance(fr.get("result"), str):
        chunks.append(fr["result"])
    return "\n".join(chunks)


def _tool_result_errors(events: list[dict]) -> dict[str, bool | None]:
    """Mapeia ``tool_use_id -> is_error`` a partir dos blocos ``tool_result``."""
    errs: dict[str, bool | None] = {}
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                tid = block.get("tool_use_id")
                if tid is not None:
                    errs[tid] = block.get("is_error")
    return errs


def extract_assemble_prompt_argv(events: list[dict]) -> str | None:
    """Extrai o argv ``--prompt`` da invocação de ``assemble.py`` **bem-sucedida**.

    O modelo às vezes faz uma primeira tentativa que **falha no shell** (ex.:
    aspas não-balanceadas ao colar um stub multilinha com ``"`` internos ->
    ``unmatched "``) e em seguida **re-tenta com escaping correto**, que
    sucede e de fato entrega o stub a ``assemble.py``. Uma tentativa falha não
    passou nada ao skill, então a verificação R2a deve olhar a chamada que
    *sucedeu*. Estratégia: entre todas as chamadas Bash a ``assemble.py``,
    preferir a **última com ``is_error`` ausente/``False``**; se nenhuma
    sucedeu, cair para a última chamada (preserva ``r2a_byte_exact`` descritivo).
    """
    errs = _tool_result_errors(events)
    calls: list[tuple[str | None, str]] = []  # (tool_use_id, command)
    for ev in events:
        msg = ev.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if (
                isinstance(block, dict)
                and block.get("type") == "tool_use"
                and block.get("name") == "Bash"
            ):
                cmd = (block.get("input", {}) or {}).get("command", "")
                if "assemble.py" in cmd:
                    calls.append((block.get("id"), cmd))

    if not calls:
        return None

    # Preferir a última chamada bem-sucedida (is_error é None ou False).
    for tid, cmd in reversed(calls):
        if errs.get(tid) is not True:
            return parse_prompt_arg(cmd)
    # Nenhuma sucedeu — usar a última (mantém o byte_exact descritivo).
    return parse_prompt_arg(calls[-1][1])


def _bash_dq_unescape(s: str, *, full: bool) -> str:
    """Desfaz o escaping de barra-invertida de aspas-duplas do bash.

    Dentro de aspas duplas o bash remove a barra antes de ``$ ` " \\`` (e
    newline) — em particular, o modelo escapa crases (`` \\` ``) para evitar
    *command substitution*, e o bash as remove antes de passar o argv, então
    ``assemble.py`` recebe os bytes originais. O ``shlex`` do Python, porém, só
    desfaz ``\\"`` e ``\\\\``, deixando ``\\`` e ``\\$`` — divergindo do que o
    bash de fato entregou. Esta função reconstrói o argv real.

    Args:
        s: String a normalizar.
        full: Se ``True`` (caminho do regex fallback, conteúdo bruto entre
            aspas), também desfaz ``\\"`` e ``\\\\``; se ``False`` (token já
            processado pelo shlex), desfaz só ``\\`` ` `` e ``\\$``.

    Returns:
        A string com o escaping de aspas-duplas do bash desfeito.
    """
    if s is None:
        return s
    chars = "`$\"\\\\" if full else "`$"
    return re.sub(r"\\([" + chars + r"])", r"\1", s)


def normalize_r2a(s: str | None) -> str | None:
    """Normalização *security-neutral* para a comparação R2a (deviation Tipo 2).

    Remove SOMENTE pontuação de formatação — crases de code-span markdown e
    aspas retas delimitadoras — além de NFC e colapso de espaços. **Não** remove
    palavras/tokens, logo não pode mascarar injeção de vocabulário de segurança
    (ex.: "sanitize", "securely"): diferenças em nível de palavra continuam
    reprovando R2a. Aplicada simetricamente aos dois lados da comparação.

    Args:
        s: Task ou argv extraído (``None`` retorna ``None``).

    Returns:
        Forma normalizada, ou ``None``.
    """
    if s is None:
        return None
    s = unicodedata.normalize("NFC", s)
    s = s.replace("`", "").replace("'", "").replace('"', "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


_ANSI_C_SIMPLE = {
    "a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f",
    "n": "\n", "r": "\r", "t": "\t", "v": "\v", "\\": "\\",
    "'": "'", '"': '"', "?": "?",
}


def _ansi_c_decode(s: str) -> str:
    """Decodifica uma string ANSI-C do bash (conteúdo de ``$'...'``).

    O bash usa ``$'...'`` (ANSI-C quoting) para passar strings multilinha:
    ``\\n`` vira newline real, ``\\'`` vira ``'`` etc., antes de entregar o
    argv ao programa. ``shlex`` do Python não entende ``$'...'`` (trata ``$``
    como literal e as aspas simples como quoting cru), então o argv extraído
    diverge do que ``assemble.py`` recebeu. Esta função reconstrói o valor real.
    """
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\" and i + 1 < n:
            nxt = s[i + 1]
            if nxt in _ANSI_C_SIMPLE:
                out.append(_ANSI_C_SIMPLE[nxt])
                i += 2
                continue
            if nxt == "x":  # \xHH
                hx = re.match(r"[0-9A-Fa-f]{1,2}", s[i + 2 : i + 4])
                if hx:
                    out.append(chr(int(hx.group(), 16)))
                    i += 2 + len(hx.group())
                    continue
            if nxt in "01234567":  # \nnn octal
                oc = re.match(r"[0-7]{1,3}", s[i + 1 : i + 4])
                out.append(chr(int(oc.group(), 8)))
                i += 1 + len(oc.group())
                continue
            # escape desconhecido — preserva a barra
            out.append(c)
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _extract_ansi_c_prompt(cmd: str) -> str | None:
    """Extrai ``--prompt $'...'`` (ANSI-C), respeitando ``\\'`` interno."""
    m = re.search(r"--prompt(?:=|\s+)\$'", cmd)
    if not m:
        return None
    i, n = m.end(), len(cmd)
    buf: list[str] = []
    while i < n:
        ch = cmd[i]
        if ch == "\\" and i + 1 < n:  # mantém o par de escape intacto
            buf.append(cmd[i : i + 2])
            i += 2
            continue
        if ch == "'":  # aspas simples não-escapada fecha o $'...'
            return _ansi_c_decode("".join(buf))
        buf.append(ch)
        i += 1
    return _ansi_c_decode("".join(buf))  # sem fechamento — decodifica o que há


def parse_prompt_arg(cmd: str) -> str | None:
    """Extrai o valor de --prompt "..." de uma string de comando shell.

    Trata o quoting ANSI-C do bash (``$'...'``), um argumento entre aspas duplas
    com possíveis aspas/newlines escapados internamente, e um fallback por regex.
    O valor retornado é igual ao que ``assemble.py`` de fato recebeu como argv
    (com unescape de aspas-duplas do bash ou decodificação ANSI-C, conforme o caso).
    """
    import shlex

    # ANSI-C $'...' primeiro — shlex o mal-interpreta.
    ansi = _extract_ansi_c_prompt(cmd)
    if ansi is not None:
        return ansi

    try:
        tokens = shlex.split(cmd)
        for i, tok in enumerate(tokens):
            if tok == "--prompt" and i + 1 < len(tokens):
                return _bash_dq_unescape(tokens[i + 1], full=False)
            if tok.startswith("--prompt="):
                return _bash_dq_unescape(tok[len("--prompt="):], full=False)
    except ValueError:
        pass
    # fallback por regex: --prompt "<...>" (greedy até a última aspa do segmento)
    m = re.search(r'--prompt\s+"(.*)"', cmd, re.DOTALL)
    if m:
        return _bash_dq_unescape(m.group(1), full=True)
    return None


def has_codeql_call(events: list[dict]) -> tuple[bool, str]:
    for name, inp in iter_tool_uses(events):
        blob = (name + " " + json.dumps(inp)).lower()
        if "codeql" in blob:
            return True, blob[:200]
    return False, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--task-file", required=True)
    ap.add_argument("--model", required=True)
    args = ap.parse_args()

    out = Path(args.out_dir)
    task = Path(args.task_file).read_text()
    model = args.model

    probe = load_events(out / "probe.session.jsonl")
    treat = load_events(out / "treatment.session.jsonl")
    ctrl = load_events(out / "control.session.jsonl")

    results: dict[str, tuple[bool, str]] = {}

    # ---- (a) Isolamento -----------------------------------------------------
    probe_text = assistant_text(probe).lower()
    leaks = sorted({t for t in LEAK_TERMS if t in probe_text})
    cold = not leaks
    results["a_isolation"] = (
        cold,
        "COLD answer; no leak terms found"
        if cold
        else f"LEAK terms present: {leaks}",
    )

    # ---- (b) Treatment executa o enriquecimento + escreve código parseável --
    treat_has_assemble = any(
        name == "Bash" and "assemble.py" in inp.get("command", "")
        for name, inp in iter_tool_uses(treat)
    )
    cand = out / "candidate_treatment.py"
    cand_parses = False
    parse_err = ""
    if cand.exists():
        try:
            ast.parse(cand.read_text())
            cand_parses = True
        except SyntaxError as e:
            parse_err = str(e)
    else:
        parse_err = "candidate_treatment.py missing"
    results["b_treatment_enrich_and_code"] = (
        treat_has_assemble and cand_parses,
        f"assemble.py Bash call={treat_has_assemble}; candidate parses={cand_parses}"
        + (f" ({parse_err})" if parse_err else ""),
    )

    # ---- (c) argv determinístico R2a + R4 sem codeql ------------------------
    argv = extract_assemble_prompt_argv(treat)
    argv_match = argv is not None and argv == task
    detail_c = []
    if argv is None:
        detail_c.append("R2a FAIL: no assemble.py --prompt argv found")
    elif argv_match:
        detail_c.append("R2a OK: --prompt argv byte-equals templated <TASK>")
    else:
        detail_c.append(
            f"R2a FAIL: argv mismatch (got {len(argv)} chars vs task {len(task)} chars)"
        )
    treat_codeql, t_ev = has_codeql_call(treat)
    ctrl_codeql, c_ev = has_codeql_call(ctrl)
    no_codeql = not treat_codeql and not ctrl_codeql
    if no_codeql:
        detail_c.append("R4 OK: no codeql/codeql-eval call in either arm")
    else:
        detail_c.append(
            f"R4 FAIL: codeql call present (treatment={treat_codeql} {t_ev!r}, "
            f"control={ctrl_codeql} {c_ev!r})"
        )
    results["c_argv_and_no_codeql"] = (argv_match and no_codeql, "; ".join(detail_c))

    # ---- (d) Model + success em cada sessão ---------------------------------
    detail_d = []
    all_ok = True
    for label, events in (("probe", probe), ("treatment", treat), ("control", ctrl)):
        fr = final_result(events)
        if fr is None:
            all_ok = False
            detail_d.append(f"{label}: NO result object")
            continue
        m = fr.get("model") or fr.get("modelUsage") or ""
        # `model` pode estar no topo ou aninhado em usage; checa ambas as formas.
        model_ok = False
        if isinstance(m, str):
            model_ok = m == model
        if not model_ok:
            # algumas versões reportam o model sob as chaves de usage
            mu = fr.get("modelUsage", {})
            if isinstance(mu, dict) and model in mu:
                model_ok = True
            blob = json.dumps(fr)
            if model in blob:
                model_ok = True
        subtype = fr.get("subtype")
        sub_ok = subtype == "success"
        ok = model_ok and sub_ok
        all_ok = all_ok and ok
        detail_d.append(
            f"{label}: model_ok={model_ok} (reported={fr.get('model')!r}), "
            f"subtype={subtype!r}"
        )
    results["d_model_and_success"] = (all_ok, "; ".join(detail_d))

    # ---- relatório ----------------------------------------------------------
    print("\n================ VERIFY-1 GATE ================")
    overall = True
    for key in [
        "a_isolation",
        "b_treatment_enrich_and_code",
        "c_argv_and_no_codeql",
        "d_model_and_success",
    ]:
        passed, detail = results[key]
        overall = overall and passed
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {key}: {detail}")
    print("===============================================")
    print("OVERALL:", "PASS" if overall else "FAIL")

    # escreve um resumo legível por máquina
    summary = {
        "overall_pass": overall,
        "assertions": {k: {"pass": v[0], "detail": v[1]} for k, v in results.items()},
        "extracted_assemble_argv": argv,
        "task_len": len(task),
    }
    (out / "assertions_summary.json").write_text(json.dumps(summary, indent=2))

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
