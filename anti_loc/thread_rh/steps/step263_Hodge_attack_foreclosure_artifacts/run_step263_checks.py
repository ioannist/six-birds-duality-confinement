#!/usr/bin/env python3
"""Validate Step 263 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step263_Hodge_attack_foreclosure_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step263_results_summary.md",
    "step263_schema.json",
    "content_classification_step263.csv",
    "nonclaim_boundary_step263.md",
    "step263_Hodge_attack_foreclosure.tex",
    "analyze_Hodge_internal_moves_step263.py",
    "run_step263_checks.py",
    "Hodge_foreclosure_conjecture_step263.csv",
    "Hodge_three_moves_step263.csv",
    "Hodge_internal_moves_audit_step263.csv",
    "what_is_not_foreclosed_Hodge_step263.csv",
    "three_track_replication_step263.csv",
    "corpus_inclusion_step263.csv",
    "residual_tree_step263.csv",
    "route_status_step263.csv",
    "construction_tasks_step263.csv",
    "classical_theorems_cited_step263.csv",
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

    schema = json.loads((ART / "step263_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 263:
        return fail("schema step mismatch")
    if schema.get("orientation") != "meta_cross_track":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_Hodge_attack_foreclosure_replicated":
        return fail("unexpected verdict")
    if len(schema.get("three_foreclosed_moves_Hodge", [])) != 3:
        return fail("expected three Hodge foreclosed moves")
    if schema["three_track_replication"]["status"] != "verified-on-3-tracks: RH, BSD, Hodge":
        return fail("three-track status mismatch")
    if "Hodge proof in general" not in schema.get("what_is_not_foreclosed_Hodge", []):
        return fail("Hodge proof nonforeclosure missing")

    moves = rows("Hodge_three_moves_step263.csv")
    move_names = {row["move"] for row in moves}
    for expected in ["carrier pivoting", "bridge import", "cascade-internal computation"]:
        if expected not in move_names:
            return fail("missing move " + expected)

    audit = rows("Hodge_internal_moves_audit_step263.csv")
    if not any(row["coverage_status"] == "not_foreclosed" for row in audit):
        return fail("fresh mechanism escape hatch missing")
    if not any("Mumford" in row["Hodge_specific_move"] for row in audit):
        return fail("Mumford-Tate audit row missing")

    replication = rows("three_track_replication_step263.csv")
    if {row["track"] for row in replication} != {"RH", "BSD", "Hodge"}:
        return fail("three-track replication rows mismatch")

    sources = rows("classical_theorems_cited_step263.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Lefschetz", "Hodge", "Deligne", "Voisin", "Cattani", "Charles"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Attack Foreclosure Conjecture" not in findings:
        return fail("findings_framework missing Attack Foreclosure entry")
    if "verified-on-3-tracks: RH, BSD, Hodge" not in findings:
        return fail("findings_framework missing three-track status")

    print("PASS step263 artifact contract")
    print("verdict=V_Hodge_attack_foreclosure_replicated")
    print("meta_theorem_status=verified-on-3-tracks: RH, BSD, Hodge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
