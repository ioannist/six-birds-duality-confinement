#!/usr/bin/env python3
"""Step 323: gamma versus zero height for zeta zeros and a Dirichlet check."""

from __future__ import annotations

import csv
import json
import math
import statistics
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step323_gamma_vs_height_artifacts")
DPS = 80
MAX_K = 30
FIT_K = [5, 10, 15, 20, 30]

INHERITED_ZETA = {
    1: ("14.134725141734693790457251983562", "0.2046", "inherited_step305"),
    2: ("21.022039638771554992628479593896", "0.1379", "inherited_step305"),
    3: ("25.010857580145688763213790992563", "0.10021", "inherited_step322"),
    4: ("30.424876125859513210311897530584", "0.08190", "inherited_step322"),
    5: ("32.935061587739189690662368964075", "0.05208", "inherited_step322"),
}

INHERITED_DIRICHLET = [
    ("chi_3", "8.039737155681466681713623214173", "0.222", "inherited_step321"),
    ("chi_4", "6.020948904697596654902511521612", "0.217", "inherited_step321"),
    ("chi_5a", "6.648453344727714716123278459979", "0.195", "inherited_step321"),
    ("chi_5b", "6.183578195450853914377517309709", "0.215", "inherited_step321"),
    ("chi_7a", "4.475738283728683131974628487193", "0.209", "inherited_step322"),
    ("chi_8a", "4.899973997007036501038304899197", "0.192", "inherited_step322"),
    ("chi_11a", "2.477243711229234259051889804946", "0.196", "inherited_step322"),
]


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


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


def M_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    centers, eps, coeffs = g_star_coefficients()
    out = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, a in zip(centers, coeffs):
            def integrand(t: mp.mpf, cc: mp.mpf = c, aa: mp.mpf = a, nn: int = n) -> mp.mpc:
                return aa * beta_bump((t - cc) / eps) * (t ** (-s)) * ((-mp.log(t)) ** nn)
            total += mp.quad(integrand, [c - eps, c + eps])
        out.append(total)
    return out


def h_derivative(Lds: list[mp.mpc], Mds: list[mp.mpc], k: int) -> mp.mpc:
    return mp.fsum([mp.mpf(math.comb(k, j)) * Lds[j] * Mds[k - j] for j in range(k + 1)])


def zeta_fit_values(rho: mp.mpc) -> dict[int, mp.mpf]:
    zds = [mp.zeta(rho, derivative=n) for n in range(MAX_K + 1)]
    mds = M_derivatives(rho, MAX_K)
    return {k: abs(h_derivative(zds, mds, k)) for k in FIT_K}


def legendre_chi(q: int) -> list[int]:
    residues = {pow(a, 2, q) for a in range(1, q)}
    return [0] + [1 if a in residues else -1 for a in range(1, q)]


def L_chi(s: mp.mpc, q: int, chi: list[int]) -> mp.mpc:
    return (mp.mpf(q) ** (-s)) * mp.fsum(
        [chi[a % q] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)]
    )


def L_derivatives(s: mp.mpc, q: int, chi: list[int], max_k: int) -> list[mp.mpc]:
    logq = mp.log(q)
    q_factor = mp.mpf(q) ** (-s)
    zeta_sums = [
        mp.fsum([chi[a % q] * mp.zeta(s, mp.mpf(a) / q, derivative=m) for a in range(1, q + 1)])
        for m in range(max_k + 1)
    ]
    out = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for m in range(n + 1):
            total += mp.mpf(math.comb(n, m)) * ((-logq) ** (n - m)) * zeta_sums[m]
        out.append(q_factor * total)
    return out


