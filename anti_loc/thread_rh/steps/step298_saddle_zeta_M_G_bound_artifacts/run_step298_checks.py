#!/usr/bin/env python3
"""Validate Step 298 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step298_saddle_zeta_M_G_bound_artifacts")
REQUIRED = [
    "compute_saddle_z_star_step298.py",
    "compute_zeta_M_G_at_saddle_step298.py",
    "saddle_locations_step298.csv",
    "zeta_M_G_at_saddle_step298.csv",
    "refined_prediction_step298.csv",
    "step298_results_summary.md",
    "step298_schema.json",
    "nonclaim_boundary_step298.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step298_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 298:
        raise SystemExit("schema mismatch")
    ks = {int(r["k"]) for r in rows("refined_prediction_step298.csv")}
    if ks != {10, 20, 30, 50}:
        raise SystemExit(f"bad prediction k set {ks}")
    if len(rows("saddle_locations_step298.csv")) != 4:
        raise SystemExit("missing saddle locations")
    print("STEP298_CHECKS_PASS")


if __name__ == "__main__":
    main()
