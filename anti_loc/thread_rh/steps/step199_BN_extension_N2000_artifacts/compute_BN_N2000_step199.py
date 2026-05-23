#!/usr/bin/env python3
"""Step 199 Beurling-Nyman harmonic chain extension.

This reuses the Step 195 arithmetic Gram formula

    G_{p,q} = sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1)).

For feasibility at N=2000, the script builds one Nmax=2000 truncated Gram
matrix using the vectorized Step 195 arithmetic series and evaluates the
active submatrices for N=1000,1500,2000.  Scalar setup uses mpmath at 80 dps.
The large linear algebra uses a symmetric eigen-pseudoinverse on the active
matrix (p=2..N) because a full 2000x2000 mpmath SVD is not feasible in this
runtime.  The N=1000 calibration against Step 195 is reported explicitly.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step199_BN_extension_N2000_artifacts")

MP_DPS = 80
N_MAX = 2000
N_VALUES_COMPUTED = [1000, 1500, 2000]
X_MAX = 40000
CHUNK = 1000
PINV_RCOND = 1e-12

STEP195_DATA = {
    5: 0.0363139368590198,
    10: 0.0238470859060593,
    20: 0.0165323317860087,
    40: 0.0127296188449689,
    80: 0.0109920955378177,
    200: 0.00892242600836957,
    500: 0.00741541353971342,
    1000: 0.00654423096394308,
}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_gram(nmax: int) -> tuple[np.ndarray, float]:
    p = np.arange(1, nmax + 1, dtype=np.float64)
    a = 1.0 / p
    gram = np.zeros((nmax, nmax), dtype=np.float64)
    for start in range(1, X_MAX, CHUNK):
        end = min(X_MAX, start + CHUNK)
        n = np.arange(start, end, dtype=np.float64)
        mid = n + 0.5
        rows = a[None, :] * n[:, None] - np.floor(a[None, :] * mid[:, None])
        weights = 1.0 / n - 1.0 / (n + 1.0)
        gram += rows.T @ (rows * weights[:, None])
    gram = 0.5 * (gram + gram.T)
    return gram, 1.0 / X_MAX


def b_vector(nmax: int) -> np.ndarray:
    return np.asarray([0.0] + [float(mp.log(k) / k) for k in range(2, nmax + 1)], dtype=np.float64)


def finite_defect_from_gram(gram: np.ndarray, b: np.ndarray, n: int) -> dict:
    # Drop p=1 because rho_1 is identically zero and b_1=0.
    active = gram[1:n, 1:n]
    b_active = b[1:n]
    vals, vecs = np.linalg.eigh(active)
    max_eval = float(vals[-1]) if len(vals) else 0.0
    cutoff = PINV_RCOND * max_eval
    keep = vals > cutoff
    coeff = vecs[:, keep].T @ b_active
    projection = float(np.sum((coeff * coeff) / vals[keep])) if np.any(keep) else 0.0
    raw_delta = 1.0 - projection
    min_kept = float(vals[keep][0]) if np.any(keep) else 0.0
    condition_proxy = float(max_eval / min_kept) if min_kept > 0 else float("inf")
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
    }


def fit_decay(rows: list[dict]) -> list[dict]:
    inherited_ns = np.asarray(sorted(STEP195_DATA), dtype=np.float64)
    inherited_d = np.asarray([STEP195_DATA[int(n)] for n in inherited_ns], dtype=np.float64)
    new_ns = np.asarray([float(row["N"]) for row in rows if row["N"] in (1500, 2000)], dtype=np.float64)
    new_d = np.asarray([float(row["delta_sq"]) for row in rows if row["N"] in (1500, 2000)], dtype=np.float64)
    all_ns = np.concatenate([inherited_ns, new_ns])
    all_d = np.concatenate([inherited_d, new_d])

    tail_mask = all_ns >= 200
    tail_mean = float(np.mean(all_d[tail_mask] * np.log(all_ns[tail_mask])))
    tail_std = float(np.std(all_d[tail_mask] * np.log(all_ns[tail_mask]), ddof=0))

    fit_mask = all_ns >= 20
    x = np.log(np.log(all_ns[fit_mask]))
    y = np.log(all_d[fit_mask])
    slope, intercept = np.polyfit(x, y, 1)
    alpha = -float(slope)
    C = float(math.exp(intercept))

    recent_mask = all_ns >= 200
    x_recent = np.log(np.log(all_ns[recent_mask]))
    y_recent = np.log(all_d[recent_mask])
    slope_r, intercept_r = np.polyfit(x_recent, y_recent, 1)
    alpha_r = -float(slope_r)
    C_r = float(math.exp(intercept_r))

    return [
        {
            "model": "tail_mean_delta_sq_logN",
            "fit_range": "N=200,500,1000,1500,2000",
            "C": f"{tail_mean:.15g}",
            "alpha": "1",
            "spread": f"{tail_std:.6g}",
            "notes": "mean and population std of delta_sq*log(N)"
        },
        {
            "model": "C_over_logN_alpha",
            "fit_range": "N>=20 including Step195 inherited plus Step199 N=1500,2000",
            "C": f"{C:.15g}",
            "alpha": f"{alpha:.10g}",
            "spread": "",
            "notes": "least-squares fit delta ~ C/(log N)^alpha"
        },
        {
            "model": "recent_C_over_logN_alpha",
            "fit_range": "N>=200 including Step195 inherited plus Step199 N=1500,2000",
            "C": f"{C_r:.15g}",
            "alpha": f"{alpha_r:.10g}",
            "spread": "",
            "notes": "tail-only fit; more sensitive to truncation and conditioning"
        }
    ]


def main() -> None:
    mp.mp.dps = MP_DPS
    output = [
        "Step 199 BN harmonic chain extension",
        f"mpmath_dps={MP_DPS}",
        f"N_max={N_MAX}",
        f"X_MAX={X_MAX}",
        f"tail_bound_per_entry={1.0 / X_MAX:.6g}",
        f"linear_algebra=symmetric_eigen_pseudoinverse_active_matrix_rcond_{PINV_RCOND:g}",
        "formula=G_pq=sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1))",
        "note=full mpmath 2000x2000 SVD infeasible; Step195-comparable eigen pseudoinverse used",
    ]

    gram, tail = build_gram(N_MAX)
    b = b_vector(N_MAX)
    rows = []
    for n in N_VALUES_COMPUTED:
        stats = finite_defect_from_gram(gram, b, n)
        inherited = STEP195_DATA.get(n)
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
            "step195_delta_sq_if_available": "" if inherited is None else f"{inherited:.15g}",
            "delta_vs_step195": calibration_delta,
            "status": "computed",
        }
        rows.append(row)
        output.append(
            f"N={n},delta_sq={stats['delta_sq']:.12g},delta_sq_logN={stats['delta_sq_logN']:.12g},rank={stats['rank']},cond={stats['condition_proxy']:.4e},delta_vs_step195={calibration_delta}"
        )

    fit_rows = fit_decay([
        {"N": int(row["N"]), "delta_sq": float(row["delta_sq"])}
        for row in rows
    ])
    for row in fit_rows:
        output.append(
            f"fit={row['model']},range={row['fit_range']},C={row['C']},alpha={row['alpha']},spread={row['spread']}"
        )

    write_csv(BASE / "extended_data_step199.csv", [
        "N",
        "delta_sq",
        "raw_delta_sq",
        "delta_sq_logN",
        "tail_bound_per_entry",
        "rank",
        "largest_eigenvalue",
        "smallest_kept_eigenvalue",
        "condition_proxy",
        "step195_delta_sq_if_available",
        "delta_vs_step195",
        "status",
    ], rows)

    write_csv(BASE / "updated_decay_fit_step199.csv", [
        "model",
        "fit_range",
        "C",
        "alpha",
        "spread",
        "notes",
    ], fit_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "N_max": N_MAX,
        "X_MAX": X_MAX,
        "tail_bound_per_entry": tail,
        "pinv_rcond": PINV_RCOND,
        "data": rows,
        "fit": fit_rows,
        "verdict_support": "slow_log_consistent_with_truncation_caveat",
    }
    (BASE / "compute_BN_N2000_status_step199.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (BASE / "compute_BN_N2000_output_step199.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()

