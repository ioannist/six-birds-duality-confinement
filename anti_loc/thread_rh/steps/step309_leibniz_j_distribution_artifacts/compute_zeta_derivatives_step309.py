#!/usr/bin/env python3
"""Step 309: zeta derivatives at rho_1."""

from __future__ import annotations

import csv
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step309_leibniz_j_distribution_artifacts")
DPS = 80
MAX_J = 50
RHO1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def sign_label(x: mp.mpf) -> str:
    if x > 0:
        return "+"
    if x < 0:
        return "-"
    return "0"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    rows = []
    for j in range(MAX_J + 1):
        val = mp.zeta(RHO1, derivative=j)
        rows.append({
            "j": j,
            "zeta_derivative_complex": cstr(val, 34),
            "zeta_derivative_abs": mp.nstr(abs(val), 34),
            "arg": mp.nstr(mp.arg(val), 34),
            "real_sign": sign_label(mp.re(val)),
            "imag_sign": sign_label(mp.im(val)),
        })
    with (ART / "zeta_derivatives_at_rho1_step309.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Step309 zeta derivatives written: {len(rows)}")


if __name__ == "__main__":
    main()