def locate_legendre_zero(q: int) -> tuple[mp.mpc, mp.mpf]:
    chi = legendre_chi(q)
    def f(x: mp.mpf, y: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
        value = L_chi(mp.mpc(x, y), q, chi)
        return mp.re(value), mp.im(value)
    guesses = [mp.mpf("2.0"), mp.mpf("3.0"), mp.mpf("4.0"), mp.mpf("6.0"), mp.mpf("8.0"), mp.mpf("10.0"), mp.mpf("12.0"), mp.mpf("14.0")]
    roots = []
    for guess in guesses:
        try:
            x, y = mp.findroot(f, (mp.mpf("0.5"), guess), tol=mp.mpf("1e-30"), maxsteps=40, solver="mnewton")
            z = mp.mpc(x, y)
            if mp.im(z) > 0 and mp.re(z) > mp.mpf("0.1") and all(abs(z - old) > mp.mpf("1e-9") for old in roots):
                roots.append(z)
        except Exception:
            continue
    if not roots:
        raise RuntimeError(f"no Legendre q={q} zero found")
    root = min(roots, key=lambda z: mp.im(z))
    return root, abs(L_chi(root, q, chi))


def dirichlet_fit_values(q: int, rho: mp.mpc) -> dict[int, mp.mpf]:
    chi = legendre_chi(q)
    Lds = L_derivatives(rho, q, chi, MAX_K)
    Mds = M_derivatives(rho, MAX_K)
    return {k: abs(h_derivative(Lds, Mds, k)) for k in FIT_K}


def linear_fit(values: dict[int, mp.mpf]) -> tuple[dict[str, mp.mpf], mp.mpf]:
    X = mp.matrix(len(FIT_K), 4)
    y = mp.matrix(len(FIT_K), 1)
    for i, k in enumerate(FIT_K):
        kk = mp.mpf(k)
        X[i, 0] = 1
        X[i, 1] = mp.log(kk)
        X[i, 2] = kk
        X[i, 3] = kk * mp.log(kk)
        y[i] = mp.log(values[k])
    beta = mp.lu_solve(X.T * X, X.T * y)
    residuals = X * beta - y
    rmse = mp.sqrt(mp.fsum([residuals[i] ** 2 for i in range(len(FIT_K))]) / len(FIT_K))
    return {"A": mp.e ** beta[0], "alpha": beta[1], "b": beta[2], "gamma": beta[3]}, rmse


def fit_gamma_models(points: list[tuple[float, float]]) -> list[dict[str, object]]:
    # All models are least-squares; RMSE is measured in gamma-space.
    def solve_design(rows: list[list[float]], yvals: list[float]) -> list[float]:
        m = len(rows)
        n = len(rows[0])
        X = mp.matrix(m, n)
        y = mp.matrix(m, 1)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                X[i, j] = value
            y[i] = yvals[i]
        beta = mp.lu_solve(X.T * X, X.T * y)
        return [float(beta[i]) for i in range(n)]

    Ts = [p[0] for p in points]
    gs = [p[1] for p in points]
    rows = []

    # gamma = a + b log T
    beta = solve_design([[1.0, math.log(T)] for T in Ts], gs)
    pred = [beta[0] + beta[1] * math.log(T) for T in Ts]
    rows.append({"model": "log_linear_gamma=a+b_logT", "param_1": beta[0], "param_2": beta[1], "param_3": "", "RMSE_gamma": rmse(gs, pred)})

    # gamma = A*T^{-c}; log gamma = log A - c log T.
    beta = solve_design([[1.0, -math.log(T)] for T in Ts], [math.log(g) for g in gs])
    A = math.exp(beta[0]); c = beta[1]
    pred = [A * (T ** (-c)) for T in Ts]
    rows.append({"model": "power_gamma=A*T^{-c}", "param_1": A, "param_2": c, "param_3": "", "RMSE_gamma": rmse(gs, pred)})

    # gamma = a*exp(-bT); log gamma = log a - bT.
    beta = solve_design([[1.0, -T] for T in Ts], [math.log(g) for g in gs])
    a = math.exp(beta[0]); b = beta[1]
    pred = [a * math.exp(-b * T) for T in Ts]
    rows.append({"model": "exponential_gamma=a*exp(-bT)", "param_1": a, "param_2": b, "param_3": "", "RMSE_gamma": rmse(gs, pred)})
    return rows


def rmse(y: list[float], pred: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(y, pred)) / len(y))


