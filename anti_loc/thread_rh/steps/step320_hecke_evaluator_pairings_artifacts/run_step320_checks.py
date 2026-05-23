#!/usr/bin/env python3
"""Validate Step 320 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
REQUIRED = [
    "compute_L_chi_zeros_step320.py",
    "compute_hecke_evaluator_pairings_step320.py",
    "L_chi_first_zeros_step320.csv",
    "hecke_L_k_values_step320.csv",
    "branch_C_vs_hecke_comparison_step320.csv",
    "step320_results_summary.md",
    "step320_schema.json",
    "nonclaim_boundary_step320.md",
    "run_step320_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    zeros = read_csv("L_chi_first_zeros_step320.csv")
    if len(zeros) != 4:
        raise SystemExit(f"expected 4 zero rows, found {len(zeros)}")
    vals = read_csv("hecke_L_k_values_step320.csv")
    if len(vals) != 44:
        raise SystemExit(f"expected 44 evaluator rows, found {len(vals)}")
    chars = sorted({r["character"] for r in vals})
    if chars != ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        raise SystemExit(f"unexpected characters: {chars}")
    for ch in chars:
        ks = sorted(int(r["k"]) for r in vals if r["character"] == ch)
        if ks != list(range(11)):
            raise SystemExit(f"{ch} missing k values: {ks}")
    comp = read_csv("branch_C_vs_hecke_comparison_step320.csv")
    if len(comp) != 11:
        raise SystemExit(f"expected 11 comparison rows, found {len(comp)}")
    schema = json.loads((ART / "step320_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 320:
        raise SystemExit("schema step is not 320")
    if "GRH" not in (ART / "nonclaim_boundary_step320.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary does not mention GRH")
    print("STEP320_CHECKS_PASS")


if __name__ == "__main__":
    main()
