#!/usr/bin/env python3
"""Step 307: order/type audit and finite-type obstruction."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step307_delta_Dk_lower_bound_artifacts")
MP_DPS = 80
CERTIFIED = {
    5: mp.mpf("4.2765574702035627"),
    10: mp.mpf("165.438682954225418261054825"),
    15: mp.mpf("8515.269827226146629003791658"),
    20: mp.mpf("554847.0159555452761473487386"),
    30: mp.mpf("4.0851435758143067e9"),
    50: mp.mpf("1.1691354860063852e18"),
}


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    radii = [10, 20, 50, 100, 200]
    rows = []
    for R in radii:
        # Probe the far-left real ray away from trivial-zero integers by adding
        # a small imaginary part.  This illustrates log|zeta|/R growing like
        # log R, i.e. infinite order-1 type.
        z = mp.mpc(-mp.mpf(R), mp.mpf("0.37"))
        log_zeta = mp.log(abs(mp.zeta(z)))
        rows.append({
            "R": R,
            "z": f"{mp.nstr(mp.re(z), 20)}+{mp.nstr(mp.im(z), 20)}j",
            "log_abs_zeta": mp.nstr(log_zeta, 30),
            "log_abs_zeta_over_R": mp.nstr(log_zeta / R, 30),
            "log_R": mp.nstr(mp.log(R), 30),
            "interpretation": "growth/R increases with log R; finite type tau is not available",
        })
    with (ART / "h_order_type_probe_step307.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Constants for M(G): support is [1.3, 3.7] under t^{-z}.
    support = {
        "support_min": 1.3,
        "support_max": 3.7,
        "M_exponential_indicator_bound": "max(log(3.7), -log(1.3)) = log(3.7)",
        "log_3p7": float(mp.log(mp.mpf("3.7"))),
        "minus_log_1p3": float(-mp.log(mp.mpf("1.3"))),
        "zeta_type_status": "order 1, infinite type in the meromorphic zeta factor; after M(1)=0 cancellation h is entire but not finite type by this route",
    }
    (ART / "h_order_type_step307.json").write_text(json.dumps(support, indent=2), encoding="utf-8")

    # A deliberately labeled finite-sample diagnostic bound.  It is not claimed
    # as a theorem; it records how weak an elementary exponential lower scale
    # can be while still lying below the certified points.
    A0 = mp.mpf("1e-6")
    b0 = mp.mpf("2.0")
    alpha0 = mp.mpf("0.0")
    lb_rows = []
    for k, cert in CERTIFIED.items():
        bound = A0 * (b0 ** k) * (mp.mpf(k) ** alpha0)
        lb_rows.append({
            "k": k,
            "candidate_A0": mp.nstr(A0, 18),
            "candidate_b0": mp.nstr(b0, 18),
            "candidate_alpha0": mp.nstr(alpha0, 18),
            "candidate_k0": 10,
            "predicted_lower_bound": mp.nstr(bound, 30),
            "certified_delta_abs": mp.nstr(cert, 30),
            "bound_over_certified": mp.nstr(bound / cert, 30),
            "status": "finite_sample_diagnostic_not_theorem",
        })
    with (ART / "predicted_lower_bound_step307.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(lb_rows[0].keys()))
        writer.writeheader()
        writer.writerows(lb_rows)

    m_json = ART / "M_G_at_1_step307.json"
    m_info = json.loads(m_json.read_text(encoding="utf-8")) if m_json.exists() else {}
    verdict = "V_delta_Dk_lower_bound_blocked_no_finite_type"
    summary = (
        "# Step 307 Results Summary\n\n"
        f"`M(G_star)(1)` absolute value: `{m_info.get('M_G_star_1_abs', 'run compute_M_G_at_1_step307.py')}`. "
        "This numerically cancels the zeta pole at `z=1`; `M(G_star)(rho_1)` is nonzero, so the zero at `rho_1` comes from zeta.\n\n"
        "The finite-type route fails: the zeta functional equation gives `log|zeta(-R+i eta)| = R log R + O(R)` off trivial-zero rays, so after the pole cancellation `h=zeta*M(G_star)` is not finite type in the order-one sense. "
        "Cauchy-Hadamard/Stirling finite-type coefficient asymptotics therefore do not apply.\n\n"
        "No theorem-grade lower bound `|delta_Dk| >= A0 b0^k k^alpha0` for all `k >= k0` was derived from standard entire-function order/type tools. "
        "The CSV contains only a finite-sample diagnostic lower scale, explicitly not a theorem.\n\n"
        f"Final verdict: `{verdict}`.\n"
    )
    (ART / "step307_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 307,
        "orientation": "lower_bound_attempt",
        "target": "theorem-grade lower bound for delta_Dk rho1 G_star",
        "M_G_star_1_abs": m_info.get("M_G_star_1_abs"),
        "M_G_star_rho1_abs": m_info.get("M_G_star_rho1_abs"),
        "order": "1",
        "type_status": "infinite_type_by_zeta_functional_equation_route",
        "explicit_lower_bound_derived": False,
        "final_verdict": verdict,
    }
    (ART / "step307_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step307.md").write_text(
        "# Step 307 Nonclaim Boundary\n\n"
        "- Direct Branch C lower-bound attempt only; no RH claim and no Branch C closure claim.\n"
        "- The finite-sample diagnostic bound in `predicted_lower_bound_step307.csv` is not asserted as a theorem.\n",
        encoding="utf-8",
    )
    print("Step307 order/type probe")
    print(json.dumps(support, indent=2))
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
