#!/usr/bin/env python3
"""Step 304: direct Cauchy integral verification for delta_Dk(k=10)."""

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


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step304_cauchy_direct_verification_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

MP_DPS = 80
N_THETA = 2048
K = 10
RADII = [mp.mpf("3"), mp.mpf("5.06"), mp.mpf("8"), mp.mpf("11.34"), mp.mpf("14.0")]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


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


class MellinFast:
    def __init__(self, step292, n_nodes: int = 260):
        self.step292 = step292
        self.centers, self.epsilons, self.coeffs = step292.moment_coefficients(step292.GENERATORS["G_star"])
        x, w = np.polynomial.legendre.leggauss(n_nodes)
        self.nodes = []
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps
            mid = (lo + hi) / 2
            half = (hi - lo) / 2
            for xi, wi in zip(x, w):
                t = mid + half * mp.mpf(str(xi))
                weight = half * mp.mpf(str(wi))
                bump = step292.beta_bump((t - c) / eps)
                self.nodes.append((t, weight * coeff * bump))

    def __call__(self, z: mp.mpc) -> mp.mpc:
        total = mp.mpc(0)
        for t, wg in self.nodes:
            total += wg * (t ** (-z))
        return total


def cauchy_delta(rho: mp.mpc, R: mp.mpf, M: MellinFast) -> mp.mpc:
    total = mp.mpc(0)
    for j in range(N_THETA):
        theta = 2 * mp.pi * j / N_THETA
        z = rho + R * mp.e ** (1j * theta)
        h = mp.zeta(z) * M(z)
        total += h * mp.e ** (-1j * K * theta)
    return mp.factorial(K) * total / (mp.mpf(N_THETA) * (R ** K))


def leibniz_delta(step292, gamma: mp.mpf, dps: int) -> mp.mpc:
    zds = step292.zeta_derivatives(gamma, K, dps)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, K, dps)
    return step292.delta_from_derivatives(zds, mds, K)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    t0 = time.time()
    step196 = load_module("step196_for_step304", STEP196_SCRIPT)
    step292 = load_module("step292_for_step304", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    rho = mp.mpc(mp.mpf("0.5"), gamma)
    M = MellinFast(step292, n_nodes=260)

    leib80 = leibniz_delta(step292, gamma, 80)
    leib120 = leibniz_delta(step292, gamma, 120)

    rows = []
    for R in RADII:
        tR = time.time()
        val = cauchy_delta(rho, R, M)
        rel_complex = abs(val - leib120) / abs(leib120)
        rel_abs = abs(abs(val) - abs(leib120)) / abs(leib120)
        rows.append({
            "R": mp.nstr(R, 18),
            "N_theta": N_THETA,
            "cauchy_complex": cstr(val, 34),
            "cauchy_abs": mp.nstr(abs(val), 34),
            "cauchy_real": mp.nstr(mp.re(val), 34),
            "cauchy_imag": mp.nstr(mp.im(val), 34),
            "leibniz_dps80_complex": cstr(leib80, 34),
            "leibniz_dps80_abs": mp.nstr(abs(leib80), 34),
            "leibniz_dps120_complex": cstr(leib120, 34),
            "leibniz_dps120_abs": mp.nstr(abs(leib120), 34),
            "rel_err_complex_vs_dps120": mp.nstr(rel_complex, 18),
            "rel_err_abs_vs_dps120": mp.nstr(rel_abs, 18),
            "runtime_seconds_R": f"{time.time() - tR:.3f}",
        })

    write_csv(ART / "cauchy_quadrature_per_R_step304.csv", rows)
    max_rel = max(mp.mpf(r["rel_err_complex_vs_dps120"]) for r in rows)
    leib_rel = abs(leib80 - leib120) / abs(leib120)
    verdict = "V_cauchy_direct_verified" if max_rel < mp.mpf("1e-3") else "V_cauchy_direct_partial_radius_instability"
    summary = (
        "# Step 304 Results Summary\n\n"
        f"Direct Cauchy trapezoidal quadrature used `N={N_THETA}` angles and the inherited `t^(-z)` convention. "
        f"Leibniz dps80 and dps120 relative difference: `{mp.nstr(leib_rel, 18)}`.\n\n"
        f"Final verdict: `{verdict}`. The radius table records whether direct contour quadrature agrees with the dps120 Leibniz value.\n"
    )
    (ART / "step304_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 304,
        "orientation": "cauchy_direct_verification",
        "target": "delta_Dk k=10 rho1 G_star",
        "mellin_convention": "inherited t^{-z}",
        "N_theta": N_THETA,
        "leibniz_dps80_abs": mp.nstr(abs(leib80), 34),
        "leibniz_dps120_abs": mp.nstr(abs(leib120), 34),
        "leibniz_dps80_dps120_rel": mp.nstr(leib_rel, 18),
        "max_cauchy_rel_err_complex": mp.nstr(max_rel, 18),
        "final_verdict": verdict,
    }
    (ART / "step304_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step304.md").write_text(
        "# Step 304 Nonclaim Boundary\n\n"
        "- Direct numerical Cauchy verification only; no RH claim and no Branch C closure claim.\n"
        "- Agreement or disagreement diagnoses numerical/asymptotic status of the Branch C proxy `delta_Dk`, not projected `L_k` closure.\n",
        encoding="utf-8",
    )
    output = [
        "Step304 direct Cauchy verification",
        f"mpmath_dps={MP_DPS}",
        f"N_theta={N_THETA}",
        f"leibniz_dps120={cstr(leib120, 20)} abs={mp.nstr(abs(leib120), 20)}",
        f"max_rel_complex_vs_dps120={mp.nstr(max_rel, 12)}",
        f"verdict={verdict}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step304_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
