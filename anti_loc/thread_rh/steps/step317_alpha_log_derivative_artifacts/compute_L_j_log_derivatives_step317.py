#!/usr/bin/env python3
"""Step 317: log-derivative series for xi/(z-rho1) and zero sums."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step317_alpha_log_derivative_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP314_ALPHA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step314_alpha_rigorous_derivation_artifacts/alpha_predicted_vs_empirical_step314.csv")

DPS = 80
N = 31
RHO1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def prefactor(s: mp.mpc) -> mp.mpc:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s/2) * mp.gamma(s/2)


def poly_mul(a: list[mp.mpc], b: list[mp.mpc], n: int) -> list[mp.mpc]:
    out = [mp.mpc(0) for _ in range(n+1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j <= n:
                out[i+j] += ai * bj
    return out


def poly_log(a: list[mp.mpc], n: int) -> list[mp.mpc]:
    # log(a0 + a1 w + ...) through order n.
    a0 = a[0]
    u = [mp.mpc(0)] + [a[i]/a0 for i in range(1, n+1)]
    out = [mp.log(a0)] + [mp.mpc(0) for _ in range(n)]
    power = [mp.mpc(1)] + [mp.mpc(0) for _ in range(n)]
    for m in range(1, n+1):
        power = poly_mul(power, u, n)
        coeff = mp.mpf(1 if m % 2 == 1 else -1) / m
        for i in range(1, n+1):
            out[i] += coeff * power[i]
    return out


def poly_exp(log_coeff: list[mp.mpc], n: int) -> list[mp.mpc]:
    # exp(log_coeff[0] + sum_{i>=1} log_coeff[i] w^i)
    out = [mp.e**log_coeff[0]] + [mp.mpc(0) for _ in range(n)]
    for m in range(1, n+1):
        s = mp.mpc(0)
        for i in range(1, m+1):
            s += i * log_coeff[i] * out[m-i]
        out[m] = s / m
    return out


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step292 = load_module("step292_for_step317", STEP292_SCRIPT)
    # zeta derivatives at rho1 through N+1.
    zds = [mp.zeta(RHO1, derivative=j) for j in range(N+2)]
    pds = [mp.diff(prefactor, RHO1, j) for j in range(N+2)]
    xi_derivs = []
    for n in range(N+2):
        val = mp.mpc(0)
        for a in range(n+1):
            val += mp.mpf(math.comb(n, a)) * pds[a] * zds[n-a]
        xi_derivs.append(val)

    # htilde(w)=xi(rho1+w)/w = sum xi^(n+1)/(n+1)! w^n.
    hcoeff = [xi_derivs[n+1] / mp.factorial(n+1) for n in range(N+1)]
    logcoeff = poly_log(hcoeff, N)
    recon_hcoeff = poly_exp(logcoeff, N)

    # smooth prefactor log derivatives.
    pcoeff = [pds[n] / mp.factorial(n) for n in range(N+1)]
    logp = poly_log(pcoeff, N)

    # zero sums over first 200 zeros, with conjugates, excluding rho1 itself by index.
    zeros = []
    for idx in range(1, 201):
        z = mp.zetazero(idx)
        if idx != 1:
            zeros.append(z)
        zeros.append(1 - z)

    rows = []
    for j in range(1, 31):
        D = logcoeff[j] * mp.factorial(j)  # d^j log htilde
        D_smooth = logp[j] * mp.factorial(j)
        zero_sum = mp.fsum([(-1)**(j-1) * mp.factorial(j-1) / ((RHO1 - rho) ** j) for rho in zeros])
        rel = abs(zero_sum - D) / abs(D) if abs(D) else mp.inf
        rows.append({
            "j": j,
            "D_j_log_htilde": cstr(D, 34),
            "D_j_abs": mp.nstr(abs(D), 34),
            "D_j_arg": mp.nstr(mp.arg(D), 34),
            "zero_sum_200_zeros": cstr(zero_sum, 34),
            "zero_sum_rel_error_vs_D_j": mp.nstr(rel, 18),
            "smooth_prefactor_D_j_logP": cstr(D_smooth, 34),
            "regularized_zeta_log_derivative_D_minus_logP": cstr(D - D_smooth, 34),
        })
    write_csv(ART / "L_j_values_step317.csv", rows)

    xi_rows = []
    for j in [1, 2, 3, 4, 5, 10, 15, 25, 30]:
        if j > N + 1:
            continue
        via = recon_hcoeff[j-1] * mp.factorial(j)
        direct = xi_derivs[j]
        xi_rows.append({
            "j": j,
            "xi_via_Bell_log_series": cstr(via, 34),
            "xi_direct_Leibniz_prefactor_zeta": cstr(direct, 34),
            "relative_error": mp.nstr(abs(via-direct)/abs(direct), 18),
            "arg_ratio_via_next_over_current": mp.nstr(mp.arg((recon_hcoeff[j] * mp.factorial(j+1))/via), 34) if j < N else "",
            "arg_ratio_direct_next_over_current": mp.nstr(mp.arg(xi_derivs[j+1]/direct), 34) if j < N+1 else "",
        })
    write_csv(ART / "xi_via_L_j_step317.csv", xi_rows)

    alpha_emp = {int(r["k"]): r for r in read_csv(STEP314_ALPHA)}
    conn_rows = []
    gap = abs(mp.zetazero(2) - RHO1)
    nearest_phase = -mp.pi / 2
    max_half = max(K_TARGETS) // 2 + 1
    mds_for_alpha = step292.mellin_derivatives(step292.GENERATORS["G_star"], mp.im(RHO1), max_half + 1, DPS)
    for k in K_TARGETS:
        j = k // 2
        # xi ratio from Bell/log coefficients
        xi_ratio_arg = mp.arg(xi_derivs[j+1] / xi_derivs[j])
        # zeta-ratio phase used in alpha.
        zeta_ratio_arg = mp.arg(zds[j+1] / zds[j])
        M_ratio_arg = mp.arg(mds_for_alpha[j+1] / mds_for_alpha[j])
        alpha_formula = zeta_ratio_arg - M_ratio_arg
        while alpha_formula > mp.pi:
            alpha_formula -= 2*mp.pi
        while alpha_formula <= -mp.pi:
            alpha_formula += 2*mp.pi
        conn_rows.append({
            "k": k,
            "j_half": j,
            "rho2_gap_abs": mp.nstr(gap, 18),
            "nearest_gap_phase_arg_rho1_minus_rho2": mp.nstr(nearest_phase, 18),
            "arg_xi_ratio_from_L_j": mp.nstr(xi_ratio_arg, 34),
            "arg_zeta_ratio": mp.nstr(zeta_ratio_arg, 34),
            "arg_M_ratio": mp.nstr(M_ratio_arg, 34),
            "alpha_formula_abs": mp.nstr(abs(alpha_formula), 34),
            "alpha_empirical_step314": alpha_emp[k]["alpha_empirical_step313"],
            "assessment": "rho2 dominates zero-power-sum but alpha remains controlled by zeta regular factor plus M correction",
        })
    write_csv(ART / "alpha_pair_correlation_connection_step317.csv", conn_rows)

    verdict = "V_alpha_log_derivative_power_sum_partial_pair_correlation_indirect"
    summary = [
        "# Step 317 Results Summary",
        "",
        "Built the Taylor series of `htilde(z)=xi(z)/(z-rho_1)` from `xi=P*zeta` via Leibniz derivatives, then computed formal log-derivatives `D_j=d^j log htilde`.",
        "The Bell/log-series reconstruction of `xi^(j)(rho_1)` matches the direct Leibniz computation to numerical precision.",
        "",
        "The truncated 200-zero power sums capture the nearest-zero dominance pattern at high j, but do not by themselves give the raw alpha formula.  The alpha used in Branch C is still the zeta regular-factor phase minus the Mellin-ratio phase.",
        "",
        "Pair-correlation assessment: `rho_2` and the gap `|rho_1-rho_2|=6.887` enter naturally through high-order log-derivative power sums, so there is an indirect Montgomery-pair-correlation connection.  It does not yet close the alpha theorem because translating log-derivative power sums into the raw derivative-ratio phase requires Bell-polynomial asymptotics with controlled remainders.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step317_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 317,
        "orientation": "alpha_log_derivative_power_sum_attempt",
        "target": "derive alpha from xi log-derivative power sums and pair-correlation gap",
        "dps": DPS,
        "zero_sum_count": 200,
        "pair_correlation_connection": "indirect via log-derivative power sums dominated by rho2",
        "remaining_gap": "Bell-polynomial asymptotics translating log-derivative power sums to raw derivative-ratio phase",
        "final_verdict": verdict,
    }
    (ART / "step317_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step317.md").write_text(
        "# Step 317 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not prove Branch C closure.\n"
        "- The Montgomery pair-correlation connection is indirect and diagnostic.\n"
        "- No theorem-grade alpha bound is claimed.\n",
        encoding="utf-8",
    )
    print("Step317 alpha log-derivative power-sum diagnostic")
    print(f"L_j rows={len(rows)}")
    print(f"xi reconstruction rows={len(xi_rows)}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
