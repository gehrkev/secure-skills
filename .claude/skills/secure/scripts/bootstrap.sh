#!/usr/bin/env bash
# Self-contained bootstrap for the `secure` skill.
# Creates a local venv, installs deps, builds the CWE knowledge base.
# Idempotent: re-runs skip already-done steps unless --reset is passed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV="$SKILL_DIR/.venv"
PYBIN="$VENV/bin/python"
PIP="$VENV/bin/pip"
CHROMA="$SKILL_DIR/knowledge_base/store/chroma_db"

RESET=""
if [ "${1:-}" = "--reset" ]; then
	RESET="--reset"
fi

# 1. venv
if [ ! -x "$PYBIN" ]; then
	echo "[bootstrap] Creating venv at $VENV"
	python3 -m venv "$VENV"
else
	echo "[bootstrap] venv already present"
fi

# 2. deps (always run pip install; pip is fast when up-to-date)
echo "[bootstrap] Installing requirements (first run downloads onnxruntime + tokenizers, ~2–4 min)"
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet -r "$SKILL_DIR/requirements.txt"

# 3. KB build
if [ -d "$CHROMA" ] && [ -z "$RESET" ]; then
	# Quick non-empty check: any sqlite file inside
	if find "$CHROMA" -name "*.sqlite3" -size +1c | grep -q .; then
		echo "[bootstrap] Knowledge base already present at $CHROMA (pass --reset to rebuild)"
		exit 0
	fi
fi

echo "[bootstrap] Building CWE knowledge base (downloads View 1003 + Top 25 XML, embeds ~2250 chunks; ~60–180s first time)"
cd "$SKILL_DIR"
"$PYBIN" -m knowledge_base.build_knowledge_base $RESET

echo "[bootstrap] Done."
