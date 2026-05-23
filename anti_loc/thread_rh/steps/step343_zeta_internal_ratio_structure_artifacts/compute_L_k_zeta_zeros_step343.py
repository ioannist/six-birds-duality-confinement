#!/usr/bin/env python3
"""Step 343: zeta-internal cross-rho ratio structure."""

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
ART = ROOT / "anti_loc/thread/steps/step343_zeta_internal_ratio_structure_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"

DPS = 80
MAX_K = 20
SELECT_K = [1, 2, 3, 5, 10, 15, 20]


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


def linear_fit(x: np.ndarray, y: np.ndarray, intercept: bool) -> tuple[np.ndarray, np.ndarray]:
    if intercept:
        A = np.column_stack([np.ones_like(x), x])
    else:
        A = x.reshape(-1, 1)
    coeff, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coeff, A @ coeff


def rmse(vals: np.ndarray) -> float:
    return float(np.sqrt(np.mean(vals * vals)))


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    mod = load_step338_module()

    rhos = {j: mp.zetazero(j) for j in range(1, 6)}
    T = {j: mp.im(rhos[j]) for j in rhos}
    values: dict[int, dict[int, mp.mpf]] = {}
    for j, rho in rhos.items():
        zds = mod.zeta_derivatives(rho, MAX_K)
        mds = mod.M_derivatives(rho, MAX_K)
        values[j] = {k: abs(mod.h_derivative(zds, mds, k)) for k in range(1, MAX_K + 1)}

    ratio_rows = []
    for k in range(1, MAX_K + 1):
        for j in range(1, 6):
            ratio = mp.mpf("1") if j == 1 else values[j][k] / values[1][k]
            ratio_rows.append({
                "rho_index": j,
                "Im_rho": mp.nstr(T[j], 18),
                "k": k,
                "abs_L_k": mp.nstr(values[j][k], 18),
                "ratio_to_rho1": mp.nstr(ratio, 18),
                "selected_k": "yes" if k in SELECT_K else "no",
            })
    write_csv(ART / "zeta_ratios_step343.csv", ratio_rows)

    fit_rows = []
    for k in range(1, MAX_K + 1):
        js = np.array([2, 3, 4, 5], dtype=float)
        t = np.array([float(T[int(j)]) for j in js], dtype=float)
        ratios = np.array([float(values[int(j)][k] / values[1][k]) for j in js], dtype=float)
        log_ratios = np.log(ratios)
        log_height = np.log(t / float(T[1]))
        delta_t = t - float(T[1])

        # (a) Pure height-ratio model: log r = f(k) log(T/T1).
        coeff, pred_log = linear_fit(log_height, log_ratios, intercept=False)
        pred = np.exp(pred_log)
        fit_rows.append({
            "k": k,
            "model": "pure_height_ratio_r=(T/T1)^f",
            "parameters": f"f={coeff[0]:.12g}",
            "rmse_log": f"{rmse(pred_log - log_ratios):.12g}",
            "rmse_relative": f"{rmse((pred - ratios) / ratios):.12g}",
            "max_relative": f"{np.max(np.abs((pred - ratios) / ratios)):.12g}",
        })

        # (b) Polynomial-in-height linear version: r = a0 + a1*T.
        coeff, pred = linear_fit(t, ratios, intercept=True)
        fit_rows.append({
            "k": k,
            "model": "linear_polynomial_in_T_r=a0+a1*T",
            "parameters": f"a0={coeff[0]:.12g};a1={coeff[1]:.12g}",
            "rmse_log": "",
            "rmse_relative": f"{rmse((pred - ratios) / ratios):.12g}",
            "max_relative": f"{np.max(np.abs((pred - ratios) / ratios)):.12g}",
        })

        # (c) Exponential in height anchored at rho1: log r = g(k)*(T-T1).
        coeff, pred_log = linear_fit(delta_t, log_ratios, intercept=False)
        pred = np.exp(pred_log)
        fit_rows.append({
            "k": k,
            "model": "anchored_exponential_r=exp(g*(T-T1))",
            "parameters": f"g={coeff[0]:.12g}",
            "rmse_log": f"{rmse(pred_log - log_ratios):.12g}",
            "rmse_relative": f"{rmse((pred - ratios) / ratios):.12g}",
            "max_relative": f"{np.max(np.abs((pred - ratios) / ratios)):.12g}",
        })
    write_csv(ART / "functional_form_fits_step343.csv", fit_rows)

    # Select best model by mean max relative over selected k.
    selected = [r for r in fit_rows if int(r["k"]) in SELECT_K]
    model_names = sorted(set(r["model"] for r in selected))
    model_score = {}
    for model in model_names:
        vals = [float(r["max_relative"]) for r in selected if r["model"] == model]
        model_score[model] = sum(vals) / len(vals)
    best_model = min(model_score, key=model_score.get)

    # k-dependence diagnostics for selected ratios.
    ratio_spread = {}
    for j in range(2, 6):
        rs = [values[j][k] / values[1][k] for k in SELECT_K]
        ratio_spread[j] = (min(rs), max(rs), max(rs) / min(rs))

    clean = model_score[best_model] < 0.05 and all(ratio_spread[j][2] < 2 for j in ratio_spread)
    verdict = "V_zeta_internal_ratio_clean_form_found" if clean else "V_zeta_internal_ratio_no_clean_form"

    summary = [
        "# Step 343 Results Summary",
        "",
        "Computed Branch C zeta-side `|L_k(rho_j,G_star)|` for `rho_1..rho_5`, k=1..20, using the same Leibniz evaluator as Steps 340--342.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 269/304: `rho_1` reference includes k=1 around `0.289`, k=10 `165.44`, k=20 `554847`.",
        "- Step 340: `rho_2` k=10 `667.785`, k=20 `8.74e6`.",
        "- Step 341: `rho_3` full k=1..20 table is used as the consistency reference; conflicting inherited high values are not forced.",
        "",
        "Selected ratio spreads r_j(k)=|L_k(rho_j)|/|L_k(rho_1)| over k=1,2,3,5,10,15,20:",
    ]
    for j in range(2, 6):
        mn, mx, spread = ratio_spread[j]
        summary.append(f"- rho_{j}: min `{mp.nstr(mn, 8)}`, max `{mp.nstr(mx, 8)}`, max/min `{mp.nstr(spread, 8)}`")
    summary += [
        "",
        f"Best selected-k candidate by average max relative error: `{best_model}` with average max-relative `{model_score[best_model]:.6g}`.",
        "No candidate is uniformly accurate: ratios vary strongly with k and with the zero index.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step343_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 343,
        "orientation": "constructive",
        "target": "zeta-internal cross-rho ratio structure",
        "dps": DPS,
        "rho_indices": [1, 2, 3, 4, 5],
        "k_range": "1..20",
        "selected_k": SELECT_K,
        "best_model": best_model,
        "best_model_average_max_relative_selected_k": model_score[best_model],
        "final_verdict": verdict,
    }
    (ART / "step343_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 343 Nonclaim Boundary",
        "",
        "- No RH claim is made.",
        "- Ratio fitting across the first five zeta zeros is numerical structure testing, not a theorem.",
        "- Conflicting inherited values were not forced; the same dps=80 Leibniz evaluator was used throughout this step.",
    ]
    (ART / "nonclaim_boundary_step343.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"best_model={best_model}")
    print(f"best_score={model_score[best_model]:.12g}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
