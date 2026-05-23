#!/usr/bin/env python3
"""Validate Step 251 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step251_BN_N5000_extension_artifacts")

REQUIRED = [
    "step251_results_summary.md",
    "step251_schema.json",
    "content_classification_step251.csv",
    "nonclaim_boundary_step251.md",
    "step251_BN_N5000_extension.tex",
    "compute_BN_N5000_step251.py",
    "compute_BN_N5000_output_step251.txt",
    "run_step251_BN_N5000_checks.py",
    "extended_data_step251.csv",
    "updated_decay_fit_step251.csv",
    "residual_tree_step251.csv",
    "route_status_step251.csv",
    "construction_tasks_step251.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail(msg: str) -> int:
    print("FAIL", msg)
    return 1


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        return fail("missing files: " + ", ".join(missing))

    schema = json.loads((ART / "step251_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 251:
        return fail("schema step mismatch")
    if schema.get("orientation") != "adequacy":
        return fail("schema orientation mismatch")
    if schema.get("final_verdict") != "V_BN_N5000_consistent":
        return fail("unexpected final verdict")
    if schema.get("N_values_computed") != [3000, 4000, 5000]:
        return fail("N_values_computed mismatch")

    data = read_csv("extended_data_step251.csv")
    by_n = {int(row["N"]): row for row in data}
    for n in [2000, 3000, 4000, 5000]:
        if n not in by_n:
            return fail(f"missing N={n}")
        if float(by_n[n]["delta_sq"]) <= 0:
            return fail(f"N={n} nonpositive delta_sq")
        if float(by_n[n]["delta_sq_logN"]) <= 0:
            return fail(f"N={n} nonpositive delta_sq_logN")
        if float(by_n[n]["tail_bound_per_entry"]) > 3.4e-6:
            return fail(f"N={n} tail bound too large")

    n5000 = float(by_n[5000]["delta_sq_logN"])
    if not (0.043 <= n5000 <= 0.047):
        return fail("N=5000 delta_sq_logN outside slow-log band")

    fit = read_csv("updated_decay_fit_step251.csv")
    names = {row["model"] for row in fit}
    for needed in ["tail_mean_delta_sq_logN", "recent_tail_mean_delta_sq_logN", "newest_C_over_logN_alpha"]:
        if needed not in names:
            return fail("missing fit row " + needed)

    output = (ART / "compute_BN_N5000_output_step251.txt").read_text(encoding="utf-8")
    for token in ["N=3000", "N=4000", "N=5000", "X_MAX=300000"]:
        if token not in output:
            return fail("output missing token " + token)

    print("PASS step251 artifact contract")
    print("verdict=V_BN_N5000_consistent")
    print(f"N5000_delta_sq={float(by_n[5000]['delta_sq']):.12g}")
    print(f"N5000_delta_sq_logN={n5000:.12g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
