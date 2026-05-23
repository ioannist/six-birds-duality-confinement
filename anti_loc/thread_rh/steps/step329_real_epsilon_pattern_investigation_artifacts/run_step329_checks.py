#!/usr/bin/env python3
"""Minimal validator for Step 329 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step329_real_epsilon_pattern_investigation_artifacts")
REQUIRED = [
    "extracted_construction_step329.md",
    "additional_characters_step329.csv",
    "self_dual_hypothesis_test_step329.csv",
    "step329_results_summary.md",
    "step329_schema.json",
    "nonclaim_boundary_step329.md",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step329_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 329:
        raise SystemExit("schema step mismatch")
    if "not_Burnol_theorem" not in schema.get("final_verdict", ""):
        raise SystemExit("verdict does not preserve extrapolation boundary")
    add = read_csv("additional_characters_step329.csv")
    hyp = read_csv("self_dual_hypothesis_test_step329.csv")
    labels = {row["character"] for row in add}
    for label in ["chi_7b", "chi_8b", "chi_11c", "chi_13a"]:
        if label not in labels:
            raise SystemExit(f"missing additional character row: {label}")
    invalid = [row for row in add if row["character"] == "chi_8b"]
    if not invalid or "invalid" not in invalid[0]["status"]:
        raise SystemExit("chi_8b invalidity not recorded")
    self_rows = [row for row in hyp if row["self_dual"] == "True" and row["max_kappa_abs"] != "NA"]
    non_rows = [row for row in hyp if row["self_dual"] == "False" and row["max_kappa_abs"] != "NA"]
    if not self_rows or not non_rows:
        raise SystemExit("self-dual/non-self-dual rows missing")
    max_self = max(float(row["max_kappa_abs"]) for row in self_rows)
    min_non = min(float(row["max_kappa_abs"]) for row in non_rows)
    if not max_self < 1e-40:
        raise SystemExit(f"self-dual cancellation threshold failed: {max_self}")
    if not min_non > 1e-8:
        raise SystemExit(f"non-self-dual nontrivial threshold failed: {min_non}")
    print("STEP329_CHECKS_PASS")
    print(f"self_dual_rows={len(self_rows)} non_self_dual_rows={len(non_rows)}")
    print(f"max_self={max_self:.3e} min_non={min_non:.3e}")


if __name__ == "__main__":
    main()
