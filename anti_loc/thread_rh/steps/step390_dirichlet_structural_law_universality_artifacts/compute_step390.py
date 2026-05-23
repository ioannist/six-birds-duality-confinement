#!/usr/bin/env python3
"""Step 390: Branch C structural law test for L(s, chi_3)."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step390_dirichlet_structural_law_universality_artifacts")
STEP389 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step389_dirichlet_close_pair_universality_artifacts")
STEP322_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts/compute_L_k_more_instances_step322.py")
DPS = 60
Q = 3
K_VALUES = [5, 10, 15, 20, 30]
N_ZEROS = 10


def load_step322():
    spec = importlib.util.spec_from_file_location("step322_for_step390", STEP322_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP322_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_rho(s: str) -> mp.mpc:
    # Stored form is Re+Imj with positive imaginary part.
    clean = s.rstrip("j")
    # Split on the final plus sign between real and imaginary fields.
    idx = clean.rfind("+")
    return mp.mpc(mp.mpf(clean[:idx]), mp.mpf(clean[idx + 1:]))


def product_derivative(Lds: list[mp.mpc], Mds: list[mp.mpc], k: int) -> mp.mpc:
    return mp.fsum([mp.binomial(k, j) * Lds[j] * Mds[k - j] for j in range(k + 1)])


def fit_linear_gamma(vals: dict[int, mp.mpf]) -> tuple[float, float, float, float]:
    # log|delta_Dk| = a + alpha log(k) - gamma k.
    y = np.array([float(mp.log(vals[k])) for k in K_VALUES], dtype=float)
    X = np.column_stack([
        np.ones(len(K_VALUES)),
        np.log(np.array(K_VALUES, dtype=float)),
        -np.array(K_VALUES, dtype=float),
    ])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    return float(beta[0]), float(beta[1]), float(beta[2]), rmse


def main() -> None:
    mp.mp.dps = DPS
    ART.mkdir(parents=True, exist_ok=True)
    step322 = load_step322()
    zero_rows = read_csv(STEP389 / "dirichlet_L_zeros_and_derivatives_step389.csv")[:N_ZEROS]

    gamma_rows: list[dict[str, object]] = []
    comp_rows: list[dict[str, object]] = []
    for row in zero_rows:
        j = int(row["j"])
        rho = parse_rho(row["rho"])
        T = mp.im(rho)
        Lds = step322.L_derivatives(rho, Q, [0, 1, -1], max(K_VALUES))
        Mds = step322.M_derivatives(rho, "G_star", max(K_VALUES))
        vals = {k: abs(product_derivative(Lds, Mds, k)) for k in K_VALUES}
        a, alpha, gamma, rmse = fit_linear_gamma(vals)
        pred_q3 = mp.pi / (T * mp.log(Q * T / (2 * mp.pi)))
        pred_q1 = mp.pi / (T * mp.log(T / (2 * mp.pi)))
        rel_q3 = abs(mp.mpf(gamma) - pred_q3) / abs(pred_q3)
        rel_q1 = abs(mp.mpf(gamma) - pred_q1) / abs(pred_q1)
        gamma_rows.append({
            "j": j,
            "character": "chi_3",
            "q": Q,
            "rho": row["rho"],
            "T": mp.nstr(T, 30),
            "gamma_L_linear_in_k": f"{gamma:.17e}",
            "fit_intercept_a": f"{a:.17e}",
            "fit_alpha_logk": f"{alpha:.17e}",
            "fit_log_RMSE": f"{rmse:.17e}",
            "k5_abs_delta": mp.nstr(vals[5], 30),
            "k10_abs_delta": mp.nstr(vals[10], 30),
            "k15_abs_delta": mp.nstr(vals[15], 30),
            "k20_abs_delta": mp.nstr(vals[20], 30),
            "k30_abs_delta": mp.nstr(vals[30], 30),
            "evaluator": "delta_Dk^L=(L(s,chi_3)*M(G_star)(s))^(k)(rho), Leibniz with Hurwitz-zeta L-derivatives",
        })
        comp_rows.append({
            "j": j,
            "T": mp.nstr(T, 30),
            "gamma_L_linear_in_k": f"{gamma:.17e}",
            "pred_q3_pi_over_T_log_qT": mp.nstr(pred_q3, 30),
            "rel_err_q3": mp.nstr(rel_q3, 30),
            "pred_q1_pi_over_T_log_T": mp.nstr(pred_q1, 30),
            "rel_err_q1": mp.nstr(rel_q1, 30),
            "better_predictor": "q3" if rel_q3 < rel_q1 else "q1",
        })

    q3_errs = [mp.mpf(r["rel_err_q3"]) for r in comp_rows]
    q1_errs = [mp.mpf(r["rel_err_q1"]) for r in comp_rows]
    mean_q3 = mp.fsum(q3_errs) / len(q3_errs)
    mean_q1 = mp.fsum(q1_errs) / len(q1_errs)
    median_q3 = sorted(q3_errs)[len(q3_errs) // 2]
    median_q1 = sorted(q1_errs)[len(q1_errs) // 2]
    verdict = "universal_with_q_adjustment" if mean_q3 < mp.mpf("0.20") else (
        "q1_better_conductor_adjustment_wrong_direction" if mean_q3 > mp.mpf("0.50") and mean_q1 < mean_q3 else
        "both_versions_fail_structural_law_not_supported_for_raw_linear_fit"
    )

    write_csv(ART / "L_chi3_gamma_extraction_step390.csv", gamma_rows)
    write_csv(ART / "comparison_to_predicted_structural_step390.csv", comp_rows)

    summary = [
        "# Step 390 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 324: global Branch C gamma fitting dataset.",
        "- Step 366: `A_predicted(T) = pi/log(T/(2pi))` structural coefficient hypothesis.",
        "- Step 378/381: close-pair local-geometry mechanism.",
        "- Step 389: `zeta-like universality supported` for Re L'' sign flips.",
        "",
        "Evaluator: `delta_Dk^L=(L(s,chi_3) M(G_star)(s))^(k)(rho)` using Hurwitz-zeta derivatives and Leibniz.",
        f"Zeros used: `{N_ZEROS}`.",
        f"Mean relative error q=3 prediction: `{mp.nstr(mean_q3, 18)}`.",
        f"Median relative error q=3 prediction: `{mp.nstr(median_q3, 18)}`.",
        f"Mean relative error q=1 prediction: `{mp.nstr(mean_q1, 18)}`.",
        f"Median relative error q=1 prediction: `{mp.nstr(median_q1, 18)}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step390_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 390,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "character": "chi_3",
        "q": Q,
        "zeros_used": N_ZEROS,
        "k_values": K_VALUES,
        "mpmath_dps": DPS,
        "mean_rel_err_q3": float(mean_q3),
        "median_rel_err_q3": float(median_q3),
        "mean_rel_err_q1": float(mean_q1),
        "median_rel_err_q1": float(median_q1),
        "verdict": verdict,
    }
    (ART / "step390_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step390.md").write_text(
        "# Nonclaim Boundary - Step 390\n\n"
        "No RH claim is made. This is a numerical raw-proxy test for `L(s,chi_3)`, "
        "not a theorem for Dirichlet L-functions or the Selberg class. The fitted "
        "linear-in-k coefficient is sensitive to normalization and should not be "
        "identified with a projected Burnol/Sonine gamma without the missing projector.\n"
    )

    print(f"mean_rel_err_q3={mp.nstr(mean_q3, 12)}")
    print(f"mean_rel_err_q1={mp.nstr(mean_q1, 12)}")
    print(verdict)


if __name__ == "__main__":
    main()
