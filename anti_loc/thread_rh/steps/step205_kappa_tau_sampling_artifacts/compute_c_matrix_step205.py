#!/usr/bin/env python3
"""Step 205 c_ij attempt.

Because the sampled values are only candidate boundary kernels and not certified
T_a^*K samples, this script does not compute a certified c-matrix.  It records
the formal integral and the blocker.
"""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step205_kappa_tau_sampling_artifacts")


def main() -> None:
    rows = []
    for i in range(1, 4):
        for j in range(1, 4):
            rows.append({
                "i": i,
                "j": j,
                "ell": "log(2)",
                "c_real": "",
                "c_imag": "",
                "c_abs": "",
                "error_bound": "not_certified",
                "status": "not_evaluated_certified",
                "reason": "kappa_tau samples are candidate K-boundary values, not certified T_a^*K samples; using them in K_infty^op would be an ambient-shadow substitution",
                "formula": "int conj(kappa_i(tau))[(I-P_infty)M_m P_infty kappa_j](tau)d tau/(2pi)",
            })
    with (BASE / "c_matrix_step205.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("Step 205 c_matrix")
    print("not_evaluated_certified: kappa_tau formula not verified as T_a^*K")


if __name__ == "__main__":
    main()
