#!/usr/bin/env python3
"""Step 388: asymptotic-large-sieve H6 attack attempt.

The key test is whether the cascade Hecke evaluator can be placed into the
large-sieve form sum_n alpha_n chi(n) with alpha_n independent of chi across a
family.  It cannot: the cascade evaluates each character at its own first zero
rho_chi, so the formal coefficients alpha_n^{(chi,k)} depend on chi.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step388_large_sieve_H6_attack_artifacts")
STEP320 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts")
STEP321 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step321_hecke_high_k_universality_artifacts")
STEP322 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step322_gamma_G_invariance_test_artifacts")
STEP383 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step383_extended_close_pair_validation_artifacts")
STEP322_SCRIPT = STEP322 / "compute_L_k_more_instances_step322.py"

DPS = 60
K_VALUES = [5, 10, 15, 20, 30]
COEFF_K = [5, 10]
N_TRUNC = 25
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7a", "chi_8a", "chi_11a"]


def load_step322():
    spec = importlib.util.spec_from_file_location("step322_for_step388", STEP322_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP322_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 24) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def roots() -> dict[str, mp.mpc]:
    out: dict[str, mp.mpc] = {}
    for row in read_csv(STEP320 / "L_chi_first_zeros_step320.csv"):
        out[row["character"]] = mp.mpc(mp.mpf(row["Re_rho"]), mp.mpf(row["Im_rho"]))
    for row in read_csv(STEP322 / "critical_line_zeros_step322.csv"):
        obj = row["object"]
        if obj in CHARS:
            out[obj] = mp.mpc(mp.mpf(row["Re_rho"]), mp.mpf(row["Im_rho"]))
    return out


def hecke_values() -> dict[tuple[str, int], mp.mpf]:
    vals: dict[tuple[str, int], mp.mpf] = {}
    for row in read_csv(STEP320 / "hecke_L_k_values_step320.csv"):
        ch, k = row["character"], int(row["k"])
        if ch in CHARS and k in [5, 10]:
            vals[(ch, k)] = mp.mpf(row["h_derivative_abs"])
    for row in read_csv(STEP321 / "hecke_L_k_chi_high_k_step321.csv"):
        ch, k = row["character"], int(row["k"])
        if ch in CHARS and k in [15, 20, 30]:
            vals[(ch, k)] = mp.mpf(row["h_derivative_abs_raw"])
    for row in read_csv(STEP322 / "fitted_gamma_per_instance_step322.csv"):
        if row["family"] == "Dirichlet" and row["G"] == "G_star":
            ch = row["instance_id"].replace("_G_star", "")
            if ch in CHARS:
                for k in K_VALUES:
                    key = f"k{k}_abs"
                    if row.get(key):
                        vals[(ch, k)] = mp.mpf(row[key])
    return vals


def zeta_values() -> dict[tuple[int, int], mp.mpf]:
    vals: dict[tuple[int, int], mp.mpf] = {}
    for row in read_csv(STEP383 / "gamma_R_table_100_zeros_step383.csv"):
        j = int(row["j"])
        if j <= len(CHARS):
            for k in K_VALUES:
                vals[(j, k)] = mp.mpf(row[f"k{k}_abs_delta_proxy"])
    return vals


def main() -> None:
    mp.mp.dps = DPS
    ART.mkdir(parents=True, exist_ok=True)
    step322 = load_step322()
    rhos = roots()
    hvals = hecke_values()
    zvals = zeta_values()

    coeff_rows: list[dict[str, object]] = []
    diagonal_norms: dict[tuple[str, int], mp.mpf] = {}
    for ch in CHARS:
        q, _chi = step322.char_values(ch)
        rho = rhos[ch]
        Mds = step322.M_derivatives(rho, "G_star", max(COEFF_K))
        for k in COEFF_K:
            diag = mp.mpf("0")
            for n in range(1, N_TRUNC + 1):
                nn = mp.mpf(n)
                logn = mp.log(nn)
                poly = mp.mpc(0)
                for j in range(k + 1):
                    poly += mp.binomial(k, j) * Mds[k - j] * ((-logn) ** j)
                alpha = (nn ** (-rho)) * poly
                diag += abs(alpha) ** 2
                coeff_rows.append({
                    "character": ch,
                    "q": q,
                    "rho_chi": cstr(rho, 30),
                    "k": k,
                    "n": n,
                    "alpha_n_k_real": mp.nstr(mp.re(alpha), 24),
                    "alpha_n_k_imag": mp.nstr(mp.im(alpha), 24),
                    "abs_alpha_n_k": mp.nstr(abs(alpha), 24),
                    "coefficient_formula": "formal alpha_n^{chi,k}=n^{-rho_chi} sum_{j<=k} binom(k,j) M^{(k-j)}(rho_chi)(-log n)^j",
                    "large_sieve_hypothesis_status": "fails_common_alpha_condition_coefficients_depend_on_rho_chi",
                })
            diagonal_norms[(ch, k)] = diag

    comparison_rows: list[dict[str, object]] = []
    for k in K_VALUES:
        hecke_abs2 = [hvals[(ch, k)] ** 2 for ch in CHARS if (ch, k) in hvals]
        zeta_abs2 = [zvals[(j, k)] ** 2 for j in range(1, len(CHARS) + 1) if (j, k) in zvals]
        if not hecke_abs2 or not zeta_abs2:
            continue
        hecke_mean = mp.fsum(hecke_abs2) / len(hecke_abs2)
        zeta_mean = mp.fsum(zeta_abs2) / len(zeta_abs2)
        diag_proxy = ""
        diag_to_empirical = ""
        if k in COEFF_K:
            diag_vals = [diagonal_norms[(ch, k)] for ch in CHARS]
            diag_mean = mp.fsum(diag_vals) / len(diag_vals)
            diag_proxy = mp.nstr(diag_mean, 24)
            diag_to_empirical = mp.nstr(diag_mean / hecke_mean, 24)
        comparison_rows.append({
            "k": k,
            "hecke_family": "7 low-conductor primitive Dirichlet characters from steps 320-322",
            "hecke_count": len(hecke_abs2),
            "hecke_empirical_mean_abs2": mp.nstr(hecke_mean, 24),
            "zeta_baseline": "first 7 zeta zeros raw Step383 delta proxy",
            "zeta_count": len(zeta_abs2),
            "zeta_empirical_mean_abs2": mp.nstr(zeta_mean, 24),
            "hecke_over_zeta_mean_abs2": mp.nstr(hecke_mean / zeta_mean, 24),
            "truncated_diagonal_large_sieve_proxy_N25": diag_proxy,
            "diagonal_proxy_over_hecke_empirical": diag_to_empirical,
            "status": "diagnostic_only_CIS_asymptotic_inapplicable_to_7_character_rho_dependent_dataset",
        })

    write_csv(ART / "hecke_linear_form_step388.csv", coeff_rows)
    write_csv(ART / "family_averaged_comparison_step388.csv", comparison_rows)

    md = """# Step 388 Large-Sieve H6 Attack

