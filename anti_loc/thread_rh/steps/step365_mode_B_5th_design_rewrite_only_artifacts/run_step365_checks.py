#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step365_mode_B_5th_design_rewrite_only_artifacts")
REQUIRED = [
    "U_flat_R_rewrite_system_step365.md",
    "SAU_6_of_6_check_step365.csv",
    "stage_II_preview_step365.csv",
    "stage_III_attempt_step365.csv",
    "mode_B_5_design_space_summary_step365.md",
    "step365_results_summary.md",
    "step365_schema.json",
    "nonclaim_boundary_step365.md",
    "run_step365_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 365 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    design = (BASE / "U_flat_R_rewrite_system_step365.md").read_text()
    for token in ["no explicit state set", "Term Signature", "H(chi,k)", "Tau_R", "Rewrite Rules"]:
        require(token in design, f"rewrite design missing {token}")

    sau = read_csv("SAU_6_of_6_check_step365.csv")
    require(len(sau) == 6, "expected six SAU gates")
    require(all(row["status"] == "pass" for row in sau), "not all SAU gates pass")

    preview = read_csv("stage_II_preview_step365.csv")
    require(len(preview) == 50, f"expected 50 Stage II cells, got {len(preview)}")
    require(all(row["cell_pass"] == "yes" and row["relative_error"] == "0" for row in preview),
            "Stage II preview has failed cells")

    stage3 = read_csv("stage_III_attempt_step365.csv")
    summaries = {row["test_target"]: row for row in stage3 if row["row_type"] == "summary"}
    require(set(summaries) == {"rho_1", "rho_2", "rho_3"}, "missing Stage III summaries")
    train = float(summaries["rho_1"]["lambda_total"])
    hold2 = float(summaries["rho_2"]["lambda_total"])
    hold3 = float(summaries["rho_3"]["lambda_total"])
    require(train > 1.0 and hold2 > 1.0 and hold3 > 1.0, "rewrite Stage III failure not recorded")
    require(all(row["admissible"] == "no" for row in summaries.values()), "Stage III summaries should not be admissible")

    audit = (BASE / "mode_B_5_design_space_summary_step365.md").read_text()
    for token in ["U^flat_R", "rewrite-system-only", "state-based carriers", "graph/path-predicate carriers"]:
        require(token in audit, f"five-design audit missing {token}")

    schema = json.loads((BASE / "step365_schema.json").read_text())
    require(schema["step"] == 365, "schema step mismatch")
    require(schema["explicit_state_set"] is False, "schema explicit_state_set should be false")
    require(schema["SAU_gates_passed"] == 6, "schema SAU mismatch")
    require(schema["stage_II_preview_passed"] == 50, "schema Stage II mismatch")
    require(schema["stage_III_passed"] is False, "schema Stage III flag mismatch")
    require(schema["mode_B_design_retract_count"] == 5, "schema retract count mismatch")

    boundary = (BASE / "nonclaim_boundary_step365.md").read_text()
    require("does not claim" in boundary and "H6 closure" in boundary, "nonclaim boundary incomplete")

    print("Step 365 validator: PASS")


if __name__ == "__main__":
    main()
