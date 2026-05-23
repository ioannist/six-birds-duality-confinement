#!/usr/bin/env python3
"""Validate Step 323 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step323_gamma_vs_height_artifacts")
REQUIRED = [
    "compute_gamma_higher_zeros_step323.py",
    "gamma_vs_im_rho_step323.csv",
    "functional_form_fit_step323.csv",
    "cross_family_universality_step323.csv",
    "step323_results_summary.md",
    "step323_schema.json",
    "nonclaim_boundary_step323.md",
    "run_step323_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    gamma = rows("gamma_vs_im_rho_step323.csv")
    if len(gamma) != 15:
        raise SystemExit(f"expected 15 zeta gamma rows, found {len(gamma)}")
    computed = [r for r in gamma if r["source"] == "computed_step323"]
    if len(computed) != 10:
        raise SystemExit(f"expected 10 computed zeta rows, found {len(computed)}")
    forms = rows("functional_form_fit_step323.csv")
    if len(forms) != 3:
        raise SystemExit(f"expected 3 functional-form fits, found {len(forms)}")
    cross = rows("cross_family_universality_step323.csv")
    if not any(r["object"] == "chi_13a_legendre_first_zero" for r in cross):
        raise SystemExit("missing chi_13a cross-family candidate")
    schema = json.loads((ART / "step323_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 323 or schema.get("dps", 0) < 80:
        raise SystemExit("schema step/dps incorrect")
    if "GRH" not in (ART / "nonclaim_boundary_step323.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing GRH")
    print("STEP323_CHECKS_PASS")


if __name__ == "__main__":
    main()
