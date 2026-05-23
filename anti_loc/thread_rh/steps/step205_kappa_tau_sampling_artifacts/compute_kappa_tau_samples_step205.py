#!/usr/bin/env python3
"""Compute candidate boundary-kernel samples for Step 205.

The values written here are samples of K_{1/2}^Gamma(1/2+i tau,rho_i).  The
Step 205 derivation audit shows that these samples are not certified as
kappa_i(tau)=T_{1/2}^*K(.,rho_i)(1/2+i tau) without an extra transport theorem.
They are included as an attempted numerical shadow, not as the final kappa
input for c_ij.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step205_kappa_tau_sampling_artifacts")
STEP202_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py")
MP_DPS = 70
N_GRID = 200
T_MAX = 40.0


def load_step202_module():
    spec = importlib.util.spec_from_file_location("step202_E", STEP202_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step202 E module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step202_E"] = mod
    spec.loader.exec_module(mod)
    return mod


def zeros() -> dict[int, mp.mpc]:
    return {
        1: mp.mpc(mp.mpf("0.5"), mp.mpf("14.1347251417346937904572519836")),
        2: mp.mpc(mp.mpf("0.5"), mp.mpf("21.0220396387715549926284795939")),
        3: mp.mpc(mp.mpf("0.5"), mp.mpf("25.0108575801456887632137909926")),
    }


def read_E_rho_values() -> dict[str, mp.mpc]:
    vals = {}
    with Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/E_half_values_step202.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vals[row["label"]] = mp.mpc(mp.mpf(row["E_real"]), mp.mpf(row["E_imag"]))
    return vals


def kernel_candidate(s: mp.mpc, rho: mp.mpc, E_s: mp.mpc, E_1_minus_s: mp.mpc, E_rho: mp.mpc, E_1_minus_rho: mp.mpc) -> mp.mpc:
    return (E_s * E_rho - E_1_minus_s * E_1_minus_rho) / (s + rho - 1)


def main() -> None:
    mp.mp.dps = MP_DPS
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_step202_module()
    data = mod.build_resolvent(120)
    vals = read_E_rho_values()
    raw_x, raw_w = leggauss(N_GRID)
    tau = T_MAX * raw_x
    rows = []
    # Cache E(s) and E(1-s) for grid points.
    e_cache: dict[float, tuple[mp.mpc, mp.mpc, mp.mpf]] = {}
    for t in tau:
        tv = float(t)
        s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(tv)))
        e_s, err_s, _ = mod.e_lambda(s, data)
        e_1s, err_1s, _ = mod.e_lambda(1 - s, data)
        e_cache[tv] = (e_s, e_1s, max(err_s, err_1s))

    for tv in tau:
        s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(float(tv))))
        e_s, e_1s, e_err = e_cache[float(tv)]
        for idx, rho in zeros().items():
            k = kernel_candidate(
                s,
                rho,
                e_s,
                e_1s,
                vals[f"rho_{idx}"],
                vals[f"one_minus_rho_{idx}"],
            )
            rows.append({
                "tau": f"{float(tv):.18e}",
                "rho_index": idx,
                "kappa_candidate_real": mp.nstr(mp.re(k), 30),
                "kappa_candidate_imag": mp.nstr(mp.im(k), 30),
                "kappa_candidate_abs": mp.nstr(abs(k), 30),
                "error_bound": mp.nstr(e_err, 20),
                "status": "candidate_boundary_kernel_not_certified_as_kappa",
                "formula": "K_{1/2}^Gamma(1/2+i tau,rho_i)",
            })

    with (BASE / "kappa_tau_samples_step205.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("Step 205 candidate kappa_tau samples")
    print(f"grid_nodes={N_GRID}, tau_range=[{-T_MAX},{T_MAX}], values={len(rows)}")
    for target in [-25.0, -14.0, 0.0, 14.0, 25.0]:
        nearest = min(tau, key=lambda x: abs(float(x) - target))
        subset = [r for r in rows if r["tau"] == f"{float(nearest):.18e}" and r["rho_index"] == 1]
        if subset:
            r = subset[0]
            print(f"tau~{target}: rho_1 candidate={r['kappa_candidate_real']}+{r['kappa_candidate_imag']}i")


if __name__ == "__main__":
    main()
