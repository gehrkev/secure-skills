#!/usr/bin/env python3
"""Exploração descritiva dos resultados M3 (nível candidato + concordância).

Complementa ``aggregate.py`` (que produz as métricas oficiais) com as leituras
exploratórias usadas na análise`:

- **Nível candidato** - taxa de ``target_cwe_hit`` por geração (sem o colapso
  de pior caso do ``vulnerable@k``), por (modalidade x braço) e agregada.
- **Concordância por célula** - partição dos pares (prompt x modalidade) em
  ambos-seguros / ambos-vulneráveis / ``b`` (skill consertou) / ``c`` (skill
  piorou), e a fração dos prompts vulneráveis no *control* que a skill deixou
  totalmente limpa nos k candidatos.

Stdlib apenas (sem pandas) para rodar de forma reprodutível em qualquer
intérprete. Um *notebook* guiado (pandas + seaborn) está planejado para
registrar a exploração com gráficos; estas funções servem de referência
numérica para ele.

Uso::

    python3 eval/runner/analysis/explore_m3.py --run-id m3_20260601_150010
    python3 eval/runner/analysis/explore_m3.py --run-id <id> --json out.json
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / "eval" / "runs"

ARMS = ("control", "treatment")
MODALITIES = ("nl", "stub")


def load_codeql_records(run_dir: Path) -> list[dict]:
    """Carrega o último registro CodeQL por (prompt, k) de cada shard.

    Args:
        run_dir: Diretório da execução (``eval/runs/<id>``).

    Returns:
        Lista de registros com ``prompt_id, arm, modality, k, target_cwe_hit``.
    """
    records: list[dict] = []
    for fp in glob.glob(str(run_dir / "codeql_progress_*.jsonl")):
        last: dict[tuple, dict] = {}
        with open(fp, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    last[(r["prompt_id"], r["k"])] = r
        records.extend(last.values())
    return records


def candidate_rates(records: list[dict]) -> dict:
    """Taxa de vulnerabilidade por geração, por (modalidade x braço) e agregada.

    Ignora candidatos com ``target_cwe_hit`` nulo (inconclusivos).

    Args:
        records: Registros CodeQL por candidato.

    Returns:
        Dict ``{(modality, arm): {"vuln": int, "total": int, "rate": float}}``
        mais a chave ``("pooled", arm)``.
    """
    acc: dict[tuple, list[int]] = {}
    for r in records:
        hit = r.get("target_cwe_hit")
        if hit is None:
            continue
        for key in ((r["modality"], r["arm"]), ("pooled", r["arm"])):
            v, t = acc.get(key, (0, 0))
            acc[key] = (v + (1 if hit else 0), t + 1)
    out: dict = {}
    for key, (v, t) in acc.items():
        out[key] = {"vuln": v, "total": t, "rate": (v / t if t else None)}
    return out


def cell_concordance(records: list[dict]) -> dict:
    """Partição de concordância dos pares (prompt x modalidade), via vulnerable@k.

    ``vulnerable@k`` da célula = 1 se algum candidato tem ``target_cwe_hit=True``
    (células totalmente nulas são descartadas).

    Args:
        records: Registros CodeQL por candidato.

    Returns:
        Dict por modalidade com ``both_safe, both_vuln, b, c, ctrl_vuln,
        n_pairs`` (``b`` = control vulnerável / treatment seguro).
    """
    # vulnerable@k por (prompt, modality, arm)
    cells: dict[tuple, dict] = {}
    for r in records:
        key = (r["prompt_id"], r["modality"], r["arm"])
        cells.setdefault(key, {"any_hit": False, "any_conclusive": False})
        if r.get("target_cwe_hit") is not None:
            cells[key]["any_conclusive"] = True
            if r["target_cwe_hit"]:
                cells[key]["any_hit"] = True

    def vatk(prompt: str, modality: str, arm: str):
        c = cells.get((prompt, modality, arm))
        if not c or not c["any_conclusive"]:
            return None
        return 1 if c["any_hit"] else 0

    prompts = sorted({p for (p, _m, _a) in cells})
    out: dict = {}
    for modality in MODALITIES:
        both_safe = both_vuln = b = c = 0
        for prompt in prompts:
            t = vatk(prompt, modality, "treatment")
            ctrl = vatk(prompt, modality, "control")
            if t is None or ctrl is None:
                continue
            if t == 0 and ctrl == 0:
                both_safe += 1
            elif t == 1 and ctrl == 1:
                both_vuln += 1
            elif t == 0 and ctrl == 1:
                b += 1
            elif t == 1 and ctrl == 0:
                c += 1
        out[modality] = {
            "both_safe": both_safe,
            "both_vuln": both_vuln,
            "b": b,
            "c": c,
            "ctrl_vuln": both_vuln + b,
            "n_pairs": both_safe + both_vuln + b + c,
        }
    return out


def _print_report(rates: dict, conc: dict) -> None:
    """Imprime o relatório exploratório em stdout."""
    print("=== Nível candidato - taxa de vulnerabilidade por geração ===")
    for modality in (*MODALITIES, "pooled"):
        ctrl = rates.get((modality, "control"))
        trt = rates.get((modality, "treatment"))
        if not ctrl or not trt:
            continue
        abs_pp = (ctrl["rate"] - trt["rate"]) * 100
        rel = (1 - trt["rate"] / ctrl["rate"]) * 100 if ctrl["rate"] else 0.0
        label = "agregado" if modality == "pooled" else modality
        print(
            f"  {label:9s}: control {ctrl['rate']*100:4.1f}% ({ctrl['vuln']}/{ctrl['total']})"
            f"  treatment {trt['rate']*100:4.1f}% ({trt['vuln']}/{trt['total']})"
            f"  Δ -{abs_pp:.1f}pp (-{rel:.0f}%)"
        )

    print("\n=== Concordância por célula (prompt x modalidade), vulnerable@k ===")
    tot_b = tot_ctrl = 0
    for modality in MODALITIES:
        s = conc[modality]
        tot_b += s["b"]
        tot_ctrl += s["ctrl_vuln"]
        frac = 100 * s["b"] / s["ctrl_vuln"] if s["ctrl_vuln"] else 0.0
        print(
            f"  {modality:4s} (n={s['n_pairs']}): ambos_seguros={s['both_safe']} "
            f"ambos_vuln={s['both_vuln']} b={s['b']} c={s['c']} "
            f"-> skill limpou {s['b']}/{s['ctrl_vuln']} dos vulneráveis no control ({frac:.0f}%)"
        )
    pooled_frac = 100 * tot_b / tot_ctrl if tot_ctrl else 0.0
    print(
        f"  AGREGADO: skill limpou totalmente {tot_b}/{tot_ctrl} "
        f"dos prompts vulneráveis no control ({pooled_frac:.0f}%)"
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-id", required=True, help="ID da execução em eval/runs/")
    p.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    p.add_argument("--json", type=Path, default=None, help="Grava o resumo em JSON")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    run_dir = args.runs_dir / args.run_id
    records = load_codeql_records(run_dir)
    rates = candidate_rates(records)
    conc = cell_concordance(records)
    _print_report(rates, conc)
    if args.json:
        payload = {
            "run_id": args.run_id,
            "candidate_rates": {f"{m}/{a}": v for (m, a), v in rates.items()},
            "cell_concordance": conc,
        }
        args.json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON gravado em {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
