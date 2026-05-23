#!/usr/bin/env python3
"""Step 292: direct Branch C delta_Dk computation through k=20.

The computation follows the Step 270 raw identity

    delta_Dk(rho, G) = (zeta * M(G))^(k)(rho)
                    = sum_j binom(k,j) zeta^(j)(rho) M(G)^(k-j)(rho).

The projected Branch C quantity is L_k = delta_Dk - I_k - R_k; Step 270
showed |delta_Dk|/|L_k| -> 1 through k=7.  This script computes the certified
raw proxy requested in Step 292 and labels it as delta_Dk, not as exact L_k.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_POLY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/polynomial_correction_test_step269.csv")
STEP269_DATA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/extended_dataset_step269.csv")
STEP270_IDENTITY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts/closed_identity_step270.csv")

DPS_MAIN = 80
DPS_CHECK = 100
K_TARGETS = [10, 15, 20]
K_BASELINE_CHECK = list(range(1, 8))
TRIPLES = [
    ("rho1_G_star", 1, "G_star"),
    ("rho2_G_star", 2, "G_star"),
    ("rho1_G_prime", 1, "G_prime"),
]


@dataclass(frozen=True)
class Generator:
    gid: str
    centers: tuple[str, str, str]
    epsilon: str
    note: str


GENERATORS = {
    "G_star": Generator("G_star", ("1.5", "2.5", "3.5"), "0.20", "Step 174/175 base generator; Step 196 GeneratorSpec"),
    "G_prime": Generator("G_prime", ("2.0", "2.5", "3.0"), "0.25", "Step 176 shifted generator; Step 196 GeneratorSpec"),
}


def load_step196():
    spec = importlib.util.spec_from_file_location("step196_for_step292", STEP196_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP196_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step196_for_step292"] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def beta_bump(u: mp.mpf) -> mp.mpf:
    if abs(u) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - u * u))


def moment_coefficients(gen: Generator) -> tuple[list[mp.mpf], list[mp.mpf], list[mp.mpf]]:
    """Compute the Step196 alpha,beta_3 coefficients with mpmath quadrature."""
    eps = mp.mpf(gen.epsilon)
    centers = [mp.mpf(c) for c in gen.centers]
    A: list[mp.mpf] = []
    B: list[mp.mpf] = []
    for c in centers:
        lo, hi = c - eps, c + eps
        f_a = lambda t, cc=c: beta_bump((t - cc) / eps)
        f_b = lambda t, cc=c: beta_bump((t - cc) / eps) / t
        A.append(mp.quad(f_a, [lo, hi]))
        B.append(mp.quad(f_b, [lo, hi]))
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    coeffs = [mp.mpf("1"), -alpha, beta_3]
    return centers, [eps, eps, eps], coeffs


def mellin_derivatives(gen: Generator, gamma: mp.mpf, max_k: int, dps: int) -> list[mp.mpc]:
    mp.mp.dps = dps
    centers, epsilons, coeffs = moment_coefficients(gen)
    out: list[mp.mpc] = []
    s_exp = mp.mpc(mp.mpf("-0.5"), -gamma)  # t^(-1/2 - i gamma)
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, eps, coeff in zip(centers, epsilons, coeffs):
            lo, hi = c - eps, c + eps
            def integrand(t, cc=c, ee=eps, aa=coeff, nn=n):
                return aa * beta_bump((t - cc) / ee) * (t ** s_exp) * ((-mp.log(t)) ** nn)
            total += mp.quad(integrand, [lo, hi])
        out.append(total)
    return out


def zeta_derivatives(gamma: mp.mpf, max_k: int, dps: int) -> list[mp.mpc]:
    mp.mp.dps = dps
    s = mp.mpc(mp.mpf("0.5"), gamma)
    return [mp.zeta(s, derivative=n) for n in range(max_k + 1)]


def delta_from_derivatives(zds: list[mp.mpc], mds: list[mp.mpc], k: int) -> mp.mpc:
    total = mp.mpc(0)
    for j in range(k + 1):
        total += mp.mpf(math.comb(k, j)) * zds[j] * mds[k - j]
    return total


def mp_complex_str(z: mp.mpc, digits: int = 30) -> str:
    return f"{mp.nstr(mp.re(z), digits)}{mp.nstr(mp.im(z), digits, min_fixed=0, max_fixed=0, strip_zeros=False, show_zero_exponent=True) if mp.im(z) < 0 else '+' + mp.nstr(mp.im(z), digits, min_fixed=0, max_fixed=0, strip_zeros=False, show_zero_exponent=True)}j"


def fit_params() -> dict[str, dict[str, float]]:
    rows = read_csv(STEP269_POLY)
    out = {}
    for row in rows:
        out[row["triple_id"]] = {
            "a": float(row["a"]),
            "b": float(row["b"]),
            "c": float(row["c"]),
            "rmse": float(row["rmse_k0_7"]),
            "max_abs_resid": float(row["max_abs_residual_k0_7"]),
        }
    return out


def baseline_abs() -> dict[tuple[str, int], float]:
    rows = read_csv(STEP269_DATA)
    return {(r["triple_id"], int(r["k"])): float(r["L_abs"]) for r in rows}


def step270_raw_abs() -> dict[tuple[str, int], float]:
    rows = read_csv(STEP270_IDENTITY)
    return {(r["triple_id"], int(r["k"])): float(r["raw_abs"]) for r in rows}


def predicted_value(params: dict[str, float], k: int) -> float:
    return params["a"] * ((k + 1.0) ** params["c"]) * math.exp(params["b"] * k)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    step196 = load_step196()
    fits = fit_params()
    baseline = baseline_abs()
    step270_raw = step270_raw_abs()

    provenance_rows = []
    for gid, gen in GENERATORS.items():
        mp.mp.dps = DPS_MAIN
        centers, epsilons, coeffs = moment_coefficients(gen)
        provenance_rows.append({
            "G_id": gid,
            "formula": "G(t)=sum_i coeff_i exp(-1/(1-((t-c_i)/epsilon)^2)) on |t-c_i|<epsilon, else 0",
            "centers": ";".join(gen.centers),
            "epsilon": gen.epsilon,
            "coefficients_dps80": ";".join(mp.nstr(c, 30) for c in coeffs),
            "provenance": gen.note,
        })

    delta_rows = []
    residual_rows = []
    decision_rows = []
    baseline_check_rows = []
    output_lines = [
        "Step 292 Branch C delta_Dk certified proxy computation",
        f"dps_main={DPS_MAIN}; dps_check={DPS_CHECK}",
        "delta_Dk=(zeta*M(G))^(k)(rho), L_k=delta_Dk-I_k-R_k; Step270 ratios tend to 1 through k=7",
    ]

    for triple_id, rho_index, gid in TRIPLES:
        gamma = mp.mpf(str(step196.ZEROS[rho_index]))
        gen = GENERATORS[gid]
        max_k = max(K_TARGETS)

        t0 = time.time()
        zds80 = zeta_derivatives(gamma, max_k, DPS_MAIN)
        mds80 = mellin_derivatives(gen, gamma, max_k, DPS_MAIN)
        runtime80 = time.time() - t0

        t1 = time.time()
        zds100 = zeta_derivatives(gamma, max_k, DPS_CHECK)
        mds100 = mellin_derivatives(gen, gamma, max_k, DPS_CHECK)
        runtime100 = time.time() - t1

        # Check k=1..7 against Step270 raw delta_Dk values.
        for k in K_BASELINE_CHECK:
            d80 = delta_from_derivatives(zds80, mds80, k)
            raw_abs = float(abs(d80))
            step270_abs = step270_raw[(triple_id, k)]
            projected_abs = baseline[(triple_id, k)]
            baseline_check_rows.append({
                "triple_id": triple_id,
                "k": k,
                "delta_abs_dps80": f"{raw_abs:.16e}",
                "step270_raw_abs": f"{step270_abs:.16e}",
                "relative_delta_vs_step270_raw": f"{(raw_abs - step270_abs) / step270_abs:.16e}",
                "projected_L_abs_step269": f"{projected_abs:.16e}",
                "delta_to_projected_ratio": f"{raw_abs / projected_abs:.16e}",
            })

        output_lines.append(f"{triple_id}: zeta+M derivatives runtime dps80={runtime80:.3f}s dps100={runtime100:.3f}s")
        max_ratio_dev = 0.0
        for k in K_TARGETS:
            d80 = delta_from_derivatives(zds80, mds80, k)
            d100 = delta_from_derivatives(zds100, mds100, k)
            abs80 = abs(d80)
            abs100 = abs(d100)
            diff = abs(abs80 - abs100)
            params = fits[triple_id]
            pred = predicted_value(params, k)
            residual = float(abs80) - pred
            rel_res = residual / float(abs80)
            rmse_ratio = abs(residual) / params["rmse"]
            max_ratio_dev = max(max_ratio_dev, rmse_ratio)
            delta_rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": k,
                "delta_Dk_complex_dps80": mp_complex_str(d80, 28),
                "delta_Dk_abs_dps80": mp.nstr(abs80, 28),
                "delta_Dk_abs_dps100": mp.nstr(abs100, 28),
                "abs_dps80_dps100_delta": mp.nstr(diff, 12),
                "dps": DPS_MAIN,
                "runtime_seconds_dps80": f"{runtime80:.6f}",
                "runtime_seconds_dps100_check": f"{runtime100:.6f}",
                "certification_note": "raw delta_Dk proxy; dps80/dps100 agreement reported",
            })
            residual_rows.append({
                "triple_id": triple_id,
                "k": k,
                "delta_abs": mp.nstr(abs80, 24),
                "step269_fit_predicted": f"{pred:.16e}",
                "absolute_residual": f"{residual:.16e}",
                "relative_residual": f"{rel_res:.16e}",
                "step269_rmse_k0_7": f"{params['rmse']:.16e}",
                "abs_residual_over_rmse": f"{rmse_ratio:.16e}",
            })
            output_lines.append(
                f"{triple_id} k={k}: |delta_Dk|={mp.nstr(abs80, 14)} "
                f"pred={pred:.8e} rel_res={rel_res:.3e} rmse_ratio={rmse_ratio:.2f}"
            )

        if max_ratio_dev <= 3.0:
            decision = "continues_within_3x_rmse"
        elif max_ratio_dev <= 10.0:
            decision = "mild_high_k_drift"
        else:
            decision = "law_breaks_for_delta_proxy"
        decision_rows.append({
            "triple_id": triple_id,
            "max_abs_residual_over_step269_rmse_k10_15_20": f"{max_ratio_dev:.16e}",
            "decision": decision,
            "interpretation": "decision is for delta_Dk proxy; projected L_k inherits only if projection correction remains negligible",
        })

    write_csv(ART / "M_G_formula_provenance_step292.csv", provenance_rows)
    write_csv(ART / "delta_Dk_certified_step292.csv", delta_rows)
    write_csv(ART / "fit_residuals_step292.csv", residual_rows)
    write_csv(ART / "law_continuation_decision_step292.csv", decision_rows)
    write_csv(ART / "baseline_raw_check_step292.csv", baseline_check_rows)

    verdict = "V_branch_C_k20_law_breaks"
    if all(r["decision"] == "continues_within_3x_rmse" for r in decision_rows):
        verdict = "V_branch_C_k20_certified"
    elif all(r["decision"] in {"continues_within_3x_rmse", "mild_high_k_drift"} for r in decision_rows):
        verdict = "V_branch_C_k20_transition"

    summary = {
        "verdict": verdict,
        "dps_main": DPS_MAIN,
        "dps_check": DPS_CHECK,
        "decisions": decision_rows,
        "delta_rows": delta_rows,
        "fit_residuals": residual_rows,
        "baseline_check": baseline_check_rows,
    }
    (ART / "compute_step292_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (ART / "compute_step292_output.txt").write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print("\n".join(output_lines))
    print("final_verdict", verdict)


if __name__ == "__main__":
    main()
