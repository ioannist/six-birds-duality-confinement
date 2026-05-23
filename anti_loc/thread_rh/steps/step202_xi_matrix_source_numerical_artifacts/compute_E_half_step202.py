#!/usr/bin/env python3
"""Step 202 numerical evaluation of Burnol E_{1/2}.

This script implements a finite-dimensional cosine-transform discretization of
Burnol 2002 Definition 2 / Theorem 8 for lambda=1/2.  It is an honest
numerical attempt, not a certification theorem: the oscillatory tail of the
Theorem 8 integral is estimated by cutoff comparison and is the dominant
uncertainty recorded in the output.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts")
LAMBDA = 0.5
MP_DPS = 70
N_RESOLVENT = 160
N_INTEGRAL = 520
CUTOFF_MAIN = 80.0
CUTOFF_CHECK = 55.0


@dataclass(frozen=True)
class ResolventData:
    nodes: np.ndarray
    weights: np.ndarray
    u_plus: np.ndarray
    u_minus: np.ndarray
    cond_plus: float
    cond_minus: float


def rho_values() -> list[tuple[str, mp.mpc]]:
    mp.mp.dps = MP_DPS
    fallback = [
        mp.mpf("14.134725141734693790457251983562"),
        mp.mpf("21.022039638771554992628479593896"),
        mp.mpf("25.010857580145688763213790992562"),
    ]
    out: list[tuple[str, mp.mpc]] = []
    for idx in range(1, 4):
        try:
            z = mp.zetazero(idx)
        except Exception:
            z = mp.mpc(mp.mpf("0.5"), fallback[idx - 1])
        out.append((f"rho_{idx}", z))
        out.append((f"one_minus_rho_{idx}", 1 - z))
    return out


def build_resolvent(n: int = N_RESOLVENT) -> ResolventData:
    # Half-line even convention: L^2(0,lambda) with Fourier cosine kernel.
    raw_x, raw_w = leggauss(n)
    nodes = 0.5 * LAMBDA * (raw_x + 1.0)
    weights = 0.5 * LAMBDA * raw_w
    x = nodes[:, None]
    y = nodes[None, :]
    fmat = 2.0 * np.cos(2.0 * np.pi * x * y) * weights[None, :]
    rhs = 2.0 * np.cos(2.0 * np.pi * LAMBDA * nodes)
    ident = np.eye(n)
    u_plus = np.linalg.solve(ident + fmat, rhs)
    u_minus = np.linalg.solve(ident - fmat, rhs)
    return ResolventData(
        nodes=nodes,
        weights=weights,
        u_plus=u_plus,
        u_minus=u_minus,
        cond_plus=float(np.linalg.cond(ident + fmat)),
        cond_minus=float(np.linalg.cond(ident - fmat)),
    )


def cosine_transform_at(t: np.ndarray, u: np.ndarray, data: ResolventData) -> np.ndarray:
    return 2.0 * (np.cos(2.0 * np.pi * t[:, None] * data.nodes[None, :]) * (data.weights * u)[None, :]).sum(axis=1)


def psi_diff_at(t: np.ndarray, data: ResolventData) -> np.ndarray:
    # Burnol manager-provided sign convention:
    # psi_+ = 2cos(pi t) - F_+ u_plus, psi_- = 2cos(pi t) + F_+ u_minus.
    return -cosine_transform_at(t, data.u_plus, data) - cosine_transform_at(t, data.u_minus, data)


def integral_to_cutoff(w: mp.mpc, data: ResolventData, cutoff: float, n_int: int = N_INTEGRAL) -> mp.mpc:
    raw_x, raw_w = leggauss(n_int)
    a = LAMBDA
    b = cutoff
    t = 0.5 * (b - a) * raw_x + 0.5 * (b + a)
    weights = 0.5 * (b - a) * raw_w
    psi_vals = psi_diff_at(t, data)
    total = mp.mpc(0)
    for tv, wv, pv in zip(t, weights, psi_vals, strict=True):
        total += mp.mpf(str(wv)) * mp.mpf(str(pv)) * mp.power(mp.mpf(str(tv)), -w)
    return total


def e_lambda(w: mp.mpc, data: ResolventData) -> tuple[mp.mpc, mp.mpf, dict[str, str]]:
    main_int = integral_to_cutoff(w, data, CUTOFF_MAIN)
    check_int = integral_to_cutoff(w, data, CUTOFF_CHECK)
    integral_err = abs(main_int - check_int)
    prefactor = mp.power(mp.pi, -w / 2) * mp.gamma(w / 2)
    bracket = mp.power(mp.mpf(str(LAMBDA)), mp.mpf("0.5") - w) + (mp.sqrt(mp.mpf(str(LAMBDA))) / 2) * main_int
    value = prefactor * bracket
    # Conservative error: cutoff comparison pushed through the same prefactor,
    # plus a small resolvent discretization floor from the condition numbers.
    propagated = abs(prefactor) * (mp.sqrt(mp.mpf(str(LAMBDA))) / 2) * integral_err
    floor = mp.mpf("1e-10") * max(mp.mpf(1), abs(value)) * mp.mpf(str(max(data.cond_plus, data.cond_minus)))
    return value, propagated + floor, {
        "main_integral": mp.nstr(main_int, 25),
        "check_integral": mp.nstr(check_int, 25),
        "cutoff_difference": mp.nstr(integral_err, 12),
        "prefactor_abs": mp.nstr(abs(prefactor), 12),
    }


def cstr(z: mp.mpc, digits: int = 24) -> str:
    return f"{mp.nstr(mp.re(z), digits)}{mp.nstr(mp.im(z), digits, min_fixed=0, max_fixed=0)}j"


def main() -> None:
    mp.mp.dps = MP_DPS
    BASE.mkdir(parents=True, exist_ok=True)
    data = build_resolvent()
    rows = []
    json_rows = []
    print("Step 202 E_{1/2} numerical evaluation")
    print(f"lambda={LAMBDA}, mp_dps={MP_DPS}, n_resolvent={N_RESOLVENT}, n_integral={N_INTEGRAL}")
    print(f"cond(I+F_lambda)={data.cond_plus:.6e}, cond(I-F_lambda)={data.cond_minus:.6e}")
    for label, w in rho_values():
        value, err, meta = e_lambda(w, data)
        row = {
            "label": label,
            "w_real": mp.nstr(mp.re(w), 30),
            "w_imag": mp.nstr(mp.im(w), 30),
            "E_real": mp.nstr(mp.re(value), 30),
            "E_imag": mp.nstr(mp.im(value), 30),
            "E_abs": mp.nstr(abs(value), 30),
            "E_arg": mp.nstr(mp.arg(value), 30),
            "error_bound": mp.nstr(err, 30),
            "source": "Burnol 2002 math/0208121 Theorem 8; finite cosine-resolvent discretization",
            **meta,
        }
        rows.append(row)
        json_rows.append({**row, "E_complex": [row["E_real"], row["E_imag"]]})
        print(f"{label}: w={mp.nstr(w, 18)} E={cstr(value, 16)} |E|={mp.nstr(abs(value), 12)} err<={mp.nstr(err, 8)}")

    with (BASE / "E_half_values_step202.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "E_half_values_step202.json").write_text(json.dumps({
        "lambda": LAMBDA,
        "mp_dps": MP_DPS,
        "n_resolvent": N_RESOLVENT,
        "n_integral": N_INTEGRAL,
        "cutoff_main": CUTOFF_MAIN,
        "cutoff_check": CUTOFF_CHECK,
        "cond_plus": data.cond_plus,
        "cond_minus": data.cond_minus,
        "values": json_rows,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
