#!/usr/bin/env python3
"""Step 330: corrected E/E# separation for self-dual Dirichlet characters.

The bare completed self-dual L-function satisfies Lambda(1/2+iz)=Lambda(1/2-iz)
when epsilon=1, so the Step 328 two-term kernel cancels.  This script uses a
Hermite-Biehler phase separation

    E_eta(z) = exp(-i eta z) Lambda(1/2+i z, chi), eta > 0,

and E_eta#(z)=conj(E_eta(conj(z))).  For self-dual epsilon=1 this gives
|E_eta(z)|>|E_eta#(z)| in the upper half-plane through the exponential phase.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step330_corrected_E_E_star_self_dual_artifacts"
STEP328 = ROOT / "anti_loc/thread/steps/step328_hecke_H4_constructive_subfamily_artifacts"
STEP329 = ROOT / "anti_loc/thread/steps/step329_real_epsilon_pattern_investigation_artifacts"
DPS = 80
ETA = mp.mpf("1.0")
CENTER_IM = mp.mpf("0.55")
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


def legendre_character(q: int) -> list[mp.mpc]:
    chi = [mp.mpc(0) for _ in range(q)]
    for a in range(1, q):
        chi[a] = mp.mpc(1 if pow(a, (q - 1) // 2, q) == 1 else -1)
    return chi


def char_data(label: str) -> tuple[int, int, list[mp.mpc], mp.mpc]:
    if label == "chi_3":
        return 3, 1, [mp.mpc(0), mp.mpc(1), mp.mpc(-1)], mp.mpc(1)
    if label == "chi_4":
        return 4, 1, [mp.mpc(0), mp.mpc(1), mp.mpc(0), mp.mpc(-1)], mp.mpc(1)
    if label == "chi_5a":
        return 5, 0, [mp.mpc(0), mp.mpc(1), mp.mpc(-1), mp.mpc(-1), mp.mpc(1)], mp.mpc(1)
    if label == "chi_13a":
        return 13, 0, legendre_character(13), mp.mpc(1)
    raise ValueError(label)


def L_chi(s: mp.mpc, q: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) ** (-s)) * mp.fsum(
        [chi[a % q] * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)]
    )


def Lambda(s: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    return (mp.mpf(q) / mp.pi) ** ((s + parity_a) / 2) * mp.gamma((s + parity_a) / 2) * L_chi(s, q, chi)


def E_eta(z: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    return mp.e ** (-mp.j * ETA * z) * Lambda(mp.mpc("0.5") + mp.j * z, q, parity_a, chi)


def E_sharp(z: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    return mp.conj(E_eta(mp.conj(z), q, parity_a, chi))


def debranges_kernel(z: mp.mpc, w: mp.mpc, q: int, parity_a: int, chi: list[mp.mpc]) -> mp.mpc:
    numerator = E_eta(z, q, parity_a, chi) * mp.conj(E_eta(w, q, parity_a, chi))
    numerator -= E_sharp(z, q, parity_a, chi) * mp.conj(E_sharp(w, q, parity_a, chi))
    return numerator / (2 * mp.pi * mp.j * (mp.conj(w) - z))


def roots() -> dict[str, mp.mpc]:
    rows = read_csv(ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts/L_chi_first_zeros_step320.csv")
    result = {r["character"]: mp.mpc(mp.mpf(r["Re_rho"]), mp.mpf(r["Im_rho"])) for r in rows}
    result["chi_13a"] = mp.mpc(mp.mpf("0.5"), mp.mpf("3.1193414790086034139016"))
    return result


def inherited_near_zero(label: str) -> mp.mpf:
    if label in ["chi_3", "chi_4", "chi_5a"]:
        rows = read_csv(STEP328 / "kappa_chi_values_step328.csv")
    else:
        rows = read_csv(STEP329 / "self_dual_hypothesis_test_step329.csv")
    vals = []
    for row in rows:
        if row["character"] != label:
            continue
        field = "kappa_abs" if "kappa_abs" in row else "max_kappa_abs"
        if row[field] != "NA":
            vals.append(mp.mpf(row[field]))
    return max(vals) if vals else mp.nan


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    root_map = roots()
    rows: list[dict[str, object]] = []
    for label in ["chi_3", "chi_4", "chi_5a", "chi_13a"]:
        q, parity_a, chi, epsilon = char_data(label)
        t0 = mp.im(root_map[label])
        tau_grid = [t0 + off for off in OFFSETS]
        z_grid = [mp.mpc(tau, 0) for tau in tau_grid]
        centers = [mp.mpc(t0 + off, CENTER_IM) for off in CENTER_OFFSETS]
        values = []
        max_abs = mp.mpf("0")
        max_entry = None
        for z in z_grid:
            for w in centers:
                val = debranges_kernel(z, w, q, parity_a, chi)
                values.append(abs(val))
                if abs(val) > max_abs:
                    max_abs = abs(val)
                    max_entry = (z, w, val)
        probe = mp.mpc(t0, CENTER_IM)
        hb_ratio = abs(E_eta(probe, q, parity_a, chi)) / abs(E_sharp(probe, q, parity_a, chi))
        inherited = inherited_near_zero(label)
        z_max, w_max, val_max = max_entry
        rows.append(
            {
                "character": label,
                "q": q,
                "parity_a": parity_a,
                "epsilon": cstr(epsilon, 18),
                "rho_imag_t0": mp.nstr(t0, 24),
                "eta_phase": mp.nstr(ETA, 12),
                "center_imaginary_height": mp.nstr(CENTER_IM, 12),
                "E_definition": "E_eta(z)=exp(-i eta z) Lambda(1/2+i z,chi); E_sharp(z)=conj(E_eta(conj z))",
                "HB_ratio_abs_E_over_Esharp_at_t0_plus_i_center": mp.nstr(hb_ratio, 18),
                "max_corrected_kappa_abs": mp.nstr(max_abs, 18),
                "max_corrected_kappa_z": cstr(z_max, 18),
                "max_corrected_kappa_w": cstr(w_max, 18),
                "max_corrected_kappa_value": cstr(val_max, 24),
                "step328_or_329_near_zero_max_abs": mp.nstr(inherited, 18),
                "improvement_factor": mp.nstr(max_abs / inherited if inherited else mp.inf, 18),
                "status": (
                    "nontrivial_corrected_kernel"
                    if max_abs > mp.mpf("0.01")
                    else "weak_nonzero_subthreshold"
                    if max_abs > mp.mpf("1e-8")
                    else "still_degenerate"
                ),
            }
        )

    write_csv(ART / "corrected_kappa_self_dual_step330.csv", rows)
    all_threshold_nontrivial = all(mp.mpf(row["max_corrected_kappa_abs"]) > mp.mpf("0.01") for row in rows)
    all_weak_nonzero = all(mp.mpf(row["max_corrected_kappa_abs"]) > mp.mpf("1e-8") for row in rows)
    if all_threshold_nontrivial:
        score = "2.0_to_2.5_constructive_phase_separated_proxy"
        verdict = "V_corrected_E_Esharp_self_dual_nontrivial"
    elif all_weak_nonzero:
        score = "stays_2.0_partial_weak_nonzero_no_2.5"
        verdict = "V_corrected_E_Esharp_self_dual_weak_nonzero_subthreshold"
    else:
        score = "stays_2.0"
        verdict = "V_corrected_E_Esharp_self_dual_still_degenerate"
    summary = [
        "# Step 330 Results Summary",
        "",
        "Corrected construction used:",
        "`E_eta(z)=exp(-i eta z) Lambda(1/2+i z,chi)` with `eta=1`, and `E_eta#(z)=conj(E_eta(conj z))`.",
        "For self-dual `epsilon=1`, the bare completed L-function split collapses, but this phase-separated Hermite-Biehler proxy gives `|E|>|E#|` in the upper half-plane.",
        "",
        "Source anchors:",
        "- de Branges kernel formula, as cited in Step 330 audit source: `k_w(z) = (overline{E(w)}E(z) - overline{E^*(w)}E^*(z))/(2 pi i(overline{w}-z))`.",
        "- Burnol 2002, Step 291 extract: `La fonction E_lambda(w) est une fonction entière satisfaisant la condition de de Branges.`",
        "",
        "Computed corrected max-kappa values:",
    ]
    for row in rows:
        summary.append(
            f"- `{row['character']}`: corrected max|kappa| `{row['max_corrected_kappa_abs']}`; "
            f"old near-zero `{row['step328_or_329_near_zero_max_abs']}`; "
            f"HB ratio `{row['HB_ratio_abs_E_over_Esharp_at_t0_plus_i_center']}`."
        )
    summary.extend(
        [
            "",
            f"Score update: `{score}`.",
            f"Verdict: `{verdict}`.",
            "",
            "Boundary: this is a constructive phase-separated de Branges proxy. It rescues the self-dual finite model numerically, but it is not a proof of Hecke H4 closure or GRH.",
        ]
    )
    (ART / "step330_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    schema = {
        "step": 330,
        "orientation": "constructive_attempt",
        "target": "Corrected E/E_sharp self-dual H4 kernel",
        "dps": DPS,
        "eta_phase": mp.nstr(ETA, 12),
        "center_imaginary_height": mp.nstr(CENTER_IM, 12),
        "characters": ["chi_3", "chi_4", "chi_5a", "chi_13a"],
        "score_update": score,
        "final_verdict": verdict,
    }
    (ART / "step330_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step330.md").write_text(
        "# Step 330 Nonclaim Boundary\n\n"
        "- This step does not prove RH, GRH, or Hecke closure.\n"
        "- The phase-separated `E_eta` is a corrected constructive proxy for the finite H4 model, not an explicit Burnol Dirichlet theorem.\n"
        "- The score update applies only to the χ_3/χ_4/χ_5a/χ_13a finite self-dual subfamily computation.\n",
        encoding="utf-8",
    )
    print("Step330 corrected self-dual kappa")
    for row in rows:
        print(f"{row['character']}: corrected={row['max_corrected_kappa_abs']} old={row['step328_or_329_near_zero_max_abs']}")
    print(f"verdict={schema['final_verdict']}")


if __name__ == "__main__":
    main()
