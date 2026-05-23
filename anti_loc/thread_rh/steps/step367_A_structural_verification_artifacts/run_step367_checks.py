#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step367_A_structural_verification_artifacts")
REQUIRED = [
    "A_predicted_vs_effective_step367.csv",
    "relative_errors_step367.csv",
    "position_stratification_step367.csv",
    "step367_results_summary.md",
    "step367_schema.json",
    "nonclaim_boundary_step367.md",
    "run_step367_checks.py",
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"Step 367 validator: FAIL: {message}")


def read_csv(name):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    for name in REQUIRED:
        p = BASE / name
        require(p.exists(), f"missing {name}")
        require(p.stat().st_size > 0, f"empty {name}")

    cells = read_csv("A_predicted_vs_effective_step367.csv")
    require(len(cells) == 30, f"expected 30 cells, got {len(cells)}")
    require(set(r["G"] for r in cells) == {"G_star", "G_prime"}, "missing G groups")
    require(set(r["position_band"] for r in cells) == {"low_1_5", "mid_6_10", "high_11_15"}, "missing position bands")

    stats = {r["group"]: r for r in read_csv("relative_errors_step367.csv")}
    require("all_30" in stats and "G_star_all" in stats and "G_prime_all" in stats, "missing error stats groups")
    require(float(stats["all_30"]["mean"]) > 0.20, "all-cell mean should show non-universal failure")
    require(float(stats["G_star_all"]["mean"]) < float(stats["G_prime_all"]["mean"]), "G_star should fit better than G_prime")

    strat = read_csv("position_stratification_step367.csv")
    low_star = [r for r in strat if r["G"] == "G_star" and r["position_band"] == "low_1_5"][0]
    high_prime = [r for r in strat if r["G"] == "G_prime" and r["position_band"] == "high_11_15"][0]
    require(float(low_star["mean"]) < 0.20, "low G_star band should be the best match")
    require(float(high_prime["mean"]) > 0.80, "high G_prime band should fail strongly")

    schema = json.loads((BASE / "step367_schema.json").read_text())
    require(schema["step"] == 367, "schema step mismatch")
    require(schema["cell_count"] == 30, "schema cell count mismatch")
    require("not_universal" in schema["verdict"], "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step367.md").read_text()
    require("does not claim" in boundary and "Universal validity" in boundary, "nonclaim boundary incomplete")

    print("Step 367 validator: PASS")


if __name__ == "__main__":
    main()
