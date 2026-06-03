#!/usr/bin/env python3
"""
Assemble an enriched prompt for secure code generation.

Takes a user's coding task description, retrieves relevant CWE security
knowledge via c_know's RAG (mitigations + secure-code examples), and prints
a structured block: security context + original task + generation instructions.

The agent invoking this skill is expected to read the output and produce code
that follows the embedded guidance.

Usage:
    assemble.py --prompt "<coding task description>"

Optional:
    --top-k N           number of CWE chunks to retrieve (default 3)
    --max-chars N       budget for security context (default 1500)
"""

import argparse
import logging
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from components.c_know import SecurityKnowledge  # noqa: E402


ENRICHED_TEMPLATE = """\
=== SecureContext-enriched prompt ===

{security_context}

## Task

{prompt}

## Instructions

Generate Python code for the task above. Apply the security guidance from the
CWE knowledge in the security context. Output only the code (no commentary, no
markdown fences) so it can be saved directly to a `.py` file.
"""


def main():
    logging.disable(logging.CRITICAL)

    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True, help="Coding task description")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--max-chars", type=int, default=2000)
    args = p.parse_args()

    c_know = SecurityKnowledge()
    security_context = c_know.retrieve_for_prompt(
        args.prompt,
        top_k=args.top_k,
        include_types=["mitigation", "example_secure"],
        max_chars=args.max_chars,
    )

    if not security_context.strip():
        security_context = (
            "## Security Knowledge (retrieved by c_know)\n"
            "_No specific CWE patterns matched this task; apply general "
            "secure-coding hygiene._"
        )

    print(ENRICHED_TEMPLATE.format(
        security_context=security_context.rstrip(),
        prompt=args.prompt,
    ))


if __name__ == "__main__":
    main()
