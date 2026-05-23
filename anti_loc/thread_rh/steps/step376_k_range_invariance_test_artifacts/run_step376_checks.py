#!/usr/bin/env python3
"""Validate Step 376 k-range invariance diagnostic artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step376_k_range_invariance_test_artifacts")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"STEP376_CHECK_FAIL: {message}")


def main() -> None:
    required = [
        "zeta_gamma_3_ranges_step376.csv",
        "hecke_gamma_3_ranges_step376.csv",
        "cluster_means_per_range_step376.csv",
        "step376_results_summary.md",
        "step376_schema.json",
        "nonclaim_boundary_step376.md",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    zeta = read_csv(BASE / "zeta_gamma_3_ranges_step376.csv")
    hecke = read_csv(BASE / "hecke_gamma_3_ranges_step376.csv")
    clusters = read_csv(BASE / "cluster_means_per_range_step376.csv")
    require(len(zeta) == 15, f"expected 15 zeta rows, got {len(zeta)}")
    require(len(hecke) == 15, f"expected 15 Hecke rows, got {len(hecke)}")
    require(len(clusters) == 6, f"expected 6 cluster rows, got {len(clusters)}")

    sides = {(row["side"], row["range_id"]) for row in clusters}
    expected = {
        ("zeta", "L_low"),
        ("zeta", "M_medium"),
        ("zeta", "H_high"),
        ("Hecke", "L_low"),
        ("Hecke", "M_medium"),
        ("Hecke", "H_high"),
    }
    require(sides == expected, f"unexpected cluster side/range set {sides}")

    by_side: dict[str, dict[str, float]] = {}
    for row in clusters:
        by_side.setdefault(row["side"], {})[row["range_id"]] = float(row["gamma_mean"])
        require(float(row["n_cells"]) == 5.0, f"cluster row not 5 cells: {row}")

    for side in ("zeta", "Hecke"):
        low = by_side[side]["L_low"]
        mid = by_side[side]["M_medium"]
        high = by_side[side]["H_high"]
        require(low < mid < high, f"{side} means are not increasing with k-range")
        require(high - low > 0.75, f"{side} total drift too small for artifact diagnostic")

    schema = json.loads((BASE / "step376_schema.json").read_text())
    require(schema.get("dps") == 80, "schema dps is not 80")
    require(schema.get("final_verdict") == "Stirling_artifact_confirmed_parallel_k_range_drift", "unexpected final verdict")

    boundary = (BASE / "nonclaim_boundary_step376.md").read_text().lower()
    require("does not prove rh" in boundary, "nonclaim boundary missing RH disclaimer")
    require("step 375" in boundary, "nonclaim boundary missing step 375 scope")

    print("STEP376_CHECK_PASS")
    print(f"zeta_rows={len(zeta)} hecke_rows={len(hecke)} cluster_rows={len(clusters)}")
    print(f"zeta_drift={by_side['zeta']['H_high'] - by_side['zeta']['L_low']:.12g}")
    print(f"hecke_drift={by_side['Hecke']['H_high'] - by_side['Hecke']['L_low']:.12g}")


if __name__ == "__main__":
    main()
