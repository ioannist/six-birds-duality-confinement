#!/usr/bin/env python3
"""Step 341: rho-parametric multiplicative H6 bridge fit."""

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
ART = ROOT / "anti_loc/thread/steps/step341_H6_rho_parametric_bridge_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"

DPS = 80
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
MAX_K = 20
TRAIN_K = list(range(1, 11))
CV_K = [1, 5, 10, 15, 20]


def load_step338_module():
    spec = importlib.util.spec_from_file_location("step338_compute", STEP338_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Step 338 compute module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def feature_vector(T: mp.mpf, log_he: dict[str, mp.mpf], include_logT: bool = True) -> list[mp.mpf]:
    row = [mp.mpf("1"), T]
    if include_logT:
        row.append(mp.log(T))
    for ch in CHARS:
        row.append(log_he[ch])
        row.append(T * log_he[ch])
    return row


def param_names(include_logT: bool = True) -> list[str]:
    names = ["c0", "c1"]
    if include_logT:
        names.append("c2_logT")
    for ch in CHARS:
        names.extend([f"a0_{ch}", f"a1_{ch}"])
    return names


def solve_ls(A: list[list[mp.mpf]], y: list[mp.mpf]) -> tuple[mp.matrix, int, float]:
    """Minimum-norm least squares using SVD.

    The requested model has 17 columns but only two rho-values; several
    columns are nearly dependent.  SVD least-squares is therefore the right
    numerical object to record instead of unstable normal equations.
    """
    arr = np.array([[float(v) for v in row] for row in A], dtype=float)
    yy = np.array([float(v) for v in y], dtype=float)
    sol, _, rank, singular = np.linalg.lstsq(arr, yy, rcond=None)
    cond = float(singular[0] / singular[-1]) if len(singular) and singular[-1] != 0 else float("inf")
    return mp.matrix([mp.mpf(str(v)) for v in sol]), int(rank), cond


def predict_log(coeff: mp.matrix, row: list[mp.mpf]) -> mp.mpf:
    return mp.fsum([coeff[i] * row[i] for i in range(len(row))])


def residual(actual_abs: mp.mpf, pred_log: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    pred_abs = mp.e ** pred_log
    log_error = pred_log - mp.log(actual_abs)
    rel = abs(pred_abs - actual_abs) / actual_abs
    return pred_abs, log_error, rel


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    mod = load_step338_module()

    # Fixed Hecke inputs through k=20.
    roots = mod.roots()
    hecke: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    for ch in CHARS:
        q, chi = mod.char_values(ch)
        rho = roots[ch]
        Lds = mod.dirichlet_L_derivatives(rho, q, chi, MAX_K)
        Mds = mod.M_derivatives(rho, MAX_K)
        for k in range(1, MAX_K + 1):
            hecke[ch][k] = abs(mod.h_derivative(Lds, Mds, k))

    # Branch C targets at rho_1, rho_2, rho_3.
    rho_targets = {
        "rho_1": mp.zetazero(1),
        "rho_2": mp.zetazero(2),
        "rho_3": mp.zetazero(3),
    }
    targets: dict[str, dict[int, mp.mpf]] = {}
    Tvals: dict[str, mp.mpf] = {}
    for label, rho in rho_targets.items():
        Tvals[label] = mp.im(rho)
        zds = mod.zeta_derivatives(rho, MAX_K)
        mds = mod.M_derivatives(rho, MAX_K)
        targets[label] = {k: abs(mod.h_derivative(zds, mds, k)) for k in range(1, MAX_K + 1)}

    # Fit on rho_1 and rho_2, k=1..10.
    A: list[list[mp.mpf]] = []
    y: list[mp.mpf] = []
    for rho_label in ["rho_1", "rho_2"]:
        T = Tvals[rho_label]
        for k in TRAIN_K:
            log_he = {ch: mp.log(hecke[ch][k]) for ch in CHARS}
            A.append(feature_vector(T, log_he, include_logT=True))
            y.append(mp.log(targets[rho_label][k]))
    coeff, design_rank, design_condition = solve_ls(A, y)
    names = param_names(include_logT=True)

    param_rows = []
    for name, val in zip(names, list(coeff)):
        param_rows.append({"parameter": name, "value": mp.nstr(val, 18), "model": "with_c2_logT"})
    write_csv(ART / "rho_parametric_fit_step341.csv", param_rows)

    train_rows = []
    max_train = mp.mpf("0")
    for rho_label in ["rho_1", "rho_2"]:
        T = Tvals[rho_label]
        for k in TRAIN_K:
            row = feature_vector(T, {ch: mp.log(hecke[ch][k]) for ch in CHARS}, include_logT=True)
            pred_abs, log_error, rel = residual(targets[rho_label][k], predict_log(coeff, row))
            max_train = max(max_train, rel)
            train_rows.append({
                "rho_label": rho_label,
                "T": mp.nstr(T, 18),
                "k": k,
                "actual_abs": mp.nstr(targets[rho_label][k], 18),
                "predicted_abs": mp.nstr(pred_abs, 18),
                "log_error": mp.nstr(log_error, 12),
                "relative_residual": mp.nstr(rel, 12),
                "verdict": "pass_under_5pct" if rel < mp.mpf("0.05") else "fail_under_5pct",
            })
    write_csv(ART / "training_residuals_step341.csv", train_rows)

    cv_rows = []
    max_cv = mp.mpf("0")
    T3 = Tvals["rho_3"]
    for k in CV_K:
        row = feature_vector(T3, {ch: mp.log(hecke[ch][k]) for ch in CHARS}, include_logT=True)
        pred_abs, log_error, rel = residual(targets["rho_3"][k], predict_log(coeff, row))
        max_cv = max(max_cv, rel)
        cv_rows.append({
            "rho_label": "rho_3",
            "T": mp.nstr(T3, 18),
            "k": k,
            "actual_abs": mp.nstr(targets["rho_3"][k], 18),
            "predicted_abs": mp.nstr(pred_abs, 18),
            "log_error": mp.nstr(log_error, 12),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_5pct" if rel < mp.mpf("0.05") else "fail_under_5pct",
        })
    write_csv(ART / "cross_validation_rho_3_step341.csv", cv_rows)

    if max_cv < mp.mpf("0.05"):
        verdict = "V_H6_rho_parametric_bridge_cross_rho3_passes"
        bridge_candidate = True
    else:
        verdict = "V_H6_rho_parametric_bridge_cross_rho3_fails"
        bridge_candidate = False

    summary = [
        "# Step 341 Results Summary",
        "",
        "Constructive rho-parametric multiplicative H6 bridge test:",
        "`log|L_k(rho,G_star)| = c0 + c1 T + c2 log T + sum_chi (a0_chi+a1_chi T) log|L_k^chi|`.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.",
        "- Step 339: product bridge passed rho_1 holdout through k=20.",
        "- Step 340: fixed Step 339 coefficients failed rho_2 with max residual `0.935983109276`; even rho_2-specific intercept failed with max residual `3.08309698613`.",
        "",
        "rho_3 actual values k=1..20:",
    ]
    for k in range(1, MAX_K + 1):
        summary.append(f"- k={k}: `{mp.nstr(targets['rho_3'][k], 18)}`")
    summary += [
        "",
        f"Design rank from SVD least squares: `{design_rank}` of `{len(names)}` columns; condition estimate `{design_condition:.6e}`.",
        f"Training max residual over rho_1/rho_2, k=1..10: `{mp.nstr(max_train, 12)}`.",
        f"rho_3 holdout max residual over k=1,5,10,15,20: `{mp.nstr(max_cv, 12)}`.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step341_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 341,
        "orientation": "constructive_cross_validation",
        "target": "rho-parametric multiplicative H6 bridge",
        "dps": DPS,
        "training_rhos": ["rho_1", "rho_2"],
        "holdout_rho": "rho_3",
        "training_k": TRAIN_K,
        "holdout_k": CV_K,
        "parameter_count": len(names),
        "training_point_count": len(A),
        "design_rank": design_rank,
        "design_condition_estimate": design_condition,
        "max_training_relative_residual": mp.nstr(max_train, 18),
        "max_rho3_holdout_relative_residual": mp.nstr(max_cv, 18),
        "bridge_candidate": bridge_candidate,
        "final_verdict": verdict,
    }
    (ART / "step341_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 341 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- A rho-parametric regression is not a proof of a Hecke-to-Burnol zeta-fiber descent theorem.",
        "- Passing or failing rho_3 cross-validation only tests this explicit finite ansatz.",
        "- The theorem-grade H6 object would still need carrier/projection/kernel-preserving derivation.",
    ]
    (ART / "nonclaim_boundary_step341.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_train_rel={mp.nstr(max_train, 12)}")
    print(f"max_cv_rel={mp.nstr(max_cv, 12)}")
    print(f"design_rank={design_rank}")
    print(f"design_condition_estimate={design_condition:.6e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
