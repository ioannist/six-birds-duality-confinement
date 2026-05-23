#!/usr/bin/env python3
"""Validator for Step 306 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step306_branch_B_cand_re_examination_artifacts")
REQUIRED = [
    "extract_steps_205_207_step306.md",
    "compute_cand1_cand2_tau0_step306.py",
    "cand1_cand2_tau0_comparison_step306.csv",
    "step306_results_summary.md",
    "step306_schema.json",
    "nonclaim_boundary_step306.md",
    "run_step306_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP306_ARTIFACTS {missing}")
    comp = rows("cand1_cand2_tau0_comparison_step306.csv")
    primary = next((r for r in comp if r["comparison"] == "bilinear_recomputed160_vs_CAND2"), None)
    if primary is None:
        raise SystemExit("MISSING_PRIMARY_COMPARISON")
    if float(primary["ratio_abs"]) >= 1e-6:
        raise SystemExit("PRIMARY_RATIO_NOT_SMALL")
    schema = json.loads((ART / "step306_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 306:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("final_verdict") != "V_branch_B_CAND1_CAND2_wrong_premise":
        raise SystemExit("BAD_VERDICT")
    print("STEP306_CHECKS_PASS")


if __name__ == "__main__":
    main()
