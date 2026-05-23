#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step368_branch_C_residual_structure_artifacts")
REQUIRED = [
    "residuals_and_predictors_step368.csv",
    "correlations_step368.csv",
    "best_fit_corrections_step368.csv",
    "step368_results_summary.md",
    "step368_schema.json",
    "nonclaim_boundary_step368.md",
    "run_step368_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 368 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    residuals = read_csv("residuals_and_predictors_step368.csv")
    require(len(residuals) == 15, f"expected 15 residual rows, got {len(residuals)}")
    require(all("R" in r and r["R"] != "" for r in residuals), "missing residual values")
    require(all(r["defect_order_d"] == "0" for r in residuals), "defect order should default to 0")

    corrs = read_csv("correlations_step368.csv")
    require(len(corrs) >= 9, "expected correlations for candidate variables")
    corr_map = {r["variable"]: r for r in corrs}
    require("s_min" in corr_map and "spacing_asym" in corr_map, "missing spacing predictors")
    require(corr_map["defect_order_d"]["pearson_r"].startswith("undefined"), "constant defect order should be undefined")
    require(corr_map["eta_sign_Re_zeta2"]["pearson_r"].startswith("undefined"), "constant eta should be undefined")

    fits = {r["fit_type"]: r for r in read_csv("best_fit_corrections_step368.csv")}
    require("baseline_no_correction" in fits and "best_single" in fits and "best_pair" in fits, "missing fit summaries")
    baseline = float(fits["baseline_no_correction"]["mean_rel_err"])
    single = float(fits["best_single"]["mean_rel_err"])
    pair = float(fits["best_pair"]["mean_rel_err"])
    require(single < baseline, "single-variable correction should improve baseline")
    require(pair < single, "two-variable correction should improve single-variable correction")
    require(pair > 0.25, "best pair should not be strong enough to close residual")

    schema = json.loads((BASE / "step368_schema.json").read_text())
    require(schema["step"] == 368, "schema step mismatch")
    require(schema["best_single_variable"] == "s_min", "schema best single mismatch")
    require(schema["best_pair_variables"] == ["s_bwd", "s_min"], "schema best pair mismatch")
    require("complex" in schema["final_verdict"], "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step368.md").read_text()
    require("does not claim" in boundary and "fully explains" in boundary, "nonclaim boundary incomplete")

    print("Step 368 validator: PASS")


if __name__ == "__main__":
    main()
