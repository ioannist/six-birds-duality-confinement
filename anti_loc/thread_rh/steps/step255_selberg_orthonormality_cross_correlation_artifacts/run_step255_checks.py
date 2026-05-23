#!/usr/bin/env python3
"""Validate Step 255 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step255_selberg_orthonormality_cross_correlation_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step255_results_summary.md",
    "step255_schema.json",
    "content_classification_step255.csv",
    "nonclaim_boundary_step255.md",
    "step255_selberg_orthonormality_cross_correlation.tex",
    "derive_orthonormality_step255.py",
    "run_step255_checks.py",
    "orthonormality_declaration_step255.csv",
    "cross_correlation_extension_step255.csv",
    "instance_evidence_step255.csv",
    "corpus_inclusion_step255.csv",
    "residual_tree_step255.csv",
    "route_status_step255.csv",
    "construction_tasks_step255.csv",
    "classical_theorems_cited_step255.csv",
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

    schema = json.loads((ART / "step255_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 255:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_selberg_orthonormality_cross_correlation_typed":
        return fail("unexpected verdict")
    note = schema["orthonormality_carrier_definition"]["normalization_note"]
    if "not the pole order" not in note:
        return fail("normalization correction missing")

    evidence = rows("instance_evidence_step255.csv")
    if len(evidence) != 2:
        return fail("expected exactly two evidence instances")
    if not any("SOC" in r["instance"] for r in evidence):
        return fail("SOC evidence missing")
    if not any("diagonal" in r["instance"] for r in evidence):
        return fail("diagonal evidence missing")

    extension = rows("cross_correlation_extension_step255.csv")
    if not extension or "candidate" not in extension[0]["status"]:
        return fail("extension candidate status missing")

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Selberg-Class Cross-Correlation Extension" not in findings:
        return fail("findings_framework.md missing deposited finding")

    sources = rows("classical_theorems_cited_step255.csv")
    joined = " ".join(r["source"] for r in sources)
    for token in ["Selberg", "Conrey", "Liu", "Kaczorowski"]:
        if token not in joined:
            return fail("missing source token " + token)

    print("PASS step255 artifact contract")
    print("verdict=V_selberg_orthonormality_cross_correlation_typed")
    print("finding_deposited=anti_loc/findings_framework.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
