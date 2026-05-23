#!/usr/bin/env python3
"""Avenue B: analytical Burnol-kernel evaluation audit for Step 290.

This script deliberately distinguishes a Burnol-kernel E/K quadrature probe
from the full projected commutator c_ij entries.  The inherited artifacts do
not contain a closed formula for the full c-entry integral after the Step 173
P-operator, so the analytical avenue is recorded as blocked for c_ij even
though the Burnol kernel itself is probed with mpmath.quad at dps=200.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step290_branch_B_c_matrix_precision_artifacts"
STEP202_SCRIPT = ROOT / "anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def fmt(z: mp.mpf | mp.mpc, digits: int = 30) -> str:
    return mp.nstr(z, digits, min_fixed=0, max_fixed=0)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = 200
    step202 = load_module(STEP202_SCRIPT, "step202_quad_for_step290")
    data = step202.build_resolvent(120)
    rho1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))
    w = rho1

    def psi_diff_scalar(t: mp.mpf) -> mp.mpf:
        # The inherited Step202 resolvent is finite-dimensional/double-backed;
        # convert t to float for the same diagnostic convention.
        val = step202.psi_diff_at(np.array([float(t)]), data)[0]
        return mp.mpf(str(float(val)))

    t0 = time.perf_counter()
    try:
        integral = mp.quad(lambda tt: psi_diff_scalar(tt) * mp.power(tt, -w), [mp.mpf("0.5"), 1, 2, 5, 10, 20, 40])
        prefactor = mp.power(mp.pi, -w / 2) * mp.gamma(w / 2)
        e_probe = prefactor * (mp.power(mp.mpf("0.5"), mp.mpf("0.5") - w) + (mp.sqrt(mp.mpf("0.5")) / 2) * integral)
        probe_status = "mpmath_quad_probe_completed_dps200_finite_resolvent_diagnostic"
        probe_error = ""
    except Exception as exc:  # noqa: BLE001
        integral = mp.nan
        e_probe = mp.nan
        probe_status = "mpmath_quad_probe_failed"
        probe_error = f"{type(exc).__name__}: {exc}"
    seconds = time.perf_counter() - t0

    rows = []
    for candidate in ["CAND1", "CAND2"]:
        for i in range(1, 4):
            for j in range(1, 4):
                rows.append(
                    {
                        "candidate": candidate,
                        "i": i,
                        "j": j,
                        "analytical_c_real": "",
                        "analytical_c_imag": "",
                        "analytical_error_bound": "",
                        "status": "blocked_no_closed_projected_commutator_c_entry_formula_in_inherited_artifacts",
                        "burnol_kernel_probe_status": probe_status if (candidate, i, j) == ("CAND1", 1, 1) else "see_CAND1_1_1_probe",
                        "quad_dps": "200" if (candidate, i, j) == ("CAND1", 1, 1) else "",
                        "quad_seconds": f"{seconds:.6f}" if (candidate, i, j) == ("CAND1", 1, 1) else "",
                        "E_rho1_probe_real": fmt(mp.re(e_probe)) if (candidate, i, j) == ("CAND1", 1, 1) and probe_error == "" else "",
                        "E_rho1_probe_imag": fmt(mp.im(e_probe)) if (candidate, i, j) == ("CAND1", 1, 1) and probe_error == "" else "",
                        "probe_error": probe_error if (candidate, i, j) == ("CAND1", 1, 1) else "",
                        "reason": "Burnol K(z1,z2) is available, but Step208 c_ij also applies P, sinc convolution, PSWF truncation, and transport samples; no closed c_ij integral is preserved.",
                    }
                )

    with (ART / "c_matrix_entries_analytical_step290.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Append analytical avenue to uncertainty table if the grid script already created it.
    red_path = ART / "uncertainty_reduction_step290.csv"
    write_header = not red_path.exists()
    with red_path.open("a", newline="", encoding="utf-8") as f:
        fieldnames = [
            "avenue",
            "candidate",
            "i",
            "j",
            "before_error",
            "after_proxy_error",
            "reduction_factor",
            "target_10_orders_met",
            "dominant_remaining_source",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "avenue": "B_analytical_burnol_kernel",
                "candidate": "all",
                "i": "all",
                "j": "all",
                "before_error": "inherited_step208",
                "after_proxy_error": "not_available",
                "reduction_factor": "0",
                "target_10_orders_met": "False",
                "dominant_remaining_source": "missing closed formula for full projected c_ij entries, despite dps=200 Burnol-kernel quad probe",
            }
        )

    print("Step 290 analytical avenue")
    print(f"probe_status={probe_status}")
    print(f"probe_seconds={seconds:.3f}")
    print("full_c_matrix_status=blocked_no_closed_projected_commutator_formula")


if __name__ == "__main__":
    main()
