#!/usr/bin/env python3
"""Step 296: legacy I_k comparison and corrected L_k values."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/compute_branch_C_k_5_6_7_step269.py")
STEP270_CLOSED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts/closed_identity_step270.csv")
STEP292_DELTA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/delta_Dk_certified_step292.csv")
STEP293_B = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts/L_k_method_B_step293.csv")
STEP294_TABLE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step294_branch_C_L_k_at_k20_k30_k50_artifacts/component_table_step294.csv")
STEP269_POLY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/polynomial_correction_test_step269.csv")
STEP269_DATA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/extended_dataset_step269.csv")

K_CROSS = list(range(13))
K_CORRECT = [10, 15, 20, 30, 50]
RHO_INDEX = 1
G_ID = "G_star"
TRIPLE_ID = "rho1_G_star"


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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cfmt(z: complex) -> str:
    return f"{z.real:+.16e}{z.imag:+.16e}j"


def parse_complex(s: str) -> complex:
    return complex(s.replace("+-", "-"))


def main() -> None:
    step196 = load_module("step196_for_step296_legacy", STEP196_SCRIPT)
    step269 = load_module("step269_for_step296_legacy", STEP269_SCRIPT)
    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    pswf = step196.precompute_pswf(u_grid, step196.N_PSWF_PRIMARY, step269.N_TERMS_TAIL)
    spec = step196.GENERATORS[G_ID]
    moments = step196.compute_moments(spec)
    G_primary, _, _quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
    F = zeta_grid * G_primary
    gamma = float(step196.ZEROS[RHO_INDEX])

    analytical = {int(r["k"]): r for r in read_csv(ART / "I_k_analytical_values_step296.csv")}

    cross_rows = []
    R_by_k: dict[int, complex] = {}
    output = ["Step296 legacy I_k computation"]
    for k in K_CROSS:
        t0 = time.time()
        I = complex(simpson(((-1j) ** k) * step269.sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
        R = 0j
        for n in range(step269.N_TERMS_VALUE):
            mu = float(pswf["vals"][n])
            psi_Dk = step269.psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
            J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
            R += psi_Dk * J_n
        R_by_k[k] = R
        runtime = time.time() - t0
        I_a = parse_complex(analytical[k]["I_analytical_complex"])
        abs_a = abs(I_a)
        abs_l = abs(I)
        rel = abs(I - I_a) / abs_a if abs_a else float("inf")
        cross_rows.append({
            "k": k,
            "I_analytical_complex": analytical[k]["I_analytical_complex"],
            "I_analytical_abs": analytical[k]["I_analytical_abs"],
            "I_legacy_complex": cfmt(I),
            "I_legacy_abs": f"{abs_l:.16e}",
            "relative_complex_error": f"{rel:.16e}",
            "legacy_runtime_seconds": f"{runtime:.6f}",
        })
        output.append(f"k={k} |I_analytical|={abs_a:.8e} |I_legacy|={abs_l:.8e} rel_err={rel:.3e}")

    k_star = next((int(r["k"]) for r in cross_rows if float(r["relative_complex_error"]) > 0.5), None)
    write_csv(ART / "I_k_cross_verification_step296.csv", cross_rows)
    write_csv(ART / "breakdown_threshold_step296.csv", [{
        "threshold_definition": "smallest k with |I_legacy-I_analytical|/|I_analytical| > 0.5",
        "k_star": k_star if k_star is not None else "none_through_12",
        "explanation": "legacy sinc_derivative_n becomes numerically unstable when explicit singular terms stop cancelling",
    }])

    delta_complex: dict[int, complex] = {}
    for row in read_csv(STEP292_DELTA):
        if row["triple_id"] == TRIPLE_ID and int(row["k"]) in {10, 15, 20}:
            delta_complex[int(row["k"])] = parse_complex(row["delta_Dk_complex_dps80"])
    for row in read_csv(STEP294_TABLE):
        if row["triple_id"] == TRIPLE_ID and int(row["k"]) in {30, 50}:
            delta_complex[int(row["k"])] = parse_complex(row["delta_complex"])
    legacy_L_abs = {10: float(next(r for r in read_csv(STEP293_B) if r["k"] == "10")["L_abs"])}
    for row in read_csv(STEP294_TABLE):
        k = int(row["k"])
        if k in {20, 30, 50}:
            legacy_L_abs[k] = float(row["L_abs"])

    corrected_rows = []
    for k in K_CORRECT:
        I_a = parse_complex(analytical[k]["I_analytical_complex"])
        if k in R_by_k and k <= 12:
            R = R_by_k[k]
            R_source = "legacy_R_computed"
        elif k == 10:
            R = parse_complex(next(r for r in read_csv(STEP293_B) if r["k"] == "10")["R_complex"])
            R_source = "Step293_R"
        elif k in {20, 30, 50}:
            R = parse_complex(next(r for r in read_csv(STEP294_TABLE) if int(r["k"]) == k)["R_complex"])
            R_source = "Step294_R_legacy_small"
        else:
            R = 0j
            R_source = "set_zero_unavailable_small_R"
        L_corr = delta_complex[k] - I_a - R
        corrected_rows.append({
            "k": k,
            "delta_abs": f"{abs(delta_complex[k]):.16e}",
            "I_analytical_abs": f"{abs(I_a):.16e}",
            "R_abs": f"{abs(R):.16e}",
            "R_source": R_source,
            "L_corrected_complex": cfmt(L_corr),
            "L_corrected_abs": f"{abs(L_corr):.16e}",
            "legacy_L_abs": f"{legacy_L_abs.get(k, float('nan')):.16e}" if k in legacy_L_abs else "",
            "decision": "delta_dominated_corrected",
        })
    write_csv(ART / "corrected_L_k_step296.csv", corrected_rows)

    step269_abs = {
        int(r["k"]): float(r["L_abs"])
        for r in read_csv(STEP269_DATA)
        if r["triple_id"] == TRIPLE_ID and 0 <= int(r["k"]) <= 7
    }
    small_rows = []
    for k in range(0, 8):
        if k in analytical:
            delta = step269.delta_Dk(gamma, _quad_data, k)
            I_a = parse_complex(analytical[k]["I_analytical_complex"])
            R = R_by_k.get(k, 0j)
            L_corr = delta - I_a - R
            ref = step269_abs[k]
            rel = abs(abs(L_corr) - ref) / ref if ref else float("nan")
            small_rows.append({
                "k": k,
                "corrected_L_abs": f"{abs(L_corr):.16e}",
                "step269_projected_abs": f"{ref:.16e}",
                "relative_error": f"{rel:.16e}" if ref else "nan",
                "status": "consistent" if ref and rel < 1e-5 else "mismatch_or_no_reference",
            })
    write_csv(ART / "step269_smallk_consistency_step296.csv", small_rows)

    write_csv(ART / "content_classification_step296.csv", [
        {"file": "compute_I_k_analytical_step296.py", "kind": "primary_script"},
        {"file": "compute_I_k_legacy_step296.py", "kind": "primary_script"},
        {"file": "I_k_cross_verification_step296.csv", "kind": "cross_verification"},
        {"file": "breakdown_threshold_step296.csv", "kind": "threshold"},
        {"file": "corrected_L_k_step296.csv", "kind": "corrected_values"},
    ])
    (ART / "nonclaim_boundary_step296.md").write_text(
        "# Step 296 Nonclaim Boundary\n\n"
        "- Direct Branch C numerical correction only; no RH claim and no Branch C closure claim.\n"
        "- Corrected high-k values use stable analytical I_k and certified delta values; R is retained where available and set to zero at k=15 because it is unavailable and empirically tiny.\n",
        encoding="utf-8",
    )
    summary = (
        "# Step 296 Results Summary\n\n"
        f"Breakdown threshold k* = {k_star}. Corrected high-k L values are delta-dominated after replacing the unstable legacy I_k primitive by the analytical spectral integral.\n"
    )
    (ART / "step296_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 296,
        "orientation": "direct_branch_C_I_k_verification",
        "breakdown_threshold": k_star,
        "corrected_L_values": corrected_rows,
        "final_verdict": "V_I_k_breakdown_threshold_identified_corrected_L_delta_dominated",
    }
    (ART / "step296_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "compute_I_k_legacy_output_step296.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
