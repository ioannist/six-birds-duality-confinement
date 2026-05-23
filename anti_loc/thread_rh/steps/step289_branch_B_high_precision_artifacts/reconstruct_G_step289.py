#!/usr/bin/env python3
"""Reconstruct Step 289 Branch B Gram matrix provenance from preserved Step 208 artifacts."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step289_branch_B_high_precision_artifacts"
STEP208 = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"
STEP207 = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    src208 = STEP208 / "G_matrix_step208.csv"
    src207 = STEP207 / "G_matrix_step207.csv"
    out_copy = ART / "G_matrix_step289.csv"
    shutil.copyfile(src208, out_copy)

    rows = []
    with src208.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "i": row["i"],
                    "j": row["j"],
                    "step289_copy": str(out_copy),
                    "step208_source": str(src208),
                    "step207_source": str(src207),
                    "G_real": row["G_real"],
                    "G_imag": row["G_imag"],
                    "status": row["status"],
                    "source_note": row["source"],
                    "provenance_summary": "Step208 copied Step207 G; diagonals from Step203 LHopital, off-diagonals from Step204 conjugate convention.",
                }
            )

    with (ART / "G_provenance_step289.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"reconstructed {out_copy}")


if __name__ == "__main__":
    main()
