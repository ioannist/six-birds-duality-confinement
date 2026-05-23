#!/usr/bin/env python3
"""Step 348: KL-divergence virtual algebra calibration."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step348_mode_A_KL_calibration_artifacts"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts"
STEP338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts"
STEP343 = ROOT / "anti_loc/thread/steps/step343_zeta_internal_ratio_structure_artifacts"

DPS = 80
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
RHO = [1, 2, 3]
K_RANGE = list(range(1, 11))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_hecke_values() -> dict[str, list[mp.mpf]]:
    raw = {ch: {} for ch in CHARS}
    for row in read_csv(STEP320 / "hecke_L_k_values_step320.csv"):
        ch = row["character"]
        k = int(row["k"])
        if ch in raw and k in K_RANGE:
            raw[ch][k] = mp.mpf(row["h_derivative_abs"])
    for row in read_csv(STEP338 / "additional_hecke_evaluators_step338.csv"):
        ch = row["character"]
        k = int(row["k"])
        if ch in raw and k in K_RANGE:
            raw[ch][k] = mp.mpf(row["h_derivative_abs"])
    return {ch: [raw[ch][k] for k in K_RANGE] for ch in CHARS}


def load_zeta_values() -> dict[int, list[mp.mpf]]:
    raw = {j: {} for j in RHO}
    for row in read_csv(STEP343 / "zeta_ratios_step343.csv"):
        j = int(row["rho_index"])
        k = int(row["k"])
        if j in raw and k in K_RANGE:
            raw[j][k] = mp.mpf(row["abs_L_k"])
    return {j: [raw[j][k] for k in K_RANGE] for j in RHO}


def normalize(vals: list[mp.mpf]) -> list[mp.mpf]:
    total = mp.fsum(vals)
    return [v / total for v in vals]


def kl(p: list[mp.mpf], q: list[mp.mpf]) -> mp.mpf:
    return mp.fsum([pi * mp.log(pi / qi) for pi, qi in zip(p, q)])


def tv(p: list[mp.mpf], q: list[mp.mpf]) -> mp.mpf:
    return mp.mpf("0.5") * mp.fsum([abs(pi - qi) for pi, qi in zip(p, q)])


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS

    hecke = {ch: normalize(vals) for ch, vals in load_hecke_values().items()}
    zeta = {j: normalize(vals) for j, vals in load_zeta_values().items()}

    pair_rows = []
    pinsker_rows = []
    pair_stats = {}
    for ch in CHARS:
        for j in RHO:
            p = hecke[ch]
            q = zeta[j]
            D = kl(p, q)
            T = tv(p, q)
            bound = 2 * T * T
            margin = D - bound
            key = (ch, j)
            pair_stats[key] = (D, T, bound, margin)
            pair_rows.append({
                "character": ch,
                "rho_index": j,
                "k_support": "1..10",
                "KL_P_chi_given_Q_rho": mp.nstr(D, 18),
                "TV": mp.nstr(T, 18),
                "Pinsker_2TV2": mp.nstr(bound, 18),
                "Pinsker_margin": mp.nstr(margin, 18),
                "KL_nonnegative": "yes" if D >= 0 else "no",
            })
            pinsker_rows.append({
                "character": ch,
                "rho_index": j,
                "KL": mp.nstr(D, 18),
                "TV": mp.nstr(T, 18),
                "2TV2": mp.nstr(bound, 18),
                "KL_minus_2TV2": mp.nstr(margin, 18),
                "pinsker_holds": "yes" if margin >= -mp.mpf("1e-60") else "no",
                "independent_TV_computation": "0.5*sum_abs_P_minus_Q",
            })
    write_csv(ART / "KL_pairs_step348.csv", pair_rows)
    write_csv(ART / "pinsker_check_step348.csv", pinsker_rows)

    # Structural ablations: formulas still compute the same D and TV, so numeric
    # Pinsker reproduction does not break.  Proof-certificate labels change.
    ablation_rows = []
    for ablation in ["drop_nonnegativity_axiom", "drop_chain_rule_axiom"]:
        changed = 0
        failed = 0
        cert_fail = 0
        for ch in CHARS:
            for j in RHO:
                D, T, bound, margin = pair_stats[(ch, j)]
                numeric_holds = margin >= -mp.mpf("1e-60")
                if ablation == "drop_nonnegativity_axiom":
                    proof_certificate = "unavailable_for_KL_ge_0_and_Pinsker_certificate"
                    cert_fail += 1
                else:
                    proof_certificate = "unchanged_for_static_Pinsker;_chain_rule_not_used"
                ablation_rows.append({
                    "ablation": ablation,
                    "character": ch,
                    "rho_index": j,
                    "KL_original": mp.nstr(D, 18),
                    "KL_ablated": mp.nstr(D, 18),
                    "TV_original": mp.nstr(T, 18),
                    "TV_ablated": mp.nstr(T, 18),
                    "numeric_output_changed": "no",
                    "pinsker_numeric_holds_after_ablation": "yes" if numeric_holds else "no",
                    "proof_certificate_status": proof_certificate,
                })
                failed += int(not numeric_holds)
        ablation_rows.append({
            "ablation": ablation,
            "character": "SUMMARY",
            "rho_index": "",
            "KL_original": "",
            "KL_ablated": "",
            "TV_original": "",
            "TV_ablated": "",
            "numeric_output_changed": f"changed_pairs={changed}/21",
            "pinsker_numeric_holds_after_ablation": f"numeric_failures={failed}/21",
            "proof_certificate_status": f"certificate_failures={cert_fail}/21",
        })
    write_csv(ART / "ablation_KL_axiom_step348.csv", ablation_rows)

    pinsker_pass = sum(1 for r in pinsker_rows if r["pinsker_holds"] == "yes")
    min_margin = min(pair_stats[key][3] for key in pair_stats)
    max_kl = max(pair_stats[key][0] for key in pair_stats)
    max_pair = max(pair_stats, key=lambda key: pair_stats[key][0])
    verdict = "V_mode_A_KL_nominal_pinsker_passes_but_ablation_inert_cyclic_retract"

    summary = [
        "# Step 348 Results Summary",
        "",
        "Constructed the KL-divergence typed virtual algebra over k=1..10 normalized Branch C carrier distributions.",
        "",
        "Definitions:",
        "- `P_chi(k)=|L_k^chi|/sum_k |L_k^chi|`.",
        "- `Q_j(k)=|L_k(rho_j)|/sum_k |L_k(rho_j)|`.",
        "- `Delta_KL[P|Q]=sum_k P(k) log(P(k)/Q(k))`.",
        "",
        f"Computed `21` KL pairs. Pinsker checks passed `{pinsker_pass}/21`; minimum KL-2TV^2 margin `{mp.nstr(min_margin, 12)}`.",
        f"Largest KL pair: `{max_pair[0]}` vs `rho_{max_pair[1]}` with KL `{mp.nstr(max_kl, 12)}`.",
        "",
        "Substantive ablation:",
        "- Dropping non-negativity does not change numerical KL/TV/Pinsker outputs; it only removes the proof certificate.",
        "- Dropping chain rule also does not change numerical KL/TV/Pinsker outputs because the static Pinsker check does not use chain factorization.",
        "",
        "Interpretation: the information-divergence calculus earns a nominal Pinsker reproduction, but its listed axioms are not numerically load-bearing for this finite computation. This is a second Mode A cyclic retract, not a successful Stage I/II calibration.",
        "",
        f"Final verdict: `{verdict}`.",
    ]
    (ART / "step348_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 348,
        "orientation": "Mode A Stage I 2nd calibration",
        "target": "information-divergence typed KL algebra",
        "dps": DPS,
        "support_k": "1..10",
        "KL_pair_count": 21,
        "pinsker_pass_count": pinsker_pass,
        "ablation_numeric_output_changed": False,
        "mode_A_retract_count_update": 2,
        "final_verdict": verdict,
    }
    (ART / "step348_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 348 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- KL/Pinsker checks are finite distribution diagnostics, not an H6 bridge.",
        "- Because ablations do not alter numerical outputs, this calibration is not counted as a substantive Mode A success.",
    ]
    (ART / "nonclaim_boundary_step348.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"pinsker_pass={pinsker_pass}/21")
    print(f"min_margin={mp.nstr(min_margin, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
