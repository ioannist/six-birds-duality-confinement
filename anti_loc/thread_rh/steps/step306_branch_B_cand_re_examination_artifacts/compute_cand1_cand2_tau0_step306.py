#!/usr/bin/env python3
"""Step 306: direct tau=0 comparison of Branch B CAND1/CAND2."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step306_branch_B_cand_re_examination_artifacts")
STEP202_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py")
STEP202_VALUES = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/E_half_values_step202.csv")

MP_DPS = 80
RHO1 = mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def cstr(z: mp.mpc, digits: int = 36) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def read_step202_values() -> dict[str, mp.mpc]:
    vals: dict[str, mp.mpc] = {}
    with STEP202_VALUES.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            vals[row["label"]] = mp.mpc(mp.mpf(row["E_real"]), mp.mpf(row["E_imag"]))
    return vals


def zeta_prime(s: mp.mpc) -> mp.mpc:
    return mp.diff(lambda z: mp.zeta(z), s)


def kernel_bilinear(s: mp.mpc, w: mp.mpc, E_s: mp.mpc, E_1s: mp.mpc, E_w: mp.mpc, E_1w: mp.mpc) -> mp.mpc:
    return (E_s * E_w - E_1s * E_1w) / (s + w - 1)


def kernel_hermitian_text_variant(s: mp.mpc, w: mp.mpc, E_s: mp.mpc, E_1s: mp.mpc, E_w: mp.mpc, E_1w: mp.mpc) -> mp.mpc:
    return (E_s * mp.conj(E_w) - E_1s * mp.conj(E_1w)) / (s + w - 1)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    t0 = time.time()
    step202 = load_module("step202_for_step306", STEP202_SCRIPT)
    s = mp.mpc(mp.mpf("0.5"), mp.mpf("0"))

    # Recompute E-values with one common resolvent to avoid mixing grids.
    data160 = step202.build_resolvent(160)
    E_s, err_s, _ = step202.e_lambda(s, data160)
    E_1s, err_1s, _ = step202.e_lambda(1 - s, data160)
    E_rho, err_rho, _ = step202.e_lambda(RHO1, data160)
    E_1rho, err_1rho, _ = step202.e_lambda(1 - RHO1, data160)

    cand1_bilinear = kernel_bilinear(s, RHO1, E_s, E_1s, E_rho, E_1rho)
    cand1_hermitian = kernel_hermitian_text_variant(s, RHO1, E_s, E_1s, E_rho, E_1rho)

    # Exact zeta-dual candidate from Step 207.
    zp = zeta_prime(RHO1)
    completion = mp.power(mp.pi, -RHO1 / 2) * mp.gamma(RHO1 / 2)
    cand2 = mp.zeta(s) / ((s - RHO1) * zp * completion)

    # Step205 mixed-grid value for provenance compatibility.
    vals = read_step202_values()
    data120 = step202.build_resolvent(120)
    E_s_120, _, _ = step202.e_lambda(s, data120)
    E_1s_120, _, _ = step202.e_lambda(1 - s, data120)
    cand1_step205_mixed = kernel_bilinear(
        s,
        RHO1,
        E_s_120,
        E_1s_120,
        vals["rho_1"],
        vals["one_minus_rho_1"],
    )

    rows = []
    for label, val in [
        ("CAND1_bilinear_recomputed160", cand1_bilinear),
        ("CAND1_hermitian_text_variant", cand1_hermitian),
        ("CAND1_step205_mixed_grid", cand1_step205_mixed),
        ("CAND2_zeta_dual", cand2),
    ]:
        rows.append({
            "quantity": label,
            "tau": "0",
            "rho_index": 1,
            "value_complex": cstr(val),
            "abs": mp.nstr(abs(val), 36),
            "real": mp.nstr(mp.re(val), 36),
            "imag": mp.nstr(mp.im(val), 36),
        })

    comparison_rows = []
    for label, c1 in [
        ("bilinear_recomputed160_vs_CAND2", cand1_bilinear),
        ("hermitian_text_variant_vs_CAND2", cand1_hermitian),
        ("step205_mixed_grid_vs_CAND2", cand1_step205_mixed),
    ]:
        ratio = c1 / cand2
        comparison_rows.append({
            "comparison": label,
            "CAND1_abs": mp.nstr(abs(c1), 36),
            "CAND2_abs": mp.nstr(abs(cand2), 36),
            "ratio_complex": cstr(ratio),
            "ratio_abs": mp.nstr(abs(ratio), 36),
            "relative_difference_abs": mp.nstr(abs(c1 - cand2) / abs(cand2), 36),
        })

    with (ART / "cand1_cand2_tau0_values_step306.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (ART / "cand1_cand2_tau0_comparison_step306.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison_rows[0].keys()))
        writer.writeheader()
        writer.writerows(comparison_rows)

    schema = {
        "step": 306,
        "orientation": "branch_B_candidate_reexamination",
        "target": "CAND1/CAND2 tau=0 direct comparison",
        "mpmath_dps": MP_DPS,
        "E_lambda_method": "Step202 finite cosine-resolvent numerical E_{1/2}",
        "final_verdict": "V_branch_B_CAND1_CAND2_wrong_premise",
    }
    (ART / "step306_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step306.md").write_text(
        "# Step 306 Nonclaim Boundary\n\n"
        "- Direct Branch B CAND1/CAND2 comparison only; no RH claim and no Branch B closure claim.\n"
        "- CAND1 uses Step202/205 numerical E_{1/2}; it is an inherited candidate boundary value, not a certified kappa transport theorem.\n",
        encoding="utf-8",
    )
    summary = (
        "# Step 306 Results Summary\n\n"
        "At `tau=0`, CAND1 boundary-kernel values and CAND2 zeta-dual values disagree by large nonconstant factors. "
        "The inherited artifacts already labeled CAND1 as a boundary-kernel candidate and CAND2 as a single-term `a=1/2` normalization probe. "
        "The equality premise is therefore not licensed by Burnol in the inherited records.\n\n"
        f"Primary ratio `|CAND1_bilinear/CAND2| = {comparison_rows[0]['ratio_abs']}`.\n"
    )
    (ART / "step306_results_summary.md").write_text(summary, encoding="utf-8")
    print("Step306 CAND1/CAND2 tau=0")
    print(f"CAND1_bilinear={cstr(cand1_bilinear, 20)} abs={mp.nstr(abs(cand1_bilinear), 20)}")
    print(f"CAND2={cstr(cand2, 20)} abs={mp.nstr(abs(cand2), 20)}")
    print(f"ratio_abs={mp.nstr(abs(cand1_bilinear / cand2), 20)}")
    print(f"runtime_seconds={time.time() - t0:.3f}")


if __name__ == "__main__":
    main()
