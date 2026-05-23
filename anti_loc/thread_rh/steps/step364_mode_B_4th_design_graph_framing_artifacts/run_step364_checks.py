#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step364_mode_B_4th_design_graph_framing_artifacts")
REQUIRED = [
    "U_flat_G_design_step364.md",
    "SAU_6_of_6_check_step364.csv",
    "stage_II_preview_step364.csv",
    "stage_III_attempt_step364.csv",
    "mode_B_4_design_space_summary_step364.md",
    "step364_results_summary.md",
    "step364_schema.json",
    "nonclaim_boundary_step364.md",
    "run_step364_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 364 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    design = (BASE / "U_flat_G_design_step364.md").read_text()
    for token in ["Nodes V", "Edges E", "Path predicates", "e_load_H", "P_admit"]:
        require(token in design, f"graph design missing {token}")

    sau = read_csv("SAU_6_of_6_check_step364.csv")
    require(len(sau) == 6, "expected six SAU gates")
    require(all(row["status"] == "pass" for row in sau), "not all SAU gates pass")

    preview = read_csv("stage_II_preview_step364.csv")
    require(len(preview) == 50, f"expected 50 Stage II cells, got {len(preview)}")
    require(all(row["cell_pass"] == "yes" and row["relative_error"] == "0" for row in preview),
            "Stage II preview has failed cells")

    stage3 = read_csv("stage_III_attempt_step364.csv")
    summaries = {row["test_target"]: row for row in stage3 if row["row_type"] == "summary"}
    require(set(summaries) == {"rho_1", "rho_2", "rho_3"}, "missing Stage III summaries")
    train = float(summaries["rho_1"]["lambda_total"])
    hold2 = float(summaries["rho_2"]["lambda_total"])
    hold3 = float(summaries["rho_3"]["lambda_total"])
    require(train > 1.0 and hold2 > 1.0 and hold3 > 1.0, "graph Stage III failure not recorded")
    require(all(row["admissible"] == "no" for row in summaries.values()), "Stage III should not be admissible")

    audit = (BASE / "mode_B_4_design_space_summary_step364.md").read_text()
    for token in ["U^flat", "U^flat-prime", "U^flat-double-prime", "U^flat_G", "Four structurally distinct"]:
        require(token in audit, f"design-space summary missing {token}")

    schema = json.loads((BASE / "step364_schema.json").read_text())
    require(schema["step"] == 364, "schema step mismatch")
    require(schema["SAU_gates_passed"] == 6, "schema SAU mismatch")
    require(schema["stage_II_preview_passed"] == 50, "schema Stage II mismatch")
    require(schema["stage_III_passed"] is False, "schema Stage III flag mismatch")
    require(schema["mode_B_design_retract_count"] == 4, "schema retract count mismatch")

    boundary = (BASE / "nonclaim_boundary_step364.md").read_text()
    require("does not claim" in boundary and "H6 closure" in boundary, "nonclaim boundary incomplete")

    print("Step 364 validator: PASS")


if __name__ == "__main__":
    main()
