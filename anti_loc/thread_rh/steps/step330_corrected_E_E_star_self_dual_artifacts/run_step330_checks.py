#!/usr/bin/env python3
"""Minimal validator for Step 330 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step330_corrected_E_E_star_self_dual_artifacts")
REQUIRED = [
    "compute_corrected_kappa_chi_step330.py",
    "corrected_kappa_self_dual_step330.csv",
    "step330_results_summary.md",
    "step330_schema.json",
    "nonclaim_boundary_step330.md",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step330_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 330:
        raise SystemExit("schema step mismatch")
    with (ART / "corrected_kappa_self_dual_step330.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    labels = {row["character"] for row in rows}
    for label in ["chi_3", "chi_4", "chi_5a", "chi_13a"]:
        if label not in labels:
            raise SystemExit(f"missing character {label}")
    max_vals = [float(row["max_corrected_kappa_abs"]) for row in rows]
    old_vals = [float(row["step328_or_329_near_zero_max_abs"]) for row in rows]
    hb = [float(row["HB_ratio_abs_E_over_Esharp_at_t0_plus_i_center"]) for row in rows]
    if not all(v > 1e-8 for v in max_vals):
        raise SystemExit(f"corrected kappa still exactly degenerate: {max_vals}")
    if not all(v < 1e-40 for v in old_vals):
        raise SystemExit(f"old near-zero baseline not preserved: {old_vals}")
    if not all(v > 1 for v in hb):
        raise SystemExit(f"HB upper-half-plane separation failed: {hb}")
    threshold_count = sum(v > 0.01 for v in max_vals)
    print("STEP330_CHECKS_PASS")
    print(
        f"min_corrected={min(max_vals):.6g} threshold_count_gt_0p01={threshold_count}/4 "
        f"max_old={max(old_vals):.3e} min_HB_ratio={min(hb):.6g}"
    )


if __name__ == "__main__":
    main()
