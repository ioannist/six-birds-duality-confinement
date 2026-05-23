#!/usr/bin/env python3
"""Compute zeta derivatives at the first two non-trivial zeros."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step252_branch_C_zeta_derivative_artifacts")
MP_DPS = 80
K_MAX = 4


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    mp.mp.dps = MP_DPS
    rows: list[dict[str, str]] = []
    payload = {"mpmath_dps": MP_DPS, "derivatives": []}
    for idx in [1, 2]:
        rho = mp.zetazero(idx)
        for k in range(K_MAX + 1):
            val = mp.zeta(rho, derivative=k)
            row = {
                "rho_index": str(idx),
                "rho": mp.nstr(rho, 40),
                "k": str(k),
                "zeta_derivative_real": mp.nstr(mp.re(val), 30),
                "zeta_derivative_imag": mp.nstr(mp.im(val), 30),
                "zeta_derivative_abs": mp.nstr(abs(val), 30),
            }
            rows.append(row)
            payload["derivatives"].append(row)
    write_csv(ART / "zeta_derivatives_step252.csv", [
        "rho_index",
        "rho",
        "k",
        "zeta_derivative_real",
        "zeta_derivative_imag",
        "zeta_derivative_abs",
    ], rows)
    (ART / "zeta_derivatives_step252.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(
            "rho={rho_index} k={k} |zeta^{k}|={zeta_derivative_abs} zeta={zeta_derivative_real} + {zeta_derivative_imag}i".format(**row)
        )


if __name__ == "__main__":
    main()
