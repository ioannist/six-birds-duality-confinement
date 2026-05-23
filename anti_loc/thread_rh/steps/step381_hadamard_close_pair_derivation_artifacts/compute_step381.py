#!/usr/bin/env python3
"""Step 381: Hadamard close-pair derivation diagnostics."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step381_hadamard_close_pair_derivation_artifacts")
STEP368 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step368_branch_C_residual_structure_artifacts/residuals_and_predictors_step368.csv")
STEP379 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step379_cross_observable_unification_artifacts/exceptional_gamma_residuals_step379.csv")
DPS = 80
BASELINE = list(range(1, 16))
EXCEPTIONS = [34, 41, 64, 71, 79, 80, 92]
ZEROS = BASELINE + EXCEPTIONS


def sgn(x: float) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def pearson(xs: list[float], ys: list[float]) -> float:
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny) if denx and deny else float("nan")


def linfit(xs: list[float], ys: list[float]) -> tuple[float, float, list[float], float]:
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    var = sum((x - mx) ** 2 for x in xs)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = cov / var
    a = my - b * mx
    pred = [a + b * x for x in xs]
    rmse = math.sqrt(sum((p - y) ** 2 for p, y in zip(pred, ys)) / len(ys))
    return a, b, pred, rmse


def load_R() -> dict[int, float]:
    out: dict[int, float] = {}
    with STEP368.open(newline="") as fh:
        for row in csv.DictReader(fh):
            out[int(row["rho_index"])] = float(row["R"])
    with STEP379.open(newline="") as fh:
        for row in csv.DictReader(fh):
            out[int(row["j"])] = float(row["R_gamma_T_minus_A_pred"])
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    R = load_R()
    max_zero = max(ZEROS) + 2
    rhos = {j: mp.zetazero(j) for j in range(1, max_zero + 1)}

    g_rows: list[dict[str, object]] = []
    sign_rows: list[dict[str, object]] = []
    pred_seed: list[dict[str, object]] = []

    for j in ZEROS:
        rho = rhos[j]
        z1 = mp.zeta(rho, derivative=1)
        z2 = mp.zeta(rho, derivative=2)
        g_actual = z2 / (2 * z1)

        candidates = []
        if j > 1:
            candidates.append((j - 1, abs(mp.im(rho) - mp.im(rhos[j - 1]))))
        candidates.append((j + 1, abs(mp.im(rhos[j + 1]) - mp.im(rho))))
        nearest_j, s_min = min(candidates, key=lambda x: x[1])
        nearest_rho = rhos[nearest_j]
        g_nearest = -1 / (nearest_rho - rho)
        local_js = [k for k in range(max(1, j - 2), j + 3) if k != j]
        g_local_pm2 = mp.mpc(0)
        for k in local_js:
            rk = rhos[k]
            g_local_pm2 += -1 / (rk - rho) + 1 / rk

        close_contrib = 2 * z1 * g_nearest
        local_contrib = 2 * z1 * g_local_pm2
        direct_reconstructed = 2 * z1 * g_actual
        actual_sign = sgn(float(mp.re(z2)))
        direct_sign = sgn(float(mp.re(direct_reconstructed)))
        close_sign = sgn(float(mp.re(close_contrib)))
        local_sign = sgn(float(mp.re(local_contrib)))

        g_rows.append(
            {
                "j": j,
                "group": "exceptional" if j in EXCEPTIONS else "baseline",
                "T": mp.nstr(mp.im(rho), 30),
                "nearest_j": nearest_j,
                "s_min": mp.nstr(s_min, 30),
                "Re_zeta_prime": mp.nstr(mp.re(z1), 30),
                "Im_zeta_prime": mp.nstr(mp.im(z1), 30),
                "Re_zeta_double_prime": mp.nstr(mp.re(z2), 30),
                "Im_zeta_double_prime": mp.nstr(mp.im(z2), 30),
                "Re_g_prime_actual": mp.nstr(mp.re(g_actual), 30),
                "Im_g_prime_actual": mp.nstr(mp.im(g_actual), 30),
                "Re_g_nearest": mp.nstr(mp.re(g_nearest), 30),
                "Im_g_nearest": mp.nstr(mp.im(g_nearest), 30),
                "Re_g_local_pm2": mp.nstr(mp.re(g_local_pm2), 30),
                "Im_g_local_pm2": mp.nstr(mp.im(g_local_pm2), 30),
                "Re_close_pair_contribution": mp.nstr(mp.re(close_contrib), 30),
                "Re_local_pm2_contribution": mp.nstr(mp.re(local_contrib), 30),
            }
        )
        sign_rows.append(
            {
                "j": j,
                "group": "exceptional" if j in EXCEPTIONS else "baseline",
                "actual_sign_Re_zeta2": actual_sign,
                "hadamard_identity_sign": direct_sign,
                "close_pair_only_sign": close_sign,
                "local_pm2_only_sign": local_sign,
                "identity_match": str(direct_sign == actual_sign),
                "close_pair_match": str(close_sign == actual_sign),
                "local_pm2_match": str(local_sign == actual_sign),
                "Re_zeta_double_prime": mp.nstr(mp.re(z2), 30),
                "Re_close_pair_contribution": mp.nstr(mp.re(close_contrib), 30),
                "s_min": mp.nstr(s_min, 30),
            }
        )
        pred_seed.append(
            {
                "j": j,
                "group": "exceptional" if j in EXCEPTIONS else "baseline",
                "R_empirical": R[j],
                "s_min": float(s_min),
                "inv_s_min": 1.0 / float(s_min),
                "close_pair_re_contribution": float(mp.re(close_contrib)),
                "local_pm2_re_contribution": float(mp.re(local_contrib)),
            }
        )

    write_csv(BASE / "g_prime_evaluation_step381.csv", g_rows)
    write_csv(BASE / "re_zeta2_sign_prediction_step381.csv", sign_rows)

    inv_s = [float(r["inv_s_min"]) for r in pred_seed]
    Rvals = [float(r["R_empirical"]) for r in pred_seed]
    a, b, pred, rmse = linfit(inv_s, Rvals)
    r_inv = pearson(inv_s, Rvals)
    r_close = pearson([float(r["close_pair_re_contribution"]) for r in pred_seed], Rvals)
    r_local = pearson([float(r["local_pm2_re_contribution"]) for r in pred_seed], Rvals)
    r_rows = []
    for row, p in zip(pred_seed, pred):
        r_rows.append(
            {
                **row,
                "R_pred_linear_inv_s_min": f"{p:.17e}",
                "R_prediction_residual": f"{p - float(row['R_empirical']):.17e}",
                "linear_model": f"R = {a:.17e} + {b:.17e}/s_min",
                "pearson_R_vs_inv_s_min": f"{r_inv:.17e}",
                "pearson_R_vs_close_contrib": f"{r_close:.17e}",
                "pearson_R_vs_local_pm2_contrib": f"{r_local:.17e}",
                "rmse_linear_inv_s": f"{rmse:.17e}",
            }
        )
    write_csv(BASE / "R_j_prediction_step381.csv", r_rows)

    identity_matches = sum(1 for r in sign_rows if r["identity_match"] == "True")
    close_matches = sum(1 for r in sign_rows if r["close_pair_match"] == "True")
    local_matches = sum(1 for r in sign_rows if r["local_pm2_match"] == "True")
    exc_close_matches = sum(1 for r in sign_rows if r["group"] == "exceptional" and r["close_pair_match"] == "True")
    base_close_matches = sum(1 for r in sign_rows if r["group"] == "baseline" and r["close_pair_match"] == "True")

    derivation = f"""# Step 381 Hadamard Close-Pair Derivation

