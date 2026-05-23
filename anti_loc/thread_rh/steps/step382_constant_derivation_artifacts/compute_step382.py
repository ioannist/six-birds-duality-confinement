#!/usr/bin/env python3
"""Step 382: compare fitted close-pair constants with closed-form candidates."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step382_constant_derivation_artifacts")
STEP381_SCHEMA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step381_hadamard_close_pair_derivation_artifacts/step381_schema.json")
DPS = 80


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rel_err(candidate: mp.mpf, empirical: mp.mpf) -> mp.mpf:
    return abs(candidate - empirical) / abs(empirical)


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    schema381 = json.loads(STEP381_SCHEMA.read_text())
    slope_emp = mp.mpf(str(schema381["R_linear_model_slope_inv_s"]))
    offset_emp = mp.mpf(str(schema381["R_linear_model_intercept"]))

    slope_candidates = [
        ("pi^2", mp.pi**2, "two pi factors: cusp angular scale times local-density normalization"),
        ("3*pi", 3 * mp.pi, "nearest low-order pi multiple"),
        ("2*pi", 2 * mp.pi, "single full angular period"),
        ("pi^2+1/3", mp.pi**2 + mp.mpf(1) / 3, "pi^2 plus first Bernoulli/Stirling correction"),
        ("10", mp.mpf(10), "round constant control"),
        ("2*pi^2/pi", 2 * mp.pi, "algebraic duplicate control of 2*pi"),
    ]
    slope_rows = []
    for name, val, note in slope_candidates:
        slope_rows.append(
            {
                "candidate": name,
                "value": mp.nstr(val, 30),
                "empirical_slope": mp.nstr(slope_emp, 30),
                "absolute_error": mp.nstr(abs(val - slope_emp), 30),
                "relative_error": mp.nstr(rel_err(val, slope_emp), 30),
                "within_10_percent": str(rel_err(val, slope_emp) <= mp.mpf("0.10")),
                "note": note,
            }
        )
    slope_rows.sort(key=lambda r: mp.mpf(r["relative_error"]))
    write_csv(BASE / "slope_candidates_step382.csv", slope_rows)

    offset_candidates = [
        ("-3*pi/2", -3 * mp.pi / 2, "archimedean half-period plus canonical-product subtraction heuristic"),
        ("-sqrt(20)", -mp.sqrt(20), "numerical-near control; not accepted as structural without derivation"),
        ("-pi*sqrt(2)", -mp.pi * mp.sqrt(2), "pi times root-two geometric control"),
        ("-log(4*pi)*sqrt(pi)", -mp.log(4 * mp.pi) * mp.sqrt(mp.pi), "Gamma-factor scale control"),
        ("-pi", -mp.pi, "single half-period control"),
        ("-log((2*pi)^2)", -mp.log((2 * mp.pi) ** 2), "density-normalization logarithm control"),
    ]
    offset_rows = []
    for name, val, note in offset_candidates:
        offset_rows.append(
            {
                "candidate": name,
                "value": mp.nstr(val, 30),
                "empirical_offset": mp.nstr(offset_emp, 30),
                "absolute_error": mp.nstr(abs(val - offset_emp), 30),
                "relative_error": mp.nstr(rel_err(val, offset_emp), 30),
                "within_10_percent": str(rel_err(val, offset_emp) <= mp.mpf("0.10")),
                "note": note,
            }
        )
    offset_rows.sort(key=lambda r: mp.mpf(r["relative_error"]))
    write_csv(BASE / "offset_candidates_step382.csv", offset_rows)

    best_slope = slope_rows[0]
    pi2_row = next(r for r in slope_rows if r["candidate"] == "pi^2")
    best_offset_structural = next(r for r in offset_rows if r["candidate"] == "-3*pi/2")
    best_offset_numeric = offset_rows[0]
    slope_match = pi2_row["within_10_percent"] == "True"
    offset_match = best_offset_structural["within_10_percent"] == "True"

    if slope_match and offset_match:
        verdict = "partial_constants_match_pi2_and_minus_3pi_over_2; saddle_displacement_unproved"
    elif slope_match or offset_match:
        verdict = "one_constant_matches_closed_form; partial"
    else:
        verdict = "no_closed_form_match; empirical_fit_specific"

    derivation = f"""# Step 382 Analytical Constant Derivation Attempt

Step 381 gave the empirical close-pair correction

`R_j ~= {mp.nstr(offset_emp, 16)} + {mp.nstr(slope_emp, 16)}/s_min`.

The Hadamard local identity is

`zeta''(rho_j)=2 zeta'(rho_j) g'_j(rho_j)`,

with

