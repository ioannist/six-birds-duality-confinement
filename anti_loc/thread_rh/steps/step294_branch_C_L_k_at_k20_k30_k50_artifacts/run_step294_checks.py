#!/usr/bin/env python3
"""Validate Step 294 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step294_branch_C_L_k_at_k20_k30_k50_artifacts")

REQUIRED = [
    "compute_L_k_method_B_step294.py",
    "compute_step294_output.txt",
    "component_table_step294.csv",
    "cross_check_k20_step294.csv",
    "asymptotic_regime_step294.md",
    "step294_results_summary.md",
    "step294_schema.json",
    "content_classification_step294.csv",
    "nonclaim_boundary_step294.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step294_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 294:
        raise SystemExit("schema step mismatch")
    if schema.get("final_verdict") != "V_branch_C_high_k_I_dominates":
        raise SystemExit("unexpected final verdict")

    table = rows("component_table_step294.csv")
    ks = {int(row["k"]) for row in table}
    if ks != {10, 20, 30, 50}:
        raise SystemExit(f"unexpected k set: {ks}")
    for row in table:
        if int(row["k"]) >= 20 and float(row["L_over_I"]) < 0.999999:
            raise SystemExit(f"I dominance not captured: {row}")

    cross = rows("cross_check_k20_step294.csv")
    if len(cross) != 1 or cross[0]["decision"] != "agree":
        raise SystemExit("k=20 cross-check did not agree")

    print("STEP294_CHECKS_PASS")


if __name__ == "__main__":
    main()
