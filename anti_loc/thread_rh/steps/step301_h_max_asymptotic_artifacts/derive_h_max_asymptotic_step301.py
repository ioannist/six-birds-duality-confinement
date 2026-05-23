#!/usr/bin/env python3
"""Step 301: far-left arc model for max |zeta(z) M(G_star)(z)|.

The certified Branch C delta_Dk computations use the inherited Mellin
convention M(z)=int G(t) t^{-z} dt.  The circle maxima found in step 300 are on
the far-left arc, where zeta is best represented by the functional equation and
M(G_star) is dominated by the right endpoint of the last compact bump.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step301_h_max_asymptotic_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

MP_DPS = 80
R_SCAN = [mp.mpf("5.0"), mp.mpf("5.06"), mp.mpf("8.0"), mp.mpf("11.3406995042713383"), mp.mpf("14.0"), mp.mpf("20.0"), mp.mpf("30.0")]
K_TARGETS = [10, 20, 30, 50]
CERTIFIED = {
    10: mp.mpf("165.438682954225418261054825"),
    20: mp.mpf("554847.0159555452761473487386"),
    30: mp.mpf("4.0851435758143067e9"),
    50: mp.mpf("1.1691354860063852e18"),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


class MellinFast:
    def __init__(self, step292, n_nodes: int = 180):
        self.step292 = step292
        self.centers, self.epsilons, self.coeffs = step292.moment_coefficients(step292.GENERATORS["G_star"])
        x, w = np.polynomial.legendre.leggauss(n_nodes)
        self.nodes = []
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps
            mid = (lo + hi) / 2
            half = (hi - lo) / 2
            for xi, wi in zip(x, w):
                t = mid + half * mp.mpf(str(xi))
                weight = half * mp.mpf(str(wi))
                bump = step292.beta_bump((t - c) / eps)
                self.nodes.append((t, weight * coeff * bump))

    def __call__(self, z: mp.mpc) -> mp.mpc:
        total = mp.mpc(0)
        for t, wg in self.nodes:
            total += wg * (t ** (-z))
        return total

    def quad(self, z: mp.mpc) -> mp.mpc:
        total = mp.mpc(0)
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t, cc=c, ee=eps, aa=coeff):
                return aa * self.step292.beta_bump((t - cc) / ee) * (t ** (-z))

            total += mp.quad(integrand, [lo, hi])
        return total


def chi(s: mp.mpc) -> mp.mpc:
    return (2 ** s) * (mp.pi ** (s - 1)) * mp.sin(mp.pi * s / 2) * mp.gamma(1 - s)


def endpoint_mellin_abs(z: mp.mpc, centers: list[mp.mpf], epsilons: list[mp.mpf], coeffs: list[mp.mpf]) -> mp.mpf:
    """Right-endpoint Laplace model for the final G_star bump.

    Near b=c+eps, beta((t-c)/eps) ~ exp(-eps/(2(b-t))).  With the inherited
    t^{-z} convention, the endpoint integral is approximated by

      |a_3| b^{-Re z} sqrt(pi) (eps/2)^(1/4) |(-z/b)|^(-3/4)
      * exp(-Re(2 sqrt((eps/2)(-z/b)))).
    """
    c = centers[-1]
    eps = epsilons[-1]
    coeff = abs(coeffs[-1])
    b = c + eps
    lam = -z / b
    if abs(lam) == 0:
        return mp.inf
    pref = mp.sqrt(mp.pi) * (eps / 2) ** mp.mpf("0.25") * (abs(lam) ** mp.mpf("-0.75"))
    endpoint_exp = mp.e ** (-mp.re(2 * mp.sqrt((eps / 2) * lam)))
    return coeff * (b ** (-mp.re(z))) * pref * endpoint_exp


def h_endpoint_model_abs(z: mp.mpc, centers: list[mp.mpf], epsilons: list[mp.mpf], coeffs: list[mp.mpf]) -> mp.mpf:
    # Functional equation: zeta(z)=chi(z) zeta(1-z).  On the far-left arc,
    # zeta(1-z) is close to 1, but keeping it exact improves medium-R checks.
    return abs(chi(z)) * abs(mp.zeta(1 - z)) * endpoint_mellin_abs(z, centers, epsilons, coeffs)


def scan_exact_radius(rho: mp.mpc, R: mp.mpf, M: MellinFast, n_angles: int = 720) -> dict[str, object]:
    best = None
    for j in range(n_angles):
        theta = 2 * mp.pi * j / n_angles
        z = rho + R * mp.e ** (1j * theta)
        h_abs = abs(mp.zeta(z) * M(z))
        if best is None or h_abs > best["h_abs_fast"]:
            best = {"theta": theta, "z": z, "h_abs_fast": h_abs}
    assert best is not None
    h_quad = abs(mp.zeta(best["z"]) * M.quad(best["z"]))
    best["h_abs_quad"] = h_quad
    return best


def scan_model_radius(rho: mp.mpc, R: mp.mpf, centers, epsilons, coeffs, n_angles: int = 1440) -> dict[str, object]:
    best = None
    for j in range(n_angles):
        theta = 2 * mp.pi * j / n_angles
        z = rho + R * mp.e ** (1j * theta)
        h_abs = h_endpoint_model_abs(z, centers, epsilons, coeffs)
        if best is None or h_abs > best["h_abs"]:
            best = {"theta": theta, "z": z, "h_abs": h_abs}
    assert best is not None
    return best


def fit_log_h(rows: list[dict[str, object]]) -> tuple[np.ndarray, dict[str, float]]:
    # log H(R) = d + p R log R + q R + a log R.
    x = []
    y = []
    for row in rows:
        R = float(row["R"])
        H = float(row["numerical_max_h"])
        x.append([1.0, R * math.log(R), R, math.log(R)])
        y.append(math.log(H))
    beta, *_ = np.linalg.lstsq(np.array(x), np.array(y), rcond=None)
    keys = ["d", "p", "q", "a"]
    return beta, dict(zip(keys, [float(v) for v in beta]))


def log_h_fit(R: mp.mpf, beta: np.ndarray) -> mp.mpf:
    rr = float(R)
    return mp.mpf(str(beta[0] + beta[1] * rr * math.log(rr) + beta[2] * rr + beta[3] * math.log(rr)))


def derivative_log_h_fit(R: mp.mpf, beta: np.ndarray) -> mp.mpf:
    rr = float(R)
    return mp.mpf(str(beta[1] * (math.log(rr) + 1.0) + beta[2] + beta[3] / rr))


def solve_R_star(k: int, beta: np.ndarray) -> mp.mpf:
    # Minimize log F = log(k!) + logH(R) - k log R.
    def dlogF(R):
        return derivative_log_h_fit(R, beta) - mp.mpf(k) / R

    # Bracket the first sign change from negative to positive.
    prev_R = mp.mpf("1.5")
    prev = dlogF(prev_R)
    for i in range(2, 800):
        R = mp.mpf("1.5") + mp.mpf(i) * mp.mpf("0.1")
        val = dlogF(R)
        if prev <= 0 and val >= 0:
            try:
                root = mp.findroot(dlogF, (prev_R, R))
                return root
            except Exception:
                return R
        prev_R, prev = R, val
    # Fallback: scan finite interval.
    best_R = mp.mpf("1.5")
    best_val = mp.inf
    for i in range(1, 1000):
        R = mp.mpf("1.5") + mp.mpf(i) * mp.mpf("0.1")
        val = log_h_fit(R, beta) - mp.mpf(k) * mp.log(R)
        if val < best_val:
            best_R, best_val = R, val
    return best_R


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    t0 = time.time()
    step196 = load_module("step196_for_step301", STEP196_SCRIPT)
    step292 = load_module("step292_for_step301", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    rho = mp.mpc(mp.mpf("0.5"), gamma)
    M = MellinFast(step292, n_nodes=180)
    centers, epsilons, coeffs = step292.moment_coefficients(step292.GENERATORS["G_star"])

    # Calibration showing convention difference at z=2.
    z_cal = mp.mpc(2)
    inherited = M.quad(z_cal)
    standard = mp.mpc(0)
    for c, eps, coeff in zip(centers, epsilons, coeffs):
        lo, hi = c - eps, c + eps
        standard += mp.quad(lambda t, cc=c, ee=eps, aa=coeff: aa * step292.beta_bump((t - cc) / ee) * (t ** (z_cal - 1)), [lo, hi])

    scan_rows = []
    for R in R_SCAN:
        exact = scan_exact_radius(rho, R, M, n_angles=720)
        model = scan_model_radius(rho, R, centers, epsilons, coeffs, n_angles=1440)
        rel = abs(model["h_abs"] - exact["h_abs_quad"]) / exact["h_abs_quad"]
        scan_rows.append({
            "R": mp.nstr(R, 18),
            "numerical_max_h": mp.nstr(exact["h_abs_quad"], 18),
            "numerical_theta": mp.nstr(exact["theta"], 18),
            "numerical_z_real": mp.nstr(mp.re(exact["z"]), 18),
            "numerical_z_imag": mp.nstr(mp.im(exact["z"]), 18),
            "endpoint_model_max_h": mp.nstr(model["h_abs"], 18),
            "endpoint_model_theta": mp.nstr(model["theta"], 18),
            "endpoint_model_z_real": mp.nstr(mp.re(model["z"]), 18),
            "endpoint_model_z_imag": mp.nstr(mp.im(model["z"]), 18),
            "endpoint_model_rel_err": mp.nstr(rel, 18),
        })

    beta, fit_params = fit_log_h(scan_rows)

    opt_rows = []
    for k in K_TARGETS:
        R_star = solve_R_star(k, beta)
        log_bound = mp.log(mp.factorial(k)) + log_h_fit(R_star, beta) - mp.mpf(k) * mp.log(R_star)
        pred = mp.e ** log_bound
        direct_star = scan_exact_radius(rho, R_star, M, n_angles=720)
        direct_pred = mp.factorial(k) * direct_star["h_abs_quad"] / (R_star ** k)
        cert = CERTIFIED[k]
        rel = abs(pred - cert) / cert
        direct_rel = abs(direct_pred - cert) / cert
        Ck = pred / cert
        direct_Ck = direct_pred / cert
        opt_rows.append({
            "k": k,
            "R_star_fit": mp.nstr(R_star, 18),
            "max_h_at_R_star_direct": mp.nstr(direct_star["h_abs_quad"], 18),
            "theta_at_R_star_direct": mp.nstr(direct_star["theta"], 18),
            "z_real_at_R_star_direct": mp.nstr(mp.re(direct_star["z"]), 18),
            "z_imag_at_R_star_direct": mp.nstr(mp.im(direct_star["z"]), 18),
            "predicted_delta_abs_cauchy_fit": mp.nstr(pred, 18),
            "predicted_delta_abs_cauchy_direct": mp.nstr(direct_pred, 18),
            "certified_delta_abs": mp.nstr(cert, 18),
            "relative_error_fit": mp.nstr(rel, 18),
            "relative_error_direct": mp.nstr(direct_rel, 18),
            "C_k_looseness_fit": mp.nstr(Ck, 18),
            "C_k_looseness_direct": mp.nstr(direct_Ck, 18),
            "log_h_fit_at_R_star": mp.nstr(log_h_fit(R_star, beta), 18),
        })

    write_csv(ART / "h_max_at_R_scan_step301.csv", scan_rows)
    write_csv(ART / "R_optimal_per_k_step301.csv", opt_rows)

    derivation = (
        "# Step 301 Results Summary\n\n"
        "The far-left circle maxima are modeled with the zeta functional equation\n"
        "`zeta(z)=chi(z) zeta(1-z)` and the right endpoint `b=3.7` of the final\n"
        "`G_star` bump in the inherited convention `M(z)=int G(t)t^{-z}dt`.\n\n"
        "Near `t=b-y`, the bump satisfies `beta ~ exp(-epsilon/(2y))`, so\n"
        "`M(G)(z)` is approximated by\n\n"
        "`|a_3| b^{-Re z} sqrt(pi) (epsilon/2)^{1/4} |(-z/b)|^{-3/4} exp(-Re(2 sqrt((epsilon/2)(-z/b))))`.\n\n"
        "Thus `max_R |h|` is approximated by maximizing the product of this endpoint term with\n"
        "`|chi(z) zeta(1-z)|` over `z=rho+R exp(i theta)`.  For Cauchy optimization,\n"
        "the scanned maxima were summarized by the fitted closed form\n\n"
        f"`log H(R)=d+p R log R+q R+a log R`, with `d={fit_params['d']:.12g}`, "
        f"`p={fit_params['p']:.12g}`, `q={fit_params['q']:.12g}`, `a={fit_params['a']:.12g}`.\n\n"
        f"Calibration at `z=2`: inherited `t^(-z)` M(G)(2) = `{mp.nstr(inherited, 18)}`, "
        f"standard `t^(z-1)` Mellin = `{mp.nstr(standard, 18)}`.\n\n"
        "The Cauchy prediction is an upper-bound scale, not an equality: direct rescans at the fitted `R*(k)` show `C_k=predicted/certified` remains large and variable.\n"
    )
    (ART / "step301_results_summary.md").write_text(derivation, encoding="utf-8")

    schema = {
        "step": 301,
        "orientation": "h_max_asymptotic",
        "target": "max |zeta(z) M(G_star)(z)| asymptotic and Cauchy R*(k)",
        "mellin_convention": "inherited t^{-z}",
        "fit_log_H": fit_params,
        "calibration": {
            "M_inherited_t_minus_z_at_2": mp.nstr(inherited, 30),
            "M_standard_t_z_minus_1_at_2": mp.nstr(standard, 30),
        },
        "final_verdict": "V_h_max_asymptotic_partial_cauchy_looseness_not_constant",
    }
    (ART / "step301_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step301.md").write_text(
        "# Step 301 Nonclaim Boundary\n\n"
        "- Direct Branch C asymptotic attempt only; no RH claim and no Branch C closure claim.\n"
        "- The Cauchy-bound prediction is an upper-bound scale; equality is not asserted.\n"
        "- The fitted `log H(R)` summarizes scanned maxima and is not a theorem-grade proof of the exact maximum.\n",
        encoding="utf-8",
    )
    output = [
        "Step301 h_max asymptotic attempt",
        f"mpmath_dps={MP_DPS}",
        f"fit_log_H d={fit_params['d']:.12g} p={fit_params['p']:.12g} q={fit_params['q']:.12g} a={fit_params['a']:.12g}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step301_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