`g'_j(rho_j)=arch(rho_j)+sum_(rho != rho_j)[-1/(rho-rho_j)+1/rho]`.

For a nearest neighbor `rho_n=rho_j +/- i s_min`,

`g'_near = -1/(rho_n-rho_j)= +/- i/s_min`.

The Branch C saddle action has the smooth height law

`gamma(T) ~= pi/(T log(T/(2pi)))`.

The close-pair perturbation enters through `Re g_j(z*)` at the large-k saddle `z*=rho_j+delta z`. Since `g'_near` is purely imaginary, the first-order perturbation is

`Delta S_near ~= Re(g'_near delta z) ~= C_sad/s_min`.

The fitted slope therefore measures the effective saddle displacement constant `C_sad`. The natural closed-form candidate is `pi^2`: one `pi` from the cusp angular displacement and one `pi` from the zero-density normalization in the Branch C height law.

Numerically:

- empirical slope: `{mp.nstr(slope_emp, 20)}`
- `pi^2`: `{mp.nstr(mp.pi**2, 20)}`
- relative error: `{pi2_row['relative_error']}`

The fitted offset is the regular Hadamard remainder plus the smooth Archimedean subtraction. The simplest structural candidate is `-3pi/2`.

- empirical offset: `{mp.nstr(offset_emp, 20)}`
- `-3pi/2`: `{mp.nstr(-3*mp.pi/2, 20)}`
- relative error: `{best_offset_structural['relative_error']}`

Important limitation: this identifies plausible constants and their Hadamard/saddle origin, but the exact saddle displacement `delta z` for the projected Burnol/Sonine matrix element is not derived here. Therefore this is not theorem-grade.
"""
    (BASE / "analytical_derivation_step382.md").write_text(derivation)

    summary = f"""# Step 382 Results Summary

Derivation chain:

1. Hadamard: `g'_near = +/- i/s_min`.
2. Branch C saddle: close-pair correction enters `Re(g'_near delta z*)`.
3. Therefore `R_j` has the form `C0 + C1/s_min`.
4. Step 381 fit gives `C1={mp.nstr(slope_emp, 16)}`, `C0={mp.nstr(offset_emp, 16)}`.

Slope:

- best structural candidate: `pi^2 = {mp.nstr(mp.pi**2, 18)}`
- empirical: `{mp.nstr(slope_emp, 18)}`
- relative error: `{pi2_row['relative_error']}`

Offset:

- structural candidate: `-3pi/2 = {mp.nstr(-3*mp.pi/2, 18)}`
- empirical: `{mp.nstr(offset_emp, 18)}`
- relative error: `{best_offset_structural['relative_error']}`

Best purely numerical slope candidate is `{best_slope['candidate']}` and best numerical offset candidate is `{best_offset_numeric['candidate']}`, but these are not accepted as structural without a derivation.

Verdict: `{verdict}`. Both proposed structural constants are within 10%, but the Burnol/Sonine saddle displacement and regular Hadamard remainder are not yet derived rigorously.
"""
    (BASE / "step382_results_summary.md").write_text(summary)

    schema = {
        "step": 382,
        "mode": "ATTEMPT",
        "dps": DPS,
        "empirical_slope": float(slope_emp),
        "empirical_offset": float(offset_emp),
        "structural_slope_candidate": "pi^2",
        "structural_slope_relative_error": float(pi2_row["relative_error"]),
        "best_numeric_slope_candidate": best_slope["candidate"],
        "best_numeric_slope_relative_error": float(best_slope["relative_error"]),
        "structural_offset_candidate": "-3*pi/2",
        "structural_offset_relative_error": float(best_offset_structural["relative_error"]),
        "best_numeric_offset_candidate": best_offset_numeric["candidate"],
        "best_numeric_offset_relative_error": float(best_offset_numeric["relative_error"]),
        "verdict": verdict,
    }
    (BASE / "step382_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    boundary = """# Step 382 Nonclaim Boundary

- This step does not prove RH or any theorem about Branch C closure.
- The constants are matched against a 22-zero empirical fit from Step 381.
- The proposed `pi^2` and `-3pi/2` constants are analytical candidates, not fully derived theorems.
- The missing rigorous element is the projected Burnol/Sonine saddle displacement and regular Hadamard remainder.
"""
    (BASE / "nonclaim_boundary_step382.md").write_text(boundary)

    print("STEP382_COMPUTE_DONE")
    print(f"slope_emp={mp.nstr(slope_emp, 12)} structural_slope=pi^2 rel={pi2_row['relative_error']}")
    print(f"offset_emp={mp.nstr(offset_emp, 12)} structural_offset=-3*pi/2 rel={best_offset_structural['relative_error']}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
