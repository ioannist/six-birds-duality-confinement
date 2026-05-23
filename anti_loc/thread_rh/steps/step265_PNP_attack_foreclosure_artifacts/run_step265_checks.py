#!/usr/bin/env python3
"""Validate Step 265 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step265_PNP_attack_foreclosure_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step265_results_summary.md",
    "step265_schema.json",
    "content_classification_step265.csv",
    "nonclaim_boundary_step265.md",
    "step265_PNP_attack_foreclosure.tex",
    "analyze_PNP_internal_moves_step265.py",
    "run_step265_checks.py",
    "PNP_foreclosure_conjecture_step265.csv",
    "PNP_three_moves_step265.csv",
    "PNP_internal_moves_audit_step265.csv",
    "what_is_not_foreclosed_PNP_step265.csv",
    "five_track_replication_step265.csv",
    "corpus_inclusion_step265.csv",
    "residual_tree_step265.csv",
    "route_status_step265.csv",
    "construction_tasks_step265.csv",
    "classical_theorems_cited_step265.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(message: str) -> int:
    print("FAIL", message)
    return 1


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        return fail("missing files: " + ", ".join(missing))

    schema = json.loads((ART / "step265_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 265:
        return fail("schema step mismatch")
    if schema.get("orientation") != "meta_cross_track":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_PNP_attack_foreclosure_replicated":
        return fail("unexpected verdict")
    if len(schema.get("three_foreclosed_moves_PNP", [])) != 3:
        return fail("expected three PNP foreclosed moves")
    expected_status = "verified-on-5-tracks: RH, BSD, Hodge, NS, P-vs-NP"
    if schema["five_track_replication"]["status"] != expected_status:
        return fail("five-track status mismatch")
    if "P-vs-NP proof in either direction" not in schema.get("what_is_not_foreclosed_PNP", []):
        return fail("P-vs-NP nonforeclosure missing")

    moves = rows("PNP_three_moves_step265.csv")
    move_names = {row["move"] for row in moves}
    for expected in ["carrier pivoting", "bridge import", "cascade-internal computation"]:
        if expected not in move_names:
            return fail("missing move " + expected)

    audit = rows("PNP_internal_moves_audit_step265.csv")
    if not any(row["coverage_status"] == "not_foreclosed" for row in audit):
        return fail("fresh mechanism escape hatch missing")
    if not any("diagonalization" in row["PNP_specific_move"] for row in audit):
        return fail("diagonalization audit row missing")
    if not any("GCT" in row["PNP_specific_move"] for row in audit):
        return fail("GCT audit row missing")

    replication = rows("five_track_replication_step265.csv")
    if {row["track"] for row in replication} != {"RH", "BSD", "Hodge", "NS", "P-vs-NP"}:
        return fail("five-track replication rows mismatch")

    sources = rows("classical_theorems_cited_step265.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Cook", "Karp", "Baker", "Razborov", "Aaronson", "Williams", "Mulmuley"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Attack Foreclosure Conjecture" not in findings:
        return fail("findings_framework missing Attack Foreclosure entry")
    if expected_status not in findings:
        return fail("findings_framework missing five-track status")
    if "P-vs-NP replication (step 265)" not in findings:
        return fail("findings_framework missing P-vs-NP replication")

    print("PASS step265 artifact contract")
    print("verdict=V_PNP_attack_foreclosure_replicated")
    print("meta_theorem_status=" + expected_status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
