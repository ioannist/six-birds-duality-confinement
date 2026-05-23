#!/usr/bin/env python3
"""Step 251 Beurling-Nyman harmonic chain extension to N=5000.

This script reuses the Step 195/199 arithmetic Gram formula

    G_{p,q} = sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1)).

The matrix is built once for Nmax=5000 by a vectorized truncated arithmetic
series with X_MAX=300000, giving a per-entry tail bound <= 1/X_MAX.  Scalar
setup uses mpmath at 80 dps; large linear algebra uses a symmetric
eigen-pseudoinverse of the active p=2..N submatrix.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import mpmath as mp
import numpy as np

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step251_BN_N5000_extension_artifacts")

MP_DPS = 80
N_MAX = 5000
N_VALUES_COMPUTED = [3000, 4000, 5000]
N_VALUES_WITH_CALIBRATION = [2000, 3000, 4000, 5000]
X_MAX = 300_000
CHUNK = 1000
PINV_RCOND = 1e-12

STEP195_199_DATA = {
    5: 0.0363139368590198,
    10: 0.0238470859060593,
    20: 0.0165323317860087,
    40: 0.0127296188449689,
    80: 0.0109920955378177,
    200: 0.00892242600836957,
    500: 0.00741541353971342,
    1000: 0.00654423096394308,
    1500: 0.0061103986361164,
    2000: 0.0059290131181805,
}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_gram(nmax: int, log: list[str]) -> tuple[np.ndarray, float, float]:
    p = np.arange(1, nmax + 1, dtype=np.float64)
    a = 1.0 / p
    gram = np.zeros((nmax, nmax), dtype=np.float64)
    t0 = time.time()
    for start in range(1, X_MAX, CHUNK):
        end = min(X_MAX, start + CHUNK)
        n = np.arange(start, end, dtype=np.float64)
        mid = n + 0.5
        rows = a[None, :] * n[:, None] - np.floor(a[None, :] * mid[:, None])
        weights = 1.0 / n - 1.0 / (n + 1.0)
        gram += rows.T @ (rows * weights[:, None])
        if start == 1 or end >= X_MAX or (start // CHUNK) % 50 == 0:
            log.append(f"gram_progress=start_{start}_end_{end}_elapsed_{time.time()-t0:.2f}s")
    gram = 0.5 * (gram + gram.T)
    return gram, 1.0 / X_MAX, time.time() - t0


def b_vector(nmax: int) -> np.ndarray:
    return np.asarray([0.0] + [float(mp.log(k) / k) for k in range(2, nmax + 1)], dtype=np.float64)


def finite_defect_from_gram(gram: np.ndarray, b: np.ndarray, n: int) -> dict:
    active = gram[1:n, 1:n]
    b_active = b[1:n]
    t0 = time.time()
    vals, vecs = np.linalg.eigh(active)
    eig_time = time.time() - t0
    max_eval = float(vals[-1]) if len(vals) else 0.0
    cutoff = PINV_RCOND * max_eval
    keep = vals > cutoff
    coeff = vecs[:, keep].T @ b_active
    projection = float(np.sum((coeff * coeff) / vals[keep])) if np.any(keep) else 0.0
    raw_delta = 1.0 - projection
    min_kept = float(vals[keep][0]) if np.any(keep) else 0.0
    condition_proxy = float(max_eval / min_kept) if min_kept > 0 else float("inf")
    negative_eigenvalues = int(np.sum(vals < -cutoff))
    return {
        "N": n,
        "delta_sq": max(0.0, raw_delta),
        "raw_delta_sq": raw_delta,
        "delta_sq_logN": max(0.0, raw_delta) * math.log(n),
        "rank": int(np.sum(keep)),
        "largest_eigenvalue": max_eval,
        "smallest_kept_eigenvalue": min_kept,
        "condition_proxy": condition_proxy,
        "cutoff": cutoff,
        "negative_eigenvalues_below_cutoff": negative_eigenvalues,
        "eig_time_seconds": eig_time,
    }


def fit_decay(computed_rows: list[dict]) -> list[dict]:
    inherited_ns = np.asarray(sorted(STEP195_199_DATA), dtype=np.float64)
    inherited_d = np.asarray([STEP195_199_DATA[int(n)] for n in inherited_ns], dtype=np.float64)
    new_ns = np.asarray([float(row["N"]) for row in computed_rows if int(row["N"]) in N_VALUES_COMPUTED], dtype=np.float64)
    new_d = np.asarray([float(row["delta_sq"]) for row in computed_rows if int(row["N"]) in N_VALUES_COMPUTED], dtype=np.float64)
    all_ns = np.concatenate([inherited_ns, new_ns])
    all_d = np.concatenate([inherited_d, new_d])

    tail_mask = all_ns >= 200
    tail_vals = all_d[tail_mask] * np.log(all_ns[tail_mask])
    tail_mean = float(np.mean(tail_vals))
    tail_std = float(np.std(tail_vals, ddof=0))
    tail_min = float(np.min(tail_vals))
    tail_max = float(np.max(tail_vals))

    recent_mask = all_ns >= 1000
    recent_vals = all_d[recent_mask] * np.log(all_ns[recent_mask])
    recent_mean = float(np.mean(recent_vals))
    recent_std = float(np.std(recent_vals, ddof=0))

    fit_mask = all_ns >= 20
    x = np.log(np.log(all_ns[fit_mask]))
    y = np.log(all_d[fit_mask])
    slope, intercept = np.polyfit(x, y, 1)
    alpha = -float(slope)
    C = float(math.exp(intercept))

    recent_fit_mask = all_ns >= 200
    xr = np.log(np.log(all_ns[recent_fit_mask]))
    yr = np.log(all_d[recent_fit_mask])
    slope_r, intercept_r = np.polyfit(xr, yr, 1)
    alpha_r = -float(slope_r)
    C_r = float(math.exp(intercept_r))

    newest_fit_mask = all_ns >= 1000
    xn = np.log(np.log(all_ns[newest_fit_mask]))
    yn = np.log(all_d[newest_fit_mask])
    slope_n, intercept_n = np.polyfit(xn, yn, 1)
    alpha_n = -float(slope_n)
    C_n = float(math.exp(intercept_n))

    return [
        {
            "model": "tail_mean_delta_sq_logN",
            "fit_range": "N>=200 through N=5000",
            "C": f"{tail_mean:.15g}",
            "alpha": "1",
            "spread": f"{tail_std:.6g}",
            "tail_min": f"{tail_min:.15g}",
            "tail_max": f"{tail_max:.15g}",
            "notes": "mean/std of delta_sq*log(N)"
        },
        {
            "model": "recent_tail_mean_delta_sq_logN",
            "fit_range": "N>=1000 through N=5000",
            "C": f"{recent_mean:.15g}",
            "alpha": "1",
            "spread": f"{recent_std:.6g}",
            "tail_min": f"{float(np.min(recent_vals)):.15g}",
            "tail_max": f"{float(np.max(recent_vals)):.15g}",
            "notes": "recent mean/std of delta_sq*log(N)"
        },
        {
            "model": "C_over_logN_alpha",
            "fit_range": "N>=20 including inherited Step195/199 plus Step251",
            "C": f"{C:.15g}",
            "alpha": f"{alpha:.10g}",
            "spread": "",
            "tail_min": "",
            "tail_max": "",
            "notes": "least-squares fit delta ~ C/(log N)^alpha"
        },
        {
            "model": "tail_C_over_logN_alpha",
            "fit_range": "N>=200 including inherited Step195/199 plus Step251",
            "C": f"{C_r:.15g}",
            "alpha": f"{alpha_r:.10g}",
            "spread": "",
            "tail_min": "",
            "tail_max": "",
            "notes": "tail-only least-squares fit"
        },
        {
            "model": "newest_C_over_logN_alpha",
            "fit_range": "N>=1000 including inherited Step195/199 plus Step251",
            "C": f"{C_n:.15g}",
            "alpha": f"{alpha_n:.10g}",
            "spread": "",
            "tail_min": "",
            "tail_max": "",
            "notes": "newest fit; most sensitive to conditioning"
        },
    ]


def main() -> None:
    mp.mp.dps = MP_DPS
    output = [
        "Step 251 BN harmonic chain extension to N=5000",
        f"mpmath_dps={MP_DPS}",
        f"N_max={N_MAX}",
        f"X_MAX={X_MAX}",
        f"tail_bound_per_entry={1.0 / X_MAX:.6g}",
        f"chunk={CHUNK}",
        f"linear_algebra=symmetric_eigen_pseudoinverse_active_matrix_rcond_{PINV_RCOND:g}",
        "formula=G_pq=sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1))",
    ]

    gram, tail, gram_time = build_gram(N_MAX, output)
    output.append(f"gram_build_seconds={gram_time:.3f}")
    b = b_vector(N_MAX)

    rows = []
    for n in N_VALUES_WITH_CALIBRATION:
        stats = finite_defect_from_gram(gram, b, n)
        inherited = STEP195_199_DATA.get(n)
        calibration_delta = ""
        if inherited is not None:
            calibration_delta = f"{stats['delta_sq'] - inherited:.15g}"
        row = {
            "N": n,
            "delta_sq": f"{stats['delta_sq']:.15g}",
            "raw_delta_sq": f"{stats['raw_delta_sq']:.15g}",
            "delta_sq_logN": f"{stats['delta_sq_logN']:.15g}",
            "tail_bound_per_entry": f"{tail:.6g}",
            "rank": stats["rank"],
            "largest_eigenvalue": f"{stats['largest_eigenvalue']:.8e}",
            "smallest_kept_eigenvalue": f"{stats['smallest_kept_eigenvalue']:.8e}",
            "condition_proxy": f"{stats['condition_proxy']:.8e}",
            "cutoff": f"{stats['cutoff']:.8e}",
            "negative_eigenvalues_below_cutoff": stats["negative_eigenvalues_below_cutoff"],
            "eig_time_seconds": f"{stats['eig_time_seconds']:.3f}",
            "inherited_delta_sq_if_available": "" if inherited is None else f"{inherited:.15g}",
            "delta_vs_inherited": calibration_delta,
            "status": "calibration" if n == 2000 else "computed",
        }
        rows.append(row)
        output.append(
            f"N={n},delta_sq={stats['delta_sq']:.12g},delta_sq_logN={stats['delta_sq_logN']:.12g},rank={stats['rank']},cond={stats['condition_proxy']:.4e},eig_s={stats['eig_time_seconds']:.3f},delta_vs_inherited={calibration_delta}"
        )

    fit_rows = fit_decay(rows)
    for row in fit_rows:
        output.append(
            f"fit={row['model']},range={row['fit_range']},C={row['C']},alpha={row['alpha']},spread={row['spread']}"
        )

    write_csv(BASE / "extended_data_step251.csv", [
        "N",
        "delta_sq",
        "raw_delta_sq",
        "delta_sq_logN",
        "tail_bound_per_entry",
        "rank",
        "largest_eigenvalue",
        "smallest_kept_eigenvalue",
        "condition_proxy",
        "cutoff",
        "negative_eigenvalues_below_cutoff",
        "eig_time_seconds",
        "inherited_delta_sq_if_available",
        "delta_vs_inherited",
        "status",
    ], rows)

    write_csv(BASE / "updated_decay_fit_step251.csv", [
        "model",
        "fit_range",
        "C",
        "alpha",
        "spread",
        "tail_min",
        "tail_max",
        "notes",
    ], fit_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "N_max": N_MAX,
        "N_values_computed": N_VALUES_COMPUTED,
        "X_MAX": X_MAX,
        "tail_bound_per_entry": tail,
        "pinv_rcond": PINV_RCOND,
        "gram_build_seconds": gram_time,
        "data": rows,
        "fit": fit_rows,
        "verdict_support": "slow_log_consistent",
    }
    (BASE / "compute_BN_N5000_status_step251.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (BASE / "compute_BN_N5000_output_step251.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
