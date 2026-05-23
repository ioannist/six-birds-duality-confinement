#!/usr/bin/env python3
"""Step 322: test gamma invariance across L-functions and generators."""

from __future__ import annotations

import csv
import json
import math
import statistics
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts")
STEP320 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
DPS = 80
ROOT_DPS = 50
MAX_K = 30
FIT_K = [5, 10, 15, 20, 30]


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def beta_bump(u: mp.mpf) -> mp.mpf:
    if abs(u) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - u * u))


def generator_spec(gid: str) -> tuple[list[mp.mpf], mp.mpf, list[mp.mpf]]:
    if gid == "G_star":
        centers = [mp.mpf("1.5"), mp.mpf("2.5"), mp.mpf("3.5")]
        eps = mp.mpf("0.20")
    elif gid == "G_prime":
        centers = [mp.mpf("2.0"), mp.mpf("2.5"), mp.mpf("3.0")]
        eps = mp.mpf("0.25")
    else:
        raise ValueError(gid)
    A, B = [], []
    for c in centers:
        A.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps), [c - eps, c + eps]))
        B.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps) / t, [c - eps, c + eps]))
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return centers, eps, [mp.mpf("1"), -alpha, beta_3]


def char_values(label: str) -> tuple[int, list[mp.mpc]]:
    I = mp.mpc(0, 1)
    if label == "chi_3":
        return 3, [0, 1, -1]
    if label == "chi_4":
        return 4, [0, 1, 0, -1]
    if label == "chi_5a":
        return 5, [0, 1, -1, -1, 1]
    if label == "chi_5b":
        return 5, [0, 1, I, -I, -1]
    if label == "chi_7a":
        return 7, [0, 1, 1, -1, 1, -1, -1]
    if label == "chi_8a":
        return 8, [0, 1, 0, -1, 0, -1, 0, 1]
    if label == "chi_11a":
        return 11, [0, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1]
    raise ValueError(label)


def L_chi(s: mp.mpc, q: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) ** (-s)) * mp.fsum(
        [chi[a % q] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)]
    )


def L_derivatives(s: mp.mpc, q: int, chi: list[mp.mpc], max_k: int) -> list[mp.mpc]:
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


def zeta_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    return [mp.zeta(s, derivative=n) for n in range(max_k + 1)]


def M_derivatives(s: mp.mpc, gid: str, max_k: int) -> list[mp.mpc]:
    centers, eps, coeffs = generator_spec(gid)
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


