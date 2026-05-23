#!/usr/bin/env python3
"""Validate Step 261 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step261_RH_attack_foreclosure_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step261_results_summary.md",
    "step261_schema.json",
    "content_classification_step261.csv",
    "nonclaim_boundary_step261.md",
    "step261_RH_attack_foreclosure.tex",
    "analyze_internal_moves_step261.py",
    "run_step261_checks.py",
    "foreclosure_conjecture_step261.csv",
    "three_foreclosed_moves_step261.csv",
    "internal_moves_audit_step261.csv",
    "what_is_not_foreclosed_step261.csv",
    "findings_coverage_step261.csv",
    "corpus_inclusion_step261.csv",
    "residual_tree_step261.csv",
    "route_status_step261.csv",
    "construction_tasks_step261.csv",
    "classical_theorems_cited_step261.csv",
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

    schema = json.loads((ART / "step261_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 261:
        return fail("schema step mismatch")
    if schema.get("orientation") != "meta":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_RH_attack_foreclosure_well_typed":
        return fail("unexpected verdict")
    if len(schema.get("three_foreclosed_moves", [])) != 3:
        return fail("expected three foreclosed moves")
    if "RH proof in general" not in schema.get("what_is_not_foreclosed", []):
        return fail("nonforeclosure of RH proof missing")
    if len(schema.get("framework_findings_coverage", [])) != 9:
        return fail("expected nine findings in coverage")

    moves = rows("three_foreclosed_moves_step261.csv")
    move_names = {row["move"] for row in moves}
    for expected in ["carrier pivoting", "bridge import", "cascade-internal computation"]:
        if expected not in move_names:
            return fail("missing move " + expected)

    internal = rows("internal_moves_audit_step261.csv")
    if not any(row["coverage_status"] == "not_foreclosed" and "fresh typed" in row["candidate_move"] for row in internal):
        return fail("fresh typed mechanism escape hatch missing")

    not_foreclosed = rows("what_is_not_foreclosed_step261.csv")
    if not any(row["item"] == "RH proof in general" for row in not_foreclosed):
        return fail("RH proof nonforeclosure row missing")

    coverage = rows("findings_coverage_step261.csv")
    if len(coverage) != 9:
        return fail("coverage CSV should have nine findings")
    joined = " ".join(row["finding"] for row in coverage)
    for token in ["CTMT", "CRCFT", "Bridge", "Zero-Density"]:
        if token not in joined:
            return fail("missing coverage token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "RH Attack Foreclosure Conjecture" not in findings:
        return fail("findings_framework missing RH Attack Foreclosure entry")
    if "candidate (meta-theorem; corpus-pending" not in findings:
        return fail("findings_framework missing corpus-pending meta status")

    print("PASS step261 artifact contract")
    print("verdict=V_RH_attack_foreclosure_well_typed")
    print("meta_theorem=RH Attack Foreclosure Conjecture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
