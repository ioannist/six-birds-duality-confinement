#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step360_mode_B_stage_V_external_handoff_artifacts")

REQUIRED = [
    "fetched_sources_stage_V_step360.csv",
    "paper_extracts_stage_V_step360.md",
    "refined_gap_translation_step360.csv",
    "Mode_B_Stage_V_verdict_step360.md",
    "step360_results_summary.md",
    "step360_schema.json",
    "nonclaim_boundary_step360.md",
    "run_step360_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 360 validator: FAIL: {message}")


def main():
    for name in REQUIRED:
        path = BASE / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")

    with (BASE / "fetched_sources_stage_V_step360.csv").open(newline="") as f:
        sources = list(csv.DictReader(f))
    require(len(sources) >= 5, "expected at least five fetched sources")
    require(all(row["accessible"] == "Y" for row in sources), "all recorded sources should be accessible")

    extracts = (BASE / "paper_extracts_stage_V_step360.md").read_text()
    for token in ["Sakellaridis", "Lapid-Mao", "Wan", "Arthur", "transfer operators"]:
        require(token in extracts, f"extracts missing token {token}")

    with (BASE / "refined_gap_translation_step360.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    require(any(row["source"] == "overall_step360" and row["overall_outcome"] == "partial_with_named_gap" for row in rows),
            "overall partial_with_named_gap row missing")
    require(any("Burnol/Sonine" in row["Hecke_to_Burnol_Sonine_match"] or "Burnol/Sonine" in row["named_gap"] for row in rows),
            "Burnol/Sonine named gap missing")

    schema = json.loads((BASE / "step360_schema.json").read_text())
    require(schema["step"] == 360, "schema step mismatch")
    require(schema["outcome"] == "partial_with_named_gap", "schema outcome mismatch")
    require(schema["closure_available"] is False, "schema closure flag mismatch")
    require(schema["no_go_found"] is False, "schema no-go flag mismatch")

    boundary = (BASE / "nonclaim_boundary_step360.md").read_text()
    require("does not claim" in boundary and "RH" in boundary and "H6 bridge is resolved" in boundary,
            "nonclaim boundary incomplete")

    print("Step 360 validator: PASS")


if __name__ == "__main__":
    main()
