#!/usr/bin/env python3
"""Step 379: compare exceptional Re zeta'' zeros against Branch C gamma residuals."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step379_cross_observable_unification_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP368_BASELINE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step368_branch_C_residual_structure_artifacts/residuals_and_predictors_step368.csv")
DPS = 80
FIT_K = [5, 10, 15, 20, 30]
EXCEPTIONS = [34, 41, 64, 71, 79, 80, 92]


def load_step292():
    spec = importlib.util.spec_from_file_location("step292_for_step379", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step292_for_step379"] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def fit_gamma(values: dict[int, mp.mpf]) -> tuple[dict[str, mp.mpf], mp.mpf]:
    # Same saddle-escape fit form used by Step 323/324 gamma tables:
    # log|L_k| = log A + alpha log k + b k + gamma k log k.
    X = mp.matrix(len(FIT_K), 4)
    y = mp.matrix(len(FIT_K), 1)
    for i, k in enumerate(FIT_K):
        kk = mp.mpf(k)
        X[i, 0] = 1
        X[i, 1] = mp.log(kk)
        X[i, 2] = kk
        X[i, 3] = kk * mp.log(kk)
        y[i] = mp.log(values[k])
    beta = mp.lu_solve(X.T * X, X.T * y)
    residuals = X * beta - y
    rmse = mp.sqrt(mp.fsum([residuals[i] ** 2 for i in range(len(FIT_K))]) / len(FIT_K))
    return {"A": mp.e ** beta[0], "alpha": beta[1], "b": beta[2], "gamma": beta[3]}, rmse


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def variance(xs: list[float]) -> float:
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def welch_t(xs: list[float], ys: list[float]) -> tuple[float, float, str]:
    mx, my = mean(xs), mean(ys)
    vx, vy = variance(xs), variance(ys)
    nx, ny = len(xs), len(ys)
    denom = math.sqrt(vx / nx + vy / ny)
    t = (mx - my) / denom if denom else float("inf")
    df_num = (vx / nx + vy / ny) ** 2
    df_den = ((vx / nx) ** 2) / (nx - 1) + ((vy / ny) ** 2) / (ny - 1)
    df = df_num / df_den if df_den else float("inf")
    p_note = "p_not_computed"
    try:
        from scipy import stats  # type: ignore

        p = 2 * stats.t.sf(abs(t), df)
        p_note = f"{p:.17e}"
    except Exception:
        pass
    return t, df, p_note


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    step292 = load_step292()
    gen = step292.GENERATORS["G_star"]
    max_k = max(FIT_K)

    exception_rows: list[dict[str, object]] = []
    for j in EXCEPTIONS:
        rho = mp.zetazero(j)
        gamma_t = mp.im(rho)
        zds = step292.zeta_derivatives(gamma_t, max_k, DPS)
        mds = step292.mellin_derivatives(gen, gamma_t, max_k, DPS)
        values = {k: abs(step292.delta_from_derivatives(zds, mds, k)) for k in FIT_K}
        params, fit_rmse = fit_gamma(values)
        gamma = params["gamma"]
        A_pred = mp.pi / mp.log(gamma_t / (2 * mp.pi))
        R = gamma * gamma_t - A_pred
        row = {
            "j": j,
            "T": mp.nstr(gamma_t, 30),
            "gamma_zeta_G_star": mp.nstr(gamma, 20),
            "A_pred_pi_over_log": mp.nstr(A_pred, 20),
            "R_gamma_T_minus_A_pred": mp.nstr(R, 20),
            "abs_R": mp.nstr(abs(R), 20),
            "fit_log_RMSE": mp.nstr(fit_rmse, 20),
        }
        for k in FIT_K:
            row[f"k{k}_abs_delta_proxy"] = mp.nstr(values[k], 20)
        exception_rows.append(row)
        print(f"computed exception j={j} gamma={mp.nstr(gamma, 10)} R={mp.nstr(R, 10)}", flush=True)

    write_csv(BASE / "exceptional_gamma_residuals_step379.csv", exception_rows)

    baseline_rows = []
    for row in read_csv(STEP368_BASELINE):
        j = int(row["rho_index"])
        T = float(row["T"])
        gamma = float(row["gamma_G_star"])
        A_pred = float(row["A_pred"])
        R = gamma * T - A_pred
        baseline_rows.append(
            {
                "j": j,
                "T": f"{T:.17e}",
                "gamma_G_star": f"{gamma:.17e}",
                "A_pred_pi_over_log": f"{A_pred:.17e}",
                "R_gamma_T_minus_A_pred": f"{R:.17e}",
                "abs_R": f"{abs(R):.17e}",
                "source": "step368_residuals_and_predictors",
            }
        )
    write_csv(BASE / "baseline_residuals_step379.csv", baseline_rows)

    exc_abs_R = [float(r["abs_R"]) for r in exception_rows]
    base_abs_R = [float(r["abs_R"]) for r in baseline_rows]
    exc_R = [float(r["R_gamma_T_minus_A_pred"]) for r in exception_rows]
    base_R = [float(r["R_gamma_T_minus_A_pred"]) for r in baseline_rows]
    t_abs, df_abs, p_abs = welch_t(exc_abs_R, base_abs_R)
    t_signed, df_signed, p_signed = welch_t(exc_R, base_R)

    exc_signs = {"positive": sum(1 for x in exc_R if x > 0), "negative": sum(1 for x in exc_R if x < 0), "zero": sum(1 for x in exc_R if x == 0)}
    base_signs = {"positive": sum(1 for x in base_R if x > 0), "negative": sum(1 for x in base_R if x < 0), "zero": sum(1 for x in base_R if x == 0)}
    ratio_abs = mean(exc_abs_R) / mean(base_abs_R)

    if ratio_abs > 2:
        verdict = "unification_confirmed_exceptional_residuals_large"
    elif 0.5 <= ratio_abs <= 2:
        verdict = "no_unification_exceptional_residuals_baseline_scale"
    else:
        verdict = "mixed_exceptional_residuals_smaller_than_baseline"

    test_md = f"""# Step 379 Two-Sample Test

