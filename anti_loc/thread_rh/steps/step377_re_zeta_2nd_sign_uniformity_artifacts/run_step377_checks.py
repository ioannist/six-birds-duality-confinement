#!/usr/bin/env python3
"""Validate Step 377 sign-uniformity artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step377_re_zeta_2nd_sign_uniformity_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP377_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "zeta_double_prime_at_zeros_step377.csv",
        "sign_count_summary_step377.md",
        "exceptional_zeros_step377.csv",
        "step377_results_summary.md",
        "step377_schema.json",
        "nonclaim_boundary_step377.md",
        "run_step377_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    all_rows = rows("zeta_double_prime_at_zeros_step377.csv")
    exceptional = rows("exceptional_zeros_step377.csv")
    cross = rows("step368_crosscheck_step377.csv")
    require(len(all_rows) == 100, f"expected 100 zeta rows, got {len(all_rows)}")
    require(len(exceptional) == 7, f"expected 7 exceptional rows, got {len(exceptional)}")
    require(len(cross) == 15, f"expected 15 step368 cross-check rows, got {len(cross)}")

    neg = sum(1 for r in all_rows if r["sign_Re"] == "-1")
    pos = sum(1 for r in all_rows if r["sign_Re"] == "1")
    zero = sum(1 for r in all_rows if r["sign_Re"] == "0")
    require(neg == 93 and pos == 7 and zero == 0, f"unexpected signs neg={neg} pos={pos} zero={zero}")
    require([r["j"] for r in exceptional] == ["34", "41", "64", "71", "79", "80", "92"], "unexpected exceptional j list")
    require(all(r["sign_matches"] == "True" for r in cross), "step368 sign cross-check mismatch")

    schema = json.loads((BASE / "step377_schema.json").read_text())
    require(schema["dps"] >= 50, "dps below hard constraint")
    require(schema["negative_count"] == 93, "schema negative_count mismatch")
    require(schema["verdict"] == "majority_negative_not_uniform", "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step377.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("empirical" in boundary, "missing empirical scope")

    print("STEP377_CHECK_PASS")
    print(f"rows={len(all_rows)} negative={neg} positive={pos} zero={zero}")
    print("exceptions=34,41,64,71,79,80,92")


if __name__ == "__main__":
    main()
