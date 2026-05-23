#!/usr/bin/env python3
"""Generate Step 170 CP-RED test-generator artifacts.

All writes are intentionally confined to the absolute Step 170 artifact path.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import quad


OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/step170_cp_red_test_generators_artifacts/")


def bump(t: float, r: float, R: float) -> float:
    if t <= r or t >= R:
        return 0.0
    return math.exp(-((R - r) ** 2) / ((t - r) * (R - t)))


INTERVALS = [(0.40, 0.70), (0.90, 1.30), (1.70, 2.30)]


def moment(r: float, R: float, power: float) -> float:
    value, _ = quad(
        lambda x: bump(x, r, R) * (x**power),
        r,
        R,
        epsabs=1e-13,
        epsrel=1e-12,
        limit=200,
    )
    return float(value)


M0 = [moment(r, R, 0.0) for r, R in INTERVALS]
M1 = [moment(r, R, -1.0) for r, R in INTERVALS]
coeff_tail = np.linalg.solve(
    np.array([[M0[1], M0[2]], [M1[1], M1[2]]], dtype=float),
    -np.array([M0[0], M1[0]], dtype=float),
)
COEFFS = [1.0, float(coeff_tail[0]), float(coeff_tail[1])]


def g(t: float) -> float:
    return float(sum(COEFFS[i] * bump(t, *INTERVALS[i]) for i in range(3)))


def ghat(s: complex) -> complex:
    real, _ = quad(
        lambda x: (g(x) * x ** (-s)).real,
        0.40,
        2.30,
        epsabs=1e-11,
        epsrel=1e-10,
        limit=300,
    )
    imag, _ = quad(
        lambda x: (g(x) * x ** (-s)).imag,
        0.40,
        2.30,
        epsabs=1e-11,
        epsrel=1e-10,
        limit=300,
    )
    return complex(real, imag)


def c_g(t: float) -> tuple[float, list[tuple[int, float]]]:
    terms: list[tuple[int, float]] = []
    total = 0.0
    for n in range(1, int(math.floor(t / 0.40)) + 1):
        val = g(t / n) / n
        total += val
        if abs(val) > 1e-8:
            terms.append((n, float(val)))
    # The inherited legality requires ghat(1)=0; numerical residual is recorded separately.
    return float(total), terms


def fmt_complex(z: complex) -> str:
    return f"{z.real:.12e}{z.imag:+.12e}i"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    moment0 = sum(COEFFS[i] * M0[i] for i in range(3))
    moment1 = sum(COEFFS[i] * M1[i] for i in range(3))
    ell = "log(2)"
    a = "1/4"
    support = "[0.40,0.70] union [0.90,1.30] union [1.70,2.30] subset [1/4,4]"

    taus = [0.0, 1.0, 5.0, 14.134725141734693]
    sample_rows = []
    for tau in taus:
        s = complex(0.5, tau)
        gh = ghat(s)
        zgh = complex(mp.zeta(s)) * gh
        ml = 2 ** (s - 0.5)
        sample_rows.append(
            {
                "generator_id": "G170_1",
                "s": f"1/2 + {tau:.15g} i",
                "ghat": fmt_complex(gh),
                "zeta_times_ghat": fmt_complex(zgh),
                "m_log2": fmt_complex(ml),
                "note": (
                    "first zeta zero row; zeta_times_ghat is numerically zero to quadrature precision"
                    if abs(tau - 14.134725141734693) < 1e-12
                    else "ordinary critical-line sample"
                ),
            }
        )

    cg_rows = []
    for t in [0.35, 0.45, 0.60, 1.00, 2.00, 3.00, 5.00]:
        val, terms = c_g(t)
        cg_rows.append(
            {
                "generator_id": "G170_1",
                "t": f"{t:.2f}",
                "C_g_t": f"{val:.12e}",
                "nonzero_terms_n_g_t_over_n": "; ".join(
                    f"n={n}: {v:.12e}" for n, v in terms
                )
                or "none",
            }
        )

    generator_formula = (
        "g(t)=beta_{0.40,0.70}(t)"
        f"{COEFFS[1]:+.15g} beta_{{0.90,1.30}}(t)"
        f"{COEFFS[2]:+.15g} beta_{{1.70,2.30}}(t), "
        "beta_{r,R}(t)=exp(-(R-r)^2/((t-r)(R-t))) on r<t<R and 0 otherwise"
    )
    transported_packet = (
        "For u_G=Cg and G(s)=ghat(s): "
        "M(J_a P_infty tau_log2 (I-P_infty) u_G)(s)="
        "[T_{1/4} mathsf P_infty M_{2^{s-1/2}}"
        "(I-mathsf P_infty) M_zeta G](s). "
        "Expanded: [T_{1/4} mathsf P_infty M_zeta(2^{s-1/2}G)](s)"
        "-[T_{1/4} mathsf P_infty M_{2^{s-1/2}} mathsf P_infty M_zeta G](s)."
    )
    target_form = (
        "C h(t)=sum_{n>=1} h(t/n)/n-hhat(1), "
        "M(C h)(s)=zeta(s) hhat(s). For h=g, the computed target is zeta(s)G(s)."
    )
    comparison = (
        "Direct h=g comparison would require "
        "[T_{1/4} mathsf P_infty M_{2^{s-1/2}}(I-mathsf P_infty)M_zeta G](s)=zeta(s)G(s). "
        "General CP-RED would require the same left side to equal zeta(s)H(s) for a legal H. "
        "The computation halts at applying mathsf P_infty and T_{1/4} to the explicit profile G; inherited records give their formal placement but not their kernel, matrix elements, or zeta-ideal covariance on this profile."
    )

    write_csv(
        OUT / "test_generators_step170.csv",
        [
            "id",
            "type",
            "support",
            "formula",
            "coefficients",
            "moment_ghat_0",
            "moment_ghat_1",
            "legality_check",
        ],
        [
            {
                "id": "G170_1",
                "type": "corrected C_c^infty bump triple",
                "support": support,
                "formula": generator_formula,
                "coefficients": json.dumps(COEFFS),
                "moment_ghat_0": f"{moment0:.16e}",
                "moment_ghat_1": f"{moment1:.16e}",
                "legality_check": "passes numerical moment vanishings; endpoints vanish to infinite order by bump definition",
            }
        ],
    )

    write_csv(
        OUT / "co_poisson_samples_step170.csv",
        ["generator_id", "t", "C_g_t", "nonzero_terms_n_g_t_over_n"],
        cg_rows,
    )
    write_csv(
        OUT / "mellin_samples_step170.csv",
        ["generator_id", "s", "ghat", "zeta_times_ghat", "m_log2", "note"],
        sample_rows,
    )

    write_csv(
        OUT / "per_generator_computation_step170.csv",
        [
            "generator_id",
            "u_formula",
            "transported_packet_symbolic_form",
            "target_co_poisson_form",
            "comparison",
            "verdict_per_generator",
            "actual_computation_rows",
        ],
        [
            {
                "generator_id": "G170_1",
                "u_formula": "u_G := Cg, the legal Burnol/co-Poisson atom generated by G170_1",
                "transported_packet_symbolic_form": transported_packet,
                "target_co_poisson_form": target_form,
                "comparison": comparison,
                "verdict_per_generator": "V_CPRED_STUCK",
                "actual_computation_rows": "test_generators_step170.csv:G170_1; co_poisson_samples_step170.csv:G170_1; mellin_samples_step170.csv:G170_1",
            }
        ],
    )

    write_csv(
        OUT / "verdict_step170.csv",
        [
            "overall_verdict",
            "supporting_generator_rows",
            "key_computation",
            "stuck_algebraic_step",
            "branch_C_status_update",
        ],
        [
            {
                "overall_verdict": "V_CPRED_STUCK",
                "supporting_generator_rows": "G170_1",
                "key_computation": transported_packet,
                "stuck_algebraic_step": "Need explicit action or zeta-ideal covariance of mathsf P_infty and T_a on M_zeta G for the displayed corrected bump profile.",
                "branch_C_status_update": "unchanged",
            }
        ],
    )

    write_csv(
        OUT / "branch_C_status_step170.csv",
        ["branch", "previous_status", "step170_update", "basis", "next_step_lane"],
        [
            {
                "branch": "Xi_cP_shifted_l / CP-RED_{l,a}",
                "previous_status": "V_stuck_attempt",
                "step170_update": "V_CPRED_STUCK",
                "basis": "explicit legal generator computed; transported packet remains unevaluable past inherited P_infty/T_a placement",
                "next_step_lane": "derive or refute zeta-ideal covariance for mathsf P_infty and T_a on legal co-Poisson profiles",
            }
        ],
    )

    write_csv(
        OUT / "residual_tree_step170.csv",
        ["node_id", "parent_id", "tree", "node_type", "previous_status", "updated_status", "source_step", "notes"],
        [
            {
                "node_id": "Xi_BC",
                "parent_id": "",
                "tree": "Burnol_Sonine",
                "node_type": "parent_residual",
                "previous_status": "active",
                "updated_status": "active",
                "source_step": "158-170",
                "notes": "Parent residual carried unchanged.",
            },
            {
                "node_id": "Xi_cP_shifted_l",
                "parent_id": "Xi_BC",
                "tree": "Burnol_Sonine",
                "node_type": "child_residual",
                "previous_status": "V_stuck_attempt",
                "updated_status": "V_CPRED_STUCK",
                "source_step": "169-170",
                "notes": "Explicit generator test reaches the same P_infty/T_a algebraic gap.",
            },
        ],
    )

    write_csv(
        OUT / "route_status_step170.csv",
        ["route", "status", "orientation", "cascade_role", "notes"],
        [
            {
                "route": "Branch_C_shifted_co_Poisson",
                "status": "V_CPRED_STUCK",
                "orientation": "adequacy",
                "cascade_role": "Burnol_child",
                "notes": "Concrete co-Poisson atom test did not establish or refute CP-RED.",
            },
            {
                "route": "public-shadow non-promotion",
                "status": "retained_no_go",
                "orientation": "framework_boundary",
                "cascade_role": "retained",
                "notes": "No public shadow is promoted to an exact carrier identity.",
            },
            {
                "route": "finite-window Calkin blindness",
                "status": "retained_no_go",
                "orientation": "framework_boundary",
                "cascade_role": "retained",
                "notes": "No finite diagnostic is promoted beyond its scope.",
            },
            {
                "route": "auxiliary-GRH smuggling",
                "status": "retained_no_go",
                "orientation": "Hecke_boundary",
                "cascade_role": "retained",
                "notes": "No auxiliary zero theorem is imported.",
            },
            {
                "route": "incomplete character spectrum support-only",
                "status": "retained_no_go",
                "orientation": "Hecke_boundary",
                "cascade_role": "retained",
                "notes": "Tail and exhaustivity gates remain required.",
            },
            {
                "route": "scalar L-function identity is not carrier identity",
                "status": "retained_no_go",
                "orientation": "H6_boundary",
                "cascade_role": "retained",
                "notes": "No scalar identity is treated as a carrier equality.",
            },
        ],
    )

    write_csv(
        OUT / "construction_tasks_step170.csv",
        ["task_id", "step", "lane", "status", "description", "trigger"],
        [
            {
                "task_id": "T171_1",
                "step": 171,
                "lane": "derive_P_infty_zeta_ideal_covariance_on_G170_class",
                "status": "forward_push",
                "description": "Compute whether mathsf P_infty M_zeta G admits a zeta-divisible representation on corrected bump profiles.",
                "trigger": "V_CPRED_STUCK",
            },
            {
                "task_id": "T171_2",
                "step": 171,
                "lane": "derive_Ta_zeta_ideal_covariance",
                "status": "forward_push",
                "description": "Compute whether T_a mathsf P_infty M_zeta H remains in zeta times the legal Burnol Mellin class.",
                "trigger": "V_CPRED_STUCK",
            },
            {
                "task_id": "T171_3",
                "step": 171,
                "lane": "operator_kernel_lookup_or_countertest",
                "status": "forward_push",
                "description": "Locate an inherited exact kernel/matrix for P_infty or T_a; if found, evaluate it on G170_1 and compare with zeta divisibility.",
                "trigger": "V_CPRED_STUCK",
            },
        ],
    )

    content_rows = [
        {
            "output": "step170_results_summary.md",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "V_CPRED_STUCK",
            "actual_computation_rows": "G170_1",
            "notes": "Narrative records corrected bump moments, Cg samples, Mellin samples, and the transported-packet halt.",
        },
        {
            "output": "step170_schema.json",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "recorded",
            "actual_computation_rows": "G170_1",
            "notes": "Machine-readable verdict and generator computation.",
        },
        {
            "output": "content_classification_step170.csv",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "recorded",
            "actual_computation_rows": "G170_1",
            "notes": "Classifies every output and ties diagnostic claims to computation rows.",
        },
        {
            "output": "nonclaim_boundary_step170.md",
            "category": "nonclaim_boundary",
            "grade": "n/a",
            "status": "active",
            "actual_computation_rows": "G170_1",
            "notes": "Required nonclaims and no-go preservation.",
        },
        {
            "output": "step170_cp_red_test.tex",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "V_CPRED_STUCK",
            "actual_computation_rows": "G170_1",
            "notes": "Self-contained computation on the corrected bump generator.",
        },
        {
            "output": "run_step170_cp_red_checks.py",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "recorded",
            "actual_computation_rows": "G170_1",
            "notes": "Validation script.",
        },
        {
            "output": "generate_step170_artifacts.py",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "recorded",
            "actual_computation_rows": "G170_1",
            "notes": "Artifact generation script for the explicit bump computation.",
        },
        {
            "output": "test_generators_step170.csv",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "computed",
            "actual_computation_rows": "G170_1",
            "notes": "Explicit corrected bump generator and moment checks.",
        },
        {
            "output": "per_generator_computation_step170.csv",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "computed",
            "actual_computation_rows": "G170_1",
            "notes": "Transported packet and co-Poisson comparison.",
        },
        {
            "output": "co_poisson_samples_step170.csv",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "computed",
            "actual_computation_rows": "G170_1",
            "notes": "Direct finite-term Cg(t) samples.",
        },
        {
            "output": "mellin_samples_step170.csv",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "computed",
            "actual_computation_rows": "G170_1",
            "notes": "G(s), zeta(s)G(s), and shift multiplier samples.",
        },
        {
            "output": "verdict_step170.csv",
            "category": "finite_carrier_diagnostic_content",
            "grade": "finite-carrier diagnostic",
            "status": "V_CPRED_STUCK",
            "actual_computation_rows": "G170_1",
            "notes": "Overall verdict with supporting computation row.",
        },
        {
            "output": "branch_C_status_step170.csv",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "updated",
            "actual_computation_rows": "G170_1",
            "notes": "Branch C remains unchanged after explicit test.",
        },
        {
            "output": "residual_tree_step170.csv",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "updated",
            "actual_computation_rows": "G170_1",
            "notes": "Residual tree update.",
        },
        {
            "output": "route_status_step170.csv",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "updated",
            "actual_computation_rows": "G170_1",
            "notes": "Route statuses and retained no-gos.",
        },
        {
            "output": "construction_tasks_step170.csv",
            "category": "organizational_record",
            "grade": "n/a",
            "status": "forward_push_lanes",
            "actual_computation_rows": "G170_1",
            "notes": "Step 171 lanes.",
        },
    ]
    write_csv(
        OUT / "content_classification_step170.csv",
        ["output", "category", "grade", "status", "actual_computation_rows", "notes"],
        content_rows,
    )

    schema = {
        "step": 170,
        "orientation": "adequacy",
        "active_residual": "Xi_BC / Xi_cP_shifted_l",
        "main_object": "CP-RED_{l,a} membership test on explicit generators",
        "inherited_records": [119, 153, 154, 165, 169],
        "test_generators": [
            {
                "id": "G170_1",
                "type": "corrected C_c^infty bump triple",
                "support": support,
                "formula": generator_formula,
            }
        ],
        "per_generator_computation": [
            {
                "generator_id": "G170_1",
                "transported_packet": transported_packet,
                "target_co_poisson_form": target_form,
                "comparison": comparison,
                "verdict_per_generator": "V_CPRED_STUCK",
            }
        ],
        "factorization_verdict": "V_CPRED_STUCK",
        "stuck_algebraic_step": {
            "named_record_gap": "P_infty/T_a action gap on explicit co-Poisson profile",
            "detail": "Inherited records provide T_a=M_Gamma J_a U_infty^{-1} and formal P_infty placement, but not the exact action needed to decide zeta-divisibility for G170_1.",
        },
        "retained_nogos": [
            "public-shadow non-promotion",
            "finite-window Calkin blindness",
            "auxiliary-GRH smuggling",
            "incomplete character spectrum is support-only without tail/exhaustivity",
            "scalar L-function identity is not carrier identity",
        ],
        "branch_C_status_update": "unchanged",
        "final_verdict": "V_CPRED_STUCK",
        "next_step": 171,
        "step171_forward_push_lanes": [
            "derive_P_infty_zeta_ideal_covariance_on_G170_class",
            "derive_Ta_zeta_ideal_covariance",
            "operator_kernel_lookup_or_countertest",
        ],
        "numeric_checks": {
            "moment_ghat_0": moment0,
            "moment_ghat_1": moment1,
            "sample_files": ["co_poisson_samples_step170.csv", "mellin_samples_step170.csv"],
        },
    }
    (OUT / "step170_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    summary = f"""# Step 170 Results Summary

