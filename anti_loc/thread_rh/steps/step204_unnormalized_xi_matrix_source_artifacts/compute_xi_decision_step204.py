#!/usr/bin/env python3
"""Step 204 Xi decision from unnormalized formulation."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts")


def main() -> None:
    # Since c_ij is not certified, M=G^{-1/2}cG^{-1/2} is not formed.
    m_rows = []
    for i in range(1, 4):
        for j in range(1, 4):
            m_rows.append({
                "i": i,
                "j": j,
                "M_real": "",
                "M_imag": "",
                "M_abs": "",
                "status": "not_formed",
                "reason": "c_matrix not certified; c-only trace identity also computes compressed operator, not full C_l P_eta HS norm",
            })
    with (BASE / "M_matrix_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(m_rows[0].keys()))
        writer.writeheader()
        writer.writerows(m_rows)

    decision = {
        "xi_matrix_source_value": "",
        "xi_matrix_source_lower_bound": "",
        "xi_matrix_source_error": "not_certified",
        "xi_matrix_source_verdict": "V_unnormalized_partial",
        "reason": "symbolic derivation shows c-only trace is the compressed P_eta C P_eta diagnostic, not the full ||C_l P_eta||_HS^2 unless an extra range-in-H_eta condition holds; in addition c_ij was not numerically certified because kappa boundary samples remain unavailable as numerical functions.",
        "next_subresidual": "derive_certified_kappa_boundary_sampling_or_H_matrix_<Ckappa_i,Ckappa_j>",
    }
    with (BASE / "xi_decision_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(decision.keys()))
        writer.writeheader()
        writer.writerow(decision)
    (BASE / "xi_decision_payload_step204.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    print("Step 204 Xi decision")
    print("verdict=V_unnormalized_partial")
    print("reason=c-only trace identity insufficient for full HS residual; c_ij not numerically certified")


if __name__ == "__main__":
    main()
