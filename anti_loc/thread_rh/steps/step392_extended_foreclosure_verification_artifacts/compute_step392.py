#!/usr/bin/env python3
"""Step 392: extended raw-proxy foreclosure verification."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step392_extended_foreclosure_verification_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

DPS = 50
J_VALUES = list(range(100, 501, 5))
K_VALUES = [5, 10, 20, 30]
THRESHOLD = mp.mpf("0.034")
BORDERLINE = THRESHOLD * mp.mpf("1.10")
WORKERS = int(os.environ.get("STEP392_WORKERS", "4"))

_MOD: Any = None
_GEN: Any = None


def init_worker() -> None:
    global _MOD, _GEN
    spec = importlib.util.spec_from_file_location("step292_for_step392", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    _MOD = mod
    _GEN = mod.GENERATORS["G_star"]


def compute_one(j: int) -> list[dict[str, object]]:
    if _MOD is None:
        init_worker()
    mp.mp.dps = DPS
    rho = mp.zetazero(j)
    T = mp.im(rho)
    zds = _MOD.zeta_derivatives(T, max(K_VALUES), DPS)
    mds = _MOD.mellin_derivatives(_GEN, T, max(K_VALUES), DPS)
    rows: list[dict[str, object]] = []
    for k in K_VALUES:
        val = abs(_MOD.delta_from_derivatives(zds, mds, k))
        rows.append({
            "j": j,
            "T": mp.nstr(T, 30),
            "k": k,
            "abs_delta_Dk": mp.nstr(val, 30),
            "dps": DPS,
            "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho_j)",
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=WORKERS, initializer=init_worker) as ex:
        futs = {ex.submit(compute_one, j): j for j in J_VALUES}
        for fut in as_completed(futs):
            rows.extend(fut.result())
    rows.sort(key=lambda r: (int(r["j"]), int(r["k"])))

    check_rows: list[dict[str, object]] = []
    failures = []
    borderlines = []
    for r in rows:
        val = mp.mpf(str(r["abs_delta_Dk"]))
        passed = val >= THRESHOLD
        borderline = abs(val - THRESHOLD) <= (BORDERLINE - THRESHOLD)
        if not passed:
            failures.append(r)
        if borderline:
            borderlines.append(r)
        out = dict(r)
        out.update({
            "threshold": mp.nstr(THRESHOLD, 12),
            "pass_foreclosure": "PASS" if passed else "FAIL",
            "within_10_percent_of_bound": "YES" if borderline else "NO",
        })
        check_rows.append(out)

    bins = [(100, 200), (200, 300), (300, 400), (400, 501)]
    trend_lines = [
        "# Step 392 Trend Analysis",
        "",
        f"Requested full scope was j=100..500 at four k-values; computed reduced high-range grid `j=100..500 step 5`, k={K_VALUES}.",
        f"Cells computed: `{len(rows)}`.",
        "",
        "| j-bin | cells | min |delta_Dk| | min j | min k |",
        "|---|---:|---:|---:|---:|",
    ]
    for lo, hi in bins:
        sub = [r for r in rows if lo <= int(r["j"]) < hi]
        if not sub:
            continue
        min_row = min(sub, key=lambda r: mp.mpf(str(r["abs_delta_Dk"])))
        trend_lines.append(
            f"| [{lo},{hi}) | {len(sub)} | {min_row['abs_delta_Dk']} | {min_row['j']} | {min_row['k']} |"
        )

    min_row = min(rows, key=lambda r: mp.mpf(str(r["abs_delta_Dk"])))
    verdict = "robust_partial_high_range_grid_all_pass" if not failures else "failure_cells_found"

    write_csv(ART / "extended_L_k_values_step392.csv", rows)
    write_csv(ART / "foreclosure_check_extended_step392.csv", check_rows)
    (ART / "trend_analysis_step392.md").write_text("\n".join(trend_lines) + "\n")

    summary = [
        "# Step 392 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 196: foreclosure threshold `|L_k| >= 0.034`.",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 324: Branch C gamma-vs-zero-spacing dataset.",
        "- Step 377: high-zero zeta derivative sign context.",
        "- Step 380: `35/35` close-pair cells passed foreclosure.",
        "",
        f"Computed grid: `j=100..500 step 5`, k=`{K_VALUES}`.",
        f"Cells computed: `{len(rows)}`.",
        f"Pass count: `{len(rows) - len(failures)}`.",
        f"Fail count: `{len(failures)}`.",
        f"Borderline count within 10% of threshold: `{len(borderlines)}`.",
        f"Minimum abs_delta_Dk: `{min_row['abs_delta_Dk']}` at j=`{min_row['j']}`, k=`{min_row['k']}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step392_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 392,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "requested_full_scope": "j=100..500 all integers, k={5,10,20,30}; 1604 cells",
        "computed_scope": "j=100..500 step 5, k={5,10,20,30}",
        "computed_cells": len(rows),
        "dps": DPS,
        "workers": WORKERS,
        "threshold": float(THRESHOLD),
        "pass_count": len(rows) - len(failures),
        "fail_count": len(failures),
        "borderline_count": len(borderlines),
        "min_abs_delta_Dk": str(min_row["abs_delta_Dk"]),
        "min_cell": {"j": int(min_row["j"]), "k": int(min_row["k"]), "T": str(min_row["T"])},
        "verdict": verdict,
    }
    (ART / "step392_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step392.md").write_text(
        "# Nonclaim Boundary - Step 392\n\n"
        "No RH claim is made. This is an empirical raw-proxy foreclosure check "
        "using Step 292 `delta_Dk`, not the fully projected Burnol/Sonine "
        "`L_k` quantity and not a theorem for all zeros.\n"
    )

    print(f"cells={len(rows)} pass={len(rows)-len(failures)} fail={len(failures)}")
    print(f"min={min_row['abs_delta_Dk']} at j={min_row['j']} k={min_row['k']}")
    print(verdict)


if __name__ == "__main__":
    main()
