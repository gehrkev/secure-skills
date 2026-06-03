---
description: >-
  Inject CWE security context into Python code-generation tasks. Auto-invoke
  on ANY request to write Python that touches a common vulnerability surface:
  OS commands / subprocess / shell calls; SQL queries; file paths or filenames
  from user input; deserialization (pickle, yaml.load, marshal); HTTP request
  handling that accepts untrusted input; web template rendering; authentication
  flows; hashing or cryptography. The skill's purpose is to harden naive
  prompts by default — fire even when the user did NOT say "secure", "safe",
  or "hardened". Do not skip just because the user didn't ask for security;
  the framework's value is exactly in those cases. The sister skill
  `codeql-eval` runs static analysis on the generated code via CodeQL
  queries (CWE-mapped findings); surface it as a follow-up step after
  generating. This is the SecureContext framework's c_know component.
allowed-tools: Bash(python3 *) Bash(bash *)
---

# secure

Enriches a coding task with relevant security knowledge from a local
vector store over MITRE View 1003 ∪ View 1435 (NVD's CVE-mapping
weaknesses ∪ the 2025 CWE Top 25, 133 CWEs total), then asks the agent
to generate code that applies the retrieved guidance.

**Scope (MVP):** Only the `c_know` component (RAG over CWE chunks) is wired up.
The other framework components (`c_instr`, `c_mem`) are placeholders.

## Preconditions

The skill ships its own framework copy and creates its own venv. Run the
bootstrap once, in a fresh checkout:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/bootstrap.sh
```

What it does:

1. Creates `.venv/` inside the skill directory.
2. Installs `chromadb` + `requests` (transitively pulls onnxruntime,
   tokenizers, numpy, pydantic). First run: ~2–4 min.
3. Builds the CWE knowledge base (default source: `m3` = View 1003 ∪
   Top 25, 133 CWEs / ~2250 chunks): downloads the MITRE XMLs, parses,
   chunks (9 types per CWE), embeds via `all-MiniLM-L6-v2`, persists into
   `knowledge_base/store/chroma_db/`. First run: ~60–180s.

Re-running `bootstrap.sh` is idempotent: it skips venv creation if present and
skips KB rebuild if chroma_db is non-empty. Pass `--reset` to force a rebuild.

The bootstrap requires Python 3.10+, network access (for pip + the CWE XML
download), and ~500 MB of disk for the venv and embeddings.

## How to invoke

```bash
${CLAUDE_SKILL_DIR}/.venv/bin/python ${CLAUDE_SKILL_DIR}/scripts/assemble.py \
    --prompt "<the user's coding task in natural language>"
```

The script prints an "enriched prompt" block to stdout:

```
=== SecureContext-enriched prompt ===

## Security Knowledge (retrieved by c_know)
...
### CWE-XX: Name
**[mitigation]**
...
**[example_secure]**
...

## Task
<the user's prompt>

## Instructions
Generate Python code ...
```

After running it: **read the enriched output, then generate and save the
Python code that satisfies the task while applying the retrieved guidance.**
Output the code only, no markdown fences, no explanation in the saved file,
so it can be evaluated directly.

## After generating: mention the sister skill `codeql-eval`

After saving the generated code, **surface to the user that the `codeql-eval`
skill exists** and can run CodeQL static analysis on the result, reporting any
CWE-mapped findings. Don't run it without being asked, but mention it as a
natural next step. Suggested phrasing along the lines of:

> "Saved to `<path>`. The `codeql-eval` skill can run CodeQL static analysis
> on this file and report any CWE-mapped findings. Want me to run it?"

Why surface it: the user may not know the eval skill is available unless
prompted, and static analysis is a cheap way to confirm the retrieved
guidance actually landed in the generated code. Don't auto-run; ask first.

Typical chain when the user agrees:

1. Generate code from the enriched prompt and save it.
2. Invoke `codeql-eval --code <path>` (optionally `--cwe <target>` if the
   target CWE is known).
3. Read the JSON output and summarize findings to the user.

## What this skill is NOT

- Not a `c_instr` or `c_mem` implementation — those framework components are
  placeholders in this MVP. Only `c_know` (RAG) drives the enrichment.
- Not an external-LLM gateway. The enrichment script prints the prompt; the
  agent itself produces the code. For experiments that compare specific
  models (Claude vs GPT vs Gemini) you need a separate runner outside this
  skill.
- Not a security validator. It guides generation; it does not verify the
  result. Use `codeql-eval` to validate.

## Layout

```
.claude/skills/secure/
├── SKILL.md                          (this file)
├── requirements.txt                  (chromadb, requests)
├── components/
│   └── c_know.py                     (SecurityKnowledge class — RAG retrieval)
├── knowledge_base/
│   ├── build_knowledge_base.py       (KB orchestrator)
│   ├── pipelines/                    (downloader, parser, chunker)
│   └── store/
│       ├── vector_store.py           (ChromaDB wrapper)
│       └── chroma_db/                (populated after bootstrap)
├── scripts/
│   ├── bootstrap.sh                  (venv + deps + KB build)
│   └── assemble.py                   (prompt → enriched output)
└── .venv/                            (created by bootstrap)
```
