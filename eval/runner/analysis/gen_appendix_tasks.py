"""Gera o apêndice LaTeX com a tripla (ID da tarefa, stub, prompt NL) das 100 tarefas.

Lê ``treated_dataset.jsonl`` de uma execução e emite um arquivo ``.tex`` com um
bloco por tarefa: o ID em ``\\texttt``, o stub num ambiente ``lstlisting`` (código
verbatim) e a paráfrase NL como parágrafo. O stub não é escapado (lstlisting é
verbatim); ID e NL passam por escape de caracteres especiais do LaTeX.

Uso:
    python3 gen_appendix_tasks.py --run-id m3_20260601_150010 \
        --out <repo>/TCC-tex/.../PosTextuais/ApendiceTarefas.tex
"""

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

_LATEX_ESCAPE = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_tex(s: str) -> str:
    """Escapa caracteres especiais do LaTeX em texto corrido."""
    out = []
    for ch in s:
        out.append(_LATEX_ESCAPE.get(ch, ch))
    return "".join(out)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-id", required=True)
    p.add_argument("--out", required=True, help="Caminho do .tex de saída")
    args = p.parse_args()

    ds = REPO_ROOT / "eval" / "runs" / args.run_id / "treated_dataset.jsonl"
    rows = [json.loads(l) for l in ds.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows.sort(key=lambda r: r["prompt_id"])

    non_ascii = sorted({ch for r in rows for ch in (r["stub"] + r.get("nl_paraphrase", "")) if ord(ch) > 127})

    lines = [
        "% Gerado por eval/runner/analysis/gen_appendix_tasks.py — NÃO editar à mão.",
        f"% Execução: {args.run_id}. {len(rows)} tarefas.",
        "",
    ]
    for r in rows:
        pid = escape_tex(r["prompt_id"])
        cwe = escape_tex(r.get("target_cwe", ""))
        stratum = escape_tex(r.get("stratum", ""))
        nl = escape_tex(r.get("nl_paraphrase", "").strip())
        stub = r["stub"].rstrip("\n")
        lines += [
            r"\bigskip",
            rf"\noindent\textbf{{Tarefa:}}~\texttt{{{pid}}}\quad"
            rf"(\textbf{{CWE:}}~{cwe},~\textbf{{estrato:}}~{stratum})",
            "",
            r"\noindent\textbf{\textit{stub}:}",
            r"\begin{lstlisting}",
            stub,
            r"\end{lstlisting}",
            r"\noindent\textbf{Prompt NL:} " + nl,
            "",
        ]

    out = Path(args.out)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito: {out} ({len(rows)} tarefas)")
    if non_ascii:
        print(f"AVISO: {len(non_ascii)} caracteres não-ASCII encontrados: {non_ascii}")
    else:
        print("Sem caracteres não-ASCII (config listings mínima é suficiente).")


if __name__ == "__main__":
    main()