Verdict: `V_CPRED_STUCK`.

The explicit legal generator is `G170_1`, supported in {support}. It is
constructed from three fixed smooth bumps
`beta_{{r,R}}(t)=exp(-(R-r)^2/((t-r)(R-t)))` on `r<t<R`, zero otherwise:

`{generator_formula}`.

The computed moment checks are

- `ghat(0) = {moment0:.16e}`
- `ghat(1) = {moment1:.16e}`

so the inherited Step 119 co-Poisson legality conditions hold to numerical
quadrature precision. The corresponding legal Burnol atom is
`u_G := Cg`, with
`Cg(t)=sum_{{n>=1}} g(t/n)/n - ghat(1)`.

For the first test generator and shift `ell=log(2)`, the inherited Step 169
subclass computation gives the transported packet

`{transported_packet}`

The co-Poisson target for the same generator has
`M(Cg)(s)=zeta(s)G(s)`. The numerical Mellin samples in
`mellin_samples_step170.csv` include the first nontrivial zeta-zero ordinate;
there the target `zeta(s)G(s)` is zero to quadrature precision.

The comparison halts before a POS/NEG/PART verdict: the inherited records do
not give the exact action of `mathsf P_infty` or `T_a` on the explicit profile
`M_zeta G`, nor a zeta-ideal covariance statement for those operators. Thus
the computation neither establishes a legal `h` with transported packet `C h`
nor proves that no such `h` exists.
"""
    (OUT / "step170_results_summary.md").write_text(summary)

    nonclaim = """# Step 170 Nonclaim Boundary

