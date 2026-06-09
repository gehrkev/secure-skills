#!/usr/bin/env bash
# Constrói (idempotente) o venv com as dependências pinned do SALLM usado pela
# checagem `imports_clean` em functional.py. Roda uma vez por checkout.
#
#   bash eval/runner/eval/setup_env.sh
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/functional_venv"
REQ="$HERE/functional_requirements.txt"

if [[ ! -d "$VENV" ]]; then
  echo "[setup_env] criando venv em $VENV"
  python3 -m venv "$VENV"
fi

echo "[setup_env] instalando dependências pinned do SALLM"
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet -r "$REQ"

echo "[setup_env] ok — interpretador: $VENV/bin/python"
"$VENV/bin/python" -c "import flask, flask_sqlalchemy, Crypto; print('[setup_env] imports de sanidade ok')"
