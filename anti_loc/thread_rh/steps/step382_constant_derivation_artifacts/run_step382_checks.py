#!/usr/bin/env python3
"""Validate Step 382 constant-derivation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step382_constant_derivation_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP382_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "analytical_derivation_step382.md",
        "slope_candidates_step382.csv",
        "offset_candidates_step382.csv",
        "step382_results_summary.md",
        "step382_schema.json",
        "nonclaim_boundary_step382.md",
        "run_step382_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    slopes = rows("slope_candidates_step382.csv")
    offsets = rows("offset_candidates_step382.csv")
    require(any(r["candidate"] == "pi^2" for r in slopes), "missing pi^2 slope candidate")
    require(any(r["candidate"] == "-3*pi/2" for r in offsets), "missing -3*pi/2 offset candidate")
    pi2 = next(r for r in slopes if r["candidate"] == "pi^2")
    off = next(r for r in offsets if r["candidate"] == "-3*pi/2")
    require(float(pi2["relative_error"]) < 0.10, "pi^2 not within 10 percent")
    require(float(off["relative_error"]) < 0.10, "-3*pi/2 not within 10 percent")

    schema = json.loads((BASE / "step382_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["structural_slope_candidate"] == "pi^2", "schema slope candidate mismatch")
    require(schema["structural_offset_candidate"] == "-3*pi/2", "schema offset candidate mismatch")
    require("saddle_displacement_unproved" in schema["verdict"], "missing partial verdict caveat")

    deriv = (BASE / "analytical_derivation_step382.md").read_text()
    require("g'_near = -1/(rho_n-rho_j)" in deriv, "missing Hadamard close-pair term")
    require("not theorem-grade" in deriv, "missing theorem-grade caveat")
    boundary = (BASE / "nonclaim_boundary_step382.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("not fully derived theorems" in boundary, "missing constant caveat")

    print("STEP382_CHECK_PASS")
    print(f"pi2_rel_error={float(pi2['relative_error']):.12g}")
    print(f"minus_3pi_over_2_rel_error={float(off['relative_error']):.12g}")
    print(f"verdict={schema['verdict']}")


if __name__ == "__main__":
    main()