This step does not establish RH.

This step does not establish `Xi_BC = 0`.

This step does not prove CP-RED for the legal Burnol generator class.

This step does not disprove CP-RED.

This step does not close Branch C.

This step does not promote the unshifted co-Poisson identity
`M(Cg)=zeta*ghat` to the shifted packet
`J_a P_infty tau_l (I-P_infty)u` without computing the missing
`P_infty` and `T_a` actions.

This step retains all five inherited no-go boundaries:

- Public-shadow non-promotion.
- Finite-window Calkin blindness.
- Auxiliary-GRH smuggling.
- Incomplete character spectrum is support-only without tail/exhaustivity.
- Scalar L-function identity is not carrier identity.
"""
    (OUT / "nonclaim_boundary_step170.md").write_text(nonclaim)

    tex = rf"""\documentclass[11pt]{{article}}
\usepackage{{amsmath,amssymb,amsthm,mathtools,booktabs,geometry}}
\geometry{{margin=1in}}
\title{{Step 170: CP-RED Test on Explicit Legal Burnol Generators}}
\author{{RH Membrane / Burnol--Sonine Residual Thread}}
\date{{}}
\newcommand{{\Chat}}{{\mathcal C}}
\newcommand{{\Mell}}{{\mathcal M}}
\newcommand{{\Pinfty}}{{P_\infty}}
\newcommand{{\Pinfm}}{{\mathsf P_\infty}}
\newcommand{{\Uinf}}{{\mathcal U_\infty}}
\begin{{document}}
\maketitle

