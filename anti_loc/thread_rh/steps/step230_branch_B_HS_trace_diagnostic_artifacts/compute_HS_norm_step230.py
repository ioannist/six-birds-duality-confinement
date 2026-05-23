#!/usr/bin/env python3
"""Step 230 HS/trace diagnostic from the Step 216 orthonormalized kappa data.

This is intentionally conservative.  Step 216 already performed the expensive
Gram-Schmidt and C_l evaluations for CAND1 through n=20 and CAND2 through n=10.
Here we compute the Hilbert-Schmidt trace partial sums and classify whether the
finite data can support convergence/divergence for the full H_eta.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path("/home/repos/six-birds-foundations-iii")
OUT = ROOT / "anti_loc/thread/steps/step230_branch_B_HS_trace_diagnostic_artifacts"
STEP216 = ROOT / "anti_loc/thread/steps/step216_branch_A_gram_schmidt_weyl_artifacts/gram_schmidt_step216.csv"


def read_step216() -> list[dict[str, str]]:
    with STEP216.open() as f:
        return list(csv.DictReader(f))


def compute_terms(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    cumulative: dict[str, float] = {}
    for row in rows:
        model = row["model"]
        cumulative.setdefault(model, 0.0)
        c = row["C_l_v_n_norm"]
        c_norm = float("nan") if c == "nan" else float(c)
        term = float("nan") if not math.isfinite(c_norm) else c_norm * c_norm
        if math.isfinite(term):
            cumulative[model] += term
        out.append(
            {
                "model": model,
                "n": int(row["n"]),
                "raw_norm": row["raw_norm"],
                "w_residual_norm": row["w_residual_norm"],
                "relative_residual_norm": row["relative_residual_norm"],
                "stability": row["stability"],
                "C_l_v_n_norm": c if c != "nan" else "nan",
                "C_l_v_n_squared": f"{term:.17e}" if math.isfinite(term) else "nan",
                "cumulative_HS_partial_sum": f"{cumulative[model]:.17e}",
                "error_bound_in_norm": row["error_bound"],
            }
        )
    return out


def analyze(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for model in sorted(set(str(r["model"]) for r in rows)):
        mrows = [r for r in rows if r["model"] == model]
        finite = [r for r in mrows if r["C_l_v_n_squared"] != "nan"]
        usable = [r for r in finite if r["stability"] == "usable"]
        low = [r for r in finite if r["stability"] == "low_absolute_signal"]
        last_sum = float(finite[-1]["cumulative_HS_partial_sum"]) if finite else float("nan")
        terms = [float(r["C_l_v_n_squared"]) for r in finite]
        tail5 = terms[-5:] if len(terms) >= 5 else terms
        min_tail5 = min(tail5) if tail5 else float("nan")
        mean_tail5 = sum(tail5) / len(tail5) if tail5 else float("nan")
        if model == "CAND1":
            verdict = "precision_limited_CAND1_low_absolute_signal"
            interpretation = (
                "CAND1 gives only two high-confidence orthogonal directions; "
                "later terms cannot certify HS convergence or divergence."
            )
        else:
            verdict = "comparison_model_divergence_diagnostic"
            interpretation = (
                "CAND2 stable orthogonal directions have nondecaying terms; "
                "if this were the true transport model, HS would diverge."
            )
        results.append(
            {
                "model": model,
                "basis_size": len(mrows),
                "finite_terms": len(finite),
                "usable_terms": len(usable),
                "low_signal_terms": len(low),
                "partial_sum": f"{last_sum:.17e}",
                "min_tail5_term": f"{min_tail5:.17e}" if math.isfinite(min_tail5) else "nan",
                "mean_tail5_term": f"{mean_tail5:.17e}" if math.isfinite(mean_tail5) else "nan",
                "analysis_verdict": verdict,
                "interpretation": interpretation,
            }
        )
    return results


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_step216()
    terms = compute_terms(rows)
    fields = list(terms[0].keys())
    with (OUT / "HS_terms_step230.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(terms)

    analysis = analyze(terms)
    with (OUT / "convergence_analysis_step230.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(analysis[0].keys()))
        writer.writeheader()
        writer.writerows(analysis)

    robustness = [
        {
            "check": "CAND1_step216_reuse",
            "status": "primary_Burnol_boundary_model",
            "value": analysis[0]["partial_sum"] if analysis[0]["model"] == "CAND1" else analysis[1]["partial_sum"],
            "notes": "Uses Step 216 CAND1 orthonormalized kappa directions n=1..20 at mpmath 80 input precision.",
        },
        {
            "check": "CAND2_comparison",
            "status": "stable_but_not_verified_transport",
            "value": analysis[1]["partial_sum"] if analysis[1]["model"] == "CAND2" else analysis[0]["partial_sum"],
            "notes": "Zeta-form comparison model gives nondecaying HS terms but is not asserted as the true a=1/2 kappa.",
        },
        {
            "check": "ell_variation",
            "status": "not_rerun_this_step",
            "value": "ell=log2 only",
            "notes": "Step 230 remains partial for ell robustness; inherited Branch A wavepacket scans cover ell variation for C_l P_infty only.",
        },
    ]
    with (OUT / "robustness_step230.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness[0].keys()))
        writer.writeheader()
        writer.writerows(robustness)

    with (OUT / "compute_HS_norm_output_step230.txt").open("w") as f:
        f.write("Step 230 HS trace diagnostic\n")
        for row in analysis:
            f.write(
                f"{row['model']}: finite_terms={row['finite_terms']} "
                f"usable={row['usable_terms']} partial_sum={row['partial_sum']} "
                f"mean_tail5={row['mean_tail5_term']} verdict={row['analysis_verdict']}\n"
            )
        f.write("final_verdict=V_HS_partial\n")

    print((OUT / "compute_HS_norm_output_step230.txt").read_text())


if __name__ == "__main__":
    main()
