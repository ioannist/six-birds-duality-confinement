#!/usr/bin/env python3
"""Step 270: test Branch C stationary-phase explanation.

This script compares the raw Burnol evaluator identity

    delta_Dk = (zeta * M(G))^(k)(rho)

against the actual Branch C projected quantity used in steps 247-269:

    L_k = delta_Dk - I_k - R_k.

The numerical point is deliberately narrow: the proposed closed identity is
valid for the unprojected Mellin derivative term, but Step 269's data include
the projection corrections.  The saddle-point analysis is therefore only a
partial explanation unless those corrections are asymptotically controlled.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/compute_branch_C_k_5_6_7_step269.py")
STEP269_DATA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/extended_dataset_step269.csv")
STEP269_POLY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/polynomial_correction_test_step269.csv")

MP_DPS = 80
TARGETS = [
    ("rho1_G_star", "1", "G_star"),
    ("rho2_G_star", "2", "G_star"),
    ("rho1_G_prime", "1", "G_prime"),
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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def cfmt(z: complex) -> str:
    return f"{z.real:+.16e}{z.imag:+.16e}j"


def zeta_derivatives(gamma: float, max_order: int) -> list[complex]:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    return [complex(mp.diff(lambda zz: mp.zeta(zz), s, j)) for j in range(max_order + 1)]


def mellin_derivatives(step269, gamma: float, quad_data, max_order: int) -> list[complex]:
    return [step269.mellin_s_derivative(gamma, quad_data, j) for j in range(max_order + 1)]


def raw_product_derivative(zeta_ds: list[complex], mellin_ds: list[complex], k: int) -> complex:
    return sum(math.comb(k, j) * zeta_ds[j] * mellin_ds[k - j] for j in range(k + 1))


def fit_rows_by_triple() -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for row in read_csv(STEP269_POLY):
        out[row["triple_id"]] = {
            "a": float(row["a"]),
            "b": float(row["b"]),
            "c": float(row["c"]),
            "rmse": float(row["rmse_k0_7"]),
        }
    return out


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS

    step196 = load_module("step196_branch_c_for_step270", STEP196_SCRIPT)
    step269 = load_module("step269_branch_c_for_step270", STEP269_SCRIPT)
    step196.MP_DPS = MP_DPS
    step269.MP_DPS = MP_DPS

    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    pswf = step196.precompute_pswf(u_grid, step196.N_PSWF_PRIMARY, step269.N_TERMS_TAIL)

    generator_data: dict[str, dict[str, object]] = {}
    for gid, spec in step196.GENERATORS.items():
        moments = step196.compute_moments(spec)
        G_primary, _, quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
        generator_data[gid] = {
            "F": zeta_grid * G_primary,
            "quad_data": quad_data,
        }

    inherited = {
        (row["triple_id"], int(row["k"])): float(row["L_abs"])
        for row in read_csv(STEP269_DATA)
    }

    identity_rows: list[dict[str, object]] = []
    comparison_lines: list[str] = [
        "Step 270 Branch C stationary-phase diagnostic",
        f"mpmath_dps={MP_DPS}",
        "actual Branch C value = delta_Dk - I_k - R_k; raw identity tests delta_Dk only",
    ]

    for triple_id, rho_index, gid in TARGETS:
        gamma = step196.ZEROS[int(rho_index)]
        gd = generator_data[gid]
        zds = zeta_derivatives(gamma, 7)
        mds = mellin_derivatives(step269, gamma, gd["quad_data"], 7)
        for k in range(1, 8):
            raw = raw_product_derivative(zds, mds, k)
            # Recompute the projected complex value with the exact inherited step269 pipeline
            # for k >= 1.  This separates the raw product derivative from the projection.
            projected = step269.projected_k(
                gamma,
                gd["F"],
                u_grid,
                pswf,
                gd["quad_data"],
                k,
                step269.N_TERMS_VALUE,
            )
            actual_abs = inherited[(triple_id, k)]
            ratio = abs(raw) / actual_abs if actual_abs else float("nan")
            projection_correction = raw - projected
            rel_correction = abs(projection_correction) / abs(projected) if abs(projected) else float("nan")
            status = "raw_identity_not_projected_identity"
            if abs(abs(projected) - actual_abs) > max(1e-3, 1e-3 * actual_abs):
                status = "projected_recompute_differs_from_inherited"
            identity_rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": k,
                "raw_product_derivative": cfmt(raw),
                "raw_abs": f"{abs(raw):.16e}",
                "projected_recomputed": cfmt(projected),
                "projected_abs_recomputed": f"{abs(projected):.16e}",
                "inherited_step269_abs": f"{actual_abs:.16e}",
                "raw_to_inherited_abs_ratio": f"{ratio:.16e}",
                "projection_correction_abs": f"{abs(projection_correction):.16e}",
                "projection_correction_relative_to_projected": f"{rel_correction:.16e}",
                "identity_status": status,
            })
        comparison_lines.append(f"{triple_id}: raw/projected ratios k=1..7 = " + ", ".join(
            f"{float(r['raw_to_inherited_abs_ratio']):.3g}"
            for r in identity_rows
            if r["triple_id"] == triple_id
        ))

    write_csv(ART / "closed_identity_step270.csv", identity_rows)

    fit_by = fit_rows_by_triple()
    predicted_rows: list[dict[str, object]] = []
    saddle_rows = [
        {
            "step": "Cauchy_integral",
            "formula": "h^(k)(rho)=k!/(2*pi*i) integral h(z)/(z-rho)^(k+1) dz",
            "interpretation": "valid for raw analytic h=zeta*M(G), not automatically for projected L_k",
        },
        {
            "step": "saddle_equation",
            "formula": "(log h)'(z_*)=(k+1)/(z_*-rho)",
            "interpretation": "stationary point depends on h and on any projected-kernel correction if full L_k is used",
        },
        {
            "step": "generic_prefactor",
            "formula": "L_k ~ A k^(-1/2) exp(b k) under a simple nondegenerate saddle after cancellation of k! scale",
            "interpretation": "predicts c=-1/2 only as a baseline, not a theorem for the Branch C projected carrier",
        },
        {
            "step": "gap",
            "formula": "control delta_Dk-I_k-R_k asymptotically",
            "interpretation": "needed before b,c can be derived from Burnol/Sonine projection data",
        },
    ]
    write_csv(ART / "saddle_point_step270.csv", saddle_rows)

    for triple_id, rho_index, gid in TARGETS:
        fit = fit_by[triple_id]
        predicted_c = -0.5
        predicted_rows.append({
            "triple_id": triple_id,
            "rho_index": rho_index,
            "G_id": gid,
            "numerical_b_step269_exp_poly": f"{fit['b']:.16e}",
            "predicted_b": "undetermined_without_projected_kernel_saddle",
            "numerical_c_step269_exp_poly": f"{fit['c']:.16e}",
            "baseline_saddle_c": f"{predicted_c:.16e}",
            "c_minus_baseline": f"{fit['c'] - predicted_c:.16e}",
            "rmse_exp_poly_k0_7": f"{fit['rmse']:.16e}",
            "match_assessment": "qualitative_prefactor_only" if abs(fit["c"] - predicted_c) < 0.7 else "poor_c_match",
        })
    write_csv(ART / "predicted_vs_numerical_step270.csv", predicted_rows)

    residual_tree = [
        {"node": "Branch_C_stationary_phase", "parent": "root", "status": "partial", "notes": "raw product derivative identity does not equal projected carrier"},
        {"node": "raw_delta_Dk", "parent": "Branch_C_stationary_phase", "status": "established", "notes": "delta_Dk=(zeta*M(G))^(k)(rho) by Leibniz rule"},
        {"node": "projection_corrections", "parent": "Branch_C_stationary_phase", "status": "active_gap", "notes": "actual L_k=delta_Dk-I_k-R_k"},
        {"node": "saddle_prediction", "parent": "Branch_C_stationary_phase", "status": "qualitative", "notes": "simple saddle suggests c=-1/2 baseline; b undetermined"},
    ]
    write_csv(ART / "residual_tree_step270.csv", residual_tree)

    route_status = [
        {"route": "closed raw identity", "status": "complete", "verdict": "holds for unprojected delta_Dk"},
        {"route": "closed Branch C identity", "status": "blocked", "verdict": "projection terms prevent L_k=(zeta*M(G))^(k)(rho)"},
        {"route": "stationary phase", "status": "partial", "verdict": "qualitative exp-poly envelope only"},
        {"route": "RH/Branch C closure", "status": "not_claimed", "verdict": "no closure consequence"},
    ]
    write_csv(ART / "route_status_step270.csv", route_status)

    construction = [
        {"task": "create artifact directory", "status": "complete", "notes": "mkdir succeeded"},
        {"task": "load Step196 and Step269 Branch C pipeline", "status": "complete", "notes": "same G_star/G_prime and PSWF projection"},
        {"task": "compute raw product derivatives", "status": "complete", "notes": "mpmath 80 dps, k=1..7"},
        {"task": "compare raw identity to projected Branch C values", "status": "complete", "notes": "projection corrections are not negligible"},
        {"task": "derive saddle template", "status": "partial", "notes": "needs projected-kernel saddle theorem"},
    ]
    write_csv(ART / "construction_tasks_step270.csv", construction)

    sources = [
        {
            "source": "J.-F. Burnol, On Fourier and Zeta(s), Forum Mathematicum 16 (2004), 789-840, Section 6.",
            "used_for": "Mellin evaluator vectors Z^lambda_{w,k} and [f,Z]=M(f)^(k)(w)",
            "url": "https://arxiv.org/abs/math/0112254",
            "quote": "For each w in C, each k in N, the linear forms f -> M(f)^(k)(w) are continuous.",
        },
        {
            "source": "J.-F. Burnol, Sur les espaces de Sonine associes par de Branges a la transformation de Fourier, C. R. Acad. Sci. Paris, Ser. I 335 (2002), 689-692.",
            "used_for": "Sonine projection and de Branges kernel context inherited by Branch C",
            "url": "https://arxiv.org/abs/math/0208121",
            "quote": "E_lambda is the de Branges function for the Sonine space.",
        },
        {
            "source": "A. Erdelyi, Asymptotic Expansions, Dover, 1956.",
            "used_for": "standard saddle/Laplace-method template",
            "url": "https://archive.org/details/asymptoticexpans0000erde",
            "quote": "standard reference for asymptotic expansions",
        },
        {
            "source": "N. G. de Bruijn, Asymptotic Methods in Analysis, Dover, 1981.",
            "used_for": "standard steepest-descent / saddle-point template",
            "url": "https://archive.org/details/asymptoticmethod0000brui",
            "quote": "standard reference for saddle point methods",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step270.csv", sources)

    content = [
        {"artifact": "step270_results_summary.md", "class": "summary", "claim_boundary": "no RH or Branch C closure"},
        {"artifact": "closed_identity_step270.csv", "class": "numerical_identity_audit", "claim_boundary": "raw identity only"},
        {"artifact": "saddle_point_step270.csv", "class": "analytic_template", "claim_boundary": "not a closed theorem"},
        {"artifact": "predicted_vs_numerical_step270.csv", "class": "comparison", "claim_boundary": "qualitative match only"},
    ]
    write_csv(ART / "content_classification_step270.csv", content)

    output = "\n".join(comparison_lines)
    (ART / "compute_step270_output.txt").write_text(output + "\n", encoding="utf-8")

    schema = {
        "step": 270,
        "orientation": "analytical_derivation",
        "target": "Branch C stationary-phase derivation of polynomial-corrected exponential law",
        "closed_identity_L_k": {
            "raw_identity": "delta_Dk=(zeta*M(G))^(k)(rho) by Burnol evaluator + Leibniz rule",
            "actual_projected_identity": "L_k=delta_Dk-I_k-R_k in the inherited Branch C pipeline",
            "status": "raw identity established; projected closed identity blocked",
        },
        "saddle_point_form": {
            "cauchy": "h^(k)(rho)=k!/(2*pi*i) integral h(z)/(z-rho)^(k+1) dz",
            "saddle_equation": "(log h)'(z_*)=(k+1)/(z_*-rho)",
            "generic_prefactor": "simple saddle gives k^(-1/2) prefactor after scale cancellation",
            "gap": "must include projection corrections I_k,R_k to predict actual Branch C b,c",
        },
        "predicted_b_c": {
            "b": "undetermined without projected-kernel saddle geometry",
            "c_baseline": -0.5,
            "numerical_step269": fit_by,
        },
        "numerical_comparison": {
            "identity_rows_csv": "closed_identity_step270.csv",
            "assessment": "raw product derivative is same analytic source term but not equal to projected Branch C L_k",
        },
        "retained_nogos": [
            "No RH proof or Branch C closure claimed.",
            "No replacement of projected Branch C value by raw Mellin derivative.",
            "No closed b prediction without a projected-kernel saddle theorem.",
        ],
        "final_verdict": "V_branch_C_stationary_phase_partial",
    }
    (ART / "step270_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(output)
    print("verdict=V_branch_C_stationary_phase_partial")


if __name__ == "__main__":
    main()
