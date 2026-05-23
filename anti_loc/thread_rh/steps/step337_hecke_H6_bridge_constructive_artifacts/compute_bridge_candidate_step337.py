#!/usr/bin/env python3
import csv
import json
import math
import re
from pathlib import Path

import mpmath as mp

mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step337_hecke_H6_bridge_constructive_artifacts"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b"]


def csv_rows(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def parse_complex(s):
    s = s.replace(" ", "").replace("j", "")
    # Split on the last sign that is not part of an exponent.
    m = re.match(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)([+-](?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)$", s)
    if not m:
        return mp.mpc(s)
    return mp.mpc(mp.mpf(m.group(1)), mp.mpf(m.group(2)))


def bump(t, c, eps):
    x = (t - c) / eps
    if abs(x) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - x * x))


CENTERS = [mp.mpf("1.5"), mp.mpf("2.5"), mp.mpf("3.5")]
EPS = mp.mpf("0.20")
COEFFS = [mp.mpf("1"), mp.mpf("-3.3409952306"), mp.mpf("2.3409952306")]


def M_derivative(s, n):
    total = mp.mpc(0)
    for a, c in zip(COEFFS, CENTERS):
        lo = c - EPS
        hi = c + EPS
        mid = c

        def integrand(t):
            return a * bump(t, c, EPS) * ((-mp.log(t)) ** n) * (t ** (-s))

        total += mp.quad(integrand, [lo, mid, hi])
    return total


def zeta_derivative(s, n):
    if n == 0:
        return mp.zeta(s)
    return mp.diff(lambda z: mp.zeta(z), s, n)


def zeta_branch_raw_derivative(k):
    rho1 = mp.zetazero(1)
    total = mp.mpc(0)
    for j in range(k + 1):
        total += mp.binomial(k, j) * zeta_derivative(rho1, j) * M_derivative(rho1, k - j)
    return total


def dirichlet_L(s, q, values):
    # values indexed by residue 0..q-1.
    total = mp.mpc(0)
    for a in range(1, q + 1):
        val = values[a % q]
        if val != 0:
            total += val * mp.zeta(s, mp.mpf(a) / q)
    return total / (q ** s)


def char_values(label):
    I = mp.j
    if label == "chi_3":
        return 3, [0, 1, -1]
    if label == "chi_4":
        return 4, [0, 1, 0, -1]
    if label == "chi_5a":
        return 5, [0, 1, -1, -1, 1]
    if label == "chi_5b":
        return 5, [0, 1, I, -I, -1]
    raise ValueError(label)


def principal_values(q):
    return [0 if math.gcd(a, q) != 1 else 1 for a in range(q)]


def prime_divisors(q):
    out = []
    n = q
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def all_dirichlet_chars_prime(q):
    # Enough for q=3 and q=5 prime. Characters are powers of a primitive root.
    if q == 3:
        return [[0, 1, 1], [0, 1, -1]]
    if q == 5:
        I = mp.j
        return [
            [0, 1, 1, 1, 1],
            [0, 1, I, -I, -1],
            [0, 1, -1, -1, 1],
            [0, 1, -I, I, -1],
        ]
    raise ValueError(q)


def relative(num, den):
    den_abs = abs(den)
    if den_abs == 0:
        return "inf"
    return mp.nstr(abs(num) / den_abs, 12)


def solve_complex_ls(A, b):
    # Normal equations over complex mpmath matrices.
    m = len(A)
    n = len(A[0])
    AH_A = mp.matrix(n, n)
    AH_b = mp.matrix(n, 1)
    for i in range(n):
        for j in range(n):
            AH_A[i, j] = sum(mp.conj(A[r][i]) * A[r][j] for r in range(m))
        AH_b[i] = sum(mp.conj(A[r][i]) * b[r] for r in range(m))
    return mp.lu_solve(AH_A, AH_b)


