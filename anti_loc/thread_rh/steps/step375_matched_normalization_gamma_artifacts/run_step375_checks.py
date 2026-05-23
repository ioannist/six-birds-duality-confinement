#!/usr/bin/env python3
"""Validator for Step 375 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step375_matched_normalization_gamma_artifacts")
REQUIRED = [
    "zeta_gamma_with_k_factorial_step375.csv",
    "zeta_vs_hecke_matched_step375.csv",
    "T_dependence_test_step375.md",
    "step375_results_summary.md",
    "step375_schema.json",
    "nonclaim_boundary_step375.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for name in REQUIRED:
        path = ART / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")
    zg = read_csv("zeta_gamma_with_k_factorial_step375.csv")
    comp = read_csv("zeta_vs_hecke_matched_step375.csv")
    schema = json.loads((ART / "step375_schema.json").read_text(encoding="utf-8"))
    boundary = (ART / "nonclaim_boundary_step375.md").read_text(encoding="utf-8")
    require(len(zg) == 15, f"expected 15 zeta gamma rows, got {len(zg)}")
    require(len(comp) == 17, f"expected 17 comparison rows, got {len(comp)}")
    require("divided by k!" in schema["evaluator"], "schema should record k! normalization")
    require(schema["relative_error_zeta_mean_vs_hecke_mean"] < 0.25, "matched means should pass Pattern A threshold")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")
    print("STEP375_VALIDATION_OK")
    print(f"verdict={schema['final_verdict']}")
    print(f"rel_mean={schema['relative_error_zeta_mean_vs_hecke_mean']:.12e}")


if __name__ == "__main__":
    main()
