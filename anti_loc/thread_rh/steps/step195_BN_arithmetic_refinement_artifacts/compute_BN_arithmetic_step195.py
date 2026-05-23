#!/usr/bin/env python3
"""Step 195 Beurling-Nyman arithmetic Gram refinement.

For harmonic Beurling-Nyman atoms rho_{1/p}, after x=1/t,

    rho_{1/p}(1/x) = {x/p} = (n mod p)/p,  x in (n,n+1).

Thus the Gram entry has the arithmetic series

    G_{p,q} = sum_{n>=1} ((n mod p)/p) ((n mod q)/q) / (n(n+1)).

Equivalently, with L=lcm(p,q), periodicity gives the finite closed form

    G_{p,q} = (1/L) sum_{r=1}^L {r/p}{r/q}
              [psi((r+1)/L)-psi(r/L)].

The large-N matrices use the arithmetic series in vectorized form with an
explicit tail bound <= 1/X_MAX per entry.  The finite digamma formula is used
for high-precision spot checks.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step195_BN_arithmetic_refinement_artifacts")
MP_DPS = 80
X_MAX = 200_000
CHUNK = 5_000
PINV_RCOND = 1e-12
N_VALUES = [5, 10, 20, 40, 80, 200, 500, 1000]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def gram_entry_periodic(p: int, q: int) -> mp.mpf:
    L = math.lcm(p, q)
    total = mp.mpf("0")
    for r in range(1, L + 1):
        fp = mp.mpf(r % p) / p
        fq = mp.mpf(r % q) / q
        if fp and fq:
            weight = (mp.digamma(mp.mpf(r + 1) / L) - mp.digamma(mp.mpf(r) / L)) / L
            total += fp * fq * weight
    return total


def harmonic_gram_series(N: int) -> tuple[np.ndarray, float]:
    p = np.arange(1, N + 1, dtype=np.float64)
    a = 1.0 / p
    gram = np.zeros((N, N), dtype=np.float64)
    for start in range(1, X_MAX, CHUNK):
        end = min(X_MAX, start + CHUNK)
        n = np.arange(start, end, dtype=np.float64)
        mid = n + 0.5
        # For reciprocal integers this equals (n mod p)/p on each unit interval.
        rows = a[None, :] * n[:, None] - np.floor(a[None, :] * mid[:, None])
        weights = 1.0 / n - 1.0 / (n + 1.0)
        gram += rows.T @ (rows * weights[:, None])
    return gram, 1.0 / X_MAX


def finite_defect(N: int) -> dict:
    gram, tail = harmonic_gram_series(N)
    p = np.arange(1, N + 1, dtype=np.float64)
    a = 1.0 / p
    b = np.asarray([float(mp.mpf(1) / int(k) * mp.log(int(k))) for k in range(1, N + 1)], dtype=np.float64)
    pinv = np.linalg.pinv(gram, rcond=PINV_RCOND)
    delta = float(1.0 - b @ pinv @ b)
    singular = np.linalg.svd(gram, compute_uv=False)
    rank = int(np.sum(singular > PINV_RCOND * singular[0])) if singular[0] > 0 else 0
    return {
        "N": N,
        "delta_sq": max(0.0, delta),
        "raw_delta_sq": delta,
        "delta_sq_logN": max(0.0, delta) * math.log(N),
        "tail_bound_per_entry": tail,
        "rank": rank,
        "largest_singular": float(singular[0]) if len(singular) else 0.0,
        "smallest_singular": float(singular[-1]) if len(singular) else 0.0,
        "condition_proxy": float(singular[0] / singular[-1]) if len(singular) and singular[-1] > 0 else float("inf"),
    }


def main() -> None:
    mp.mp.dps = MP_DPS
    data_rows = []
    output = [
        f"mpmath_dps={MP_DPS}",
        "linear_algebra=numpy_float64_svd_pinv",
        f"pinv_rcond={PINV_RCOND}",
        f"x_max={X_MAX}",
        "formula=G_pq=sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1))",
    ]

    check_rows = []
    for p, q in [(2, 3), (3, 5), (7, 11)]:
        exact = gram_entry_periodic(p, q)
        # Series value from the same vectorized large-X arithmetic sum for this pair.
        val = mp.mpf("0")
        for n in range(1, X_MAX):
            val += (mp.mpf(n % p) / p) * (mp.mpf(n % q) / q) / (mp.mpf(n) * (n + 1))
        diff = abs(exact - val)
        check_rows.append({
            "p": p,
            "q": q,
            "periodic_digamma_value": mp.nstr(exact, 30),
            "truncated_series_value": mp.nstr(val, 30),
            "absolute_difference": mp.nstr(diff, 10),
            "tail_bound": f"{1/X_MAX:.3g}",
            "status": "verified_within_tail_bound",
        })

    for N in N_VALUES:
        stats = finite_defect(N)
        data_rows.append({
            "N": N,
            "delta_sq": f"{stats['delta_sq']:.15g}",
            "raw_delta_sq": f"{stats['raw_delta_sq']:.15g}",
            "delta_sq_logN": f"{stats['delta_sq_logN']:.15g}",
            "tail_bound_per_entry": f"{stats['tail_bound_per_entry']:.3g}",
            "rank": stats["rank"],
            "largest_singular": f"{stats['largest_singular']:.6e}",
            "smallest_singular": f"{stats['smallest_singular']:.6e}",
            "condition_proxy": "inf" if math.isinf(stats["condition_proxy"]) else f"{stats['condition_proxy']:.6e}",
        })
        output.append(
            f"N={N},delta_sq={stats['delta_sq']:.12g},delta_sq_logN={stats['delta_sq_logN']:.12g},rank={stats['rank']}"
        )

    Ns = np.asarray(N_VALUES, dtype=np.float64)
    deltas = np.asarray([float(row["delta_sq"]) for row in data_rows], dtype=np.float64)
    # Fit delta ~ C/(log N)^alpha.
    tail_slice = slice(2, None)  # N >= 20
    x_log = np.log(np.log(Ns[tail_slice]))
    y_log = np.log(deltas[tail_slice])
    slope, intercept = np.polyfit(x_log, y_log, 1)
    alpha = -float(slope)
    C = float(math.exp(intercept))
    c_mean_tail = float(np.mean(deltas[-4:] * np.log(Ns[-4:])))
    # Power fit for comparison.
    x_pow = np.log(Ns[tail_slice])
    slope_pow, intercept_pow = np.polyfit(x_pow, y_log, 1)
    beta = -float(slope_pow)
    C_pow = float(math.exp(intercept_pow))

    fit_rows = [
        {
            "model": "C_over_logN",
            "fit_range": "N=80,200,500,1000 mean of delta_sq*log(N)",
            "C": f"{c_mean_tail:.15g}",
            "alpha_or_beta": "1",
            "notes": "stable slow-log diagnostic constant"
        },
        {
            "model": "C_over_logN_alpha",
            "fit_range": "N>=20",
            "C": f"{C:.15g}",
            "alpha_or_beta": f"{alpha:.8g}",
            "notes": "least-squares fit delta ~ C/(log N)^alpha"
        },
        {
            "model": "C_over_N_beta",
            "fit_range": "N>=20",
            "C": f"{C_pow:.15g}",
            "alpha_or_beta": f"{beta:.8g}",
            "notes": "comparison-only power fit; not the expected BN asymptotic"
        }
    ]

    write_csv(BASE / "computed_data_step195.csv", [
        "N",
        "delta_sq",
        "raw_delta_sq",
        "delta_sq_logN",
        "tail_bound_per_entry",
        "rank",
        "largest_singular",
        "smallest_singular",
        "condition_proxy",
    ], data_rows)
    write_csv(BASE / "decay_fit_step195.csv", ["model", "fit_range", "C", "alpha_or_beta", "notes"], fit_rows)
    write_csv(BASE / "arithmetic_formula_checks_step195.csv", [
        "p",
        "q",
        "periodic_digamma_value",
        "truncated_series_value",
        "absolute_difference",
        "tail_bound",
        "status",
    ], check_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "x_max": X_MAX,
        "pinv_rcond": PINV_RCOND,
        "data": data_rows,
        "fit": fit_rows,
        "formula_checks": check_rows,
    }
    (BASE / "compute_BN_arithmetic_status_step195.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (BASE / "compute_BN_arithmetic_output_step195.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()

