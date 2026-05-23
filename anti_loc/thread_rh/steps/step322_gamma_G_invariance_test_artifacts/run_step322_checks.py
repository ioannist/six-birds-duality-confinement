#!/usr/bin/env python3
"""Validate Step 322 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts")
REQUIRED = [
    "compute_L_k_more_instances_step322.py",
    "critical_line_zeros_step322.csv",
    "fitted_gamma_per_instance_step322.csv",
    "gamma_universality_summary_step322.csv",
    "step322_results_summary.md",
    "step322_schema.json",
    "nonclaim_boundary_step322.md",
    "run_step322_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    zeros = rows("critical_line_zeros_step322.csv")
    objects = {r["object"] for r in zeros}
    expected = {"chi_7a", "chi_8a", "chi_11a", "zeta_rho3", "zeta_rho4", "zeta_rho5"}
    if not expected.issubset(objects):
        raise SystemExit(f"zero table missing expected objects: {expected - objects}")
    fit = rows("fitted_gamma_per_instance_step322.csv")
    computed = [r for r in fit if r["source"] == "computed_step322"]
    if len(computed) != 9:
        raise SystemExit(f"expected 9 computed fit rows, found {len(computed)}")
    summary = rows("gamma_universality_summary_step322.csv")
    if not any(r["G"] == "G_star" and r["family"] == "ALL" for r in summary):
        raise SystemExit("missing G_star ALL summary")
    if not any(r["G"] == "G_prime" and r["family"] == "ALL" for r in summary):
        raise SystemExit("missing G_prime ALL summary")
    schema = json.loads((ART / "step322_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 322 or schema.get("dps", 0) < 80:
        raise SystemExit("schema step/dps incorrect")
    if "GRH" not in (ART / "nonclaim_boundary_step322.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing GRH")
    print("STEP322_CHECKS_PASS")


if __name__ == "__main__":
    main()
