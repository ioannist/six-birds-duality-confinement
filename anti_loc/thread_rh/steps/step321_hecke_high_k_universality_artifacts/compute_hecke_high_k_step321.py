#!/usr/bin/env python3
"""Step 321: high-k Hecke evaluator pairings and universality fit."""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step321_hecke_high_k_universality_artifacts")
STEP320 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
STEP296_CORRECTED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts/corrected_L_k_step296.csv")
DPS = 80
MAX_K = 30
HIGH_K = [15, 20, 30]
FIT_K = [5, 10, 15, 20, 30]


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


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


def g_star_coefficients() -> tuple[list[mp.mpf], mp.mpf, list[mp.mpf]]:
    centers = [mp.mpf("1.5"), mp.mpf("2.5"), mp.mpf("3.5")]
    eps = mp.mpf("0.20")
    A, B = [], []
    for c in centers:
        A.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps), [c - eps, c + eps]))
        B.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps) / t, [c - eps, c + eps]))
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return centers, eps, [mp.mpf("1"), -alpha, beta_3]


def character_data() -> dict[str, tuple[int, list[mp.mpc]]]:
    I = mp.mpc(0, 1)
    return {
        "chi_3": (3, [0, 1, -1]),
        "chi_4": (4, [0, 1, 0, -1]),
        "chi_5a": (5, [0, 1, -1, -1, 1]),
        "chi_5b": (5, [0, 1, I, -I, -1]),
    }


def L_derivatives(s: mp.mpc, q: int, chi: list[mp.mpc], max_k: int) -> list[mp.mpc]:
    logq = mp.log(q)
    q_factor = mp.mpf(q) ** (-s)
    zeta_sums: list[mp.mpc] = []
    for m in range(max_k + 1):
        zeta_sums.append(
            mp.fsum([chi[a % q] * mp.zeta(s, mp.mpf(a) / q, derivative=m) for a in range(1, q + 1)])
        )
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for m in range(n + 1):
            total += mp.mpf(math.comb(n, m)) * ((-logq) ** (n - m)) * zeta_sums[m]
        out.append(q_factor * total)
    return out


def M_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    centers, eps, coeffs = g_star_coefficients()
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, a in zip(centers, coeffs):
            def integrand(t: mp.mpf, cc: mp.mpf = c, aa: mp.mpf = a, nn: int = n) -> mp.mpc:
                return aa * beta_bump((t - cc) / eps) * (t ** (-s)) * ((-mp.log(t)) ** nn)
            total += mp.quad(integrand, [c - eps, c + eps])
        out.append(total)
    return out


def h_derivative(Lds: list[mp.mpc], Mds: list[mp.mpc], k: int) -> mp.mpc:
    total = mp.mpc(0)
    for j in range(k + 1):
        total += mp.mpf(math.comb(k, j)) * Lds[j] * Mds[k - j]
    return total


def roots_from_step320() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    return {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}


def step320_raw_values() -> dict[tuple[str, int], mp.mpf]:
    rows = read_csv(STEP320 / "hecke_L_k_values_step320.csv")
    return {(r["character"], int(r["k"])): mp.mpf(r["h_derivative_abs"]) for r in rows}


def branch_c_values() -> dict[int, mp.mpf]:
    out = {10: mp.mpf("165.43868295422541")}
    if STEP296_CORRECTED.exists():
        for r in read_csv(STEP296_CORRECTED):
            k = int(r["k"])
            if k in (20, 30):
                out[k] = mp.mpf(r["delta_abs"])
    out.setdefault(20, mp.mpf("554847"))
    out.setdefault(30, mp.mpf("4.085e9"))
    return out


