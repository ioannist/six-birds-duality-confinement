#!/usr/bin/env python3
"""Step 377: audit signs of Re zeta'' at the first 100 zeta zeros."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step377_re_zeta_2nd_sign_uniformity_artifacts")
STEP368 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step368_branch_C_residual_structure_artifacts/residuals_and_predictors_step368.csv")
DPS = 80
N = 100


def sgn(x: mp.mpf) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def read_step368() -> dict[int, dict[str, str]]:
    if not STEP368.exists():
        return {}
    with STEP368.open(newline="") as fh:
        return {int(row["rho_index"]): row for row in csv.DictReader(fh)}


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    step368 = read_step368()

    rows: list[dict[str, str]] = []
    exceptions: list[dict[str, str]] = []
    re_vals: list[float] = []
    im_vals: list[float] = []
    abs_vals: list[float] = []
    cross_rows: list[dict[str, str]] = []

    for j in range(1, N + 1):
        rho = mp.zetazero(j)
        z2 = mp.zeta(rho, derivative=2)
        re_z2 = mp.re(z2)
        im_z2 = mp.im(z2)
        abs_z2 = abs(z2)
        sign_re = sgn(re_z2)
        T = mp.im(rho)
        row = {
            "j": str(j),
            "rho_real": mp.nstr(mp.re(rho), 50),
            "T": mp.nstr(T, 50),
            "Re_zeta_double_prime": mp.nstr(re_z2, 50),
            "Im_zeta_double_prime": mp.nstr(im_z2, 50),
            "abs_zeta_double_prime": mp.nstr(abs_z2, 50),
            "sign_Re": str(sign_re),
        }
        rows.append(row)
        re_vals.append(float(re_z2))
        im_vals.append(float(im_z2))
        abs_vals.append(float(abs_z2))
        if re_z2 >= 0:
            exceptions.append(row)
        if j in step368:
            prev_abs = float(step368[j]["abs_zeta2"])
            prev_sign = int(step368[j]["eta_sign_Re_zeta2"])
            rel_abs_diff = abs(float(abs_z2) - prev_abs) / max(abs(prev_abs), 1e-300)
            cross_rows.append(
                {
                    "j": str(j),
                    "step368_sign": str(prev_sign),
                    "step377_sign": str(sign_re),
                    "step368_abs_zeta2": f"{prev_abs:.17e}",
                    "step377_abs_zeta2": f"{float(abs_z2):.17e}",
                    "relative_abs_difference": f"{rel_abs_diff:.17e}",
                    "sign_matches": str(prev_sign == sign_re),
                }
            )
        if j % 10 == 0:
            print(f"computed {j}/{N}")

    neg_count = sum(1 for row in rows if row["sign_Re"] == "-1")
    pos_count = sum(1 for row in rows if row["sign_Re"] == "1")
    zero_count = sum(1 for row in rows if row["sign_Re"] == "0")
    mean_re = sum(re_vals) / len(re_vals)
    var_re = sum((x - mean_re) ** 2 for x in re_vals) / len(re_vals)
    std_re = math.sqrt(var_re)
    mean_im = sum(im_vals) / len(im_vals)
    mean_abs = sum(abs_vals) / len(abs_vals)
    min_re = min(re_vals)
    max_re = max(re_vals)
    max_abs_cross_rel = max((float(r["relative_abs_difference"]) for r in cross_rows), default=float("nan"))
    all_cross_sign_match = all(r["sign_matches"] == "True" for r in cross_rows)

    with (BASE / "zeta_double_prime_at_zeros_step377.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (BASE / "exceptional_zeros_step377.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(exceptions)

    with (BASE / "step368_crosscheck_step377.csv").open("w", newline="") as fh:
        if cross_rows:
            writer = csv.DictWriter(fh, fieldnames=list(cross_rows[0].keys()))
            writer.writeheader()
            writer.writerows(cross_rows)

    if neg_count == N:
        verdict = "uniform_negative_first_100"
    elif neg_count >= 95:
        verdict = "strong_not_uniform_95_percent_plus"
    elif neg_count > N / 2:
        verdict = "majority_negative_not_uniform"
    else:
        verdict = "not_uniform_low_j_artifact"
    summary = f"""# Step 377 Sign Count Summary

