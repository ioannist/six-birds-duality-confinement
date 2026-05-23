#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step366_branch_C_A_structural_origin_pivot_artifacts")
REQUIRED = [
    "candidate_derivations_step366.md",
    "numerical_predictions_step366.csv",
    "comparison_to_empirical_step366.csv",
    "step366_results_summary.md",
    "step366_schema.json",
    "nonclaim_boundary_step366.md",
    "run_step366_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 366 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    deriv = (BASE / "candidate_derivations_step366.md").read_text()
    for token in ["Local Zero Density", "Plancherel", "Zeta-Derivative", "pi/log(T/(2*pi))"]:
        require(token in deriv, f"derivation missing {token}")

    preds = read_csv("numerical_predictions_step366.csv")
    require(len(preds) == 20, f"expected 20 prediction rows, got {len(preds)}")

    comp = read_csv("comparison_to_empirical_step366.csv")
    require(len(comp) == 20, f"expected 20 comparison rows, got {len(comp)}")
    rho1_half = [r for r in comp if r["rho_index"] == "1" and r["candidate"] == "local_zero_density_half_spacing"][0]
    require(float(rho1_half["relative_error_vs_A_global_G_star_rho1_only"]) < 0.10,
            "rho1 half-spacing should match global A within 10%")
    zeta_fail = [r for r in comp if r["candidate"] == "zeta_prime_inverse"]
    require(all(float(r["relative_error"]) > 0.5 for r in zeta_fail), "zeta prime inverse should fail per-zero comparison")

    schema = json.loads((BASE / "step366_schema.json").read_text())
    require(schema["step"] == 366, "schema step mismatch")
    require(schema["best_candidate"] == "local_zero_density_half_spacing", "schema best candidate mismatch")
    require("partial" in schema["final_verdict"], "schema verdict should be partial")

    boundary = (BASE / "nonclaim_boundary_step366.md").read_text()
    require("does not claim" in boundary and "A = pi/log" in boundary, "nonclaim boundary incomplete")

    print("Step 366 validator: PASS")


if __name__ == "__main__":
    main()
