#!/usr/bin/env python3
"""Step 389: Dirichlet L close-pair universality test for chi_3."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step389_dirichlet_close_pair_universality_artifacts")
DPS_SCAN = 32
DPS_ROOT = 45
DPS_DERIV = 50
Q = 3
CHAR_LABEL = "chi_3"
TARGET_N = 50
MIN_N = 25
SCAN_STEP = mp.mpf("0.08")
T_START = mp.mpf("0.50")
T_MAX_INIT = mp.mpf("180.0")


def L_chi3(s: mp.mpc) -> mp.mpc:
    return (mp.mpf(3) ** (-s)) * (mp.zeta(s, mp.mpf(1) / 3) - mp.zeta(s, mp.mpf(2) / 3))


def L_chi3_derivatives(s: mp.mpc, max_n: int = 2) -> list[mp.mpc]:
    logq = mp.log(3)
    qfac = mp.mpf(3) ** (-s)
    zeta_sums = [
        mp.zeta(s, mp.mpf(1) / 3, derivative=m) - mp.zeta(s, mp.mpf(2) / 3, derivative=m)
        for m in range(max_n + 1)
    ]
    out: list[mp.mpc] = []
    for n in range(max_n + 1):
        total = mp.mpc(0)
        for m in range(n + 1):
            total += mp.binomial(n, m) * ((-logq) ** (n - m)) * zeta_sums[m]
        out.append(qfac * total)
    return out


def locate_zeros() -> tuple[list[mp.mpc], str]:
    roots: list[mp.mpc] = []
    t_max = T_MAX_INIT
    note = ""
    while len(roots) < TARGET_N and t_max <= 320:
        mp.mp.dps = DPS_SCAN
        samples: list[tuple[mp.mpf, mp.mpf]] = []
        t = T_START
        while t <= t_max:
            try:
                val = abs(L_chi3(mp.mpc(mp.mpf("0.5"), t)))
            except Exception:
                val = mp.inf
            samples.append((t, val))
            t += SCAN_STEP

        minima: list[mp.mpf] = []
        for i in range(1, len(samples) - 1):
            if samples[i][1] < samples[i - 1][1] and samples[i][1] < samples[i + 1][1]:
                minima.append(samples[i][0])

        mp.mp.dps = DPS_ROOT
        roots = []

        def f(x: mp.mpf, y: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
            z = L_chi3(mp.mpc(x, y))
            return mp.re(z), mp.im(z)

        for guess in minima:
            try:
                x, y = mp.findroot(
                    f,
                    (mp.mpf("0.5"), guess),
                    tol=mp.mpf("1e-28"),
                    maxsteps=50,
                    solver="mnewton",
                )
                z = mp.mpc(x, y)
                if mp.im(z) <= 0 or abs(mp.re(z) - mp.mpf("0.5")) > mp.mpf("1e-20"):
                    continue
                if all(abs(z - old) > mp.mpf("1e-8") for old in roots):
                    roots.append(z)
            except Exception:
                continue
        roots.sort(key=lambda z: mp.im(z))
        if len(roots) < TARGET_N:
            note = f"only {len(roots)} roots found up to T={t_max}; increasing scan range"
            t_max += 60
        else:
            note = f"found {len(roots)} roots up to T={t_max}"
            break
    if len(roots) < MIN_N:
        raise RuntimeError(f"root search found only {len(roots)} roots; below minimum {MIN_N}")
    return roots[: min(TARGET_N, len(roots))], note


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2 or float(np.std(x)) == 0 or float(np.std(y)) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    roots, search_note = locate_zeros()
    n = len(roots)

    mp.mp.dps = DPS_DERIV
    rows: list[dict[str, object]] = []
    re2_vals: list[float] = []
    close_predictors: list[float] = []
    smins: list[float] = []
    signs: list[int] = []
    exceptions: list[int] = []
    for idx, rho in enumerate(roots, start=1):
        T = mp.im(rho)
        derivs = L_chi3_derivatives(rho, 2)
        Lp, L2 = derivs[1], derivs[2]
        s_bwd = T - mp.im(roots[idx - 2]) if idx > 1 else mp.nan
        s_fwd = mp.im(roots[idx]) - T if idx < n else mp.nan
        finite_spacings = [s for s in [s_bwd, s_fwd] if not mp.isnan(s)]
        s_min = min(finite_spacings) if finite_spacings else mp.nan
        mean_spacing = 2 * mp.pi / mp.log(Q * T / (2 * mp.pi))
        close_pred = mean_spacing - s_min if not mp.isnan(s_min) else mp.nan
        sign = -1 if mp.re(L2) < 0 else 1
        if sign >= 0:
            exceptions.append(idx)
        ratio = abs(L2 / Lp) if abs(Lp) != 0 else mp.nan
        rows.append({
            "j": idx,
            "character": CHAR_LABEL,
            "q": Q,
            "rho": f"{mp.nstr(mp.re(rho), 30)}+{mp.nstr(mp.im(rho), 30)}j",
            "T": mp.nstr(T, 30),
            "Re_L_double_prime": mp.nstr(mp.re(L2), 30),
            "Im_L_double_prime": mp.nstr(mp.im(L2), 30),
            "abs_L_double_prime": mp.nstr(abs(L2), 30),
            "abs_L_double_prime_over_L_prime": mp.nstr(ratio, 30),
            "s_bwd": "" if mp.isnan(s_bwd) else mp.nstr(s_bwd, 30),
            "s_fwd": "" if mp.isnan(s_fwd) else mp.nstr(s_fwd, 30),
            "s_min": "" if mp.isnan(s_min) else mp.nstr(s_min, 30),
            "mean_spacing_2pi_over_log_qT": mp.nstr(mean_spacing, 30),
            "close_pair_predictor_mean_minus_smin": "" if mp.isnan(close_pred) else mp.nstr(close_pred, 30),
            "sign_Re_L_double_prime": sign,
        })
        if not mp.isnan(close_pred):
            re2_vals.append(float(mp.re(L2)))
            close_predictors.append(float(close_pred))
            smins.append(float(s_min))
            signs.append(sign)

    re2 = np.array(re2_vals, dtype=float)
    close = np.array(close_predictors, dtype=float)
    smins_np = np.array(smins, dtype=float)
    sign_np = np.array(signs, dtype=int)
    neg_count = sum(1 for r in rows if int(r["sign_Re_L_double_prime"]) < 0)
    pos_count = n - neg_count
    exc_smins = [float(rows[j - 1]["s_min"]) for j in exceptions if rows[j - 1]["s_min"] != ""]
    non_smins = [float(row["s_min"]) for row in rows if int(row["sign_Re_L_double_prime"]) < 0 and row["s_min"] != ""]

    corr_rows = [
        {
            "character": CHAR_LABEL,
            "q": Q,
            "N_zeros": n,
            "negative_Re_Lpp_count": neg_count,
            "nonnegative_Re_Lpp_count": pos_count,
            "negative_fraction": f"{neg_count / n:.17e}",
            "mean_Re_Lpp": f"{float(np.mean([float(r['Re_L_double_prime']) for r in rows])):.17e}",
            "pearson_Re_Lpp_vs_mean_spacing_minus_smin": f"{pearson(re2, close):.17e}",
            "pearson_Re_Lpp_vs_smin": f"{pearson(re2, smins_np):.17e}",
            "mean_smin_exceptional": f"{float(np.mean(exc_smins)):.17e}" if exc_smins else "",
            "mean_smin_negative": f"{float(np.mean(non_smins)):.17e}" if non_smins else "",
            "exceptional_j_list": ";".join(str(j) for j in exceptions),
            "search_note": search_note,
        }
    ]

    write_csv(ART / "dirichlet_L_zeros_and_derivatives_step389.csv", rows)
    write_csv(ART / "close_pair_correlation_step389.csv", corr_rows)

    zeta_neg_frac = 0.93
    zeta_r = 0.7322
    this_r = float(corr_rows[0]["pearson_Re_Lpp_vs_mean_spacing_minus_smin"])
    verdict = (
        "partial_universality_close_pair_correlation_present_but_sign_bias_differs"
        if abs(this_r) > 0.4
        else "zeta_specific_no_strong_dirichlet_close_pair_correlation"
    )
    if neg_count / n > 0.85 and abs(this_r - zeta_r) < 0.25:
        verdict = "zeta_like_universality_supported"

    comparison_md = [
        "# Step 389 Comparison to Zeta",
        "",
        "Inherited zeta baseline from Step 378:",
        "- `93/100` zeta zeros have `Re zeta''(rho_j) < 0`.",
        "- Exceptional zeta zeros have compressed local spacing.",
        "- Pearson `r(Re zeta'', Delta_bar - s_min) = 0.7322`.",
        "",
        f"Dirichlet `{CHAR_LABEL}` result:",
        f"- zeros computed: `{n}`.",
        f"- negative / nonnegative Re L'': `{neg_count}/{pos_count}`.",
        f"- Pearson `r(Re L'', Delta_bar_L - s_min)`: `{this_r:.6g}`.",
        f"- exceptional j list: `{';'.join(str(j) for j in exceptions) or 'none'}`.",
        "",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "comparison_to_zeta_step389.md").write_text("\n".join(comparison_md) + "\n")

    summary = [
        "# Step 389 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 377: `93/100 zeros have Re zeta''(rho_j) < 0; 7 exceptions identified`.",
        "- Step 378: `Pearson r = 0.732 between Re zeta''(rho_j) and (Delta_bar - s_min)`.",
        "- Step 381: `close-pair contribution g_j'_near = +/- i/s_min`.",
        "",
        f"Character: `{CHAR_LABEL}` mod `{Q}`.",
        f"Zeros computed: `{n}`.",
        f"Sign count Re L'': negative `{neg_count}`, nonnegative `{pos_count}`.",
        f"Pearson close-pair correlation: `{this_r:.17e}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step389_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 389,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "character": CHAR_LABEL,
        "q": Q,
        "target_zeros": TARGET_N,
        "computed_zeros": n,
        "mpmath_dps_scan": DPS_SCAN,
        "mpmath_dps_root": DPS_ROOT,
        "mpmath_dps_derivative": DPS_DERIV,
        "negative_count": neg_count,
        "nonnegative_count": pos_count,
        "pearson_close_pair": this_r,
        "verdict": verdict,
    }
    (ART / "step389_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step389.md").write_text(
        "# Nonclaim Boundary - Step 389\n\n"
        "No RH claim is made. Zeros are numerical critical-line zeros found for "
        "`L(s,chi_3)` by direct root-finding; this is an empirical universality "
        "test, not a proof of GRH or a theorem for all Dirichlet L-functions.\n"
    )

    print(f"computed_zeros={n}")
    print(f"negative={neg_count} nonnegative={pos_count}")
    print(f"pearson={this_r:.17e}")
    print(verdict)


if __name__ == "__main__":
    main()