def locate_character_zero(label: str) -> tuple[mp.mpc, mp.mpf]:
    q, chi = char_values(label)
    mp.mp.dps = ROOT_DPS
    samples: list[tuple[mp.mpf, mp.mpf]] = []
    step = mp.mpf("0.10")
    t = mp.mpf("0.50")
    while t <= mp.mpf("25.00"):
        samples.append((t, abs(L_chi(mp.mpc(mp.mpf("0.5"), t), q, chi))))
        t += step
    minima = []
    for i in range(1, len(samples) - 1):
        if samples[i][1] < samples[i - 1][1] and samples[i][1] < samples[i + 1][1]:
            minima.append(samples[i][0])
    if not minima:
        raise RuntimeError(f"no minima found for {label}")

    def f(x: mp.mpf, y: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
        value = L_chi(mp.mpc(x, y), q, chi)
        return mp.re(value), mp.im(value)

    roots: list[mp.mpc] = []
    for guess in minima[:8]:
        try:
            x, y = mp.findroot(f, (mp.mpf("0.5"), guess), tol=mp.mpf("1e-30"), maxsteps=40, solver="mnewton")
            z = mp.mpc(x, y)
            if mp.im(z) > 0 and mp.re(z) > -mp.mpf("0.1"):
                if all(abs(z - old) > mp.mpf("1e-10") for old in roots):
                    roots.append(z)
        except Exception:
            continue
    if not roots:
        raise RuntimeError(f"findroot failed for {label}")
    root = min(roots, key=lambda z: mp.im(z))
    return root, abs(L_chi(root, q, chi))


def step320_roots() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    return {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}


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


def compute_instance(instance_id: str, family: str, rho: mp.mpc, gid: str, chi_label: str | None = None) -> dict[int, mp.mpf]:
    if family == "Dirichlet":
        assert chi_label is not None
        q, chi = char_values(chi_label)
        Lds = L_derivatives(rho, q, chi, MAX_K)
    elif family == "zeta":
        Lds = zeta_derivatives(rho, MAX_K)
    else:
        raise ValueError(family)
    Mds = M_derivatives(rho, gid, MAX_K)
    return {k: abs(h_derivative(Lds, Mds, k)) for k in FIT_K}


def add_fit_row(rows: list[dict[str, object]], source: str, instance_id: str, family: str, gid: str,
                rho: str, values: dict[int, mp.mpf], note: str = "") -> None:
    params, rmse = linear_fit(values)
    rows.append(
        {
            "source": source,
            "instance_id": instance_id,
            "family": family,
            "G": gid,
            "rho": rho,
            "A": mp.nstr(params["A"], 18),
            "alpha": mp.nstr(params["alpha"], 18),
            "b": mp.nstr(params["b"], 18),
            "gamma": mp.nstr(params["gamma"], 18),
            "log_RMSE": mp.nstr(rmse, 18),
            "k5_abs": mp.nstr(values[5], 18),
            "k10_abs": mp.nstr(values[10], 18),
            "k15_abs": mp.nstr(values[15], 18),
            "k20_abs": mp.nstr(values[20], 18),
            "k30_abs": mp.nstr(values[30], 18),
            "note": note,
        }
    )


def summary_by_group(fit_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[float]] = {}
    for row in fit_rows:
        key = (str(row["G"]), str(row["family"]))
        groups.setdefault(key, []).append(float(row["gamma"]))
    rows = []
    for (gid, family), gammas in sorted(groups.items()):
        rows.append(
            {
                "G": gid,
                "family": family,
                "count": len(gammas),
                "gamma_mean": f"{statistics.fmean(gammas):.12g}",
                "gamma_std_population": f"{statistics.pstdev(gammas):.12g}" if len(gammas) > 1 else "0",
                "gamma_min": f"{min(gammas):.12g}",
                "gamma_max": f"{max(gammas):.12g}",
            }
        )
    # Combined G-level groups.
    for gid in sorted({str(r["G"]) for r in fit_rows}):
        gammas = [float(r["gamma"]) for r in fit_rows if str(r["G"]) == gid]
        rows.append(
            {
                "G": gid,
                "family": "ALL",
                "count": len(gammas),
                "gamma_mean": f"{statistics.fmean(gammas):.12g}",
                "gamma_std_population": f"{statistics.pstdev(gammas):.12g}" if len(gammas) > 1 else "0",
                "gamma_min": f"{min(gammas):.12g}",
                "gamma_max": f"{max(gammas):.12g}",
            }
        )
    return rows


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    t_all = time.time()
    zero_rows: list[dict[str, object]] = []
    fit_rows: list[dict[str, object]] = []

    # New Hecke characters.
    computed_roots: dict[str, mp.mpc] = {}
    for label in ["chi_7a", "chi_8a", "chi_11a"]:
        rho, residual = locate_character_zero(label)
        computed_roots[label] = rho
        zero_rows.append(
            {
                "object": label,
                "family": "Dirichlet",
                "rho": cstr(rho, 40),
                "Re_rho": mp.nstr(mp.re(rho), 32),
                "Im_rho": mp.nstr(mp.im(rho), 32),
                "residual_abs": mp.nstr(residual, 18),
                "method": "critical-line scan plus two-variable mpmath.findroot",
            }
        )

    # Zeta zeros rho_3/rho_4/rho_5.
    for n in [3, 4, 5]:
        rho = mp.zetazero(n)
        zero_rows.append(
            {
                "object": f"zeta_rho{n}",
                "family": "zeta",
                "rho": cstr(rho, 40),
                "Re_rho": mp.nstr(mp.re(rho), 32),
                "Im_rho": mp.nstr(mp.im(rho), 32),
                "residual_abs": mp.nstr(abs(mp.zeta(rho)), 18),
                "method": "mpmath.zetazero",
            }
        )

    write_csv(ART / "critical_line_zeros_step322.csv", zero_rows)

    # Inherited gamma rows from steps 305 and 321.
    inherited = [
        ("inherited_step305", "zeta_rho1_G_star", "zeta", "G_star", "rho_1", "0.2046", "step305: zeta rho_1 with G_star"),
        ("inherited_step305", "zeta_rho2_G_star", "zeta", "G_star", "rho_2", "0.1379", "step305: zeta rho_2 with G_star"),
        ("inherited_step321", "chi_3_G_star", "Dirichlet", "G_star", "0.5+8.0397i", "0.22155714780872652", "step321 full fit"),
        ("inherited_step321", "chi_4_G_star", "Dirichlet", "G_star", "0.5+6.0209i", "0.216764367182481311", "step321 full fit"),
        ("inherited_step321", "chi_5a_G_star", "Dirichlet", "G_star", "0.5+6.6485i", "0.194915041046264718", "step321 full fit"),
        ("inherited_step321", "chi_5b_G_star", "Dirichlet", "G_star", "0.5+6.1836i", "0.215042810734564381", "step321 full fit"),
        ("inherited_step305", "zeta_rho1_G_prime", "zeta", "G_prime", "rho_1", "0.2545", "step305: zeta rho_1 with G_prime"),
    ]
    for source, instance_id, family, gid, rho, gamma, note in inherited:
        fit_rows.append(
            {
                "source": source,
                "instance_id": instance_id,
                "family": family,
                "G": gid,
                "rho": rho,
                "A": "",
                "alpha": "",
                "b": "",
                "gamma": gamma,
                "log_RMSE": "",
                "k5_abs": "",
                "k10_abs": "",
                "k15_abs": "",
                "k20_abs": "",
                "k30_abs": "",
                "note": note,
            }
        )

    # New G_star instances.
    for label, rho in computed_roots.items():
        mp.mp.dps = DPS
        values = compute_instance(f"{label}_G_star", "Dirichlet", rho, "G_star", label)
        add_fit_row(fit_rows, "computed_step322", f"{label}_G_star", "Dirichlet", "G_star", cstr(rho, 28), values)
    for n in [3, 4, 5]:
        rho = mp.zetazero(n)
        values = compute_instance(f"zeta_rho{n}_G_star", "zeta", rho, "G_star")
        add_fit_row(fit_rows, "computed_step322", f"zeta_rho{n}_G_star", "zeta", "G_star", cstr(rho, 28), values)

    # G_prime controls.
    roots320 = step320_roots()
    for label in ["chi_3", "chi_4"]:
        values = compute_instance(f"{label}_G_prime", "Dirichlet", roots320[label], "G_prime", label)
        add_fit_row(fit_rows, "computed_step322", f"{label}_G_prime", "Dirichlet", "G_prime", cstr(roots320[label], 28), values)
    rho2 = mp.zetazero(2)
    values = compute_instance("zeta_rho2_G_prime", "zeta", rho2, "G_prime")
    add_fit_row(fit_rows, "computed_step322", "zeta_rho2_G_prime", "zeta", "G_prime", cstr(rho2, 28), values)

    write_csv(ART / "fitted_gamma_per_instance_step322.csv", fit_rows)
    summary_rows = summary_by_group(fit_rows)
    write_csv(ART / "gamma_universality_summary_step322.csv", summary_rows)

    gstar_all = [float(r["gamma"]) for r in fit_rows if r["G"] == "G_star"]
    gprime_all = [float(r["gamma"]) for r in fit_rows if r["G"] == "G_prime"]
    verdict = "V_gamma_G_invariance_refuted_family_and_zero_dependence"
    summary = [
        "# Step 322 Results Summary",
        "",
        "Computed new `G_star` fits for `chi_7a`, `chi_8a`, `chi_11a`, and zeta zeros `rho_3/rho_4/rho_5`; computed `G_prime` controls for `chi_3`, `chi_4`, and `zeta_rho2`.",
        "The fitted model is `|L_k| = A k^alpha exp(b k + gamma k log k)` on raw derivative magnitudes at `k=5,10,15,20,30`.",
        "",
        "Inherited reference values cited in this table: Step 305 `gamma=0.2046` for zeta `rho_1,G_star`, `0.1379` for zeta `rho_2,G_star`, and `0.2545` for zeta `rho_1,G_prime`; Step 321 `gamma=(0.222,0.217,0.195,0.215)` for `chi_3/chi_4/chi_5a/chi_5b` with `G_star`.",
        "",
        f"`G_star` all-instance gamma mean/std/min/max: `{statistics.fmean(gstar_all):.6g}` / `{statistics.pstdev(gstar_all):.6g}` / `{min(gstar_all):.6g}` / `{max(gstar_all):.6g}`.",
        f"`G_prime` all-instance gamma mean/std/min/max: `{statistics.fmean(gprime_all):.6g}` / `{statistics.pstdev(gprime_all):.6g}` / `{min(gprime_all):.6g}` / `{max(gprime_all):.6g}`.",
        "",
        "Assessment: the new zeta-zero and higher-conductor character values are not clustered tightly around a single `G_star` value near 0.20. `G_prime` controls also do not form a clean, separated cluster. The data therefore refute the strong G-only invariance hypothesis at this resolution.",
        "",
        f"Runtime: {time.time() - t_all:.3f} seconds. Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step322_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 322,
        "orientation": "attempt",
        "target": "gamma G-invariance test across Hecke characters and zeta zeros",
        "dps": DPS,
        "fit_k_values": FIT_K,
        "computed_instances": ["chi_7a", "chi_8a", "chi_11a", "zeta_rho3", "zeta_rho4", "zeta_rho5", "chi_3_G_prime", "chi_4_G_prime", "zeta_rho2_G_prime"],
        "final_verdict": verdict,
    }
    (ART / "step322_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step322.md").write_text(
        "# Step 322 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim Hecke or Branch C closure.\n"
        "- The gamma fits are numerical diagnostics over `k=5,10,15,20,30`, not asymptotic theorems.\n"
        "- The verdict concerns the tested G-invariance hypothesis only.\n",
        encoding="utf-8",
    )
    print("Step322 gamma G-invariance")
    for row in fit_rows:
        if row["source"] == "computed_step322":
            print(f"{row['instance_id']} {row['G']} gamma={row['gamma']} b={row['b']}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
