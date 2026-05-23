#!/usr/bin/env python3
"""Step 294: compute projected Branch C L_k at k=20,30,50.

This script reuses the exact Step 293 component split

    L_k = delta_Dk - I_k - R_k

for rho1_G_star.  The raw delta_Dk term is computed with the Step 292
Leibniz/Mellin derivative method, while I_k and R_k use the inherited Step
269/293 projected-grid formulas.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import simpson

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step294_branch_C_L_k_at_k20_k30_k50_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/compute_branch_C_k_5_6_7_step269.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP293_B = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts/L_k_method_B_step293.csv")

MP_DPS = 80
RHO_INDEX = 1
G_ID = "G_star"
TRIPLE_ID = "rho1_G_star"
K_TARGETS = [20, 30, 50]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cfmt(z: complex | mp.mpc) -> str:
    zc = complex(z)
    return f"{zc.real:+.16e}{zc.imag:+.16e}j"


def projected_I_R(step269, gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, k: int, n_terms: int) -> tuple[complex, complex]:
    I = complex(simpson(((-1j) ** k) * step269.sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
    R = 0j
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_Dk = step269.psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        R += psi_Dk * J_n
    return I, R


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step294", STEP196_SCRIPT)
    step269 = load_module("step269_for_step294", STEP269_SCRIPT)
    step292 = load_module("step292_for_step294", STEP292_SCRIPT)
    step196.MP_DPS = MP_DPS
    step269.MP_DPS = MP_DPS

    t_setup = time.time()
    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    pswf = step196.precompute_pswf(u_grid, step196.N_PSWF_PRIMARY, step269.N_TERMS_TAIL)
    spec = step196.GENERATORS[G_ID]
    moments = step196.compute_moments(spec)
    G_primary, _, _quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
    F = zeta_grid * G_primary
    gamma = float(step196.ZEROS[RHO_INDEX])

    # Step 292 direct delta_Dk setup, extended to k=50.
    gen = step292.GENERATORS[G_ID]
    gamma_mp = mp.mpf(str(step196.ZEROS[RHO_INDEX]))
    t_delta = time.time()
    zds = step292.zeta_derivatives(gamma_mp, max(K_TARGETS), MP_DPS)
    mds = step292.mellin_derivatives(gen, gamma_mp, max(K_TARGETS), MP_DPS)
    delta_derivative_runtime = time.time() - t_delta

    component_rows: list[dict[str, object]] = []
    output_lines = [
        "Step 294 Branch C rho1_G_star projected L_k via Method B",
        f"mpmath_dps={MP_DPS}",
        f"setup_seconds={time.time() - t_setup:.6f}",
        f"delta_derivative_precompute_seconds={delta_derivative_runtime:.6f}",
        "Step293 k=10 inherited verbatim: |delta|=165.438682954222, |I|=1.4477151875233229e4, |R|=0.00601761, |L|=1.4536004275822408e4",
    ]

    # Include inherited k=10 row verbatim from Step293.
    step293_rows = read_csv(STEP293_B)
    k10 = next(row for row in step293_rows if row["k"] == "10")
    component_rows.append({
        "triple_id": TRIPLE_ID,
        "k": 10,
        "delta_abs": k10["delta_abs"],
        "I_abs": k10["I_abs"],
        "R_abs": k10["R_abs"],
        "L_abs": k10["L_abs"],
        "L_over_I": f"{float(k10['L_abs']) / float(k10['I_abs']):.16e}",
        "delta_complex": k10["delta_complex"],
        "I_complex": k10["I_complex"],
        "R_complex": k10["R_complex"],
        "L_complex": k10["L_complex"],
        "method": "inherited_step293",
        "runtime_seconds": "0.000000",
        "precision_note": "verbatim Step293 component split",
    })

    cross_rows: list[dict[str, object]] = []
    for k in K_TARGETS:
        t0 = time.time()
        delta = step292.delta_from_derivatives(zds, mds, k)
        I, R = projected_I_R(step269, gamma, F, u_grid, pswf, k, step269.N_TERMS_VALUE)
        L = complex(delta) - I - R
        runtime = time.time() - t0
        row = {
            "triple_id": TRIPLE_ID,
            "k": k,
            "delta_abs": f"{abs(complex(delta)):.16e}",
            "I_abs": f"{abs(I):.16e}",
            "R_abs": f"{abs(R):.16e}",
            "L_abs": f"{abs(L):.16e}",
            "L_over_I": f"{abs(L) / abs(I):.16e}" if abs(I) else "nan",
            "delta_complex": cfmt(delta),
            "I_complex": cfmt(I),
            "R_complex": cfmt(R),
            "L_complex": cfmt(L),
            "method": "B_delta_minus_I_minus_R",
            "runtime_seconds": f"{runtime:.6f}",
            "precision_note": "delta dps80 via Step292 Leibniz; I/R inherited projected grid double precision",
        }
        component_rows.append(row)
        output_lines.append(
            f"k={k} |delta|={float(row['delta_abs']):.8e} |I|={float(row['I_abs']):.8e} "
            f"|R|={float(row['R_abs']):.8e} |L|={float(row['L_abs']):.8e} "
            f"|L|/|I|={float(row['L_over_I']):.8e} runtime={runtime:.3f}s"
        )

        if k == 20:
            tA = time.time()
            try:
                L_A = step269.projected_k(gamma, F, u_grid, pswf, _quad_data, k, step269.N_TERMS_VALUE)
                A_status = "completed"
                A_abs = abs(L_A)
                A_minus_B = abs(L_A - L)
                A_runtime = time.time() - tA
                A_complex = cfmt(L_A)
            except Exception as exc:  # pragma: no cover
                A_status = f"failed:{exc}"
                A_abs = float("nan")
                A_minus_B = float("nan")
                A_runtime = time.time() - tA
                A_complex = ""
            cross_rows.append({
                "triple_id": TRIPLE_ID,
                "k": 20,
                "method_A_status": A_status,
                "method_A_L_abs": f"{A_abs:.16e}",
                "method_A_L_complex": A_complex,
                "method_B_L_abs": row["L_abs"],
                "abs_A_minus_B": f"{A_minus_B:.16e}",
                "relative_A_minus_B": f"{A_minus_B / abs(L):.16e}" if abs(L) else "nan",
                "method_A_runtime_seconds": f"{A_runtime:.6f}",
                "decision": "agree" if A_status == "completed" and A_minus_B <= max(1e-6, 1e-10 * abs(L)) else "disagree_or_failed",
            })
            output_lines.append(
                f"k=20 MethodA |L|={A_abs:.8e} MethodB |L|={abs(L):.8e} "
                f"|A-B|={A_minus_B:.3e} status={cross_rows[-1]['decision']}"
            )

    write_csv(ART / "component_table_step294.csv", component_rows)
    write_csv(ART / "cross_check_k20_step294.csv", cross_rows)
    (ART / "compute_step294_output.txt").write_text("\n".join(output_lines) + "\n", encoding="utf-8")

    # Small narrative/metadata artifacts.
    ratios = [(int(r["k"]), float(r["L_over_I"])) for r in component_rows]
    regime = "I_k dominates everywhere tested; L_k grows with I_k" if all(0.9 <= r <= 1.2 for k, r in ratios if k >= 10) else "nontrivial cancellation or numerical transition detected"
    (ART / "asymptotic_regime_step294.md").write_text(
        "# Step 294 Asymptotic Regime\n\n"
        + "\n".join(f"- k={k}: |L_k|/|I_k| = {r:.8g}" for k, r in ratios)
        + f"\n\nAssessment: {regime}.\n",
        encoding="utf-8",
    )
    (ART / "step294_results_summary.md").write_text(
        "# Step 294 Results Summary\n\n"
        "Computed `rho1_G_star` projected `L_k` by Method B at k=20,30,50, with inherited k=10 from Step293. "
        f"The ratio assessment is: {regime}.\n",
        encoding="utf-8",
    )
    (ART / "nonclaim_boundary_step294.md").write_text(
        "# Step 294 Nonclaim Boundary\n\n"
        "- Direct Branch C numerical computation only.\n"
        "- No RH claim and no Branch C closure claim.\n"
        "- I/R correction terms use the inherited projected-grid implementation; high-k floating-grid sensitivity remains a numerical caveat.\n",
        encoding="utf-8",
    )
    write_csv(ART / "content_classification_step294.csv", [
        {"file": "compute_L_k_method_B_step294.py", "kind": "primary_script", "note": "Method B component computation"},
        {"file": "component_table_step294.csv", "kind": "primary_data", "note": "new k=20,30,50 values plus inherited k=10"},
        {"file": "cross_check_k20_step294.csv", "kind": "cross_check", "note": "Method A vs Method B at k=20"},
        {"file": "asymptotic_regime_step294.md", "kind": "interpretation", "note": "ratio behavior"},
    ])
    schema = {
        "step": 294,
        "orientation": "direct_branch_C_high_k_computation",
        "target": "|L_k(rho1,G_star)| at k=20,30,50",
        "dps": MP_DPS,
        "component_table": component_rows,
        "cross_check_k20": cross_rows,
        "asymptotic_regime": regime,
        "retained_nogos": ["no RH claim", "no Branch C closure claim"],
        "final_verdict": "V_branch_C_high_k_I_dominates" if "dominates" in regime else "V_branch_C_high_k_partial_cancellation",
    }
    (ART / "step294_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print("\n".join(output_lines))


if __name__ == "__main__":
    main()