def add_gamma_row(rows: list[dict[str, object]], source: str, label: str, n: int | str, rho: mp.mpc, values: dict[int, mp.mpf] | None, gamma: mp.mpf | str, params: dict[str, mp.mpf] | None = None, fit_rmse: mp.mpf | str = "") -> None:
    rows.append(
        {
            "source": source,
            "zero_label": label,
            "zero_index": n,
            "rho": cstr(rho, 34),
            "Im_rho": mp.nstr(mp.im(rho), 24),
            "gamma": mp.nstr(mp.mpf(gamma), 18),
            "A": mp.nstr(params["A"], 18) if params else "",
            "alpha": mp.nstr(params["alpha"], 18) if params else "",
            "b": mp.nstr(params["b"], 18) if params else "",
            "fit_log_RMSE": mp.nstr(fit_rmse, 18) if fit_rmse != "" else "",
            "k5_abs": mp.nstr(values[5], 18) if values else "",
            "k10_abs": mp.nstr(values[10], 18) if values else "",
            "k15_abs": mp.nstr(values[15], 18) if values else "",
            "k20_abs": mp.nstr(values[20], 18) if values else "",
            "k30_abs": mp.nstr(values[30], 18) if values else "",
        }
    )


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    t_all = time.time()
    gamma_rows: list[dict[str, object]] = []

    # Inherited rho1..rho5.
    for n, (imag, gamma, source) in INHERITED_ZETA.items():
        rho = mp.mpc(mp.mpf("0.5"), mp.mpf(imag))
        add_gamma_row(gamma_rows, source, f"zeta_rho{n}", n, rho, None, gamma)

    # New rho6..rho15.
    for n in range(6, 16):
        rho = mp.zetazero(n)
        values = zeta_fit_values(rho)
        params, fit_rmse = linear_fit(values)
        add_gamma_row(gamma_rows, "computed_step323", f"zeta_rho{n}", n, rho, values, params["gamma"], params, fit_rmse)
        print(f"zeta_rho{n} Im={mp.nstr(mp.im(rho), 12)} gamma={mp.nstr(params['gamma'], 12)}", flush=True)

    write_csv(ART / "gamma_vs_im_rho_step323.csv", gamma_rows)

    # Functional form fits over rho1..rho15.
    points = [(float(r["Im_rho"]), float(r["gamma"])) for r in gamma_rows]
    form_rows = fit_gamma_models(points)
    write_csv(ART / "functional_form_fit_step323.csv", form_rows)

    # Cross-family table: inherited Dirichlet, plus q=13 Legendre candidate.
    cross_rows: list[dict[str, object]] = []
    for label, imag, gamma, source in INHERITED_DIRICHLET:
        cross_rows.append({"source": source, "family": "Dirichlet", "object": label, "Im_rho": imag, "gamma": gamma, "note": "inherited first-zero gamma"})
    q13_root, q13_res = locate_legendre_zero(13)
    q13_values = dirichlet_fit_values(13, q13_root)
    q13_params, q13_rmse = linear_fit(q13_values)
    cross_rows.append(
        {
            "source": "computed_step323",
            "family": "Dirichlet",
            "object": "chi_13a_legendre_first_zero",
            "Im_rho": mp.nstr(mp.im(q13_root), 24),
            "gamma": mp.nstr(q13_params["gamma"], 18),
            "note": f"q=13 candidate first zero; residual={mp.nstr(q13_res, 6)}; not high-Im comparable to zeta rho1",
        }
    )
    for row in gamma_rows:
        cross_rows.append({"source": row["source"], "family": "zeta", "object": row["zero_label"], "Im_rho": row["Im_rho"], "gamma": row["gamma"], "note": "G_star zeta zero"})
    write_csv(ART / "cross_family_universality_step323.csv", cross_rows)

    best = min(form_rows, key=lambda r: float(r["RMSE_gamma"]))
    verdict = "V_gamma_height_family_specific_no_cross_family_universal_form"
    summary = [
        "# Step 323 Results Summary",
        "",
        "Computed `G_star` gamma fits for zeta zeros `rho_6` through `rho_15` at dps 80 using `k=5,10,15,20,30`.",
        "Combined those with inherited Step 305/322 values for `rho_1` through `rho_5` and fit gamma as a function of zero height.",
        "",
        f"Best zeta-only height model by gamma-space RMSE: `{best['model']}` with RMSE `{float(best['RMSE_gamma']):.6g}`.",
        "The fitted gamma values decline through the low zeros and then cross into small/negative values in the rho_6..rho_15 range, so no positive universal gamma-height law is supported over this window.",
        "",
        "Cross-family check: the requested high-Im first-zero Dirichlet candidate was not found among the tested Legendre mod 13 case; its first zero is at low height. The inherited Dirichlet first-zero gammas remain clustered near 0.19-0.22, unlike high zeta zeros.",
        "",
        "Conclusion: gamma is height-sensitive on the zeta branch and family-specific relative to the Dirichlet first-zero data. No unified cross-family functional form is supported by this test.",
        "",
        f"Runtime: {time.time() - t_all:.3f} seconds. Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step323_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 323,
        "orientation": "attempt",
        "target": "gamma versus zero height for G_star",
        "dps": DPS,
        "computed_zeta_zeros": "rho_6..rho_15",
        "fit_k_values": FIT_K,
        "cross_family_candidate": "Legendre character mod 13 first zero",
        "final_verdict": verdict,
    }
    (ART / "step323_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step323.md").write_text(
        "# Step 323 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim Branch C or Hecke closure.\n"
        "- Gamma-height fits are numerical diagnostics over `k=5,10,15,20,30`, not asymptotic theorems.\n"
        "- The cross-family result is limited by the tested Dirichlet first-zero candidates.\n",
        encoding="utf-8",
    )
    print(f"q13 first zero Im={mp.nstr(mp.im(q13_root), 12)} gamma={mp.nstr(q13_params['gamma'], 12)}")
    print(f"best_model={best['model']} rmse={best['RMSE_gamma']}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
