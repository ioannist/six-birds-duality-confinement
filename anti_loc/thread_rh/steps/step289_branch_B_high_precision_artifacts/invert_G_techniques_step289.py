#!/usr/bin/env python3
"""High-precision Branch B G^{-1} attack for Step 289."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step289_branch_B_high_precision_artifacts"
STEP208 = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"


def fmt(x: mp.mpf | mp.mpc, digits: int = 40) -> str:
    return mp.nstr(x, digits, min_fixed=0, max_fixed=0)


def read_matrix(path: Path, real_col: str, imag_col: str, n: int = 3) -> mp.matrix:
    m = mp.matrix(n, n)
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            i = int(row["i"]) - 1
            j = int(row["j"]) - 1
            m[i, j] = mp.mpc(mp.mpf(row[real_col]), mp.mpf(row[imag_col]))
    return m


def read_error(path: Path, n: int = 3) -> mp.matrix:
    m = mp.matrix(n, n)
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            i = int(row["i"]) - 1
            j = int(row["j"]) - 1
            m[i, j] = mp.mpf(row["error_bound"])
    return m


def dagger(m: mp.matrix) -> mp.matrix:
    out = mp.matrix(m.cols, m.rows)
    for i in range(m.rows):
        for j in range(m.cols):
            out[j, i] = mp.conj(m[i, j])
    return out


def fro_norm(m: mp.matrix) -> mp.mpf:
    s = mp.mpf("0")
    for i in range(m.rows):
        for j in range(m.cols):
            s += abs(m[i, j]) ** 2
    return mp.sqrt(s)


def trace(m: mp.matrix) -> mp.mpc:
    return sum(m[i, i] for i in range(min(m.rows, m.cols)))


def xi_value(g_inv: mp.matrix, c: mp.matrix) -> mp.mpc:
    return trace(g_inv * dagger(c) * g_inv * c)


def xi_error(g_inv: mp.matrix, c: mp.matrix, cerr: mp.matrix) -> mp.mpf:
    gi = fro_norm(g_inv)
    cn = fro_norm(c)
    en = fro_norm(cerr)
    return gi**2 * (2 * cn * en + en**2)


def singular_values_real(g: mp.matrix) -> list[mp.mpf]:
    # The preserved G has zero imaginary parts. Use A=G^T G as a real
    # symmetric matrix to avoid complex-ordering issues in eigsy.
    gr = mp.matrix(g.rows, g.cols)
    for i in range(g.rows):
        for j in range(g.cols):
            gr[i, j] = mp.re(g[i, j])
    a = gr.T * gr
    vals, _ = mp.eigsy(a)
    return [mp.sqrt(max(mp.mpf("0"), v)) for v in vals]


def identity(n: int) -> mp.matrix:
    m = mp.matrix(n, n)
    for i in range(n):
        m[i, i] = 1
    return m


def inverse_lu(g: mp.matrix) -> mp.matrix:
    n = g.rows
    inv = mp.matrix(n, n)
    eye = identity(n)
    for j in range(n):
        col = mp.lu_solve(g, eye[:, j])
        for i in range(n):
            inv[i, j] = col[i]
    return inv


def inverse_svd(g: mp.matrix, threshold: mp.mpf) -> tuple[mp.matrix, int]:
    u, s, v = mp.svd(g)
    sinv = mp.matrix(len(s), len(s))
    kept = 0
    for i, val in enumerate(s):
        if val > threshold:
            sinv[i, i] = 1 / val
            kept += 1
    # mpmath returns A = U * diag(s) * V, not V^H.
    return v.T * sinv * u.T, kept


def inverse_newton_refine(g: mp.matrix, start_dps: int, final_dps: int, iterations: int = 8) -> mp.matrix:
    old = mp.mp.dps
    try:
        mp.mp.dps = start_dps
        g0 = +g
        x = g0 ** -1
        mp.mp.dps = final_dps
        x = +x
        gf = +g
        eye = identity(g.rows)
        for _ in range(iterations):
            x = x * (2 * eye - gf * x)
        return x
    finally:
        mp.mp.dps = old


def compute_condition_rows() -> list[dict[str, str]]:
    rows = []
    for dps in [80, 200, 500, 1000]:
        mp.mp.dps = dps
        g = read_matrix(STEP208 / "G_matrix_step208.csv", "G_real", "G_imag")
        t0 = time.perf_counter()
        s = singular_values_real(g)
        elapsed = time.perf_counter() - t0
        rows.append(
            {
                "dps": str(dps),
                "sigma_min": fmt(s[0]),
                "sigma_mid": fmt(s[1]),
                "sigma_max": fmt(s[-1]),
                "condition_number": fmt(s[-1] / s[0]),
                "det_G": fmt(mp.det(g)),
                "fro_norm_G_inv": fmt(fro_norm(g ** -1)),
                "compute_seconds": f"{elapsed:.6f}",
                "status": "stable_from_preserved_decimal_G",
            }
        )
    return rows


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    condition_rows = compute_condition_rows()
    with (ART / "condition_number_vs_dps_step289.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(condition_rows[0].keys()))
        writer.writeheader()
        writer.writerows(condition_rows)

    mp.mp.dps = 500
    g = read_matrix(STEP208 / "G_matrix_step208.csv", "G_real", "G_imag")
    c_by = {
        "CAND1": read_matrix(STEP208 / "c_matrix_CAND1_step208.csv", "c_real", "c_imag"),
        "CAND2": read_matrix(STEP208 / "c_matrix_CAND2_step208.csv", "c_real", "c_imag"),
    }
    e_by = {
        "CAND1": read_error(STEP208 / "c_matrix_CAND1_step208.csv"),
        "CAND2": read_error(STEP208 / "c_matrix_CAND2_step208.csv"),
    }

    techniques: list[tuple[str, str, callable[[], tuple[mp.matrix | None, str]]]] = [
        ("direct_inverse", "G ** -1 at dps=500", lambda: (g ** -1, "ok")),
        ("lu_solve_columns", "mpmath.lu_solve per basis column at dps=500", lambda: (inverse_lu(g), "ok")),
        ("svd_pseudoinverse", "mpmath.svd pseudo-inverse threshold 1e-100", lambda: (*inverse_svd(g, mp.mpf("1e-100")),)[0:2]),
        ("tikhonov_lambda_1e-80", "(G + 1e-80 I)^-1", lambda: ((g + mp.mpf("1e-80") * identity(3)) ** -1, "ok")),
        ("tikhonov_lambda_1e-30", "(G + 1e-30 I)^-1", lambda: ((g + mp.mpf("1e-30") * identity(3)) ** -1, "ok")),
        ("newton_refinement", "80-dps inverse refined by Newton-Schulz at dps=500", lambda: (inverse_newton_refine(g, 80, 500), "ok")),
    ]

    rows = []
    values_for_stability: dict[str, list[tuple[str, mp.mpc, mp.mpf]]] = {"CAND1": [], "CAND2": []}
    for name, desc, maker in techniques:
        t0 = time.perf_counter()
        try:
            result = maker()
            g_inv = result[0]
            aux = result[1]
            if isinstance(aux, int):
                aux_status = f"kept_singular_values={aux}"
            else:
                aux_status = str(aux)
            status = "ok"
        except Exception as exc:  # noqa: BLE001
            g_inv = None
            aux_status = f"{type(exc).__name__}: {exc}"
            status = "failed"
        elapsed = time.perf_counter() - t0
        for cand in ["CAND1", "CAND2"]:
            if g_inv is None:
                rows.append(
                    {
                        "technique": name,
                        "description": desc,
                        "candidate": cand,
                        "dps": "500",
                        "time_seconds": f"{elapsed:.6f}",
                        "status": status,
                        "aux_status": aux_status,
                        "next_layer_value_real": "",
                        "next_layer_value_imag": "",
                        "next_layer_value_abs": "",
                        "error_bound": "",
                        "inverse_residual_fro": "",
                    }
                )
                continue
            val = xi_value(g_inv, c_by[cand])
            err = xi_error(g_inv, c_by[cand], e_by[cand])
            inv_resid = fro_norm(g * g_inv - identity(3))
            values_for_stability[cand].append((name, val, err))
            rows.append(
                {
                    "technique": name,
                    "description": desc,
                    "candidate": cand,
                    "dps": "500",
                    "time_seconds": f"{elapsed:.6f}",
                    "status": status,
                    "aux_status": aux_status,
                    "next_layer_value_real": fmt(mp.re(val)),
                    "next_layer_value_imag": fmt(mp.im(val)),
                    "next_layer_value_abs": fmt(abs(val)),
                    "error_bound": fmt(err),
                    "inverse_residual_fro": fmt(inv_resid),
                }
            )

    # Explicitly document requested techniques that are not available/applicable.
    for requested, reason in [
        ("qr_column_pivoting", "mpmath has no QR column-pivoting API available in this environment"),
        ("cholesky_regularized", "G is not Hermitian positive definite; Cholesky is not applicable to preserved G"),
    ]:
        for cand in ["CAND1", "CAND2"]:
            rows.append(
                {
                    "technique": requested,
                    "description": reason,
                    "candidate": cand,
                    "dps": "500",
                    "time_seconds": "0",
                    "status": "not_available_or_not_applicable",
                    "aux_status": reason,
                    "next_layer_value_real": "",
                    "next_layer_value_imag": "",
                    "next_layer_value_abs": "",
                    "error_bound": "",
                    "inverse_residual_fro": "",
                }
            )

    with (ART / "inversion_techniques_step289.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    stability_rows = []
    for cand, vals in values_for_stability.items():
        direct = next(v for n, v, _ in vals if n == "direct_inverse")
        for name, val, err in vals:
            rel = abs(val - direct) / max(abs(direct), mp.mpf("1e-300"))
            stable_value = rel < mp.mpf("1e-80")
            decisive = abs(val) > 10 * err
            stability_rows.append(
                {
                    "candidate": cand,
                    "technique": name,
                    "relative_difference_vs_direct": fmt(rel),
                    "value_stable_vs_direct": str(stable_value),
                    "error_bound": fmt(err),
                    "value_abs": fmt(abs(val)),
                    "decisive_against_error_bound": str(decisive),
                    "interpretation": "inverse stable but c-matrix error dominates" if not decisive else "value exceeds propagated c-error",
                }
            )

    with (ART / "next_layer_stability_step289.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(stability_rows[0].keys()))
        writer.writeheader()
        writer.writerows(stability_rows)

    schema = {
        "step": 289,
        "orientation": "adequacy",
        "target": "Branch B G^{-1} precision wall direct re-attack",
        "inherited_G_provenance": "Step208 G_matrix_step208.csv copied from Step207; diagonals Step203 LHopital; off-diagonals Step204 conjugate convention.",
        "condition_number_vs_dps": condition_rows,
        "inversion_techniques_compared": ["direct_inverse", "lu_solve_columns", "svd_pseudoinverse", "tikhonov_lambda_1e-80", "tikhonov_lambda_1e-30", "newton_refinement", "qr_column_pivoting_unavailable", "cholesky_not_applicable"],
        "next_layer_value_per_technique": rows,
        "cross_technique_stability": stability_rows,
        "final_verdict": "V_branch_B_G_inv_partial",
    }
    (ART / "step289_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    print("Step 289 Branch B G inverse attack")
    print(f"condition_dps_500={condition_rows[2]['condition_number']}")
    for cand in ["CAND1", "CAND2"]:
        direct_row = next(r for r in rows if r["technique"] == "direct_inverse" and r["candidate"] == cand)
        print(
            f"{cand}: Xi_abs={direct_row['next_layer_value_abs']} "
            f"err={direct_row['error_bound']}"
        )
    print("final_verdict=V_branch_B_G_inv_partial")


if __name__ == "__main__":
    main()
