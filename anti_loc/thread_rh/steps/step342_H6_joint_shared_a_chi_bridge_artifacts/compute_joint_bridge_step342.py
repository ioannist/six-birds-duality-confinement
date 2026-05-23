#!/usr/bin/env python3
"""Step 342: jointly constrained multiplicative bridge with shared a(chi)."""

from __future__ import annotations

import csv
import importlib.util
import json
import time
from pathlib import Path

import mpmath as mp
import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step342_H6_joint_shared_a_chi_bridge_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"

DPS = 80
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
RHO_LABELS = ["rho_1", "rho_2", "rho_3"]
TRAIN_K = list(range(1, 11))
MAX_K = 20


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


def design_row(rho_label: str, log_he: dict[str, mp.mpf]) -> list[mp.mpf]:
    row = [mp.mpf("1") if rho_label == lab else mp.mpf("0") for lab in RHO_LABELS]
    row.extend([log_he[ch] for ch in CHARS])
    return row


def param_names() -> list[str]:
    return [f"b0_{r}" for r in RHO_LABELS] + [f"a_{ch}" for ch in CHARS]


def solve_lstsq(A: list[list[mp.mpf]], y: list[mp.mpf]) -> tuple[mp.matrix, int, float]:
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

    # Hecke inputs through k=20.
    roots = mod.roots()
    hecke: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    for ch in CHARS:
        q, chi = mod.char_values(ch)
        rho = roots[ch]
        Lds = mod.dirichlet_L_derivatives(rho, q, chi, MAX_K)
        Mds = mod.M_derivatives(rho, MAX_K)
        for k in range(1, MAX_K + 1):
            hecke[ch][k] = abs(mod.h_derivative(Lds, Mds, k))

    # Branch C targets rho_1..rho_4.
    rho_map = {f"rho_{i}": mp.zetazero(i) for i in range(1, 5)}
    targets: dict[str, dict[int, mp.mpf]] = {}
    for label, rho in rho_map.items():
        zds = mod.zeta_derivatives(rho, MAX_K)
        mds = mod.M_derivatives(rho, MAX_K)
        targets[label] = {k: abs(mod.h_derivative(zds, mds, k)) for k in range(1, MAX_K + 1)}

    A: list[list[mp.mpf]] = []
    y: list[mp.mpf] = []
    for rho_label in RHO_LABELS:
        for k in TRAIN_K:
            A.append(design_row(rho_label, {ch: mp.log(hecke[ch][k]) for ch in CHARS}))
            y.append(mp.log(targets[rho_label][k]))

    coeff, rank, cond = solve_lstsq(A, y)
    names = param_names()

    rows: list[dict[str, object]] = []
    for name, val in zip(names, list(coeff)):
        rows.append({
            "row_type": "parameter",
            "rho_label": "",
            "k": "",
            "parameter": name,
            "value": mp.nstr(val, 18),
            "actual_abs": "",
            "predicted_abs": "",
            "log_error": "",
            "relative_residual": "",
            "verdict": "joint_least_squares_parameter",
        })

    max_by_rho = {rho: mp.mpf("0") for rho in RHO_LABELS}
    sum_by_rho = {rho: mp.mpf("0") for rho in RHO_LABELS}
    max_all = mp.mpf("0")
    for rho_label in RHO_LABELS:
        for k in TRAIN_K:
            row = design_row(rho_label, {ch: mp.log(hecke[ch][k]) for ch in CHARS})
            pred_abs, log_error, rel = residual(targets[rho_label][k], predict_log(coeff, row))
            max_all = max(max_all, rel)
            max_by_rho[rho_label] = max(max_by_rho[rho_label], rel)
            sum_by_rho[rho_label] += rel
            rows.append({
                "row_type": "training_residual",
                "rho_label": rho_label,
                "k": k,
                "parameter": "",
                "value": "",
                "actual_abs": mp.nstr(targets[rho_label][k], 18),
                "predicted_abs": mp.nstr(pred_abs, 18),
                "log_error": mp.nstr(log_error, 12),
                "relative_residual": mp.nstr(rel, 12),
                "verdict": "pass_under_5pct" if rel < mp.mpf("0.05") else "fail_under_5pct",
            })
    for rho_label in RHO_LABELS:
        rows.append({
            "row_type": "rho_summary",
            "rho_label": rho_label,
            "k": "1..10",
            "parameter": "",
            "value": "",
            "actual_abs": "",
            "predicted_abs": "",
            "log_error": "",
            "relative_residual": mp.nstr(max_by_rho[rho_label], 12),
            "verdict": f"mean_relative_residual={mp.nstr(sum_by_rho[rho_label] / 10, 12)}",
        })
    write_csv(ART / "joint_fit_step342.csv", rows)

    # rho_4: calibrate a fresh b0 at k=10 using shared a, then predict k=20.
    shared_a = {ch: coeff[3 + i] for i, ch in enumerate(CHARS)}
    sum10 = mp.fsum([shared_a[ch] * mp.log(hecke[ch][10]) for ch in CHARS])
    b0_rho4 = mp.log(targets["rho_4"][10]) - sum10
    cv_rows = [{
        "row_type": "rho4_intercept",
        "k": "calibrated_at_10",
        "b0_rho4": mp.nstr(b0_rho4, 18),
        "actual_abs": "",
        "predicted_abs": "",
        "log_error": "",
        "relative_residual": "",
        "verdict": "shared_a_chi_with_rho4_specific_intercept",
    }]
    max_cv = mp.mpf("0")
    for k in [10, 20]:
        pred_log = b0_rho4 + mp.fsum([shared_a[ch] * mp.log(hecke[ch][k]) for ch in CHARS])
        pred_abs, log_error, rel = residual(targets["rho_4"][k], pred_log)
        max_cv = max(max_cv, rel)
        cv_rows.append({
            "row_type": "rho4_prediction",
            "k": k,
            "b0_rho4": mp.nstr(b0_rho4, 18),
            "actual_abs": mp.nstr(targets["rho_4"][k], 18),
            "predicted_abs": mp.nstr(pred_abs, 18),
            "log_error": mp.nstr(log_error, 12),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_5pct" if rel < mp.mpf("0.05") else "fail_under_5pct",
        })
    write_csv(ART / "cross_validation_rho_4_step342.csv", cv_rows)

    if max_all < mp.mpf("0.05") and max_cv < mp.mpf("0.05"):
        verdict = "V_H6_joint_shared_a_chi_bridge_candidate_passes"
        bridge_candidate = True
    elif max_all < mp.mpf("0.05"):
        verdict = "V_H6_joint_shared_a_chi_training_passes_rho4_holdout_fails"
        bridge_candidate = False
    else:
        verdict = "V_H6_joint_shared_a_chi_training_fails"
        bridge_candidate = False

    summary = [
        "# Step 342 Results Summary",
        "",
        "Joint shared-exponent multiplicative H6 fit:",
        "`log|L_k(rho_j,G_star)| = b0(rho_j) + sum_chi a(chi) log|L_k^chi|`.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.",
        "- Step 339: product bridge passed rho_1 holdout with max residual `0.00893202095224`.",
        "- Step 340/341: rho-cross tests showed single-rho coefficients and richer rho-parametric coefficients did not generalize.",
        "",
        f"Design rank: `{rank}` of `10`; condition estimate `{cond:.6e}`.",
        f"Max training residual over 30 cells: `{mp.nstr(max_all, 12)}`.",
    ]
    for rho_label in RHO_LABELS:
        summary.append(
            f"- {rho_label}: max `{mp.nstr(max_by_rho[rho_label], 12)}`, mean `{mp.nstr(sum_by_rho[rho_label] / 10, 12)}`"
        )
    summary += [
        f"rho_4 b0 calibrated at k=10: `{mp.nstr(b0_rho4, 12)}`.",
        f"rho_4 k=20 holdout residual: `{mp.nstr(max_cv, 12)}`.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step342_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 342,
        "orientation": "constructive",
        "target": "joint shared a(chi) multiplicative H6 bridge",
        "dps": DPS,
        "training_rhos": RHO_LABELS,
        "training_k": TRAIN_K,
        "parameter_count": 10,
        "training_point_count": 30,
        "design_rank": rank,
        "design_condition_estimate": cond,
        "max_training_relative_residual": mp.nstr(max_all, 18),
        "rho4_k20_holdout_relative_residual": mp.nstr(max_cv, 18),
        "bridge_candidate": bridge_candidate,
        "final_verdict": verdict,
    }
    (ART / "step342_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 342 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- A joint finite regression is not a proof of an H6 descent theorem.",
        "- A passing rho_4 holdout would be a numerical bridge candidate only.",
        "- The theorem-grade target remains a carrier/projection/kernel-preserving Hecke-to-Burnol zeta-fiber descent.",
    ]
    (ART / "nonclaim_boundary_step342.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_train_rel={mp.nstr(max_all, 12)}")
    print(f"rho4_k20_rel={mp.nstr(max_cv, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
