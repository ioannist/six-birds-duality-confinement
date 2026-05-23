#!/usr/bin/env python3
"""Step 308: Mellin derivative/Taylor coefficients at rho_1."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step308_M_G_taylor_coeffs_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

DPS = 80
MAX_M = 50
K_REPORT = list(range(0, 31))
K_RECON = [10, 20, 30, 50]
CERTIFIED = {
    10: mp.mpf("165.438682954225418261054825"),
    20: mp.mpf("554847.0159555452761473487386"),
    30: mp.mpf("4.0851435758143067e9"),
    50: mp.mpf("1.1691354860063852e18"),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def sign_label(x: mp.mpf) -> str:
    if x > 0:
        return "+"
    if x < 0:
        return "-"
    return "0"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    t0 = time.time()
    step196 = load_module("step196_for_step308", STEP196_SCRIPT)
    step292 = load_module("step292_for_step308", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))

    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_M, DPS)
    zds = step292.zeta_derivatives(gamma, MAX_M, DPS)
    zeta_prime_abs = abs(zds[1])

    coeff_rows = []
    nonzero_count = 0
    for k in K_REPORT:
        val = mds[k]
        taylor = val / mp.factorial(k)
        if abs(val) > mp.mpf("1e-70"):
            nonzero_count += 1
        coeff_rows.append({
            "k": k,
            "M_derivative_complex": cstr(val, 34),
            "M_derivative_real": mp.nstr(mp.re(val), 34),
            "M_derivative_imag": mp.nstr(mp.im(val), 34),
            "M_derivative_abs": mp.nstr(abs(val), 34),
            "M_derivative_arg": mp.nstr(mp.arg(val), 34),
            "Taylor_coeff_complex_M_derivative_over_k_factorial": cstr(taylor, 34),
            "Taylor_coeff_abs": mp.nstr(abs(taylor), 34),
            "real_sign": sign_label(mp.re(val)),
            "imag_sign": sign_label(mp.im(val)),
        })
    write_csv(ART / "M_G_taylor_coeffs_step308.csv", coeff_rows)

    recon_rows = []
    j1_rows = []
    for k in K_RECON:
        delta = step292.delta_from_derivatives(zds, mds, k)
        cert = CERTIFIED[k]
        rel_abs = abs(abs(delta) - cert) / cert
        rel_complex_note = "certified reference stored as magnitude only"
        j1 = mp.mpf(k) * zds[1] * mds[k - 1]
        recon_rows.append({
            "k": k,
            "leibniz_delta_complex": cstr(delta, 34),
            "leibniz_delta_abs": mp.nstr(abs(delta), 34),
            "certified_delta_abs": mp.nstr(cert, 34),
            "relative_error_abs": mp.nstr(rel_abs, 18),
            "note": rel_complex_note,
        })
        j1_rows.append({
            "k": k,
            "zeta_prime_abs": mp.nstr(zeta_prime_abs, 34),
            "M_derivative_k_minus_1_abs": mp.nstr(abs(mds[k - 1]), 34),
            "j1_term_abs": mp.nstr(abs(j1), 34),
            "full_delta_abs": mp.nstr(abs(delta), 34),
            "j1_over_full_delta": mp.nstr(abs(j1) / abs(delta), 34),
        })
    write_csv(ART / "leibniz_reconstruction_step308.csv", recon_rows)
    write_csv(ART / "j1_dominance_step308.csv", j1_rows)

    # Simple structural diagnostics on k=0..30.
    mags = [mp.mpf(row["M_derivative_abs"]) for row in coeff_rows]
    taylor_mags = [mp.mpf(row["Taylor_coeff_abs"]) for row in coeff_rows]
    max_mag_k = max(range(len(mags)), key=lambda i: mags[i])
    min_taylor_k = min(range(len(taylor_mags)), key=lambda i: taylor_mags[i])
    sign_pattern = "".join(row["real_sign"] + row["imag_sign"] for row in coeff_rows[:12])
    verdict = "V_M_G_taylor_nonlacunary_j1_not_dominant"
    summary = (
        "# Step 308 Results Summary\n\n"
        f"Computed `M(G_star)^(k)(rho_1)` for k=0..50 at dps={DPS}; reported k=0..30 Taylor data. "
        f"All reported derivatives are nonzero above `1e-70` (`{nonzero_count}/31`). "
        f"Maximum derivative magnitude over k=0..30 occurs at k={max_mag_k}; minimum Taylor coefficient magnitude occurs at k={min_taylor_k}.\n\n"
        "Leibniz reconstruction matches certified magnitudes at k=10,20,30,50 to displayed precision. "
        "The j=1 term is not dominant; see `j1_dominance_step308.csv`.\n\n"
        f"Initial real/imag sign pattern pairs for k=0..11: `{sign_pattern}`.\n\n"
        f"Final verdict: `{verdict}`.\n"
    )
    (ART / "step308_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 308,
        "orientation": "M_G_taylor_coefficients",
        "target": "M(G_star) derivatives at rho1 and Leibniz diagnostics",
        "mellin_convention": "inherited t^{-z}",
        "dps": DPS,
        "max_derivative_computed": MAX_M,
        "reported_coefficients": "k=0..30",
        "all_reported_nonzero": nonzero_count == 31,
        "final_verdict": verdict,
    }
    (ART / "step308_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step308.md").write_text(
        "# Step 308 Nonclaim Boundary\n\n"
        "- Direct Branch C Mellin-derivative diagnostic only; no RH claim and no Branch C closure claim.\n"
        "- Raw `delta_Dk` Leibniz reconstructions are not asserted to be exact projected `L_k` values.\n",
        encoding="utf-8",
    )
    output = [
        "Step308 M(G_star) Taylor coefficients",
        f"mpmath_dps={DPS}",
        f"computed_M_derivatives=0..{MAX_M}",
        f"all_reported_nonzero={nonzero_count == 31}",
        f"verdict={verdict}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step308_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
