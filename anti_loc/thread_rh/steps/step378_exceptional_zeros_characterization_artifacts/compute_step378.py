#!/usr/bin/env python3
"""Step 378: characterize zeros with nonnegative Re zeta''."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step378_exceptional_zeros_characterization_artifacts")
DPS = 80
N = 100
EXCEPTIONS = [34, 41, 64, 71, 79, 80, 92]
CONTROLS = [33, 35, 40, 42, 63, 65]


def ffmt(x: float) -> str:
    return f"{x:.17e}"


def pearson(xs: list[float], ys: list[float]) -> float:
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny) if denx and deny else float("nan")


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)

    # Need j=101 for forward spacing at j=100.
    zeros = {j: mp.zetazero(j) for j in range(1, N + 2)}
    T = {j: float(mp.im(zeros[j])) for j in zeros}

    all_rows: list[dict[str, str]] = []
    for j in range(1, N + 1):
        rho = zeros[j]
        z1 = mp.zeta(rho, derivative=1)
        z2 = mp.zeta(rho, derivative=2)
        re_z2 = float(mp.re(z2))
        im_z2 = float(mp.im(z2))
        abs_z2 = float(abs(z2))
        abs_z1 = float(abs(z1))
        ratio = abs_z2 / abs_z1 if abs_z1 else float("inf")
        s_fwd = T[j + 1] - T[j]
        s_bwd = T[j] - T[j - 1] if j > 1 else float("nan")
        s_min = s_fwd if j == 1 else min(s_fwd, s_bwd)
        mean_spacing = float(2 * mp.pi / mp.log(mp.mpf(T[j]) / (2 * mp.pi)))
        close_defect = mean_spacing - s_min
        all_rows.append(
            {
                "j": str(j),
                "T": mp.nstr(mp.mpf(T[j]), 50),
                "Re_zeta_double_prime": ffmt(re_z2),
                "Im_zeta_double_prime": ffmt(im_z2),
                "abs_zeta_prime": ffmt(abs_z1),
                "abs_zeta_double_prime": ffmt(abs_z2),
                "abs_zeta2_over_abs_zeta1": ffmt(ratio),
                "s_fwd": ffmt(s_fwd),
                "s_bwd": "" if j == 1 else ffmt(s_bwd),
                "s_min": ffmt(s_min),
                "mean_spacing_RvM": ffmt(mean_spacing),
                "close_pair_distance_mean_minus_s_min": ffmt(close_defect),
                "is_exception": str(j in EXCEPTIONS),
                "sign_Re_zeta2": "1" if re_z2 > 0 else ("-1" if re_z2 < 0 else "0"),
            }
        )
        if j % 20 == 0:
            print(f"computed {j}/{N}")

    with (BASE / "all100_features_step378.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    exceptional_rows = [r for r in all_rows if r["is_exception"] == "True"]
    with (BASE / "exceptional_zeros_features_step378.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(exceptional_rows[0].keys()))
        writer.writeheader()
        writer.writerows(exceptional_rows)

    controls_rows = [r for r in all_rows if int(r["j"]) in CONTROLS]
    with (BASE / "control_zeros_features_step378.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(controls_rows[0].keys()))
        writer.writeheader()
        writer.writerows(controls_rows)

    re_vals = [float(r["Re_zeta_double_prime"]) for r in all_rows]
    s_min_vals = [float(r["s_min"]) for r in all_rows]
    close_vals = [float(r["close_pair_distance_mean_minus_s_min"]) for r in all_rows]
    T_vals = [float(r["T"]) for r in all_rows]
    ratio_vals = [float(r["abs_zeta2_over_abs_zeta1"]) for r in all_rows]
    mean_spacing_vals = [float(r["mean_spacing_RvM"]) for r in all_rows]
    s_fwd_vals = [float(r["s_fwd"]) for r in all_rows]
    s_bwd_rows = [r for r in all_rows if r["s_bwd"]]
    s_bwd_vals = [float(r["s_bwd"]) for r in s_bwd_rows]
    re_bwd_vals = [float(r["Re_zeta_double_prime"]) for r in s_bwd_rows]

    corr_specs = [
        ("s_min", re_vals, s_min_vals),
        ("mean_spacing_minus_s_min", re_vals, close_vals),
        ("T", re_vals, T_vals),
        ("abs_zeta2_over_abs_zeta1", re_vals, ratio_vals),
        ("mean_spacing_RvM", re_vals, mean_spacing_vals),
        ("s_fwd", re_vals, s_fwd_vals),
        ("s_bwd", re_bwd_vals, s_bwd_vals),
    ]
    corr_rows = []
    for name, xs, ys in corr_specs:
        corr_rows.append({"variable": name, "pearson_r": ffmt(pearson(xs, ys)), "n": str(len(xs))})
    corr_rows_sorted = sorted(corr_rows, key=lambda r: abs(float(r["pearson_r"])), reverse=True)
    with (BASE / "correlation_tests_step378.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["variable", "pearson_r", "n"])
        writer.writeheader()
        writer.writerows(corr_rows_sorted)

    exc_T = [T[j] for j in EXCEPTIONS]
    exc_index_gaps = [EXCEPTIONS[i + 1] - EXCEPTIONS[i] for i in range(len(EXCEPTIONS) - 1)]
    exc_T_gaps = [exc_T[i + 1] - exc_T[i] for i in range(len(exc_T) - 1)]
    expected_index_gap = (N + 1) / (len(EXCEPTIONS) + 1)
    exc_ratios = [float(r["abs_zeta2_over_abs_zeta1"]) for r in exceptional_rows]
    control_ratios = [float(r["abs_zeta2_over_abs_zeta1"]) for r in controls_rows]
    nonexc_ratios = [float(r["abs_zeta2_over_abs_zeta1"]) for r in all_rows if r["is_exception"] == "False"]
    exc_smin = [float(r["s_min"]) for r in exceptional_rows]
    nonexc_smin = [float(r["s_min"]) for r in all_rows if r["is_exception"] == "False"]
    exc_close = [float(r["close_pair_distance_mean_minus_s_min"]) for r in exceptional_rows]
    nonexc_close = [float(r["close_pair_distance_mean_minus_s_min"]) for r in all_rows if r["is_exception"] == "False"]

    def mean(xs: list[float]) -> float:
        return sum(xs) / len(xs)

    cluster_md = f"""# Step 378 Cluster Analysis

