#!/usr/bin/env python3
"""Step 296: stable analytical I_k via Fourier/spectral integral."""

from __future__ import annotations

import csv
import importlib.util
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import simpson

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP295_INTEGRAND = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step295_I_k_saddle_asymptotic_artifacts/I_k_integrand_step295.md")

MP_DPS = 80
K_CROSS = list(range(13))
K_TARGETS = [10, 15, 20, 30, 50]
RHO_INDEX = 1
G_ID = "G_star"


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


def cfmt(z: complex) -> str:
    return f"{z.real:+.16e}{z.imag:+.16e}j"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    _ = STEP295_INTEGRAND.read_text(encoding="utf-8")
    step196 = load_module("step196_for_step296_analytical", STEP196_SCRIPT)
    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    spec = step196.GENERATORS[G_ID]
    moments = step196.compute_moments(spec)
    G_primary, _, _quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
    F = zeta_grid * G_primary
    gamma = float(step196.ZEROS[RHO_INDEX])

    def H_float(t: float) -> complex:
        return complex(simpson(F * np.exp(-1j * t * u_grid), x=u_grid))

    def integrand_real(t_mp: mp.mpf, k: int) -> mp.mpf:
        t = float(t_mp)
        val = (t ** k) * np.exp(1j * t * gamma) * H_float(t) / (2.0 * np.pi)
        return mp.mpf(str(val.real))

    def integrand_imag(t_mp: mp.mpf, k: int) -> mp.mpf:
        t = float(t_mp)
        val = (t ** k) * np.exp(1j * t * gamma) * H_float(t) / (2.0 * np.pi)
        return mp.mpf(str(val.imag))

    rows = []
    output = [
        "Step296 analytical I_k computation",
        f"mpmath_dps={MP_DPS}",
        "I_k=(1/(2*pi))*int_{-1}^1 t^k exp(i*t*gamma) H(t) dt",
    ]
    for k in sorted(set(K_CROSS + K_TARGETS)):
        t0 = time.time()
        real = mp.quad(lambda tt, kk=k: integrand_real(tt, kk), [-1, 0, 1])
        imag = mp.quad(lambda tt, kk=k: integrand_imag(tt, kk), [-1, 0, 1])
        val = complex(float(real), float(imag))
        runtime = time.time() - t0
        rows.append({
            "k": k,
            "I_analytical_complex": cfmt(val),
            "I_analytical_abs": f"{abs(val):.16e}",
            "runtime_seconds": f"{runtime:.6f}",
            "method": "mpmath_quad_t_integral_with_grid_H",
        })
        output.append(f"k={k} |I_analytical|={abs(val):.12e} runtime={runtime:.3f}s")

    write_csv(ART / "I_k_analytical_values_step296.csv", rows)
    (ART / "compute_I_k_analytical_output_step296.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
