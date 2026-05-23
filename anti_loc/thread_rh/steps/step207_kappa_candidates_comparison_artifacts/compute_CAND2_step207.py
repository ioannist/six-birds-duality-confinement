#!/usr/bin/env python3
"""Step 207 CAND2 samples: Burnol 2004 [19] zeta-dual candidate.

CAND2_i(tau) =
    zeta(1/2+i tau) /
    ((1/2+i tau-rho_i) zeta'(rho_i) pi^{-rho_i/2} Gamma(rho_i/2)).

For a=1/2 this is a candidate/normalization probe, not an asserted exact
formula: Burnol's a<1 dual system is described as suitable linear
combinations of zeta(s)/(s-rho)^l.
"""

from __future__ import annotations

import csv
from pathlib import Path

import mpmath as mp


mp.mp.dps = 70

ROOT = Path("/home/repos/six-birds-foundations-iii")
OUTDIR = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
CAND1 = OUTDIR / "CAND1_samples_step207.csv"
OUT = OUTDIR / "CAND2_samples_step207.csv"

RHO = {
    1: mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699")),
    2: mp.mpc(mp.mpf("0.5"), mp.mpf("21.022039638771554992628479593896902777334340524903")),
    3: mp.mpc(mp.mpf("0.5"), mp.mpf("25.010857580145688763213790992562821818659549672558")),
}


def fmt(z: mp.mpf | mp.mpc) -> str:
    return mp.nstr(z, 36, min_fixed=0, max_fixed=0)


def zeta_prime(s: mp.mpc) -> mp.mpc:
    return mp.diff(lambda z: mp.zeta(z), s)


def main() -> None:
    if not CAND1.exists():
        raise FileNotFoundError(f"run compute_CAND1_step207.py first: {CAND1}")

    tau_rows = []
    with CAND1.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["rho_index"] == "1":
                tau_rows.append((row["tau"], mp.mpf(row["tau"])))

    deriv = {}
    completion = {}
    for i, rho in RHO.items():
        deriv[i] = zeta_prime(rho)
        completion[i] = mp.power(mp.pi, -rho / 2) * mp.gamma(rho / 2)

    rows = []
    for tau_label, tau in tau_rows:
        s = mp.mpc(mp.mpf("0.5"), tau)
        zeta_s = mp.zeta(s)
        for i, rho in RHO.items():
            denom = (s - rho) * deriv[i] * completion[i]
            val = zeta_s / denom
            rows.append(
                {
                    "tau": tau_label,
                    "rho_index": i,
                    "CAND2_real": fmt(mp.re(val)),
                    "CAND2_imag": fmt(mp.im(val)),
                    "CAND2_abs": fmt(abs(val)),
                    "error_bound": "mpmath_70dps_heuristic_not_certified",
                    "status": "zeta_dual_candidate_not_exact_for_a_lt_1_without_linear_combination",
                    "formula": "zeta(s)/((s-rho_i) zeta'(rho_i) pi^{-rho_i/2} Gamma(rho_i/2))",
                }
            )

    with OUT.open("w", newline="") as f:
        fieldnames = [
            "tau",
            "rho_index",
            "CAND2_real",
            "CAND2_imag",
            "CAND2_abs",
            "error_bound",
            "status",
            "formula",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CAND2 rows written: {len(rows)}")
    for i in sorted(RHO):
        print(f"rho_{i}={fmt(RHO[i])}")
        print(f"zeta_prime_{i}={fmt(deriv[i])}")
        print(f"completion_{i}={fmt(completion[i])}")
    for r in rows[0:3]:
        print(f"sample CAND2 tau={r['tau']} rho={r['rho_index']} abs={r['CAND2_abs']}")


if __name__ == "__main__":
    main()