def main():
    hecke_rows = csv_rows(STEP320 / "hecke_L_k_values_step320.csv")
    hecke = {ch: {} for ch in CHARS}
    for r in hecke_rows:
        ch = r["character"]
        k = int(r["k"])
        if ch in hecke and 1 <= k <= 10:
            hecke[ch][k] = parse_complex(r["h_derivative_complex"])

    branch = {k: zeta_branch_raw_derivative(k) for k in range(1, 11)}

    identity_rows = []
    rho1 = mp.zetazero(1)
    zrho = mp.zeta(rho1)

    for q in [3, 5]:
        pv = principal_values(q)
        Lp = dirichlet_L(rho1, q, pv)
        corr = mp.mpc(1)
        for p in prime_divisors(q):
            corr *= 1 - p ** (-rho1)
        identity_rows.append({
            "candidate": "principal_character_correction",
            "modulus": q,
            "formula": "L(s,chi0_q)/prod_{p|q}(1-p^-s)=zeta(s)",
            "lhs_abs": mp.nstr(abs(Lp / corr), 18),
            "rhs_abs": mp.nstr(abs(zrho), 18),
            "residual_abs": mp.nstr(abs(Lp / corr - zrho), 18),
            "status": "true_scalar_identity_but_uses_principal_character_not_H5_subfamily",
        })

        sum_all = sum(dirichlet_L(rho1, q, vals) for vals in all_dirichlet_chars_prime(q))
        identity_rows.append({
            "candidate": "unweighted_sum_all_characters",
            "modulus": q,
            "formula": "sum_{chi mod q} L(s,chi) ?= zeta(s)",
            "lhs_abs": mp.nstr(abs(sum_all), 18),
            "rhs_abs": mp.nstr(abs(zrho), 18),
            "residual_abs": mp.nstr(abs(sum_all - zrho), 18),
            "status": "false; orthogonality gives residue-class zeta sums, not zeta",
        })

    sum_h5 = mp.mpc(0)
    for ch in CHARS:
        q, vals = char_values(ch)
        sum_h5 += dirichlet_L(rho1, q, vals)
    identity_rows.append({
        "candidate": "sum_H5_nonprincipal_subfamily",
        "modulus": "3,4,5",
        "formula": "sum_{chi in H5} L(rho1,chi) ?= zeta(rho1)",
        "lhs_abs": mp.nstr(abs(sum_h5), 18),
        "rhs_abs": mp.nstr(abs(zrho), 18),
        "residual_abs": mp.nstr(abs(sum_h5 - zrho), 18),
        "status": "false; finite nonprincipal subfamily does not reconstruct zeta",
    })
    write_csv(ART / "zeta_dirichlet_identities_step337.csv", identity_rows,
              ["candidate", "modulus", "formula", "lhs_abs", "rhs_abs", "residual_abs", "status"])

    A = [[hecke[ch][k] for ch in CHARS] for k in range(1, 11)]
    b = [branch[k] for k in range(1, 11)]
    coeff = solve_complex_ls(A, b)
    coeffs = {ch: coeff[i] for i, ch in enumerate(CHARS)}

    # Magnitude-only real least squares using mpmath normal equations.
    Am = [[abs(hecke[ch][k]) for ch in CHARS] for k in range(1, 11)]
    bm = [abs(branch[k]) for k in range(1, 11)]
    AtA = mp.matrix(4, 4)
    Atb = mp.matrix(4, 1)
    for i in range(4):
        for j in range(4):
            AtA[i, j] = sum(Am[r][i] * Am[r][j] for r in range(10))
        Atb[i] = sum(Am[r][i] * bm[r] for r in range(10))
    coeff_mag = mp.lu_solve(AtA, Atb)

    fit_rows = []
    for ch in CHARS:
        c = coeffs[ch]
        fit_rows.append({
            "row_type": "complex_coefficient",
            "k": "",
            "character": ch,
            "coefficient_real": mp.nstr(mp.re(c), 18),
            "coefficient_imag": mp.nstr(mp.im(c), 18),
            "zeta_target_abs": "",
            "fit_abs": "",
            "residual_abs": "",
            "relative_residual": "",
            "verdict": "least_squares_coefficient",
        })
    for i, ch in enumerate(CHARS):
        fit_rows.append({
            "row_type": "magnitude_fit_coefficient",
            "k": "",
            "character": ch,
            "coefficient_real": mp.nstr(coeff_mag[i], 18),
            "coefficient_imag": "0",
            "zeta_target_abs": "",
            "fit_abs": "",
            "residual_abs": "",
            "relative_residual": "",
            "verdict": "least_squares_coefficient_on_abs_values",
        })

    rss = mp.mpf("0")
    tss = mp.mpf("0")
    mean_abs = sum(abs(branch[k]) for k in range(1, 11)) / 10
    max_rel = mp.mpf("0")
    for k in range(1, 11):
        pred = sum(coeffs[ch] * hecke[ch][k] for ch in CHARS)
        res = branch[k] - pred
        rel = abs(res) / abs(branch[k])
        max_rel = max(max_rel, rel)
        rss += abs(res) ** 2
        tss += (abs(branch[k]) - mean_abs) ** 2
        fit_rows.append({
            "row_type": "complex_fit_residual",
            "k": k,
            "character": "all",
            "coefficient_real": "",
            "coefficient_imag": "",
            "zeta_target_abs": mp.nstr(abs(branch[k]), 18),
            "fit_abs": mp.nstr(abs(pred), 18),
            "residual_abs": mp.nstr(abs(res), 18),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
        })

    mag_max_rel = mp.mpf("0")
    for k in range(1, 11):
        pred = sum(coeff_mag[i] * Am[k - 1][i] for i in range(4))
        res = bm[k - 1] - pred
        rel = abs(res) / bm[k - 1]
        mag_max_rel = max(mag_max_rel, rel)
        fit_rows.append({
            "row_type": "magnitude_fit_residual",
            "k": k,
            "character": "all_abs",
            "coefficient_real": "",
            "coefficient_imag": "",
            "zeta_target_abs": mp.nstr(bm[k - 1], 18),
            "fit_abs": mp.nstr(abs(pred), 18),
            "residual_abs": mp.nstr(abs(res), 18),
            "relative_residual": mp.nstr(rel, 12),
            "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
        })

    write_csv(
        ART / "bridge_coefficient_fit_step337.csv",
        fit_rows,
        [
            "row_type", "k", "character", "coefficient_real", "coefficient_imag",
            "zeta_target_abs", "fit_abs", "residual_abs", "relative_residual", "verdict",
        ],
    )

    complex_pass = max_rel < mp.mpf("0.01")
    mag_pass = mag_max_rel < mp.mpf("0.01")
    verdict = (
        "V_hecke_H6_finite_fit_small_but_structural_bridge_missing"
        if complex_pass or mag_pass
        else "V_hecke_H6_constructive_bridge_failed_missing_carrier_descent"
    )

    summary = [
        "# Step 337 Results Summary",
        "",
        "Constructive H6 bridge attempt using Step 320 H5 evaluator pairings and Branch C zeta raw derivatives.",
        "",
        "Scalar identity audit:",
        "- Principal-character correction recovers zeta, but it uses the principal imprimitive character and only scalar L-functions.",
        "- Unweighted sums over all characters do not equal zeta; character orthogonality reconstructs residue-class zeta sums.",
        "- The finite H5 nonprincipal subfamily does not vanish at rho_1 and does not reconstruct zeta.",
        "",
        "Finite coefficient fit:",
        f"- Complex least-squares max relative residual over k=1..10: `{mp.nstr(max_rel, 12)}`.",
        f"- Magnitude-only least-squares max relative residual over k=1..10: `{mp.nstr(mag_max_rel, 12)}`.",
        "",
        "Interpretation:",
        "Even if a finite numerical fit is small on this short range, it is only interpolation across four unrelated Hecke zero carriers. It does not supply a carrier/projection/kernel-preserving descent from Hecke spaces to the Burnol/Sonine zeta residual.",
        "",
        "Missing element:",
        "A functorial carrier descent identifying the Hecke Dirichlet-Sonine spaces, zero evaluators, projections, and residual pairings with the zeta Burnol/Sonine carrier. Scalar L-function identities alone are insufficient.",
        "",
        f"Final verdict: `{verdict}`.",
    ]
    (ART / "step337_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 337,
        "orientation": "constructive",
        "target": "Hecke H6 bridge construction attempt",
        "dps": 80,
        "characters": CHARS,
        "k_fit_range": "1..10",
        "complex_fit_max_relative_residual": mp.nstr(max_rel, 18),
        "magnitude_fit_max_relative_residual": mp.nstr(mag_max_rel, 18),
        "bridge_claimed": False,
        "final_verdict": verdict,
        "missing_element": "carrier/projection/kernel-preserving Hecke-to-Burnol zeta-fiber descent",
    }
    (ART / "step337_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    nonclaim = [
        "# Step 337 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- No H6 bridge is claimed from scalar L-function identities.",
        "- Least-squares coefficients over k=1..10 are numerical interpolation, not a descent theorem.",
        "- The missing object remains a carrier/projection/kernel-preserving Hecke-to-Burnol zeta-fiber descent.",
    ]
    (ART / "nonclaim_boundary_step337.md").write_text("\n".join(nonclaim) + "\n")

    print(f"complex_max_rel={mp.nstr(max_rel, 12)}")
    print(f"magnitude_max_rel={mp.nstr(mag_max_rel, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
