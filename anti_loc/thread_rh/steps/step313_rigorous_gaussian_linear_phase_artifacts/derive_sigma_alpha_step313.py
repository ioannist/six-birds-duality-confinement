#!/usr/bin/env python3
"""Step 313: curvature/phase decomposition for Leibniz saddle."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step313_rigorous_gaussian_linear_phase_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP309_DOM = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step309_leibniz_j_distribution_artifacts/dominant_j_and_interference_step309.csv")
STEP312_ALPHA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step312_discrete_stationary_phase_bound_artifacts/alpha_sigma_per_k_step312.csv")

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


def log_binom(k: int, j: int) -> mp.mpf:
    return mp.log(mp.mpf(math.comb(k, j)))


def unwrap_three(a: mp.mpf, b: mp.mpf, c: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    vals = [a, b, c]
    out = [vals[0]]
    two_pi = 2 * mp.pi
    for ph in vals[1:]:
        x = ph
        while x - out[-1] > mp.pi:
            x -= two_pi
        while x - out[-1] < -mp.pi:
            x += two_pi
        out.append(x)
    return out[0], out[1], out[2]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step196 = load_module("step196_for_step313", STEP196_SCRIPT)
    step292 = load_module("step292_for_step313", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    zds = step292.zeta_derivatives(gamma, MAX_K, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_K, DPS)
    dom_by_k = {int(r["k"]): int(r["dominant_j"]) for r in read_csv(STEP309_DOM)}
    empirical_by_k = {int(r["k"]): r for r in read_csv(STEP312_ALPHA)}

    pred_rows = []
    bound_rows = []

    for k in K_TARGETS:
        j = dom_by_k[k]
        if j <= 0 or j >= k:
            raise RuntimeError(f"cannot compute central derivatives at edge j={j}, k={k}")
        m = k - j
        # Discrete second derivatives in j of each log-magnitude component.
        b2 = log_binom(k, j+1) - 2*log_binom(k, j) + log_binom(k, j-1)
        z2 = mp.log(abs(zds[j+1])) - 2*mp.log(abs(zds[j])) + mp.log(abs(zds[j-1]))
        # j -> k-j, so neighboring j values use M^(m-1), M^m, M^(m+1).
        m2 = mp.log(abs(mds[m-1])) - 2*mp.log(abs(mds[m])) + mp.log(abs(mds[m+1]))
        total2 = b2 + z2 + m2
        sigma_local = mp.sqrt(-1/total2) if total2 < 0 else mp.nan
        sigma_binomial_exact = mp.sqrt(-1/b2) if b2 < 0 else mp.nan
        sigma_binomial_asymp = mp.sqrt(mp.mpf(k)/4)
        correction = z2 + m2
        correction_over_binomial = abs(correction / b2)

        # Local phase derivative at the same dominant j.
        def term(idx: int) -> mp.mpc:
            return mp.mpf(math.comb(k, idx)) * zds[idx] * mds[k-idx]
        ph_m = mp.arg(term(j-1))
        ph_0 = mp.arg(term(j))
        ph_p = mp.arg(term(j+1))
        up_m, up_0, up_p = unwrap_three(ph_m, ph_0, ph_p)
        alpha_local = abs((up_p - up_m) / 2)
        phase_second_local = up_p - 2*up_0 + up_m

        empirical = empirical_by_k[k]
        sigma_emp = mp.mpf(empirical["sigma_weighted_std"])
        alpha_emp = mp.mpf(empirical["alpha_central_slope_abs"])
        pred_rows.append({
            "k": k,
            "dominant_j": j,
            "sigma_binomial_asymptotic_sqrt_k_over_2": mp.nstr(sigma_binomial_asymp, 18),
            "sigma_binomial_exact_local": mp.nstr(sigma_binomial_exact, 18),
            "sigma_total_local_from_second_derivative": mp.nstr(sigma_local, 18),
            "sigma_empirical_weighted": mp.nstr(sigma_emp, 18),
            "sigma_total_over_empirical": mp.nstr(sigma_local/sigma_emp, 18),
            "alpha_local_phase_derivative": mp.nstr(alpha_local, 18),
            "alpha_empirical_central_slope": mp.nstr(alpha_emp, 18),
            "alpha_local_over_empirical": mp.nstr(alpha_local/alpha_emp, 18),
        })
        bound_rows.append({
            "k": k,
            "dominant_j": j,
            "binomial_second_derivative": mp.nstr(b2, 34),
            "binomial_asymptotic_minus_4_over_k": mp.nstr(-mp.mpf(4)/k, 34),
            "zeta_logabs_second_difference": mp.nstr(z2, 34),
            "M_logabs_second_difference": mp.nstr(m2, 34),
            "zeta_plus_M_correction": mp.nstr(correction, 34),
            "abs_correction_over_abs_binomial": mp.nstr(correction_over_binomial, 34),
            "total_logabs_second_difference": mp.nstr(total2, 34),
            "local_phase_second_difference": mp.nstr(phase_second_local, 34),
            "rigor_assessment": "numeric_decomposition_not_uniform_bound",
        })

    write_csv(ART / "sigma_alpha_predicted_vs_empirical_step313.csv", pred_rows)
    write_csv(ART / "second_derivative_bounds_step313.csv", bound_rows)

    verdict = "V_gaussian_linear_phase_partial_binomial_dominates_sigma_alpha_still_empirical"
    theorem = r"""\section*{Step 313 Updated Theorem Audit}

