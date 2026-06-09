#!/usr/bin/env python3
"""Agregador de métricas M3 para avaliação secure-skills.

Consome todas as saídas de uma execução completa (T11 + T12), calcula métricas
@k, testes estatísticos (McNemar exato + regressão logística com prompt
dummies), tabelas estratificadas (A/B/C) e grava um diretório ``metrics/``
autocontido mais ``RERUN.md``.

Uso::

    python3 eval/runner/aggregate/aggregate.py --run-id <id>
    python3 eval/runner/aggregate/aggregate.py --selftest
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import sys
import tempfile
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # backend não-interativo para geração de imagens
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sst
import statsmodels.api as sm

# ---------------------------------------------------------------------------
# Ajuste de sys.path - permite importar lib/ como pacote irmão.
# ---------------------------------------------------------------------------
_RUNNER_ROOT = Path(__file__).resolve().parents[1]
if str(_RUNNER_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUNNER_ROOT))

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATASET = REPO_ROOT / "eval" / "runner" / "dataset" / "treated_dataset.jsonl"
DEFAULT_RUNS_DIR = REPO_ROOT / "eval" / "runs"

ARMS = ("treatment", "control")
MODALITIES = ("nl", "stub")
STRATA = ("A", "B", "C")

# Número de candidatos k por célula.
K = 5


# ---------------------------------------------------------------------------
# Helpers de I/O
# ---------------------------------------------------------------------------


def _load_jsonl(path: Path) -> list[dict]:
    """Carrega um arquivo JSONL em uma lista de dicts.

    Args:
        path: Caminho do arquivo ``.jsonl``.

    Returns:
        Lista de dicts decodificados (linhas vazias ignoradas).

    Raises:
        FileNotFoundError: Se ``path`` não existir.
    """
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _load_dataset(path: Path) -> dict[str, dict]:
    """Carrega o dataset tratado indexado por ``prompt_id``.

    Args:
        path: Caminho do ``treated_dataset.jsonl``.

    Returns:
        Mapa ``prompt_id -> linha``.
    """
    dataset: dict[str, dict] = {}
    if not path.exists():
        logger.warning("Dataset não encontrado em %s.", path)
        return dataset
    for row in _load_jsonl(path):
        pid = row.get("prompt_id") or row.get("id")
        if pid:
            dataset[pid] = row
    return dataset


def _load_codeql_records(run_dir: Path) -> list[dict]:
    """Carrega todos os registros de progresso CodeQL da execução.

    Varre os arquivos ``codeql_progress_<modality>_<arm>.jsonl`` para todas
    as combinações conhecidas.

    Args:
        run_dir: Diretório raiz da execução.

    Returns:
        Lista de registros CodeQL (podem ter ``target_cwe_hit=null``).
    """
    records: list[dict] = []
    for modality in MODALITIES:
        for arm in ARMS:
            path = run_dir / f"codeql_progress_{modality}_{arm}.jsonl"
            if path.exists():
                records.extend(_load_jsonl(path))
                logger.info("CodeQL carregado: %s (%d total)", path.name, len(records))
            else:
                logger.warning("Arquivo CodeQL não encontrado: %s", path)
    return records


def _load_functional_records(run_dir: Path) -> list[dict]:
    """Carrega os registros de resultado funcional da execução.

    Args:
        run_dir: Diretório raiz da execução.

    Returns:
        Lista de registros funcionais.
    """
    path = run_dir / "functional_results.jsonl"
    if not path.exists():
        logger.warning("functional_results.jsonl não encontrado em %s", run_dir)
        return []
    records = _load_jsonl(path)
    logger.info("Funcional carregado: %d registros", len(records))
    return records


def _load_manifest(run_dir: Path) -> dict:
    """Carrega o manifest.json de uma execução.

    Args:
        run_dir: Diretório raiz da execução.

    Returns:
        Dict com metadados da execução (vazio se não existir).
    """
    path = run_dir / "manifest.json"
    if not path.exists():
        logger.warning("manifest.json não encontrado em %s", run_dir)
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Construção dos DataFrames de trabalho
# ---------------------------------------------------------------------------


def _build_codeql_df(records: list[dict]) -> pd.DataFrame:
    """Constrói DataFrame de registros CodeQL normalizado.

    Cada linha representa um candidato (prompt x arm x modality x k).
    ``target_cwe_hit`` é preservado como ``Optional[bool]`` (``None`` = falha
    de avaliação).

    Args:
        records: Lista bruta de registros CodeQL.

    Returns:
        DataFrame com colunas: ``prompt_id, arm, modality, k, target_cwe_hit``.
    """
    rows = []
    for rec in records:
        hit_raw = rec.get("target_cwe_hit")
        # null JSON -> None Python; True/False mantidos
        hit: Optional[bool] = None if hit_raw is None else bool(hit_raw)
        rows.append({
            "prompt_id": rec["prompt_id"],
            "arm": rec["arm"],
            "modality": rec["modality"],
            "k": int(rec["k"]),
            "target_cwe_hit": hit,
        })
    df = pd.DataFrame(rows, columns=["prompt_id", "arm", "modality", "k", "target_cwe_hit"])
    logger.info("CodeQL DataFrame: %d linhas", len(df))
    return df


def _build_functional_df(records: list[dict]) -> pd.DataFrame:
    """Constrói DataFrame de registros funcionais normalizado.

    Args:
        records: Lista bruta de registros funcionais.

    Returns:
        DataFrame com colunas: ``prompt_id, arm, modality, k, parses,
        defines_symbol, imports_clean``.
    """
    rows = []
    for rec in records:
        rows.append({
            "prompt_id": rec["prompt_id"],
            "arm": rec["arm"],
            "modality": rec["modality"],
            "k": int(rec["k"]),
            "parses": bool(rec.get("parses", False)),
            "defines_symbol": bool(rec.get("defines_symbol", False)),
            "imports_clean": bool(rec.get("imports_clean", False)),
        })
    df = pd.DataFrame(rows, columns=[
        "prompt_id", "arm", "modality", "k",
        "parses", "defines_symbol", "imports_clean",
    ])
    logger.info("Funcional DataFrame: %d linhas", len(df))
    return df


# ---------------------------------------------------------------------------
# Métricas @k (Siddiq et al. 2024, k=5)
# ---------------------------------------------------------------------------


def _compute_atk_metrics(
    codeql_df: pd.DataFrame,
    func_df: pd.DataFrame,
    dataset: dict[str, dict],
) -> pd.DataFrame:
    """Computa ``vulnerable@k``, ``security@k`` e ``pass@k`` por célula.

    Cada célula é ``(prompt_id, arm, modality)``.

    Definições:
    - ``vulnerable@k`` = 1 se QUALQUER candidato tem ``target_cwe_hit=True``.
      Se TODOS os candidatos têm ``target_cwe_hit=None``, a célula é marcada
      como ausente (``NaN``).
    - ``security@k`` = 1 se QUALQUER candidato tem ``target_cwe_hit=False``
      (ou seja, existe pelo menos um candidato não-vulnerável).
    - ``pass@k`` = 1 se QUALQUER candidato tem ``parses=True AND
      defines_symbol=True AND imports_clean=True``.

    Args:
        codeql_df: DataFrame CodeQL por candidato.
        func_df: DataFrame funcional por candidato.
        dataset: Mapa ``prompt_id -> linha`` do dataset tratado (para estrato).

    Returns:
        DataFrame com uma linha por célula e colunas:
        ``prompt_id, arm, modality, stratum, vulnerable_at_k,
        security_at_k, pass_at_k``.
    """
    # Células únicas
    cells: list[tuple[str, str, str]] = list(
        {(r["prompt_id"], r["arm"], r["modality"])
         for r in codeql_df.to_dict("records")}
        | {(r["prompt_id"], r["arm"], r["modality"])
           for r in func_df.to_dict("records")}
    )

    rows_out: list[dict] = []
    for prompt_id, arm, modality in cells:
        # --- CodeQL ---
        codeql_cell = codeql_df[
            (codeql_df["prompt_id"] == prompt_id)
            & (codeql_df["arm"] == arm)
            & (codeql_df["modality"] == modality)
        ]

        hits = codeql_cell["target_cwe_hit"].dropna()
        all_null = len(codeql_cell) > 0 and codeql_cell["target_cwe_hit"].isna().all()

        if all_null or len(codeql_cell) == 0:
            vulnerable_at_k = float("nan")
            security_at_k = float("nan")
        else:
            vulnerable_at_k = 1.0 if (hits == True).any() else 0.0  # noqa: E712
            security_at_k = 1.0 if (hits == False).any() else 0.0  # noqa: E712

        # --- Funcional ---
        func_cell = func_df[
            (func_df["prompt_id"] == prompt_id)
            & (func_df["arm"] == arm)
            & (func_df["modality"] == modality)
        ]
        if len(func_cell) == 0:
            pass_at_k = float("nan")
        else:
            pass_mask = (
                func_cell["parses"]
                & func_cell["defines_symbol"]
                & func_cell["imports_clean"]
            )
            pass_at_k = 1.0 if pass_mask.any() else 0.0

        # Estrato do dataset
        stratum = dataset.get(prompt_id, {}).get("stratum", "?")

        rows_out.append({
            "prompt_id": prompt_id,
            "arm": arm,
            "modality": modality,
            "stratum": stratum,
            "vulnerable_at_k": vulnerable_at_k,
            "security_at_k": security_at_k,
            "pass_at_k": pass_at_k,
        })

    df = pd.DataFrame(rows_out)
    df = df.sort_values(["prompt_id", "arm", "modality"]).reset_index(drop=True)
    logger.info("Métricas @k: %d células calculadas", len(df))
    return df


# ---------------------------------------------------------------------------
# McNemar exato por modalidade
# ---------------------------------------------------------------------------


def _mcnemar_exact(
    per_prompt_df: pd.DataFrame,
    modality: str,
) -> dict:
    """Executa o teste de McNemar exato para uma modalidade.

    Constrói a tabela 2x2 (treatment x control) para ``vulnerable@k`` e
    aplica ``scipy.stats.binomtest(b, b+c, 0.5)`` (dois lados).

    Args:
        per_prompt_df: DataFrame com uma linha por (prompt_id, arm, modality).
        modality: ``"nl"`` ou ``"stub"``.

    Returns:
        Dict com ``b, c, p_value, risk_diff, log_odds, log_odds_se``.
        Retorna dict com ``None`` se não houver dados suficientes.
    """
    df_mod = per_prompt_df[per_prompt_df["modality"] == modality].dropna(
        subset=["vulnerable_at_k"]
    )

    treat = df_mod[df_mod["arm"] == "treatment"].set_index("prompt_id")["vulnerable_at_k"]
    ctrl = df_mod[df_mod["arm"] == "control"].set_index("prompt_id")["vulnerable_at_k"]

    # Somente prompts com dados em ambos os braços
    common = treat.index.intersection(ctrl.index)
    if len(common) < 2:
        logger.warning("McNemar %s: poucos prompts com dados em ambos os braços (%d)", modality, len(common))
        return {
            "b": None, "c": None, "p_value": None,
            "risk_diff": None, "log_odds": None, "log_odds_se": None,
            "n_prompts": len(common),
        }

    v_treat = treat.loc[common]
    v_ctrl = ctrl.loc[common]

    # b = treatment=0, control=1 (treatment ajudou - reduziu vulnerabilidade)
    b = int(((v_treat == 0) & (v_ctrl == 1)).sum())
    # c = treatment=1, control=0 (treatment prejudicou)
    c = int(((v_treat == 1) & (v_ctrl == 0)).sum())

    n = b + c
    if n == 0:
        # Sem discordância - p-value = 1
        p_value = 1.0
    else:
        result = sst.binomtest(b, n, 0.5, alternative="two-sided")
        p_value = float(result.pvalue)

    risk_diff = float(v_ctrl.mean() - v_treat.mean())

    # Log-odds ratio (Haldane-Anscombe com +0.5 para estabilidade)
    b_adj = b + 0.5
    c_adj = c + 0.5
    log_odds = float(math.log(b_adj / c_adj))
    log_odds_se = float(math.sqrt(1.0 / b_adj + 1.0 / c_adj))

    return {
        "b": b,
        "c": c,
        "p_value": p_value,
        "risk_diff": risk_diff,
        "log_odds": log_odds,
        "log_odds_se": log_odds_se,
        "n_prompts": len(common),
    }


# ---------------------------------------------------------------------------
# Regressão logística com dummies de prompt
# ---------------------------------------------------------------------------


_LOGIT_NOTE = (
    "GLMM logístico de efeitos mistos com intercepto aleatório de prompt "
    "(vulnerable ~ arm * modality + (1|prompt)), ajustado por Bayes "
    "variacional (statsmodels BinomialBayesMixedGLM). Os coeficientes são "
    "log-odds condicionais (subject-specific); os OR têm magnitude maior que "
    "as taxas marginais @k porque a variância entre prompts é grande. O p é "
    "uma aproximação tipo-Wald da posterior VB (|média|/desvio)."
)


def _logistic_regression(codeql_df: pd.DataFrame) -> dict:
    """Ajusta o GLMM logístico com intercepto aleatório de prompt.

    Modelo: ``vulnerable ~ arm * modality + (1|prompt)``, ajustado por Bayes
    variacional (``BinomialBayesMixedGLM``). O *prior* regulariza os efeitos
    fixos, mantendo estimativas finitas e identificadas mesmo sob separação
    perfeita por prompt (prompts constantes e McNemar c=0).

    Args:
        codeql_df: DataFrame CodeQL por candidato.

    Returns:
        Dict com coeficientes, OR, IC 95% (credível) e p aproximado para
        ``arm``, ``modality`` e ``arm_x_modality``, mais o desvio-padrão do
        intercepto aleatório; nota metodológica incluída.
    """
    df = codeql_df.dropna(subset=["target_cwe_hit"]).copy()
    df["y"] = df["target_cwe_hit"].astype(int)
    df["arm_bin"] = (df["arm"] == "treatment").astype(int)
    df["modality_bin"] = (df["modality"] == "stub").astype(int)
    df["arm_x_modality"] = df["arm_bin"] * df["modality_bin"]

    # Efeitos fixos: intercepto + arm + modality + interação.
    fe_names = ["const", "arm_bin", "modality_bin", "arm_x_modality"]
    exog_fe = pd.DataFrame(
        {
            "const": 1.0,
            "arm_bin": df["arm_bin"].astype(float),
            "modality_bin": df["modality_bin"].astype(float),
            "arm_x_modality": df["arm_x_modality"].astype(float),
        },
        index=df.index,
    )

    # Efeito aleatório: um intercepto por prompt, componente de variância única.
    exog_vc = pd.get_dummies(df["prompt_id"], dtype=float)
    ident = np.zeros(exog_vc.shape[1], dtype=int)  # todos no mesmo VC (1|prompt)

    try:
        from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

        model = BinomialBayesMixedGLM(
            df["y"].values, exog_fe.values, exog_vc.values, ident
        )
        result = model.fit_vb(verbose=False)
    except Exception as exc:  # pragma: no cover - caminho de degradação
        logger.error("GLMM logístico falhou: %s", exc)
        return {"note": _LOGIT_NOTE, "error": str(exc)}

    def _safe_exp(x: float) -> float:
        """``math.exp`` que satura em ``inf``/``0`` em vez de estourar."""
        try:
            return float(math.exp(x))
        except OverflowError:
            return float("inf") if x > 0 else 0.0

    def _extract_term(idx: int) -> dict:
        coef = float(result.fe_mean[idx])
        sd = float(result.fe_sd[idx])
        # p aproximado tipo-Wald a partir da posterior VB.
        p = float(2.0 * sst.norm.sf(abs(coef) / sd)) if sd > 0 else 0.0
        return {
            "coef": coef,
            "sd": sd,
            "OR": _safe_exp(coef),
            "CI_lower": _safe_exp(coef - 1.96 * sd),
            "CI_upper": _safe_exp(coef + 1.96 * sd),
            "p": p,
        }

    out = {
        "note": _LOGIT_NOTE,
        "arm": _extract_term(fe_names.index("arm_bin")),
        "modality": _extract_term(fe_names.index("modality_bin")),
        "arm_x_modality": _extract_term(fe_names.index("arm_x_modality")),
    }
    # Desvio-padrão do intercepto aleatório de prompt (escala log-odds).
    try:
        out["prompt_intercept_sd"] = float(np.exp(result.vcp_mean[0]))
    except Exception:  # pragma: no cover
        pass
    return out


# ---------------------------------------------------------------------------
# Métricas resumidas por armxmodality
# ---------------------------------------------------------------------------


def _mean_metrics(df_subset: pd.DataFrame) -> dict:
    """Computa médias de ``vulnerable@k``, ``security@k`` e ``pass@k``.

    Args:
        df_subset: Subconjunto do DataFrame de métricas @k.

    Returns:
        Dict com chaves ``vulnerable_at_k``, ``security_at_k``, ``pass_at_k``
        (média, NaN tratado como ausente).
    """
    def _safe_mean(series: pd.Series) -> Optional[float]:
        valid = series.dropna()
        return float(valid.mean()) if len(valid) > 0 else None

    return {
        "vulnerable_at_k": _safe_mean(df_subset["vulnerable_at_k"]),
        "security_at_k": _safe_mean(df_subset["security_at_k"]),
        "pass_at_k": _safe_mean(df_subset["pass_at_k"]),
        "n_prompts": int(df_subset["prompt_id"].nunique()),
    }


# ---------------------------------------------------------------------------
# Análise estratificada
# ---------------------------------------------------------------------------


def _stratified_analysis(
    per_prompt_df: pd.DataFrame,
    mcnemar_min_n: int = 5,
) -> dict:
    """Computa métricas e McNemar por estrato (A, B, C).

    Grupo C (n=5) é reportado apenas descritivamente conforme O1.

    Args:
        per_prompt_df: DataFrame com uma linha por (prompt_id, arm, modality).
        mcnemar_min_n: Número mínimo de prompts para rodar McNemar.

    Returns:
        Dict ``{stratum: {...}}``.
    """
    strata_out: dict[str, dict] = {}

    for stratum in STRATA:
        df_s = per_prompt_df[per_prompt_df["stratum"] == stratum]
        n_prompts = df_s["prompt_id"].nunique()

        stratum_data: dict = {
            "n_prompts": n_prompts,
            "metrics": {},
        }

        if stratum == "C":
            stratum_data["note"] = (
                "n=5 prompts — descriptive only (O1 decision)"
            )

        for arm in ARMS:
            for modality in MODALITIES:
                cell = df_s[(df_s["arm"] == arm) & (df_s["modality"] == modality)]
                stratum_data["metrics"][f"{arm}_{modality}"] = _mean_metrics(cell)

        # McNemar por modalidade dentro do estrato
        if stratum != "C" and n_prompts >= mcnemar_min_n:
            mcnemar_by_mod: dict = {}
            for modality in MODALITIES:
                mcnemar_by_mod[modality] = _mcnemar_exact(df_s, modality)
            stratum_data["mcnemar"] = mcnemar_by_mod
        else:
            stratum_data["mcnemar"] = None
            if stratum == "C":
                stratum_data["o1_decision"] = (
                    "Group C (n=5) too small for powered McNemar; reported descriptively"
                )

        strata_out[stratum] = stratum_data

    return strata_out


# ---------------------------------------------------------------------------
# Geração de gráficos
# ---------------------------------------------------------------------------


def _plot_vulnerable_by_stratum(
    per_prompt_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Gera gráfico de barras de ``vulnerable@k`` por estrato x arm x modality.

    Args:
        per_prompt_df: DataFrame com métricas @k por (prompt_id, arm, modality).
        output_path: Caminho de saída do PNG.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax_idx, modality in enumerate(MODALITIES):
        df_mod = per_prompt_df[per_prompt_df["modality"] == modality]
        data_arms: dict[str, list[float]] = {arm: [] for arm in ARMS}

        for stratum in STRATA:
            df_s = df_mod[df_mod["stratum"] == stratum]
            for arm in ARMS:
                subset = df_s[df_s["arm"] == arm]["vulnerable_at_k"].dropna()
                data_arms[arm].append(float(subset.mean()) if len(subset) > 0 else 0.0)

        x = np.arange(len(STRATA))
        width = 0.35

        ax = axes[ax_idx]
        ax.bar(x - width / 2, data_arms["treatment"], width, label="treatment", alpha=0.8)
        ax.bar(x + width / 2, data_arms["control"], width, label="control", alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(STRATA)
        ax.set_xlabel("Estrato")
        ax.set_ylabel("vulnerable@k (média)")
        ax.set_title(f"vulnerable@k por estrato — modality={modality}")
        ax.legend()
        ax.set_ylim(0, 1.05)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Gráfico gravado: %s", output_path)


def _plot_vulnerable_by_modality(
    per_prompt_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Gera gráfico de barras de ``vulnerable@k`` por modality x arm.

    Args:
        per_prompt_df: DataFrame com métricas @k.
        output_path: Caminho de saída do PNG.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    data_arms: dict[str, list[float]] = {arm: [] for arm in ARMS}
    for modality in MODALITIES:
        df_mod = per_prompt_df[per_prompt_df["modality"] == modality]
        for arm in ARMS:
            subset = df_mod[df_mod["arm"] == arm]["vulnerable_at_k"].dropna()
            data_arms[arm].append(float(subset.mean()) if len(subset) > 0 else 0.0)

    x = np.arange(len(MODALITIES))
    width = 0.35

    ax.bar(x - width / 2, data_arms["treatment"], width, label="treatment", alpha=0.8)
    ax.bar(x + width / 2, data_arms["control"], width, label="control", alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(MODALITIES)
    ax.set_xlabel("Modalidade")
    ax.set_ylabel("vulnerable@k (média)")
    ax.set_title("vulnerable@k por modalidade × arm")
    ax.legend()
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Gráfico gravado: %s", output_path)


# ---------------------------------------------------------------------------
# Escrita de RERUN.md
# ---------------------------------------------------------------------------


def _write_rerun_md(run_dir: Path, run_id: str) -> None:
    """Escreve o arquivo ``RERUN.md`` na raiz da execução.

    Args:
        run_dir: Diretório raiz da execução.
        run_id: Identificador da execução.
    """
    content = f"""# Rerun metrics from saved generations

