#!/usr/bin/env python3
"""Mode C Stage III OL-minimizing transfer fits."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, median, pstdev

import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step353_mode_C_stage_III_OL_minimizing_transfer_artifacts"
STEP352 = ROOT / "anti_loc/thread/steps/step352_mode_C_stage_II_at_scale_artifacts/reproduction_table_step352.csv"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
RHOS = ["rho_1", "rho_2", "rho_3"]
KS = list(range(1, 11))


def load_data():
    h: dict[tuple[str, int], float] = {}
    z: dict[tuple[str, int], float] = {}
    with STEP352.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["cell_type"] == "hecke_reproduction":
                h[(row["character"], int(row["k"]))] = float(row["H_value"])
            elif row["cell_type"] == "zeta_descent_attempt":
                z[(row["rho_target"], int(row["k"]))] = float(row["Z_value"])
    return h, z


def residual_stats(residuals: list[float]) -> dict[str, float]:
    return {
        "cell_count": len(residuals),
        "mean_lambda": mean(residuals),
        "median_lambda": median(residuals),
        "max_lambda": max(residuals),
        "min_lambda": min(residuals),
        "rmse_lambda": math.sqrt(mean([r * r for r in residuals])),
        "std_lambda": pstdev(residuals),
    }


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    h, z = load_data()

    scalar_rows = []
    affine_rows = []
    cv_rows = []
    scalar_params = {}
    affine_params = {}

    # Candidate (a): log(c_j) is mean log(Z/H) for each target.
    for rho in RHOS:
        diffs = []
        for ch in CHARS:
            for k in KS:
                diffs.append(math.log(z[(rho, k)]) - math.log(h[(ch, k)]))
        log_c = mean(diffs)
        c = math.exp(log_c)
        residuals = [abs(log_c + math.log(h[(ch, k)]) - math.log(z[(rho, k)])) for ch in CHARS for k in KS]
        stats = residual_stats(residuals)
        scalar_rows.append({"rho_target": rho, "log_c": log_c, "c": c, **stats})
        scalar_params[rho] = log_c

    # Candidate (b): y = alpha_j + beta_j log H.
    for rho in RHOS:
        xs, ys = [], []
        for ch in CHARS:
            for k in KS:
                xs.append(math.log(h[(ch, k)]))
                ys.append(math.log(z[(rho, k)]))
        X = np.column_stack([np.ones(len(xs)), np.array(xs)])
        y = np.array(ys)
        alpha, beta = np.linalg.lstsq(X, y, rcond=None)[0]
        pred = X @ np.array([alpha, beta])
        residuals = [abs(a - b) for a, b in zip(pred, y)]
        stats = residual_stats(residuals)
        affine_rows.append({"rho_target": rho, "alpha": alpha, "beta": beta, **stats})
        affine_params[rho] = (alpha, beta)

    # Candidate (d): weighted geometric mean across characters at each k.
    # In-sample per target: log Z_j,k = sum_ch w_j,ch log H_ch,k.
    w_rows = []
    X = np.array([[math.log(h[(ch, k)]) for ch in CHARS] for k in KS])
    for rho in RHOS:
        y = np.array([math.log(z[(rho, k)]) for k in KS])
        w = np.linalg.lstsq(X, y, rcond=None)[0]
        pred_by_k = X @ w
        # Expand residuals over 7 character-indexed cells per k to match the OL table shape.
        residuals = [abs(pred_by_k[i] - y[i]) for i in range(len(KS)) for _ in CHARS]
        stats = residual_stats(residuals)
        row = {"fit_scope": f"in_sample_{rho}", "rho_target": rho}
        row.update({f"w_{ch}": w[idx] for idx, ch in enumerate(CHARS)})
        row.update(stats)
        w_rows.append(row)

    # Cross-validation: train on rho_1 only, then apply to rho_2/rho_3.
    log_c_train = scalar_params["rho_1"]
    alpha_train, beta_train = affine_params["rho_1"]
    for rho in RHOS:
        scalar_residuals = [
            abs(log_c_train + math.log(h[(ch, k)]) - math.log(z[(rho, k)]))
            for ch in CHARS
            for k in KS
        ]
        cv_rows.append({"candidate": "scalar_train_rho1", "train_target": "rho_1", "test_target": rho, **residual_stats(scalar_residuals)})

        affine_residuals = [
            abs(alpha_train + beta_train * math.log(h[(ch, k)]) - math.log(z[(rho, k)]))
            for ch in CHARS
            for k in KS
        ]
        cv_rows.append({"candidate": "affine_log_train_rho1", "train_target": "rho_1", "test_target": rho, **residual_stats(affine_residuals)})

    # Candidate d cross-validation with geometric weights trained on rho_1.
    y_train = np.array([math.log(z[("rho_1", k)]) for k in KS])
    w_train = np.linalg.lstsq(X, y_train, rcond=None)[0]
    for rho in ["rho_1", "rho_2", "rho_3"]:
        y = np.array([math.log(z[(rho, k)]) for k in KS])
        pred = X @ w_train
        residuals = [abs(pred[i] - y[i]) for i in range(len(KS)) for _ in CHARS]
        stats = residual_stats(residuals)
        cv_rows.append({"candidate": "weighted_geometric_train_rho1", "train_target": "rho_1", "test_target": rho, **stats})

    write_rows(BASE / "scalar_normalizer_fit_step353.csv", scalar_rows, list(scalar_rows[0].keys()))
    write_rows(BASE / "affine_log_fit_step353.csv", affine_rows, list(affine_rows[0].keys()))
    write_rows(BASE / "weighted_geometric_mean_fit_step353.csv", w_rows, list(w_rows[0].keys()))
    write_rows(BASE / "cross_validation_transfer_step353.csv", cv_rows, list(cv_rows[0].keys()))

    print("scalar best rmse", min(row["rmse_lambda"] for row in scalar_rows))
    print("affine best rmse", min(row["rmse_lambda"] for row in affine_rows))
    print("weighted in-sample best rmse", min(row["rmse_lambda"] for row in w_rows))
    print(
        "weighted rho2 holdout rmse",
        [
            row
            for row in cv_rows
            if row["candidate"] == "weighted_geometric_train_rho1" and row["test_target"] == "rho_2"
        ][0]["rmse_lambda"],
    )
    print(
        "weighted rho3 holdout rmse",
        [
            row
            for row in cv_rows
            if row["candidate"] == "weighted_geometric_train_rho1" and row["test_target"] == "rho_3"
        ][0]["rmse_lambda"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
