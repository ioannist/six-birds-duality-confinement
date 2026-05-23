#!/usr/bin/env python3
"""Step 286 Branch C k=10,15,20 attempt.

The full Step 269 projected-value pipeline at mpmath dps=120 was attempted
but did not complete in a practical time.  This script records the inherited
k=0..7 data and a clearly marked k=10,15,20 model-probe extrapolation from
the k=0..7 polynomial-corrected exponential fit.  The step verdict is
therefore partial, not a certified high-k computation.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step286_branch_C_k20_extension_artifacts")
STEP269_DATA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/extended_dataset_step269.csv")
MP_DPS_ATTEMPTED = 120
HIGH_K = [10, 15, 20]
TRIPLES = ["rho1_G_star", "rho2_G_star", "rho1_G_prime"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def model(k, a, b, c):
    return a * ((k + 1.0) ** c) * np.exp(b * k)


def fit_old(rows: list[dict[str, object]], triple: str):
    sub = sorted([r for r in rows if r["triple_id"] == triple and int(r["k"]) <= 7], key=lambda r: int(r["k"]))
    k = np.array([int(r["k"]) for r in sub], dtype=float)
    y = np.array([float(r["L_abs"]) for r in sub], dtype=float)
    popt, pcov = curve_fit(model, k, y, p0=(max(1e-9, y[0]), 0.7, -0.3), maxfev=100000)
    pred = model(k, *popt)
    rmse = float(np.sqrt(np.mean((y - pred) ** 2)))
    return popt, pcov, rmse


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    inherited = [dict(r) for r in read_csv(STEP269_DATA)]
    rows: list[dict[str, object]] = []
    rows.extend(inherited)

    fit_rows = []
    high_resid_rows = []
    saddle_rows = []
    output = [
        "Step 286 Branch C k=10,15,20 extension",
        f"full_projected_pipeline_attempted_mpmath_dps={MP_DPS_ATTEMPTED}",
        "status=partial_projection_timeout",
        "high_k_values=model_probe_from_step269_k0_7_fit_not_certified",
    ]

    for triple in TRIPLES:
        popt, pcov, old_rmse = fit_old(rows, triple)
        se = np.sqrt(np.diag(pcov))
        fit_rows.append({
            "triple_id": triple,
            "model": "a*(k+1)^c*exp(b*k)",
            "a": f"{popt[0]:.16e}",
            "b": f"{popt[1]:.16e}",
            "c": f"{popt[2]:.16e}",
            "a_stderr": f"{se[0]:.16e}",
            "b_stderr": f"{se[1]:.16e}",
            "c_stderr": f"{se[2]:.16e}",
            "rmse_k0_7": f"{old_rmse:.16e}",
            "rmse_k0_20": "not_computed_certified_high_k_missing",
            "fit_status": "k0_7_fit_only",
        })
        sample = next(r for r in rows if r["triple_id"] == triple)
        for k in HIGH_K:
            pred = float(model(np.array([k], dtype=float), *popt)[0])
            rows.append({
                "triple_id": triple,
                "rho_index": sample["rho_index"],
                "G_id": sample["G_id"],
                "k": str(k),
                "L_abs": f"{pred:.16e}",
                "error_bound": "nan",
                "lower_bound": "nan",
                "method": "model_probe_step286_full_projection_timeout_not_certified",
            })
            high_resid_rows.append({
                "triple_id": triple,
                "k": str(k),
                "model_probe_abs_L": f"{pred:.16e}",
                "step269_k0_7_fit_pred": f"{pred:.16e}",
                "certified_observed_abs_L": "not_available",
                "relative_residual": "not_available",
                "diagnostic": "projection_timeout",
            })
            output.append(f"triple={triple} k={k} model_probe_abs={pred:.12e} certified=false")
        saddle_rows.append({
            "triple_id": triple,
            "rho_index": sample["rho_index"],
            "G_id": sample["G_id"],
            "k": "20",
            "delta_Dk_abs": "not_computed",
            "L_abs": "not_computed",
            "L_over_delta_abs": "not_computed",
            "saddle_note": "full high-derivative/projection computation timed out; saddle check deferred",
        })

    rows = sorted(rows, key=lambda r: (str(r["triple_id"]), int(r["k"])))
    write_csv(ART / "extended_dataset_step286.csv", rows)
    write_csv(ART / "exponential_fit_extended_step286.csv", fit_rows)
    write_csv(ART / "residual_high_k_step286.csv", high_resid_rows)
    write_csv(ART / "saddle_check_step286.csv", saddle_rows)

    residual_tree = [
        {"node": "Branch_C_k20_extension", "parent": "root", "status": "partial", "notes": "full projection attempt timed out"},
        {"node": "k0_7_model_probe", "parent": "Branch_C_k20_extension", "status": "complete", "notes": "extrapolative k=10,15,20 table produced"},
        {"node": "certified_high_k_values", "parent": "Branch_C_k20_extension", "status": "missing", "notes": "requires optimized derivative/projection implementation"},
        {"node": "foreclosure_theorem", "parent": "Branch_C_k20_extension", "status": "missing", "notes": "no RH closure claimed"},
    ]
    write_csv(ART / "residual_tree_step286.csv", residual_tree)

    route = [
        {"route": "full_projected_pipeline", "status": "attempted_timeout", "verdict": "mpmath dps 120 attempt did not complete"},
        {"route": "model_probe", "status": "complete", "verdict": "k0..7 exp-poly extrapolation produced"},
        {"route": "extended_fit", "status": "partial", "verdict": "certified k0..20 fit unavailable"},
        {"route": "saddle_check", "status": "deferred", "verdict": "delta_Dk k=20 not computed"},
        {"route": "final", "status": "complete", "verdict": "V_branch_C_k20_partial"},
    ]
    write_csv(ART / "route_status_step286.csv", route)

    construction = [
        {"task": "mkdir", "status": "complete", "notes": "artifact directory created"},
        {"task": "attempt_full_projection", "status": "attempted_timeout", "notes": "Step269 pipeline at dps 120 did not finish in practical time"},
        {"task": "load_k0_7", "status": "complete", "notes": "Step269 dataset reused"},
        {"task": "model_probe_k10_15_20", "status": "complete", "notes": "not certified numerical L-values"},
        {"task": "run_validator", "status": "pending", "notes": "run after docs"},
    ]
    write_csv(ART / "construction_tasks_step286.csv", construction)

    sources = [
        {
            "source": "J.-F. Burnol, On Fourier and Zeta(s), Forum Mathematicum 16 (2004), 789-840.",
            "used_for": "Mellin evaluator vectors Z^lambda_{w,k}; [f,Z]=M(f)^(k)(w)",
            "url": "https://arxiv.org/abs/math/0112254",
        },
        {
            "source": "Step 269 Branch C k-extension artifacts.",
            "used_for": "baseline k=0..7 data and polynomial-corrected exponential fit",
            "url": "anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/",
        },
        {
            "source": "Step 270/271 Branch C stationary-phase artifacts.",
            "used_for": "closed identity and saddle-point context",
            "url": "anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts/",
        },
    ]
    write_csv(ART / "classical_theorems_cited_step286.csv", sources)

    summary = {
        "verdict": "V_branch_C_k20_partial",
        "mpmath_dps_attempted": MP_DPS_ATTEMPTED,
        "high_k": HIGH_K,
        "fit_rows": fit_rows,
        "certification": "not certified; full projected computation timed out",
    }
    (ART / "compute_step286_output.txt").write_text("\n".join(output) + "\nverdict=V_branch_C_k20_partial\n", encoding="utf-8")
    (ART / "compute_step286_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n".join(output))
    print("verdict=V_branch_C_k20_partial")


if __name__ == "__main__":
    main()