\section{{Inherited Records Used}}
Step 119 supplies, for legal Burnol generators,
\[
  \widehat g(s)=\int_0^\infty g(t)t^{{-s}}\,dt,\qquad
  \Chat g(t)=\sum_{{n\ge1}}\frac{{g(t/n)}}n-\widehat g(1),
\]
and, when \(\widehat g(0)=\widehat g(1)=0\),
\[
  \Mell(\Chat g)(s)=\zeta(s)\widehat g(s).
\]
Step 169 supplies the shifted packet formula
\[
  \Mell(J_a\Pinfty\tau_\ell(I-\Pinfty)u)(s)
  =
  [T_a\Pinfm M_{{m_\ell}}(I-\Pinfm)\Uinf u](s),
  \qquad m_\ell(s)=e^{{-\ell(1/2-s)}}.
\]
For the co-Poisson subclass \(u=\Chat g\), Step 169 records
\[
  \Uinf u = M_\zeta G,\qquad G=\widehat g,
\]
so
\[
  \Mell(J_a\Pinfty\tau_\ell(I-\Pinfty)\Chat g)(s)
  =
  [T_a\Pinfm M_{{m_\ell}}(I-\Pinfm)M_\zeta G](s).
\]

\section{{Explicit Legal Generator}}
Take \(a=1/4\), \(A=4\), and \(\ell=\log 2\).  For \(r<R\), define
\[
  \beta_{{r,R}}(t)=
  \begin{{cases}}
  \exp\!\left(-\dfrac{{(R-r)^2}}{{(t-r)(R-t)}}\right),& r<t<R,\\
  0,&\text{{otherwise.}}
  \end{{cases}}
\]
This is \(C_c^\infty\) and vanishes to infinite order at the endpoints.  The
test generator is
\[
\begin{{aligned}}
g(t)=&\ \beta_{{0.40,0.70}}(t)
({COEFFS[1]:+.15g})\beta_{{0.90,1.30}}(t)
({COEFFS[2]:+.15g})\beta_{{1.70,2.30}}(t).
\end{{aligned}}
\]
Its support is contained in \([1/4,4]\).  Direct quadrature gives
\[
  \widehat g(0)={moment0:.16e},\qquad
  \widehat g(1)={moment1:.16e}.
\]
Thus \(g\) is a legal Step 119 generator to numerical quadrature precision.