Computed `zeta''(rho_j)` for `j=1..{N}` using `mpmath.zetazero(j)` and `mpmath.zeta(rho_j, derivative=2)` at `dps={DPS}`.

- negative Re count: `{neg_count}/{N}`
- nonnegative Re count: `{pos_count + zero_count}/{N}` (`positive={pos_count}`, `zero={zero_count}`)
- mean Re zeta'': `{mean_re:.17e}`
- variance Re zeta'': `{var_re:.17e}`
- std Re zeta'': `{std_re:.17e}`
- min Re zeta'': `{min_re:.17e}`
- max Re zeta'': `{max_re:.17e}`
- mean Im zeta'': `{mean_im:.17e}`
- mean |zeta''|: `{mean_abs:.17e}`
- Step 368 cross-check rows: `{len(cross_rows)}`; all signs match: `{all_cross_sign_match}`; max relative |zeta''| difference: `{max_abs_cross_rel:.3e}`

Verdict: `{verdict}`.
"""
    (BASE / "sign_count_summary_step377.md").write_text(summary)

    results = f"""# Step 377 Results Summary

Step 368 observation cited verbatim: `eta_j = sgn(Re zeta''(rho_j)) = -1` for all `j=1..15`.

The Step 377 extension computed the first `{N}` zeta zeros directly with mpmath at `dps={DPS}`. Result:

- `Re zeta''(rho_j) < 0` for `{neg_count}/{N}` zeros.
- Exceptional nonnegative zeros: `{', '.join(row['j'] for row in exceptions) if exceptions else 'none'}`.
- Mean `Re zeta''(rho_j)`: `{mean_re:.17e}`.
- Variance: `{var_re:.17e}`.
- Min/Max Re values: `{min_re:.17e}` / `{max_re:.17e}`.

Cross-check against Step 368 for `j=1..15`: all signs match `{all_cross_sign_match}`; max relative difference in `|zeta''|` is `{max_abs_cross_rel:.3e}`.

Verdict: `{verdict}`. This is empirical evidence for first-100 per-zero negativity, stronger than a negative-mean statement, but it is not a theorem and does not prove RH.
"""
    (BASE / "step377_results_summary.md").write_text(results)

    schema = {
        "step": 377,
        "mode": "ATTEMPT",
        "dps": DPS,
        "n_zeros": N,
        "rho_source": "mpmath.zetazero(j)",
        "zeta_double_prime_source": "mpmath.zeta(rho_j, derivative=2)",
        "negative_count": neg_count,
        "positive_count": pos_count,
        "zero_count": zero_count,
        "mean_re_zeta_double_prime": mean_re,
        "variance_re_zeta_double_prime": var_re,
        "verdict": verdict,
        "artifacts": [
            "zeta_double_prime_at_zeros_step377.csv",
            "sign_count_summary_step377.md",
            "exceptional_zeros_step377.csv",
            "step377_results_summary.md",
            "step377_schema.json",
            "nonclaim_boundary_step377.md",
            "run_step377_checks.py",
        ],
    }
    (BASE / "step377_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

    boundary = """# Step 377 Nonclaim Boundary

- This step does not prove RH, GRH, or any zero-location theorem.
- The sign uniformity is an empirical first-100-zero audit, not a published theorem.
- The known negative-mean background is distinct from the stronger per-zero uniformity tested here.
- Numerical values use mpmath at finite precision and should be treated as audit evidence.
"""
    (BASE / "nonclaim_boundary_step377.md").write_text(boundary)

    print("STEP377_COMPUTE_DONE")
    print(f"negative_count={neg_count}/{N}")
    print(f"nonnegative={[row['j'] for row in exceptions]}")
    print(f"mean_re={mean_re:.17e}")
    print(f"crosscheck_signs={all_cross_sign_match} max_abs_rel={max_abs_cross_rel:.3e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
