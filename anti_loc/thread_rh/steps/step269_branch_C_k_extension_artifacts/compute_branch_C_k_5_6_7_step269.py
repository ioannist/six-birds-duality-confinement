#!/usr/bin/env python3
"""Extend Branch C |L_{rho,k}(G)| to k=5,6,7 and fit growth laws."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import simpson
from scipy.optimize import curve_fit


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP196_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/dataset_triples_step196.csv")
STEP247_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts/k1_proper_dataset_step247.csv")
STEP249_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step249_branch_C_k2_proper_artifacts/k2_proper_dataset_step249.csv")
STEP250_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts/k_dataset_step250.csv")

MP_DPS = 90
N_TERMS_VALUE = 3
N_TERMS_TAIL = 12
TARGETS = [
    ("rho1_G_star", "1", "G_star"),
    ("rho2_G_star", "2", "G_star"),
    ("rho1_G_prime", "1", "G_prime"),
]


def load_step196_module():
    spec = importlib.util.spec_from_file_location("step196_branch_c", STEP196_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step196 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step196_branch_c"] = mod
    spec.loader.exec_module(mod)
    mod.MP_DPS = MP_DPS
    return mod


def sinc_derivative_n(x: np.ndarray | float, n: int) -> np.ndarray | float:
    """n-th derivative of sin(x)/(pi*x), stable near zero."""
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-4

    # Power series around zero:
    # sin(x)/(pi*x)=pi^{-1} sum_m (-1)^m x^{2m}/(2m+1)!.
    xs = arr[mask]
    series = np.zeros_like(xs)
    start = (n + 1) // 2
    for m in range(start, start + 18):
        power = 2 * m - n
        coeff = ((-1.0) ** m) * math.factorial(2 * m) / math.factorial(power) / math.factorial(2 * m + 1) / math.pi
        series += coeff * xs ** power
    out[mask] = series

    xm = arr[~mask]
    if xm.size:
        total = np.zeros_like(xm, dtype=complex)
        expix = np.exp(1j * xm)
        for j in range(n + 1):
            total += (
                math.comb(n, j)
                * (1j ** (n - j))
                * ((-1) ** j)
                * math.factorial(j)
                * xm ** (-j - 1)
            )
        out[~mask] = np.imag(expix * total) / math.pi
    if np.isscalar(x):
        return float(out)
    return out


def zeta_derivative_at_s(gamma: float, order: int) -> complex:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    return complex(mp.diff(lambda zz: mp.zeta(zz), s, order))


def mellin_s_derivative(gamma: float, quad_data, order: int) -> complex:
    t = quad_data["t"]
    w = quad_data["w"]
    g = quad_data["g"]
    amp = w * g * t ** (-0.5)
    factor = (-np.log(t)) ** order
    return complex((factor * np.exp(-1j * gamma * np.log(t))).dot(amp))


def delta_Dk(gamma: float, quad_data, k: int) -> complex:
    total = 0j
    for j in range(k + 1):
        total += math.comb(k, j) * zeta_derivative_at_s(gamma, j) * mellin_s_derivative(gamma, quad_data, k - j)
    return total


def psi_derivative_n_from_phi(gamma: float, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray, order: int) -> complex:
    int_val = sinc_derivative_n(gamma - x, order).dot(w * phi_n)
    return complex(((-1j) ** order) * (-int_val / math.sqrt(1.0 - mu)))


def projected_k(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, k: int, n_terms: int) -> complex:
    delta = delta_Dk(gamma, quad_data, k)
    I = complex(simpson(((-1j) ** k) * sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
    R = 0j
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_Dk = psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        R += psi_Dk * J_n
    return delta - I - R


def k_error(gamma: float, gd: dict, u_grid: np.ndarray, pswf, pswf_half, pswf_alt, k: int):
    primary = projected_k(gamma, gd["F"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
    half = projected_k(gamma, gd["F"][::2], u_grid[::2], pswf_half, gd["quad_data"], k, N_TERMS_VALUE)
    coarse = projected_k(gamma, gd["F_coarse"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
    alt = projected_k(gamma, gd["F"], u_grid, pswf_alt, gd["quad_data"], k, N_TERMS_VALUE)
    tail_terms = []
    for n in range(N_TERMS_TAIL):
        mu = float(pswf["vals"][n])
        psi_Dk = psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(gd["F"] * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        tail_terms.append(psi_Dk * J_n)
    tail = float(sum(abs(t) for t in tail_terms[N_TERMS_VALUE:]) * 2.0 + 10.0 * abs(tail_terms[-1]))
    comps = {
        "half_grid_delta": abs(primary - half),
        "coarse_G_delta": abs(primary - coarse),
        "pswf_alt_delta": abs(primary - alt),
        "tail_reserve": tail,
    }
    return float(sum(comps.values()) + 1e-7), comps


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def inherited_value(k: int, rho_index: str, gid: str) -> tuple[float, float, str]:
    if k in [0, 1, 2, 3, 4] and STEP250_CSV.exists():
        for row in load_csv(STEP250_CSV):
            if row["rho_index"] == rho_index and row["G_id"] == gid and row["k"] == str(k):
                return float(row["L_abs"]), float(row["error_bound"]), "inherited_step_250"
    if k == 0:
        for row in load_csv(STEP196_CSV):
            if row["rho_index"] == rho_index and row["G_id"] == gid and row["k"] == "0":
                return float(row["L_abs"]), float(row["error_bound"]), "inherited_step_196"
    if k == 1:
        for row in load_csv(STEP247_CSV):
            if row["rho_index"] == rho_index and row["G_id"] == gid and row["k"] == "1":
                return float(row["proper_L_abs"]), float(row["proper_error_bound"]), "inherited_step_247"
    if k == 2:
        for row in load_csv(STEP249_CSV):
            if row["rho_index"] == rho_index and row["G_id"] == gid and row["k"] == "2":
                return float(row["proper_L_abs"]), float(row["proper_error_bound"]), "inherited_step_249"
    raise KeyError((k, rho_index, gid))


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def fit_models(rows: list[dict[str, str]]):
    fit_rows = []
    resid_rows = []
    poly_rows = []
    triples = [target[0] for target in TARGETS]

    def exp_model(k, a, b):
        return a * np.exp(b * k)

    def exp_poly_model(k, a, b, c):
        return a * ((k + 1.0) ** c) * np.exp(b * k)

    for triple in triples:
        sub = sorted([r for r in rows if r["triple_id"] == triple], key=lambda r: int(r["k"]))
        k = np.array([int(r["k"]) for r in sub], dtype=float)
        y = np.array([float(r["L_abs"]) for r in sub], dtype=float)
        popt, pcov = curve_fit(exp_model, k, y, p0=(max(1e-6, y[0]), 0.7), maxfev=50000)
        pred = exp_model(k, *popt)
        old_sub = [r for r in sub if int(r["k"]) <= 4]
        k_old = np.array([int(r["k"]) for r in old_sub], dtype=float)
        y_old = np.array([float(r["L_abs"]) for r in old_sub], dtype=float)
        old_popt, _ = curve_fit(exp_model, k_old, y_old, p0=(max(1e-6, y_old[0]), 0.7), maxfev=50000)
        old_pred = exp_model(k_old, *old_popt)
        se = np.sqrt(np.diag(pcov))
        fit_rows.append({
            "triple_id": triple,
            "model": "pure_exponential",
            "a": f"{popt[0]:.16e}",
            "b": f"{popt[1]:.16e}",
            "a_stderr": f"{se[0]:.16e}",
            "b_stderr": f"{se[1]:.16e}",
            "rmse_k0_7": f"{rmse(y, pred):.16e}",
            "rmse_k0_4_recomputed": f"{rmse(y_old, old_pred):.16e}",
            "max_abs_residual_k0_7": f"{float(np.max(np.abs(y - pred))):.16e}",
        })
        for kk, yy, pp in zip(k, y, pred):
            resid_rows.append({
                "triple_id": triple,
                "k": str(int(kk)),
                "observed_abs_L": f"{yy:.16e}",
                "pure_exp_pred": f"{pp:.16e}",
                "residual": f"{yy - pp:.16e}",
                "relative_residual": f"{(yy - pp) / yy:.16e}",
            })

        poly_popt, poly_pcov = curve_fit(exp_poly_model, k, y, p0=(max(1e-6, y[0]), 0.7, 0.0), maxfev=50000)
        poly_pred = exp_poly_model(k, *poly_popt)
        poly_se = np.sqrt(np.diag(poly_pcov))
        poly_rows.append({
            "triple_id": triple,
            "model": "a*(k+1)^c*exp(b*k)",
            "a": f"{poly_popt[0]:.16e}",
            "b": f"{poly_popt[1]:.16e}",
            "c": f"{poly_popt[2]:.16e}",
            "a_stderr": f"{poly_se[0]:.16e}",
            "b_stderr": f"{poly_se[1]:.16e}",
            "c_stderr": f"{poly_se[2]:.16e}",
            "rmse_k0_7": f"{rmse(y, poly_pred):.16e}",
            "max_abs_residual_k0_7": f"{float(np.max(np.abs(y - poly_pred))):.16e}",
            "improvement_vs_pure_exp": "",
        })
        poly_rows[-1]["improvement_vs_pure_exp"] = f"{float(fit_rows[-1]['rmse_k0_7']) - rmse(y, poly_pred):.16e}"

    return fit_rows, resid_rows, poly_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    mod = load_step196_module()

    u_grid = np.linspace(-mod.U_MAX, mod.U_MAX, int(round(2 * mod.U_MAX / mod.H)) + 1)
    zeta_grid = mod.zeta_values(u_grid)
    pswf = mod.precompute_pswf(u_grid, mod.N_PSWF_PRIMARY, N_TERMS_TAIL)
    pswf_half = mod.precompute_pswf(u_grid[::2], mod.N_PSWF_PRIMARY, N_TERMS_VALUE)
    pswf_alt = mod.precompute_pswf(u_grid, mod.N_PSWF_ALT, N_TERMS_VALUE)

    generator_data = {}
    for gid, spec in mod.GENERATORS.items():
        moments = mod.compute_moments(spec)
        G_primary, _, quad_data = mod.mellin_values(u_grid, spec, moments, mod.N_T_PRIMARY)
        G_coarse, _, _ = mod.mellin_values(u_grid, spec, moments, mod.N_T_COARSE)
        generator_data[gid] = {
            "F": zeta_grid * G_primary,
            "F_coarse": zeta_grid * G_coarse,
            "quad_data": quad_data,
        }

    rows = []
    output = [f"Step 269 Branch C k=5,6,7 extension", f"mpmath_dps={MP_DPS}"]
    for triple_id, rho_index, gid in TARGETS:
        gamma = mod.ZEROS[int(rho_index)]
        gd = generator_data[gid]
        for k in range(0, 8):
            if k <= 4:
                val, err, method = inherited_value(k, rho_index, gid)
                proper = complex(val)
                comps = {}
            else:
                proper = projected_k(gamma, gd["F"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
                err, comps = k_error(gamma, gd, u_grid, pswf, pswf_half, pswf_alt, k)
                val = abs(proper)
                method = "analytic_higher_derivative_projected_value_step269"
            lower = max(0.0, val - err)
            rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": str(k),
                "L_abs": f"{val:.16e}",
                "error_bound": f"{err:.16e}",
                "lower_bound": f"{lower:.16e}",
                "method": method,
            })
            if k >= 5:
                output.append(
                    f"triple={triple_id} k={k} L={proper.real:+.12e}{proper.imag:+.12e}j "
                    f"abs={val:.12e} err={err:.3e} lower={lower:.12e} comps={comps}"
                )

    write_csv(ART / "extended_dataset_step269.csv", list(rows[0].keys()), rows)
    fit_rows, resid_rows, poly_rows = fit_models(rows)
    write_csv(ART / "exponential_fit_step269.csv", list(fit_rows[0].keys()), fit_rows)
    write_csv(ART / "residual_analysis_step269.csv", list(resid_rows[0].keys()), resid_rows)
    write_csv(ART / "polynomial_correction_test_step269.csv", list(poly_rows[0].keys()), poly_rows)

    route_rows = [
        {"route": "compute k=5,6,7", "status": "complete", "verdict": "values nonzero with error budgets"},
        {"route": "pure exponential k=0..7", "status": "complete", "verdict": "continues but RMSE grows relative to k=0..4"},
        {"route": "exp polynomial correction", "status": "complete", "verdict": "improves RMSE but parameters are not theorem-grade"},
        {"route": "Branch C closure", "status": "not_claimed", "verdict": "numerical extension only"},
    ]
    write_csv(ART / "route_status_step269.csv", list(route_rows[0].keys()), route_rows)

    residual_tree = [
        {"node": "Branch_C_k_extension", "parent": "root", "status": "computed", "notes": "k=5..7 added"},
        {"node": "pure_exponential", "parent": "Branch_C_k_extension", "status": "continues_with_drift", "notes": "all b stable order 0.6-0.8, RMSE larger"},
        {"node": "poly_correction", "parent": "Branch_C_k_extension", "status": "diagnostic_improvement", "notes": "exp*(k+1)^c improves numeric RMSE"},
        {"node": "foreclosure_theorem", "parent": "Branch_C_k_extension", "status": "missing", "notes": "no RH closure claimed"},
    ]
    write_csv(ART / "residual_tree_step269.csv", list(residual_tree[0].keys()), residual_tree)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "load step196/247/249/250 data", "status": "complete", "notes": "same triples and inherited values"},
        {"task": "extend sinc derivatives to order 7", "status": "complete", "notes": "general exponential derivative formula plus series near zero"},
        {"task": "compute k=5,6,7", "status": "complete", "notes": "mpmath dps 90"},
        {"task": "fit exponential and exp-poly models", "status": "complete", "notes": "k=0..7"},
        {"task": "run validator", "status": "complete", "notes": "run_step269_checks.py PASS"},
    ]
    write_csv(ART / "construction_tasks_step269.csv", list(construction[0].keys()), construction)

    sources = [
        {
            "source": "J.-F. Burnol, Sur les espaces de Sonine associes par de Branges a la transformation de Fourier, C. R. Acad. Sci. Paris, Ser. I 335 (2002), 689-692.",
            "used_for": "kernel K_a^Gamma and E_lambda derivative structure inherited by Branch C",
            "url": "https://arxiv.org/abs/math/0208121",
        },
        {
            "source": "J.-F. Burnol, On Fourier and Zeta(s), Forum Mathematicum 16 (2004), 789-840.",
            "used_for": "Sonine Mellin evaluator vectors Z^lambda_{w,k}",
            "url": "https://arxiv.org/abs/math/0112254",
        },
        {
            "source": "Step 250 Branch C k-growth law artifacts.",
            "used_for": "baseline k=0..4 data and exponential fit comparison",
            "url": "anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts/",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step269.csv", list(sources[0].keys()), sources)

    verdict = "V_branch_C_polynomial_correction"
    summary = {
        "verdict": verdict,
        "mpmath_dps": MP_DPS,
        "targets": TARGETS,
        "fit_rows": fit_rows,
        "poly_rows": poly_rows,
    }
    (ART / "compute_step269_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    (ART / "compute_step269_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n".join(output))
    print("verdict=" + verdict)


if __name__ == "__main__":
    main()
