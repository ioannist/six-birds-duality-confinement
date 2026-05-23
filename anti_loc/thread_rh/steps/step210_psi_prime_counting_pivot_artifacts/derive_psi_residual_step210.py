#!/usr/bin/env python3
"""Step 210 symbolic/numerical formulation for the Chebyshev psi carrier."""

from __future__ import annotations

import csv
import math
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step210_psi_prime_counting_pivot_artifacts")


def primes_upto(n: int) -> list[int]:
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : n + 1 : step] = [False] * (((n - start) // step) + 1)
    return [i for i, ok in enumerate(sieve) if ok]


def psi(x: int) -> float:
    total = 0.0
    for p in primes_upto(x):
        pk = p
        while pk <= x:
            total += math.log(p)
            pk *= p
    return total


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    xs = [10, 100, 1000, 10000]
    rows = []
    for x in xs:
        val = psi(x)
        denom_von_koch = math.sqrt(x) * (math.log(x) ** 2)
        rows.append(
            {
                "x": x,
                "psi_x": f"{val:.12f}",
                "psi_minus_x": f"{val - x:.12f}",
                "sqrt_x_log2_x": f"{denom_von_koch:.12f}",
                "normalized_abs_error": f"{abs(val - x) / denom_von_koch:.12f}",
                "status": "finite_sample_not_RH_evidence",
            }
        )
    with (BASE / "psi_samples_step210.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("Step 210 psi residual formulation")
    print("Xi_psi(epsilon)=limsup |psi(x)-x|/x^(1/2+epsilon)")
    print("Xi_psi=limsup |psi(x)-x|/(sqrt(x) log^2 x)")
    print("von Koch 1901: Xi_psi finite iff RH")
    print("verdict=V_psi_CRCFT_TE")


if __name__ == "__main__":
    main()
