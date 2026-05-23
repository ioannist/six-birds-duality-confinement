#!/usr/bin/env python3
"""Validate Step 206 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step206_transport_sampling_derivation_artifacts")
REQUIRED = [
    "step206_results_summary.md",
    "step206_schema.json",
    "content_classification_step206.csv",
    "nonclaim_boundary_step206.md",
    "step206_transport_sampling_derivation.tex",
    "derive_transport_sampling_step206.py",
    "compute_step206_output.txt",
    "run_step206_checks.py",
    "operator_chain_decoding_step206.csv",
    "assembled_chain_step206.csv",
    "boundary_identity_status_step206.csv",
    "residual_tree_step206.csv",
    "route_status_step206.csv",
    "construction_tasks_step206.csv",
    "classical_theorems_cited_step206.csv",
]
ALLOWED = {
    "V_transport_sampling_identity",
    "V_transport_sampling_corrected",
    "V_transport_sampling_external_required",
    "V_transport_sampling_partial",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL step206: {msg}")


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")
    schema = json.loads((BASE / "step206_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "chain_decoding",
        "assembled_chain_formula",
        "boundary_identity_status",
        "transport_sampling_verdict",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 206:
        fail("schema step must be 206")
    if schema["final_verdict"] not in ALLOWED:
        fail("invalid verdict")
    if schema["transport_sampling_verdict"] != schema["final_verdict"]:
        fail("final verdict mismatch")
    if len(read_csv("operator_chain_decoding_step206.csv")) != 4:
        fail("operator decoding must have 4 rows")
    if len(read_csv("assembled_chain_step206.csv")) != 4:
        fail("assembled chain must have 4 rows")
    boundary = (BASE / "boundary_identity_status_step206.csv").read_text(encoding="utf-8")
    if "explicit U_infty J_a^* M_Gamma^* action" not in boundary:
        fail("boundary status must name missing theorem")
    citations = (BASE / "classical_theorems_cited_step206.csv").read_text(encoding="utf-8")
    for token in ["Step145", "Step152", "Step153", "Step173", "Burnol 2002", "Burnol 2004"]:
        if token not in citations:
            fail(f"missing citation token {token}")
    tex = (BASE / "step206_transport_sampling_derivation.tex").read_text(encoding="utf-8")
    for token in ["V\\_transport\\_sampling\\_external\\_required", "U_\\infty J_a^*M_\\Gamma^*", "External Dependency"]:
        if token not in tex:
            fail(f"tex missing {token}")
    output = (BASE / "compute_step206_output.txt").read_text(encoding="utf-8")
    if "verdict=V_transport_sampling_external_required" not in output:
        fail("output must contain verdict")
    print("PASS step206 transport sampling derivation checks")


if __name__ == "__main__":
    main()
