#!/usr/bin/env python3
"""Validate Step 256 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step256_montgomery_pair_correlation_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step256_results_summary.md",
    "step256_schema.json",
    "content_classification_step256.csv",
    "nonclaim_boundary_step256.md",
    "step256_montgomery_pair_correlation.tex",
    "derive_pair_correlation_step256.py",
    "run_step256_checks.py",
    "mpc_declaration_step256.csv",
    "extension_classification_step256.csv",
    "subtype_refinement_step256.csv",
    "instance_evidence_step256.csv",
    "corpus_inclusion_step256.csv",
    "residual_tree_step256.csv",
    "route_status_step256.csv",
    "construction_tasks_step256.csv",
    "classical_theorems_cited_step256.csv",
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

    schema = json.loads((ART / "step256_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 256:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_montgomery_subtype_refinement":
        return fail("unexpected verdict")
    if "Type_Ib" not in schema.get("refinement_call", {}):
        return fail("Type Ib refinement missing")

    subtypes = rows("subtype_refinement_step256.csv")
    names = {r["subtype"] for r in subtypes}
    if names != {"Type Ia", "Type Ib", "Type II"}:
        return fail(f"subtype set mismatch: {names}")

    evidence = rows("instance_evidence_step256.csv")
    if len(evidence) != 3:
        return fail("expected three evidence instances")
    if not any("Montgomery" in r["instance"] and r["subtype"] == "Type Ib" for r in evidence):
        return fail("Montgomery Type Ib evidence missing")

    sources = rows("classical_theorems_cited_step256.csv")
    joined = " ".join(r["source"] for r in sources)
    for token in ["Montgomery", "Odlyzko", "Hejhal", "Rudnick", "Sarnak"]:
        if token not in joined:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "verified-on-3-Selberg-instances" not in findings:
        return fail("findings_framework.md not updated to 3 instances")
    if "Type Ib" not in findings:
        return fail("findings_framework.md missing subtype refinement")

    print("PASS step256 artifact contract")
    print("verdict=V_montgomery_subtype_refinement")
    print("cross_correlation_extension=verified_on_3_Selberg_instances_subtype_refined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
