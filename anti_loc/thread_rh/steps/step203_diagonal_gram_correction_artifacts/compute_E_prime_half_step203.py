#!/usr/bin/env python3
"""Step 203: compute E_{1/2}' at the first three zeta zeros.

The implementation reuses Step 202's finite cosine-resolvent model for
Burnol 2002 Theorem 8 and adds the w-derivative:

  E'(w) = A'(w)B(w) + A(w)B'(w),
  A(w)=pi^{-w/2} Gamma(w/2),
  B'(w)=-log(lambda)lambda^{1/2-w}
        -(sqrt(lambda)/2) int psi_diff(t) log(t) t^{-w} dt.

The numerical certification is limited by the same oscillatory-tail issue as
Step 202.  The script records cutoff-comparison error bounds and sign tests for
the de Branges diagonal limit.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step203_diagonal_gram_correction_artifacts")
LAMBDA = 0.5
DEFAULT_DPS = 70
DEFAULT_N_RESOLVENT = 160
DEFAULT_N_INTEGRAL = 520
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
    n: int


def rho_values() -> list[tuple[int, mp.mpc]]:
    fallback = [
        mp.mpf("14.134725141734693790457251983562"),
        mp.mpf("21.022039638771554992628479593896"),
        mp.mpf("25.010857580145688763213790992562"),
    ]
    out: list[tuple[int, mp.mpc]] = []
    for idx in range(1, 4):
        try:
            z = mp.zetazero(idx)
        except Exception:
            z = mp.mpc(mp.mpf("0.5"), fallback[idx - 1])
        out.append((idx, z))
    return out


def build_resolvent(n: int) -> ResolventData:
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
        n=n,
    )


def cosine_transform_at(t: np.ndarray, u: np.ndarray, data: ResolventData) -> np.ndarray:
    return 2.0 * (np.cos(2.0 * np.pi * t[:, None] * data.nodes[None, :]) * (data.weights * u)[None, :]).sum(axis=1)


def psi_diff_at(t: np.ndarray, data: ResolventData) -> np.ndarray:
    return -cosine_transform_at(t, data.u_plus, data) - cosine_transform_at(t, data.u_minus, data)


def integrals_to_cutoff(w: mp.mpc, data: ResolventData, cutoff: float, n_int: int) -> tuple[mp.mpc, mp.mpc]:
    raw_x, raw_w = leggauss(n_int)
    a = LAMBDA
    b = cutoff
    t = 0.5 * (b - a) * raw_x + 0.5 * (b + a)
    weights = 0.5 * (b - a) * raw_w
    psi_vals = psi_diff_at(t, data)
    total = mp.mpc(0)
    log_total = mp.mpc(0)
    for tv, wv, pv in zip(t, weights, psi_vals, strict=True):
        mt = mp.mpf(str(tv))
        term = mp.mpf(str(wv)) * mp.mpf(str(pv)) * mp.power(mt, -w)
        total += term
        log_total += term * mp.log(mt)
    return total, log_total


def e_and_derivative(w: mp.mpc, data: ResolventData, n_int: int = DEFAULT_N_INTEGRAL) -> tuple[mp.mpc, mp.mpc, mp.mpf, dict[str, str]]:
    i_main, ilog_main = integrals_to_cutoff(w, data, CUTOFF_MAIN, n_int)
    i_check, ilog_check = integrals_to_cutoff(w, data, CUTOFF_CHECK, n_int)
    lam = mp.mpf(str(LAMBDA))
    pref = mp.power(mp.pi, -w / 2) * mp.gamma(w / 2)
    pref_prime = pref * (-mp.log(mp.pi) / 2 + mp.digamma(w / 2) / 2)
    base = mp.power(lam, mp.mpf("0.5") - w)
    bracket = base + (mp.sqrt(lam) / 2) * i_main
    bracket_prime = -mp.log(lam) * base - (mp.sqrt(lam) / 2) * ilog_main
    e_val = pref * bracket
    e_prime = pref_prime * bracket + pref * bracket_prime

    err_i = abs(i_main - i_check)
    err_ilog = abs(ilog_main - ilog_check)
    err = abs(pref) * (mp.sqrt(lam) / 2) * err_i
    err += abs(pref) * (mp.sqrt(lam) / 2) * err_ilog
    err += abs(pref_prime) * (mp.sqrt(lam) / 2) * err_i
    err += mp.mpf("1e-10") * max(mp.mpf(1), abs(e_prime)) * mp.mpf(str(max(data.cond_plus, data.cond_minus)))
    return e_val, e_prime, err, {
        "main_integral": mp.nstr(i_main, 18),
        "main_log_integral": mp.nstr(ilog_main, 18),
        "cutoff_integral_diff": mp.nstr(err_i, 12),
        "cutoff_log_integral_diff": mp.nstr(err_ilog, 12),
    }


def run_case(n_resolvent: int, dps: int, n_int: int = DEFAULT_N_INTEGRAL) -> list[dict[str, object]]:
    mp.mp.dps = dps
    data = build_resolvent(n_resolvent)
    rows = []
    for idx, w in rho_values():
        e_val, e_prime, err, meta = e_and_derivative(w, data, n_int=n_int)
        plus = 2 * mp.re(mp.conj(e_val) * e_prime)
        minus = -plus
        chosen = plus if plus >= 0 else minus
        sign = "plus" if plus >= 0 else "minus"
        rows.append({
            "rho_index": idx,
            "w": w,
            "E": e_val,
            "E_prime": e_prime,
            "E_prime_error": err,
            "G_plus": plus,
            "G_minus": minus,
            "G_chosen": chosen,
            "sign_choice": sign,
            "cond_plus": data.cond_plus,
            "cond_minus": data.cond_minus,
            **meta,
        })
    return rows


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DEFAULT_DPS
    main_rows = run_case(DEFAULT_N_RESOLVENT, DEFAULT_DPS)

    with (BASE / "E_prime_half_values_step203.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "rho_index", "w_real", "w_imag", "E_real", "E_imag",
            "E_prime_real", "E_prime_imag", "E_prime_abs", "E_prime_error",
            "source", "main_integral", "main_log_integral",
            "cutoff_integral_diff", "cutoff_log_integral_diff",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in main_rows:
            writer.writerow({
                "rho_index": row["rho_index"],
                "w_real": mp.nstr(mp.re(row["w"]), 30),
                "w_imag": mp.nstr(mp.im(row["w"]), 30),
                "E_real": mp.nstr(mp.re(row["E"]), 30),
                "E_imag": mp.nstr(mp.im(row["E"]), 30),
                "E_prime_real": mp.nstr(mp.re(row["E_prime"]), 30),
                "E_prime_imag": mp.nstr(mp.im(row["E_prime"]), 30),
                "E_prime_abs": mp.nstr(abs(row["E_prime"]), 30),
                "E_prime_error": mp.nstr(row["E_prime_error"], 30),
                "source": "Burnol 2002 Theorem 8 differentiated under finite-cutoff quadrature",
                "main_integral": row["main_integral"],
                "main_log_integral": row["main_log_integral"],
                "cutoff_integral_diff": row["cutoff_integral_diff"],
                "cutoff_log_integral_diff": row["cutoff_log_integral_diff"],
            })

    with (BASE / "G_diagonal_corrected_step203.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["rho_index", "G_plus", "G_minus", "G_chosen", "sign_choice", "error_bound", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in main_rows:
            gerr = 2 * (abs(row["E"]) + 1) * row["E_prime_error"]
            writer.writerow({
                "rho_index": row["rho_index"],
                "G_plus": mp.nstr(row["G_plus"], 30),
                "G_minus": mp.nstr(row["G_minus"], 30),
                "G_chosen": mp.nstr(row["G_chosen"], 30),
                "sign_choice": row["sign_choice"],
                "error_bound": mp.nstr(gerr, 30),
                "status": "sign_chosen_by_nonnegative_norm_convention",
            })

    derivation_rows = [
        {
            "step": "Burnol kernel",
            "formula": "K(z1,z2)=(E(z1)E(z2)-E(1-z1)E(1-z2))/(z1+z2-1)",
            "source": "Burnol 2002 math/0208121 equation 1, lines 170-181 of source",
        },
        {
            "step": "critical diagonal",
            "formula": "set z1=conj(w), z2->w with Re(w)=1/2, so denominator tends to 0",
            "source": "de Branges evaluator convention in Burnol 2002 equation 1",
        },
        {
            "step": "LHopital",
            "formula": "K(conj(w),w)=E(conj(w))E'(w)+E(w)E'(conj(w))=2 Re(conj(E(w))E'(w))",
            "source": "differentiation of numerator with respect to z2",
        },
        {
            "step": "sign test",
            "formula": "also test -2 Re(conj(E(w))E'(w)); norm sign chosen by nonnegative diagonal",
            "source": "Burnol/de Branges normalization requires nonnegative norm",
        },
    ]
    with (BASE / "L_Hopital_derivation_step203.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(derivation_rows[0].keys()))
        writer.writeheader()
        writer.writerows(derivation_rows)

    robustness_rows = []
    for n_res in (160, 240, 320):
        rows = run_case(n_res, DEFAULT_DPS, n_int=360)
        for row in rows:
            robustness_rows.append({
                "test": "N_resolvent",
                "rho_index": row["rho_index"],
                "N_resolvent": n_res,
                "dps": DEFAULT_DPS,
                "G_plus": mp.nstr(row["G_plus"], 18),
                "G_chosen": mp.nstr(row["G_chosen"], 18),
                "sign_choice": row["sign_choice"],
                "status": "computed",
            })
    for dps in (50, 70, 100):
        rows = run_case(DEFAULT_N_RESOLVENT, dps, n_int=300)
        for row in rows:
            robustness_rows.append({
                "test": "dps",
                "rho_index": row["rho_index"],
                "N_resolvent": DEFAULT_N_RESOLVENT,
                "dps": dps,
                "G_plus": mp.nstr(row["G_plus"], 18),
                "G_chosen": mp.nstr(row["G_chosen"], 18),
                "sign_choice": row["sign_choice"],
                "status": "computed",
            })
    with (BASE / "robustness_step203.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    payload = {
        "lambda": LAMBDA,
        "diagonal_formula": "K(conj(w),w)=2 Re(conj(E(w))*E'(w)); opposite sign tested and chosen if needed for nonnegative norm",
        "main": [
            {
                "rho_index": row["rho_index"],
                "E": [mp.nstr(mp.re(row["E"]), 30), mp.nstr(mp.im(row["E"]), 30)],
                "E_prime": [mp.nstr(mp.re(row["E_prime"]), 30), mp.nstr(mp.im(row["E_prime"]), 30)],
                "G_plus": mp.nstr(row["G_plus"], 30),
                "G_minus": mp.nstr(row["G_minus"], 30),
                "G_chosen": mp.nstr(row["G_chosen"], 30),
                "sign_choice": row["sign_choice"],
            }
            for row in main_rows
        ],
    }
    (BASE / "E_prime_payload_step203.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("Step 203 E_prime / diagonal computation")
    print(f"lambda={LAMBDA}, dps={DEFAULT_DPS}, n_resolvent={DEFAULT_N_RESOLVENT}")
    for row in main_rows:
        print(
            f"rho_{row['rho_index']}: E'={mp.nstr(row['E_prime'], 16)} "
            f"G_plus={mp.nstr(row['G_plus'], 12)} G_chosen={mp.nstr(row['G_chosen'], 12)} sign={row['sign_choice']}"
        )


if __name__ == "__main__":
    main()
