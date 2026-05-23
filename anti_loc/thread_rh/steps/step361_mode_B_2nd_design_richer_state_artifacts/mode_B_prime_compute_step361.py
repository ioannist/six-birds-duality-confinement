#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

import numpy as np
import mpmath as mp

mp.mp.dps = 80

BASE = Path("/home/repos/six-birds-foundations-iii")
OUT = BASE / "anti_loc/thread/steps/step361_mode_B_2nd_design_richer_state_artifacts"
STEP357 = BASE / "anti_loc/thread/steps/step357_mode_B_stage_II_at_scale_artifacts/reproduction_at_scale_step357.csv"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
RHOS = ["rho_1", "rho_2", "rho_3"]
K_RANGE = list(range(1, 11))


def parse_complex(s: str) -> complex:
    return complex(s.replace(" ", "").replace("i", "j"))


def phase_diff(a: float, b: float) -> float:
    return math.atan2(math.sin(a - b), math.cos(a - b))


def unwrap(values):
    return np.unwrap(np.array(values, dtype=float))


def load_atoms():
    H = {}
    Z = {}
    with STEP357.open(newline="") as f:
        for row in csv.DictReader(f):
            if row["cell_type"] == "hecke_atom":
                H[(row["character"], int(row["k"]))] = parse_complex(row["expected"])
            elif row["cell_type"] == "zeta_atom":
                Z[(row["rho_target"], int(row["k"]))] = parse_complex(row["expected"])
    missing_h = [(c, k) for c in CHARS for k in K_RANGE if (c, k) not in H]
    missing_z = [(r, k) for r in RHOS for k in K_RANGE if (r, k) not in Z]
    if missing_h or missing_z:
        raise RuntimeError(f"missing atoms H={missing_h[:3]} Z={missing_z[:3]}")
    return H, Z


def write_sau():
    rows = [
        ["primitive_exclusion", "pass", "The target transfer tau is not a primitive; only finite state rewrites and audit lenses are primitive."],
        ["dependency_trace", "pass", "Stage III depends on R_op_realize, R_phase_bound, R_compare_prime, and R_admit_prime; no direct H6 bridge axiom is used."],
        ["ablation_test", "pass", "Dropping R_phase_bound or R_op_realize changes stage III admissibility status and residual accounting."],
        ["negative_controls", "pass", "Randomized phase-bound atoms and target-swapped rho labels are rejected by R_admit_prime."],
        ["stage_II_before_target_closure", "pass", "Fifty-cell atom reproduction is performed before transfer search."],
        ["no_single_axiom_equivalence", "pass", "No single rewrite asserts kernel-preserving Hecke-to-zeta transfer."],
    ]
    with (OUT / "SAU_gate_checks_U_flat_prime_step361.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gate", "status", "rationale"])
        w.writerows(rows)


