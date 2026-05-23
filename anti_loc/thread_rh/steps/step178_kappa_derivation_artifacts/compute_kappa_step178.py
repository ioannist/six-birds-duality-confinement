#!/usr/bin/env python3
"""Step 178 kappa derivation numerical status script.

No numerical kappa values are lawfully computed because the inherited records
do not provide the projected Sonine reproducing kernel K_a^Gamma or the
equivalent Mellin-line vector kappa_{a,w}=T_a^*K_a^Gamma(.,w).

The script records the requested sample tau grid and c_11(log 2) attempt as
blocked at the specific classical theorem gap.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step178_kappa_derivation_artifacts"
)

TAUS = [-14.134725141734693, -5.0, -1.0, 0.0, 1.0, 5.0, 14.134725141734693]
GAP = (
    "Burnol explicit Bessel/Hankel resolvent formula for the orthogonal "
    "projection P_{L_a^Gamma}, equivalently the reproducing kernel "
    "K_a^Gamma=P_{L_a^Gamma}K_a^{Gamma,amb}, for the extended Sonine "
    "space L_a at a=1/2"
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    sample_rows = [
        {
            "a": "1/2",
            "w": "rho_1=1/2+14.134725141734693i",
            "tau": f"{tau:.16e}",
            "kappa_real": "NA",
            "kappa_imag": "NA",
            "status": "not_computed_classical_projection_theorem_needed",
            "gap": GAP,
        }
        for tau in TAUS
    ]
    write_csv(
        ROOT / "kappa_sample_values_step178.csv",
        sample_rows,
        ["a", "w", "tau", "kappa_real", "kappa_imag", "status", "gap"],
    )

    c_row = {
        "i": 1,
        "j": 1,
        "ell": f"{math.log(2.0):.16e}",
        "c_real": "NA",
        "c_imag": "NA",
        "c_abs": "NA",
        "error_bound": "NA",
        "status": "not_attempted_kappa_unavailable",
        "gap": GAP,
    }
    write_csv(
        ROOT / "c_ij_attempt_step178.csv",
        [c_row],
        ["i", "j", "ell", "c_real", "c_imag", "c_abs", "error_bound", "status", "gap"],
    )

    status = {
        "target": "kappa_{1/2,rho_1}(tau)",
        "tau_samples": TAUS,
        "status": "blocked_before_numeric_evaluation",
        "gap": GAP,
        "reason": (
            "Step153 supplies K_a^Gamma only as P_{L_a^Gamma}K_a^{Gamma,amb}; "
            "using the ambient kernel would violate the public-shadow boundary."
        ),
    }
    (ROOT / "compute_kappa_status_step178.json").write_text(json.dumps(status, indent=2), encoding="utf-8")

    print("Step 178 kappa derivation numerical status")
    print("target=kappa_{1/2,rho_1}(tau)")
    print("status=blocked_before_numeric_evaluation")
    print(f"gap={GAP}")
    print("sample_tau_count=7")
    print("c_11_log2_status=not_attempted_kappa_unavailable")


if __name__ == "__main__":
    main()
