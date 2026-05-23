#!/usr/bin/env python3
"""Fit growth laws for Branch C |L|_k data."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts")


def load_rows():
    with (BASE / "k_dataset_step250.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def rmse(y, pred):
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def maxabs(y, pred):
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.max(np.abs(y - pred)))


def main() -> None:
    rows = load_rows()
    triples = sorted(set(r["triple_id"] for r in rows))
    fit_rows = []
    extra_rows = []
    model_defs = {
        "linear": (lambda k, a, b: a + b * k, (0.1, 0.2), 2),
        "quadratic": (lambda k, a, b, c: a + b * k + c * k * k, (0.1, 0.2, 0.05), 3),
        "exponential": (lambda k, a, b: a * np.exp(b * k), (0.1, 0.5), 2),
        "factorial": (lambda k, a: a * np.array([math.factorial(int(x)) for x in k], dtype=float), (0.1,), 1),
        "affine_factorial": (lambda k, a, b: a + b * np.array([math.factorial(int(x)) for x in k], dtype=float), (0.1, 0.01), 2),
        "pochhammer_1k": (lambda k, a: a * np.array([math.gamma(1 + int(x)) for x in k], dtype=float), (0.1,), 1),
    }
    extrap = []
    for triple in triples:
        sub = [r for r in rows if r["triple_id"] == triple]
        k = np.array([int(r["k"]) for r in sub], dtype=float)
        y = np.array([float(r["L_abs"]) for r in sub], dtype=float)
        best = None
        best_pred = None
        best_func = None
        best_popt = None
        for name, (func, p0, npar) in model_defs.items():
            try:
                popt, _ = curve_fit(func, k, y, p0=p0, maxfev=50000)
                pred = func(k, *popt)
                rec = {
                    "triple_id": triple,
                    "model": name,
                    "parameters": ";".join(f"{p:.12g}" for p in np.atleast_1d(popt)),
                    "rmse": f"{rmse(y, pred):.16e}",
                    "max_abs_residual": f"{maxabs(y, pred):.16e}",
                    "n_parameters": str(npar),
                    "status": "fit_ok",
                }
            except Exception as exc:
                rec = {
                    "triple_id": triple,
                    "model": name,
                    "parameters": "fit_failed",
                    "rmse": "nan",
                    "max_abs_residual": "nan",
                    "n_parameters": str(npar),
                    "status": str(exc),
                }
                fit_rows.append(rec)
                continue
            fit_rows.append(rec)
            score = float(rec["rmse"])
            if best is None or score < float(best["rmse"]):
                best, best_pred, best_func, best_popt = rec, pred, func, popt
        for kk in [5, 10]:
            val = float(best_func(np.array([kk], dtype=float), *best_popt)[0])
            extrap.append({
                "triple_id": triple,
                "best_model": best["model"],
                "k": str(kk),
                "predicted_abs_L": f"{val:.16e}",
                "note": "model extrapolation from k=0..4; not theorem-grade",
            })
        extra_rows.append({
            "triple_id": triple,
            "best_model": best["model"],
            "best_rmse": best["rmse"],
            "comment": "best raw RMSE over tested models",
        })

    # Global normalized fit: divide each triple by its k=0 value.
    norm_rows = []
    for triple in triples:
        sub = [r for r in rows if r["triple_id"] == triple]
        base = float([r for r in sub if r["k"] == "0"][0]["L_abs"])
        for r in sub:
            norm_rows.append((triple, int(r["k"]), float(r["L_abs"]) / base))
    k_all = np.array([x[1] for x in norm_rows], dtype=float)
    y_all = np.array([x[2] for x in norm_rows], dtype=float)
    for name, (func, p0, npar) in model_defs.items():
        popt, _ = curve_fit(func, k_all, y_all, p0=p0, maxfev=50000)
        pred = func(k_all, *popt)
        fit_rows.append({
            "triple_id": "GLOBAL_NORMALIZED_BY_K0",
            "model": name,
            "parameters": ";".join(f"{p:.12g}" for p in np.atleast_1d(popt)),
            "rmse": f"{rmse(y_all, pred):.16e}",
            "max_abs_residual": f"{maxabs(y_all, pred):.16e}",
            "n_parameters": str(npar),
            "status": "fit_ok",
        })

    with (BASE / "growth_law_fits_step250.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fit_rows[0].keys()))
        writer.writeheader()
        writer.writerows(fit_rows)
    with (BASE / "extrapolation_step250.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(extrap[0].keys()))
        writer.writeheader()
        writer.writerows(extrap)
    with (BASE / "best_fit_summary_step250.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(extra_rows[0].keys()))
        writer.writeheader()
        writer.writerows(extra_rows)
    verdict = "V_branch_C_k_growth_law_polynomial" if all(r["best_model"] == "quadratic" for r in extra_rows) else "V_branch_C_k_growth_law_other"
    (BASE / "fit_growth_law_output_step250.txt").write_text(
        "best_fits\\n" + "\\n".join(str(r) for r in extra_rows) + f"\\nverdict={verdict}\\n"
    )
    print((BASE / "fit_growth_law_output_step250.txt").read_text())


if __name__ == "__main__":
    main()
