#!/usr/bin/env python3
"""Step 386 artifact writer.

This step attempts the numerical P_infty projected asymptotic requested by the
cascade manager.  The inherited records expose the operator identity

    K_infty^op = delta - sinc - sum_n Psi_n^lambda (Psi_n^lambda)^*

but do not expose a numerical evaluator for the transported coefficients
c_{n,k}(rho) or the weights D_n.  The artifacts therefore record the full
requested grid as attempted and blocked, and import the available Step 383 raw
delta-proxy values only as a non-projected comparator.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step386_numerical_P_infty_projected_artifacts")
STEP383 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step383_extended_close_pair_validation_artifacts/gamma_R_table_100_zeros_step383.csv")

RHO_JS = [1, 5, 10, 15]
KS = [5, 10, 15, 20, 30]
NS = list(range(31))
MISSING_REASON = (
    "blocked_missing_transported_PSWF_evaluator: inherited Step173 names "
    "T174_2/T174_4 as open; no numerical routine for Psi_n^lambda, "
    "D_n=<M_zeta G,Psi_n>, or c_{n,k}(rho)=<T_a^* partial_bar_rho^k "
    "K_a^Gamma(.,rho),Psi_n^lambda> was found"
)


def read_step383() -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    if not STEP383.exists():
        return rows
    with STEP383.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows[int(row["j"])] = row
            except (KeyError, ValueError):
                continue
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    step383 = read_step383()

    c_rows: list[dict[str, object]] = []
    for j in RHO_JS:
        src = step383.get(j, {})
        T = src.get("T", "")
        for k in KS:
            for n in NS:
                c_rows.append({
                    "rho_j": j,
                    "T": T,
                    "lambda": 1,
                    "n": n,
                    "k": k,
                    "c_n_k_rho_real": "",
                    "c_n_k_rho_imag": "",
                    "abs_c_n_k_rho": "",
                    "status": "blocked",
                    "reason": MISSING_REASON,
                })
    write_csv(
        OUT / "c_n_k_rho_grid_step386.csv",
        ["rho_j", "T", "lambda", "n", "k", "c_n_k_rho_real", "c_n_k_rho_imag", "abs_c_n_k_rho", "status", "reason"],
        c_rows,
    )

    l_rows: list[dict[str, object]] = []
    for j in RHO_JS:
        src = step383.get(j, {})
        for k in KS:
            raw_key = f"k{k}_abs_delta_proxy"
            l_rows.append({
                "rho_j": j,
                "T": src.get("T", ""),
                "k": k,
                "A_k_delta_component": "",
                "B_k_sinc_component": "",
                "sum_Dn_cnk": "",
                "L_k_projected_abs": "",
                "raw_delta_proxy_abs_from_step383": src.get(raw_key, ""),
                "status": "blocked_projected_sum",
                "reason": MISSING_REASON,
            })
    write_csv(
        OUT / "L_k_projected_step386.csv",
        ["rho_j", "T", "k", "A_k_delta_component", "B_k_sinc_component", "sum_Dn_cnk", "L_k_projected_abs", "raw_delta_proxy_abs_from_step383", "status", "reason"],
        l_rows,
    )

    g_rows: list[dict[str, object]] = []
    for j in RHO_JS:
        src = step383.get(j, {})
        T = src.get("T", "")
        gamma_struct = ""
        try:
            Tf = float(T)
            gamma_struct = math.pi / (Tf * math.log(Tf / (2 * math.pi)))
        except (TypeError, ValueError, ZeroDivisionError):
            pass
        g_rows.append({
            "rho_j": j,
            "T": T,
            "gamma_projected": "",
            "gamma_struct_pi_over_T_log": f"{gamma_struct:.17g}" if gamma_struct != "" else "",
            "gamma_raw_delta_proxy_from_step383": src.get("gamma_zeta_G_star", src.get("gamma_zeta", src.get("gamma", ""))),
            "relative_error_projected_vs_struct": "",
            "status": "blocked",
            "reason": MISSING_REASON,
        })
    write_csv(
        OUT / "gamma_projected_comparison_step386.csv",
        ["rho_j", "T", "gamma_projected", "gamma_struct_pi_over_T_log", "gamma_raw_delta_proxy_from_step383", "relative_error_projected_vs_struct", "status", "reason"],
        g_rows,
    )

    schema = {
        "step": 386,
        "mode": "ATTEMPT",
        "artifact_dir": str(OUT),
        "requested_c_grid_cells": len(RHO_JS) * len(KS) * len(NS),
        "attempted_c_grid_cells": len(c_rows),
        "computed_c_grid_cells": 0,
        "requested_projected_L_cells": len(RHO_JS) * len(KS),
        "computed_projected_L_cells": 0,
        "requested_gamma_cells": len(RHO_JS),
        "computed_gamma_projected_cells": 0,
        "lambda_baseline": 1,
        "rhos": RHO_JS,
        "ks": KS,
        "n_range": [0, 30],
        "verdict": "blocked_missing_numerical_c_nk_Dn_evaluator",
        "missing_components": [
            "numerical Psi_n^lambda construction in transported Sonine/Mellin coordinates",
            "D_n=<M_zeta G,Psi_n^lambda> coefficients",
            "c_{n,k}(rho)=<T_a^* partial_bar_rho^k K_a^Gamma(.,rho),Psi_n^lambda>",
            "A_k and B_k delta/sinc components compatible with the same normalization",
        ],
        "nonclaim": "No RH claim; no projected gamma was computed.",
    }
    (OUT / "step386_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (OUT / "nonclaim_boundary_step386.md").write_text(
        "# Nonclaim Boundary - Step 386\n\n"
        "No RH claim is made. This attempt does not claim RH, does not claim a theorem-grade "
        "P_infty asymptotic, and does not claim numerical reproduction of "
        "gamma_zeta_projected.  The available cascade records contain the "
        "operator identity but not the numerical coefficient evaluator needed "
        "to instantiate the projected PSWF expansion.\n"
    )

    (OUT / "step386_results_summary.md").write_text(
        "# Step 386 Results Summary\n\n"
        "## Attempted Grid\n"
        f"- Requested/attempted c-grid cells: {len(c_rows)} "
        "(n=0..30, k={5,10,15,20,30}, rho_j={1,5,10,15}).\n"
        "- Numeric c_{n,k}(rho) cells computed: 0.\n"
        "- Projected L_k cells computed: 0.\n"
        "- Projected gamma cells computed: 0.\n\n"
        "## Inherited Record Audit\n"
        "- Step 173 supplies the operational identity "
        "`K_infty^op = delta - sinc - sum_n Psi_n^lambda (Psi_n^lambda)^*`.\n"
        "- Step 173 also records the required follow-up tasks as open: "
        "`T174_2 compute_Mellin_PSWF_tails`, `T174_3 numerical_PSWF_implementation`, "
        "and `T174_4 evaluator_pairings`.\n"
        "- Step 196 contains a final finite-dataset PSWF projection approximation, "
        "but it does not export the decomposed coefficients `D_n` and `c_{n,k}` "
        "required by this step.\n"
        "- Step 292/383 raw delta-proxy values were imported only as reference; "
        "they are not the requested projected sum.\n\n"
        "## Verdict\n"
        "The numerical workaround is blocked at the same structural point named "
        "in Step 385: the cascade lacks a concrete evaluator for the transported "
        "PSWF coefficients and compatible delta/sinc/PSWF decomposition.  This "
        "is not evidence against the pi/(T log(T/(2pi))) law; it is a missing "
        "implementation of the projector-side expansion.\n"
    )


if __name__ == "__main__":
    main()
