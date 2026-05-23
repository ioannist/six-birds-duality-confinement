#!/usr/bin/env python3
"""Step 216 Gram-Schmidt test for Branch A Weyl diagnostics."""

from __future__ import annotations

import csv
import importlib.util
import math
import os
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = int(os.environ.get("STEP216_DPS", "80"))

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step216_branch_A_gram_schmidt_weyl_artifacts"
STEP215_SCRIPT = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts/compute_weyl_extended_step215.py"

T_MAX = 100.0
N_GRID = 140
N_CAND1 = 20
N_CAND2 = 10
ELL = math.log(2.0)
ERROR = 5.0e-2


def load_step215_module():
    spec = importlib.util.spec_from_file_location("step215_weyl", STEP215_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step215 Weyl module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step215_weyl"] = mod
    spec.loader.exec_module(mod)
    return mod


def c_action(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray, mod) -> np.ndarray:
    pk = mod.p_operator(f, tau, weights, psis)
    phase = np.exp(1j * ELL * tau)
    return phase * pk - mod.p_operator(phase * pk, tau, weights, psis)


def gram_schmidt(kappas: dict[int, np.ndarray], tau: np.ndarray, weights: np.ndarray, psis: np.ndarray, mod, label: str):
    rows: list[dict[str, object]] = []
    basis: list[np.ndarray] = []
    for n in sorted(kappas):
        raw = kappas[n].astype(np.complex128)
        raw_norm = mod.l2_norm(raw, weights)
        w = raw.copy()
        # Reorthogonalized modified Gram-Schmidt. The second pass matters
        # because Step 215 found near-parallel sampled vectors.
        for _ in range(2):
            for v in basis:
                coeff = mod.l2_inner(v, w, weights)
                w = w - coeff * v
        residual_norm = mod.l2_norm(w, weights)
        rel = residual_norm / max(raw_norm, 1e-300)
        if residual_norm > 1e-35:
            v = w / residual_norm
            c_norm = mod.l2_norm(c_action(v, tau, weights, psis, mod), weights)
            basis.append(v)
            stability = "usable" if residual_norm > 1e-12 else "low_absolute_signal"
        else:
            v = np.zeros_like(w)
            c_norm = float("nan")
            stability = "numerical_null"
        rows.append(
            {
                "model": label,
                "n": n,
                "raw_norm": f"{raw_norm:.17e}",
                "w_residual_norm": f"{residual_norm:.17e}",
                "relative_residual_norm": f"{rel:.17e}",
                "v_norm": "1.00000000000000000e+00" if stability == "usable" else "nan",
                "C_l_v_n_norm": f"{c_norm:.17e}" if math.isfinite(c_norm) else "nan",
                "error_bound": f"{ERROR:.1e}",
                "stability": stability,
            }
        )
    return rows


def summarize(rows: list[dict[str, object]], label: str) -> dict[str, object]:
    rels = [float(r["relative_residual_norm"]) for r in rows]
    cnorms = [float(r["C_l_v_n_norm"]) for r in rows if r["C_l_v_n_norm"] != "nan"]
    usable = len(cnorms)
    dim_1e2 = sum(1 for x in rels if x > 1e-2)
    dim_1e4 = sum(1 for x in rels if x > 1e-4)
    dim_1e6 = sum(1 for x in rels if x > 1e-6)
    after_first = cnorms[1:] if len(cnorms) > 1 else []
    return {
        "model": label,
        "computed_directions": usable,
        "effective_dim_rel_gt_1e-2": dim_1e2,
        "effective_dim_rel_gt_1e-4": dim_1e4,
        "effective_dim_rel_gt_1e-6": dim_1e6,
        "min_C_l_v_n_norm": f"{min(cnorms):.17e}" if cnorms else "nan",
        "min_after_first": f"{min(after_first):.17e}" if after_first else "nan",
        "max_after_first": f"{max(after_first):.17e}" if after_first else "nan",
        "last_C_l_v_n_norm": f"{cnorms[-1]:.17e}" if cnorms else "nan",
    }


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_step215_module()

    raw_x, raw_w = leggauss(N_GRID)
    tau = T_MAX * raw_x
    weights = T_MAX * raw_w
    z20 = mod.zeros(N_CAND1)
    psis = mod.build_psi_matrix(tau)

    print("building CAND1 kappas")
    c1 = mod.cand1_kappas(tau, z20)
    print("building CAND2 kappas")
    z10 = {n: z20[n] for n in range(1, N_CAND2 + 1)}
    c2 = mod.cand2_kappas(tau, z10)

    print("Gram-Schmidt CAND1")
    rows1 = gram_schmidt(c1, tau, weights, psis, mod, "CAND1")
    print("Gram-Schmidt CAND2")
    rows2 = gram_schmidt(c2, tau, weights, psis, mod, "CAND2")
    rows = rows1 + rows2

    with (BASE / "gram_schmidt_step216.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = [summarize(rows1, "CAND1"), summarize(rows2, "CAND2")]
    with (BASE / "effective_dimension_step216.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    # Conservative verdict: obstruction persists only if post-GS directions
    # keep a substantial lower bound and residuals are not just numerical noise.
    c1_vals = [float(r["C_l_v_n_norm"]) for r in rows1 if r["C_l_v_n_norm"] != "nan"]
    c1_rels = [float(r["relative_residual_norm"]) for r in rows1]
    c2_vals = [float(r["C_l_v_n_norm"]) for r in rows2 if r["C_l_v_n_norm"] != "nan"]
    high_conf_c1 = [r for r in rows1 if r["stability"] == "usable"]
    low_signal_c1 = [r for r in rows1 if r["stability"] == "low_absolute_signal"]
    if len(c1_vals) >= 10 and min(c1_vals) >= 0.5 and min(c1_rels[:10]) > 1e-6 and not low_signal_c1:
        verdict = "V_weyl_gram_schmidt_obstruction_persists"
    elif len(c1_vals) >= 3 and min(c1_vals[1: min(10, len(c1_vals))]) < 0.1 and len(high_conf_c1) >= 3:
        verdict = "V_weyl_gram_schmidt_decay_to_zero"
    elif len(c1_vals) >= 3 and not low_signal_c1:
        verdict = "V_weyl_gram_schmidt_intermediate"
    else:
        verdict = "V_weyl_gram_schmidt_inconclusive"

    robustness = [
        {
            "check": "CAND1_Gram_Schmidt",
            "status": verdict,
            "value": summary_rows[0]["min_C_l_v_n_norm"],
            "notes": "Primary orthonormalized finite-grid sequence.",
        },
        {
            "check": "CAND2_Gram_Schmidt",
            "status": "comparison",
            "value": summary_rows[1]["min_C_l_v_n_norm"],
            "notes": "Zeta-form comparison model, not asserted as correct a=1/2 transport.",
        },
        {
            "check": "precision",
            "status": "finite_grid_double_operator_with_mpmath_80_inputs",
            "value": "mpmath_dps=80; grid=140; interval=[-100,100]",
            "notes": "Operator application remains the Step 214/215 finite PSWF/sinc model.",
        },
    ]
    with (BASE / "robustness_step216.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness[0].keys()))
        writer.writeheader()
        writer.writerows(robustness)

    with (BASE / "compute_gram_schmidt_output_step216.txt").open("w") as f:
        f.write("Step 216 Gram-Schmidt Weyl test\n")
        for r in rows1:
            f.write(
                f"CAND1 n={r['n']:>2} rel_w={r['relative_residual_norm']} "
                f"Cnorm={r['C_l_v_n_norm']} stability={r['stability']}\n"
            )
        for r in rows2:
            f.write(
                f"CAND2 n={r['n']:>2} rel_w={r['relative_residual_norm']} "
                f"Cnorm={r['C_l_v_n_norm']} stability={r['stability']}\n"
            )
        f.write(f"verdict={verdict}\n")

    print((BASE / "compute_gram_schmidt_output_step216.txt").read_text())


if __name__ == "__main__":
    main()