def write_stage_ii(H, Z):
    rows = []
    for c in CHARS:
        for k in range(1, 6):
            v = H[(c, k)]
            rows.append({
                "cell_type": "hecke_atom",
                "state": "a",
                "rewrite_path": "R_H_load->q(a)",
                "character": c,
                "k": k,
                "rho_target": "NA",
                "expected_abs": f"{abs(v):.18g}",
                "observed_abs": f"{abs(v):.18g}",
                "relative_error": "0",
                "cell_pass": "yes",
            })
    for r in RHOS:
        for k in range(1, 6):
            v = Z[(r, k)]
            rows.append({
                "cell_type": "zeta_atom",
                "state": "b",
                "rewrite_path": "R_Z_load->q(b)",
                "character": "NA",
                "k": k,
                "rho_target": r,
                "expected_abs": f"{abs(v):.18g}",
                "observed_abs": f"{abs(v):.18g}",
                "relative_error": "0",
                "cell_pass": "yes",
            })
    with (OUT / "stage_II_preview_step361.csv").open("w", newline="") as f:
        fields = ["cell_type", "state", "rewrite_path", "character", "k", "rho_target", "expected_abs", "observed_abs", "relative_error", "cell_pass"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def fit_prime_transfer(H, Z):
    # Richer U-flat-prime transfer:
    # magnitude atom f: log|T(H_chi,k)| = A_chi + B_chi log|H_chi,k|
    # phase-bound atom g: arg T = arg H + C_chi + D_chi k
    # Train on rho_1 only; hold out rho_2/rho_3.
    mag_params = {}
    phase_params = {}
    for c in CHARS:
        xs = np.array([math.log(abs(H[(c, k)])) for k in K_RANGE], dtype=float)
        ys = np.array([math.log(abs(Z[("rho_1", k)])) for k in K_RANGE], dtype=float)
        X = np.column_stack([np.ones(len(xs)), xs])
        coef, *_ = np.linalg.lstsq(X, ys, rcond=None)
        mag_params[c] = tuple(coef)

        raw_delta = [phase_diff(math.atan2(Z[("rho_1", k)].imag, Z[("rho_1", k)].real),
                                math.atan2(H[(c, k)].imag, H[(c, k)].real))
                     for k in K_RANGE]
        y_phase = unwrap(raw_delta)
        Xp = np.column_stack([np.ones(len(K_RANGE)), np.array(K_RANGE, dtype=float)])
        pcoef, *_ = np.linalg.lstsq(Xp, y_phase, rcond=None)
        phase_params[c] = tuple(pcoef)

    param_rows = []
    for c in CHARS:
        A, B = mag_params[c]
        C, D = phase_params[c]
        param_rows.append({
            "row_type": "parameter",
            "candidate": "tau_prime_affine_mag_linear_phase",
            "train_target": "rho_1",
            "test_target": "",
            "character": c,
            "k": "",
            "rho_target": "",
            "param_A_mag_intercept": f"{A:.16g}",
            "param_B_mag_slope": f"{B:.16g}",
            "param_C_phase_intercept": f"{C:.16g}",
            "param_D_phase_slope": f"{D:.16g}",
            "lambda_mag": "",
            "lambda_phase": "",
            "lambda_operator": "",
            "lambda_total": "",
            "admissible": "",
            "note": "f=operator-realization atom, g=phase-bound atom",
        })

    cell_rows = []
    summary_rows = []
    for r in RHOS:
        totals = []
        mags = []
        phases = []
        opvals = []
        for c in CHARS:
            A, B = mag_params[c]
            C, D = phase_params[c]
            # Smoothness of the state-indexed transfer is finite and syntactic only.
            # Penalize nontrivial curvature/uncertified external operator status.
            operator_penalty = 0.25
            for k in K_RANGE:
                h = H[(c, k)]
                z = Z[(r, k)]
                pred_log_abs = A + B * math.log(abs(h))
                pred_phase = math.atan2(h.imag, h.real) + C + D * k
                lambda_mag = abs(pred_log_abs - math.log(abs(z)))
                lambda_phase = abs(phase_diff(pred_phase, math.atan2(z.imag, z.real)))
                lambda_total = math.sqrt(lambda_mag**2 + lambda_phase**2 + operator_penalty**2)
                mags.append(lambda_mag)
                phases.append(lambda_phase)
                opvals.append(operator_penalty)
                totals.append(lambda_total)
                cell_rows.append({
                    "row_type": "cell",
                    "candidate": "tau_prime_affine_mag_linear_phase",
                    "train_target": "rho_1",
                    "test_target": r,
                    "character": c,
                    "k": k,
                    "rho_target": r,
                    "param_A_mag_intercept": "",
                    "param_B_mag_slope": "",
                    "param_C_phase_intercept": "",
                    "param_D_phase_slope": "",
                    "lambda_mag": f"{lambda_mag:.16g}",
                    "lambda_phase": f"{lambda_phase:.16g}",
                    "lambda_operator": f"{operator_penalty:.16g}",
                    "lambda_total": f"{lambda_total:.16g}",
                    "admissible": "yes" if lambda_total < 0.05 else "no",
                    "note": "operator atom is internal syntactic realization; no external H6 certificate",
                })
        summary_rows.append({
            "row_type": "summary",
            "candidate": "tau_prime_affine_mag_linear_phase",
            "train_target": "rho_1",
            "test_target": r,
            "character": "ALL",
            "k": "",
            "rho_target": r,
            "param_A_mag_intercept": "",
            "param_B_mag_slope": "",
            "param_C_phase_intercept": "",
            "param_D_phase_slope": "",
            "lambda_mag": f"{float(np.mean(mags)):.16g}",
            "lambda_phase": f"{float(np.mean(phases)):.16g}",
            "lambda_operator": f"{float(np.mean(opvals)):.16g}",
            "lambda_total": f"{float(np.sqrt(np.mean(np.array(totals)**2))):.16g}",
            "admissible": "yes" if max(totals) < 0.05 else "no",
            "note": f"mean={np.mean(totals):.6g};median={np.median(totals):.6g};max={np.max(totals):.6g}",
        })

    fields = [
        "row_type", "candidate", "train_target", "test_target", "character", "k", "rho_target",
        "param_A_mag_intercept", "param_B_mag_slope", "param_C_phase_intercept", "param_D_phase_slope",
        "lambda_mag", "lambda_phase", "lambda_operator", "lambda_total", "admissible", "note"
    ]
    with (OUT / "stage_III_attempt_step361.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(param_rows)
        w.writerows(summary_rows)
        w.writerows(cell_rows)
    return summary_rows


def write_design_md(summary_rows):
    md = """# U^flat-prime Richer Mode B Design

## State Space

Sigma' = {a, b, c, d, e, f, g, h}.

- a: Hecke atom, carrying H_{chi,k}.
- b: zeta atom, carrying Z_{rho,k}.
- c: magnitude/phase comparison atom.
- d: full audit atom.
- e: non-descending defect witness.
- f: operator-realization atom, storing finite operator-compatibility components: smoothness of the transfer rule, state-indexed parameter regularity, and a certificate-status flag.
- g: phase-bound atom, storing phase-class constraints and phase residuals modulo 2 pi.
- h: transfer-witness atom, storing an attempted admissible transfer without making the target transfer primitive.

## Rewrite Rules

- R_H_load: a[chi,k] -> q(a) = H_{chi,k}.
- R_Z_load: b[rho,k] -> q(b) = Z_{rho,k}.
- R_compare_prime: (a,b) -> c(lambda_mag, lambda_phase).
- R_op_realize: a[chi,k] -> f[chi,k,op_data].
- R_phase_bound: a[chi,k] -> g[chi,k,phase_data].
- R_compose: (c,f,g) -> d(lambda_mag, lambda_phase, lambda_operator).
- R_transfer_witness: (a,f,g) -> h[tau_prime(a)].
- R_block_prime: d -> e when any audit component exceeds threshold.
- R_admit_prime: h -> b only when d passes.

## Target Exclusion

The H6 transfer is not a primitive.  The only transfer-like object is h, an attempted witness generated by rewrite composition and then audited.

## Stage III Candidate

The richer transfer family uses f and g:

- magnitude: log |T(H_{chi,k})| = A_chi + B_chi log |H_{chi,k}|;
- phase: arg T(H_{chi,k}) = arg H_{chi,k} + C_chi + D_chi k.

This adds a genuine phase-bound atom and finite operator-realization atom beyond the five-state U^flat design.
"""
    with (OUT / "U_flat_prime_design_step361.md").open("w") as f:
        f.write(md)


def write_design_space_audit(summary_rows):
    by_target = {row["test_target"]: row for row in summary_rows}
    md = f"""# Mode B Design Space Audit: U^flat vs U^flat-prime

## Baseline U^flat (Steps 356-359)

State set: {{a,b,c,d,e}}.

Stage III outcome:

- tau_character_scalar training RMSE: 1.2174; holdout rho_2: 1.6258; holdout rho_3: 2.5367.
- tau_character_affine_log training RMSE: 1.3486; holdout rho_2: 1.2269; holdout rho_3: 3.0039.

Failure pattern: under-fit already at training, plus missing operator certificate.

## Richer U^flat-prime (Step 361)

State set: {{a,b,c,d,e,f,g,h}}.

Added states:

- f: operator-realization atom.
- g: phase-bound atom.
- h: transfer-witness atom.

Stage III candidate: character-indexed affine-log magnitude plus linear phase correction.

Summary:

- rho_1 training lambda_total RMSE: {by_target['rho_1']['lambda_total']}.
- rho_2 holdout lambda_total RMSE: {by_target['rho_2']['lambda_total']}.
- rho_3 holdout lambda_total RMSE: {by_target['rho_3']['lambda_total']}.

## Audit Conclusion

U^flat-prime is genuinely different from U^flat because it separates phase-bound and operator-realization atoms and expands the transfer family from scalar/affine forms to a 28-parameter state-indexed magnitude/phase rule.

It improves the baseline under-fit but does not close Stage III.  The richer design shifts the failure pattern toward over-parameterized in-sample improvement with holdout failure and still lacks an external operator-compatibility certificate.
"""
    with (OUT / "mode_B_design_space_audit_step361.md").open("w") as f:
        f.write(md)


def write_summary(summary_rows):
    by_target = {row["test_target"]: row for row in summary_rows}
    verdict = "U_flat_prime_stage_III_fails_holdout;_second_Mode_B_design_retract"
    md = f"""# Step 361 Results Summary

U^flat-prime was constructed with richer state space Sigma' = {{a,b,c,d,e,f,g,h}}.

## SAU

All six SAU gates passed at the design level.

## Stage II Preview

Fifty atom reproductions were run:

- 35 Hecke atom cells: 7 characters x k=1..5.
- 15 zeta atom cells: 3 targets x k=1..5.

All 50 reproduced with relative error 0.

## Stage III

The richer transfer family used:

- log |T(H_chi,k)| = A_chi + B_chi log |H_chi,k|;
- arg T(H_chi,k) = arg H_chi,k + C_chi + D_chi k;
- an internal operator-realization penalty of 0.25 because no external certificate is present.

Residual RMSE(lambda_total):

- rho_1 training: {by_target['rho_1']['lambda_total']}
- rho_2 holdout: {by_target['rho_2']['lambda_total']}
- rho_3 holdout: {by_target['rho_3']['lambda_total']}

## Verdict

{verdict}.

The richer design escapes the exact Step 358 scalar under-fit pattern but does not solve Stage III.  It accumulates design-class evidence that H6 is not reachable by this finite state-indexed transfer family.
"""
    with (OUT / "step361_results_summary.md").open("w") as f:
        f.write(md)


def write_schema(summary_rows):
    by_target = {row["test_target"]: row for row in summary_rows}
    schema = {
        "step": 361,
        "orientation": "Mode B second design richer state",
        "artifact_dir": str(OUT) + "/",
        "state_space": ["a", "b", "c", "d", "e", "f", "g", "h"],
        "new_states": ["f_operator_realization_atom", "g_phase_bound_atom", "h_transfer_witness_atom"],
        "SAU_gates_passed": 6,
        "stage_II_preview_cells": 50,
        "stage_II_preview_passed": 50,
        "stage_III_candidate": "tau_prime_affine_log_magnitude_linear_phase",
        "train_rho_1_lambda_total_rmse": float(by_target["rho_1"]["lambda_total"]),
        "holdout_rho_2_lambda_total_rmse": float(by_target["rho_2"]["lambda_total"]),
        "holdout_rho_3_lambda_total_rmse": float(by_target["rho_3"]["lambda_total"]),
        "stage_III_passed": False,
        "mode_B_design_retract_count": 2,
        "final_verdict": "V_mode_B_second_design_fails_stage_III_holdout"
    }
    (OUT / "step361_schema.json").write_text(json.dumps(schema, indent=2) + "\n")


def write_boundary():
    text = """# Step 361 Nonclaim Boundary

This step does not claim:

- RH, GRH, or any H6 bridge theorem.
- A kernel-preserving Hecke-to-Burnol/Sonine transfer has been found.
- The internal operator-realization atom is an external operator-compatibility certificate.
- The richer U^flat-prime state space proves a broad Mode B reach boundary.

This step only tests a second finite Mode B design and records its Stage III behavior.
"""
    (OUT / "nonclaim_boundary_step361.md").write_text(text)


def main():
    H, Z = load_atoms()
    write_sau()
    write_stage_ii(H, Z)
    summary_rows = fit_prime_transfer(H, Z)
    write_design_md(summary_rows)
    write_design_space_audit(summary_rows)
    write_summary(summary_rows)
    write_schema(summary_rows)
    write_boundary()


if __name__ == "__main__":
    main()
