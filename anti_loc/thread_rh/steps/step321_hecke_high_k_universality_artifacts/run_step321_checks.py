#!/usr/bin/env python3
"""Validate Step 321 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step321_hecke_high_k_universality_artifacts")
REQUIRED = [
    "compute_hecke_high_k_step321.py",
    "hecke_L_k_chi_high_k_step321.csv",
    "hecke_saddle_fit_per_chi_step321.csv",
    "hecke_vs_branch_C_ratios_step321.csv",
    "step321_results_summary.md",
    "step321_schema.json",
    "nonclaim_boundary_step321.md",
    "run_step321_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    high = rows("hecke_L_k_chi_high_k_step321.csv")
    if len(high) != 12:
        raise SystemExit(f"expected 12 high-k rows, found {len(high)}")
    chars = sorted({r["character"] for r in high})
    if chars != ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        raise SystemExit(f"unexpected chars {chars}")
    for ch in chars:
        ks = sorted(int(r["k"]) for r in high if r["character"] == ch)
        if ks != [15, 20, 30]:
            raise SystemExit(f"{ch} missing high-k rows: {ks}")
    fit = rows("hecke_saddle_fit_per_chi_step321.csv")
    if len(fit) != 8:
        raise SystemExit(f"expected 8 fit rows, found {len(fit)}")
    ratios = rows("hecke_vs_branch_C_ratios_step321.csv")
    if [int(r["k"]) for r in ratios] != [10, 20, 30]:
        raise SystemExit("ratio table k rows incorrect")
    schema = json.loads((ART / "step321_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 321 or schema.get("dps", 0) < 80:
        raise SystemExit("schema step/dps incorrect")
    if "GRH" not in (ART / "nonclaim_boundary_step321.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing GRH")
    print("STEP321_CHECKS_PASS")


if __name__ == "__main__":
    main()
