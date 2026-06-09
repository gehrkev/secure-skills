#!/usr/bin/env python3
"""
CodeQL single-file evaluator.

Runs static security analysis on ONE Python file via the CodeQL
security-extended query suite inside the prebuilt CodeQL image, then emits a
JSON summary of CWE-mapped findings to stdout.

Usage:
    run_eval.py --code <path> [--cwe CWE-XX] [--suite <suite>] [--image <tag>]

Build the image once with scripts/bootstrap.sh before running.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = "securecontext-codeql-eval:2.25.4"
CODEQL = "/opt/codeql/codeql"  # absolute path inside the image
DEFAULT_SUITE = "codeql/python-queries:codeql-suites/python-security-extended.qls"

CWE_TAG_RE = re.compile(r"external/cwe/cwe-(\d+)$")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def ensure_image(image):
    if run(["docker", "image", "inspect", image]).returncode != 0:
        sys.exit(
            f"Docker image '{image}' not found. Build it first:\n"
            f"  bash {SKILL_DIR / 'scripts' / 'bootstrap.sh'}"
        )


def normalize_cwe(num_str):
    """'089' -> 'CWE-89'."""
    return f"CWE-{int(num_str)}"


def normalize_cwe_arg(value):
    """Accept 'CWE-78', 'cwe-78', '78' -> 'CWE-78'."""
    m = re.search(r"(\d+)", value)
    if not m:
        sys.exit(f"Could not parse a CWE number from --cwe '{value}'")
    return normalize_cwe(m.group(1))


def parse_sarif(sarif_path):
    """Return a list of {cwe, line, rule_id, message} findings."""
    data = json.loads(sarif_path.read_text())
    findings = []
    for run_obj in data.get("runs", []):
        rule_cwes = {}
        driver = run_obj.get("tool", {}).get("driver", {})
        for rule in driver.get("rules", []):
            rid = rule.get("id")
            tags = rule.get("properties", {}).get("tags", []) or []
            cwes = []
            for tag in tags:
                m = CWE_TAG_RE.match(tag)
                if m:
                    cwes.append(normalize_cwe(m.group(1)))
            if rid is not None:
                rule_cwes[rid] = sorted(set(cwes))

        for result in run_obj.get("results", []):
            rid = result.get("ruleId")
            cwes = rule_cwes.get(rid, [])
            message = result.get("message", {}).get("text", "")
            line = None
            locations = result.get("locations", [])
            if locations:
                region = locations[0].get("physicalLocation", {}).get("region", {})
                line = region.get("startLine")
            if not cwes:
                findings.append(
                    {"cwe": None, "line": line, "rule_id": rid, "message": message}
                )
                continue
            for cwe in cwes:
                findings.append(
                    {"cwe": cwe, "line": line, "rule_id": rid, "message": message}
                )
    return findings


def analyze_in_container(image, code_path, suite, sarif_out):
    """Create a container, copy the candidate in, run CodeQL, copy the SARIF out."""
    inner = (
        f"{CODEQL} database create /work/db --language=python "
        f"--source-root /work/src --quiet && "
        f"{CODEQL} database analyze /work/db {suite} "
        f"--format=sarif-latest --output /work/results.sarif --quiet"
    )
    create = run(["docker", "create", "--platform=linux/amd64", image, "sh", "-c", inner])
    if create.returncode != 0:
        sys.exit("docker create failed:\n" + create.stderr)
    cid = create.stdout.strip()
    try:
        cp_in = run(["docker", "cp", str(code_path), f"{cid}:/work/src/{code_path.name}"])
        if cp_in.returncode != 0:
            sys.exit("Could not copy the candidate into the container:\n" + cp_in.stderr)

        started = run(["docker", "start", "-a", cid])
        if started.returncode != 0:
            detail = started.stderr or started.stdout
            sys.exit("CodeQL analysis failed:\n" + detail)

        cp_out = run(["docker", "cp", f"{cid}:/work/results.sarif", str(sarif_out)])
        if cp_out.returncode != 0 or not sarif_out.is_file():
            sys.exit("Could not copy the SARIF report out of the container:\n" + cp_out.stderr)
    finally:
        run(["docker", "rm", "-f", cid])


def main():
    p = argparse.ArgumentParser(description="CodeQL single-file security eval")
    p.add_argument("--code", required=True, help="Path to candidate Python file")
    p.add_argument("--cwe", default=None, help="Target CWE id, e.g. CWE-78")
    p.add_argument("--suite", default=DEFAULT_SUITE, help="CodeQL query suite")
    p.add_argument("--image", default=DEFAULT_IMAGE, help="CodeQL image tag")
    args = p.parse_args()

    ensure_image(args.image)

    code_path = Path(args.code).resolve()
    if not code_path.is_file():
        sys.exit(f"Code file not found: {code_path}")
    if code_path.suffix != ".py":
        sys.exit(f"Expected a .py file, got: {code_path}")

    target_cwe = normalize_cwe_arg(args.cwe) if args.cwe else None

    work_dir = Path(tempfile.mkdtemp(prefix="codeql-eval-"))
    sarif_path = work_dir / "results.sarif"
    analyze_in_container(args.image, code_path, args.suite, sarif_path)

    findings = parse_sarif(sarif_path)

    by_cwe = {}
    for f in findings:
        if f["cwe"] is None:
            continue
        by_cwe[f["cwe"]] = by_cwe.get(f["cwe"], 0) + 1

    target_cwe_hit = None
    if target_cwe is not None:
        target_cwe_hit = target_cwe in by_cwe

    summary = {
        "file": str(code_path),
        "target_cwe": target_cwe,
        "findings": findings,
        "summary": {
            "total_findings": len(findings),
            "by_cwe": by_cwe,
        },
        "target_cwe_hit": target_cwe_hit,
        "raw_sarif_path": str(sarif_path),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
