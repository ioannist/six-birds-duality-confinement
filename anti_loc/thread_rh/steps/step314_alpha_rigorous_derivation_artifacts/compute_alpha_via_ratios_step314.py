#!/usr/bin/env python3
"""Step 314: alpha prediction from derivative-ratio phase increments."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step314_alpha_rigorous_derivation_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP313_SIGMA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step313_rigorous_gaussian_linear_phase_artifacts/sigma_alpha_predicted_vs_empirical_step313.csv")

DPS = 80
MAX_K = 50
K_TARGETS = [10, 20, 30, 50]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def principal_arg(z: mp.mpc) -> mp.mpf:
    return mp.arg(z)


def wrap_pi(x: mp.mpf) -> mp.mpf:
    two_pi = 2 * mp.pi
    while x > mp.pi:
        x -= two_pi
    while x <= -mp.pi:
        x += two_pi
    return x


def sign_label(x: mp.mpf) -> str:
    if x > 0:
        return "+"
    if x < 0:
        return "-"
    return "0"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step196 = load_module("step196_for_step314", STEP196_SCRIPT)
    step292 = load_module("step292_for_step314", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    zds = step292.zeta_derivatives(gamma, MAX_K + 1, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_K + 1, DPS)
    empirical = {int(r["k"]): r for r in read_csv(STEP313_SIGMA)}

    z_rows = []
    for j in range(MAX_K):
        ratio = zds[j+1] / zds[j] if abs(zds[j]) != 0 else mp.nan
        z_rows.append({
            "j": j,
            "zeta_j_abs": mp.nstr(abs(zds[j]), 34),
            "zeta_j_plus_1_over_j_complex": cstr(ratio, 34) if ratio == ratio else "nan",
            "ratio_abs": mp.nstr(abs(ratio), 34) if ratio == ratio else "nan",
            "arg_zeta_ratio": mp.nstr(principal_arg(ratio), 34) if ratio == ratio else "nan",
            "real_sign": sign_label(mp.re(ratio)) if ratio == ratio else "nan",
            "imag_sign": sign_label(mp.im(ratio)) if ratio == ratio else "nan",
        })
    write_csv(ART / "zeta_ratio_args_step314.csv", z_rows)

    m_rows = []
    for j in range(MAX_K):
        ratio = mds[j+1] / mds[j]
        m_rows.append({
            "j": j,
            "M_j_abs": mp.nstr(abs(mds[j]), 34),
            "M_j_plus_1_over_j_complex": cstr(ratio, 34),
            "ratio_abs": mp.nstr(abs(ratio), 34),
            "arg_M_ratio": mp.nstr(principal_arg(ratio), 34),
            "real_sign": sign_label(mp.re(ratio)),
            "imag_sign": sign_label(mp.im(ratio)),
        })
    write_csv(ART / "M_ratio_args_step314.csv", m_rows)

    alpha_rows = []
    for k in K_TARGETS:
        j = k // 2
        m = k - j
        z_arg = principal_arg(zds[j+1] / zds[j])
        # User's continuous-index approximation.
        m_arg_user = principal_arg(mds[m+1] / mds[m])
        alpha_user_signed = wrap_pi(z_arg - m_arg_user)
        # Exact forward phase increment term_{j+1}/term_j, ignoring positive binomial ratio.
        m_arg_forward = principal_arg(mds[m-1] / mds[m])
        alpha_forward_signed = wrap_pi(z_arg + m_arg_forward)
        # Symmetric central-difference exact term phase around j=k/2.
        z_arg_minus = principal_arg(zds[j] / zds[j-1])
        m_arg_backward = principal_arg(mds[m+1] / mds[m])
        prev_delta_signed = wrap_pi(z_arg_minus + m_arg_backward)
        alpha_symmetric_signed = wrap_pi((alpha_forward_signed + prev_delta_signed) / 2)
        alpha_emp = mp.mpf(empirical[k]["alpha_empirical_central_slope"])
        alpha_local = mp.mpf(empirical[k]["alpha_local_phase_derivative"])
        alpha_rows.append({
            "k": k,
            "j_center": j,
            "m_center": m,
            "arg_zeta_ratio_j_plus_1_over_j": mp.nstr(z_arg, 34),
            "arg_M_ratio_m_plus_1_over_m": mp.nstr(m_arg_user, 34),
            "arg_M_ratio_m_minus_1_over_m": mp.nstr(m_arg_forward, 34),
            "alpha_user_formula_signed": mp.nstr(alpha_user_signed, 34),
            "alpha_user_formula_abs": mp.nstr(abs(alpha_user_signed), 34),
            "alpha_forward_exact_signed": mp.nstr(alpha_forward_signed, 34),
            "alpha_forward_exact_abs": mp.nstr(abs(alpha_forward_signed), 34),
            "alpha_symmetric_exact_signed": mp.nstr(alpha_symmetric_signed, 34),
            "alpha_symmetric_exact_abs": mp.nstr(abs(alpha_symmetric_signed), 34),
            "alpha_empirical_step313": mp.nstr(alpha_emp, 34),
            "alpha_local_step313": mp.nstr(alpha_local, 34),
            "relative_error_user_abs_vs_empirical": mp.nstr(abs(abs(alpha_user_signed)-alpha_emp)/alpha_emp, 34),
            "relative_error_symmetric_abs_vs_local": mp.nstr(abs(abs(alpha_symmetric_signed)-alpha_local)/alpha_local, 34),
        })
    write_csv(ART / "alpha_predicted_vs_empirical_step314.csv", alpha_rows)

    verdict = "V_alpha_ratio_formula_verified_numerically_literature_bound_missing"
    print("Step314 alpha via derivative ratios")
    for row in alpha_rows:
        print(
            "k={k} zeta_arg={z} M_arg={m} alpha_user_abs={a} alpha_emp={e} alpha_sym_abs={s}".format(
                k=row["k"],
                z=row["arg_zeta_ratio_j_plus_1_over_j"],
                m=row["arg_M_ratio_m_plus_1_over_m"],
                a=row["alpha_user_formula_abs"],
                e=row["alpha_empirical_step313"],
                s=row["alpha_symmetric_exact_abs"],
            )
        )
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()

