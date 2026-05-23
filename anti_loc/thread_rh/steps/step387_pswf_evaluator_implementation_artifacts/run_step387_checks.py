#!/usr/bin/env python3
"""Validate Step 387 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step387_pswf_evaluator_implementation_artifacts")
REQUIRED = [
    "pswf_evaluator_step387.py",
    "c_n_k_rho1_step387.csv",
    "D_n_step387.csv",
    "projected_gamma_rho1_step387.md",
    "step387_results_summary.md",
    "step387_schema.json",
    "nonclaim_boundary_step387.md",
    "run_step387_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step387_schema.json").read_text())
    if schema.get("step") != 387:
        raise SystemExit("wrong step in schema")
    if schema.get("mpmath_dps", 0) < 50:
        raise SystemExit("mpmath dps below requirement")
    if schema.get("pswf_backend") != "scipy.special.pro_ang1":
        raise SystemExit("unexpected PSWF backend")
    if schema.get("c_cells") < 30:
        raise SystemExit("fewer than 30 c cells")
    if schema.get("D_cells") < 10:
        raise SystemExit("fewer than 10 D cells")

    c_rows = rows("c_n_k_rho1_step387.csv")
    d_rows = rows("D_n_step387.csv")
    if len(c_rows) != schema["c_cells"]:
        raise SystemExit("c row count mismatch")
    if len(d_rows) != schema["D_cells"]:
        raise SystemExit("D row count mismatch")
    for row in c_rows:
        float(row["abs_c_n_k"])
        if row["transport_status"] != "standard_coordinate_proxy_not_U_infty_transport":
            raise SystemExit("transport caveat missing from c rows")
    for row in d_rows:
        float(row["abs_D_n"])

    gamma = float(schema["gamma_projected_proxy"])
    gamma_struct = float(schema["gamma_struct"])
    rel_err = float(schema["relative_error"])
    if not all(map(lambda x: x == x, [gamma, gamma_struct, rel_err])):
        raise SystemExit("NaN gamma fields")
    if gamma_struct <= 0:
        raise SystemExit("bad structural comparator")

    nonclaim = (ART / "nonclaim_boundary_step387.md").read_text()
    if "No RH claim" not in nonclaim:
        raise SystemExit("nonclaim boundary missing RH statement")
    if "not an exact Burnol/Sonine" not in nonclaim:
        raise SystemExit("transport caveat missing from nonclaim")

    print("step387 checks passed")


if __name__ == "__main__":
    main()
