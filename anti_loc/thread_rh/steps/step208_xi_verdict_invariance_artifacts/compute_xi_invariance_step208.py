#!/usr/bin/env python3
"""Compute Xi_matrix_source for Step 208 under CAND1 and CAND2."""

from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path

import mpmath as mp


mp.mp.dps = 100

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"
G_SRC = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts/G_matrix_step207.csv"
G_OUT = BASE / "G_matrix_step208.csv"


def mpc_from(real: str, imag: str) -> mp.mpc:
    return mp.mpc(mp.mpf(real), mp.mpf(imag))


def read_g() -> mp.matrix:
    shutil.copyfile(G_SRC, G_OUT)
    g = mp.matrix(3, 3)
    with G_OUT.open(newline="") as f:
        for row in csv.DictReader(f):
            i = int(row["i"]) - 1
            j = int(row["j"]) - 1
            g[i, j] = mpc_from(row["G_real"], row["G_imag"])
    return g


def read_c(candidate: str) -> tuple[mp.matrix, mp.matrix]:
    c = mp.matrix(3, 3)
    e = mp.matrix(3, 3)
    with (BASE / f"c_matrix_{candidate}_step208.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            i = int(row["i"]) - 1
            j = int(row["j"]) - 1
            c[i, j] = mpc_from(row["c_real"], row["c_imag"])
            e[i, j] = mp.mpf(row["error_bound"])
    return c, e


def dagger(m: mp.matrix) -> mp.matrix:
    out = mp.matrix(m.cols, m.rows)
    for i in range(m.rows):
        for j in range(m.cols):
            out[j, i] = mp.conj(m[i, j])
    return out


def fro_norm(m: mp.matrix) -> mp.mpf:
    total = mp.mpf("0")
    for i in range(m.rows):
        for j in range(m.cols):
            total += abs(m[i, j]) ** 2
    return mp.sqrt(total)


def op_norm_bound(m: mp.matrix) -> mp.mpf:
    # Conservative small-matrix bound sufficient for error propagation.
    return fro_norm(m)


def trace(m: mp.matrix) -> mp.mpc:
    return sum(m[i, i] for i in range(min(m.rows, m.cols)))


def xi_value(g_inv: mp.matrix, c: mp.matrix) -> mp.mpc:
    return trace(g_inv * dagger(c) * g_inv * c)


def xi_error_bound(g_inv: mp.matrix, c: mp.matrix, cerr: mp.matrix) -> mp.mpf:
    # For F(c)=tr(G^-1 c^* G^-1 c), use Frobenius/submultiplicative bound:
    # |F(c+e)-F(c)| <= ||G^-1||_F^2 (2||c||_F||e||_F + ||e||_F^2).
    gi = op_norm_bound(g_inv)
    cn = fro_norm(c)
    en = fro_norm(cerr)
    return gi**2 * (2 * cn * en + en**2)


def verdict_from(value: mp.mpc, error: mp.mpf) -> tuple[str, mp.mpf]:
    mag = abs(value)
    lower = max(mp.mpf("0"), mag - error)
    # Treat "zero within error" as a closure verdict only if the absolute
    # error is itself small on the residual scale.  Otherwise the diagnostic
    # is precision-limited rather than closed.
    if mag <= error and error <= mp.mpf("1e-8"):
        return "closes_within_error", lower
    if lower > 0 and mag > 10 * error:
        return "nonzero", lower
    return "inconclusive", lower


def fmt(z: mp.mpf | mp.mpc) -> str:
    return mp.nstr(z, 36, min_fixed=0, max_fixed=0)


def write_xi(candidate: str, value: mp.mpc, error: mp.mpf, local_verdict: str, lower: mp.mpf) -> None:
    with (BASE / f"xi_matrix_source_{candidate}_step208.csv").open("w", newline="") as f:
        fieldnames = [
            "candidate",
            "xi_real",
            "xi_imag",
            "xi_abs",
            "error_bound",
            "lower_bound_abs",
            "candidate_verdict",
            "formula",
            "status",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "candidate": candidate,
                "xi_real": fmt(mp.re(value)),
                "xi_imag": fmt(mp.im(value)),
                "xi_abs": fmt(abs(value)),
                "error_bound": fmt(error),
                "lower_bound_abs": fmt(lower),
                "candidate_verdict": local_verdict,
                "formula": "tr(G^{-1} c^dagger G^{-1} c)",
                "status": "diagnostic_candidate_invariance_test",
            }
        )


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    g = read_g()
    g_inv = g ** -1

    results = {}
    for candidate in ["CAND1", "CAND2"]:
        c, cerr = read_c(candidate)
        val = xi_value(g_inv, c)
        err = xi_error_bound(g_inv, c, cerr)
        local_verdict, lower = verdict_from(val, err)
        results[candidate] = (val, err, local_verdict, lower)
        write_xi(candidate, val, err, local_verdict, lower)

    v1 = results["CAND1"][2]
    v2 = results["CAND2"][2]
    if v1 == v2 == "closes_within_error":
        final = "V_xi_invariant_closes"
        inv = "invariant"
    elif v1 == v2 == "nonzero":
        final = "V_xi_invariant_nonzero"
        inv = "invariant"
    elif "inconclusive" in (v1, v2):
        final = "V_xi_invariant_partial"
        inv = "precision_limited"
    else:
        final = "V_xi_candidate_dependent"
        inv = "candidate_dependent"

    with (BASE / "verdict_invariance_step208.csv").open("w", newline="") as f:
        fieldnames = [
            "CAND1_verdict",
            "CAND2_verdict",
            "verdict_invariance",
            "final_verdict",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "CAND1_verdict": v1,
                "CAND2_verdict": v2,
                "verdict_invariance": inv,
                "final_verdict": final,
                "notes": "Diagnostic only: both computations use sampled candidate kappas, not a resolved transport theorem.",
            }
        )

    print("Step 208 Xi invariance")
    for candidate, (val, err, local_verdict, lower) in results.items():
        print(
            f"{candidate}: Xi={fmt(val)} |Xi|={fmt(abs(val))} "
            f"err<={fmt(err)} lower={fmt(lower)} verdict={local_verdict}"
        )
    print(f"final_verdict={final}")


if __name__ == "__main__":
    main()
