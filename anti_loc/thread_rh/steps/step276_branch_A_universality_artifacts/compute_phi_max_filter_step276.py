#!/usr/bin/env python3
"""Step 276: compare Branch A Phi at the inherited maximizer across filters."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step276_branch_A_universality_artifacts"
STEP215_SCRIPT = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts/compute_weyl_extended_step215.py"

T_CENTER = 5000.0
N_GRID = 1400
LOCAL_WINDOW = 80.0
LAMBDA = 1.0
SIGMA = 0.35
ELL = 2.0


def load_step215_module():
    spec = importlib.util.spec_from_file_location("step215_weyl_filter", STEP215_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step 215 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step215_weyl_filter"] = mod
    spec.loader.exec_module(mod)
    return mod


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1e-12
    out[mask] = LAMBDA / math.pi
    out[~mask] = np.sin(LAMBDA * arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def l2_inner(f: np.ndarray, g: np.ndarray, weights: np.ndarray) -> complex:
    return complex(np.sum(weights * np.conjugate(f) * g) / (2.0 * math.pi))


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(max(0.0, l2_inner(f, f, weights).real))


def local_grid() -> tuple[np.ndarray, np.ndarray]:
    x, w = leggauss(N_GRID)
    return T_CENTER + LOCAL_WINDOW * x, LOCAL_WINDOW * w


def packet(tau: np.ndarray, weights: np.ndarray) -> np.ndarray:
    z = np.exp(-((tau - T_CENTER) ** 2) / (2.0 * SIGMA * SIGMA))
    z[np.abs(tau - T_CENTER) > 3.0 * SIGMA] = 0.0
    nrm = l2_norm(z.astype(np.complex128), weights)
    return (z / max(nrm, 1e-300)).astype(np.complex128)


def make_operator(tau: np.ndarray, weights: np.ndarray, family: str, psis: np.ndarray | None = None):
    delta = tau[:, None] - tau[None, :]
    sinc_mat = sinc_kernel(delta)
    if family == "holomorphic_truncation_sinc_only":
        kernel = sinc_mat
        psi_conj = None
        psis_local = None
    elif family == "smoothed_step_sinc_gaussian_edge":
        kernel = sinc_mat * np.exp(-(delta / 12.0) ** 2)
        psi_conj = None
        psis_local = None
    elif family == "burnol_sonine_pswf12_truncated":
        if psis is None:
            raise ValueError("psis required")
        kernel = sinc_mat
        psis_local = psis[:12]
        psi_conj = np.conjugate(psis_local)
    elif family == "burnol_sonine_pswf24_baseline":
        if psis is None:
            raise ValueError("psis required")
        kernel = sinc_mat
        psis_local = psis[:24]
        psi_conj = np.conjugate(psis_local)
    else:
        raise ValueError(f"unknown filter family {family}")

    def p_operator(f: np.ndarray) -> np.ndarray:
        band_part = kernel.dot(weights * f)
        if psis_local is None or psi_conj is None:
            return f - band_part
        inner = psi_conj.dot(weights * f)
        pswf_part = psis_local.T.dot(inner)
        return f - band_part - pswf_part

    return p_operator


def phi_for_operator(tau: np.ndarray, weights: np.ndarray, p_operator) -> tuple[float, float]:
    u = packet(tau, weights)
    pu = p_operator(u)
    phase = np.exp(1j * ELL * tau)
    h = phase * pu - p_operator(phase * pu)
    return l2_norm(h, weights), l2_norm(pu, weights)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mod = load_step215_module()
    tau, weights = local_grid()
    psis = mod.build_psi_matrix(tau, n_terms=24)

    families = [
        ("burnol_sonine_pswf24_baseline", "inherited Burnol/Sonine local-window PSWF approximation"),
        ("burnol_sonine_pswf12_truncated", "same Sonine family with fewer PSWF modes"),
        ("holomorphic_truncation_sinc_only", "hard band-truncation / sinc-only diagnostic filter"),
        ("smoothed_step_sinc_gaussian_edge", "smoothed step-function diagnostic filter with Gaussian edge"),
    ]
    rows = []
    for family, notes in families:
        op = make_operator(tau, weights, family, psis=psis)
        phi, pu_norm = phi_for_operator(tau, weights, op)
        rows.append(
            {
                "filter_family": family,
                "sigma": f"{SIGMA:.8f}",
                "ell": f"{ELL:.8f}",
                "Phi": f"{phi:.17e}",
                "P_u_norm": f"{pu_norm:.17e}",
                "T": f"{T_CENTER:.8f}",
                "mpmath_dps": "80",
                "quadrature": f"GL{N_GRID}_double_local_window",
                "notes": notes,
            }
        )
        print(f"{family}: Phi={phi:.12f}")

    write_csv(ART / "filter_family_step276.csv", rows)

    values = [float(row["Phi"]) for row in rows]
    payload = {
        "baseline_phi": rows[0]["Phi"],
        "min_phi": f"{min(values):.17e}",
        "max_phi": f"{max(values):.17e}",
        "spread": f"{(max(values)-min(values)):.17e}",
        "verdict_hint": "family_specific" if (max(values) - min(values)) > 0.02 else "stable",
    }
    (ART / "compute_phi_max_filter_output_step276.txt").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
