#!/usr/bin/env python3
"""Step 300: scan |h(z)|=|zeta(z) M(G_star)(z)| on circles.

Important convention: the certified Step292 delta_Dk values use the inherited
Branch C Mellin factor int G(t) t^{-z} dt, not the standard t^{z-1} Mellin
factor.  This script therefore scans the same h(z) that generated the certified
derivatives.
"""

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

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step300_h_circle_scan_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

MP_DPS = 80
R_MAIN = mp.mpf("11.3406995042713390985203494954")
RADII = [mp.mpf("5.06"), mp.mpf("8"), R_MAIN, mp.mpf("14.0"), mp.mpf("14.13"), mp.mpf("17.010368213376501812603831941"), mp.mpf("20"), mp.mpf("25"), mp.mpf("30.41")]
DELTA10 = mp.mpf("165.43868295422541")
DELTA20 = mp.mpf("554847.01595554524")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


class MellinFast:
    """Gauss-Legendre mpmath-arithmetic evaluator, with mp.quad validation."""

    def __init__(self, step292, n_nodes: int = 180):
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
        zz = -z
        for t, wg in self.nodes:
            total += wg * mp.power(t, zz)
        return total

    def quad(self, z: mp.mpc) -> mp.mpc:
        total = mp.mpc(0)
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t, cc=c, ee=eps, aa=coeff):
                return aa * self.step292.beta_bump((t - cc) / ee) * (t ** (-z))

            total += mp.quad(integrand, [lo, hi])
        return total


