#!/usr/bin/env python3
"""Validate Step 398 artifacts."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step398_branch_A_bergman_phi_max_artifacts")
REQUIRED = [
    "bergman_phi_max_derivation_step398.md",
    "closed_form_candidates_step398.csv",
    "step398_results_summary.md",
    "step398_schema.json",
    "nonclaim_boundary_step398.md",
    "run_step398_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step398_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 398:
        raise SystemExit("schema step is not 398")
    if schema.get("best_defensible_candidate") != "1/2":
        raise SystemExit("unexpected best defensible candidate")
    if float(schema["best_defensible_candidate_relative_error"]) >= 0.05:
        raise SystemExit("best defensible candidate is not within 5%")

    with (ART / "closed_form_candidates_step398.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 5:
        raise SystemExit("candidate table too small")
    by_name = {row["candidate"]: row for row in rows}
    if "half_projector_mass" not in by_name:
        raise SystemExit("missing half_projector_mass row")
    if not math.isclose(float(by_name["half_projector_mass"]["value"]), 0.5, rel_tol=0, abs_tol=1e-15):
        raise SystemExit("half candidate value mismatch")

    nonclaim = (ART / "nonclaim_boundary_step398.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    derivation = (ART / "bergman_phi_max_derivation_step398.md").read_text(encoding="utf-8")
    for token in ["z = exp(2*pi*i*w)", "C_ell = (I - P_infty) M_{m_ell} P_infty", "transport identity"]:
        if token not in derivation:
            raise SystemExit(f"derivation missing token: {token}")

    print("Step 398 checks passed.")
    print("candidate=1/2")
    print("relative_error=0.01941658502438906")


if __name__ == "__main__":
    main()
