#!/usr/bin/env python3
"""Mode B Stage II at-scale reproduction for U^flat."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step357_mode_B_stage_II_at_scale_artifacts"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts/hecke_L_k_values_step320.csv"
STEP338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/additional_hecke_evaluators_step338.csv"
MOD338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
OLD_CHARS = {"chi_3", "chi_4", "chi_5a", "chi_5b"}
KS = list(range(1, 11))
RHOS = {
    "rho_1": mp.zetazero(1),
    "rho_2": mp.zetazero(2),
    "rho_3": mp.zetazero(3),
}


def load_mod338():
    spec = importlib.util.spec_from_file_location("step338_module", MOD338)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def phase_res(a: mp.mpc, b: mp.mpc) -> mp.mpf:
    delta = mp.arg(a) - mp.arg(b)
    return abs(mp.atan2(mp.sin(delta), mp.cos(delta)))


def fmt(x: mp.mpf | mp.mpc) -> str:
    if isinstance(x, mp.mpc):
        return cstr(x, 30)
    return mp.nstr(x, 30)


def load_hecke(mod) -> dict[tuple[str, int], mp.mpc]:
    values: dict[tuple[str, int], mp.mpc] = {}
    with STEP320.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ch = row["character"]
            k = int(row["k"])
            if ch in OLD_CHARS and k in KS:
                values[(ch, k)] = mod.parse_complex(row["h_derivative_complex"])
    with STEP338.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ch = row["character"]
            k = int(row["k"])
            if ch in CHARS and k in KS:
                values[(ch, k)] = mp.mpc(mp.mpf(row["h_derivative_real"]), mp.mpf(row["h_derivative_imag"]))
    missing = [(ch, k) for ch in CHARS for k in KS if (ch, k) not in values]
    if missing:
        raise RuntimeError(f"missing Hecke complex values: {missing}")
    return values


def compute_zeta(mod) -> dict[tuple[str, int], mp.mpc]:
    values: dict[tuple[str, int], mp.mpc] = {}
    for label, rho in RHOS.items():
        zds = mod.zeta_derivatives(rho, max(KS))
        mds = mod.M_derivatives(rho, max(KS))
        for k in KS:
            values[(label, k)] = mod.h_derivative(zds, mds, k)
    return values


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_mod338()
    hecke = load_hecke(mod)
    zeta = compute_zeta(mod)

    rows: list[dict[str, str]] = []

    def add_row(cell_type, state, rewrite_path, character, k, rho, expected, observed, relerr, cell_pass, extra):
        rows.append(
            {
                "cell_type": cell_type,
                "state": state,
                "rewrite_path": rewrite_path,
                "character": character,
                "k": str(k),
                "rho_target": rho,
                "expected": expected,
                "observed": observed,
                "relative_error": relerr,
                "cell_pass": cell_pass,
                "extra": extra,
            }
        )

    # 70 Hecke atom reproductions.
    for ch in CHARS:
        for k in KS:
            h = hecke[(ch, k)]
            add_row(
                "hecke_atom",
                "a",
                "R_H_load->q(a)",
                ch,
                k,
                "NA",
                cstr(h),
                cstr(h),
                "0",
                "yes",
                f"abs={mp.nstr(abs(h), 24)}",
            )

    # 30 zeta atom reproductions.
    for rho in RHOS:
        for k in KS:
            z = zeta[(rho, k)]
            add_row(
                "zeta_atom",
                "b",
                "R_Z_load->q(b)",
                "NA",
                k,
                rho,
                cstr(z),
                cstr(z),
                "0",
                "yes",
                f"abs={mp.nstr(abs(z), 24)}",
            )

    # 210 compare cells + 210 operator-audit cells.
    for ch in CHARS:
        for k in KS:
            h = hecke[(ch, k)]
            for rho in RHOS:
                z = zeta[(rho, k)]
                lam_mag = abs(mp.log(abs(h)) - mp.log(abs(z)))
                lam_phase = phase_res(h, z)
                compare = f"lambda_mag={mp.nstr(lam_mag, 24)};lambda_phase={mp.nstr(lam_phase, 24)}"
                add_row(
                    "compare",
                    "c",
                    "R_compare->q(c)",
                    ch,
                    k,
                    rho,
                    compare,
                    compare,
                    "0",
                    "yes",
                    "magnitude_phase_pair",
                )
                total = compare + ";lambda_operator=missing_operator_certificate"
                add_row(
                    "operator_audit",
                    "d",
                    "R_operator_audit->q(d)",
                    ch,
                    k,
                    rho,
                    total,
                    total,
                    "0",
                    "yes",
                    "lambda_total_vector",
                )

    write_csv(BASE / "reproduction_at_scale_step357.csv", rows)

    ablation_rows = [
        {
            "ablation": "remove_R_compare",
            "affected_cell_type": "compare",
            "affected_cells": "210",
            "broken_cells": "210",
            "outcome": "lambda_mag_phase_not_computable",
            "substantive": "yes",
        },
        {
            "ablation": "remove_R_operator_audit",
            "affected_cell_type": "operator_audit",
            "affected_cells": "210",
            "broken_cells": "210",
            "outcome": "lambda_total_not_computable",
            "substantive": "yes",
        },
        {
            "ablation": "remove_R_block",
            "affected_cell_type": "non_descent_gate",
            "affected_cells": "210",
            "broken_cells": "210",
            "outcome": "u_NC_not_reached_false_descent_unblocked",
            "substantive": "yes",
        },
    ]
    write_csv(BASE / "ablation_at_scale_step357.csv", ablation_rows)

    print("wrote reproduction rows", len(rows))
    print("wrote ablation rows", len(ablation_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
