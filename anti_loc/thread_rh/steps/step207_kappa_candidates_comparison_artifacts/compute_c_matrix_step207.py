#!/usr/bin/env python3
"""Step 207 commutator matrix placeholder/gate.

The hard constraint says not to choose a candidate arbitrarily if CAND1 and
CAND2 disagree structurally. This script therefore emits an explicit
not-evaluated c-matrix when the ratio audit returns disagreement.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
OUTDIR = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
RESOLUTION = OUTDIR / "transport_sampling_resolution_step207.csv"
OUT = OUTDIR / "c_matrix_step207.csv"


def final_verdict() -> str:
    with RESOLUTION.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["rho_index"] == "overall":
                return row["verdict"]
    raise RuntimeError("missing overall row in transport resolution")


def main() -> None:
    verdict = final_verdict()
    rows = []
    for i in range(1, 4):
        for j in range(1, 4):
            rows.append(
                {
                    "i": i,
                    "j": j,
                    "c_real": "",
                    "c_imag": "",
                    "c_abs": "",
                    "error_bound": "",
                    "status": "not_evaluated_transport_sampling_unresolved",
                    "reason": f"{verdict}; Step207 does not select CAND1 or CAND2 arbitrarily.",
                }
            )

    with OUT.open("w", newline="") as f:
        fieldnames = ["i", "j", "c_real", "c_imag", "c_abs", "error_bound", "status", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"c-matrix rows written: {len(rows)}")
    print(f"c-matrix status: not evaluated because transport verdict is {verdict}")


if __name__ == "__main__":
    main()