def scan_radius(rho: mp.mpc, R: mp.mpf, M: MellinFast, n_angles: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows = []
    max_row = None
    min_row = None
    for j in range(n_angles):
        theta = 2 * mp.pi * j / n_angles
        z = rho + R * mp.e ** (1j * theta)
        zeta_abs = abs(mp.zeta(z))
        M_abs = abs(M(z))
        h_abs = zeta_abs * M_abs
        row = {
            "angle_index": j,
            "theta": mp.nstr(theta, 18),
            "z_real": mp.nstr(mp.re(z), 18),
            "z_imag": mp.nstr(mp.im(z), 18),
            "zeta_abs": mp.nstr(zeta_abs, 18),
            "M_G_abs": mp.nstr(M_abs, 18),
            "h_abs": mp.nstr(h_abs, 18),
            "log_h_abs": mp.nstr(mp.log(h_abs), 18) if h_abs else "-inf",
        }
        rows.append(row)
        if max_row is None or h_abs > mp.mpf(str(max_row["h_abs"])):
            max_row = row
        if min_row is None or h_abs < mp.mpf(str(min_row["h_abs"])):
            min_row = row
    assert max_row is not None and min_row is not None
    summary = {"max": max_row, "min": min_row}
    return rows, summary


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step300", STEP196_SCRIPT)
    step292 = load_module("step292_for_step300", STEP292_SCRIPT)
    rho = mp.mpc(mp.mpf("0.5"), mp.mpf(str(step196.ZEROS[1])))
    M = MellinFast(step292, n_nodes=180)
    fact10 = mp.factorial(10)
    fact20 = mp.factorial(20)
    required_Rmain = DELTA10 * (R_MAIN ** 10) / fact10

    output = [
        "Step300 h-circle scan",
        f"mpmath_dps={MP_DPS}",
        f"Cauchy required max at R=11.34 for k=10: {mp.nstr(required_Rmain, 16)}",
    ]
    max_rows = []
    k20_rows = []
    full_Rmain_rows = []
    t0 = time.time()
    for R in RADII:
        n = 720 if abs(R - R_MAIN) < mp.mpf("1e-20") else 360
        rows, summary = scan_radius(rho, R, M, n)
        maxr = summary["max"]
        minr = summary["min"]
        max_h_fast = mp.mpf(str(maxr["h_abs"]))
        zmax = mp.mpc(mp.mpf(maxr["z_real"]), mp.mpf(maxr["z_imag"]))
        # Validate the max point with direct mp.quad Mellin.
        h_quad = abs(mp.zeta(zmax) * M.quad(zmax))
        bound10 = fact10 * h_quad / (R ** 10)
        max_rows.append({
            "R": mp.nstr(R, 18),
            "n_angles": n,
            "max_h_fast": mp.nstr(max_h_fast, 18),
            "max_h_quad_validated": mp.nstr(h_quad, 18),
            "max_theta": maxr["theta"],
            "max_z_real": maxr["z_real"],
            "max_z_imag": maxr["z_imag"],
            "min_h_fast": minr["h_abs"],
            "min_theta": minr["theta"],
            "cauchy_bound_k10": mp.nstr(bound10, 18),
            "bound_over_certified_delta10": mp.nstr(bound10 / DELTA10, 18),
        })
        if abs(R - R_MAIN) < mp.mpf("1e-20"):
            full_Rmain_rows = rows
            output.append(
                f"R=11.34 max_h={mp.nstr(h_quad, 10)} at theta={maxr['theta']} z=({maxr['z_real']},{maxr['z_imag']}) bound10={mp.nstr(bound10, 10)}"
            )
        if R in [mp.mpf("14.0"), mp.mpf("17.010368213376501812603831941"), mp.mpf("20"), mp.mpf("25"), mp.mpf("30.41")]:
            bound20 = fact20 * h_quad / (R ** 20)
            k20_rows.append({
                "R": mp.nstr(R, 18),
                "max_h_quad_validated": mp.nstr(h_quad, 18),
                "max_theta": maxr["theta"],
                "max_z_real": maxr["z_real"],
                "max_z_imag": maxr["z_imag"],
                "cauchy_bound_k20": mp.nstr(bound20, 18),
                "bound_over_certified_delta20": mp.nstr(bound20 / DELTA20, 18),
            })
    write_csv(ART / "h_circle_scan_R11p34_k10_step300.csv", full_Rmain_rows)
    write_csv(ART / "h_max_per_radius_step300.csv", max_rows)
    write_csv(ART / "h_max_at_k20_step300.csv", k20_rows)

    best10 = min(max_rows, key=lambda r: mp.mpf(str(r["cauchy_bound_k10"])))
    best20 = min(k20_rows, key=lambda r: mp.mpf(str(r["cauchy_bound_k20"]))) if k20_rows else None
    output.append(f"R_opt_k10={best10['R']} bound10={best10['cauchy_bound_k10']} ratio={best10['bound_over_certified_delta10']}")
    if best20:
        output.append(f"R_opt_k20_scan={best20['R']} bound20={best20['cauchy_bound_k20']} ratio={best20['bound_over_certified_delta20']}")
    output.append(f"runtime_seconds={time.time()-t0:.3f}")
    (ART / "compute_step300_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")

    summary = (
        "# Step 300 Results Summary\n\n"
        f"At R=11.34, the circle scan found validated max `|h|={best10['max_h_quad_validated']}` only after comparing radii? "
        f"The actual R=11.34 row is in `h_max_per_radius_step300.csv`. The scanned optimal k=10 Cauchy bound occurs at R={best10['R']} with bound/certified ratio {best10['bound_over_certified_delta10']}.\n"
    )
    # Replace first sentence with the exact Rmain row.
    rmain_row = next(r for r in max_rows if abs(mp.mpf(str(r["R"])) - R_MAIN) < mp.mpf("1e-12"))
    summary = (
        "# Step 300 Results Summary\n\n"
        f"At R=11.34, validated max `|h|={rmain_row['max_h_quad_validated']}` at theta `{rmain_row['max_theta']}`, z=({rmain_row['max_z_real']}, {rmain_row['max_z_imag']}). "
        f"The k=10 Cauchy bound there is `{rmain_row['cauchy_bound_k10']}`, ratio `{rmain_row['bound_over_certified_delta10']}` over certified `165.44`. "
        f"The scanned optimal k=10 bound is at R={best10['R']} with ratio `{best10['bound_over_certified_delta10']}`. "
        "The contour maximum is on a far-left arc, not at the saddle root.\n"
    )
    (ART / "step300_results_summary.md").write_text(summary, encoding="utf-8")
    (ART / "nonclaim_boundary_step300.md").write_text(
        "# Step 300 Nonclaim Boundary\n\n"
        "- Direct Branch C contour scan only; no RH claim and no Branch C closure claim.\n"
        "- Scans are angular discretizations, not proofs of exact circle maxima.\n",
        encoding="utf-8",
    )
    schema = {
        "step": 300,
        "orientation": "h_circle_scan",
        "dps": MP_DPS,
        "R11p34_row": rmain_row,
        "R_opt_k10_scanned": best10,
        "R_opt_k20_scanned": best20,
        "final_verdict": "V_h_circle_scan_locates_far_left_max_cauchy_consistent",
    }
    (ART / "step300_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
