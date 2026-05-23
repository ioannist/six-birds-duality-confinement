#!/usr/bin/env python3
"""Validator for Step 278 pure-mpmath artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step278_phi_max_pure_mpmath_artifacts")

REQUIRED = [
    "step278_results_summary.md",
    "step278_schema.json",
    "content_classification_step278.csv",
    "nonclaim_boundary_step278.md",
    "step278_phi_max_pure_mpmath.tex",
    "compute_phi_max_pure_mpmath_step278.py",
    "pslq_high_precision_step278.py",
    "compute_step278_output.txt",
    "run_step278_checks.py",
    "convergence_check_step278.csv",
    "phi_max_high_precision_step278.csv",
    "pslq_retry_step278.csv",
    "persistence_step278.csv",
    "residual_tree_step278.csv",
    "route_status_step278.csv",
    "construction_tasks_step278.csv",
    "classical_theorems_cited_step278.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step278_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 278
    assert schema["orientation"] == "numerical_high_precision"
    assert schema["final_verdict"] == "V_branch_A_high_precision_partial"
    assert schema["phi_max_high_precision"]["trusted_digits_vs_reference"] == 0
    assert schema["pslq_high_precision_results"]["status"] == "not_run_unstable_input"

    convergence = read_csv("convergence_check_step278.csv")
    assert len(convergence) >= 6
    assert any(row["dps"] == "120" for row in convergence)
    assert all(row["projection"] == "pure_mpmath_sinc_hard_band_proxy" for row in convergence)

    high = read_csv("phi_max_high_precision_step278.csv")
    assert high[0]["stability_status"] == "not_stable_enough_for_pslq"

    pslq = read_csv("pslq_retry_step278.csv")
    assert all(row["status"] == "not_run_unstable_input" for row in pslq)

    output = (ART / "compute_step278_output.txt").read_text(encoding="utf-8")
    assert "final_verdict=V_branch_A_high_precision_partial" in output
    assert "full_PSWF_Sonine_replacement=not_completed" in output

    script = (ART / "compute_phi_max_pure_mpmath_step278.py").read_text(encoding="utf-8")
    assert "import numpy" not in script
    assert "mpmath" in script

    print("run_step278_checks.py PASS")


if __name__ == "__main__":
    main()