\section{{Co-Poisson Computation}}
The Burnol atom is \(u_G=\Chat g\), i.e.
\[
  u_G(t)=\sum_{{n\ge1}}\frac{{g(t/n)}}n-\widehat g(1).
\]
Since \(g\) is supported in \([0.40,2.30]\), this is a finite sum at each fixed
\(t\).  For example:
\[
\begin{{array}}{{c|c}}
t & u_G(t)\\
\hline
0.45 & {cg_rows[1]["C_g_t"]}\\
0.60 & {cg_rows[2]["C_g_t"]}\\
1.00 & {cg_rows[3]["C_g_t"]}\\
2.00 & {cg_rows[4]["C_g_t"]}\\
3.00 & {cg_rows[5]["C_g_t"]}
\end{{array}}
\]
The Mellin target is
\[
  \Mell(u_G)(s)=\zeta(s)G(s),\qquad G(s)=\widehat g(s).
\]
At the sampled first zero ordinate \(\tau_1=14.134725141734693\),
\[
  G(1/2+i\tau_1)={sample_rows[3]["ghat"]},\qquad
  \zeta(1/2+i\tau_1)G(1/2+i\tau_1)
  ={sample_rows[3]["zeta_times_ghat"]}.
\]

\section{{Transported Packet for the Same Legal Input}}
For \(u_G=\Chat g\) and \(\ell=\log 2\), \(m_\ell(s)=2^{{s-1/2}}\).  The
inherited operator records give the explicit transported packet
\[
\boxed{{
  \Mell(J_{{1/4}}\Pinfty\tau_{{\log 2}}(I-\Pinfty)u_G)(s)
  =
  [T_{{1/4}}\Pinfm M_{{2^{{s-1/2}}}}(I-\Pinfm)M_\zeta G](s).
}}
\]
Expanding the complementary projection:
\[
\begin{{aligned}}
&[T_{{1/4}}\Pinfm M_{{2^{{s-1/2}}}}(I-\Pinfm)M_\zeta G](s)\\
&\quad=
[T_{{1/4}}\Pinfm M_\zeta(2^{{s-1/2}}G)](s)
-
[T_{{1/4}}\Pinfm M_{{2^{{s-1/2}}}}\Pinfm M_\zeta G](s).
\end{{aligned}}
\]

