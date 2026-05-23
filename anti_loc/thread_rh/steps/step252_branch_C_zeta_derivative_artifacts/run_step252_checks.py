#!/usr/bin/env python3
"""Validate Step 252 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step252_branch_C_zeta_derivative_artifacts")

REQUIRED = [
    "step252_results_summary.md",
    "step252_schema.json",
    "content_classification_step252.csv",
    "nonclaim_boundary_step252.md",
    "step252_branch_C_zeta_derivative.tex",
    "compute_zeta_derivatives_step252.py",
    "compute_xi_derivatives_step252.py",
    "compute_step252_output.txt",
    "run_step252_checks.py",
    "zeta_derivatives_step252.csv",
    "xi_derivatives_step252.csv",
    "L_k_vs_derivatives_step252.csv",
    "candidate_relationships_step252.csv",
    "residual_tree_step252.csv",
    "route_status_step252.csv",
    "construction_tasks_step252.csv",
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

    schema = json.loads((ART / "step252_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 252:
        return fail("schema step mismatch")
    if schema.get("final_verdict") != "V_branch_C_zeta_derivative_no_simple_connection":
        return fail("unexpected final verdict")

    zeta = rows("zeta_derivatives_step252.csv")
    xi = rows("xi_derivatives_step252.csv")
    if len(zeta) != 10 or len(xi) != 10:
        return fail("expected 10 zeta and 10 xi derivative rows")
    for table, name in [(zeta, "zeta"), (xi, "xi")]:
        for idx in ["1", "2"]:
            ks = sorted(int(r["k"]) for r in table if r["rho_index"] == idx)
            if ks != [0, 1, 2, 3, 4]:
                return fail(f"{name} rho{idx} missing k rows: {ks}")

    comp = rows("L_k_vs_derivatives_step252.csv")
    if len(comp) != 15:
        return fail("expected 15 comparison rows")
    if not any(r["triple_id"] == "rho1_G_star" and r["k"] == "4" and float(r["L_over_zeta_derivative_abs"]) > 4 for r in comp):
        return fail("rho1_G_star k=4 zeta ratio check failed")

    rel = rows("candidate_relationships_step252.csv")
    if not rel:
        return fail("empty candidate relationships")
    if not any(r["status"] == "rejected_not_constant" for r in rel):
        return fail("no rejected candidate relationship rows")

    output = (ART / "compute_step252_output.txt").read_text(encoding="utf-8")
    if "verdict=V_branch_C_zeta_derivative_no_simple_connection" not in output:
        return fail("output missing verdict")

    print("PASS step252 artifact contract")
    print("verdict=V_branch_C_zeta_derivative_no_simple_connection")
    print("zeta_rows=10 xi_rows=10 comparison_rows=15")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
