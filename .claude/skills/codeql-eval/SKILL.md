---
description: >-
  Run static security analysis on a Python file via CodeQL with the
  security-extended query suite. Use to validate generated Python code for
  CWE patterns (SQL injection, command injection, path traversal,
  deserialization, etc.) without executing the code. Output is JSON with
  per-finding CWE labels and line numbers. The sister skill `secure`
  generates code; this skill validates it. Auto-invoke after code is
  generated or whenever the user asks to audit a Python file for security.
allowed-tools: Bash(bash *) Bash(python3 *) Bash(docker *)
---

# codeql-eval

Runs CodeQL static analysis on a single Python file and reports CWE-mapped
findings as JSON. Purely static: it never executes the candidate code.

## Preconditions

Requires only **python3** and **docker** (a running daemon). Build the image
once, in a fresh checkout:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/bootstrap.sh
```

What it does:

1. Provisions an Ubuntu container with the version-pinned CodeQL bundle (which
   ships the standard `codeql/python-queries` pack).
2. Verifies the `python-queries` pack resolves.
3. Commits it to the `securecontext-codeql-eval:2.25.4` image.

Idempotent: re-running skips the build if the image already exists. The first
build downloads the bundle (~1.3 GB, producing a ~3.4 GB image) and takes a few
minutes; network access is required.

## How to invoke

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run_eval.py --code <path-to-file.py>
```

With a target CWE (lets a batch runner compute security@k / vulnerable@k
against a specific class):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run_eval.py --code <path-to-file.py> --cwe CWE-89
```

Options:

- `--code` (required): path to the candidate `.py` file.
- `--cwe` (optional): target CWE id (`CWE-78`, `cwe-78`, or `78` all work).
- `--suite` (optional): defaults to
  `codeql/python-queries:codeql-suites/python-security-extended.qls`.
- `--image` (optional): CodeQL image tag (defaults to
  `securecontext-codeql-eval:2.25.4`).

Requires the image (built by `bootstrap.sh`) and a running Docker daemon.

## Output

JSON to stdout:

```json
{
  "file": "<absolute path>",
  "target_cwe": "CWE-78",
  "findings": [
    {"cwe": "CWE-78", "line": 12, "rule_id": "py/command-line-injection", "message": "..."}
  ],
  "summary": {
    "total_findings": 3,
    "by_cwe": {"CWE-78": 2, "CWE-22": 1}
  },
  "target_cwe_hit": true,
  "raw_sarif_path": "/tmp/codeql-eval-XXXX/results.sarif"
}
```

`target_cwe` and `target_cwe_hit` are `null` when `--cwe` is not supplied. The
raw SARIF is kept on disk (path printed) so callers can inspect or archive it.

## Result interpretation

- `target_cwe_hit=true`: the candidate triggered at least one CodeQL finding
  mapped to the target CWE. This is the per-file signal a batch runner uses for
  `vulnerable@k` against that class.
- `target_cwe_hit=false`: no finding for the target CWE (other, unrelated
  findings may still be present, see `summary.by_cwe`).
- `total_findings > 0` counts ANY security finding, not just the target class.

## What this skill is NOT

- Not a behavioral / functional test. CodeQL is purely static; it does not run
  the code or check correctness.
- Not a fixer. It reports findings; it does not patch them.
- Not a generator. To generate hardened code, use the `secure` skill.

## Smoke test

Vulnerable sample (raw f-string SQL concatenation), expect `target_cwe_hit=true`:

```python
# /tmp/sample_sqli.py
from flask import Flask, request
import sqlite3
app = Flask(__name__)
@app.route('/lookup')
def lookup():
    q = request.args.get('q')
    conn = sqlite3.connect('x.db')
    return str(conn.execute("SELECT * FROM t WHERE name = '" + q + "'").fetchall())
```

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run_eval.py --code /tmp/sample_sqli.py --cwe CWE-89
```

Parameterized counterpart (`execute("... = ?", (q,))`) saved to
`/tmp/sample_safe.py` should yield `target_cwe_hit=false`.

## Layout

```
.claude/skills/codeql-eval/
├── SKILL.md                 (this file)
├── Dockerfile               (canonical image definition)
└── scripts/
    ├── bootstrap.sh         (builds the pinned CodeQL image)
    └── run_eval.py          (single-file analysis -> JSON)
```

The CodeQL toolchain lives in the `securecontext-codeql-eval` Docker image, not
in the repo tree.
