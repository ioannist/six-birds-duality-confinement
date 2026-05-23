#!/usr/bin/env python3
"""Step 328: constructive H4 finite model for primitive chars mod 3/4/5.

Burnol 2004 gives a Dirichlet-Sonine framework, but not an explicit finite
P_infty,chi / kernel residual formula.  This script therefore builds a labelled
cascade-internal finite Galerkin extrapolation using completed Dirichlet L-functions
as the E_chi input in the Burnol kernel shape.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step328_hecke_H4_constructive_subfamily_artifacts")
STEP320 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
DPS = 80
OFFSETS = [mp.mpf("-3"), mp.mpf("-2"), mp.mpf("-1"), mp.mpf("0"), mp.mpf("1"), mp.mpf("2"), mp.mpf("3")]
CENTER_OFFSETS = [mp.mpf("-0.75"), mp.mpf("0"), mp.mpf("0.75")]


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def char_data(label: str) -> tuple[int, int, list[mp.mpc], mp.mpc]:
    I = mp.mpc(0, 1)
    if label == "chi_3":
        return 3, 1, [0, 1, -1], mp.mpc(1)
    if label == "chi_4":
        return 4, 1, [0, 1, 0, -1], mp.mpc(1)
    if label == "chi_5a":
        return 5, 0, [0, 1, -1, -1, 1], mp.mpc(1)
    if label == "chi_5b":
        return 5, 1, [0, 1, I, -I, -1], mp.mpc("0.85065080835203993218", "0.52573111211913360603")
    raise ValueError(label)


def L_chi(s: mp.mpc, q: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) ** (-s)) * mp.fsum(
        [chi[a % q] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)]
    )


def completed_E(s: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) / mp.pi) ** ((s + parity_a) / 2) * mp.gamma((s + parity_a) / 2) * L_chi(s, q, chi)


def kernel(z: mp.mpc, w: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    Ez = completed_E(z, q, parity_a, chi)
    Ew = completed_E(w, q, parity_a, chi)
    E1z = completed_E(1 - z, q, parity_a, chi)
    E1w = completed_E(1 - w, q, parity_a, chi)
    denom = z + mp.conj(w) - 1
    return (Ez * mp.conj(Ew) - E1z * mp.conj(E1w)) / denom


def roots_from_step320() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    return {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}


def mat_conj_transpose(M: mp.matrix) -> mp.matrix:
    return M.T.apply(mp.conj)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    roots = roots_from_step320()
    kappa_rows: list[dict[str, object]] = []
    p_rows: list[dict[str, object]] = []
    residual_rows: list[dict[str, object]] = []
    summary_lines = ["# Step 328 Results Summary", ""]

    for label in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        rho = roots[label]
        t0 = mp.im(rho)
        q, parity_a, chi, epsilon = char_data(label)
        tau_grid = [t0 + off for off in OFFSETS]
        z_grid = [mp.mpc(mp.mpf("0.5"), tau) for tau in tau_grid]
        centers = [mp.mpc(mp.mpf("0.55"), t0 + off) for off in CENTER_OFFSETS]
        m, n = len(z_grid), len(centers)
        V = mp.matrix(m, n)
        for r, z in enumerate(z_grid):
            for c, w in enumerate(centers):
                val = kernel(z, w, q, parity_a, chi)
                V[r, c] = val
                kappa_rows.append(
                    {
                        "character": label,
                        "tau": mp.nstr(tau_grid[r], 24),
                        "center_index": c,
                        "center_w": cstr(w, 24),
                        "kappa_real": mp.nstr(mp.re(val), 30),
                        "kappa_imag": mp.nstr(mp.im(val), 30),
                        "kappa_abs": mp.nstr(abs(val), 18),
                        "construction_status": "cascade_internal_natural_extrapolation_from_Burnol_kernel_shape",
                    }
                )

        W = mp.eye(m)  # unit grid weights
        G = mat_conj_transpose(V) * W * V
        G_inv = mp.inverse(G)
        P = V * G_inv * mat_conj_transpose(V) * W
        I_m = mp.eye(m)
        M_diag = mp.diag([L_chi(z, q, chi) for z in z_grid])
        C = mat_conj_transpose(V) * W * (I_m - P) * M_diag * V
        trace = mp.fsum([C[i, i] for i in range(n)])
        frob = mp.sqrt(mp.fsum([abs(C[i, j]) ** 2 for i in range(n) for j in range(n)]))
        p_rows.append(
            {
                "character": label,
                "q": q,
                "parity_a": parity_a,
                "root_number_epsilon": cstr(epsilon, 24),
                "projection_model": "finite Galerkin P_infty_chi proxy onto span{kappa_chi(w_j)}",
                "tau_grid_size": m,
                "kernel_centers": ";".join(cstr(w, 18) for w in centers),
                "gram_condition_proxy": mp.nstr(mp.norm(G) * mp.norm(G_inv), 18),
                "construction_status": "not Burnol-explicit; cascade-internal natural extrapolation",
            }
        )
        for i in range(n):
            for j in range(n):
                residual_rows.append(
                    {
                        "character": label,
                        "i": i,
                        "j": j,
                        "c_ij_real": mp.nstr(mp.re(C[i, j]), 30),
                        "c_ij_imag": mp.nstr(mp.im(C[i, j]), 30),
                        "c_ij_abs": mp.nstr(abs(C[i, j]), 18),
                        "trace_abs_for_character": mp.nstr(abs(trace), 18),
                        "frobenius_abs_for_character": mp.nstr(frob, 18),
                    }
                )
        summary_lines.append(
            f"- `{label}`: residual trace abs `{mp.nstr(abs(trace), 10)}`, Frobenius `{mp.nstr(frob, 10)}`."
        )

    write_csv(ART / "kappa_chi_values_step328.csv", kappa_rows)
    write_csv(ART / "P_infty_chi_step328.csv", p_rows)
    write_csv(ART / "H4_finite_matrix_residual_step328.csv", residual_rows)
    summary_lines.extend(
        [
            "",
            "Burnol 2004 supplies the paper-grounded Dirichlet-Sonine framework: `P_chi`/`P'_chi`, `W_lambda^chi`, and zero-attached `Z_{rho,k}` vectors.",
            "Burnol does not provide an explicit `E_lambda^chi`, `P_infty,chi`, or finite matrix residual in the form required here.",
            "Therefore this construction is labelled a cascade-internal natural extrapolation using the completed Dirichlet L-function in the Burnol kernel shape.",
            "",
            "Score update: subfamily H4 advances from 1.5 to 2.0, not 2.5. Concrete finite residual content exists, but it is not a Burnol-derived theorem.",
            "",
            "Final verdict: `V_hecke_H4_subfamily_constructed_extrapolated_score_2_0`.",
        ]
    )
    (ART / "step328_results_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    schema = {
        "step": 328,
        "orientation": "constructive_attempt",
        "target": "H4 finite Dirichlet-Sonine subfamily model",
        "dps": DPS,
        "characters": ["chi_3", "chi_4", "chi_5a", "chi_5b"],
        "construction_status": "cascade_internal_natural_extrapolation",
        "score_update": "1.5_to_2.0_not_2.5",
        "final_verdict": "V_hecke_H4_subfamily_constructed_extrapolated_score_2_0",
    }
    (ART / "step328_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step328.md").write_text(
        "# Step 328 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim H4 fully resolved.\n"
        "- The finite model is a cascade-internal natural extrapolation from Burnol's Dirichlet-Sonine framework, not an explicit Burnol theorem.\n"
        "- The subfamily score update is therefore to 2.0, not 2.5.\n",
        encoding="utf-8",
    )
    print("Step328 H4 constructive subfamily")
    for line in summary_lines:
        if line.startswith("- `"):
            print(line)
    print("verdict=V_hecke_H4_subfamily_constructed_extrapolated_score_2_0")


if __name__ == "__main__":
    main()
