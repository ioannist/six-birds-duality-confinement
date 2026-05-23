#!/usr/bin/env python3
"""Step 298: locate z*(k) for h(z)=zeta(z) M(G_star)(z)."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step298_saddle_zeta_M_G_bound_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP271_SADDLE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step271_branch_C_saddle_numerics_artifacts/saddle_z_star_step271.csv")

MP_DPS = 80
K_VALUES = [10, 20, 30, 50]


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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_complex_pair(s: str) -> mp.mpc:
    c = complex(s.replace("+-", "-"))
    return mp.mpc(mp.mpf(str(c.real)), mp.mpf(str(c.imag)))


class MellinG:
    def __init__(self, step292):
        self.gen = step292.GENERATORS["G_star"]
        self.step292 = step292
        self.centers, self.epsilons, self.coeffs = step292.moment_coefficients(self.gen)

    def deriv(self, z: mp.mpc, n: int) -> mp.mpc:
        total = mp.mpc(0)
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t, cc=c, ee=eps, aa=coeff, nn=n):
                return aa * self.step292.beta_bump((t - cc) / ee) * (t ** (z - 1)) * (mp.log(t) ** nn)

            total += mp.quad(integrand, [lo, hi])
        return total


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step298", STEP196_SCRIPT)
    step292 = load_module("step292_for_step298", STEP292_SCRIPT)
    rho = mp.mpc(mp.mpf("0.5"), mp.mpf(str(step196.ZEROS[1])))
    mg = MellinG(step292)

    prior = {}
    for row in read_csv(STEP271_SADDLE):
        if row["triple_id"] == "rho1_G_star":
            prior[int(row["k"])] = parse_complex_pair(row["z_star"].replace(" ", ""))

    def logh_prime(z: mp.mpc) -> mp.mpc:
        zeta0 = mp.zeta(z)
        zeta1 = mp.zeta(z, derivative=1)
        M0 = mg.deriv(z, 0)
        M1 = mg.deriv(z, 1)
        return zeta1 / zeta0 + M1 / M0

    def equation(z: mp.mpc, k: int) -> mp.mpc:
        return logh_prime(z) - (k + 1) / (z - rho)

    rows = []
    z_prev = prior[20]
    for k in K_VALUES:
        if k in prior:
            start = prior[k]
        else:
            # Linear extrapolation from Step271 k=10,20 left-half-plane escape.
            z10, z20 = prior[10], prior[20]
            start = z20 + (k - 20) * (z20 - z10) / 10
        try:
            root = mp.findroot(lambda zz: equation(zz, k), (start, start * mp.mpf("1.001") + mp.mpc("0.01", "0.01")), tol=mp.mpf("1e-40"), maxsteps=50)
            status = "findroot"
        except Exception:
            root = start
            status = "fallback_start"
        d = root - rho
        rows.append({
            "k": k,
            "z_star_real": mp.nstr(mp.re(root), 30),
            "z_star_imag": mp.nstr(mp.im(root), 30),
            "z_star": f"{mp.nstr(mp.re(root), 30)}{mp.nstr(mp.im(root), 30, min_fixed=0, max_fixed=0, strip_zeros=False, show_zero_exponent=True) if mp.im(root) < 0 else '+' + mp.nstr(mp.im(root), 30, min_fixed=0, max_fixed=0, strip_zeros=False, show_zero_exponent=True)}j",
            "abs_z_minus_rho": mp.nstr(abs(d), 30),
            "arg_z_minus_rho": mp.nstr(mp.arg(d), 30),
            "residual_abs": mp.nstr(abs(equation(root, k)), 12),
            "status": status,
        })
        z_prev = root

    write_csv(ART / "saddle_locations_step298.csv", rows)
    print("wrote saddle_locations_step298.csv")


if __name__ == "__main__":
    main()
