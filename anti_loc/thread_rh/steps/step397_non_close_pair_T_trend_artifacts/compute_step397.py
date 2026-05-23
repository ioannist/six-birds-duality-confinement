#!/usr/bin/env python3
"""Step 397: non-close-pair high-T trend for the Step-292 raw proxy.

This step deliberately uses the Step 292 raw proxy

    delta_Dk = (zeta * M(G_star))^(k)(rho)

and does not relabel it as the fully projected Branch C quantity.  The
sample is the requested every-25 grid j=25..500, filtered to s_min > 1.5.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step397_non_close_pair_T_trend_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

DPS = 80
K = 5
THRESHOLD = mp.mpf("0.034")
J_CANDIDATES = list(range(25, 501, 25))
S_MIN_CUTOFF = mp.mpf("1.5")


def load_step292():
    spec = importlib.util.spec_from_file_location("step292_for_step397", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step292_for_step397"] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def mpstr(x: mp.mpf | mp.mpc, digits: int = 50) -> str:
    return mp.nstr(x, digits)


def zeta_height_cache(indices: set[int]) -> dict[int, mp.mpf]:
    mp.mp.dps = DPS
    out: dict[int, mp.mpf] = {}
    for j in sorted(indices):
        out[j] = mp.im(mp.zetazero(j))
    return out


def raw_delta_abs(step292, gamma: mp.mpf) -> mp.mpf:
    mp.mp.dps = DPS
    zds = step292.zeta_derivatives(gamma, K, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, K, DPS)
    return abs(step292.delta_from_derivatives(zds, mds, K))


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def future_linear_crossing(a: float, b: float, threshold: float, max_t: float) -> tuple[str, str]:
    if abs(b) < 1e-18:
        return "", "flat_no_crossing"
    root = (threshold - a) / b
    if root > max_t:
        return f"{root:.12g}", "future_crossing"
    if root > 0:
        return f"{root:.12g}", "past_or_in_sample_crossing"
    return "", "no_positive_crossing"


def future_quadratic_crossing(a: float, b: float, c: float, threshold: float, max_t: float) -> tuple[str, str]:
    coeff = [c, b, a - threshold]
    roots = np.roots(coeff)
    real_roots = sorted(float(np.real(r)) for r in roots if abs(np.imag(r)) < 1e-8 and np.real(r) > 0)
    future = [r for r in real_roots if r > max_t]
    if future:
        return f"{future[0]:.12g}", "future_crossing"
    if real_roots:
        return f"{real_roots[-1]:.12g}", "past_or_in_sample_crossing"
    return "", "no_real_positive_crossing"


def future_power_crossing(a: float, alpha: float, threshold: float, max_t: float) -> tuple[str, str]:
    if a <= 0 or alpha <= 0:
        return "", "nondecaying_or_invalid_power"
    root = (a / threshold) ** (1.0 / alpha)
    if root > max_t:
        return f"{root:.12g}", "future_crossing"
    if root > 0:
        return f"{root:.12g}", "past_or_in_sample_crossing"
    return "", "no_positive_crossing"


def fit_trends(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    t = np.array([float(r["T_float"]) for r in rows], dtype=float)
    y = np.array([float(r["abs_delta_Dk_float"]) for r in rows], dtype=float)
    threshold = float(THRESHOLD)
    max_t = float(np.max(t))
    out: list[dict[str, object]] = []

    x_lin = np.column_stack([np.ones_like(t), t])
    a_lin, b_lin = np.linalg.lstsq(x_lin, y, rcond=None)[0]
    pred_lin = x_lin @ np.array([a_lin, b_lin])
    cross, status = future_linear_crossing(float(a_lin), float(b_lin), threshold, max_t)
    out.append({
        "model": "linear_a_plus_bT",
        "a": f"{a_lin:.16e}",
        "b": f"{b_lin:.16e}",
        "c_or_alpha": "",
        "rmse": f"{rmse(y, pred_lin):.16e}",
        "threshold": f"{threshold:.16e}",
        "crossing_T_for_threshold": cross,
        "crossing_status": status,
    })

    x_quad = np.column_stack([np.ones_like(t), t, t * t])
    a_q, b_q, c_q = np.linalg.lstsq(x_quad, y, rcond=None)[0]
    pred_q = x_quad @ np.array([a_q, b_q, c_q])
    cross, status = future_quadratic_crossing(float(a_q), float(b_q), float(c_q), threshold, max_t)
    out.append({
        "model": "quadratic_a_plus_bT_plus_cT2",
        "a": f"{a_q:.16e}",
        "b": f"{b_q:.16e}",
        "c_or_alpha": f"{c_q:.16e}",
        "rmse": f"{rmse(y, pred_q):.16e}",
        "threshold": f"{threshold:.16e}",
        "crossing_T_for_threshold": cross,
        "crossing_status": status,
    })

    log_t = np.log(t)
    log_y = np.log(y)
    x_pow = np.column_stack([np.ones_like(log_t), -log_t])
    log_a, alpha = np.linalg.lstsq(x_pow, log_y, rcond=None)[0]
    a_p = math.exp(float(log_a))
    pred_p = a_p / (t ** float(alpha))
    cross, status = future_power_crossing(a_p, float(alpha), threshold, max_t)
    out.append({
        "model": "power_decay_a_over_T_alpha",
        "a": f"{a_p:.16e}",
        "b": "",
        "c_or_alpha": f"{alpha:.16e}",
        "rmse": f"{rmse(y, pred_p):.16e}",
        "threshold": f"{threshold:.16e}",
        "crossing_T_for_threshold": cross,
        "crossing_status": status,
    })
    return out


def write_schema(sample_size: int, pass_count: int, fail_count: int, best_model: str) -> None:
    schema = {
        "step": 397,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "dps": DPS,
        "k": K,
        "candidate_j_grid": "25,50,75,...,500",
        "non_close_pair_filter": "s_min > 1.5",
        "sample_size": sample_size,
        "foreclosure_threshold": str(THRESHOLD),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "best_trend_model_by_rmse": best_model,
        "raw_proxy": "Step292 delta_Dk=(zeta*M(G_star))^(k)(rho_j)",
        "required_files": [
            "non_cp_delta_Dk_step397.csv",
            "trend_fits_step397.csv",
            "step397_results_summary.md",
            "step397_schema.json",
            "nonclaim_boundary_step397.md",
            "run_step397_checks.py",
        ],
    }
    (ART / "step397_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    step292 = load_step292()
    indices = {j for base in J_CANDIDATES for j in (base - 1, base, base + 1)}
    heights = zeta_height_cache(indices)

    rows: list[dict[str, object]] = []
    excluded: list[str] = []
    for j in J_CANDIDATES:
        t_prev = heights[j - 1]
        t = heights[j]
        t_next = heights[j + 1]
        s_bwd = t - t_prev
        s_fwd = t_next - t
        s_min = min(s_bwd, s_fwd)
        if s_min <= S_MIN_CUTOFF:
            excluded.append(f"j={j}:s_min={mpstr(s_min, 20)}")
            continue
        val = raw_delta_abs(step292, t)
        rows.append({
            "j": j,
            "T": mpstr(t),
            "T_float": f"{float(t):.16e}",
            "s_bwd": mpstr(s_bwd),
            "s_fwd": mpstr(s_fwd),
            "s_min": mpstr(s_min),
            "k": K,
            "abs_delta_Dk": mpstr(val),
            "abs_delta_Dk_float": f"{float(val):.16e}",
            "threshold": mpstr(THRESHOLD),
            "pass_foreclosure": "PASS" if val >= THRESHOLD else "FAIL",
            "sample_type": "non_close_pair_smin_gt_1_5",
            "dps": DPS,
            "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho_j); not fully projected L_k",
        })

    fieldnames = [
        "j", "T", "T_float", "s_bwd", "s_fwd", "s_min", "k",
        "abs_delta_Dk", "abs_delta_Dk_float", "threshold", "pass_foreclosure",
        "sample_type", "dps", "evaluator",
    ]
    write_csv(ART / "non_cp_delta_Dk_step397.csv", rows, fieldnames)

    trend_rows = fit_trends(rows)
    write_csv(ART / "trend_fits_step397.csv", trend_rows, [
        "model", "a", "b", "c_or_alpha", "rmse", "threshold",
        "crossing_T_for_threshold", "crossing_status",
    ])

    values = [float(r["abs_delta_Dk_float"]) for r in rows]
    pass_count = sum(1 for r in rows if r["pass_foreclosure"] == "PASS")
    fail_count = len(rows) - pass_count
    best = min(trend_rows, key=lambda r: float(r["rmse"]))
    min_row = min(rows, key=lambda r: float(r["abs_delta_Dk_float"]))
    max_row = max(rows, key=lambda r: float(r["abs_delta_Dk_float"]))

    if fail_count:
        verdict = "non_cp_failures_observed_high_T_uniform_driver_supported"
    elif min(values) > float(THRESHOLD) * 1.1:
        if best["crossing_status"] == "future_crossing":
            verdict = "non_cp_passes_sample_but_best_trend_predicts_future_high_T_risk"
        else:
            verdict = "non_cp_stays_safely_above_threshold_in_sample"
    else:
        verdict = "non_cp_borderline_above_threshold"

    summary = f"""# Step 397 Results Summary