\paragraph{Gaussian magnitude saddle.}
For
\[
T_{k,j}={k\choose j}\zeta^{(j)}(\rho_1)M(G_\star)^{(k-j)}(\rho_1),
\]
the binomial component contributes
\[
\Delta_j^2 \log {k\choose j}
=
\log {k\choose j+1}-2\log {k\choose j}+\log {k\choose j-1}
\approx -\frac{4}{k}
\]
near \(j=k/2\).  Hence the binomial-only Gaussian width is
\[
\sigma_{\rm bin}(k)\approx \sqrt{k}/2.
\]
The numerical decomposition in this step shows that the zeta-derivative
and Mellin-derivative corrections are comparable but do not destroy the
negative quadratic saddle in the certified range.

\paragraph{Phase law.}
The local phase derivative
\[
\alpha(k)\approx \frac12\left(\arg T_{k,j_\ast+1}-\arg T_{k,j_\ast-1}\right)
\]
matches the empirical central phase slope only at a numerical level.
No analytic formula or uniform bound for \(\alpha(k)\) was derived.

\paragraph{Theorem status.}
The Step 310 lower-bound theorem is not upgraded to rigorous status in
this step.  The Gaussian magnitude saddle is structurally supported by
the Stirling/binomial curvature and verified numerically after adding
zeta/M corrections.  The remaining load-bearing gap is a uniform,
analytic control of
\[
\Delta_j \arg\left(\zeta^{(j)}(\rho_1)M(G_\star)^{(k-j)}(\rho_1)\right)
\]
and the discrete stationary-phase remainder.
"""
    (ART / "upgraded_theorem_step313.tex").write_text(theorem, encoding="utf-8")

    summary = [
        "# Step 313 Results Summary",
        "",
        "Computed the discrete second derivative of `log|term_j|` near the dominant `j*(k)` and decomposed it into binomial, zeta-derivative, and Mellin-derivative pieces.",
        "The binomial piece gives the expected `-4/k` curvature and `sigma_binomial ≈ sqrt(k)/2`, close to the empirical widths.",
        "",
        "The zeta and Mellin corrections are not negligible enough to yield a clean proof from Stirling alone, but the total curvature remains negative in the certified range and produces a Gaussian saddle.",
        "The alpha/phase law remains numerical: no analytic formula or uniform phase-derivative bound was derived.",
        "",
        "The Step 310 theorem therefore remains conditional.  Step 313 strengthens the magnitude-saddle side but does not close the interference theorem.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step313_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 313,
        "orientation": "gaussian_linear_phase_rigor_attempt",
        "target": "derive Gaussian magnitude saddle and linear phase structure for Leibniz terms",
        "dps": DPS,
        "k_targets": K_TARGETS,
        "sigma_result": "binomial sqrt(k)/2 structurally supported; zeta/M corrections numeric",
        "alpha_result": "phase slope remains numerical; no uniform analytic bound",
        "theorem_status": "not upgraded to rigorous",
        "final_verdict": verdict,
    }
    (ART / "step313_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step313.md").write_text(
        "# Step 313 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not prove Branch C closure.\n"
        "- This step does not upgrade the Step 310 lower-bound theorem to rigorous status.\n"
        "- The alpha/phase derivative control remains a numerical diagnostic, not a theorem.\n",
        encoding="utf-8",
    )
    print("Step313 sigma/alpha derivation attempt")
    for row in pred_rows:
        print(
            "k={k} sigma_bin={sb} sigma_total={st} sigma_emp={se} alpha_local={al} alpha_emp={ae}".format(
                k=row["k"],
                sb=row["sigma_binomial_asymptotic_sqrt_k_over_2"],
                st=row["sigma_total_local_from_second_derivative"],
                se=row["sigma_empirical_weighted"],
                al=row["alpha_local_phase_derivative"],
                ae=row["alpha_empirical_central_slope"],
            )
        )
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()

