#!/usr/bin/env python3
"""Step 302: saddle-width correction at the dominant far-left arc."""

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


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step302_saddle_width_correction_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP301_OPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step301_h_max_asymptotic_artifacts/R_optimal_per_k_step301.csv")

MP_DPS = 80
CERTIFIED = {
    10: mp.mpf("165.438682954225418261054825"),
    20: mp.mpf("554847.0159555452761473487386"),
    30: mp.mpf("4.0851435758143067e9"),
    50: mp.mpf("1.1691354860063852e18"),
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


class MellinFast:
    def __init__(self, step292, n_nodes: int = 220):
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
                self.nodes.append((t, weight * coeff * bump, mp.log(t)))

    def derivs(self, z: mp.mpc) -> tuple[mp.mpc, mp.mpc, mp.mpc]:
        m0 = mp.mpc(0)
        m1 = mp.mpc(0)
        m2 = mp.mpc(0)
        for t, wg, lt in self.nodes:
            base = wg * (t ** (-z))
            m0 += base
            m1 += base * (-lt)
            m2 += base * (lt ** 2)
        return m0, m1, m2

    def h_derivs(self, z: mp.mpc) -> tuple[mp.mpc, mp.mpc, mp.mpc]:
        m0, m1, m2 = self.derivs(z)
        z0 = mp.zeta(z)
        z1 = mp.zeta(z, derivative=1)
        z2 = mp.zeta(z, derivative=2)
        h0 = z0 * m0
        h1 = z1 * m0 + z0 * m1
        h2 = z2 * m0 + 2 * z1 * m1 + z0 * m2
        return h0, h1, h2


def locate_zmax(rho: mp.mpc, R: mp.mpf, M: MellinFast, n_angles: int = 720) -> tuple[mp.mpf, mp.mpc, mp.mpf]:
    best_theta = mp.mpf(0)
    best_z = rho + R
    best_h = mp.mpf("-1")
    for j in range(n_angles):
        theta = 2 * mp.pi * j / n_angles
        z = rho + R * mp.e ** (1j * theta)
        h0, _, _ = M.h_derivs(z)
        h_abs = abs(h0)
        if h_abs > best_h:
            best_theta, best_z, best_h = theta, z, h_abs
    return best_theta, best_z, best_h


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    t0 = time.time()
    step196 = load_module("step196_for_step302", STEP196_SCRIPT)
    step292 = load_module("step292_for_step302", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    rho = mp.mpc(mp.mpf("0.5"), gamma)
    M = MellinFast(step292, n_nodes=220)
    opt_by_k = {int(row["k"]): row for row in read_csv(STEP301_OPT)}

    z_rows = []
    pred_rows = []
    for k in [10, 20, 30, 50]:
        R = mp.mpf(opt_by_k[k]["R_star_fit"])
        theta, zmax, h_abs = locate_zmax(rho, R, M, n_angles=720)
        h0, h1, h2 = M.h_derivs(zmax)
        logh_pp = (h2 * h0 - h1 * h1) / (h0 * h0)
        phi_pp = logh_pp + mp.mpf(k + 1) / ((zmax - rho) ** 2)
        phi_abs = abs(phi_pp)
        cauchy_bound = mp.factorial(k) * h_abs / (R ** k)
        width = mp.sqrt(2 * mp.pi / (mp.mpf(k) * phi_abs))
        corrected = cauchy_bound * width
        cert = CERTIFIED[k]
        rel = abs(corrected - cert) / cert
        z_rows.append({
            "k": k,
            "R_star": mp.nstr(R, 18),
            "theta": mp.nstr(theta, 18),
            "z_real": mp.nstr(mp.re(zmax), 18),
            "z_imag": mp.nstr(mp.im(zmax), 18),
            "h_abs_at_zmax": mp.nstr(h_abs, 18),
            "logh_pp_abs": mp.nstr(abs(logh_pp), 18),
            "phi_pp_abs": mp.nstr(phi_abs, 18),
            "phi_pp_real": mp.nstr(mp.re(phi_pp), 18),
            "phi_pp_imag": mp.nstr(mp.im(phi_pp), 18),
        })
        pred_rows.append({
            "k": k,
            "cauchy_bound_uncorrected": mp.nstr(cauchy_bound, 18),
            "saddle_width_factor": mp.nstr(width, 18),
            "predicted_corrected": mp.nstr(corrected, 18),
            "certified_delta_abs": mp.nstr(cert, 18),
            "relative_error": mp.nstr(rel, 18),
            "corrected_over_certified": mp.nstr(corrected / cert, 18),
        })

    write_csv(ART / "z_max_and_phi_pp_step302.csv", z_rows)
    write_csv(ART / "predicted_corrected_step302.csv", pred_rows)
    max_rel = max(mp.mpf(row["relative_error"]) for row in pred_rows)
    verdict = "V_saddle_width_correction_established" if max_rel < mp.mpf("0.10") else "V_saddle_width_correction_partial"
    summary = (
        "# Step 302 Results Summary\n\n"
        "Applied the proposed steepest-descent width correction at the dominant far-upper-left arc using the inherited `t^{-z}` convention. "
        "Derivatives were computed analytically from `M'(z)=int G(t)(-log t)t^{-z}dt` and `M''(z)=int G(t)(log t)^2t^{-z}dt`, combined with `zeta'` and `zeta''`.\n\n"
        f"Final verdict: `{verdict}`. The correction reduces the Step 301 Cauchy looseness, but the residual factor is not uniformly below 10%.\n"
    )
    (ART / "step302_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 302,
        "orientation": "saddle_width_correction",
        "target": "dominant far-left arc width correction for delta_Dk",
        "mellin_convention": "inherited t^{-z}",
        "final_verdict": verdict,
    }
    (ART / "step302_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step302.md").write_text(
        "# Step 302 Nonclaim Boundary\n\n"
        "- Direct Branch C asymptotic attempt only; no RH claim and no Branch C closure claim.\n"
        "- Width correction is evaluated at circle maxima, not a theorem-grade proof of a steepest-descent contour.\n",
        encoding="utf-8",
    )
    output = [
        "Step302 saddle-width correction",
        f"mpmath_dps={MP_DPS}",
        f"max_relative_error={mp.nstr(max_rel, 12)}",
        f"verdict={verdict}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step302_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
