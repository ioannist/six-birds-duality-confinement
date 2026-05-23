#!/usr/bin/env python3
"""Assemble the Step 203 corrected finite Gram matrix."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step203_diagonal_gram_correction_artifacts")
STEP202 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts")
MP_DPS = 70


def read_diag() -> dict[int, dict[str, mp.mpf | str]]:
    out: dict[int, dict[str, mp.mpf | str]] = {}
    with (BASE / "G_diagonal_corrected_step203.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            idx = int(row["rho_index"])
            out[idx] = {
                "value": mp.mpf(row["G_chosen"]),
                "error": mp.mpf(row["error_bound"]),
                "sign": row["sign_choice"],
                "status": row["status"],
            }
    return out


def read_step202_offdiag() -> dict[tuple[int, int], dict[str, mp.mpc | mp.mpf | str]]:
    out = {}
    with (STEP202 / "G_matrix_step202.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            i = int(row["i"])
            j = int(row["j"])
            out[(i, j)] = {
                "value": mp.mpc(mp.mpf(row["G_real"]), mp.mpf(row["G_imag"])),
                "error": mp.mpf(row["error_bound"]),
                "status": row["status"],
            }
    return out


def main() -> None:
    mp.mp.dps = MP_DPS
    diag = read_diag()
    off = read_step202_offdiag()
    rows = []
    matrix_payload = []
    for i in range(1, 4):
        payload_row = []
        for j in range(1, 4):
            if i == j:
                val = mp.mpc(diag[i]["value"], 0)
                err = diag[i]["error"]
                source = "LHopital diagonal K(conj(rho_i),rho_i)=2Re(conj(E)Eprime)"
                status = "diagonal_corrected_but_error_dominant"
            else:
                val = off[(i, j)]["value"]
                err = off[(i, j)]["error"]
                source = "Step 202 off-diagonal Burnol 2002 equation 1"
                status = "off_diagonal_reused"
            row = {
                "i": i,
                "j": j,
                "G_real": mp.nstr(mp.re(val), 30),
                "G_imag": mp.nstr(mp.im(val), 30),
                "G_abs": mp.nstr(abs(val), 30),
                "error_bound": mp.nstr(err, 30),
                "status": status,
                "source": source,
            }
            rows.append(row)
            payload_row.append(row)
        matrix_payload.append(payload_row)

    with (BASE / "G_matrix_full_step203.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "G_matrix_full_step203.json").write_text(json.dumps(matrix_payload, indent=2) + "\n", encoding="utf-8")
    print("Step 203 corrected Gram matrix assembled")
    for i in range(1, 4):
        print(f"G[{i},{i}]={mp.nstr(diag[i]['value'], 12)} err<={mp.nstr(diag[i]['error'], 8)} sign={diag[i]['sign']}")


if __name__ == "__main__":
    main()
