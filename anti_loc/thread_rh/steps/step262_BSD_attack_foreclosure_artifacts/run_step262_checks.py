#!/usr/bin/env python3
"""Validate Step 262 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step262_BSD_attack_foreclosure_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step262_results_summary.md",
    "step262_schema.json",
    "content_classification_step262.csv",
    "nonclaim_boundary_step262.md",
    "step262_BSD_attack_foreclosure.tex",
    "analyze_BSD_internal_moves_step262.py",
    "run_step262_checks.py",
    "BSD_foreclosure_conjecture_step262.csv",
    "BSD_three_moves_step262.csv",
    "BSD_internal_moves_audit_step262.csv",
    "what_is_not_foreclosed_BSD_step262.csv",
    "two_track_replication_step262.csv",
    "corpus_inclusion_step262.csv",
    "residual_tree_step262.csv",
    "route_status_step262.csv",
    "construction_tasks_step262.csv",
    "classical_theorems_cited_step262.csv",
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

    schema = json.loads((ART / "step262_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 262:
        return fail("schema step mismatch")
    if schema.get("orientation") != "meta_cross_track":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_BSD_attack_foreclosure_replicated":
        return fail("unexpected verdict")
    if len(schema.get("three_foreclosed_moves_BSD", [])) != 3:
        return fail("expected three BSD foreclosed moves")
    if schema["two_track_replication"]["status"] != "verified-on-2-tracks: RH, BSD":
        return fail("two-track status mismatch")
    if "BSD proof in general" not in schema.get("what_is_not_foreclosed_BSD", []):
        return fail("BSD proof nonforeclosure missing")

    moves = rows("BSD_three_moves_step262.csv")
    move_names = {row["move"] for row in moves}
    for expected in ["carrier pivoting", "bridge import", "cascade-internal computation"]:
        if expected not in move_names:
            return fail("missing move " + expected)

    audit = rows("BSD_internal_moves_audit_step262.csv")
    if not any(row["coverage_status"] == "not_foreclosed" for row in audit):
        return fail("fresh mechanism escape hatch missing")
    if not any("Heegner" in row["BSD_specific_move"] for row in audit):
        return fail("Heegner/GZ/Kolyvagin audit row missing")

    replication = rows("two_track_replication_step262.csv")
    if {row["track"] for row in replication} != {"RH", "BSD"}:
        return fail("two-track replication rows mismatch")

    sources = rows("classical_theorems_cited_step262.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Bloch", "Burns", "Kato", "Skinner", "Gross", "Kolyvagin"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Attack Foreclosure Conjecture" not in findings:
        return fail("findings_framework missing Attack Foreclosure entry")
    if "verified-on-2-tracks: RH, BSD" not in findings:
        return fail("findings_framework missing two-track status")

    print("PASS step262 artifact contract")
    print("verdict=V_BSD_attack_foreclosure_replicated")
    print("meta_theorem_status=verified-on-2-tracks: RH, BSD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
