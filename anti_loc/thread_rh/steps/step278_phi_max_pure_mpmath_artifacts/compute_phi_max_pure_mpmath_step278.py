#!/usr/bin/env python3
"""Step 278: pure-mpmath Branch A Phi attempt.

This is a no-NumPy critical-path implementation of the local wavepacket
diagnostic.  It replaces NumPy Gauss-Legendre quadrature and matrix products
with mpmath quadrature nodes and mpmath.matrix multiplication.

Important scope boundary: this script implements the hard-band/sinc projection
proxy that Step 276 found numerically indistinguishable from the inherited
PSWF24 baseline at double precision.  A pure-mpmath PSWF eigensystem/SVD for the
full Sonine projection was not completed in this step; the result is therefore
an attempted high-precision proxy and a convergence test, not a full replacement
of the inherited pipeline.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step278_phi_max_pure_mpmath_artifacts")

SIGMA = mp.mpf("0.35")
ELL = mp.mpf("2.0")
LAMBDA = mp.mpf("1.0")
WINDOW = mp.mpf("80.0")
REFERENCE = mp.mpf("0.4904766200298252")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def panel_nodes(center: mp.mpf, a: mp.mpf, b: mp.mpf, n: int) -> list[tuple[mp.mpf, mp.mpf]]:
    xs, ws = mp.gauss_quadrature(n, "legendre")
    mid = (a + b) / 2
    half = (b - a) / 2
    return [(center + mid + half * x, half * w) for x, w in zip(xs, ws, strict=True)]


def composite_nodes(center: mp.mpf, total_n: int) -> list[tuple[mp.mpf, mp.mpf]]:
    # Concentrate nodes near the Gaussian support while retaining a long window
    # for the sinc tail.
    n1 = max(2, total_n // 20)
    n2 = max(4, total_n // 10)
    n3 = total_n - 2 * n1 - 2 * n2
    if n3 < 8:
        n3 = 8
    panels = [
        (-WINDOW, mp.mpf("-4.0"), n1),
        (mp.mpf("-4.0"), mp.mpf("-1.2"), n2),
        (mp.mpf("-1.2"), mp.mpf("1.2"), n3),
        (mp.mpf("1.2"), mp.mpf("4.0"), n2),
        (mp.mpf("4.0"), WINDOW, n1),
    ]
    pts: list[tuple[mp.mpf, mp.mpf]] = []
    for a, b, n in panels:
        pts.extend(panel_nodes(center, mp.mpf(a), mp.mpf(b), int(n)))
    return pts


def sinc(x: mp.mpf) -> mp.mpf:
    if abs(x) < mp.mpf("1e-60"):
        return LAMBDA / mp.pi
    return mp.sin(LAMBDA * x) / (mp.pi * x)


def l2_norm(vec: mp.matrix, weights: list[mp.mpf]) -> mp.mpf:
    total = mp.fsum([weights[i] * abs(vec[i]) ** 2 for i in range(len(weights))])
    return mp.sqrt(max(mp.mpf("0"), total / (2 * mp.pi)))


def kernel_matrix(nodes: list[mp.mpf], weights: list[mp.mpf]) -> mp.matrix:
    n = len(nodes)
    mat = mp.matrix(n, n)
    for i in range(n):
        ti = nodes[i]
        for j in range(n):
            mat[i, j] = weights[j] * sinc(ti - nodes[j])
    return mat


def phi_value(total_n: int, dps: int, center_text: str) -> dict[str, object]:
    mp.mp.dps = dps
    center = mp.mpf(center_text)
    pts = composite_nodes(center, total_n)
    nodes = [t for t, _ in pts]
    weights = [w for _, w in pts]
    n = len(nodes)

    u = mp.matrix(n, 1)
    for i, t in enumerate(nodes):
        x = t - center
        u[i] = mp.e ** (-(x**2) / (2 * SIGMA**2)) if abs(x) <= 3 * SIGMA else mp.mpf("0")
    un = l2_norm(u, weights)
    for i in range(n):
        u[i] /= un

    s_mat = kernel_matrix(nodes, weights)
    ident = mp.eye(n)
    p_mat = ident - s_mat
    pu = p_mat * u
    phase = mp.matrix(n, n)
    for i, t in enumerate(nodes):
        phase[i, i] = mp.e ** (1j * ELL * t)
    h = phase * pu - p_mat * (phase * pu)
    phi = l2_norm(h, weights)
    return {
        "N": str(n),
        "requested_N": str(total_n),
        "dps": str(dps),
        "T": center_text,
        "Phi": mp.nstr(phi, 80),
        "abs_error_vs_numpy_reference": mp.nstr(abs(phi - REFERENCE), 40),
        "projection": "pure_mpmath_sinc_hard_band_proxy",
        "status": "computed",
    }


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    runs = [
        (40, 80, "5000"),
        (80, 80, "5000"),
        (120, 80, "5000"),
        (160, 80, "5000"),
        (80, 120, "5000"),
        (80, 80, "10000"),
    ]
    rows = []
    for total_n, dps, center in runs:
        row = phi_value(total_n, dps, center)
        rows.append(row)
        print(f"N={row['N']} dps={dps} T={center} Phi={row['Phi']}")

    write_csv(ART / "convergence_check_step278.csv", rows)

    # No row reaches the inherited reference to 12 digits.  The high-precision
    # value is therefore intentionally marked untrusted.
    best = min(rows, key=lambda row: mp.mpf(row["abs_error_vs_numpy_reference"]))
    high_precision = [
        {
            "selected_row": "best_available_pure_mpmath_proxy",
            "N": best["N"],
            "dps": best["dps"],
            "T": best["T"],
            "Phi": best["Phi"],
            "trusted_digits_vs_reference": "0",
            "stability_status": "not_stable_enough_for_pslq",
            "notes": "pure mpmath sinc-proxy did not converge to the inherited Phi value at tested node counts",
        },
        {
            "selected_row": "inherited_reference_for_comparison",
            "N": "GL1400_numpy",
            "dps": "80 nominal",
            "T": "5000",
            "Phi": mp.nstr(REFERENCE, 80),
            "trusted_digits_vs_reference": "about 14-15 from inherited pipeline",
            "stability_status": "reference_only_not_pure_mpmath",
            "notes": "used only for comparison and PSLQ boundary",
        },
    ]
    write_csv(ART / "phi_max_high_precision_step278.csv", high_precision)

    summary = {
        "runs": rows,
        "best_available": best,
        "reference": mp.nstr(REFERENCE, 80),
        "final_status": "pure_mpmath_proxy_not_converged",
    }
    (ART / "compute_phi_max_pure_mpmath_output_step278.txt").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
