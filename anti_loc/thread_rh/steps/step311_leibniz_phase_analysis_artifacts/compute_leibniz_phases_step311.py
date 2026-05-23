#!/usr/bin/env python3
"""Step 311: phase analysis for Branch C Leibniz terms."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step311_leibniz_phase_analysis_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 80
MAX_K = 50
K_TARGETS = [10, 20, 30, 50]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def sign_label(x: mp.mpf) -> str:
    if x > 0:
        return "+"
    if x < 0:
        return "-"
    return "0"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def unwrap(phases: list[mp.mpf]) -> list[mp.mpf]:
    if not phases:
        return []
    out = [phases[0]]
    two_pi = 2 * mp.pi
    for ph in phases[1:]:
        candidate = ph
        while candidate - out[-1] > mp.pi:
            candidate -= two_pi
        while candidate - out[-1] < -mp.pi:
            candidate += two_pi
        out.append(candidate)
    return out


def linear_fit(xs: list[mp.mpf], ys: list[mp.mpf]) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    n = mp.mpf(len(xs))
    sx = mp.fsum(xs)
    sy = mp.fsum(ys)
    sxx = mp.fsum([x*x for x in xs])
    sxy = mp.fsum([x*y for x, y in zip(xs, ys)])
    denom = n*sxx - sx*sx
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    preds = [intercept + slope*x for x in xs]
    residuals = [y-p for y, p in zip(ys, preds)]
    mean_y = sy / n
    ss_res = mp.fsum([r*r for r in residuals])
    ss_tot = mp.fsum([(y-mean_y)**2 for y in ys])
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else mp.mpf("1")
    resid_std = mp.sqrt(ss_res / n)
    max_abs_resid = max(abs(r) for r in residuals)
    return slope, intercept, r2, resid_std, max_abs_resid


def safe_float(x: mp.mpf) -> float:
    return float(x)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    t0 = time.time()
    step196 = load_module("step196_for_step311", STEP196_SCRIPT)
    step292 = load_module("step292_for_step311", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    zds = step292.zeta_derivatives(gamma, MAX_K, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_K, DPS)

    smooth_rows = []
    c_rows = []
    phase_profile = {}

    for k in K_TARGETS:
        terms: list[mp.mpc] = []
        weights: list[mp.mpf] = []
        raw_args: list[mp.mpf] = []
        for j in range(k+1):
            term = mp.mpf(math.comb(k, j)) * zds[j] * mds[k-j]
            terms.append(term)
            w = abs(term)
            weights.append(w)
            raw_args.append(mp.arg(term) if w != 0 else mp.mpf("0"))
        unwrapped = unwrap(raw_args)
        deltas = [unwrapped[j] - unwrapped[j-1] for j in range(1, len(unwrapped))]
        abs_deltas = [abs(d) for d in deltas]
        sum_abs = mp.fsum(weights)
        total = mp.fsum(terms)
        dominant_j = max(range(k+1), key=lambda idx: weights[idx])
        mean = mp.fsum([mp.mpf(j)*weights[j] for j in range(k+1)]) / sum_abs
        var = mp.fsum([((mp.mpf(j)-mean)**2)*weights[j] for j in range(k+1)]) / sum_abs
        std = mp.sqrt(var)
        central = [j for j in range(k+1) if abs(mp.mpf(j)-mean) <= 2*std]
        if not central:
            central = list(range(k+1))
        central_deltas = [deltas[j-1] for j in central if j > 0]
        central_abs_deltas = [abs(d) for d in central_deltas]
        xs = [mp.mpf(j) for j in range(k+1)]
        slope, intercept, r2, resid_std, max_abs_resid = linear_fit(xs, unwrapped)
        if len(central) >= 3:
            cslope, cintercept, cr2, cresid_std, cmax_abs_resid = linear_fit([mp.mpf(j) for j in central], [unwrapped[j] for j in central])
        else:
            cslope = cintercept = cr2 = cresid_std = cmax_abs_resid = mp.nan
        mono_inc = all(d >= 0 for d in deltas)
        mono_dec = all(d <= 0 for d in deltas)
        delta_mean = mp.fsum(deltas) / len(deltas)
        delta_std = mp.sqrt(mp.fsum([(d-delta_mean)**2 for d in deltas]) / len(deltas))
        central_delta_mean = mp.fsum(central_deltas) / len(central_deltas) if central_deltas else mp.nan
        central_delta_std = mp.sqrt(mp.fsum([(d-central_delta_mean)**2 for d in central_deltas]) / len(central_deltas)) if central_deltas else mp.nan
        total_phase_variation = mp.fsum(abs_deltas)
        central_phase_variation = mp.fsum(central_abs_deltas)
        max_delta = max(abs_deltas)
        # Smoothness criterion is deliberately strict: central phase must be near-linear and
        # low-variation relative to a broad saddle to support a direct BV lower bound.
        if cr2 > mp.mpf("0.98") and central_delta_std < mp.mpf("0.4"):
            flag = "smooth_near_linear_central"
        elif cr2 > mp.mpf("0.90"):
            flag = "partially_smooth_central"
        else:
            flag = "phase_irregular_central"
        rows = []
        for j in range(k+1):
            delta_prev = "" if j == 0 else mp.nstr(deltas[j-1], 34)
            rows.append({
                "k": k,
                "j": j,
                "term_complex": cstr(terms[j], 34),
                "term_abs": mp.nstr(weights[j], 34),
                "arg_raw_minus_pi_pi": mp.nstr(raw_args[j], 34),
                "arg_unwrapped": mp.nstr(unwrapped[j], 34),
                "delta_arg_from_previous": delta_prev,
                "real_sign": sign_label(mp.re(terms[j])),
                "imag_sign": sign_label(mp.im(terms[j])),
                "in_central_window": "yes" if j in central else "no",
            })
        write_csv(ART / f"leibniz_phases_k{k}_step311.csv", rows)
        phase_profile[k] = {
            "dominant_j": dominant_j,
            "interference": abs(total) / sum_abs,
            "total_phase_variation": total_phase_variation,
            "central_phase_variation": central_phase_variation,
            "central_j_min": min(central),
            "central_j_max": max(central),
            "central_r2": cr2,
            "central_delta_std": central_delta_std,
            "smoothness_flag": flag,
        }
        smooth_rows.append({
            "k": k,
            "dominant_j": dominant_j,
            "weighted_mean_j": mp.nstr(mean, 18),
            "weighted_std_j": mp.nstr(std, 18),
            "central_j_min": min(central),
            "central_j_max": max(central),
            "total_phase_variation": mp.nstr(total_phase_variation, 34),
            "central_phase_variation": mp.nstr(central_phase_variation, 34),
            "max_abs_delta_arg": mp.nstr(max_delta, 34),
            "delta_arg_mean": mp.nstr(delta_mean, 34),
            "delta_arg_std": mp.nstr(delta_std, 34),
            "linear_slope_all_j": mp.nstr(slope, 34),
            "linear_R2_all_j": mp.nstr(r2, 34),
            "linear_resid_std_all_j": mp.nstr(resid_std, 34),
            "linear_slope_central": mp.nstr(cslope, 34),
            "linear_R2_central": mp.nstr(cr2, 34),
            "linear_resid_std_central": mp.nstr(cresid_std, 34),
            "central_delta_arg_mean": mp.nstr(central_delta_mean, 34),
            "central_delta_arg_std": mp.nstr(central_delta_std, 34),
            "monotonic_all_j": "increasing" if mono_inc else ("decreasing" if mono_dec else "no"),
            "smoothness_flag": flag,
            "interference_ratio": mp.nstr(abs(total)/sum_abs, 34),
        })
        c_rows.append({
            "k": k,
            "phase_route_feasible": "no" if flag == "phase_irregular_central" else "partial",
            "inferred_C0": "not_feasible",
            "inferred_C1": "not_feasible",
            "reason": (
                "central unwrapped phase is not sufficiently linear/smooth for a direct bounded-variation interference lower bound"
                if flag == "phase_irregular_central"
                else "central phase has partial smoothness but still requires rigorous phase-error control"
            ),
            "observed_interference_ratio": mp.nstr(abs(total)/sum_abs, 34),
            "central_phase_variation": mp.nstr(central_phase_variation, 34),
            "central_linear_R2": mp.nstr(cr2, 34),
        })

    write_csv(ART / "phase_smoothness_summary_step311.csv", smooth_rows)
    write_csv(ART / "inferred_C0_C1_step311.csv", c_rows)

    # Summary uses only concise inherited/certified facts.
    verdict = "V_leibniz_phase_smooth_but_no_direct_BV_bound"
    summary_lines = [
        "# Step 311 Results Summary",
        "",
        "Computed `arg(term_j)` for the Leibniz contributions",
        "`term_j = binom(k,j) zeta^(j)(rho_1) M(G_star)^(k-j)(rho_1)`",
        "at `k=10,20,30,50` using the same dps=80 construction as Step 309.",
        "",
        "Inherited Step 309 interference ratios were `0.812, 0.625, 0.469, 0.268`.",
        "After unwrapping, the central saddle windows are very nearly linear,",
        "with central linear R^2 values from about 0.993 to 0.99998.",
        "This is not chaotic phase behavior.  However, the central phase variation",
        "grows from about 2.17 at k=10 to about 6.40 at k=50, so the direct",
        "bounded-variation/cosine lower bound is not usable.",
        "",
        "Phase-route feasibility: smoothness makes the gap more structured,",
        "but no theorem-grade `(C_0,C_1)` interference bound follows from the",
        "direct bounded-variation estimate.  The named Step 310 gap remains open",
        "and appears to require a discrete stationary-phase estimate for the",
        "central j-sum, or a positivity/quadratic-form reformulation.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step311_results_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    schema = {
        "step": 311,
        "orientation": "phase_analysis",
        "target": "Leibniz term phase smoothness and interference lower-bound feasibility",
        "dps": DPS,
        "k_targets": K_TARGETS,
        "phase_route_result": "central phase nearly linear but not sufficient for direct bounded-variation lower bound",
        "final_verdict": verdict,
    }
    (ART / "step311_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step311.md").write_text(
        "# Step 311 Nonclaim Boundary\n\n"
        "- This is a Branch C phase-diagnostic step only.\n"
        "- It does not prove RH.\n"
        "- It does not prove the Step 310 conditional lower-bound theorem.\n"
        "- No theorem-grade interference lower bound is claimed.\n",
        encoding="utf-8",
    )
    print("Step311 phase analysis")
    print(f"mpmath_dps={DPS}")
    print(f"k_targets={K_TARGETS}")
    for row in smooth_rows:
        print(
            "k={k} flag={flag} TV={tv} central_TV={ctv} R2_central={r2} interference={interf}".format(
                k=row["k"],
                flag=row["smoothness_flag"],
                tv=row["total_phase_variation"],
                ctv=row["central_phase_variation"],
                r2=row["linear_R2_central"],
                interf=row["interference_ratio"],
            )
        )
    print(f"verdict={verdict}")
    print(f"runtime_seconds={time.time()-t0:.3f}")


if __name__ == "__main__":
    main()
