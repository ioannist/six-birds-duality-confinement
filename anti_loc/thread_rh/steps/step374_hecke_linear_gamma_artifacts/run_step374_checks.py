#!/usr/bin/env python3
"""Validator for Step 374 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step374_hecke_linear_gamma_artifacts")
REQUIRED = [
    "hecke_linear_gamma_step374.csv",
    "structural_candidate_comparison_step374.csv",
    "step374_results_summary.md",
    "step374_schema.json",
    "nonclaim_boundary_step374.md",
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
    gamma = read_csv("hecke_linear_gamma_step374.csv")
    comp = read_csv("structural_candidate_comparison_step374.csv")
    schema = json.loads((ART / "step374_schema.json").read_text(encoding="utf-8"))
    boundary = (ART / "nonclaim_boundary_step374.md").read_text(encoding="utf-8")
    require(len(gamma) == 7, f"expected 7 gamma rows, got {len(gamma)}")
    require(len(comp) == 21, f"expected 21 comparison rows, got {len(comp)}")
    require(schema["data_scale"] == "normalized |h_chi^(k)/k!|", "unexpected data scale")
    require(schema["best_candidate_mean_rel_err"] > 0.25, "best candidate should not pass threshold")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")
    print("STEP374_VALIDATION_OK")
    print(f"best={schema['best_candidate']}")
    print(f"best_mean_rel_err={schema['best_candidate_mean_rel_err']:.12e}")
    print(f"verdict={schema['final_verdict']}")


if __name__ == "__main__":
    main()
