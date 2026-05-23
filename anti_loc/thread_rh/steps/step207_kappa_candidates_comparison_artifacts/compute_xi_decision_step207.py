#!/usr/bin/env python3
"""Step 207 Xi decision gate.

Copies the inherited G matrix and records that Xi_matrix_source is not
computed because the two independent kappa candidates disagree structurally.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
OUTDIR = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
G_SRC = ROOT / "anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts/G_matrix_step204.csv"
G_OUT = OUTDIR / "G_matrix_step207.csv"
RESOLUTION = OUTDIR / "transport_sampling_resolution_step207.csv"
XI_OUT = OUTDIR / "xi_decision_step207.csv"


def final_verdict() -> str:
    with RESOLUTION.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["rho_index"] == "overall":
                return row["verdict"]
    raise RuntimeError("missing overall row in transport resolution")


def main() -> None:
    if not G_SRC.exists():
        raise FileNotFoundError(f"missing inherited G matrix: {G_SRC}")
    shutil.copyfile(G_SRC, G_OUT)
    verdict = final_verdict()

    rows = [
        {
            "quantity": "Xi_matrix_source",
            "value": "",
            "error_bound": "",
            "lower_bound": "",
            "verdict": verdict,
            "status": "not_computed_transport_sampling_unresolved",
            "formula": "tr(G^{-1} c^dagger G^{-1} c), compressed-HS in unnormalized basis",
            "reason": "CAND1 and CAND2 do not agree up to a constant; Step207 hard constraint forbids arbitrary candidate selection.",
        }
    ]
    with XI_OUT.open("w", newline="") as f:
        fieldnames = ["quantity", "value", "error_bound", "lower_bound", "verdict", "status", "formula", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"G matrix copied from {G_SRC}")
    print(f"Xi decision: {verdict}")


if __name__ == "__main__":
    main()
