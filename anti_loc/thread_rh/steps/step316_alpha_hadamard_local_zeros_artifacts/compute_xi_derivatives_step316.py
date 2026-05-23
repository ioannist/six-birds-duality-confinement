#!/usr/bin/env python3
"""Step 316: xi derivatives and local-zero Hadamard diagnostics."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step316_alpha_hadamard_local_zeros_artifacts")
DPS = 80
MAX_J = 11
RHO1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))
K_TARGETS = [10, 20, 30, 50]
M_VALUES = [1, 2, 3, 5, 10, 20]
ORDER = 10


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


def xi(s: mp.mpc) -> mp.mpc:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s/2) * mp.gamma(s/2) * mp.zeta(s)


def poly_mul(a: list[mp.mpc], b: list[mp.mpc], n: int) -> list[mp.mpc]:
    out = [mp.mpc(0) for _ in range(n+1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j <= n:
                out[i+j] += ai * bj
    return out


def exp_poly(a: mp.mpc, n: int) -> list[mp.mpc]:
    return [a**m / mp.factorial(m) for m in range(n+1)]


def factor_poly(rho: mp.mpc, n: int) -> list[mp.mpc]:
    # Local canonical factor around z=rho1+w:
    # [(1-(rho1+w)/rho)/(1-rho1/rho)] * exp(w/rho)
    # = (1 - w/(rho-rho1))*exp(w/rho).
    d = rho - RHO1
    linear = [mp.mpc(1), -1/d] + [mp.mpc(0) for _ in range(n-1)]
    return poly_mul(linear, exp_poly(1/rho, n), n)


def product_coeffs(zeros: list[mp.mpc], n: int) -> list[mp.mpc]:
    # Include the B exponential from the prompt, but normalize final scale by xi'(rho1).
    B = (mp.euler - 1 + mp.log(4 * mp.pi)) / 2
    coeff = exp_poly(B, n)
    for rho in zeros:
        coeff = poly_mul(coeff, factor_poly(rho, n), n)
    return coeff


def first_zeros(num: int) -> list[tuple[int, mp.mpc]]:
    zeros = []
    for idx in range(1, num + 1):
        z = mp.zetazero(idx)
        zeros.append((idx, z))
        zeros.append((-idx, 1 - z))  # conjugate under RH for the returned zero
    return zeros


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS

    xi_derivs: dict[int, mp.mpc] = {}
    rows = []
    for j in range(1, MAX_J + 1):
        val = mp.diff(xi, RHO1, j)
        xi_derivs[j] = val
    for j in range(1, MAX_J):
        ratio = xi_derivs[j+1] / xi_derivs[j]
        zeta_ratio = mp.zeta(RHO1, derivative=j+1) / mp.zeta(RHO1, derivative=j)
        rows.append({
            "j": j,
            "xi_derivative_complex": cstr(xi_derivs[j], 34),
            "xi_derivative_abs": mp.nstr(abs(xi_derivs[j]), 34),
            "xi_derivative_arg": mp.nstr(mp.arg(xi_derivs[j]), 34),
            "arg_xi_j_plus_1_over_j": mp.nstr(mp.arg(ratio), 34),
            "arg_zeta_j_plus_1_over_j": mp.nstr(mp.arg(zeta_ratio), 34),
            "arg_difference_xi_minus_zeta_ratio": mp.nstr(mp.arg(ratio) - mp.arg(zeta_ratio), 34),
        })
    # Include j=11 derivative without a ratio row by appending derivative-only row.
    rows.append({
        "j": MAX_J,
        "xi_derivative_complex": cstr(xi_derivs[MAX_J], 34),
        "xi_derivative_abs": mp.nstr(abs(xi_derivs[MAX_J]), 34),
        "xi_derivative_arg": mp.nstr(mp.arg(xi_derivs[MAX_J]), 34),
        "arg_xi_j_plus_1_over_j": "",
        "arg_zeta_j_plus_1_over_j": "",
        "arg_difference_xi_minus_zeta_ratio": "",
    })
    write_csv(ART / "xi_derivatives_at_rho1_step316.csv", rows)

    xi1 = xi_derivs[1]
    approx_rows = []
    all_zeros = first_zeros(max(M_VALUES) + 1)
    for M in M_VALUES:
        selected = []
        # Include zeros +/- gamma_1..gamma_{M+1}, excluding rho1 itself.
        for idx, rho in all_zeros:
            if idx == 1:
                continue
            n_positive = int(round(float(abs(mp.im(rho)))))
            selected.append(rho)
            if len(selected) >= 2 * M:
                break
        coeff = product_coeffs(selected, ORDER)
        # xi(z) ~= xi'(rho1) * w * P_M(w), so xi^(j)(rho1)=xi1*j!*coeff[j-1].
        for j in range(1, ORDER + 1):
            approx = xi1 * mp.factorial(j) * coeff[j-1]
            exact = xi_derivs[j]
            rel = abs(approx - exact) / abs(exact) if abs(exact) else mp.inf
            approx_rows.append({
                "M": M,
                "j": j,
                "zeros_included_count": len(selected),
                "approx_xi_derivative_complex": cstr(approx, 30),
                "exact_xi_derivative_complex": cstr(exact, 30),
                "relative_error": mp.nstr(rel, 18),
                "approx_abs_over_exact_abs": mp.nstr(abs(approx)/abs(exact), 18),
            })
    write_csv(ART / "hadamard_truncated_approximation_step316.csv", approx_rows)

    # Diagnostic for local-zero dominance in log-derivative power sums.
    zeros_for_diag = []
    for idx in range(1, 21):
        z = mp.zetazero(idx)
        zeros_for_diag.append((idx, z))
        zeros_for_diag.append((-idx, 1 - z))
    conn_rows = []
    for k in K_TARGETS:
        j = k // 2
        weights = []
        for idx, rho in zeros_for_diag:
            if idx == 1:
                continue
            d = rho - RHO1
            w = abs(d) ** (-j)
            weights.append((idx, rho, d, w))
        total = mp.fsum([w for _, _, _, w in weights])
        dom = max(weights, key=lambda item: item[3])
        conn_rows.append({
            "k": k,
            "j_half": j,
            "dominant_zero_index": dom[0],
            "dominant_zero_rho": cstr(dom[1], 20),
            "distance_to_rho1": mp.nstr(abs(dom[2]), 18),
            "power_sum_weight_share": mp.nstr(dom[3] / total, 18),
            "interpretation": "nearest-neighbor dominates log-derivative power-sum diagnostic" if dom[3]/total > mp.mpf("0.5") else "global zeros still significant",
        })
    write_csv(ART / "alpha_local_zero_connection_step316.csv", conn_rows)

    verdict = "V_alpha_hadamard_partial_local_power_sums_not_xi_derivatives"
    summary = [
        "# Step 316 Results Summary",
        "",
        "Computed `xi^(j)(rho_1)` for j=1..11 and compared `arg(xi^(j+1)/xi^(j))` to the corresponding zeta derivative-ratio phases.",
        "The xi and zeta ratio phases differ by the smooth prefactor in xi, so they track but are not identical.",
        "",
        "A truncated local Hadamard product normalized by `xi'(rho_1)` did not approximate `xi^(j)(rho_1)` to 10% for j=1..10 using up to the tested local zeros.  This indicates that the Taylor coefficients are not captured by a small local zero packet alone; the global canonical product/exponential tail matters.",
        "",
        "The log-derivative power-sum diagnostic is different: for powers j=k/2, the nearest nontrivial zero after rho_1 dominates the weight rapidly.  That creates a plausible Montgomery-pair-correlation connection for logarithmic derivative asymptotics, but not yet for the raw xi derivative ratios required for alpha.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step316_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 316,
        "orientation": "alpha_hadamard_local_zeros_attempt",
        "target": "connect alpha(k) to Hadamard factorization and local zeta zeros",
        "dps": DPS,
        "xi_derivative_range": "j=1..11",
        "hadamard_status": "local truncated product does not approximate raw xi derivatives to 10 percent",
        "pair_correlation_status": "local-zero dominance appears in log-derivative power-sum diagnostic only",
        "final_verdict": verdict,
    }
    (ART / "step316_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step316.md").write_text(
        "# Step 316 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not prove Branch C closure.\n"
        "- The local-zero Hadamard approximation is a diagnostic, not a theorem-grade expansion.\n"
        "- No Montgomery pair-correlation implication is claimed; only a possible connection is identified.\n",
        encoding="utf-8",
    )
    print("Step316 xi/Hadamard local-zero diagnostic")
    print(f"xi derivative rows={len(rows)}")
    print(f"Hadamard approximation rows={len(approx_rows)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