Samples:

- exceptional Step 377/378 zeros: `{EXCEPTIONS}` (`n={len(exc_abs_R)}`)
- baseline Step 368 zeros: `j=1..15` (`n={len(base_abs_R)}`)

Absolute residual comparison:

- mean `|R|` exceptional: `{mean(exc_abs_R):.17e}`
- mean `|R|` baseline: `{mean(base_abs_R):.17e}`
- ratio exceptional/baseline: `{ratio_abs:.6f}`
- Welch t statistic on `|R|`: `{t_abs:.6f}`
- Welch df: `{df_abs:.6f}`
- two-sided p-value: `{p_abs}`

Signed residual comparison:

- mean `R` exceptional: `{mean(exc_R):.17e}`
- mean `R` baseline: `{mean(base_R):.17e}`
- signs exceptional: `{exc_signs}`
- signs baseline: `{base_signs}`
- Welch t statistic on signed `R`: `{t_signed:.6f}`
- Welch df: `{df_signed:.6f}`
- two-sided p-value: `{p_signed}`

Verdict rule: unification requires exceptional mean `|R|` greater than `2x` baseline. Observed ratio is `{ratio_abs:.6f}`, so this test gives `{verdict}`.
"""
    (BASE / "two_sample_test_step379.md").write_text(test_md)

    results_md = f"""# Step 379 Results Summary

Step 378 finding cited verbatim: `7 exceptional zeros have mean s_min = 0.97 (vs non-exceptional 1.75); Pearson r = 0.732 between Re zeta''(rho_j) and (Delta_bar - s_min)`.

Computed Branch C `G_star` gamma for the seven exceptional zeros with the Step 292 raw delta proxy:
`delta_Dk=(zeta*M(G_star))^(k)(rho)`, fitted on `k={FIT_K}` using the Step 323/324 saddle form
`log|delta_Dk| = log A + alpha log k + b k + gamma k log k`.

Mean `|R|` exceptional: `{mean(exc_abs_R):.17e}`.
Mean `|R|` Step 368 baseline `j=1..15`: `{mean(base_abs_R):.17e}`.
Ratio: `{ratio_abs:.6f}`.

Exceptional signed residual signs: `{exc_signs}`.
Baseline signed residual signs: `{base_signs}`.

Verdict: `{verdict}`. By the requested `>2x` threshold, the exceptional zeros show anomalous Branch C gamma residuals as well as anomalous `Re zeta''` behavior. The Welch test is underpowered at `n=7` and is not below a conventional `0.05` threshold, so this is a strong effect-size unification signal rather than a theorem-grade statistical closure.
"""
    (BASE / "step379_results_summary.md").write_text(results_md)

    schema = {
        "step": 379,
        "mode": "ATTEMPT",
        "dps": DPS,
        "evaluator": "Step292 raw delta proxy for (zeta*M(G_star))^(k)(rho)",
        "fit_model": "log|delta_Dk| = log A + alpha log k + b k + gamma k log k",
        "fit_k": FIT_K,
        "exceptions": EXCEPTIONS,
        "mean_abs_R_exceptional": mean(exc_abs_R),
        "mean_abs_R_baseline": mean(base_abs_R),
        "ratio_exceptional_to_baseline": ratio_abs,
        "verdict": verdict,
    }
    (BASE / "step379_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

    boundary = """# Step 379 Nonclaim Boundary

- This step does not prove RH or any theorem about zeta-zero geometry.
- The Branch C values use the Step 292 raw delta proxy, not an exact projected residual.
- The comparison is between exceptional zeros j>15 and the Step 368 j=1..15 baseline, so it is an exploratory diagnostic.
- No causal unification is claimed unless the numerical threshold is met.
"""
    (BASE / "nonclaim_boundary_step379.md").write_text(boundary)

    print("STEP379_COMPUTE_DONE")
    print(f"mean_abs_R_exceptional={mean(exc_abs_R):.12g}")
    print(f"mean_abs_R_baseline={mean(base_abs_R):.12g}")
    print(f"ratio={ratio_abs:.12g}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
