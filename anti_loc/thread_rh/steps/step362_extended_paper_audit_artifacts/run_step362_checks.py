#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step362_extended_paper_audit_artifacts")
REQUIRED = [
    "fetched_new_sources_step362.csv",
    "paper_extracts_extended_step362.md",
    "extended_audit_outcome_step362.csv",
    "step362_results_summary.md",
    "step362_schema.json",
    "nonclaim_boundary_step362.md",
    "run_step362_checks.py",
]


def require(cond, msg):
    if not cond:
        raise SystemExit(f"Step 362 validator: FAIL: {msg}")


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    with (BASE / "fetched_new_sources_step362.csv").open(newline="") as f:
        sources = list(csv.DictReader(f))
    require(len(sources) >= 7, "expected at least seven new sources")
    require(all(r["accessible"] == "Y" for r in sources), "all recorded sources should be accessible")

    extracts = (BASE / "paper_extracts_extended_step362.md").read_text()
    for token in ["Beuzart-Plessis", "Sakellaridis", "Tate", "Bushnell-Henniart", "Gan-Savin", "Conrey"]:
        require(token in extracts, f"extracts missing {token}")

    with (BASE / "extended_audit_outcome_step362.csv").open(newline="") as f:
        outcomes = list(csv.DictReader(f))
    overall = [r for r in outcomes if r["source"] == "overall_step362"]
    require(overall, "missing overall outcome row")
    require("partial_with_named_gap" in overall[0]["outcome"], "overall status should be partial with named gap")
    require("no closure/no no-go" in overall[0]["H6_bridge_match"], "overall no closure/no no-go not recorded")

    schema = json.loads((BASE / "step362_schema.json").read_text())
    require(schema["step"] == 362, "schema step mismatch")
    require(schema["new_sources_fetched"] >= 7, "schema source count mismatch")
    require(schema["closure_found"] is False and schema["no_go_found"] is False, "schema closure/no-go flags mismatch")
    require("genuinely_open" in schema["cumulative_status"], "schema cumulative status mismatch")

    boundary = (BASE / "nonclaim_boundary_step362.md").read_text()
    require("does not claim" in boundary and "H6 bridge is closed" in boundary, "nonclaim boundary incomplete")

    print("Step 362 validator: PASS")


if __name__ == "__main__":
    main()
