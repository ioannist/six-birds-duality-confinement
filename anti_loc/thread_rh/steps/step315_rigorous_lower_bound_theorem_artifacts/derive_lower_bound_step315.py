#!/usr/bin/env python3
"""Step 315: attempt worst-case-alpha lower-bound theorem."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step315_rigorous_lower_bound_theorem_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP309_DOM = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step309_leibniz_j_distribution_artifacts/dominant_j_and_interference_step309.csv")
STEP308_LEIBNIZ = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step308_M_G_taylor_coeffs_artifacts/leibniz_reconstruction_step308.csv")

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


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step196 = load_module("step196_for_step315", STEP196_SCRIPT)
    step292 = load_module("step292_for_step315", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    zds = step292.zeta_derivatives(gamma, MAX_K, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_K, DPS)
    dom_by_k = {int(r["k"]): int(r["dominant_j"]) for r in read_csv(STEP309_DOM)}
    certified = {int(r["k"]): mp.mpf(r["leibniz_delta_abs"]) for r in read_csv(STEP308_LEIBNIZ)}

    term_rows = []
    bound_rows = []
    for k in K_TARGETS:
        j = dom_by_k[k]
        m = k - j
        binom = mp.mpf(math.comb(k, j))
        zabs = abs(zds[j])
        mabs = abs(mds[m])
        term_abs = binom * zabs * mabs
        worst_phase_factor = mp.e ** (-(mp.pi**2) * k / 8)
        formal_lower = term_abs * worst_phase_factor
        cert = certified[k]
        term_rows.append({
            "k": k,
            "j_star": j,
            "m": m,
            "binomial_C_k_jstar": mp.nstr(binom, 34),
            "zeta_derivative_abs": mp.nstr(zabs, 34),
            "M_derivative_abs": mp.nstr(mabs, 34),
            "term_jstar_abs": mp.nstr(term_abs, 34),
            "worst_case_phase_factor_exp_minus_pi2k_over8": mp.nstr(worst_phase_factor, 34),
            "formal_term_times_phase_lower": mp.nstr(formal_lower, 34),
        })
        bound_rows.append({
            "k": k,
            "formal_lower_term_jstar_exp_minus_pi2k_over8": mp.nstr(formal_lower, 34),
            "certified_delta_Dk_abs": mp.nstr(cert, 34),
            "certified_over_formal_lower": mp.nstr(cert/formal_lower, 34) if formal_lower != 0 else "inf",
            "formal_lower_over_certified": mp.nstr(formal_lower/cert, 34),
            "sample_check": "passes_finite_sample" if formal_lower <= cert else "fails_finite_sample",
            "proof_status": "not_rigorous_interference_step_invalid",
        })

    write_csv(ART / "term_j_star_lower_bounds_step315.csv", term_rows)
    write_csv(ART / "delta_Dk_lower_bound_step315.csv", bound_rows)

    verdict = "V_worst_case_alpha_theorem_blocked_invalid_interference_lower_bound"
    theorem = r"""\section*{Step 315 Attempted Worst-Case-\(\alpha\) Lower Bound}

\paragraph{Requested theorem form.}
The requested argument would infer
\[
|\delta_{D,k}(\rho_1,G_\star)|
\ge |T_{k,j_\ast}|\exp(-\pi^2 k/8),
\]
using \(|\alpha|\le \pi\) and \(\sigma^2\approx k/4\).

\paragraph{Blocker.}
This implication is not rigorous.  A worst-case bound
\(|\alpha|\le\pi\) does not give a positive lower bound on the magnitude
of a complex sum.  Even terms with phases in an interval of length
\(\le 2\pi\) can cancel exactly.  A Gaussian-Fourier heuristic gives
\(\exp(-\alpha^2\sigma^2/2)\) only after one has proved a Gaussian
amplitude profile, an approximately linear phase, and a controlled
stationary-phase remainder.

