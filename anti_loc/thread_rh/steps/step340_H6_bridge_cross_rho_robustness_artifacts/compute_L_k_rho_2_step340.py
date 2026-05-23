#!/usr/bin/env python3
"""Step 340: cross-rho robustness test for the Step 339 product bridge."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import time
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step340_H6_bridge_cross_rho_robustness_artifacts"
STEP338_SCRIPT = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/compute_extended_bridge_step338.py"
STEP339 = ROOT / "anti_loc/thread/steps/step339_H6_multiplicative_bridge_artifacts"

DPS = 80
KS = [1, 2, 3, 5, 10, 15, 20]
CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]


def load_step338_module():
    spec = importlib.util.spec_from_file_location("step338_compute", STEP338_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Step 338 compute module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def load_step339_coefficients() -> tuple[mp.mpf, dict[str, mp.mpf]]:
    intercept = None
    coeffs: dict[str, mp.mpf] = {}
    for row in read_csv(STEP339 / "multiplicative_fit_step339.csv"):
        if row["model"] != "unconstrained_constant_intercept":
            continue
        if row["row_type"] == "intercept":
            intercept = mp.mpf(row["coefficient"])
        elif row["row_type"] == "exponent":
            coeffs[row["character"]] = mp.mpf(row["coefficient"])
    if intercept is None or set(coeffs) != set(CHARS):
        raise RuntimeError("could not load complete Step 339 coefficients")
    return intercept, coeffs


def product_log_prediction(intercept: mp.mpf, coeffs: dict[str, mp.mpf], hecke: dict[str, dict[int, mp.mpf]], k: int) -> mp.mpf:
    return intercept + mp.fsum([coeffs[ch] * mp.log(hecke[ch][k]) for ch in CHARS])


def residual_row(k: int, actual: mp.mpf, predicted_log: mp.mpf, row_type: str) -> dict[str, object]:
    pred = mp.e ** predicted_log
    log_error = predicted_log - mp.log(actual)
    rel = abs(pred - actual) / actual
    return {
        "row_type": row_type,
        "k": k,
        "actual_abs_L_k_rho2_G_star": mp.nstr(actual, 18),
        "predicted_abs": mp.nstr(pred, 18),
        "log_error": mp.nstr(log_error, 12),
        "relative_residual": mp.nstr(rel, 12),
        "verdict": "pass_under_5pct" if rel < mp.mpf("0.05") else "fail_under_5pct",
    }


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    mod = load_step338_module()
    b0, coeffs = load_step339_coefficients()
    max_k = max(KS)

    # Fixed Hecke inputs: same character-specific first-zero pairings as Step 339.
    roots = mod.roots()
    hecke: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    for ch in CHARS:
        q, chi = mod.char_values(ch)
        rho = roots[ch]
        Lds = mod.dirichlet_L_derivatives(rho, q, chi, max_k)
        Mds = mod.M_derivatives(rho, max_k)
        for k in KS:
            hecke[ch][k] = abs(mod.h_derivative(Lds, Mds, k))

    # Target at rho_2.
    rho2 = mp.zetazero(2)
    zds = mod.zeta_derivatives(rho2, max_k)
    mds = mod.M_derivatives(rho2, max_k)
    actual = {k: abs(mod.h_derivative(zds, mds, k)) for k in KS}

    fixed_rows: list[dict[str, object]] = []
    for k in KS:
        fixed_rows.append(residual_row(k, actual[k], product_log_prediction(b0, coeffs, hecke, k), "fixed_step339_b0"))

    # rho-dependent intercept calibrated at k=10.
    sum10 = mp.fsum([coeffs[ch] * mp.log(hecke[ch][10]) for ch in CHARS])
    b0_rho2 = mp.log(actual[10]) - sum10
    rho_rows: list[dict[str, object]] = [{
        "row_type": "rho2_intercept",
        "k": "calibrated_at_10",
        "b0_rho2": mp.nstr(b0_rho2, 18),
        "delta_from_step339_b0": mp.nstr(b0_rho2 - b0, 18),
        "actual_abs_L_k_rho2_G_star": "",
        "predicted_abs": "",
        "log_error": "",
        "relative_residual": "",
        "verdict": "shared_a_chi_with_rho_dependent_intercept",
    }]
    max_rho_rel = mp.mpf("0")
    for k in KS:
        pred_log = product_log_prediction(b0_rho2, coeffs, hecke, k)
        row = residual_row(k, actual[k], pred_log, "rho2_specific_b0_shared_a_chi")
        max_rho_rel = max(max_rho_rel, mp.mpf(row["relative_residual"]))
        row["b0_rho2"] = mp.nstr(b0_rho2, 18)
        row["delta_from_step339_b0"] = mp.nstr(b0_rho2 - b0, 18)
        rho_rows.append(row)

    write_csv(ART / "cross_rho_prediction_step340.csv", fixed_rows)
    write_csv(ART / "b0_rho_specific_step340.csv", rho_rows)

    # Also write a compact actual-values block into the summary; primary actual
    # values live in the prediction CSV.
    max_fixed = max(mp.mpf(r["relative_residual"]) for r in fixed_rows)
    fixed_pass = max_fixed < mp.mpf("0.05")
    rho_pass = max_rho_rel < mp.mpf("0.05")
    if fixed_pass:
        verdict = "V_H6_multiplicative_bridge_cross_rho_fixed_b0_passes"
    elif rho_pass:
        verdict = "V_H6_multiplicative_bridge_cross_rho_needs_rho_dependent_intercept"
    else:
        verdict = "V_H6_multiplicative_bridge_cross_rho_fails"

    summary = [
        "# Step 340 Results Summary",
        "",
        "Cross-rho robustness test for the Step 339 product-form H6 bridge candidate.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 305: certified rho_2 checks include `667.785` at k=10 and about `8.74e6` at k=20.",
        "- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.",
        "- Step 339: fitted product coefficients with `b0=-2.40963`, exponent sum `1.04073`, and holdout max residual `0.00893202095224` at rho_1.",
        "",
        "Actual rho_2 target values:",
    ]
    for k in KS:
        summary.append(f"- k={k}: `{mp.nstr(actual[k], 18)}`")
    summary += [
        "",
        f"Fixed Step 339 b0 max residual on rho_2: `{mp.nstr(max_fixed, 12)}`.",
        f"Rho_2-specific b0 calibrated at k=10: `{mp.nstr(b0_rho2, 12)}`; delta from Step 339 b0: `{mp.nstr(b0_rho2 - b0, 12)}`.",
        f"Shared a(chi) with rho_2-specific b0 max residual: `{mp.nstr(max_rho_rel, 12)}`.",
        "",
        "Interpretation: the exponent vector is not enough with the original rho_1 intercept. A rho_2-specific intercept calibrated at k=10 also fails cross-k consistency, so the Step 339 product bridge is rho-specific rather than structurally cross-rho robust.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step340_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 340,
        "orientation": "cross-validation",
        "target": "cross-rho robustness of Step 339 multiplicative H6 bridge",
        "dps": DPS,
        "rho_tested": "rho_2",
        "k_values": KS,
        "fixed_b0_max_relative_residual": mp.nstr(max_fixed, 18),
        "rho_specific_b0": mp.nstr(b0_rho2, 18),
        "rho_specific_b0_max_relative_residual": mp.nstr(max_rho_rel, 18),
        "final_verdict": verdict,
        "bridge_claimed": fixed_pass,
        "rho_dependent_intercept_needed": not fixed_pass and rho_pass,
    }
    (ART / "step340_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 340 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- Cross-rho numerical consistency is not a proof of an H6 descent theorem.",
        "- If a rho-dependent intercept is needed, the original Step 339 bridge is not rho-independent.",
        "- The missing theorem-grade object remains a carrier/projection/kernel-preserving Hecke-to-Burnol zeta-fiber descent.",
    ]
    (ART / "nonclaim_boundary_step340.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_fixed_rel={mp.nstr(max_fixed, 12)}")
    print(f"b0_rho2={mp.nstr(b0_rho2, 12)}")
    print(f"max_rho_specific_rel={mp.nstr(max_rho_rel, 12)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