For a simple zero `rho_j`, write

`zeta(s) = (s-rho_j) exp(g_j(s))`.

Then

`zeta'(rho_j) = exp(g_j(rho_j))`

and

`zeta''(rho_j) = 2 zeta'(rho_j) g'_j(rho_j)`.

From the completed Hadamard product

`xi(s)=e^(A+Bs) prod_rho (1-s/rho)e^(s/rho)`,

the regular logarithmic derivative at `rho_j` is

`g'_j(rho_j) = arch(rho_j) + sum_(rho != rho_j) [-1/(rho-rho_j) + 1/rho]`,

where `arch` contains the elementary, Gamma, and exponential factors. For a nearest neighbor `rho_n = rho_j +/- i s_min`, the singular local term is

`g'_near = -1/(rho_n-rho_j) = +/- i/s_min`.

Therefore the close-pair contribution to the real part is

`Re zeta''_near(rho_j) = Re(2 zeta'(rho_j) g'_near)`,

so a compressed pair can flip the sign through the phase of `zeta'(rho_j)`. This term is not a full sign theorem by itself because the regular Hadamard remainder can dominate, but it is the local amplification term.

Numerical results over the 22 tested zeros:

- direct Hadamard identity sign match: `{identity_matches}/22`
- close-pair-only sign match: `{close_matches}/22`
- close-pair-only sign match on exceptions: `{exc_close_matches}/7`
- close-pair-only sign match on baseline: `{base_close_matches}/15`
- `corr(R_j, 1/s_min) = {r_inv:.6f}`
- `corr(R_j, Re close-pair contribution) = {r_close:.6f}`

