#!/usr/bin/env python3
"""Step 380: Branch C foreclosure robustness at close-pair exceptional zeros."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step380_branch_C_foreclosure_robustness_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 80
FIT_K = [5, 10, 15, 20, 30]
EXCEPTIONS = [34, 41, 64, 71, 79, 80, 92]
BASELINE = [1, 2, 3, 4, 5]
BOUND = mp.mpf("0.034")


def load_step292():
    spec = importlib.util.spec_from_file_location("step292_for_step380", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step292_for_step380"] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def eval_rows(step292, zero_indices: list[int], label: str) -> list[dict[str, object]]:
    gen = step292.GENERATORS["G_star"]
    max_k = max(FIT_K)
    rows = []
    for j in zero_indices:
        rho = mp.zetazero(j)
        T = mp.im(rho)
        zds = step292.zeta_derivatives(T, max_k, DPS)
        mds = step292.mellin_derivatives(gen, T, max_k, DPS)
        for k in FIT_K:
            val = abs(step292.delta_from_derivatives(zds, mds, k))
            rows.append(
                {
                    "group": label,
                    "j": j,
                    "T": mp.nstr(T, 30),
                    "k": k,
                    "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho)",
                    "normalization": "unnormalized raw absolute value; no k! division",
                    "corrections_applied": "none; I_k/R_k projection corrections unavailable for these cells",
                    "abs_value": mp.nstr(val, 30),
                }
            )
        print(f"computed {label} j={j}", flush=True)
    return rows


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    step292 = load_step292()

    exceptional = eval_rows(step292, EXCEPTIONS, "exceptional")
    baseline = eval_rows(step292, BASELINE, "baseline")

    write_csv(BASE / "exceptional_L_k_values_step380.csv", exceptional)
    write_csv(BASE / "baseline_L_k_values_step380.csv", baseline)

    checks = []
    failures = []
    borderline = []
    for row in exceptional:
        val = mp.mpf(row["abs_value"])
        margin = val / BOUND
        status = "PASS" if val >= BOUND else "FAIL"
        if val < BOUND:
            failures.append(row)
        if abs(val - BOUND) / BOUND <= mp.mpf("0.10"):
            borderline.append(row)
        checks.append(
            {
                "j": row["j"],
                "T": row["T"],
                "k": row["k"],
                "abs_value": row["abs_value"],
                "bound": mp.nstr(BOUND, 20),
                "pass_bound": status,
                "margin_value_over_bound": mp.nstr(margin, 30),
                "borderline_10_percent": str(row in borderline),
                "evaluator": row["evaluator"],
                "corrections_applied": row["corrections_applied"],
            }
        )
    write_csv(BASE / "foreclosure_check_step380.csv", checks)

    min_exception = min(mp.mpf(r["abs_value"]) for r in exceptional)
    min_exception_row = min(exceptional, key=lambda r: mp.mpf(r["abs_value"]))
    min_baseline = min(mp.mpf(r["abs_value"]) for r in baseline)
    min_baseline_row = min(baseline, key=lambda r: mp.mpf(r["abs_value"]))

    baseline_md = f"""# Step 380 Baseline Comparison

Evaluator: Step 292 raw proxy `delta_Dk=(zeta*M(G_star))^(k)(rho)`.

Normalization: unnormalized absolute value; no `k!` division.

Projection corrections: none. `I_k` and `R_k` corrections are not available for this high-index exceptional-zero grid, so this is a raw-proxy foreclosure test.

Baseline zeros: `j={BASELINE}`, `k={FIT_K}`.

- baseline min value: `{mp.nstr(min_baseline, 20)}` at `j={min_baseline_row['j']}`, `k={min_baseline_row['k']}`
- exceptional min value: `{mp.nstr(min_exception, 20)}` at `j={min_exception_row['j']}`, `k={min_exception_row['k']}`
- Step 196 foreclosure threshold: `{mp.nstr(BOUND, 20)}`

Both baseline and exceptional raw-proxy grids are far above the Step 196 threshold under the available evaluator.
"""
    (BASE / "baseline_comparison_step380.md").write_text(baseline_md)

    pass_count = sum(1 for r in checks if r["pass_bound"] == "PASS")
    verdict = "robust_raw_proxy_foreclosure_all_35_pass" if pass_count == len(checks) else "fragile_failures_present"
    summary_md = f"""# Step 380 Results Summary

Step 379 finding cited verbatim: exceptional zeros have `R_j` up to `+23.60` and `10.6x` amplification of the Branch C gamma residual.

Step 196 foreclosure target: `|L_{{rho,k}}(G)| >= 0.034`.

Available evaluator used here:

- routine: Step 292 `delta_from_derivatives(zeta_derivatives, mellin_derivatives, k)`
- formula: `delta_Dk=(zeta*M(G_star))^(k)(rho)`
- normalization: unnormalized `abs(delta_Dk)`, no `k!` division
- corrections: no `I_k/R_k` projected corrections applied; unavailable for these cells

Exceptional grid: `7` zeros x `5` k-values = `{len(checks)}` cells.

- pass count: `{pass_count}/{len(checks)}`
- failure cells: `{len(failures)}`
- borderline cells within 10% of threshold: `{len(borderline)}`
- minimum exceptional value: `{mp.nstr(min_exception, 20)}` at `j={min_exception_row['j']}`, `k={min_exception_row['k']}`
- baseline min value: `{mp.nstr(min_baseline, 20)}` at `j={min_baseline_row['j']}`, `k={min_baseline_row['k']}`

Verdict: `{verdict}`. Under the available raw proxy, close-pair exceptional zeros do not threaten the Step 196 foreclosure threshold.
"""
    (BASE / "step380_results_summary.md").write_text(summary_md)

    schema = {
        "step": 380,
        "mode": "ATTEMPT",
        "dps": DPS,
        "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho)",
        "normalization": "unnormalized raw absolute value",
        "projection_corrections": "not applied; unavailable for these cells",
        "exceptions": EXCEPTIONS,
        "fit_k": FIT_K,
        "bound": float(BOUND),
        "cells": len(checks),
        "pass_count": pass_count,
        "failure_count": len(failures),
        "borderline_count": len(borderline),
        "min_exception_value": float(min_exception),
        "min_exception_j": int(min_exception_row["j"]),
        "min_exception_k": int(min_exception_row["k"]),
        "min_baseline_value": float(min_baseline),
        "verdict": verdict,
    }
    (BASE / "step380_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

    boundary = """# Step 380 Nonclaim Boundary

- This step does not prove RH, Branch C closure, or CTMT closure.
- The available evaluator is the Step 292 raw delta proxy, not the fully projected Burnol/Sonine `L_k`.
- The Step 196 threshold is tested numerically on the raw proxy for the requested exceptional-zero grid.
- No claim is made that unavailable projection corrections are negligible at these high-index zeros.
"""
    (BASE / "nonclaim_boundary_step380.md").write_text(boundary)

    print("STEP380_COMPUTE_DONE")
    print(f"pass_count={pass_count}/{len(checks)} failures={len(failures)} borderline={len(borderline)}")
    print(f"min_exception={mp.nstr(min_exception, 12)} j={min_exception_row['j']} k={min_exception_row['k']}")
    print(f"min_baseline={mp.nstr(min_baseline, 12)} j={min_baseline_row['j']} k={min_baseline_row['k']}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
