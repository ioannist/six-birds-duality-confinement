#!/usr/bin/env python3
"""Validator for Step 277 closed-form search artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step277_phi_max_closed_form_artifacts")

REQUIRED = [
    "step277_results_summary.md",
    "step277_schema.json",
    "content_classification_step277.csv",
    "nonclaim_boundary_step277.md",
    "step277_phi_max_closed_form.tex",
    "pslq_search_step277.py",
    "compute_step277_output.txt",
    "run_step277_checks.py",
    "candidate_constants_step277.csv",
    "pslq_results_step277.csv",
    "persistence_step277.csv",
    "residual_tree_step277.csv",
    "route_status_step277.csv",
    "construction_tasks_step277.csv",
    "classical_theorems_cited_step277.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step277_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 277
    assert schema["orientation"] == "numerical_fishing"
    assert schema["target"] == "closed form for \u03a6_max"
    assert schema["final_verdict"] == "V_branch_A_no_closed_form"
    assert schema["pslq_search_results"]["strict_hits"] == 0
    assert schema["persistence_check"]["passes_20_digits"] is False

    constants = read_csv("candidate_constants_step277.csv")
    assert len(constants) >= 20
    names = {row["name"] for row in constants}
    for name in ["pi", "log2", "EulerGamma", "zeta3", "Catalan", "Gamma_1_4"]:
        assert name in names

    pslq = read_csv("pslq_results_step277.csv")
    statuses = Counter(row["status"] for row in pslq)
    assert statuses["candidate_relation"] == 0
    assert statuses["no_relation"] > 0

    persistence = read_csv("persistence_step277.csv")
    assert all(row["persistence_status"] == "reject" for row in persistence)
    assert any(row["candidate"] == "log2/sqrt2" for row in persistence)

    output = (ART / "compute_step277_output.txt").read_text(encoding="utf-8")
    assert "mpmath_dps=120" in output
    assert "strict_pslq_hits=0" in output
    assert "final_verdict=V_branch_A_no_closed_form" in output

    print("run_step277_checks.py PASS")


if __name__ == "__main__":
    main()
