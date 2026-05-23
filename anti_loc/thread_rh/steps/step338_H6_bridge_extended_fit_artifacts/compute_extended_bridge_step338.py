#!/usr/bin/env python3
"""Step 338: extend the finite H6 bridge fit with three more characters.

This is a constructive numerical attempt.  It extends the Step 337 complex
least-squares bridge by adding the Step 329 character definitions
chi_7b, chi_11c, and chi_13a.  The fit is against raw derivatives
(L*M(G_star))^(k), matching the Step 337 convention.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts"
STEP337 = ROOT / "anti_loc/thread/steps/step337_hecke_H6_bridge_constructive_artifacts"

DPS = 80
FIT_K = list(range(1, 11))
HOLDOUT_K = [11, 12, 15, 20]
ALL_K = sorted(set(FIT_K + HOLDOUT_K))

OLD_CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b"]
NEW_CHARS = ["chi_7b", "chi_11c", "chi_13a"]
ALL_CHARS = OLD_CHARS + NEW_CHARS


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


def parse_complex(s: str) -> mp.mpc:
    s = s.strip().replace(" ", "")
    if s.endswith("j"):
        s = s[:-1]
    # mpmath accepts "a+bj" poorly after j stripping, so split on the last
    # non-exponent sign.
    split = None
    for idx in range(1, len(s)):
        if s[idx] in "+-" and s[idx - 1] not in "eE":
            split = idx
    if split is None:
        return mp.mpc(mp.mpf(s), 0)
    return mp.mpc(mp.mpf(s[:split]), mp.mpf(s[split:]))


def beta_bump(u: mp.mpf) -> mp.mpf:
    if abs(u) >= 1:
        return mp.mpf("0")
    return mp.e ** (-1 / (1 - u * u))


CENTERS = [mp.mpf("1.5"), mp.mpf("2.5"), mp.mpf("3.5")]
EPS = mp.mpf("0.20")
COEFFS = [mp.mpf("1"), mp.mpf("-3.3409952306"), mp.mpf("2.3409952306")]


def M_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for c, a in zip(CENTERS, COEFFS):
            lo, hi = c - EPS, c + EPS

            def integrand(t: mp.mpf, cc: mp.mpf = c, aa: mp.mpf = a, nn: int = n) -> mp.mpc:
                return aa * beta_bump((t - cc) / EPS) * (t ** (-s)) * ((-mp.log(t)) ** nn)

            total += mp.quad(integrand, [lo, hi])
        out.append(total)
    return out


def zeta_derivatives(s: mp.mpc, max_k: int) -> list[mp.mpc]:
    return [mp.zeta(s, derivative=n) for n in range(max_k + 1)]


def dirichlet_L_derivatives(s: mp.mpc, q: int, chi: list[mp.mpc], max_k: int) -> list[mp.mpc]:
    logq = mp.log(q)
    q_factor = mp.mpf(q) ** (-s)
    zeta_sums: list[mp.mpc] = []
    for m in range(max_k + 1):
        zeta_sums.append(
            mp.fsum([chi[a % q] * mp.zeta(s, mp.mpf(a) / q, derivative=m) for a in range(1, q + 1)])
        )
    out: list[mp.mpc] = []
    for n in range(max_k + 1):
        total = mp.mpc(0)
        for m in range(n + 1):
            total += mp.mpf(math.comb(n, m)) * ((-logq) ** (n - m)) * zeta_sums[m]
        out.append(q_factor * total)
    return out


def h_derivative(fds: list[mp.mpc], mds: list[mp.mpc], k: int) -> mp.mpc:
    return mp.fsum([mp.mpf(math.comb(k, j)) * fds[j] * mds[k - j] for j in range(k + 1)])


def character_from_prime_generator(q: int, generator: int, exponent: int) -> list[mp.mpc]:
    chi = [mp.mpc(0) for _ in range(q)]
    root = mp.e ** (2 * mp.pi * mp.j * mp.mpf(exponent) / (q - 1))
    residue = 1
    value = mp.mpc(1)
    for _ in range(q - 1):
        chi[residue] = value
        residue = (residue * generator) % q
        value *= root
    return chi


def legendre_character(q: int) -> list[mp.mpc]:
    chi = [mp.mpc(0) for _ in range(q)]
    for a in range(1, q):
        chi[a] = mp.mpc(1 if pow(a, (q - 1) // 2, q) == 1 else -1)
    return chi


def char_values(label: str) -> tuple[int, list[mp.mpc]]:
    I = mp.j
    if label == "chi_3":
        return 3, [0, 1, -1]
    if label == "chi_4":
        return 4, [0, 1, 0, -1]
    if label == "chi_5a":
        return 5, [0, 1, -1, -1, 1]
    if label == "chi_5b":
        return 5, [0, 1, I, -I, -1]
    if label == "chi_7b":
        return 7, character_from_prime_generator(7, 3, 1)
    if label == "chi_11c":
        return 11, character_from_prime_generator(11, 2, 1)
    if label == "chi_13a":
        return 13, legendre_character(13)
    raise ValueError(label)


def roots() -> dict[str, mp.mpc]:
    rows = read_csv(STEP320 / "L_chi_first_zeros_step320.csv")
    out = {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}
    # These are the Step 329 roots for the requested labels.  They supersede
    # the prompt's inherited chi_7b/chi_11c approximations, which correspond to
    # the Step 322 quadratic rows chi_7a/chi_11a.
    out["chi_7b"] = mp.mpc(mp.mpf("0.5"), mp.mpf("5.198116199466545586084284074304"))
    out["chi_11c"] = mp.mpc(mp.mpf("0.5"), mp.mpf("3.5470410917194500766644763717657"))
    out["chi_13a"] = mp.mpc(mp.mpf("0.5"), mp.mpf("3.1193414790086034139016"))
    return out


def load_step320_training_values() -> dict[str, dict[int, mp.mpc]]:
    data = {ch: {} for ch in OLD_CHARS}
    for row in read_csv(STEP320 / "hecke_L_k_values_step320.csv"):
        ch = row["character"]
        k = int(row["k"])
        if ch in data and k in FIT_K:
            data[ch][k] = parse_complex(row["h_derivative_complex"])
    return data


def solve_weighted_complex_ls(values: dict[str, dict[int, mp.mpc]], target: dict[int, mp.mpc], ks: list[int]) -> dict[str, mp.mpc]:
    n = len(ALL_CHARS)
    AH_A = mp.matrix(n, n)
    AH_b = mp.matrix(n, 1)
    for i, ci in enumerate(ALL_CHARS):
        for j, cj in enumerate(ALL_CHARS):
            AH_A[i, j] = mp.fsum([
                mp.conj(values[ci][k] / abs(target[k])) * (values[cj][k] / abs(target[k]))
                for k in ks
            ])
        AH_b[i] = mp.fsum([
            mp.conj(values[ci][k] / abs(target[k])) * (target[k] / abs(target[k]))
            for k in ks
        ])
    sol = mp.lu_solve(AH_A, AH_b)
    return {ch: sol[i] for i, ch in enumerate(ALL_CHARS)}


def residual_row(k: int, values: dict[str, dict[int, mp.mpc]], target: dict[int, mp.mpc], coeffs: dict[str, mp.mpc], row_type: str, step337_rel: str = "") -> dict[str, object]:
    pred = mp.fsum([coeffs[ch] * values[ch][k] for ch in ALL_CHARS])
    res = target[k] - pred
    rel = abs(res) / abs(target[k])
    return {
        "row_type": row_type,
        "k": k,
        "character": "all",
        "coefficient_real": "",
        "coefficient_imag": "",
        "zeta_target_abs": mp.nstr(abs(target[k]), 18),
        "fit_abs": mp.nstr(abs(pred), 18),
        "residual_abs": mp.nstr(abs(res), 18),
        "relative_residual": mp.nstr(rel, 12),
        "step337_4char_relative_residual": step337_rel,
        "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
    }


def step337_residuals() -> dict[int, str]:
    out: dict[int, str] = {}
    for row in read_csv(STEP337 / "bridge_coefficient_fit_step337.csv"):
        if row["row_type"] == "complex_fit_residual":
            out[int(row["k"])] = row["relative_residual"]
    return out


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    max_k = max(ALL_K)
    rho_by_char = roots()

    values: dict[str, dict[int, mp.mpc]] = {ch: {} for ch in ALL_CHARS}
    values.update(load_step320_training_values())
    additional_rows: list[dict[str, object]] = []

    # Compute all new character values through k=20, and old-character holdouts.
    for ch in ALL_CHARS:
        q, chi = char_values(ch)
        rho = rho_by_char[ch]
        t0 = time.time()
        Lds = dirichlet_L_derivatives(rho, q, chi, max_k)
        Mds = M_derivatives(rho, max_k)
        runtime = time.time() - t0
        for k in ALL_K:
            if ch in OLD_CHARS and k in FIT_K and k in values[ch]:
                raw = values[ch][k]
                source = "loaded_step320_for_training_consistency"
            else:
                raw = h_derivative(Lds, Mds, k)
                values[ch][k] = raw
                source = "computed_step338"
            if ch in NEW_CHARS and k in FIT_K:
                additional_rows.append({
                    "character": ch,
                    "k": k,
                    "rho_chi": cstr(rho, 30),
                    "h_derivative_real": mp.nstr(mp.re(raw), 30),
                    "h_derivative_imag": mp.nstr(mp.im(raw), 30),
                    "h_derivative_abs": mp.nstr(abs(raw), 18),
                    "source": source,
                    "dps": DPS,
                    "runtime_for_character_seconds": f"{runtime:.3f}",
                })

    # Branch C zeta targets.
    rho1 = mp.zetazero(1)
    zds = zeta_derivatives(rho1, max_k)
    mds1 = M_derivatives(rho1, max_k)
    target = {k: h_derivative(zds, mds1, k) for k in ALL_K}

    coeffs = solve_weighted_complex_ls(values, target, FIT_K)
    old_resids = step337_residuals()

    fit_rows: list[dict[str, object]] = []
    for ch in ALL_CHARS:
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
            "step337_4char_relative_residual": "",
            "verdict": "least_squares_coefficient_weighted_by_target_abs",
        })

    max_train = mp.mpf("0")
    for k in FIT_K:
        row = residual_row(k, values, target, coeffs, "complex_fit_residual", old_resids.get(k, ""))
        max_train = max(max_train, mp.mpf(row["relative_residual"]))
        fit_rows.append(row)

    holdout_rows: list[dict[str, object]] = []
    max_holdout = mp.mpf("0")
    for k in HOLDOUT_K:
        row = residual_row(k, values, target, coeffs, "holdout_residual")
        max_holdout = max(max_holdout, mp.mpf(row["relative_residual"]))
        holdout_rows.append({
            "k": k,
            "zeta_target_abs": row["zeta_target_abs"],
            "fit_abs": row["fit_abs"],
            "residual_abs": row["residual_abs"],
            "relative_residual": row["relative_residual"],
            "verdict": row["verdict"],
        })

    write_csv(ART / "additional_hecke_evaluators_step338.csv", additional_rows)
    write_csv(ART / "extended_bridge_fit_step338.csv", fit_rows)
    write_csv(ART / "cross_validation_step338.csv", holdout_rows)

    train_pass = max_train < mp.mpf("0.01")
    holdout_pass = max_holdout < mp.mpf("0.01")
    if train_pass and holdout_pass:
        verdict = "V_hecke_H6_extended_bridge_candidate_verified_numerically"
        bridge_claimed = True
    elif train_pass:
        verdict = "V_hecke_H6_extended_fit_overfit_holdout_fails"
        bridge_claimed = False
    else:
        verdict = "V_hecke_H6_extended_fit_still_fails_missing_descent"
        bridge_claimed = False

    summary = [
        "# Step 338 Results Summary",
        "",
        "Constructive H6 bridge extension using the Step 337 four-character fit plus Step 329 characters `chi_7b`, `chi_11c`, and `chi_13a`.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.",
        "- Step 322 prompt/inheritance named `chi_7b` near `0.5+4.4757i` and `chi_11c` near `0.5+2.4772i`, but Step 329's actual labels give `chi_7b=0.5+5.198116199466545586084284074304i` and `chi_11c=0.5+3.5470410917194500766644763717657i`; those Step 329 roots were used for the requested labels.",
        "- Step 329: `chi_13a` uses `rho=0.5+3.1193414790086034139016i`.",
        "- Step 337: four-character residuals were `0.342, 0.131, 0.039, 0.007, 0.008, 0.005, 0.0007, 0.001, 0.0003, 1.7e-5` over `k=1..10`.",
        "",
        f"Seven-character weighted complex fit max training residual over k=1..10: `{mp.nstr(max_train, 12)}`.",
        f"Holdout max residual over k=11,12,15,20: `{mp.nstr(max_holdout, 12)}`.",
        "",
        "Interpretation:",
        "A numerical coefficient fit is only a finite-dimensional interpolation unless it also holds out of sample and is backed by a carrier/projection/kernel-preserving descent theorem. The holdout rows are therefore decisive for the H6 bridge claim boundary.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step338_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 338,
        "orientation": "constructive",
        "target": "extended Hecke H6 bridge fit with chi_7b, chi_11c, chi_13a",
        "dps": DPS,
        "characters": ALL_CHARS,
        "fit_k": FIT_K,
        "holdout_k": HOLDOUT_K,
        "mellin_convention": "t^{-s}",
        "max_training_relative_residual": mp.nstr(max_train, 18),
        "max_holdout_relative_residual": mp.nstr(max_holdout, 18),
        "bridge_claimed": bridge_claimed,
        "final_verdict": verdict,
        "label_note": "Step 329 roots used for requested chi_7b/chi_11c labels; prompt inherited roots match Step 322 quadratic rows.",
    }
    (ART / "step338_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 338 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- A finite least-squares fit is not a Hecke-to-Burnol zeta-fiber descent theorem.",
        "- H6 is only bridge-resolved if all training and holdout residuals are below 1% and the result is interpreted as a numerical bridge candidate, not a proof.",
        "- If holdout fails, the missing object remains a carrier/projection/kernel-preserving descent from Hecke spaces to the Burnol/Sonine zeta residual.",
    ]
    (ART / "nonclaim_boundary_step338.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_train_rel={mp.nstr(max_train, 12)}")
    print(f"max_holdout_rel={mp.nstr(max_holdout, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
