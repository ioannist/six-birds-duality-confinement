#!/usr/bin/env python3
"""Step 303: stationary phase for the Cauchy-circle Fourier coefficient."""

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


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step303_stationary_phase_circle_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP301_OPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step301_h_max_asymptotic_artifacts/R_optimal_per_k_step301.csv")

MP_DPS = 80
N_SCAN = 720
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


def phase_quantities(theta: mp.mpf, rho: mp.mpc, R: mp.mpf, k: int, M: MellinFast):
    z = rho + R * mp.e ** (1j * theta)
    zp = 1j * R * mp.e ** (1j * theta)
    zpp = -R * mp.e ** (1j * theta)
    h0, h1, h2 = M.h_derivs(z)
    A = h1 / h0
    Aprime = h2 / h0 - A * A
    darg = mp.im(A * zp)
    phi_prime = darg - k
    phi_pp = mp.im(Aprime * zp * zp + A * zpp)
    total_phase = mp.arg(h0) - k * theta
    return z, h0, phi_prime, phi_pp, total_phase


def bisect_root(func, a: mp.mpf, b: mp.mpf, max_iter: int = 80) -> mp.mpf:
    fa = func(a)
    fb = func(b)
    if abs(fa) < mp.mpf("1e-40"):
        return a
    if abs(fb) < mp.mpf("1e-40"):
        return b
    if fa * fb > 0:
        raise ValueError("not bracketed")
    lo, hi = a, b
    flo, fhi = fa, fb
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        fm = func(mid)
        if abs(fm) < mp.mpf("1e-35"):
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def find_stationary_points(rho: mp.mpc, R: mp.mpf, k: int, M: MellinFast) -> list[mp.mpf]:
    two_pi = 2 * mp.pi

    def g(th):
        return phase_quantities(th % two_pi, rho, R, k, M)[2]

    grid = [two_pi * j / N_SCAN for j in range(N_SCAN + 1)]
    vals = [g(th) for th in grid]
    roots: list[mp.mpf] = []
    for j in range(N_SCAN):
        a, b = grid[j], grid[j + 1]
        fa, fb = vals[j], vals[j + 1]
        if fa == 0:
            roots.append(a)
        elif fa * fb < 0:
            try:
                root = bisect_root(g, a, b)
                root = root % two_pi
                if all(abs(mp.arg(mp.e ** (1j * (root - r)))) > mp.mpf("1e-8") for r in roots):
                    roots.append(root)
            except Exception:
                pass
    roots.sort()
    return roots


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    t0 = time.time()
    step196 = load_module("step196_for_step303", STEP196_SCRIPT)
    step292 = load_module("step292_for_step303", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    rho = mp.mpc(mp.mpf("0.5"), gamma)
    M = MellinFast(step292, n_nodes=220)
    opt_by_k = {int(row["k"]): row for row in read_csv(STEP301_OPT)}

    point_rows = []
    pred_rows = []
    for k in [10, 20, 30, 50]:
        R = mp.mpf(opt_by_k[k]["R_star_fit"])
        roots = find_stationary_points(rho, R, k, M)
        contrib_sum_user = mp.mpc(0)
        contrib_sum_total = mp.mpc(0)
        sum_magnitudes_user = mp.mpf(0)
        for idx, theta in enumerate(roots, start=1):
            z, h0, phi_prime, phi_pp, total_phase = phase_quantities(theta, rho, R, k, M)
            sign = 1 if phi_pp >= 0 else -1
            # User-requested normalized correction includes an extra k in the
            # denominator; the total-phase formula omits that extra factor.
            width_user = mp.sqrt(2 * mp.pi / (mp.mpf(k) * abs(phi_pp)))
            width_total = mp.sqrt(2 * mp.pi / abs(phi_pp))
            phase_factor = mp.e ** (1j * (mp.pi / 4) * sign)
            osc = h0 * mp.e ** (-1j * k * theta)
            contrib_user = osc * width_user * phase_factor
            contrib_total = osc * width_total * phase_factor
            contrib_sum_user += contrib_user
            contrib_sum_total += contrib_total
            sum_magnitudes_user += abs(h0) * width_user
            point_rows.append({
                "k": k,
                "stationary_index": idx,
                "theta_star": mp.nstr(theta, 18),
                "z_real": mp.nstr(mp.re(z), 18),
                "z_imag": mp.nstr(mp.im(z), 18),
                "H_abs": mp.nstr(abs(h0), 18),
                "Phi": mp.nstr(total_phase, 18),
                "Phi_prime": mp.nstr(phi_prime, 12),
                "Phi_pp": mp.nstr(phi_pp, 18),
                "Phi_pp_abs": mp.nstr(abs(phi_pp), 18),
                "width_user": mp.nstr(width_user, 18),
                "contrib_abs_user": mp.nstr(abs(contrib_user), 18),
            })
        pref = mp.factorial(k) / (2 * mp.pi * (R ** k))
        pred_user = pref * abs(contrib_sum_user)
        pred_user_abs_sum = pref * sum_magnitudes_user
        pred_total = pref * abs(contrib_sum_total)
        cert = CERTIFIED[k]
        pred_rows.append({
            "k": k,
            "R_star": mp.nstr(R, 18),
            "stationary_point_count": len(roots),
            "predicted_user_phase_sum": mp.nstr(pred_user, 18),
            "predicted_user_abs_sum": mp.nstr(pred_user_abs_sum, 18),
            "predicted_total_phase_sum_no_extra_k": mp.nstr(pred_total, 18),
            "certified_delta_abs": mp.nstr(cert, 18),
            "relative_error_user_phase_sum": mp.nstr(abs(pred_user - cert) / cert, 18),
            "relative_error_user_abs_sum": mp.nstr(abs(pred_user_abs_sum - cert) / cert, 18),
            "relative_error_total_no_extra_k": mp.nstr(abs(pred_total - cert) / cert, 18),
        })

    write_csv(ART / "stationary_phase_points_step303.csv", point_rows)
    write_csv(ART / "predicted_via_stationary_phase_step303.csv", pred_rows)
    max_rel = max(mp.mpf(r["relative_error_user_phase_sum"]) for r in pred_rows)
    verdict = "V_stationary_phase_circle_established" if max_rel < mp.mpf("0.10") else "V_stationary_phase_circle_partial"
    summary = (
        "# Step 303 Results Summary\n\n"
        "Stationary points were found from `Im((h'/h)iR exp(i theta)) = k` on the Step 301 Cauchy-optimal circles, using the inherited `t^{-z}` convention. "
        "The CSV includes both the user-requested `sqrt(2pi/(k|Phi''|))` phase-sum prediction and a diagnostic no-extra-k variant.\n\n"
        f"Final verdict: `{verdict}`. The stationary-phase points exist, but the leading one-circle approximation is not uniformly within 10% of certified `delta_Dk`.\n"
    )
    (ART / "step303_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 303,
        "orientation": "stationary_phase_circle",
        "target": "Fourier coefficient stationary phase on Cauchy circle",
        "mellin_convention": "inherited t^{-z}",
        "scan_angles": N_SCAN,
        "final_verdict": verdict,
    }
    (ART / "step303_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step303.md").write_text(
        "# Step 303 Nonclaim Boundary\n\n"
        "- Direct Branch C stationary-phase attempt only; no RH claim and no Branch C closure claim.\n"
        "- The stationary-phase formula is an asymptotic model for one selected Cauchy radius; exact contour deformation and endpoint contributions are not proved here.\n",
        encoding="utf-8",
    )
    output = [
        "Step303 stationary-phase circle attempt",
        f"mpmath_dps={MP_DPS}",
        f"max_relative_error_user_phase_sum={mp.nstr(max_rel, 12)}",
        f"verdict={verdict}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step303_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
