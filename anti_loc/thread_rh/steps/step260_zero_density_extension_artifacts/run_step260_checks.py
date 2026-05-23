#!/usr/bin/env python3
"""Validate Step 260 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step260_zero_density_extension_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step260_results_summary.md",
    "step260_schema.json",
    "content_classification_step260.csv",
    "nonclaim_boundary_step260.md",
    "step260_zero_density_extension.tex",
    "derive_zero_density_step260.py",
    "run_step260_checks.py",
    "density_declaration_step260.csv",
    "density_extension_step260.csv",
    "instance_evidence_step260.csv",
    "corpus_inclusion_step260.csv",
    "residual_tree_step260.csv",
    "route_status_step260.csv",
    "construction_tasks_step260.csv",
    "classical_theorems_cited_step260.csv",
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

    schema = json.loads((ART / "step260_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 260:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_zero_density_extension_9th_finding":
        return fail("unexpected verdict")
    if "N_L(sigma,T)" not in schema["density_carrier_definition"]["zero_count"]:
        return fail("zero-count definition missing")
    if len(schema.get("three_instance_evidence", [])) != 3:
        return fail("expected three evidence instances")

    density = rows("density_declaration_step260.csv")
    if not density or "Xi_density" not in density[0]["residual"]:
        return fail("density residual missing")

    extension = rows("density_extension_step260.csv")
    if not any(row["verdict"] == "V_zero_density_extension_9th_finding" for row in extension):
        return fail("extension verdict row missing")

    evidence = rows("instance_evidence_step260.csv")
    if len(evidence) != 3:
        return fail("expected exactly three evidence rows")
    joined_evidence = " ".join(row["instance"] + " " + row["object"] for row in evidence)
    for token in ["zeta", "Dirichlet", "automorphic"]:
        if token not in joined_evidence:
            return fail("missing evidence token " + token)

    sources = rows("classical_theorems_cited_step260.csv")
    joined_sources = " ".join(row["source"] for row in sources)
    for token in ["Selberg", "Bombieri", "Huxley", "Halasz", "Vinogradov"]:
        if token not in joined_sources:
            return fail("missing source token " + token)

    findings = FINDINGS.read_text(encoding="utf-8")
    if "Selberg-Class Zero-Density Extension" not in findings:
        return fail("findings_framework missing zero-density entry")
    if "verified-on-3-density-instances" not in findings:
        return fail("findings_framework missing 3-density status")

    print("PASS step260 artifact contract")
    print("verdict=V_zero_density_extension_9th_finding")
    print("framework_entry=Selberg-Class Zero-Density Extension")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
