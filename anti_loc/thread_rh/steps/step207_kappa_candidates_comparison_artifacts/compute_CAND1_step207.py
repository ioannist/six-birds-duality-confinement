#!/usr/bin/env python3
"""Step 207 CAND1 samples.

CAND1 is the Burnol 2002 boundary value
    K_{1/2}^Gamma(1/2+i tau, rho_i)
computed in step 205 on the requested 200-node Gauss-Legendre grid.

This script imports that already-computed Burnol-boundary grid into the
step-207 artifact namespace, preserving the numerical error labels.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
STEP205 = ROOT / "anti_loc/thread/steps/step205_kappa_tau_sampling_artifacts/kappa_tau_samples_step205.csv"
OUTDIR = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
OUT = OUTDIR / "CAND1_samples_step207.csv"


def main() -> None:
    if not STEP205.exists():
        raise FileNotFoundError(f"missing inherited step205 CAND1 grid: {STEP205}")

    rows = []
    with STEP205.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "tau": row["tau"],
                    "rho_index": row["rho_index"],
                    "CAND1_real": row["kappa_candidate_real"],
                    "CAND1_imag": row["kappa_candidate_imag"],
                    "CAND1_abs": row["kappa_candidate_abs"],
                    "error_bound": row["error_bound"],
                    "status": "imported_from_step205_Burnol_boundary_candidate",
                    "formula": "K_{1/2}^Gamma(1/2+i tau,rho_i), Burnol 2002 eq.1 + Thm.8",
                }
            )

    OUTDIR.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        fieldnames = [
            "tau",
            "rho_index",
            "CAND1_real",
            "CAND1_imag",
            "CAND1_abs",
            "error_bound",
            "status",
            "formula",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    taus = sorted({r["tau"] for r in rows})
    print(f"CAND1 rows written: {len(rows)}")
    print(f"unique tau nodes: {len(taus)}")
    for target in ["-2.500000000000000000e+01", "0.000000000000000000e+00", "2.500000000000000000e+01"]:
        # Step 205 uses Gauss nodes rather than exact target values; print nearest rows.
        pass
    for r in rows[0:3]:
        print(f"sample CAND1 tau={r['tau']} rho={r['rho_index']} abs={r['CAND1_abs']}")


if __name__ == "__main__":
    main()
