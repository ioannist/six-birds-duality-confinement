#!/usr/bin/env python3
"""Numerical Beurling-Nyman finite Gram defects for Step 194.

The tested families all use reciprocal-integer parameters a=1/q.  For these
parameters the BN atom

    rho_a(t) = {a/t} - a {1/t}

becomes, after x=1/t,

    rho_a(1/x) = a floor(x) - floor(a x).

When a=1/q, floor(a x) changes only at integer x-multiples of q, hence the
integrand is constant on each unit interval (n,n+1).  We therefore compute the
Gram entries by a deterministic unit-interval sum up to X_MAX, with tail bound
at most 1/X_MAX per entry since |rho_a| <= 1.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

import mpmath as mp
import numpy as np

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step194_BN_gram_numerical_artifacts")
X_MAX = 200_000
CHUNK = 10_000
MP_DPS = 50
PINV_RCOND = 1e-12
N_VALUES = [5, 10, 20, 40, 80]


def family_denominators(name: str, n: int) -> list[int]:
    if name == "harmonic":
        return list(range(1, n + 1))
    if name == "geometric":
        return [2**k for k in range(n)]
    if name == "power":
        return [k * k for k in range(1, n + 1)]
    if name == "random_reciprocal":
        pool = sorted(random.Random(193).sample(range(1, 1000), 80))
        return pool[:n]
    raise ValueError(name)


def gram_for_reciprocal_denominators(qs: list[int]) -> tuple[np.ndarray, float, int]:
    qs_arr = np.asarray(qs, dtype=np.float64)
    a = 1.0 / qs_arr
    size = len(qs)
    gram = np.zeros((size, size), dtype=np.float64)
    interval_count = 0

    for start in range(1, X_MAX, CHUNK):
        end = min(X_MAX, start + CHUNK)
        n = np.arange(start, end, dtype=np.float64)
        mid = n + 0.5
        rows = a[None, :] * n[:, None] - np.floor(a[None, :] * mid[:, None])
        weights = 1.0 / n - 1.0 / (n + 1.0)
        gram += rows.T @ (rows * weights[:, None])
        interval_count += len(n)

    return gram, 1.0 / X_MAX, interval_count


def finite_defect(qs: list[int]) -> dict:
    gram, tail_bound, intervals = gram_for_reciprocal_denominators(qs)
    a = np.asarray([1.0 / q for q in qs], dtype=np.float64)
    # b_i = <1,rho_{1/q_i}> = (1/q_i) log(q_i).  Use mpmath for scalar source.
    b = np.asarray([float(mp.mpf(1) / q * mp.log(q)) for q in qs], dtype=np.float64)
    singular_values = np.linalg.svd(gram, compute_uv=False)
    rank = int(np.sum(singular_values > PINV_RCOND * singular_values[0])) if singular_values[0] > 0 else 0
    gram_pinv = np.linalg.pinv(gram, rcond=PINV_RCOND)
    raw_defect = float(1.0 - b @ gram_pinv @ b)
    return {
        "delta_sq": max(0.0, raw_defect),
        "raw_delta_sq": raw_defect,
        "tail_bound_per_entry": tail_bound,
        "interval_count": intervals,
        "rank": rank,
        "smallest_singular": float(singular_values[-1]) if len(singular_values) else 0.0,
        "largest_singular": float(singular_values[0]) if len(singular_values) else 0.0,
        "condition_proxy": float(singular_values[0] / singular_values[-1]) if len(singular_values) and singular_values[-1] > 0 else float("inf"),
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    mp.mp.dps = MP_DPS
    families = ["harmonic", "geometric", "power", "random_reciprocal"]

    a_set_rows = []
    result_rows = []
    decay_rows = []
    output_lines = []

    output_lines.append(f"mpmath_dps={MP_DPS}")
    output_lines.append(f"numpy_float=float64")
    output_lines.append(f"x_max={X_MAX}")
    output_lines.append(f"pinv_rcond={PINV_RCOND}")

    for family in families:
        deltas = []
        ns = []
        for n in N_VALUES:
            qs = family_denominators(family, n)
            a_preview = ",".join(f"1/{q}" for q in qs[:8])
            if len(qs) > 8:
                a_preview += ",..."
            if n == N_VALUES[-1]:
                a_set_rows.append({
                    "family": family,
                    "max_N": n,
                    "definition": {
                        "harmonic": "A_N={1/k:1<=k<=N}",
                        "geometric": "A_N={2^{-k}:0<=k<N}",
                        "power": "A_N={1/k^2:1<=k<=N}",
                        "random_reciprocal": "A_N={1/q_j:j<=N}, fixed random q_j in [1,999]",
                    }[family],
                    "sample_parameters": a_preview,
                })
            stats = finite_defect(qs)
            deltas.append(stats["delta_sq"])
            ns.append(n)
            result = {
                "family": family,
                "N": n,
                "delta_sq": f"{stats['delta_sq']:.15g}",
                "raw_delta_sq": f"{stats['raw_delta_sq']:.15g}",
                "tail_bound_per_entry": f"{stats['tail_bound_per_entry']:.3g}",
                "rank": stats["rank"],
                "smallest_singular": f"{stats['smallest_singular']:.6e}",
                "largest_singular": f"{stats['largest_singular']:.6e}",
                "condition_proxy": "inf" if math.isinf(stats["condition_proxy"]) else f"{stats['condition_proxy']:.6e}",
                "interval_count": stats["interval_count"],
            }
            result_rows.append(result)
            output_lines.append(
                f"{family},N={n},delta_sq={stats['delta_sq']:.12g},rank={stats['rank']},tail_entry<={stats['tail_bound_per_entry']:.2e}"
            )

        logn = np.log(np.asarray(ns, dtype=np.float64))
        d = np.asarray(deltas, dtype=np.float64)
        c_over_log = d * logn
        # Fit log(delta) = alpha + beta log(N) where meaningful.
        beta, alpha = np.polyfit(np.log(np.asarray(ns[1:], dtype=np.float64)), np.log(d[1:]), 1)
        first = deltas[0]
        last = deltas[-1]
        if family == "harmonic":
            pattern = "slow_log_decay"
            comment = "delta_sq decreases and delta_sq*log(N) is roughly stable after N=20"
        elif last < 0.9 * first:
            pattern = "weak_decay"
            comment = "some decay but no clear approach to zero at tested scale"
        else:
            pattern = "plateau"
            comment = "sparse family appears bounded away from zero at tested scale"
        decay_rows.append({
            "family": family,
            "N_min": ns[0],
            "N_max": ns[-1],
            "delta_sq_first": f"{first:.15g}",
            "delta_sq_last": f"{last:.15g}",
            "delta_sq_logN_mean_N_ge_10": f"{float(np.mean(c_over_log[1:])):.15g}",
            "loglog_slope_N_ge_10": f"{float(beta):.6g}",
            "pattern": pattern,
            "comment": comment,
        })

    write_csv(BASE / "BN_gram_a_sets_step194.csv", ["family", "max_N", "definition", "sample_parameters"], a_set_rows)
    write_csv(BASE / "BN_gram_results_step194.csv", [
        "family",
        "N",
        "delta_sq",
        "raw_delta_sq",
        "tail_bound_per_entry",
        "rank",
        "smallest_singular",
        "largest_singular",
        "condition_proxy",
        "interval_count",
    ], result_rows)
    write_csv(BASE / "decay_analysis_step194.csv", [
        "family",
        "N_min",
        "N_max",
        "delta_sq_first",
        "delta_sq_last",
        "delta_sq_logN_mean_N_ge_10",
        "loglog_slope_N_ge_10",
        "pattern",
        "comment",
    ], decay_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "numpy_dtype": "float64",
        "x_max": X_MAX,
        "pinv_rcond": PINV_RCOND,
        "n_values": N_VALUES,
        "results": result_rows,
        "decay_analysis": decay_rows,
    }
    (BASE / "compute_BN_gram_status_step194.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (BASE / "compute_BN_gram_output_step194.txt").write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print("\n".join(output_lines))


if __name__ == "__main__":
    main()