This reproduces aggregation + statistics from already-generated candidates without re-running any Claude Code sessions.

## Command

```bash
python3 eval/runner/aggregate/aggregate.py --run-id {run_id} [--runs-dir eval/runs/]
```

## What it reads

- `codeql_progress_<modality>_<arm>.jsonl` - CodeQL security signal (T11)
- `functional_results.jsonl` - Functional signal (T12)
- `eval/runner/dataset/treated_dataset.jsonl` - Strata + metadata

## What it writes

- `metrics/per_prompt.csv`, `per_stratum.csv`, `pooled.json`
- `metrics/plots/*.png`

## CodeQL tool label (R10)

All security metrics are qualified by CodeQL image tag recorded in `manifest.json`.
"""
    path = run_dir / "RERUN.md"
    path.write_text(content, encoding="utf-8")
    logger.info("RERUN.md gravado em %s", path)


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------


def run_aggregate(
    run_id: str,
    runs_dir: Path,
    dataset_path: Path,
) -> int:
    """Executa o pipeline completo de agregação e estatísticas.

    Args:
        run_id: Identificador da execução.
        runs_dir: Diretório raiz das execuções.
        dataset_path: Caminho do ``treated_dataset.jsonl``.

    Returns:
        Código de saída (0 = sucesso, 1 = erro).
    """
    run_dir = runs_dir / run_id
    if not run_dir.exists():
        logger.error("Diretório de execução não encontrado: %s", run_dir)
        print(f"Run dir not found: {run_dir}")
        return 1

    # --- Carregamento ---
    manifest = _load_manifest(run_dir)
    codeql_image_tag = manifest.get("codeql_image_tag", "unknown")
    model_id = manifest.get("model_id", "unknown")

    dataset = _load_dataset(dataset_path)

    codeql_records = _load_codeql_records(run_dir)
    func_records = _load_functional_records(run_dir)

    if not codeql_records and not func_records:
        logger.error("Nenhum dado de avaliação encontrado em %s", run_dir)
        print(f"No evaluation data found in {run_dir}")
        return 1

    codeql_df = _build_codeql_df(codeql_records)
    func_df = _build_functional_df(func_records)

    # --- Métricas @k ---
    per_prompt_df = _compute_atk_metrics(codeql_df, func_df, dataset)

    # --- Saída: metrics/ ---
    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    plots_dir = metrics_dir / "plots"
    plots_dir.mkdir(exist_ok=True)

    # per_prompt.csv
    per_prompt_df.to_csv(metrics_dir / "per_prompt.csv", index=False)
    logger.info("per_prompt.csv gravado (%d linhas)", len(per_prompt_df))

    # per_stratum.csv
    stratum_rows: list[dict] = []
    for stratum in STRATA:
        for arm in ARMS:
            for modality in MODALITIES:
                subset = per_prompt_df[
                    (per_prompt_df["stratum"] == stratum)
                    & (per_prompt_df["arm"] == arm)
                    & (per_prompt_df["modality"] == modality)
                ]
                m = _mean_metrics(subset)
                stratum_rows.append({
                    "stratum": stratum,
                    "arm": arm,
                    "modality": modality,
                    **m,
                })
    per_stratum_df = pd.DataFrame(stratum_rows)
    per_stratum_df.to_csv(metrics_dir / "per_stratum.csv", index=False)
    logger.info("per_stratum.csv gravado (%d linhas)", len(per_stratum_df))

    # --- Métricas por arm x modality ---
    metrics_by_group: dict = {}
    for modality in MODALITIES:
        metrics_by_group[modality] = {}
        for arm in ARMS:
            subset = per_prompt_df[
                (per_prompt_df["arm"] == arm)
                & (per_prompt_df["modality"] == modality)
            ]
            metrics_by_group[modality][arm] = _mean_metrics(subset)

    # Pooled (todos os arm x modality)
    metrics_by_group["pooled"] = {}
    for arm in ARMS:
        subset = per_prompt_df[per_prompt_df["arm"] == arm]
        metrics_by_group["pooled"][arm] = _mean_metrics(subset)

    # --- McNemar por modalidade ---
    mcnemar_results: dict = {}
    for modality in MODALITIES:
        mcnemar_results[modality] = _mcnemar_exact(per_prompt_df, modality)

    # --- Regressão logística ---
    logit_result = _logistic_regression(codeql_df)

    # --- Análise estratificada ---
    strata_result = _stratified_analysis(per_prompt_df)

    # --- pooled.json ---
    pooled = {
        "codeql_image_tag": codeql_image_tag,
        "model_id": model_id,
        "run_id": run_id,
        "k": K,
        "metrics": metrics_by_group,
        "mcnemar": mcnemar_results,
        "logistic_regression": logit_result,
        "strata": strata_result,
    }
    pooled_path = metrics_dir / "pooled.json"
    pooled_path.write_text(json.dumps(pooled, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("pooled.json gravado")

    # --- Gráficos ---
    _plot_vulnerable_by_stratum(per_prompt_df, plots_dir / "vulnerable_by_stratum.png")
    _plot_vulnerable_by_modality(per_prompt_df, plots_dir / "vulnerable_by_modality.png")

    # --- RERUN.md ---
    _write_rerun_md(run_dir, run_id)

    print(f"Métricas gravadas em {metrics_dir}")
    print(f"run_id={run_id}  k={K}  codeql_tag={codeql_image_tag}")
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------


def _run_selftest() -> int:
    """Executa o selftest com dados sintéticos e verifica as asserções.

    Cenário sintético:
    - 20 prompts, k=5, 2 arms, 2 modalities = 400 outcomes
    - Treatment: ``target_cwe_hit=True`` com prob. 0.2 (geralmente seguro)
    - Control: ``target_cwe_hit=True`` com prob. 0.8 (geralmente vulnerável)
    - Semente numpy fixa (42) para reprodutibilidade
    - ``parses=True, defines_symbol=True, imports_clean=True`` para todos

    Returns:
        0 se todas as asserções passarem, 1 caso contrário.
    """
    rng = np.random.default_rng(42)
    n_prompts = 20
    k = 5
    prompt_ids = [f"cwe078_{i}" for i in range(n_prompts)]
    strata_map = {pid: ("A" if i < 15 else ("B" if i < 19 else "C")) for i, pid in enumerate(prompt_ids)}

    codeql_rows: list[dict] = []
    func_rows: list[dict] = []

    for prompt_id in prompt_ids:
        for arm in ARMS:
            prob = 0.2 if arm == "treatment" else 0.8
            for modality in MODALITIES:
                for ki in range(k):
                    hit = bool(rng.random() < prob)
                    codeql_rows.append({
                        "prompt_id": prompt_id,
                        "arm": arm,
                        "modality": modality,
                        "k": ki,
                        "target_cwe_hit": hit,
                    })
                    func_rows.append({
                        "prompt_id": prompt_id,
                        "arm": arm,
                        "modality": modality,
                        "k": ki,
                        "parses": True,
                        "defines_symbol": True,
                        "imports_clean": True,
                    })

    # Dataset sintético (estrato e baseline)
    dataset = {
        pid: {
            "prompt_id": pid,
            "target_cwe": "CWE-78",
            "stratum": strata_map[pid],
            "baseline_target_cwe_hit": False,
        }
        for pid in prompt_ids
    }

    # --- Diretório de execução temporário ---
    with tempfile.TemporaryDirectory() as tmpdir:
        run_id = "selftest_run"
        runs_dir = Path(tmpdir) / "runs"
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True)

        # Gravar manifest sintético
        manifest = {
            "codeql_image_tag": "securecontext-codeql-eval:test",
            "model_id": "claude-selftest",
        }
        (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # Gravar arquivos de progresso CodeQL
        for modality in MODALITIES:
            for arm in ARMS:
                path = run_dir / f"codeql_progress_{modality}_{arm}.jsonl"
                lines = [
                    json.dumps(r)
                    for r in codeql_rows
                    if r["modality"] == modality and r["arm"] == arm
                ]
                path.write_text("\n".join(lines), encoding="utf-8")

        # Gravar functional_results.jsonl
        func_path = run_dir / "functional_results.jsonl"
        func_path.write_text(
            "\n".join(json.dumps(r) for r in func_rows),
            encoding="utf-8",
        )

        # --- Rodar pipeline ---
        # Precisamos passar o dataset sintético -> usamos uma versão modificada
        # de run_aggregate que aceita dataset diretamente.
        codeql_df = _build_codeql_df(codeql_rows)
        func_df = _build_functional_df(func_rows)
        per_prompt_df = _compute_atk_metrics(codeql_df, func_df, dataset)

        metrics_dir = run_dir / "metrics"
        metrics_dir.mkdir(exist_ok=True)
        plots_dir = metrics_dir / "plots"
        plots_dir.mkdir(exist_ok=True)

        # per_prompt.csv
        per_prompt_df.to_csv(metrics_dir / "per_prompt.csv", index=False)

        # per_stratum.csv
        stratum_rows: list[dict] = []
        for stratum in STRATA:
            for arm in ARMS:
                for modality in MODALITIES:
                    subset = per_prompt_df[
                        (per_prompt_df["stratum"] == stratum)
                        & (per_prompt_df["arm"] == arm)
                        & (per_prompt_df["modality"] == modality)
                    ]
                    m = _mean_metrics(subset)
                    stratum_rows.append({"stratum": stratum, "arm": arm, "modality": modality, **m})
        per_stratum_df = pd.DataFrame(stratum_rows)
        per_stratum_df.to_csv(metrics_dir / "per_stratum.csv", index=False)

        # pooled.json
        metrics_by_group: dict = {}
        for modality in MODALITIES:
            metrics_by_group[modality] = {}
            for arm in ARMS:
                subset = per_prompt_df[
                    (per_prompt_df["arm"] == arm) & (per_prompt_df["modality"] == modality)
                ]
                metrics_by_group[modality][arm] = _mean_metrics(subset)
        metrics_by_group["pooled"] = {}
        for arm in ARMS:
            metrics_by_group["pooled"][arm] = _mean_metrics(per_prompt_df[per_prompt_df["arm"] == arm])

        mcnemar_results: dict = {}
        for modality in MODALITIES:
            mcnemar_results[modality] = _mcnemar_exact(per_prompt_df, modality)

        logit_result = _logistic_regression(codeql_df)
        strata_result = _stratified_analysis(per_prompt_df)

        pooled = {
            "codeql_image_tag": "securecontext-codeql-eval:test",
            "model_id": "claude-selftest",
            "run_id": run_id,
            "k": K,
            "metrics": metrics_by_group,
            "mcnemar": mcnemar_results,
            "logistic_regression": logit_result,
            "strata": strata_result,
        }
        pooled_path = metrics_dir / "pooled.json"
        pooled_path.write_text(json.dumps(pooled, indent=2, ensure_ascii=False), encoding="utf-8")

        _plot_vulnerable_by_stratum(per_prompt_df, plots_dir / "vulnerable_by_stratum.png")
        _plot_vulnerable_by_modality(per_prompt_df, plots_dir / "vulnerable_by_modality.png")
        _write_rerun_md(run_dir, run_id)

        # --- Asserções ---
        failures: list[str] = []

        # 1. pooled.json foi gravado
        if not pooled_path.exists():
            failures.append("pooled.json não foi gravado")

        # 2. mcnemar["nl"]["p_value"] < 0.05
        nl_mc = mcnemar_results.get("nl", {})
        nl_p = nl_mc.get("p_value")
        if nl_p is None or nl_p >= 0.05:
            failures.append(
                f"mcnemar['nl']['p_value'] esperado < 0.05, obtido {nl_p}"
            )

        # 3. mcnemar["nl"]["risk_diff"] > 0
        nl_rd = nl_mc.get("risk_diff")
        if nl_rd is None or nl_rd <= 0:
            failures.append(
                f"mcnemar['nl']['risk_diff'] esperado > 0, obtido {nl_rd}"
            )

        # 4. per_prompt.csv tem 20 x 2 x 2 = 80 linhas
        n_rows = len(per_prompt_df)
        expected_rows = n_prompts * len(ARMS) * len(MODALITIES)
        if n_rows != expected_rows:
            failures.append(
                f"per_prompt.csv: esperado {expected_rows} linhas, obtido {n_rows}"
            )

        # 5. logistic_regression["arm"]["OR"] < 1
        # (tratamento reduz vulnerabilidade; arm=1=treatment -> OR < 1 para vuln.)
        lr = logit_result.get("arm", {})
        arm_or = lr.get("OR")
        if arm_or is None:
            failures.append("logistic_regression['arm']['OR'] não encontrado")
        elif arm_or >= 1.0:
            failures.append(
                f"logistic_regression['arm']['OR'] esperado < 1 (treatment reduz vuln.), obtido {arm_or:.4f}"
            )

    if failures:
        for msg in failures:
            print(f"SELFTEST FAIL: {msg}")
        return 1

    print("SELFTEST PASS")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parseia os argumentos da linha de comando.

    Args:
        argv: Lista de argumentos (``None`` usa ``sys.argv``).

    Returns:
        Namespace com os argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--run-id",
        metavar="ID",
        help="Identificador da execução a agregar.",
    )
    mode_group.add_argument(
        "--selftest",
        action="store_true",
        help="Executa o selftest com dados sintéticos e termina.",
    )

    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=DEFAULT_RUNS_DIR,
        metavar="PATH",
        help=f"Diretório raiz das execuções (padrão: {DEFAULT_RUNS_DIR}).",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        metavar="PATH",
        help=f"Dataset tratado (padrão: {DEFAULT_DATASET}).",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada principal.

    Args:
        argv: Argumentos da linha de comando (``None`` usa ``sys.argv``).

    Returns:
        Código de saída.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    args = _parse_args(argv)

    if args.selftest:
        return _run_selftest()

    return run_aggregate(
        run_id=args.run_id,
        runs_dir=args.runs_dir,
        dataset_path=args.dataset,
    )


if __name__ == "__main__":
    sys.exit(main())
