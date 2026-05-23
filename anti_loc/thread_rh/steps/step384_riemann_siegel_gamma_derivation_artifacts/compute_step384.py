#!/usr/bin/env python3
"""Step 384: Riemann-Siegel derivation attempt for Branch C gamma."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step384_riemann_siegel_gamma_derivation_artifacts")
STEP324 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step324_gamma_vs_zero_spacing_artifacts/gamma_vs_d_k_step324.csv")
DPS = 80


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rmse(vals: list[float]) -> float:
    return math.sqrt(sum(v * v for v in vals) / len(vals))


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)
    data = read_csv(STEP324)
    rows = []
    rs_resids = []
    struct_resids = []
    for row in data:
        j = int(row["k"])
        T = mp.mpf(row["Im_rho_k"])
        gamma_emp = mp.mpf(row["gamma_k"])
        log_scale = mp.log(T / (2 * mp.pi))
        gamma_struct = mp.pi / (T * log_scale)
        # Direct Cauchy/Riemann-Siegel saddle heuristic:
        # r* ~ k/log(T/(2pi)) gives linear coefficient 1 - log(log(T/(2pi))).
        gamma_rs = 1 - mp.log(log_scale)
        rs_resid = gamma_rs - gamma_emp
        struct_resid = gamma_struct - gamma_emp
        rows.append(
            {
                "j": j,
                "T": mp.nstr(T, 30),
                "gamma_emp_step324": mp.nstr(gamma_emp, 30),
                "gamma_struct_pi_over_Tlog": mp.nstr(gamma_struct, 30),
                "gamma_RS_direct": mp.nstr(gamma_rs, 30),
                "RS_minus_emp": mp.nstr(rs_resid, 30),
                "struct_minus_emp": mp.nstr(struct_resid, 30),
                "abs_RS_minus_emp": mp.nstr(abs(rs_resid), 30),
                "abs_struct_minus_emp": mp.nstr(abs(struct_resid), 30),
            }
        )
        rs_resids.append(float(rs_resid))
        struct_resids.append(float(struct_resid))
    write_csv(BASE / "derived_gamma_vs_empirical_step384.csv", rows)

    rs_rmse = rmse(rs_resids)
    struct_rmse = rmse(struct_resids)
    verdict = "different_formula_projection_missing"

    derivation = f"""# Step 384 Riemann-Siegel Derivation Attempt

Standard Riemann-Siegel setup (Titchmarsh, *Theory of the Riemann Zeta-function*, Ch. IV; Edwards, *Riemann's Zeta Function*, Ch. 7):

`zeta(1/2+it) = exp(-i theta(t)) Z(t)`,

where

`theta(t) = arg Gamma(1/4+it/2) - (t/2)log pi`

and

`theta(t) = (t/2)log(t/(2pi)) - t/2 - pi/8 + O(1/t)`.

The Riemann-Siegel main sum is

`Z(t) = 2 sum_(n<=sqrt(t/(2pi))) n^(-1/2) cos(theta(t)-t log n) + error`.

For a direct Cauchy estimate of zeta derivatives at `rho=1/2+iT`,

`zeta^(k)(rho) = k!/(2pi i) int zeta(s)/(s-rho)^(k+1) ds`.

Using the Riemann-Siegel phase scale `log(T/(2pi))`, the natural direct saddle has

`r_* ~ k/log(T/(2pi))`.

Then

`log|zeta^(k)(rho)| ~ log(k!) - k log r_* + O(k)`

which gives the linear coefficient

`gamma_RS(T) = 1 - log(log(T/(2pi)))`

under the sign convention used here.

This is not the Branch C empirical law

`gamma_BC(T) = pi/(T log(T/(2pi)))`.

The mismatch means Riemann-Siegel alone sees the unprojected zeta derivative scale. The missing ingredient is the Burnol/Sonine projector `P_infty` (or equivalently the projected kernel asymptotic from Steps 153/172/372), which suppresses the direct Riemann-Siegel saddle and introduces the cusp/zero-density scale `1/(T log T)`.

Numerical comparison over Step 324's 15-zero dataset:

- RMSE direct Riemann-Siegel formula: `{rs_rmse:.6g}`
- RMSE `pi/(T log(T/(2pi)))`: `{struct_rmse:.6g}`

Verdict: `{verdict}`.
"""
    (BASE / "riemann_siegel_derivation_step384.md").write_text(derivation)

    summary = f"""# Step 384 Results Summary

Riemann-Siegel asymptotic used:

`theta(t) = (t/2)log(t/(2pi)) - t/2 - pi/8 + O(1/t)`,

with `zeta(1/2+it)=exp(-i theta(t))Z(t)`.

Direct Cauchy/Riemann-Siegel saddle:

`r_* ~ k/log(T/(2pi))`.

Derived formula:

`gamma_RS(T) = 1 - log(log(T/(2pi)))`.

Comparison to Branch C:

- Branch C law: `pi/(T log(T/(2pi)))`
- Step 324 empirical RMSE for direct RS formula: `{rs_rmse:.6g}`
- Step 324 empirical RMSE for Branch C structural law: `{struct_rmse:.6g}`

Verdict: `{verdict}`. Riemann-Siegel alone gives a different unprojected derivative scale; the missing piece is the Burnol/Sonine `P_infty` projection or projected kernel asymptotic.
"""
    (BASE / "step384_results_summary.md").write_text(summary)

    schema = {
        "step": 384,
        "mode": "ATTEMPT",
        "dps": DPS,
        "derived_gamma_formula": "gamma_RS(T)=1-log(log(T/(2*pi)))",
        "branch_C_formula": "pi/(T*log(T/(2*pi)))",
        "n_rows": len(rows),
        "rmse_RS_direct": rs_rmse,
        "rmse_branch_C_structural": struct_rmse,
        "verdict": verdict,
    }
    (BASE / "step384_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

    boundary = """# Step 384 Nonclaim Boundary

- This step does not prove RH or Branch C closure.
- The Riemann-Siegel derivation is a direct unprojected zeta-derivative saddle, not the full Burnol/Sonine projected matrix element.
- The mismatch is treated as a named missing structure: the `P_infty` projected kernel asymptotic.
- Standard references are cited for Riemann-Siegel formulas, but no external theorem is claimed for the cascade projector.
"""
    (BASE / "nonclaim_boundary_step384.md").write_text(boundary)

    print("STEP384_COMPUTE_DONE")
    print(f"gamma_RS=1-log(log(T/(2*pi)))")
    print(f"rmse_RS={rs_rmse:.12g} rmse_struct={struct_rmse:.12g}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
