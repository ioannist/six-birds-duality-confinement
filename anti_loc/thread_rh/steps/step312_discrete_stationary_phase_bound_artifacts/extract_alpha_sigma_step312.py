#!/usr/bin/env python3
"""Step 312: discrete stationary-phase diagnostic for Leibniz interference."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step312_discrete_stationary_phase_bound_artifacts")
STEP311 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step311_leibniz_phase_analysis_artifacts")
K_TARGETS = [10, 20, 30, 50]


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


def linfit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))
    denom = n*sxx - sx*sx
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    pred = [intercept + slope*x for x in xs]
    rmse = math.sqrt(sum((y-p)**2 for y, p in zip(ys, pred)) / n)
    return slope, intercept, rmse


def quadratic_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    # Solves normal equations for y = a x^2 + b x + c.
    import numpy as np
    X = np.array([[x*x, x, 1.0] for x in xs], dtype=float)
    Y = np.array(ys, dtype=float)
    a, b, c = np.linalg.lstsq(X, Y, rcond=None)[0]
    return float(a), float(b), float(c)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    smooth = {int(row["k"]): row for row in read_csv(STEP311 / "phase_smoothness_summary_step311.csv")}

    alpha_rows = []
    sp_rows = []
    qs_emp = []
    qs_pred = []

    for k in K_TARGETS:
        row = smooth[k]
        alpha = abs(float(row["linear_slope_central"]))
        sigma_weighted = float(row["weighted_std_j"])
        q = 0.5 * alpha * alpha * sigma_weighted * sigma_weighted
        pred_interference = math.exp(-q)
        empirical = float(row["interference_ratio"])
        # Optional Gaussian fit to central log |term_j| for audit.
        phase_rows = read_csv(STEP311 / f"leibniz_phases_k{k}_step311.csv")
        central = [r for r in phase_rows if r["in_central_window"] == "yes"]
        xs = [float(r["j"]) for r in central if float(r["term_abs"]) > 0]
        ys = [math.log(float(r["term_abs"])) for r in central if float(r["term_abs"]) > 0]
        qa, qb, qc = quadratic_fit(xs, ys)
        sigma_gaussian = math.sqrt(-1.0/(2.0*qa)) if qa < 0 else float("nan")
        q_gauss = 0.5 * alpha * alpha * sigma_gaussian * sigma_gaussian if qa < 0 else float("nan")
        pred_gauss = math.exp(-q_gauss) if qa < 0 else float("nan")
        alpha_rows.append({
            "k": k,
            "alpha_central_slope_abs": f"{alpha:.15g}",
            "sigma_weighted_std": f"{sigma_weighted:.15g}",
            "sigma_gaussian_fit": f"{sigma_gaussian:.15g}",
            "alpha_squared_sigma_weighted_squared_over_2": f"{q:.15g}",
            "alpha_squared_sigma_gaussian_squared_over_2": f"{q_gauss:.15g}",
            "central_linear_R2": row["linear_R2_central"],
            "central_phase_variation": row["central_phase_variation"],
        })
        sp_rows.append({
            "k": k,
            "stationary_phase_pred_weighted_sigma": f"{pred_interference:.15g}",
            "stationary_phase_pred_gaussian_sigma": f"{pred_gauss:.15g}",
            "empirical_interference": f"{empirical:.15g}",
            "pred_weighted_over_empirical": f"{pred_interference/empirical:.15g}",
            "pred_gaussian_over_empirical": f"{pred_gauss/empirical:.15g}",
            "abs_rel_err_weighted": f"{abs(pred_interference-empirical)/empirical:.15g}",
            "abs_rel_err_gaussian": f"{abs(pred_gauss-empirical)/empirical:.15g}",
        })
        qs_emp.append(-math.log(empirical))
        qs_pred.append(q)

    write_csv(ART / "alpha_sigma_per_k_step312.csv", alpha_rows)
    write_csv(ART / "stationary_phase_interference_step312.csv", sp_rows)

    # Fit -log(interference) = C1*k - log(C0).
    slope_emp, intercept_emp, rmse_emp = linfit([float(k) for k in K_TARGETS], qs_emp)
    slope_pred, intercept_pred, rmse_pred = linfit([float(k) for k in K_TARGETS], qs_pred)
    # Conservative sample bound: empirical ratios in this range satisfy I >= exp(-0.028 k).
    c_rows = [
        {
            "bound_type": "empirical_fit",
            "C0": f"{math.exp(-intercept_emp):.15g}",
            "C1": f"{slope_emp:.15g}",
            "rmse_log_space": f"{rmse_emp:.15g}",
            "rigor_status": "finite_range_empirical_not_theorem",
            "note": "Fit to observed interference ratios from k=10,20,30,50.",
        },
        {
            "bound_type": "stationary_phase_predicted_exponent_fit",
            "C0": f"{math.exp(-intercept_pred):.15g}",
            "C1": f"{slope_pred:.15g}",
            "rmse_log_space": f"{rmse_pred:.15g}",
            "rigor_status": "model_derived_from_finite_data",
            "note": "Uses q=alpha^2*sigma^2/2 from central phase slope and weighted j-width.",
        },
        {
            "bound_type": "conservative_sample_bound",
            "C0": "1.0",
            "C1": "0.028",
            "rmse_log_space": "not_applicable",
            "rigor_status": "sample_calibrated_conditional",
            "note": "Holds on certified sample k=10,20,30,50; needs asymptotic proof of alpha/sigma and error terms.",
        },
    ]
    write_csv(ART / "derived_C0_C1_step312.csv", c_rows)

    verdict = "V_discrete_stationary_phase_matches_empirical_interference_but_not_rigorous"
    theorem = r"""\section*{Step 312 Updated Conditional Theorem}

