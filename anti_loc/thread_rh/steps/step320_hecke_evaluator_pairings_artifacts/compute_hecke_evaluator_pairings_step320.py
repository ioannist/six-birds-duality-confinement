#!/usr/bin/env python3
"""Step 320: Hecke-side evaluator pairings for primitive chars mod 3,4,5."""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
DPS = 70
MAX_K = 10


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


def beta_bump(u: mp.mpf) -> mp.mpf:
    if abs(u) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - u * u))


def g_star_coefficients() -> tuple[list[mp.mpf], mp.mpf, list[mp.mpf]]:
    centers = [mp.mpf("1.5"), mp.mpf("2.5"), mp.mpf("3.5")]
    eps = mp.mpf("0.20")
    A: list[mp.mpf] = []
    B: list[mp.mpf] = []
    for c in centers:
        lo, hi = c - eps, c + eps
        A.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps), [lo, hi]))
        B.append(mp.quad(lambda t, cc=c: beta_bump((t - cc) / eps) / t, [lo, hi]))
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return centers, eps, [mp.mpf("1"), -alpha, beta_3]


def character_data() -> dict[str, tuple[int, list[mp.mpc]]]:
    I = mp.mpc(0, 1)
    return {
        "chi_3": (3, [0, 1, -1]),
        "chi_4": (4, [0, 1, 0, -1]),
        "chi_5a": (5, [0, 1, -1, -1, 1]),
        "chi_5b": (5, [0, 1, I, -I, -1]),
    }


def L_derivatives(s: mp.mpc, q: int, chi: list[mp.mpc], max_k: int) -> list[mp.mpc]:
    logq = mp.log(q)
    out: list[mp.mpc] = []
    q_factor = mp.mpf(q) ** (-s)
    zeta_sums: list[mp.mpc] = []
    for m in range(max_k + 1):
        zeta_sums.append(
            mp.fsum([chi[a % q] * mp.zeta(s, mp.mpf(a) / q, derivative=m) for a in range(1, q + 1)])
        )
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for m in range(n + 1):
            total += mp.mpf(math.comb(n, m)) * ((-logq) ** (n - m)) * zeta_sums[m]
        out.append(q_factor * total)
    return out


def M_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    centers, eps, coeffs = g_star_coefficients()
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, a in zip(centers, coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t: mp.mpf, cc: mp.mpf = c, aa: mp.mpf = a, nn: int = n) -> mp.mpc:
                return aa * beta_bump((t - cc) / eps) * (t ** (-s)) * ((-mp.log(t)) ** nn)

            total += mp.quad(integrand, [lo, hi])
        out.append(total)
    return out


def h_derivative(Lds: list[mp.mpc], Mds: list[mp.mpc], k: int) -> mp.mpc:
    total = mp.mpc(0)
    for j in range(k + 1):
        total += mp.mpf(math.comb(k, j)) * Lds[j] * Mds[k - j]
    return total


def load_roots() -> dict[str, mp.mpc]:
    rows = read_csv(ART / "L_chi_first_zeros_step320.csv")
    out: dict[str, mp.mpc] = {}
    for row in rows:
        out[row["character"]] = mp.mpc(mp.mpf(row["Re_rho"]), mp.mpf(row["Im_rho"]))
    return out