\section{{Comparison With Co-Poisson Form}}
To verify CP-RED on this input, one must produce a legal \(h\) such that
\[
  [T_{{1/4}}\Pinfm M_{{2^{{s-1/2}}}}(I-\Pinfm)M_\zeta G](s)
  =
  \zeta(s)\widehat h(s).
\]
The direct same-generator comparison \(h=g\) would require
\[
  [T_{{1/4}}\Pinfm M_{{2^{{s-1/2}}}}(I-\Pinfm)M_\zeta G](s)
  =
  \zeta(s)G(s).
\]
This is the exact algebraic step where the computation halts.  The inherited
records provide the formal placement of \(\Pinfm\), \(M_{{m_\ell}}\), and \(T_a\),
but do not provide the kernel or matrix elements of \(\Pinfm\), the action of
\(T_a\) on this profile, or a zeta-ideal covariance theorem of the form
\[
  \Pinfm M_\zeta G \in M_\zeta(\text{{legal profiles}}),
  \qquad
  T_a\Pinfm M_\zeta H\in M_\zeta(\text{{legal profiles}}).
\]

\section{{Verdict and Nonclaim}}
\[
  \boxed{{\texttt{{factorization\_verdict = V\_CPRED\_STUCK}}.}}
\]
The step computes an explicit legal generator and its co-Poisson packet, and it
computes the inherited shifted-packet expression for the corresponding legal
input \(u_G=\Chat g\).  It neither establishes nor refutes CP-RED because the
missing operation is the exact \(\Pinfm/T_a\) action on the explicit profile
\(M_\zeta G\).

This step does not establish RH, does not establish \(\Xi_{{BC}}=0\), and does
not promote the unshifted co-Poisson identity to a shifted-packet identity.
\end{{document}}
"""
    (OUT / "step170_cp_red_test.tex").write_text(tex)


if __name__ == "__main__":
    main()