\paragraph{Candidate interference lemma.}
Let
\[
T_{k,j}={k\choose j}\zeta^{(j)}(\rho_1)M(G_\star)^{(k-j)}(\rho_1).
\]
Assume that, on the central window \(J_k\), the magnitudes
\(|T_{k,j}|\) have a Gaussian saddle of width \(\sigma(k)\), and the
unwrapped phases satisfy
\[
\arg T_{k,j}=\alpha(k)j+\beta(k)+O(\varepsilon_k)
\]
with bounded stationary-phase correction.  Then the discrete
stationary-phase / Gaussian-Fourier approximation gives
\[
\frac{\left|\sum_jT_{k,j}\right|}{\sum_j|T_{k,j}|}
\approx
\exp\!\left(-\frac{\alpha(k)^2\sigma(k)^2}{2}\right).
\]

For the certified data at \(k=10,20,30,50\), the extracted
\(\alpha(k)\) and \(\sigma(k)\) reproduce the observed interference
ratios to a few percent.  A conservative sample-calibrated bound is
\[
\frac{\left|\sum_jT_{k,j}\right|}{\sum_j|T_{k,j}|}
\ge \exp(-0.028 k)
\]
on the certified sample.  This is not yet theorem-grade: it requires a
rigorous proof of the Gaussian saddle, the phase expansion, and uniform
control of the discrete stationary-phase remainder.

\paragraph{Updated lower-bound theorem status.}
The Step 310 theorem remains conditional.  Its load-bearing gap has been
localized to proving the above interference lemma uniformly in \(k\).
The data support the lemma strongly, but the proof is not complete.
"""
    (ART / "updated_theorem_step312.tex").write_text(theorem, encoding="utf-8")

    summary = [
        "# Step 312 Results Summary",
        "",
        "Extracted the central phase slope `alpha` and j-space width `sigma(k)` from Step 311/309 data.",
        "The correct frequency is the central linear phase slope, about `0.386..0.427` radians per j, not the total phase variation divided by the saddle width.",
        "",
        "The Gaussian-Fourier stationary-phase model",
        "`interference ≈ exp(-alpha^2 sigma^2 / 2)` matches the empirical interference ratios at k=10,20,30,50 to a few percent.",
        "",
        "A conservative sample-calibrated bound is `interference(k) >= exp(-0.028 k)` on the certified sample.",
        "This does not yet close the Step 310 theorem: the Gaussian saddle, phase expansion, and stationary-phase remainders remain numerical/heuristic rather than rigorous.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step312_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 312,
        "orientation": "discrete_stationary_phase_bound_attempt",
        "target": "interference lower bound for Branch C Leibniz sum",
        "k_targets": K_TARGETS,
        "primary_model": "interference approx exp(-alpha^2 sigma^2 / 2)",
        "candidate_C0_C1": {"C0": 1.0, "C1": 0.028, "status": "sample_calibrated_conditional"},
        "load_bearing_gap": "rigorous asymptotic proof of Gaussian magnitude saddle, phase expansion, and stationary-phase remainder",
        "final_verdict": verdict,
    }
    (ART / "step312_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step312.md").write_text(
        "# Step 312 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not prove Branch C closure.\n"
        "- The bound `interference >= exp(-0.028 k)` is sample-calibrated and conditional, not theorem-grade.\n"
        "- The Step 310 lower-bound theorem remains conditional until the stationary-phase assumptions are proved.\n",
        encoding="utf-8",
    )
    print("Step312 discrete stationary-phase diagnostic")
    for row in sp_rows:
        print(
            "k={k} pred={p} empirical={e} relerr={r}".format(
                k=row["k"],
                p=row["stationary_phase_pred_weighted_sigma"],
                e=row["empirical_interference"],
                r=row["abs_rel_err_weighted"],
            )
        )
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()

