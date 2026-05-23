#!/usr/bin/env python3
"""Step 344: multiplicative H6 bridge with G_prime."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import time
from pathlib import Path

import mpmath as mp
import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step344_H6_multiplicative_G_prime_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"
STEP339 = ROOT / "anti_loc/thread/steps/step339_H6_multiplicative_bridge_artifacts"

DPS = 80
MAX_K = 20
FIT_K = list(range(1, 11))
HOLDOUT_K = [11, 12, 15, 20]
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]

G_PRIME_CENTERS = [mp.mpf("2.0"), mp.mpf("2.5"), mp.mpf("3.0")]
G_PRIME_EPS = mp.mpf("0.25")
G_PRIME_COEFFS = [mp.mpf("1"), mp.mpf("-2.5030717242"), mp.mpf("1.5030717242")]


def load_step338_module():
    spec = importlib.util.spec_from_file_location("step338_compute", STEP338_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Step 338 compute module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def beta_bump(u: mp.mpf) -> mp.mpf:
    if abs(u) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - u * u))


def M_prime_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, a in zip(G_PRIME_CENTERS, G_PRIME_COEFFS):
            lo, hi = c - G_PRIME_EPS, c + G_PRIME_EPS

            def integrand(t: mp.mpf, cc: mp.mpf = c, aa: mp.mpf = a, nn: int = n) -> mp.mpc:
                return aa * beta_bump((t - cc) / G_PRIME_EPS) * (t ** (-s)) * ((-mp.log(t)) ** nn)

            total += mp.quad(integrand, [lo, hi])
        out.append(total)
    return out


def h_derivative(fds: list[mp.mpc], mds: list[mp.mpc], k: int) -> mp.mpc:
    return mp.fsum([mp.mpf(math.comb(k, j)) * fds[j] * mds[k - j] for j in range(k + 1)])


def solve_ls(A: list[list[float]], y: list[float]) -> np.ndarray:
    arr = np.array(A, dtype=float)
    yy = np.array(y, dtype=float)
    sol, *_ = np.linalg.lstsq(arr, yy, rcond=None)
    return sol


def residual(actual_abs: mp.mpf, pred_log: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    pred_abs = mp.e ** pred_log
    log_error = pred_log - mp.log(actual_abs)
    rel = abs(pred_abs - actual_abs) / actual_abs
    return pred_abs, log_error, rel


def load_gstar_coefficients() -> tuple[mp.mpf, dict[str, mp.mpf]]:
    b0 = None
    coeffs: dict[str, mp.mpf] = {}
    for row in read_csv(STEP339 / "multiplicative_fit_step339.csv"):
        if row["model"] != "unconstrained_constant_intercept":
            continue
        if row["row_type"] == "intercept":
            b0 = mp.mpf(row["coefficient"])
        elif row["row_type"] == "exponent":
            coeffs[row["character"]] = mp.mpf(row["coefficient"])
    if b0 is None or set(coeffs) != set(CHARS):
        raise RuntimeError("could not load G_star coefficients")
    return b0, coeffs


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    mod = load_step338_module()

    roots = mod.roots()
    hecke: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    evaluator_rows = []
    for ch in CHARS:
        q, chi = mod.char_values(ch)
        rho = roots[ch]
        Lds = mod.dirichlet_L_derivatives(rho, q, chi, MAX_K)
        Mds = M_prime_derivatives(rho, MAX_K)
        for k in range(1, MAX_K + 1):
            raw = h_derivative(Lds, Mds, k)
            hecke[ch][k] = abs(raw)
            evaluator_rows.append({
                "character": ch,
                "k": k,
                "rho_chi": f"{mp.nstr(mp.re(rho), 18)}+{mp.nstr(mp.im(rho), 18)}j",
                "abs_h_derivative_G_prime": mp.nstr(abs(raw), 18),
                "real_h_derivative": mp.nstr(mp.re(raw), 24),
                "imag_h_derivative": mp.nstr(mp.im(raw), 24),
                "dps": DPS,
            })
    write_csv(ART / "hecke_evaluators_G_prime_step344.csv", evaluator_rows)

    rho1 = mp.zetazero(1)
    zds = mod.zeta_derivatives(rho1, MAX_K)
    mds = M_prime_derivatives(rho1, MAX_K)
    target = {k: abs(h_derivative(zds, mds, k)) for k in range(1, MAX_K + 1)}

    A = []
    y = []
    for k in FIT_K:
        A.append([1.0] + [float(mp.log(hecke[ch][k])) for ch in CHARS])
        y.append(float(mp.log(target[k])))
    sol = solve_ls(A, y)
    b0_prime = mp.mpf(str(sol[0]))
    coeffs_prime = {ch: mp.mpf(str(sol[i + 1])) for i, ch in enumerate(CHARS)}

    fit_rows = [{
        "row_type": "intercept",
        "k": "",
        "character": "constant",
        "G_prime_coefficient": mp.nstr(b0_prime, 18),
        "target_abs": "",
        "predicted_abs": "",
        "log_error": "",
        "relative_residual": "",
        "verdict": "fit_parameter",
    }]
    for ch in CHARS:
        fit_rows.append({
            "row_type": "exponent",
            "k": "",
            "character": ch,
            "G_prime_coefficient": mp.nstr(coeffs_prime[ch], 18),
            "target_abs": "",
            "predicted_abs": "",
            "log_error": "",
            "relative_residual": "",
            "verdict": "fit_parameter",
        })

    max_train = mp.mpf("0")
    for k in FIT_K:
        pred_log = b0_prime + mp.fsum([coeffs_prime[ch] * mp.log(hecke[ch][k]) for ch in CHARS])
        pred_abs, log_error, rel = residual(target[k], pred_log)
        max_train = max(max_train, rel)
        fit_rows.append({
            "row_type": "training_residual",
            "k": k,
            "character": "all",
            "G_prime_coefficient": "",
            "target_abs": mp.nstr(target[k], 18),
            "predicted_abs": mp.nstr(pred_abs, 18),
            "log_error": mp.nstr(log_error, 12),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
        })

    max_holdout = mp.mpf("0")
    for k in HOLDOUT_K:
        pred_log = b0_prime + mp.fsum([coeffs_prime[ch] * mp.log(hecke[ch][k]) for ch in CHARS])
        pred_abs, log_error, rel = residual(target[k], pred_log)
        max_holdout = max(max_holdout, rel)
        fit_rows.append({
            "row_type": "holdout_residual",
            "k": k,
            "character": "all",
            "G_prime_coefficient": "",
            "target_abs": mp.nstr(target[k], 18),
            "predicted_abs": mp.nstr(pred_abs, 18),
            "log_error": mp.nstr(log_error, 12),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
        })
    write_csv(ART / "multiplicative_fit_G_prime_step344.csv", fit_rows)

    b0_star, coeffs_star = load_gstar_coefficients()
    comp_rows = [{
        "parameter": "b0",
        "G_star": mp.nstr(b0_star, 18),
        "G_prime": mp.nstr(b0_prime, 18),
        "difference_G_prime_minus_G_star": mp.nstr(b0_prime - b0_star, 18),
        "ratio_G_prime_over_G_star": mp.nstr(b0_prime / b0_star, 18) if b0_star != 0 else "NA",
        "within_50pct": "NA",
    }]
    sum_star = mp.fsum([coeffs_star[ch] for ch in CHARS])
    sum_prime = mp.fsum([coeffs_prime[ch] for ch in CHARS])
    for ch in CHARS:
        diff = coeffs_prime[ch] - coeffs_star[ch]
        ratio = coeffs_prime[ch] / coeffs_star[ch] if coeffs_star[ch] != 0 else mp.nan
        within = abs(diff) <= mp.mpf("0.5") * max(abs(coeffs_star[ch]), mp.mpf("1e-40"))
        comp_rows.append({
            "parameter": f"a_{ch}",
            "G_star": mp.nstr(coeffs_star[ch], 18),
            "G_prime": mp.nstr(coeffs_prime[ch], 18),
            "difference_G_prime_minus_G_star": mp.nstr(diff, 18),
            "ratio_G_prime_over_G_star": mp.nstr(ratio, 18),
            "within_50pct": str(within),
        })
    comp_rows.append({
        "parameter": "sum_a",
        "G_star": mp.nstr(sum_star, 18),
        "G_prime": mp.nstr(sum_prime, 18),
        "difference_G_prime_minus_G_star": mp.nstr(sum_prime - sum_star, 18),
        "ratio_G_prime_over_G_star": mp.nstr(sum_prime / sum_star, 18),
        "within_50pct": str(abs(sum_prime - sum_star) <= mp.mpf("0.5") * abs(sum_star)),
    })
    write_csv(ART / "cross_G_coefficient_comparison_step344.csv", comp_rows)

    all_within = all(r["within_50pct"] == "True" for r in comp_rows if r["parameter"].startswith("a_"))
    holdout_pass = max_holdout < mp.mpf("0.01")
    if holdout_pass and all_within:
        verdict = "V_H6_multiplicative_G_prime_G_universal_candidate"
    elif holdout_pass:
        verdict = "V_H6_multiplicative_G_prime_fits_but_coefficients_G_specific"
    else:
        verdict = "V_H6_multiplicative_G_prime_holdout_fails"

    summary = [
        "# Step 344 Results Summary",
        "",
        "Repeated the Step 339 multiplicative H6 bridge with `G_prime`.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 339 G_star coefficients: `b0=-2.40963`, `sum a=1.041`, holdout k=20 residual `0.89%`.",
        "- Step 331/333 certified G_prime zeta-side values are recomputed here with the same dps=80 Leibniz evaluator.",
        "- Step 320/322/329 roots are used for the seven character carriers.",
        "",
        "Sample `|L_k^chi(rho_chi,G_prime)|` at k=10:",
    ]
    for ch in CHARS:
        summary.append(f"- {ch}: `{mp.nstr(hecke[ch][10], 18)}`")
    summary += [
        "",
        f"G_prime intercept b0': `{mp.nstr(b0_prime, 12)}`.",
        f"G_prime exponent sum: `{mp.nstr(sum_prime, 12)}`.",
        f"Training max residual k=1..10: `{mp.nstr(max_train, 12)}`.",
        f"Holdout max residual k=11/12/15/20: `{mp.nstr(max_holdout, 12)}`.",
        f"All exponents within 50% of G_star coefficients: `{all_within}`.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step344_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 344,
        "orientation": "constructive",
        "target": "multiplicative H6 bridge with G_prime",
        "dps": DPS,
        "characters": CHARS,
        "training_k": FIT_K,
        "holdout_k": HOLDOUT_K,
        "G_prime_training_max_relative_residual": mp.nstr(max_train, 18),
        "G_prime_holdout_max_relative_residual": mp.nstr(max_holdout, 18),
        "G_prime_exponent_sum": mp.nstr(sum_prime, 18),
        "all_exponents_within_50pct_of_G_star": all_within,
        "final_verdict": verdict,
    }
    (ART / "step344_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 344 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- A multiplicative fit for one test function is not a proof of an H6 bridge.",
        "- Coefficient comparison only tests G-dependence of this finite ansatz.",
    ]
    (ART / "nonclaim_boundary_step344.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_train_rel={mp.nstr(max_train, 12)}")
    print(f"max_holdout_rel={mp.nstr(max_holdout, 12)}")
    print(f"sum_prime={mp.nstr(sum_prime, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
