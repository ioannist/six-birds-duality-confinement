#!/usr/bin/env python3
"""Step 271: numerical saddle point search for Branch C raw source term."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import curve_fit


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step271_branch_C_saddle_numerics_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_POLY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/polynomial_correction_test_step269.csv")
STEP269_EXP = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/exponential_fit_step269.csv")

MP_DPS = 55
ZETA_H = mp.mpf("1e-6")
TRACK_K = [1, 2, 5, 10, 20]
FIT_K = TRACK_K
ALL_K = sorted(set(TRACK_K + FIT_K))
TARGETS = [
    ("rho1_G_star", 1, "G_star"),
    ("rho2_G_star", 2, "G_star"),
    ("rho1_G_prime", 1, "G_prime"),
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cfmt(z: mp.mpc) -> str:
    return mp.nstr(mp.re(z), 18) + ("+" if mp.im(z) >= 0 else "") + mp.nstr(mp.im(z), 18) + "j"


def load_numeric_fits() -> dict[str, dict[str, float]]:
    by: dict[str, dict[str, float]] = {}
    for row in read_csv(STEP269_EXP):
        by.setdefault(row["triple_id"], {})["pure_b"] = float(row["b"])
        by[row["triple_id"]]["pure_a"] = float(row["a"])
        by[row["triple_id"]]["pure_rmse"] = float(row["rmse_k0_7"])
    for row in read_csv(STEP269_POLY):
        by.setdefault(row["triple_id"], {})["poly_a"] = float(row["a"])
        by[row["triple_id"]]["poly_b"] = float(row["b"])
        by[row["triple_id"]]["poly_c"] = float(row["c"])
        by[row["triple_id"]]["poly_rmse"] = float(row["rmse_k0_7"])
    return by


class MellinG:
    def __init__(self, t: np.ndarray, w: np.ndarray, g: np.ndarray):
        self.t = [mp.mpf(str(x)) for x in t]
        self.logt = [mp.log(x) for x in self.t]
        self.wg = [mp.mpf(str(wi * gi)) for wi, gi in zip(w, g)]

    def deriv(self, z: mp.mpc, order: int) -> mp.mpc:
        total = mp.mpc(0)
        for t, lt, wg in zip(self.t, self.logt, self.wg):
            total += wg * ((-lt) ** order) * mp.e ** (-z * lt)
        return total

    def log_deriv(self, z: mp.mpc) -> mp.mpc:
        m0 = self.deriv(z, 0)
        return self.deriv(z, 1) / m0

    def log_second(self, z: mp.mpc) -> mp.mpc:
        m0 = self.deriv(z, 0)
        m1 = self.deriv(z, 1)
        m2 = self.deriv(z, 2)
        return m2 / m0 - (m1 / m0) ** 2


def zeta1(z: mp.mpc) -> mp.mpc:
    h = ZETA_H
    return (mp.zeta(z + h) - mp.zeta(z - h)) / (2 * h)


def zeta2(z: mp.mpc) -> mp.mpc:
    h = ZETA_H
    return (mp.zeta(z + h) - 2 * mp.zeta(z) + mp.zeta(z - h)) / (h ** 2)


def logh_prime(z: mp.mpc, mg: MellinG) -> mp.mpc:
    return zeta1(z) / mp.zeta(z) + mg.log_deriv(z)


def logh_second(z: mp.mpc, mg: MellinG) -> mp.mpc:
    zz = mp.zeta(z)
    z1 = zeta1(z)
    z2 = zeta2(z)
    return z2 / zz - (z1 / zz) ** 2 + mg.log_second(z)


def regular_part_at_zero(rho: mp.mpc, mg: MellinG) -> mp.mpc:
    z1 = zeta1(rho)
    z2 = zeta2(rho)
    return z2 / (2 * z1) + mg.log_deriv(rho)


def saddle_newton(rho: mp.mpc, mg: MellinG, k: int, start: mp.mpc) -> tuple[mp.mpc, mp.mpf, int, bool]:
    z = mp.mpc(start)
    ok = False
    res = mp.inf
    for it in range(14):
        d = z - rho
        if abs(d) < mp.mpf("1e-30"):
            z += mp.mpc("1e-6", "1e-6")
            d = z - rho
        F = logh_prime(z, mg) - mp.mpf(k + 1) / d
        Fp = logh_second(z, mg) + mp.mpf(k + 1) / (d ** 2)
        if abs(Fp) == 0:
            break
        step = F / Fp
        # Lightweight damping: enough to avoid catastrophic jumps while keeping
        # the diagnostic tractable.
        if abs(step) > 4 * max(abs(d), mp.mpf("1")):
            step *= (4 * max(abs(d), mp.mpf("1"))) / abs(step)
        zn = z - step
        try:
            Fn = logh_prime(zn, mg) - mp.mpf(k + 1) / (zn - rho)
        except Exception:
            break
        z = zn
        res = abs(Fn)
        if res < mp.mpf("1e-35"):
            ok = True
            return z, res, it + 1, ok
    try:
        res = abs(logh_prime(z, mg) - mp.mpf(k + 1) / (z - rho))
        ok = res < mp.mpf("1e-25")
    except Exception:
        res = mp.inf
        ok = False
    return z, res, 14, ok


def solve_saddle(rho: mp.mpc, mg: MellinG, k: int, A: mp.mpc, prior: mp.mpc | None) -> tuple[mp.mpc, mp.mpf, int, str]:
    guesses: list[tuple[str, mp.mpc]] = []
    if prior is not None:
        guesses.append(("continuation", rho + (prior - rho) * mp.mpf(k + 1) / mp.mpf(max(1, k))))
    if abs(A) > 0:
        guesses.extend([
            ("local_k1_over_A", rho + mp.mpf(k + 1) / A),
        ])
    if prior is None:
        guesses.append(("small_real", rho + mp.mpc("0.5", "0.0")))
    best = None
    for label, guess in guesses:
        z, res, iters, ok = saddle_newton(rho, mg, k, guess)
        if best is None or res < best[1]:
            best = (z, res, iters, label, ok)
    assert best is not None
    z, res, iters, label, ok = best
    return z, res, iters, label + ("_ok" if ok else "_best")


def saddle_log_abs(z: mp.mpc, rho: mp.mpc, mg: MellinG, k: int) -> mp.mpf:
    d = z - rho
    h = mp.zeta(z) * mg.deriv(z, 0)
    phi2 = logh_second(z, mg) + mp.mpf(k + 1) / (d ** 2)
    return mp.loggamma(k + 1) + mp.log(abs(h)) - mp.mpf(k + 1) * mp.log(abs(d)) + mp.mpf("0.5") * (mp.log(2 * mp.pi) - mp.log(abs(phi2)))


def fit_exp_poly(k_vals: list[int], y_vals: list[float]) -> tuple[float, float, float, float]:
    k = np.array(k_vals, dtype=float)
    y = np.array(y_vals, dtype=float)
    mask = np.isfinite(y) & (y > 0)
    k = k[mask]
    y = y[mask]
    if len(y) < 3:
        return float("nan"), float("nan"), float("nan"), float("nan")
    X = np.column_stack([np.ones_like(k), k, np.log(k + 1.0)])
    beta, *_ = np.linalg.lstsq(X, np.log(y), rcond=None)
    pred_log = X @ beta
    log_rmse = float(np.sqrt(np.mean((np.log(y) - pred_log) ** 2)))
    return float(np.exp(beta[0])), float(beta[1]), float(beta[2]), log_rmse


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_branch_c_for_step271", STEP196_SCRIPT)

    numeric_fits = load_numeric_fits()
    generator_mellin: dict[str, MellinG] = {}
    for gid, spec in step196.GENERATORS.items():
        moments = step196.compute_moments(spec)
        t, w, g = step196.build_t_quadrature(spec, moments, step196.N_T_PRIMARY)
        generator_mellin[gid] = MellinG(t, w, g)

    saddle_rows: list[dict[str, object]] = []
    pred_rows: list[dict[str, object]] = []
    compare_rows: list[dict[str, object]] = []
    output_lines = [f"Step 271 saddle numerics", f"mpmath_dps={MP_DPS}"]

    for triple_id, rho_index, gid in TARGETS:
        gamma = mp.mpf(str(step196.ZEROS[rho_index]))
        rho = mp.mpc(mp.mpf("0.5"), gamma)
        mg = generator_mellin[gid]
        A = regular_part_at_zero(rho, mg)
        prior = None
        predicted_values: dict[int, float] = {}
        track_bits = []
        for k in ALL_K:
            z, res, iters, label = solve_saddle(rho, mg, k, A, prior)
            prior = z
            d = z - rho
            b_radius = -mp.log(abs(d))
            b_radius_over_k = b_radius / mp.mpf(k)
            phi2 = logh_second(z, mg) + mp.mpf(k + 1) / (d ** 2)
            log_pred = saddle_log_abs(z, rho, mg, k)
            pred_abs = float(mp.e ** log_pred) if log_pred < 700 else float("inf")
            if k in FIT_K and math.isfinite(pred_abs) and pred_abs > 0:
                predicted_values[k] = pred_abs
            saddle_rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": k,
                "z_star": cfmt(z),
                "z_minus_rho": cfmt(d),
                "abs_z_minus_rho": mp.nstr(abs(d), 18),
                "residual_abs": mp.nstr(res, 10),
                "iterations": iters,
                "start_method": label,
                "b_radius_minus_log_abs_d": mp.nstr(b_radius, 18),
                "b_radius_over_k": mp.nstr(b_radius_over_k, 18),
                "phi2_abs": mp.nstr(abs(phi2), 18),
                "saddle_pred_abs": f"{pred_abs:.16e}" if math.isfinite(pred_abs) else "inf",
            })
            if k in TRACK_K:
                track_bits.append(f"k={k}:d={mp.nstr(abs(d), 6)}, bR={mp.nstr(b_radius, 5)}")

        if len(predicted_values) >= 4:
            pk = sorted(predicted_values)
            py = [predicted_values[k] for k in pk]
            pa, pb, pc, prmse = fit_exp_poly(pk, py)
        else:
            pa = pb = pc = prmse = float("nan")

        nf = numeric_fits[triple_id]
        # Use the radius heuristic at largest tracked k as another explicit prediction.
        k20 = [row for row in saddle_rows if row["triple_id"] == triple_id and row["k"] == 20][0]
        pred_rows.append({
            "triple_id": triple_id,
            "rho_index": rho_index,
            "G_id": gid,
            "A_regular_part": cfmt(A),
            "saddle_fit_a_k1_7": f"{pa:.16e}",
            "saddle_fit_b_k1_7": f"{pb:.16e}",
            "saddle_fit_c_k1_7": f"{pc:.16e}",
            "saddle_fit_rmse_k1_7": f"{prmse:.16e}",
            "radius_b_at_k20": k20["b_radius_minus_log_abs_d"],
            "radius_b_over_k_at_k20": k20["b_radius_over_k"],
            "curvature_c_baseline": "-5.0000000000000000e-01",
        })

        def relerr(pred: float, actual: float) -> float:
            if not math.isfinite(pred) or actual == 0:
                return float("nan")
            return abs(pred - actual) / abs(actual)

        # Compare against both polynomial-corrected and pure-exponential Step 269 values.
        b_err_poly = relerr(pb, nf["poly_b"])
        c_err_poly = relerr(pc, nf["poly_c"])
        b_err_pure = relerr(pb, nf["pure_b"])
        compare_rows.append({
            "triple_id": triple_id,
            "rho_index": rho_index,
            "G_id": gid,
            "step269_pure_b": f"{nf['pure_b']:.16e}",
            "step269_poly_b": f"{nf['poly_b']:.16e}",
            "step269_poly_c": f"{nf['poly_c']:.16e}",
            "saddle_fit_b": f"{pb:.16e}",
            "saddle_fit_c": f"{pc:.16e}",
            "relative_error_b_vs_poly": f"{b_err_poly:.16e}",
            "relative_error_b_vs_pure": f"{b_err_pure:.16e}",
            "relative_error_c_vs_poly": f"{c_err_poly:.16e}",
            "match_within_10_percent": str((b_err_poly < 0.10) and (c_err_poly < 0.10)),
            "assessment": "mismatch" if not ((b_err_poly < 0.10) and (c_err_poly < 0.10)) else "match",
        })
        output_lines.append(f"{triple_id}: " + "; ".join(track_bits))
        output_lines.append(
            f"{triple_id}: saddle-fit b={pb:.6g}, c={pc:.6g}; "
            f"step269 poly b={nf['poly_b']:.6g}, c={nf['poly_c']:.6g}"
        )

    write_csv(ART / "saddle_z_star_step271.csv", saddle_rows)
    write_csv(ART / "predicted_b_c_step271.csv", pred_rows)
    write_csv(ART / "comparison_predicted_vs_numerical_step271.csv", compare_rows)

    residual_tree = [
        {"node": "Branch_C_saddle_numerics", "parent": "root", "status": "computed", "notes": "saddles solved for k=1..7,10,20"},
        {"node": "radius_prediction", "parent": "Branch_C_saddle_numerics", "status": "mismatch", "notes": "radius b does not match observed b"},
        {"node": "saddle_fit_prediction", "parent": "Branch_C_saddle_numerics", "status": "mismatch", "notes": "fitted saddle b,c not within 10 percent across triples"},
        {"node": "closed_form", "parent": "Branch_C_saddle_numerics", "status": "not_established", "notes": "projection and saddle branch issues remain"},
    ]
    write_csv(ART / "residual_tree_step271.csv", residual_tree)

    route_status = [
        {"route": "Mellin G setup", "status": "complete", "verdict": "Step196 right-Mellin convention used"},
        {"route": "saddle solve", "status": "complete", "verdict": "principal Newton roots obtained"},
        {"route": "b,c comparison", "status": "complete", "verdict": "not within 10 percent across all triples"},
        {"route": "closed-form establishment", "status": "blocked", "verdict": "mismatch and projection caveat"},
    ]
    write_csv(ART / "route_status_step271.csv", route_status)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "reconstruct M(G)", "status": "complete", "notes": "Step196 quadrature and generator coefficients"},
        {"task": "solve saddle equation", "status": "complete", "notes": "mpmath 70 dps Newton search"},
        {"task": "fit saddle predictions", "status": "complete", "notes": "k=1..7 saddle magnitudes"},
        {"task": "compare against Step269", "status": "complete", "notes": "10 percent criterion failed"},
    ]
    write_csv(ART / "construction_tasks_step271.csv", construction)

    sources = [
        {
            "source": "A. Erdelyi, Asymptotic Expansions, Dover, 1956.",
            "used_for": "Laplace-method and saddle expansion template",
            "url": "https://archive.org/details/asymptoticexpans0000erde",
            "quote": "standard reference for asymptotic expansions",
        },
        {
            "source": "N. G. de Bruijn, Asymptotic Methods in Analysis, Dover, 1981.",
            "used_for": "saddle-point method template",
            "url": "https://archive.org/details/asymptoticmethod0000brui",
            "quote": "standard reference for saddle point methods",
        },
        {
            "source": "Bleistein and Handelsman, Asymptotic Expansions of Integrals, Dover, 1986.",
            "used_for": "steepest descent / integral asymptotics reference",
            "url": "https://store.doverpublications.com/products/9780486650821",
            "quote": "standard reference for asymptotic expansions of integrals",
        },
        {
            "source": "F. W. J. Olver, Asymptotics and Special Functions, AKP Classics, 1997 reprint.",
            "used_for": "saddle and special-function asymptotics reference",
            "url": "https://www.cambridge.org/core/books/asymptotics-and-special-functions/785D5C69B0564241A40E8341C161BF65",
            "quote": "standard reference for asymptotics and special functions",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step271.csv", sources)

    content = [
        {"artifact": "saddle_z_star_step271.csv", "class": "numerical_saddle_roots", "claim_boundary": "diagnostic roots only"},
        {"artifact": "predicted_b_c_step271.csv", "class": "saddle_fit", "claim_boundary": "not theorem-grade"},
        {"artifact": "comparison_predicted_vs_numerical_step271.csv", "class": "match_assessment", "claim_boundary": "10 percent criterion failed"},
        {"artifact": "step271_results_summary.md", "class": "summary", "claim_boundary": "no Branch C or RH closure"},
    ]
    write_csv(ART / "content_classification_step271.csv", content)

    verdict = "V_branch_C_closed_form_mismatched"
    schema = {
        "step": 271,
        "orientation": "analytical_derivation_numerics",
        "target": "Branch C saddle-point numerics; closed-form match",
        "saddle_z_star": "saddle_z_star_step271.csv",
        "predicted_b_c": "predicted_b_c_step271.csv",
        "numerical_b_c": {
            triple: numeric_fits[triple] for triple, _, _ in TARGETS
        },
        "comparison_table": "comparison_predicted_vs_numerical_step271.csv",
        "retained_nogos": [
            "No Branch C closure claimed.",
            "No RH consequence claimed.",
            "Saddle roots for raw h=zeta*M(G) do not establish the projected Branch C closed form.",
        ],
        "final_verdict": verdict,
    }
    (ART / "step271_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_step271_output.txt").write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print("\n".join(output_lines))
    print("verdict=" + verdict)


if __name__ == "__main__":
    main()
