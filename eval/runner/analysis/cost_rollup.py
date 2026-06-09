#!/usr/bin/env python3
"""Roll-up de custo e tokens por (modalidade x braço) - M3.

Lê os ``result.json`` de cada sessão de geração (``gen/<modality>/<arm>/
<prompt>/s<k>/result.json``) e agrega custo e tokens, comparando
*control* x *treatment* e NL x *stub*.

**Ressalva importante:** em assinatura Pro/OAuth o ``total_cost_usd`` é
**notional** (estimativa, não cobrança real por token). Serve como **medida
relativa** de esforço/throughput, não como fatura. Os tokens, sim, são
contagens reais reportadas pela API.

Stdlib apenas. Uso::

    python3 eval/runner/analysis/cost_rollup.py --run-id m3_20260601_150010
    python3 eval/runner/analysis/cost_rollup.py --run-id <id> --json out.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / "eval" / "runs"

ARMS = ("control", "treatment")
MODALITIES = ("nl", "stub")


def collect_sessions(run_dir: Path) -> list[dict]:
    """Coleta métricas de custo/tokens de cada ``result.json`` da execução.

    Args:
        run_dir: Diretório da execução (``eval/runs/<id>``).

    Returns:
        Lista de dicts com ``modality, arm, cost, out, in_fresh,
        cache_read, cache_create, duration_ms``.
    """
    out: list[dict] = []
    gen = run_dir / "gen"
    for fp in gen.glob("*/*/*/s*/result.json"):
        # caminho: gen/<modality>/<arm>/<prompt>/s<k>/result.json
        parts = fp.relative_to(gen).parts
        modality, arm = parts[0], parts[1]
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        usage = d.get("usage") or {}
        out.append({
            "modality": modality,
            "arm": arm,
            "cost": d.get("total_cost_usd") or 0.0,
            "out": usage.get("output_tokens") or 0,
            "in_fresh": usage.get("input_tokens") or 0,
            "cache_read": usage.get("cache_read_input_tokens") or 0,
            "cache_create": usage.get("cache_creation_input_tokens") or 0,
            "duration_ms": d.get("duration_ms") or 0,
        })
    return out


def _agg(rows: list[dict]) -> dict:
    """Soma/contagem dos campos numéricos de um conjunto de sessões."""
    keys = ("cost", "out", "in_fresh", "cache_read", "cache_create", "duration_ms")
    acc = {k: 0.0 for k in keys}
    for r in rows:
        for k in keys:
            acc[k] += r[k]
    acc["n"] = len(rows)
    return acc


def rollup(sessions: list[dict]) -> dict:
    """Agrega por (modalidade x braço), por braço, por modalidade e total."""
    out: dict = {}
    for modality in MODALITIES:
        for arm in ARMS:
            sub = [s for s in sessions if s["modality"] == modality and s["arm"] == arm]
            out[f"{modality}/{arm}"] = _agg(sub)
    for arm in ARMS:
        out[f"*/{arm}"] = _agg([s for s in sessions if s["arm"] == arm])
    for modality in MODALITIES:
        out[f"{modality}/*"] = _agg([s for s in sessions if s["modality"] == modality])
    out["*/*"] = _agg(sessions)
    return out


def _fmt(a: dict) -> str:
    n = a["n"] or 1
    return (
        f"n={a['n']:4d}  custo_total=${a['cost']:7.3f}  custo/sessão=${a['cost']/n:.4f}  "
        f"out/sessão={a['out']/n:6.0f}tk  in_fresh/sessão={a['in_fresh']/n:6.0f}tk  "
        f"cache_read/sessão={a['cache_read']/n:7.0f}tk  dur/sessão={a['duration_ms']/n/1000:5.1f}s"
    )


def _print_report(roll: dict) -> None:
    print("=== Custo / tokens por (modalidade x braço) ===")
    print("  (total_cost_usd é NOTIONAL em Pro/OAuth — medida relativa, não fatura)\n")
    for modality in MODALITIES:
        for arm in ARMS:
            print(f"  {modality:4s} {arm:9s}: {_fmt(roll[f'{modality}/{arm}'])}")
    print("\n  -- por braço --")
    for arm in ARMS:
        print(f"  {'*':4s} {arm:9s}: {_fmt(roll[f'*/{arm}'])}")
    print("\n  -- por modalidade --")
    for modality in MODALITIES:
        print(f"  {modality:4s} {'*':9s}: {_fmt(roll[f'{modality}/*'])}")
    print(f"\n  TOTAL          : {_fmt(roll['*/*'])}")

    # Deltas de interesse
    def cps(key):  # custo por sessão
        a = roll[key]
        return a["cost"] / (a["n"] or 1)

    print("\n=== Comparações ===")
    t, c = cps("*/treatment"), cps("*/control")
    print(f"  treatment vs control: ${t:.4f} vs ${c:.4f}/sessão  (+{100*(t/c-1):.0f}%)")
    nl, st = cps("nl/*"), cps("stub/*")
    print(f"  nl vs stub:           ${nl:.4f} vs ${st:.4f}/sessão  ({100*(nl/st-1):+.0f}%)")
    for modality in MODALITIES:
        tt, cc = cps(f"{modality}/treatment"), cps(f"{modality}/control")
        print(f"  {modality}: treatment vs control: ${tt:.4f} vs ${cc:.4f}/sessão  (+{100*(tt/cc-1):.0f}%)")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-id", required=True)
    p.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    p.add_argument("--json", type=Path, default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    run_dir = args.runs_dir / args.run_id
    sessions = collect_sessions(run_dir)
    roll = rollup(sessions)
    _print_report(roll)
    if args.json:
        args.json.write_text(json.dumps(roll, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON gravado em {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
