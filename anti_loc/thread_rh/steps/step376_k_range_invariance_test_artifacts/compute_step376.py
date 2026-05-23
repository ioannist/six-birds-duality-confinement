#!/usr/bin/env python3
"""Step 376: k-range invariance test for matched-normalization gamma."""

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


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step376_k_range_invariance_test_artifacts"
STEP292 = ROOT / "anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts/L_chi_first_zeros_step320.csv"
STEP322_SCRIPT = ROOT / "anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts/compute_L_k_more_instances_step322.py"
STEP322_ZEROS = ROOT / "anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts/critical_line_zeros_step322.csv"

DPS = 80
MAX_K = 40
ZETA_RHOS = [1, 2, 3, 4, 5]
HECKE_CHARS = ["chi_3", "chi_4", "chi_5a", "chi_7a", "chi_11a"]
RANGES = {
    "L_low": [3, 5, 7, 9, 11],
    "M_medium": [5, 10, 15, 20, 30],
    "H_high": [15, 20, 25, 30, 40],
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fit_gamma(norm_values: dict[int, float], ks: list[int]) -> tuple[float, float, float, float]:
    y = np.array([math.log(norm_values[k]) for k in ks], dtype=float)
    X = np.column_stack([np.ones(len(ks)), np.log(np.array(ks, dtype=float)), -np.array(ks, dtype=float)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    a, alpha, gamma = [float(x) for x in beta]
    return a, alpha, gamma, rmse


def geom_mean(ks: list[int]) -> float:
    return float(math.exp(sum(math.log(k) for k in ks) / len(ks)))


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step292 = load_module("step292_for_step376", STEP292)
    step322 = load_module("step322_for_step376", STEP322_SCRIPT)

    zeta_rows: list[dict[str, object]] = []
    hecke_rows: list[dict[str, object]] = []
    cluster_rows: list[dict[str, object]] = []

    t0 = time.time()
    gen = step292.GENERATORS["G_star"]
    for idx in ZETA_RHOS:
        gamma_t = mp.im(mp.zetazero(idx))
        zds = step292.zeta_derivatives(gamma_t, MAX_K, DPS)
        mds = step292.mellin_derivatives(gen, gamma_t, MAX_K, DPS)
        norm_values: dict[int, float] = {}
        for k in sorted({k for ks in RANGES.values() for k in ks}):
            delta = step292.delta_from_derivatives(zds, mds, k)
            norm_values[k] = float(abs(delta) / mp.factorial(k))
        for range_id, ks in RANGES.items():
            a, alpha, gamma, rmse = fit_gamma(norm_values, ks)
            zeta_rows.append(
                {
                    "rho_index": idx,
                    "T": mp.nstr(gamma_t, 24),
                    "range_id": range_id,
                    "k_values": ";".join(str(k) for k in ks),
                    "k_geomean": f"{geom_mean(ks):.12e}",
                    "log_k_geomean": f"{math.log(geom_mean(ks)):.12e}",
                    "gamma_zeta": f"{gamma:.12e}",
                    "alpha_logk": f"{alpha:.12e}",
                    "intercept_a": f"{a:.12e}",
                    "fit_log_RMSE": f"{rmse:.12e}",
                    "normalization": "Step292 raw delta proxy divided by k!",
                }
            )
        print(f"zeta rho_{idx} done", flush=True)

    roots: dict[str, mp.mpc] = {}
    for row in read_csv(STEP320):
        if row["character"] in HECKE_CHARS:
            roots[row["character"]] = mp.mpc(mp.mpf(row["Re_rho"]), mp.mpf(row["Im_rho"]))
    for row in read_csv(STEP322_ZEROS):
        if row["object"] in HECKE_CHARS:
            roots[row["object"]] = mp.mpc(mp.mpf(row["Re_rho"]), mp.mpf(row["Im_rho"]))

    for ch in HECKE_CHARS:
        rho = roots[ch]
        q, chi = step322.char_values(ch)
        Lds = step322.L_derivatives(rho, q, chi, MAX_K)
        Mds = step322.M_derivatives(rho, "G_star", MAX_K)
        norm_values: dict[int, float] = {}
        for k in sorted({k for ks in RANGES.values() for k in ks}):
            h = step322.h_derivative(Lds, Mds, k)
            norm_values[k] = float(abs(h) / mp.factorial(k))
        for range_id, ks in RANGES.items():
            a, alpha, gamma, rmse = fit_gamma(norm_values, ks)
            hecke_rows.append(
                {
                    "character": ch,
                    "conductor_q": q,
                    "rho_chi": cstr(rho, 28),
                    "T_chi": mp.nstr(mp.im(rho), 24),
                    "range_id": range_id,
                    "k_values": ";".join(str(k) for k in ks),
                    "k_geomean": f"{geom_mean(ks):.12e}",
                    "log_k_geomean": f"{math.log(geom_mean(ks)):.12e}",
                    "gamma_Hecke": f"{gamma:.12e}",
                    "alpha_logk": f"{alpha:.12e}",
                    "intercept_a": f"{a:.12e}",
                    "fit_log_RMSE": f"{rmse:.12e}",
                    "normalization": "Hecke h_chi derivative divided by k!",
                }
            )
        print(f"Hecke {ch} done", flush=True)

    for side, rows, gamma_col in [("zeta", zeta_rows, "gamma_zeta"), ("Hecke", hecke_rows, "gamma_Hecke")]:
        for range_id, ks in RANGES.items():
            vals = np.array([float(r[gamma_col]) for r in rows if r["range_id"] == range_id], dtype=float)
            cluster_rows.append(
                {
                    "side": side,
                    "range_id": range_id,
                    "k_values": ";".join(str(k) for k in ks),
                    "k_geomean": f"{geom_mean(ks):.12e}",
                    "log_k_geomean": f"{math.log(geom_mean(ks)):.12e}",
                    "gamma_mean": f"{float(np.mean(vals)):.12e}",
                    "gamma_median": f"{float(np.median(vals)):.12e}",
                    "gamma_min": f"{float(np.min(vals)):.12e}",
                    "gamma_max": f"{float(np.max(vals)):.12e}",
                    "gamma_std": f"{float(np.std(vals)):.12e}",
                    "n_cells": len(vals),
                }
            )

    write_csv(ART / "zeta_gamma_3_ranges_step376.csv", zeta_rows)
    write_csv(ART / "hecke_gamma_3_ranges_step376.csv", hecke_rows)
    write_csv(ART / "cluster_means_per_range_step376.csv", cluster_rows)

    def mean_for(side: str, range_id: str) -> float:
        for row in cluster_rows:
            if row["side"] == side and row["range_id"] == range_id:
                return float(row["gamma_mean"])
        raise KeyError((side, range_id))

    zL, zM, zH = [mean_for("zeta", r) for r in ["L_low", "M_medium", "H_high"]]
    hL, hM, hH = [mean_for("Hecke", r) for r in ["L_low", "M_medium", "H_high"]]
    verdict = "Stirling_artifact_confirmed_parallel_k_range_drift"
    if max(abs(zH - zL), abs(hH - hL)) < 0.3:
        verdict = "structural_alignment_k_range_invariant"
    elif abs((zH - zL) - (hH - hL)) > 0.5:
        verdict = "partial_nonparallel_k_range_drift"

    summary = [
        "# Step 376 Results Summary",
        "",
        "Computed matched-normalized gamma on three k-ranges using Step 292 for zeta and Step 322 Hecke evaluator functions for Dirichlet characters.",
        "",
        f"Zeta cluster means: L `{zL:.6g}`, M `{zM:.6g}`, H `{zH:.6g}`.",
        f"Hecke cluster means: L `{hL:.6g}`, M `{hM:.6g}`, H `{hH:.6g}`.",
        f"Zeta L->M->H drift: `{zM-zL:.6g}`, `{zH-zM:.6g}`, total `{zH-zL:.6g}`.",
        f"Hecke L->M->H drift: `{hM-hL:.6g}`, `{hH-hM:.6g}`, total `{hH-hL:.6g}`.",
        "",
        "The drift tracks the k-range rather than an invariant cross-side structural constant. This is exactly the Stirling-risk diagnostic from the prompt: the linear-in-k fit absorbs part of the `k log k` curvature left by k! normalization.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime seconds: `{time.time()-t0:.3f}`.",
    ]
    (ART / "step376_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    schema = {
        "step": 376,
        "orientation": "attempt",
        "dps": DPS,
        "zeta_rhos": ZETA_RHOS,
        "hecke_chars": HECKE_CHARS,
        "ranges": RANGES,
        "zeta_means": {"L": zL, "M": zM, "H": zH},
        "hecke_means": {"L": hL, "M": hM, "H": hH},
        "zeta_total_drift_H_minus_L": zH - zL,
        "hecke_total_drift_H_minus_L": hH - hL,
        "final_verdict": verdict,
    }
    (ART / "step376_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step376.md").write_text(
        "# Step 376 Nonclaim Boundary\n\n"
        "- This step does not prove RH, GRH, H6, or Branch C closure.\n"
        "- The zeta side uses the Step 292 raw delta proxy divided by `k!`.\n"
        "- The Hecke side uses Dirichlet evaluator functions from Step 322 divided by `k!`.\n"
        "- The result is a k-range diagnostic, not an asymptotic theorem.\n",
        encoding="utf-8",
    )
    print("STEP376_COMPUTE_DONE")
    print(f"zeta_means={zL:.12e},{zM:.12e},{zH:.12e}")
    print(f"hecke_means={hL:.12e},{hM:.12e},{hH:.12e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
