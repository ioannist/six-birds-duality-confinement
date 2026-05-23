#!/usr/bin/env python3
"""Validate Step 292 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts")

REQUIRED = [
    "step292_results_summary.md",
    "step292_schema.json",
    "content_classification_step292.csv",
    "nonclaim_boundary_step292.md",
    "step292_branch_C_k20.tex",
    "compute_delta_Dk_step292.py",
    "compute_step292_output.txt",
    "run_step292_checks.py",
    "M_G_formula_provenance_step292.csv",
    "delta_Dk_certified_step292.csv",
    "fit_residuals_step292.csv",
    "law_continuation_decision_step292.csv",
    "residual_tree_step292.csv",
    "route_status_step292.csv",
    "construction_tasks_step292.csv",
]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        print("MISSING " + ", ".join(missing))
        return 1
    schema = json.loads((ART / "step292_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 292 or schema.get("orientation") != "adequacy":
        print("BAD_SCHEMA_HEADER")
        return 1
    if schema.get("final_verdict") != "V_branch_C_k20_law_breaks":
        print("BAD_VERDICT " + repr(schema.get("final_verdict")))
        return 1
    drows = rows(ART / "delta_Dk_certified_step292.csv")
    if len(drows) != 9:
        print(f"BAD_DELTA_ROW_COUNT {len(drows)}")
        return 1
    triples = {r["triple_id"] for r in drows}
    if triples != {"rho1_G_star", "rho2_G_star", "rho1_G_prime"}:
        print("BAD_TRIPLES " + repr(triples))
        return 1
    ks = {int(r["k"]) for r in drows}
    if ks != {10, 15, 20}:
        print("BAD_KS " + repr(ks))
        return 1
    for r in drows:
        if int(r["dps"]) < 80:
            print("DPS_TOO_LOW")
            return 1
        if float(r["delta_Dk_abs_dps80"]) <= 0:
            print("NONPOSITIVE_VALUE")
            return 1
    if len(rows(ART / "fit_residuals_step292.csv")) != 9:
        print("BAD_RESIDUAL_ROW_COUNT")
        return 1
    print("STEP292_CHECKS_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
