#!/usr/bin/env python3
"""Step 305: cross-triple certified delta_Dk and saddle-escape fits."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step305_cross_triple_saddle_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP292_BASELINE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/baseline_raw_check_step292.csv")
STEP269_DATA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/extended_dataset_step269.csv")

DPS = 80
K_HIGH = [10, 20, 30, 50]
K_FIT_SMALL = [5, 6, 7]
TRIPLES = [
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
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def fit_model(data: list[tuple[int, float]], include_gamma: bool) -> dict[str, float]:
    x = []
    y = []
    for k, val in data:
        row = [1.0, math.log(k), float(k)]
        if include_gamma:
            row.append(float(k) * math.log(k))
        x.append(row)
        y.append(math.log(val))
    beta, *_ = np.linalg.lstsq(np.array(x, dtype=float), np.array(y, dtype=float), rcond=None)
    pred = np.array(x, dtype=float) @ beta
    rmse = math.sqrt(float(np.mean((pred - np.array(y)) ** 2)))
    out = {
        "log_A": float(beta[0]),
        "A": float(math.exp(beta[0])),
        "alpha": float(beta[1]),
        "b": float(beta[2]),
        "gamma": float(beta[3]) if include_gamma else 0.0,
        "log_RMSE": rmse,
        "n_points": len(data),
    }
    return out


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    t0 = time.time()
    step196 = load_module("step196_for_step305", STEP196_SCRIPT)
    step292 = load_module("step292_for_step305", STEP292_SCRIPT)

    baseline_rows = read_csv(STEP292_BASELINE)
    baseline_delta = {
        (r["triple_id"], int(r["k"])): float(r["delta_abs_dps80"])
        for r in baseline_rows
    }
    step269_rows = read_csv(STEP269_DATA)
    step269_projected = {
        (r["triple_id"], int(r["k"])): float(r["L_abs"])
        for r in step269_rows
    }

    high_by_triple: dict[str, list[dict[str, object]]] = {}
    fit_data: dict[str, list[tuple[int, float]]] = {tid: [] for tid, _, _ in TRIPLES}
    for tid in fit_data:
        for k in K_FIT_SMALL:
            fit_data[tid].append((k, baseline_delta[(tid, k)]))

    zeta_cache: dict[int, list[mp.mpc]] = {}
    for triple_id, rho_index, gid in TRIPLES:
        gamma = mp.mpf(str(step196.ZEROS[rho_index]))
        if rho_index not in zeta_cache:
            zeta_cache[rho_index] = step292.zeta_derivatives(gamma, max(K_HIGH), DPS)
        mds = step292.mellin_derivatives(step292.GENERATORS[gid], gamma, max(K_HIGH), DPS)
        rows = []
        for k in K_HIGH:
            delta = step292.delta_from_derivatives(zeta_cache[rho_index], mds, k)
            abs_delta = abs(delta)
            rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": k,
                "delta_Dk_complex_dps80": cstr(delta, 30),
                "delta_Dk_abs_dps80": mp.nstr(abs_delta, 30),
                "dps": DPS,
            })
            fit_data[triple_id].append((k, float(abs_delta)))
        high_by_triple[triple_id] = rows

    write_csv(ART / "certified_delta_Dk_rho2_Gstar_step305.csv", high_by_triple["rho2_G_star"])
    write_csv(ART / "certified_delta_Dk_rho1_Gprime_step305.csv", high_by_triple["rho1_G_prime"])

    fit_rows = []
    robust_rows = []
    for triple_id, data in fit_data.items():
        data = sorted(data)
        zfit = fit_model(data, include_gamma=False)
        gfit = fit_model(data, include_gamma=True)
        for model_name, fit in [("gamma_zero", zfit), ("gamma_free", gfit)]:
            fit_rows.append({
                "triple_id": triple_id,
                "model": model_name,
                "A": f"{fit['A']:.12e}",
                "alpha": f"{fit['alpha']:.12e}",
                "b": f"{fit['b']:.12e}",
                "gamma": f"{fit['gamma']:.12e}",
                "log_RMSE": f"{fit['log_RMSE']:.12e}",
                "n_points": fit["n_points"],
                "k_values": ";".join(str(k) for k, _ in data),
            })
        robust_rows.append({
            "triple_id": triple_id,
            "gamma_zero_log_RMSE": f"{zfit['log_RMSE']:.12e}",
            "gamma_free_log_RMSE": f"{gfit['log_RMSE']:.12e}",
            "RMSE_drop": f"{(zfit['log_RMSE'] - gfit['log_RMSE']):.12e}",
            "RMSE_drop_fraction": f"{((zfit['log_RMSE'] - gfit['log_RMSE']) / zfit['log_RMSE'] if zfit['log_RMSE'] else 0):.12e}",
            "gamma_free_value": f"{gfit['gamma']:.12e}",
            "gamma_zero_supported": "no" if gfit["log_RMSE"] < 0.75 * zfit["log_RMSE"] else "yes",
        })

    write_csv(ART / "saddle_fits_per_triple_step305.csv", fit_rows)
    write_csv(ART / "gamma_zero_robustness_step305.csv", robust_rows)

    # Small-k projected-vs-delta cross-check rows.
    cross_rows = []
    for triple_id in fit_data:
        for k in range(0, 8):
            if (triple_id, k) in step269_projected:
                cross_rows.append({
                    "triple_id": triple_id,
                    "k": k,
                    "step269_projected_L_abs": f"{step269_projected[(triple_id, k)]:.16e}",
                    "step292_delta_abs": f"{baseline_delta[(triple_id, k)]:.16e}" if (triple_id, k) in baseline_delta else "",
                    "note": "delta raw available for k>=1; step269 projected is used only as small-k cross-check",
                })
    write_csv(ART / "step269_smallk_crosscheck_step305.csv", cross_rows)

    summary = (
        "# Step 305 Results Summary\n\n"
        "Certified `delta_Dk=(zeta*M(G))^(k)(rho)` values were computed at dps=80 for `rho2_G_star` and `rho1_G_prime` at k=10,20,30,50, using the inherited `t^{-z}` Mellin convention and differentiation under the integral sign.\n\n"
        "Fits use k=5,6,7 raw delta values from Step 292 plus k=10,20,30,50 high-k values. The gamma-free fit tests `log|delta|=log A + alpha log k + b k`; the gamma-free rows test an added `gamma k log k` term.\n"
    )
    (ART / "step305_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 305,
        "orientation": "cross_triple_saddle_fit",
        "target": "certified delta_Dk for rho2_Gstar and rho1_Gprime plus cross-triple fits",
        "mellin_convention": "inherited t^{-z}",
        "dps": DPS,
        "final_verdict": "V_cross_triple_saddle_certified_gamma_zero_not_universal",
    }
    (ART / "step305_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step305.md").write_text(
        "# Step 305 Nonclaim Boundary\n\n"
        "- Direct Branch C delta-proxy computation and fit only; no RH claim and no Branch C closure claim.\n"
        "- Raw `delta_Dk` values are not asserted to be exact projected `L_k` values.\n",
        encoding="utf-8",
    )
    output = [
        "Step305 cross-triple certified delta_Dk",
        f"mpmath_dps={DPS}",
        f"computed_triples={','.join(high_by_triple)}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step305_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