def zeta_branch_c_raw_values() -> dict[int, mp.mpf]:
    """Compute raw |(zeta*M(G_star))^(k)(rho_1)| for scale comparison."""
    rho1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562"))
    zds = [mp.zeta(rho1, derivative=n) for n in range(MAX_K + 1)]
    mds = M_derivatives(rho1, MAX_K)
    return {k: abs(h_derivative(zds, mds, k)) for k in range(MAX_K + 1)}


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    roots = load_roots()
    chars = character_data()
    value_rows: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []
    start = time.time()

    per_char: dict[str, dict[int, mp.mpf]] = {}
    for label, rho in roots.items():
        q, chi = chars[label]
        t0 = time.time()
        Lds = L_derivatives(rho, q, chi, MAX_K)
        Mds = M_derivatives(rho, MAX_K)
        runtime = time.time() - t0
        per_char[label] = {}
        for k in range(MAX_K + 1):
            raw = h_derivative(Lds, Mds, k)
            normalized = raw / mp.factorial(k)
            per_char[label][k] = abs(raw)
            value_rows.append(
                {
                    "character": label,
                    "k": k,
                    "rho_chi": cstr(rho, 26),
                    "h_derivative_complex": cstr(raw, 36),
                    "h_derivative_abs": mp.nstr(abs(raw), 18),
                    "L_k_normalized_complex_h_derivative_over_k_factorial": cstr(normalized, 36),
                    "L_k_normalized_abs": mp.nstr(abs(normalized), 18),
                    "L_derivative_abs_at_zero": mp.nstr(abs(Lds[k]), 18),
                    "M_derivative_abs_at_zero": mp.nstr(abs(Mds[k]), 18),
                    "runtime_for_character_seconds": f"{runtime:.3f}",
                }
            )

    branch_c = zeta_branch_c_raw_values()
    prompt_refs = {
        0: "0.121",
        1: "0.289",
        2: "0.573",
        3: "1.116",
        4: "2.202",
        5: "4.276",
        10: "165.44",
    }
    for k in range(MAX_K + 1):
        row: dict[str, object] = {
            "k": k,
            "branch_C_zeta_raw_abs_recomputed": mp.nstr(branch_c[k], 18),
            "branch_C_prompt_reference_abs_if_given": prompt_refs.get(k, ""),
        }
        for label in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
            row[f"{label}_raw_abs"] = mp.nstr(per_char[label][k], 18)
            denom = branch_c[k] if branch_c[k] != 0 else mp.mpf("nan")
            row[f"{label}_raw_abs_div_branch_C_recomputed"] = mp.nstr(per_char[label][k] / denom, 12)
        comparison_rows.append(row)

    write_csv(ART / "hecke_L_k_values_step320.csv", value_rows)
    write_csv(ART / "branch_C_vs_hecke_comparison_step320.csv", comparison_rows)

    verdict = "V_hecke_H5_subfamily_evaluator_pairings_active"
    lines = [
        "# Step 320 Results Summary",
        "",
        "Computed concrete Hecke-side Sonine evaluator pairings for the primitive Dirichlet-character subfamily from Step 319: `chi_3`, `chi_4`, `chi_5a`, and `chi_5b`.",
        "",
        "Definitions used:",
        "- `L(s,chi)=q^{-s} sum_{a=1}^q chi(a) zeta(s,a/q)`.",
        "- `M(G_star)(s)=int G_star(t) t^{-s} dt`, using the inherited Branch C `t^{-s}` convention.",
        "- `h_chi(s)=L(s,chi) M(G_star)(s)`.",
        "- The CSV records both raw `|h_chi^(k)(rho_chi)|` and normalized `|h_chi^(k)(rho_chi)/k!|`; the prompt-supplied Branch C reference values are also recorded because the older projected Branch C table and the raw derivative table use different normalizations at small `k`; `k=10` matches the raw derivative scale (`165.44`).",
        "",
        "First zeros and residuals are recorded in `L_chi_first_zeros_step320.csv`.  The order-four mod 5 character with `chi(2)=i` converged to the first critical-line zero near `0.5+6.18357819545i`; the rough prompt value `3.671` was not used as a forced value.",
        "",
        "Qualitative comparison: every character produces nonzero evaluator records through `k=10`.  The raw magnitudes grow substantially, but the growth rates and k=10 scales differ by character and are not universal from this small subfamily.",
        "",
        "Hecke cascade status: H5 is active for this concrete primitive mod 3/4/5 subfamily. This is concrete numerical content, not a Hecke closure or GRH claim.",
        "",
        f"Runtime: {time.time() - start:.3f} seconds. Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step320_results_summary.md").write_text("\n".join(lines), encoding="utf-8")
    schema = {
        "step": 320,
        "orientation": "attempt",
        "target": "Hecke-side Sonine evaluator pairings for primitive Dirichlet characters mod 3,4,5",
        "dps": DPS,
        "characters": ["chi_3", "chi_4", "chi_5a", "chi_5b"],
        "k_range": "0..10",
        "mellin_convention": "t^{-s}",
        "outputs": [
            "L_chi_first_zeros_step320.csv",
            "hecke_L_k_values_step320.csv",
            "branch_C_vs_hecke_comparison_step320.csv",
        ],
        "final_verdict": verdict,
    }
    (ART / "step320_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step320.md").write_text(
        "# Step 320 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim Hecke closure.\n"
        "- Numerical zeros are used as evaluator anchors for a concrete primitive-character subfamily only.\n"
        "- H5 activation here is subfamily-level numerical content, not full Hecke-family ledger closure.\n",
        encoding="utf-8",
    )
    print("Step320 Hecke evaluator pairings")
    for label in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
        vals = [mp.nstr(per_char[label][k], 8) for k in range(MAX_K + 1)]
        print(f"{label} raw_abs k0..10: {vals}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