There is also a direction issue: from \(\sigma^2\ge k/4\) one obtains
\[
\exp(-\pi^2\sigma^2/2)\le \exp(-\pi^2 k/8),
\]
not a lower bound by \(\exp(-\pi^2 k/8)\).  A lower bound of that shape
would require an upper bound \(\sigma^2\le k/4\), or a separate direct
interference estimate.

\paragraph{Finite-sample diagnostic.}
The formal expression
\[
|T_{k,j_\ast}|\exp(-\pi^2k/8)
\]
is below the certified \(|\delta_{D,k}|\) for \(k=10,20,30,50\).  This
is a numerical diagnostic only; it is not a proof for all \(k\).

\paragraph{Conclusion.}
No fully rigorous constants \(A_0,b_0,k_0\) are derived in this step.
The Step 310 theorem remains conditional.  The tightness gap remains the
same: proving a uniform interference lower bound requires ratio-
conjecture-grade or stationary-phase-grade phase control, not only
\(|\alpha|\le\pi\).
"""
    (ART / "theorem_with_constants_step315.tex").write_text(theorem, encoding="utf-8")

    tightness = (
        "# Step 315 Tightness Audit\n\n"
        "The formal worst-case-alpha factor `exp(-pi^2 k/8)` is extremely small. "
        "It passes the certified finite sample only because it is very loose. "
        "However, it is not a theorem-grade interference lower bound: bounded phase frequency alone does not prevent exact cancellation.\n\n"
        "Empirically, Step 312 found alpha about `0.39-0.43`, while the worst-case uses `pi`. "
        "The sharp-vs-worst exponent gap is therefore on the order of `((pi^2-alpha^2)/2)*sigma^2`, which is exponentially large in k. "
        "Closing this gap requires the same pointwise high-order zeta-derivative phase-ratio control identified in Step 314.\n"
    )
    (ART / "tightness_audit_step315.md").write_text(tightness, encoding="utf-8")

    summary = (
        "# Step 315 Results Summary\n\n"
        "Attempted to formalize the requested worst-case-alpha theorem.  The finite-sample computation of "
        "`|T_{k,j*}| exp(-pi^2 k/8)` is below the certified `|delta_Dk|` at k=10,20,30,50, but the proof step is invalid: "
        "`|alpha| <= pi` alone does not imply a positive lower bound for a complex sum, and the claimed sigma inequality has the wrong direction for a lower bound.\n\n"
        "No explicit all-k theorem constants `(A_0,b_0,k_0)` were rigorously derived.  The Step 310 theorem remains conditional.\n\n"
        f"Final verdict: `{verdict}`.\n"
    )
    (ART / "step315_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 315,
        "orientation": "rigorous_lower_bound_attempt",
        "target": "worst-case alpha theorem for delta_Dk lower bound",
        "dps": DPS,
        "finite_sample_k": K_TARGETS,
        "formal_sample_check": "passes certified finite sample",
        "theorem_status": "blocked",
        "blocker": "bounded alpha does not imply nonzero interference lower bound; sigma inequality direction also invalid",
        "final_verdict": verdict,
    }
    (ART / "step315_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step315.md").write_text(
        "# Step 315 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not prove Branch C closure.\n"
        "- This step does not prove the Step 310 lower-bound theorem.\n"
        "- The requested worst-case-alpha theorem is blocked; no all-k constants are claimed.\n",
        encoding="utf-8",
    )
    print("Step315 worst-case-alpha lower-bound attempt")
    for row in bound_rows:
        print(
            "k={k} formal_lower={lb} certified={cert} ratio_cert_over_lower={ratio} status={status}".format(
                k=row["k"],
                lb=row["formal_lower_term_jstar_exp_minus_pi2k_over8"],
                cert=row["certified_delta_Dk_abs"],
                ratio=row["certified_over_formal_lower"],
                status=row["sample_check"],
            )
        )
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()