## External Anchor

Conrey-Iwaniec-Soundararajan 2011, arXiv:1105.1176, "Asymptotic Large Sieve", gives asymptotics for bilinear / quadratic averages over primitive Dirichlet characters of Dirichlet-polynomial linear forms.  The usable schematic form is

`sum_chi |sum_n alpha_n chi(n)|^2 = diagonal main term + controlled off-diagonal/asymptotic terms`

provided the coefficient sequences and family parameters satisfy the paper's support and averaging hypotheses.

## Cascade Hecke Linear Form

For `h_chi(s)=L(s,chi) M(G_star)(s)`,

`h_chi^(k)(rho_chi) = sum_{n>=1} alpha_n^{(chi,k)} chi(n)`,

formally with

`alpha_n^{(chi,k)} = n^{-rho_chi} sum_{j=0}^k binom(k,j) M(G_star)^{(k-j)}(rho_chi)(-log n)^j`.

This is the requested linear-form structure, but it is not a CIS-ready family because `alpha_n` depends on `chi` through `rho_chi`.

## Applicability Result

The asymptotic large sieve needs a common coefficient sequence over the character family.  The cascade data evaluates each character at its own first zero, so the coefficient sequence changes with the character.  The available seven-character set is also finite, low-conductor, and far outside the asymptotic conductor family needed by the theorem.

## Verdict

The large-sieve route is technically meaningful only after a new cascade implementation fixes a common spectral parameter or rewrites the evaluator by an approximate functional equation with common coefficients.  With the present Step 320-322 data, it does not construct an averaged H6 bridge.
"""
    (ART / "large_sieve_bridge_attempt_step388.md").write_text(md)

    summary = [
        "# Step 388 Results Summary",
        "",
        "Citations from cascade records used verbatim:",
        "- Step 320: `Computed concrete Hecke-side Sonine evaluator pairings ... chi_3, chi_4, chi_5a, and chi_5b`.",
        "- Step 322: `test gamma invariance across L-functions and generators`.",
        "- Step 366-372: `gamma_zeta approx pi/(T log(T/(2pi)))` structural Branch C law.",
        "- Step 374: `gamma_Hecke_linear` apples-to-apples extraction.",
        "- Step 376: matched-normalization alignment identified as a Stirling-artifact diagnostic.",
        "- Step 385: exact `K_infty^op = delta - sinc - sum_n Psi_n Psi_n^*` but missing projected asymptotic.",
        "",
        f"Generated formal coefficient rows: `{len(coeff_rows)}`.",
        "Computed empirical seven-character family averages for k=5,10,15,20,30.",
        "",
        "Final verdict: `mismatch_large_sieve_common_alpha_condition_fails`.",
    ]
    (ART / "step388_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 388,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "external_anchor": "Conrey-Iwaniec-Soundararajan 2011 arXiv:1105.1176 Asymptotic Large Sieve",
        "characters": CHARS,
        "coefficient_rows": len(coeff_rows),
        "family_average_rows": len(comparison_rows),
        "mpmath_dps": DPS,
        "verdict": "mismatch_large_sieve_common_alpha_condition_fails",
        "implementation_gap": "need common spectral parameter or AFE Dirichlet-polynomial coefficients independent of chi",
    }
    (ART / "step388_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step388.md").write_text(
        "# Nonclaim Boundary - Step 388\n\n"
        "No RH claim is made. This step does not claim a Conrey-Iwaniec-Soundararajan "
        "theorem has been proved inside the cascade, and does not claim an H6 bridge. "
        "The output is an applicability audit plus a finite diagnostic comparison.\n"
    )

    print(schema["verdict"])
    print(f"coefficient_rows={len(coeff_rows)}")
    print(f"family_average_rows={len(comparison_rows)}")


if __name__ == "__main__":
    main()
