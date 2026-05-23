#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step361_mode_B_2nd_design_richer_state_artifacts")

REQUIRED = [
    "U_flat_prime_design_step361.md",
    "SAU_gate_checks_U_flat_prime_step361.csv",
    "stage_II_preview_step361.csv",
    "stage_III_attempt_step361.csv",
    "mode_B_design_space_audit_step361.md",
    "step361_results_summary.md",
    "step361_schema.json",
    "nonclaim_boundary_step361.md",
    "run_step361_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 361 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        path = BASE / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")

    design = (BASE / "U_flat_prime_design_step361.md").read_text()
    for token in ["Sigma' = {a, b, c, d, e, f, g, h}", "R_op_realize", "R_phase_bound", "R_transfer_witness"]:
        require(token in design, f"design missing {token}")

    sau = read_csv("SAU_gate_checks_U_flat_prime_step361.csv")
    require(len(sau) == 6, "expected six SAU gates")
    require(all(row["status"] == "pass" for row in sau), "not all SAU gates pass")

    preview = read_csv("stage_II_preview_step361.csv")
    require(len(preview) == 50, f"expected 50 Stage II preview cells, got {len(preview)}")
    require(all(row["cell_pass"] == "yes" and row["relative_error"] == "0" for row in preview),
            "Stage II preview has failed cells")

    stage3 = read_csv("stage_III_attempt_step361.csv")
    summaries = {row["test_target"]: row for row in stage3 if row["row_type"] == "summary"}
    require(set(summaries) == {"rho_1", "rho_2", "rho_3"}, "missing Stage III summary rows")
    train = float(summaries["rho_1"]["lambda_total"])
    hold2 = float(summaries["rho_2"]["lambda_total"])
    hold3 = float(summaries["rho_3"]["lambda_total"])
    require(train < 0.5, "richer design did not improve training residual enough")
    require(hold2 > 0.5 and hold3 > 0.5, "holdout failure not recorded")
    require(all(row["admissible"] == "no" for row in summaries.values()), "Stage III should not be admissible")

    schema = json.loads((BASE / "step361_schema.json").read_text())
    require(schema["step"] == 361, "schema step mismatch")
    require(schema["SAU_gates_passed"] == 6, "schema SAU count mismatch")
    require(schema["stage_II_preview_passed"] == 50, "schema Stage II count mismatch")
    require(schema["stage_III_passed"] is False, "schema Stage III pass flag mismatch")
    require(schema["mode_B_design_retract_count"] == 2, "schema retract count mismatch")

    boundary = (BASE / "nonclaim_boundary_step361.md").read_text()
    require("does not claim" in boundary and "H6 bridge theorem" in boundary, "nonclaim boundary incomplete")

    print("Step 361 validator: PASS")


if __name__ == "__main__":
    main()