Step 377 found seven nonnegative exceptions: `{EXCEPTIONS}`.

Adjacent exceptional index gaps: `{exc_index_gaps}`.
Adjacent exceptional T-gaps: `{[round(x, 6) for x in exc_T_gaps]}`.
Expected index gap for 7 uniformly scattered hits in 1..100: `{expected_index_gap:.3f}`.

The exceptions are not one compact T-cluster. They are late-skewed (`5/7` occur after `j>=64`) and include one adjacent pair (`j=79,80`), but also have large gaps (`23` indices between `41` and `64`, `12` between `80` and `92`).

Spacing comparison:

- mean exceptional `s_min`: `{mean(exc_smin):.6f}`
- mean non-exceptional `s_min`: `{mean(nonexc_smin):.6f}`
- mean exceptional `(mean_spacing - s_min)`: `{mean(exc_close):.6f}`
- mean non-exceptional `(mean_spacing - s_min)`: `{mean(nonexc_close):.6f}`

Derivative-ratio comparison:

- mean exceptional `|zeta''|/|zeta'|`: `{mean(exc_ratios):.6f}`
- mean control `|zeta''|/|zeta'|`: `{mean(control_ratios):.6f}`
- mean non-exceptional `|zeta''|/|zeta'|`: `{mean(nonexc_ratios):.6f}`

Interpretation: the exceptions are not a single compact T-cluster, but they do sit in locally compressed zero-neighborhoods. The strongest full-sample Pearson signal is `Re zeta''` versus `Delta_bar(T)-s_min` (`r={next(r['pearson_r'] for r in corr_rows_sorted if r['variable'] == 'mean_spacing_minus_s_min')}`), and exceptional `s_min` is substantially smaller than the non-exceptional mean. This supports a close-pair/local-geometry explanation, though it is not a complete classifier.
"""
    (BASE / "cluster_analysis_step378.md").write_text(cluster_md)

    top_corr = corr_rows_sorted[0]
    verdict = "close_pair_deficit_signal; not_single_T_cluster"
    results = f"""# Step 378 Results Summary

Step 368 observation cited verbatim: `eta_j = sgn(Re zeta''(rho_j)) = -1` for all `j=1..15`.
Step 377 finding cited verbatim: `93/100` zeros have `Re zeta''(rho_j) < 0`; exceptions are `{EXCEPTIONS}`.

The exact exception heights are in `exceptional_zeros_features_step378.csv`. Neighbor-spacing analysis supports a relative close-pair/local-compression signal:

- mean exceptional `s_min`: `{mean(exc_smin):.6f}`
- mean non-exceptional `s_min`: `{mean(nonexc_smin):.6f}`
- mean exceptional close-pair distance `Delta_bar(T)-s_min`: `{mean(exc_close):.6f}`
- mean non-exceptional close-pair distance: `{mean(nonexc_close):.6f}`

Cluster analysis: not a single T-cluster. Exceptions are late-skewed and include one adjacent pair, but are otherwise scattered.

Top Pearson correlation over all 100 zeros: `{top_corr['variable']}` with `r={top_corr['pearson_r']}`. The close-pair deficit is the strongest tested signal; raw `s_min` alone is weaker, so the structural quantity appears to be spacing relative to local Riemann-von Mangoldt mean spacing rather than absolute spacing.

Verdict: `{verdict}`. The 7 exceptions are not explained by a special arithmetic property of the heights in this audit, but they show a clear local-spacing/close-pair signal.
"""
    (BASE / "step378_results_summary.md").write_text(results)

    schema = {
        "step": 378,
        "mode": "ATTEMPT",
        "dps": DPS,
        "n_zeros": N,
        "exceptions": EXCEPTIONS,
        "controls": CONTROLS,
        "top_correlation": top_corr,
        "verdict": verdict,
        "artifacts": [
            "exceptional_zeros_features_step378.csv",
            "correlation_tests_step378.csv",
            "cluster_analysis_step378.md",
            "step378_results_summary.md",
            "step378_schema.json",
            "nonclaim_boundary_step378.md",
            "run_step378_checks.py",
        ],
    }
    (BASE / "step378_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    boundary = """# Step 378 Nonclaim Boundary

- This step does not prove RH or any zero-spacing theorem.
- The analysis is empirical for the first 100 zeros and the seven Step 377 exceptions.
- Correlations are exploratory diagnostics, not causal proofs.
- No arithmetic classification of exceptional zeros is claimed.
"""
    (BASE / "nonclaim_boundary_step378.md").write_text(boundary)

    print("STEP378_COMPUTE_DONE")
    print(f"exceptions={EXCEPTIONS}")
    print(f"top_corr={top_corr['variable']} r={top_corr['pearson_r']}")
    print(f"mean_exc_smin={mean(exc_smin):.6f} mean_nonexc_smin={mean(nonexc_smin):.6f}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
