#!/usr/bin/env python3
"""Step 209 symbolic/numerical formulation of the Riemann-Siegel Z carrier."""

from __future__ import annotations

import csv
from pathlib import Path

import mpmath as mp


mp.mp.dps = 50

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step209_riemann_siegel_Z_pivot_artifacts")


def theta(t: mp.mpf) -> mp.mpf:
    z = mp.mpc(mp.mpf("0.25"), t / 2)
    return mp.im(mp.log(mp.gamma(z))) - (t / 2) * mp.log(mp.pi)


def z_value(t: mp.mpf) -> mp.mpc:
    return mp.e ** (1j * theta(t)) * mp.zeta(mp.mpc(mp.mpf("0.5"), t))


def fmt(x: mp.mpf | mp.mpc) -> str:
    return mp.nstr(x, 30, min_fixed=0, max_fixed=0)


def write_theta_samples() -> None:
    samples = [
        mp.mpf("0"),
        mp.mpf("1"),
        mp.mpf("14.1347251417346937904572519836"),
        mp.mpf("21.0220396387715549926284795939"),
        mp.mpf("25.0108575801456887632137909926"),
        mp.mpf("100"),
    ]
    rows = []
    for t in samples:
        th = theta(t)
        zeta = mp.zeta(mp.mpc(mp.mpf("0.5"), t))
        z = z_value(t)
        rows.append(
            {
                "t": fmt(t),
                "theta": fmt(th),
                "zeta_real": fmt(mp.re(zeta)),
                "zeta_imag": fmt(mp.im(zeta)),
                "Z_real": fmt(mp.re(z)),
                "Z_imag": fmt(mp.im(z)),
                "abs_Z_imag": fmt(abs(mp.im(z))),
                "status": "Z_real_valued_numerically_by_functional_equation",
            }
        )
    with (BASE / "theta_function_step209.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_residual_formulation() -> None:
    rows = [
        {
            "candidate_residual": "ImZ_L2",
            "formula": "||Im Z(t)||^2_{L2_w(R)}",
            "closure_statement": "Im Z(t)=0 for real t",
            "RH_equivalent": "false",
            "classification": "degenerate_identity",
            "notes": "Z(t) real-valued follows from zeta functional equation and theta definition; it is not RH.",
        },
        {
            "candidate_residual": "zero_count_defect",
            "formula": "Delta_Z(T)=N(T)-N_0(T), where N_0(T)=# real zeros of Z(t) in [0,T]",
            "closure_statement": "Delta_Z(T)=0 for all T outside endpoint conventions",
            "RH_equivalent": "true",
            "classification": "CRE_target_equivalent_counting_residual",
            "notes": "Closure is exactly the statement that every zeta zero in the strip lies on the critical line.",
        },
        {
            "candidate_residual": "windowed_count_defect",
            "formula": "sum_r w(r/T) - sum_gamma0 w(gamma0/T), with gamma0 real Z zeros",
            "closure_statement": "all nonnegative windowed defects vanish for separating windows",
            "RH_equivalent": "true_if_windows_separate_zero_multiset",
            "classification": "Hilbertized_distributional_TE",
            "notes": "A Hilbert/distributional reformulation is possible but does not remove target equivalence.",
        },
    ]
    with (BASE / "residual_formulation_step209.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    write_theta_samples()
    write_residual_formulation()
    print("Step 209 Z residual formulation")
    print("Im Z residual: degenerate functional-equation identity, not RH")
    print("Zero-count defect Delta_Z(T)=N(T)-N_0(T): RH-equivalent")
    print("verdict=V_Z_CRCFT_TE")


if __name__ == "__main__":
    main()
