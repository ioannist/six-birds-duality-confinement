#!/usr/bin/env python3
"""Validate Step 269 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts")

REQUIRED = [
    "step269_results_summary.md",
    "step269_schema.json",
    "content_classification_step269.csv",
    "nonclaim_boundary_step269.md",
    "step269_branch_C_k_extension.tex",
    "compute_branch_C_k_5_6_7_step269.py",
    "compute_step269_output.txt",
    "run_step269_checks.py",
    "extended_dataset_step269.csv",
    "exponential_fit_step269.csv",
    "residual_analysis_step269.csv",
    "polynomial_correction_test_step269.csv",
    "residual_tree_step269.csv",
    "route_status_step269.csv",
    "construction_tasks_step269.csv",
    "classical_theorems_cited_step269.csv",
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

    schema = json.loads((ART / "step269_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 269:
        return fail("schema step mismatch")
    if schema.get("orientation") != "numerical_extension":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_branch_C_polynomial_correction":
        return fail("unexpected verdict")

    data = rows("extended_dataset_step269.csv")
    if len(data) != 24:
        return fail("expected 24 dataset rows")
    triples = {row["triple_id"] for row in data}
    if triples != {"rho1_G_star", "rho2_G_star", "rho1_G_prime"}:
        return fail("triple set mismatch")
    for triple in triples:
        ks = {int(row["k"]) for row in data if row["triple_id"] == triple}
        if ks != set(range(8)):
            return fail("missing k values for " + triple)
    for row in data:
        if int(row["k"]) >= 5 and float(row["lower_bound"]) <= 1.0:
            return fail("high-k lower bound too small for " + row["triple_id"])

    fits = rows("exponential_fit_step269.csv")
    if len(fits) != 3:
        return fail("expected three exponential fits")
    for row in fits:
        if float(row["b"]) <= 0.5:
            return fail("exponential b unexpectedly small")

    poly = rows("polynomial_correction_test_step269.csv")
    if len(poly) != 3:
        return fail("expected three polynomial correction rows")
    for fit_row, poly_row in zip(sorted(fits, key=lambda r: r["triple_id"]), sorted(poly, key=lambda r: r["triple_id"])):
        if float(poly_row["rmse_k0_7"]) >= float(fit_row["rmse_k0_7"]):
            return fail("polynomial correction did not improve " + poly_row["triple_id"])

    sources = rows("classical_theorems_cited_step269.csv")
    joined = " ".join(row["source"] for row in sources)
    for token in ["Burnol", "Step 250"]:
        if token not in joined:
            return fail("missing source token " + token)

    print("PASS step269 artifact contract")
    print("verdict=V_branch_C_polynomial_correction")
    print("dataset_rows=24")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