## Inputs and Citations
- Step 196 foreclosure threshold used verbatim: `|L_k|>=0.034`.
- Step 292 raw proxy used verbatim: `delta_Dk=(zeta*M(G_star))^(k)(rho_j)`.
- Step 392 context used verbatim: one high-j raw-proxy failure at `j=470, k=5`.
- Step 395 context used verbatim: close-pair failure rate `15.6%`.
- Step 396 context used verbatim: `T is dominant predictor (r=0.329); s_min within CP not predictive (r=-0.021)`.

## Sample
- Candidate grid: `j = 25, 50, ..., 500`.
- Non-close-pair filter: `s_min > 1.5`.
- Included non-CP zeros: {len(rows)}.
- Excluded grid points: {", ".join(excluded) if excluded else "none"}.

## Foreclosure Statistics
- Threshold: {mpstr(THRESHOLD)}.
- Pass/fail: {pass_count}/{fail_count}.
- Minimum `|delta_Dk(k=5)|`: {min_row["abs_delta_Dk"]} at `j={min_row["j"]}`.
- Maximum `|delta_Dk(k=5)|`: {max_row["abs_delta_Dk"]} at `j={max_row["j"]}`.
- Mean `|delta_Dk(k=5)|`: {sum(values) / len(values):.16e}.

## Trend Fits
- Best model by RMSE: `{best["model"]}`.
- Best-model parameters: `a={best["a"]}`, `b={best["b"]}`, `c_or_alpha={best["c_or_alpha"]}`.
- Best-model RMSE: `{best["rmse"]}`.
- Best-model threshold crossing: `{best["crossing_T_for_threshold"]}` ({best["crossing_status"]}).

## Verdict
{verdict}.

This is a raw-proxy foreclosure diagnostic, not a theorem and not a claim about RH.
"""
    (ART / "step397_results_summary.md").write_text(summary, encoding="utf-8")

    nonclaim = """# Step 397 Nonclaim Boundary

This step uses the Step 292 raw proxy `delta_Dk=(zeta*M(G_star))^(k)(rho_j)`.
It does not assert equality with the fully projected Branch C `L_k` unless
projector corrections are separately supplied.

No RH claim is made. No CTMT theorem is strengthened beyond the sampled raw-proxy
evidence recorded in the artifacts.
"""
    (ART / "nonclaim_boundary_step397.md").write_text(nonclaim, encoding="utf-8")
    write_schema(len(rows), pass_count, fail_count, str(best["model"]))


if __name__ == "__main__":
    main()
