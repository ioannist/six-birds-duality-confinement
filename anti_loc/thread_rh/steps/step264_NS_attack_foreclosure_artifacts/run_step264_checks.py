#!/usr/bin/env python3
"""Validate Step 264 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step264_NS_attack_foreclosure_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step264_results_summary.md",
    "step264_schema.json",
    "content_classification_step264.csv",
    "nonclaim_boundary_step264.md",
    "step264_NS_attack_foreclosure.tex",
    "analyze_NS_internal_moves_step264.py",
    "run_step264_checks.py",
    "NS_foreclosure_conjecture_step264.csv",
    "NS_three_moves_step264.csv",
    "NS_internal_moves_audit_step264.csv",
    "what_is_not_foreclosed_NS_step264.csv",
    "four_track_replication_step264.csv",
    "corpus_inclusion_step264.csv",
    "residual_tree_step264.csv",
    "route_status_step264.csv",
    "construction_tasks_step264.csv",
    "classical_theorems_cited_step264.csv",
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

    schema = json.loads((ART / "step264_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 264:
        return fail("schema step mismatch")
    if schema.get("orientation") != "meta_cross_track":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_NS_attack_foreclosure_replicated":
        return fail("unexpected verdict")
    if len(schema.get("three_foreclosed_moves_NS", [])) != 3:
        return fail("expected three NS foreclosed moves")
    if schema["four_track_replication"]["status"] != "verified-on-4-tracks: RH, BSD, Hodge, NS":
        return fail("four-track status mismatch")
    if "NS proof or disproof in general" not in schema.get("what_is_not_foreclosed_NS", []):
        return fail("NS proof/disproof nonforeclosure missing")

    moves = rows("NS_three_moves_step264.csv")
    move_names = {row["move"] for row in moves}
    for expected in ["carrier pivoting", "bridge import", "cascade-internal computation"]:
        if expected not in move_names:
            return fail("missing move " + expected)

    audit = rows("NS_internal_moves_audit_step264.csv")
    if not any(row["coverage_status"] == "not_foreclosed" for row in audit):
        return fail("fresh mechanism escape hatch missing")
    if not any("Tao" in row["NS_specific_move"] for row in audit):
        return fail("Tao averaged NS audit row missing")

    replication = rows("four_track_replication_step264.csv")
    if {row["track"] for row in replication} != {"RH", "BSD", "Hodge", "NS"}:
        return fail("four-track replication rows mismatch")

    sources = rows("classical_theorems_cited_step264.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Leray", "Caffarelli", "Beale", "Tao", "Buckmaster"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Attack Foreclosure Conjecture" not in findings:
        return fail("findings_framework missing Attack Foreclosure entry")
    if "verified-on-4-tracks: RH, BSD, Hodge, NS" not in findings:
        return fail("findings_framework missing four-track status")

    print("PASS step264 artifact contract")
    print("verdict=V_NS_attack_foreclosure_replicated")
    print("meta_theorem_status=verified-on-4-tracks: RH, BSD, Hodge, NS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