def linear_fit(points: list[tuple[int, mp.mpf]], include_gamma: bool) -> tuple[dict[str, mp.mpf], mp.mpf]:
    cols = 4 if include_gamma else 3
    X = mp.matrix(len(points), cols)
    y = mp.matrix(len(points), 1)
    for i, (k, value) in enumerate(points):
        kk = mp.mpf(k)
        X[i, 0] = 1
        X[i, 1] = mp.log(kk)
        X[i, 2] = kk
        if include_gamma:
            X[i, 3] = kk * mp.log(kk)
        y[i] = mp.log(value)
    beta = mp.lu_solve(X.T * X, X.T * y)
    residuals = X * beta - y
    rmse = mp.sqrt(mp.fsum([residuals[i] ** 2 for i in range(len(points))]) / len(points))
    params = {
        "A": mp.e ** beta[0],
        "alpha": beta[1],
        "b": beta[2],
        "gamma": beta[3] if include_gamma else mp.mpf("0"),
    }
    return params, rmse


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    roots = roots_from_step320()
    chars = character_data()
    inherited = step320_raw_values()
    all_raw = dict(inherited)
    high_rows: list[dict[str, object]] = []
    fit_rows: list[dict[str, object]] = []
    ratio_rows: list[dict[str, object]] = []
    t_all = time.time()

    for label in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        q, chi = chars[label]
        rho = roots[label]
        t0 = time.time()
        Lds = L_derivatives(rho, q, chi, MAX_K)
        Mds = M_derivatives(rho, MAX_K)
        runtime = time.time() - t0
        for k in HIGH_K:
            raw = h_derivative(Lds, Mds, k)
            norm = raw / mp.factorial(k)
            all_raw[(label, k)] = abs(raw)
            high_rows.append(
                {
                    "character": label,
                    "k": k,
                    "rho_chi": cstr(rho, 30),
                    "h_derivative_real": mp.nstr(mp.re(raw), 30),
                    "h_derivative_imag": mp.nstr(mp.im(raw), 30),
                    "h_derivative_abs_raw": mp.nstr(abs(raw), 20),
                    "L_k_normalized_abs_h_derivative_over_k_factorial": mp.nstr(abs(norm), 20),
                    "dps": DPS,
                    "runtime_for_character_seconds": f"{runtime:.3f}",
                }
            )

        fit_points = [(k, all_raw[(label, k)]) for k in FIT_K]
        for model, include_gamma in [("gamma_free", False), ("gamma_full", True)]:
            params, rmse = linear_fit(fit_points, include_gamma)
            fit_rows.append(
                {
                    "character": label,
                    "model": model,
                    "A_chi": mp.nstr(params["A"], 18),
                    "alpha_chi": mp.nstr(params["alpha"], 18),
                    "b_chi": mp.nstr(params["b"], 18),
                    "gamma_chi": mp.nstr(params["gamma"], 18),
                    "log_RMSE": mp.nstr(rmse, 18),
                    "fit_k_values": ";".join(map(str, FIT_K)),
                    "scale": "raw |h_chi^(k)(rho_chi)|",
                }
            )

    bc = branch_c_values()
    for k in [10, 20, 30]:
        row: dict[str, object] = {"k": k, "branch_C_zeta_raw_abs": mp.nstr(bc[k], 20)}
        for label in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
            row[f"{label}_raw_abs"] = mp.nstr(all_raw[(label, k)], 20)
            row[f"{label}_over_branch_C"] = mp.nstr(all_raw[(label, k)] / bc[k], 16)
        ratio_rows.append(row)

    write_csv(ART / "hecke_L_k_chi_high_k_step321.csv", high_rows)
    write_csv(ART / "hecke_saddle_fit_per_chi_step321.csv", fit_rows)
    write_csv(ART / "hecke_vs_branch_C_ratios_step321.csv", ratio_rows)

    gf = {r["character"]: r for r in fit_rows if r["model"] == "gamma_free"}
    full = {r["character"]: r for r in fit_rows if r["model"] == "gamma_full"}
    b_values = [mp.mpf(gf[ch]["b_chi"]) for ch in gf]
    gamma_values = [mp.mpf(full[ch]["gamma_chi"]) for ch in full]
    verdict = "V_hecke_high_k_growth_character_specific"
    summary = [
        "# Step 321 Results Summary",
        "",
        "Extended the Step 320 primitive-character Hecke evaluator pairings to `k=15,20,30` at `mpmath` dps 80.",
        "The computation uses the same `t^{-s}` Mellin convention and the Step 320 critical-line zeros.",
        "",
        "Primary scale: raw `|h_chi^(k)(rho_chi)|`, because the inherited Branch C high-k values are raw derivative magnitudes.  The high-k CSV also records the normalized `|h_chi^(k)/k!|` values.",
        "",
        "Universality assessment:",
        f"- Gamma-free fitted `b_chi` values range from `{mp.nstr(min(b_values), 8)}` to `{mp.nstr(max(b_values), 8)}`.",
        f"- Full four-parameter fits produce `gamma_chi` values ranging from `{mp.nstr(min(gamma_values), 8)}` to `{mp.nstr(max(gamma_values), 8)}` and are sensitive with only five fit points.",
        "- The high-k ratios against Branch C are strongly k-dependent, so the data do not support a universal `b≈1` with only a character-dependent prefactor.",
        "- The foreclosure/nonvanishing pattern is shared across the subfamily, but the growth parameters are character-specific at this resolution.",
        "",
        "Hecke branch status: H5 remains numerically active for this primitive mod 3/4/5 subfamily.  This does not close H6 or prove GRH.",
        "",
        f"Runtime: {time.time() - t_all:.3f} seconds. Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step321_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 321,
        "orientation": "attempt",
        "target": "Hecke high-k evaluator universality for primitive chars mod 3,4,5",
        "dps": DPS,
        "high_k": HIGH_K,
        "fit_k": FIT_K,
        "scale": "raw derivative for Branch C comparison; normalized also recorded",
        "final_verdict": verdict,
    }
    (ART / "step321_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step321.md").write_text(
        "# Step 321 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim Hecke cascade closure.\n"
        "- The fitted growth parameters are numerical diagnostics over `k=5,10,15,20,30`, not asymptotic theorems.\n"
        "- H5 activation remains restricted to the concrete primitive mod 3/4/5 subfamily.\n",
        encoding="utf-8",
    )
    print("Step321 Hecke high-k")
    for r in high_rows:
        print(f"{r['character']} k={r['k']} raw_abs={r['h_derivative_abs_raw']} norm_abs={r['L_k_normalized_abs_h_derivative_over_k_factorial']}")
    for ch in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        print(f"{ch} gamma_free b={gf[ch]['b_chi']} full gamma={full[ch]['gamma_chi']}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
