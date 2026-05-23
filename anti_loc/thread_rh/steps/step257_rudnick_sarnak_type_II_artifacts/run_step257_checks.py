#!/usr/bin/env python3
"""Validate Step 257 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step257_rudnick_sarnak_type_II_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step257_results_summary.md",
    "step257_schema.json",
    "content_classification_step257.csv",
    "nonclaim_boundary_step257.md",
    "step257_rudnick_sarnak_type_II.tex",
    "derive_n_level_correlation_step257.py",
    "run_step257_checks.py",
    "rs_declaration_step257.csv",
    "type_II_classification_step257.csv",
    "subtype_matrix_step257.csv",
    "instance_evidence_step257.csv",
    "corpus_inclusion_step257.csv",
    "residual_tree_step257.csv",
    "route_status_step257.csv",
    "construction_tasks_step257.csv",
    "classical_theorems_cited_step257.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(msg: str) -> int:
    print("FAIL", msg)
    return 1


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        return fail("missing files: " + ", ".join(missing))

    schema = json.loads((ART / "step257_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 257:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_rudnick_sarnak_type_II_instance":
        return fail("unexpected verdict")
    if "Type_II" not in schema.get("subtype_matrix_completion", {}):
        return fail("Type II missing from schema")

    matrix = rows("subtype_matrix_step257.csv")
    counts = {r["subtype"]: r["count"] for r in matrix}
    if counts.get("Type Ia") != "2" or counts.get("Type Ib") != "1" or counts.get("Type II") != "1":
        return fail(f"unexpected subtype counts: {counts}")

    evidence = rows("instance_evidence_step257.csv")
    if len(evidence) != 4:
        return fail("expected four evidence instances")
    if not any("Rudnick" in r["instance"] and r["subtype"] == "Type II" for r in evidence):
        return fail("Rudnick-Sarnak Type II evidence missing")

    sources = rows("classical_theorems_cited_step257.csv")
    joined = " ".join(r["source"] for r in sources)
    for token in ["Rudnick", "Sarnak", "Katz", "Iwaniec", "Luo"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "verified-on-4-Selberg-instances" not in findings:
        return fail("findings_framework.md not updated to 4 instances")
    if "all-three-subtypes-covered" not in findings:
        return fail("findings_framework.md missing all-subtypes status")

    print("PASS step257 artifact contract")
    print("verdict=V_rudnick_sarnak_type_II_instance")
    print("cross_correlation_extension=verified_on_4_instances_all_three_subtypes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
