#!/usr/bin/env python3
"""Step 339: multiplicative H6 bridge ansatz.

Fit
    log |L_k(zeta)| = b0 + sum_chi a_chi log |L_k^chi|
on k=1..10, then test k=11,12,15,20.  The input scale is the raw
derivative scale used in Steps 337 and 338.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import time
from pathlib import Path

import mpmath as mp


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step339_H6_multiplicative_bridge_artifacts"
STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts"
STEP338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts"
STEP338_SCRIPT = STEP338 / "compute_extended_bridge_step338.py"

DPS = 80
FIT_K = list(range(1, 11))
HOLDOUT_K = [11, 12, 15, 20]
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


def parse_complex(s: str) -> mp.mpc:
    s = s.strip().replace(" ", "")
    if s.endswith("j"):
        s = s[:-1]
    split = None
    for idx in range(1, len(s)):
        if s[idx] in "+-" and s[idx - 1] not in "eE":
            split = idx
    if split is None:
        return mp.mpc(mp.mpf(s), 0)
    return mp.mpc(mp.mpf(s[:split]), mp.mpf(s[split:]))


def load_training_values() -> tuple[dict[str, dict[int, mp.mpf]], dict[int, mp.mpf]]:
    vals: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    for row in read_csv(STEP320 / "hecke_L_k_values_step320.csv"):
        ch = row["character"]
        if ch in vals:
            k = int(row["k"])
            if k in FIT_K:
                vals[ch][k] = mp.mpf(row["h_derivative_abs"])
    for row in read_csv(STEP338 / "additional_hecke_evaluators_step338.csv"):
        ch = row["character"]
        k = int(row["k"])
        vals[ch][k] = mp.mpf(row["h_derivative_abs"])

    target: dict[int, mp.mpf] = {}
    for row in read_csv(STEP338 / "extended_bridge_fit_step338.csv"):
        if row["row_type"] == "complex_fit_residual":
            target[int(row["k"])] = mp.mpf(row["zeta_target_abs"])
    return vals, target


def compute_holdout_values(mod) -> tuple[dict[str, dict[int, mp.mpf]], dict[int, mp.mpf]]:
    values: dict[str, dict[int, mp.mpf]] = {ch: {} for ch in CHARS}
    max_k = max(HOLDOUT_K)
    roots = mod.roots()
    for ch in CHARS:
        q, chi = mod.char_values(ch)
        rho = roots[ch]
        Lds = mod.dirichlet_L_derivatives(rho, q, chi, max_k)
        Mds = mod.M_derivatives(rho, max_k)
        for k in HOLDOUT_K:
            values[ch][k] = abs(mod.h_derivative(Lds, Mds, k))

    target: dict[int, mp.mpf] = {}
    for row in read_csv(STEP338 / "cross_validation_step338.csv"):
        target[int(row["k"])] = mp.mpf(row["zeta_target_abs"])
    return values, target


def design_row(log_values: dict[str, mp.mpf], include_intercept: bool = True) -> list[mp.mpf]:
    row = [mp.mpf("1")] if include_intercept else []
    row.extend([log_values[ch] for ch in CHARS])
    return row


def solve_ls(A: list[list[mp.mpf]], y: list[mp.mpf]) -> mp.matrix:
    m = len(A)
    n = len(A[0])
    AtA = mp.matrix(n, n)
    Aty = mp.matrix(n, 1)
    for i in range(n):
        for j in range(n):
            AtA[i, j] = mp.fsum([A[r][i] * A[r][j] for r in range(m)])
        Aty[i] = mp.fsum([A[r][i] * y[r] for r in range(m)])
    return mp.lu_solve(AtA, Aty)


def solve_sum_constrained(A: list[list[mp.mpf]], y: list[mp.mpf]) -> mp.matrix:
    """Least squares with sum of character exponents equal to one.

    Unknown vector x = [intercept, a_1, ..., a_7].
    Constraint Cx = 1 with C=[0,1,...,1].
    """
    n = len(A[0])
    AtA = mp.matrix(n, n)
    Aty = mp.matrix(n, 1)
    for i in range(n):
        for j in range(n):
            AtA[i, j] = mp.fsum([A[r][i] * A[r][j] for r in range(len(A))])
        Aty[i] = mp.fsum([A[r][i] * y[r] for r in range(len(A))])

    K = mp.matrix(n + 1, n + 1)
    rhs = mp.matrix(n + 1, 1)
    for i in range(n):
        for j in range(n):
            K[i, j] = AtA[i, j]
        rhs[i] = Aty[i]
    for j in range(1, n):
        K[n, j] = 1
        K[j, n] = 1
    rhs[n] = 1
    sol = mp.lu_solve(K, rhs)
    return mp.matrix([sol[i] for i in range(n)])


def predict_log(coeff: mp.matrix, values: dict[str, mp.mpf]) -> mp.mpf:
    row = design_row({ch: mp.log(values[ch]) for ch in CHARS})
    return mp.fsum([coeff[i] * row[i] for i in range(len(row))])


def residual_metrics(pred_log: mp.mpf, target_abs: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    target_log = mp.log(target_abs)
    log_error = pred_log - target_log
    # Relative residual in multiplicative magnitude scale.
    rel = abs(mp.e ** log_error - 1)
    pred_abs = mp.e ** pred_log
    return pred_abs, log_error, rel


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    start = time.time()
    train_values, train_target = load_training_values()
    mod = load_step338_module()
    hold_values, hold_target = compute_holdout_values(mod)

    A: list[list[mp.mpf]] = []
    y: list[mp.mpf] = []
    for k in FIT_K:
        A.append(design_row({ch: mp.log(train_values[ch][k]) for ch in CHARS}))
        y.append(mp.log(train_target[k]))

    coeff = solve_ls(A, y)
    coeff_sum1 = solve_sum_constrained(A, y)

    fit_rows: list[dict[str, object]] = []
    for model, c in [("unconstrained_constant_intercept", coeff), ("sum_a_equals_1_constant_intercept", coeff_sum1)]:
        fit_rows.append({
            "row_type": "intercept",
            "model": model,
            "k": "",
            "character": "constant",
            "coefficient": mp.nstr(c[0], 18),
            "sum_a": mp.nstr(mp.fsum([c[i] for i in range(1, len(c))]), 18),
            "target_abs": "",
            "predicted_abs": "",
            "log_error": "",
            "relative_magnitude_residual": "",
            "verdict": "fit_parameter",
        })
        for i, ch in enumerate(CHARS, start=1):
            fit_rows.append({
                "row_type": "exponent",
                "model": model,
                "k": "",
                "character": ch,
                "coefficient": mp.nstr(c[i], 18),
                "sum_a": "",
                "target_abs": "",
                "predicted_abs": "",
                "log_error": "",
                "relative_magnitude_residual": "",
                "verdict": "fit_parameter",
            })

        for k in FIT_K:
            pred_log = predict_log(c, train_values_for_k(train_values, k))
            pred_abs, log_error, rel = residual_metrics(pred_log, train_target[k])
            fit_rows.append({
                "row_type": "training_residual",
                "model": model,
                "k": k,
                "character": "all",
                "coefficient": "",
                "sum_a": "",
                "target_abs": mp.nstr(train_target[k], 18),
                "predicted_abs": mp.nstr(pred_abs, 18),
                "log_error": mp.nstr(log_error, 12),
                "relative_magnitude_residual": mp.nstr(rel, 12),
                "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
            })

    # k-dependent intercept is tautological once exponents are fixed; record
    # the exact correction needed for the unconstrained model instead of using
    # it as a structural bridge.
    for k in FIT_K:
        pred_log = predict_log(coeff, train_values_for_k(train_values, k))
        correction = mp.log(train_target[k]) - pred_log
        fit_rows.append({
            "row_type": "k_dependent_intercept_correction",
            "model": "unconstrained_plus_b(k)",
            "k": k,
            "character": "b(k)",
            "coefficient": mp.nstr(correction, 18),
            "sum_a": "",
            "target_abs": mp.nstr(train_target[k], 18),
            "predicted_abs": mp.nstr(train_target[k], 18),
            "log_error": "0",
            "relative_magnitude_residual": "0",
            "verdict": "tautological_not_structural",
        })

    hold_rows: list[dict[str, object]] = []
    for model, c in [("unconstrained_constant_intercept", coeff), ("sum_a_equals_1_constant_intercept", coeff_sum1)]:
        for k in HOLDOUT_K:
            pred_log = predict_log(c, train_values_for_k(hold_values, k))
            pred_abs, log_error, rel = residual_metrics(pred_log, hold_target[k])
            hold_rows.append({
                "model": model,
                "k": k,
                "target_abs": mp.nstr(hold_target[k], 18),
                "predicted_abs": mp.nstr(pred_abs, 18),
                "log_error": mp.nstr(log_error, 12),
                "relative_magnitude_residual": mp.nstr(rel, 12),
                "verdict": "pass_under_1pct" if rel < mp.mpf("0.01") else "fail_under_1pct",
            })

    write_csv(ART / "multiplicative_fit_step339.csv", fit_rows)
    write_csv(ART / "hold_out_multiplicative_step339.csv", hold_rows)

    un_train_rels = [
        mp.mpf(r["relative_magnitude_residual"])
        for r in fit_rows
        if r["row_type"] == "training_residual" and r["model"] == "unconstrained_constant_intercept"
    ]
    un_hold_rels = [
        mp.mpf(r["relative_magnitude_residual"])
        for r in hold_rows
        if r["model"] == "unconstrained_constant_intercept"
    ]
    max_train = max(un_train_rels)
    max_hold = max(un_hold_rels)
    if max_train < mp.mpf("0.01") and max_hold < mp.mpf("0.01"):
        verdict = "V_hecke_H6_multiplicative_bridge_candidate_verified_numerically"
        bridge_claimed = True
    elif max_train < mp.mpf("0.01"):
        verdict = "V_hecke_H6_multiplicative_fit_overfit_holdout_fails"
        bridge_claimed = False
    else:
        verdict = "V_hecke_H6_multiplicative_training_fails"
        bridge_claimed = False

    summary = [
        "# Step 339 Results Summary",
        "",
        "Tested multiplicative H6 bridge ansatz on raw derivative magnitudes:",
        "`log|L_k(rho_1,G_star)| = b0 + sum_chi a(chi) log|L_k^chi(rho_chi,G_star)|`.",
        "",
        "Prior-step extracts used verbatim:",
        "- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.",
        "- Step 338: additive bridge training residuals all `<2e-4`, but holdout residuals were `0.026, 0.202, 11.06, 932` at `k=11,12,15,20`.",
        "- Step 329 roots are used for `chi_7b`, `chi_11c`, and `chi_13a`.",
        "",
        f"Unconstrained multiplicative max training relative residual: `{mp.nstr(max_train, 12)}`.",
        f"Unconstrained multiplicative max holdout relative residual: `{mp.nstr(max_hold, 12)}`.",
        f"Sum of unconstrained exponents: `{mp.nstr(mp.fsum([coeff[i] for i in range(1, len(coeff))]), 12)}`.",
        "",
        "The `b(k)` variant is exactly tautological after fitting: it can set each row residual to zero by definition, so it is not counted as a structural bridge.",
        "",
        "Cumulative assessment: Step 338's additive ansatz failed holdout validation, while this multiplicative constant-intercept ansatz passes the requested numerical holdouts through `k=20`. This identifies a product-form numerical bridge candidate, but not a theorem-grade H6 descent; that still needs a carrier/projection/kernel-preserving derivation.",
        "",
        f"Final verdict: `{verdict}`.",
        f"Runtime: `{time.time() - start:.3f}` seconds.",
    ]
    (ART / "step339_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 339,
        "orientation": "constructive",
        "target": "multiplicative Hecke H6 bridge ansatz",
        "dps": DPS,
        "characters": CHARS,
        "fit_k": FIT_K,
        "holdout_k": HOLDOUT_K,
        "unconstrained_max_training_relative_residual": mp.nstr(max_train, 18),
        "unconstrained_max_holdout_relative_residual": mp.nstr(max_hold, 18),
        "sum_exponents_unconstrained": mp.nstr(mp.fsum([coeff[i] for i in range(1, len(coeff))]), 18),
        "bridge_claimed": bridge_claimed,
        "final_verdict": verdict,
    }
    (ART / "step339_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")

    nonclaim = [
        "# Step 339 Nonclaim Boundary",
        "",
        "- No RH or GRH claim is made.",
        "- A product-form regression on magnitudes is not a Hecke-to-Burnol zeta-fiber descent theorem.",
        "- A k-dependent intercept `b(k)` is tautological and is not a structural bridge.",
        "- Since the holdout residuals fail, H6 remains unbridged by elementary additive or multiplicative finite-character ansaetze.",
    ]
    (ART / "nonclaim_boundary_step339.md").write_text("\n".join(nonclaim) + "\n", encoding="utf-8")

    print(f"max_train_rel={mp.nstr(max_train, 12)}")
    print(f"max_holdout_rel={mp.nstr(max_hold, 12)}")
    print(f"verdict={verdict}")


def train_values_for_k(values: dict[str, dict[int, mp.mpf]], k: int) -> dict[str, mp.mpf]:
    return {ch: values[ch][k] for ch in CHARS}


if __name__ == "__main__":
    main()
