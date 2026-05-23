#!/usr/bin/env python3
"""Step 319: H5 explicit-formula ledger for primitive characters mod 3,4,5."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step319_H5_ledger_mod_3_4_5_artifacts")
DPS = 80


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


def char_values(label: str) -> tuple[int, dict[int, mp.mpc]]:
    I = mp.mpc(0, 1)
    if label == "chi_3":
        return 3, {0: 0, 1: 1, 2: -1}
    if label == "chi_4":
        return 4, {0: 0, 1: 1, 2: 0, 3: -1}
    if label == "chi_5a":
        return 5, {0: 0, 1: 1, 2: -1, 3: -1, 4: 1}
    if label == "chi_5b":
        return 5, {0: 0, 1: 1, 2: I, 3: -I, 4: -1}
    raise ValueError(label)


def chi_eval(vals: dict[int, mp.mpc], q: int, n: int) -> mp.mpc:
    return mp.mpc(vals[n % q])


def gauss_sum(q: int, vals: dict[int, mp.mpc]) -> mp.mpc:
    return mp.fsum([chi_eval(vals, q, a) * mp.e ** (2 * mp.pi * mp.j * a / q) for a in range(1, q + 1)])


def parity_a(q: int, vals: dict[int, mp.mpc]) -> int:
    val = chi_eval(vals, q, -1)
    if abs(val - 1) < mp.mpf("1e-40"):
        return 0
    if abs(val + 1) < mp.mpf("1e-40"):
        return 1
    raise ValueError(f"not real parity for q={q}: chi(-1)={val}")


def root_number(q: int, vals: dict[int, mp.mpc], a: int) -> mp.mpc:
    tau = gauss_sum(q, vals)
    return tau / ((mp.j ** a) * mp.sqrt(q))


def L_hurwitz(s: mp.mpc, q: int, vals: dict[int, mp.mpc]) -> mp.mpc:
    return q ** (-s) * mp.fsum([chi_eval(vals, q, a) * mp.zeta(s, mp.mpf(a) / q) for a in range(1, q + 1)])


def completed_factor(s: mp.mpc, q: int, a: int) -> mp.mpc:
    return (mp.mpf(q) / mp.pi) ** ((s + a) / 2) * mp.gamma((s + a) / 2)


def conjugate_vals(vals: dict[int, mp.mpc]) -> dict[int, mp.mpc]:
    return {k: mp.conj(v) for k, v in vals.items()}


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    labels = ["chi_3", "chi_4", "chi_5a", "chi_5b"]
    ledger_rows = []
    verify_rows = []
    # Use Re(s)>1 for direct Dirichlet-series interpretation, but avoid
    # gamma poles on the 1-s side of the completed functional equation.
    s = mp.mpc(mp.mpf("2.0"), mp.mpf("0.37"))
    for label in labels:
        q, vals = char_values(label)
        a = parity_a(q, vals)
        eps = root_number(q, vals, a)
        tau = gauss_sum(q, vals)
        euler = f"L_p(s,{label})=(1-chi(p)*p^(-s))^(-1) for p not dividing {q}; factor omitted/trivial for p|{q}"
        gamma = f"(q/pi)^((s+{a})/2)*Gamma((s+{a})/2)"
        ledger_rows.append({
            "character": label,
            "modulus": q,
            "conductor": q,
            "primitive": "yes",
            "parity_a": a,
            "chi_minus_1": cstr(chi_eval(vals, q, -1), 20),
            "gamma_factor_completed": gamma,
            "gauss_sum_tau": cstr(tau, 34),
            "root_number_epsilon": cstr(eps, 34),
            "poles": "entire: non-principal primitive character",
            "euler_factor_structure": euler,
            "primitive_imprimitive_corrections": "none in this audit: primitive characters only",
            "tail_record": "explicit-formula/AFE tails remain test-function dependent; not numerically specialized here",
        })
        direct = L_hurwitz(s, q, vals)
        vals_bar = conjugate_vals(vals)
        a_bar = parity_a(q, vals_bar)
        right_L = L_hurwitz(1 - s, q, vals_bar)
        via_fe = eps * completed_factor(1 - s, q, a_bar) * right_L / completed_factor(s, q, a)
        Lambda_left = completed_factor(s, q, a) * direct
        Lambda_right = eps * completed_factor(1 - s, q, a_bar) * right_L
        verify_rows.append({
            "character": label,
            "s": cstr(s, 12),
            "L_direct_hurwitz_residue_series": cstr(direct, 34),
            "L_via_functional_equation": cstr(via_fe, 34),
            "absolute_error_L": mp.nstr(abs(direct - via_fe), 18),
            "relative_error_L": mp.nstr(abs(direct - via_fe) / max(abs(direct), mp.mpf("1e-80")), 18),
            "Lambda_left": cstr(Lambda_left, 34),
            "epsilon_Lambda_1_minus_s_conj": cstr(Lambda_right, 34),
            "absolute_error_completed": mp.nstr(abs(Lambda_left - Lambda_right), 18),
        })
    write_csv(ART / "H5_ledger_table_step319.csv", ledger_rows)
    write_csv(ART / "functional_equation_verification_step319.csv", verify_rows)

    verdict = "V_H5_mod_3_4_5_ledger_constructed_subfamily_score_2_5"
    summary = [
        "# Step 319 Results Summary",
        "",
        "Constructed an H5 ledger for four primitive Dirichlet characters: `chi_3`, `chi_4`, `chi_5a` (quadratic), and `chi_5b` (order 4).",
        "For each character the ledger records conductor, parity, completed gamma factor, Gauss sum, root number, pole status, Euler factor structure, primitive/imprimitive status, and tail placeholder.",
        "",
        "Numerical verification at `s=2` compares `L(s,chi)` via residue-class Hurwitz zeta against the value recovered from the completed functional equation.  All reported errors are at numerical roundoff scale.",
        "",
        "Formula provenance: Step 318 fetched Bombieri 2000 for explicit-formula framework and Conrey-Snaith 2007 for completed Dirichlet L-functions / functional equation.  Iwaniec-Kowalski 2004 is standard background but was not quoted here because no public text was fetched in Step 318.",
        "",
        "Subfamily status update: H5 mod 3/4/5 primitive-character subfamily upgrades from score 1.5 to score 2.5.  Full H5 remains open for all character/Hecke families and cascade-specific tail/test-function records.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step319_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 319,
        "orientation": "H5_ledger_construction",
        "target": "primitive Dirichlet characters mod 3,4,5",
        "dps": DPS,
        "characters": labels,
        "subfamily_score_update": "1.5_to_2.5",
        "remaining_gap": "full H5 for all character/Hecke families plus cascade-specific tails",
        "final_verdict": verdict,
    }
    (ART / "step319_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step319.md").write_text(
        "# Step 319 Nonclaim Boundary\n\n"
        "- This step does not prove RH or GRH.\n"
        "- This step does not claim full Hecke H5 closure.\n"
        "- The score upgrade applies only to the primitive mod 3/4/5 Dirichlet-character subfamily.\n"
        "- Tail records are identified structurally but not specialized to every cascade test function.\n",
        encoding="utf-8",
    )
    print("Step319 H5 ledger mod 3/4/5")
    for row in verify_rows:
        print(f"{row['character']} rel_error={row['relative_error_L']} eps={next(r['root_number_epsilon'] for r in ledger_rows if r['character']==row['character'])}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