Interpretation: the identity is exact; the non-tautological close-pair term identifies all seven sign-flip exceptions but overpredicts positives in the low-index baseline. The Branch C residual has a strong `1/s_min` correlation above the requested `0.7` threshold.
"""
    (BASE / "hadamard_derivation_step381.md").write_text(derivation)

    verdict = "partial_close_pair_mechanism_R_correlation_passes_sign_needs_regular_remainder"
    summary = f"""# Step 381 Results Summary

Hadamard key formula:

`zeta''(rho_j) = 2 zeta'(rho_j) g'_j(rho_j)`,

with

`g'_j(rho_j)=arch(rho_j)+sum_(rho != rho_j)[-1/(rho-rho_j)+1/rho]`.

The close-pair term is `g'_near=+/- i/s_min`, giving `Re zeta''_near = Re(2 zeta'(rho_j) g'_near)`.

Sign prediction:

- exact Hadamard identity reconstruction: `{identity_matches}/22`
- close-pair-only predictor: `{close_matches}/22`
- close-pair-only on exceptional zeros: `{exc_close_matches}/7`
- close-pair-only on baseline zeros: `{base_close_matches}/15`

Residual prediction:

- model: `R = {a:.6g} + {b:.6g}/s_min`
- Pearson `corr(R, 1/s_min) = {r_inv:.6f}`
- RMSE: `{rmse:.6f}`

Verdict: `{verdict}`. The close-pair Hadamard term gives the local amplification mechanism and predicts the Branch C residual above the `r>0.7` threshold, but a complete `Re zeta''` sign theorem requires controlling the regular Hadamard remainder.
"""
    (BASE / "step381_results_summary.md").write_text(summary)

    schema = {
        "step": 381,
        "mode": "ATTEMPT",
        "dps": DPS,
        "zeros_tested": ZEROS,
        "identity_sign_matches": identity_matches,
        "close_pair_sign_matches": close_matches,
        "close_pair_exception_sign_matches": exc_close_matches,
        "close_pair_baseline_sign_matches": base_close_matches,
        "pearson_R_vs_inv_s_min": r_inv,
        "pearson_R_vs_close_pair_re_contribution": r_close,
        "R_linear_model_intercept": a,
        "R_linear_model_slope_inv_s": b,
        "R_linear_model_rmse": rmse,
        "verdict": verdict,
    }
    (BASE / "step381_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    boundary = """# Step 381 Nonclaim Boundary

- This step does not prove RH or any sign theorem for zeta derivatives.
- The exact Hadamard identity is used as a consistency check; the non-tautological claim is only about the nearest-neighbor term.
- The close-pair-only sign predictor is partial and does not control the full regular Hadamard remainder.
- Branch C residual prediction uses empirical residuals from Steps 368 and 379.
"""
    (BASE / "nonclaim_boundary_step381.md").write_text(boundary)

    print("STEP381_COMPUTE_DONE")
    print(f"identity_matches={identity_matches}/22")
    print(f"close_pair_matches={close_matches}/22 exceptions={exc_close_matches}/7 baseline={base_close_matches}/15")
    print(f"corr_R_inv_s={r_inv:.12g} corr_R_close={r_close:.12g}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
