#!/usr/bin/env python3
"""Step 298: evaluate h(z*) and refined Cauchy-saddle prediction."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step298_saddle_zeta_M_G_bound_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP292_DELTA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/delta_Dk_certified_step292.csv")
STEP296_CORRECTED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts/corrected_L_k_step296.csv")
STEP297_PRED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step297_delta_Dk_asymptotic_artifacts/predicted_vs_certified_step297.csv")

MP_DPS = 80


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


class MellinG:
    def __init__(self, step292):
        self.gen = step292.GENERATORS["G_star"]
        self.step292 = step292
        self.centers, self.epsilons, self.coeffs = step292.moment_coefficients(self.gen)

    def deriv(self, z: mp.mpc, n: int) -> mp.mpc:
        total = mp.mpc(0)
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t, cc=c, ee=eps, aa=coeff, nn=n):
                return aa * self.step292.beta_bump((t - cc) / ee) * (t ** (z - 1)) * (mp.log(t) ** nn)

            total += mp.quad(integrand, [lo, hi])
        return total


def parse_complex(s: str) -> mp.mpc:
    return mp.mpc(s.replace("+-", "-"))


def certified_values() -> dict[int, float]:
    out = {}
    for row in read_csv(STEP292_DELTA):
        if row["triple_id"] == "rho1_G_star" and int(row["k"]) in {10, 20}:
            out[int(row["k"])] = float(row["delta_Dk_abs_dps80"])
    for row in read_csv(STEP296_CORRECTED):
        k = int(row["k"])
        if k in {30, 50}:
            out[k] = float(row["delta_abs"])
    return out


def step297_errors() -> dict[int, float]:
    out = {}
    for row in read_csv(STEP297_PRED):
        if row["model"].startswith("A"):
            out[int(row["k"])] = float(row["relative_error"])
    return out


def main() -> None:
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step298_eval", STEP196_SCRIPT)
    step292 = load_module("step292_for_step298_eval", STEP292_SCRIPT)
    rho = mp.mpc(mp.mpf("0.5"), mp.mpf(str(step196.ZEROS[1])))
    mg = MellinG(step292)
    cert = certified_values()
    old_err = step297_errors()

    z_rows = read_csv(ART / "saddle_locations_step298.csv")
    product_rows = []
    pred_rows = []
    output = ["Step298 refined Cauchy-saddle prediction"]
    for row in z_rows:
        k = int(row["k"])
        z = mp.mpc(mp.mpf(row["z_star_real"]), mp.mpf(row["z_star_imag"]))
        d = z - rho
        R = abs(d)
        zeta0 = mp.zeta(z)
        zeta1 = mp.zeta(z, derivative=1)
        zeta2 = mp.zeta(z, derivative=2)
        M0 = mg.deriv(z, 0)
        M1 = mg.deriv(z, 1)
        M2 = mg.deriv(z, 2)
        h_abs = abs(zeta0 * M0)
        logh2 = zeta2 / zeta0 - (zeta1 / zeta0) ** 2 + M2 / M0 - (M1 / M0) ** 2
        phi2 = logh2 + (k + 1) / (d ** 2)
        refined = mp.factorial(k) / (R ** k) * h_abs * mp.sqrt(2 * mp.pi / (k * abs(phi2)))
        certified = mp.mpf(str(cert[k]))
        rel_err = abs(refined - certified) / certified
        product_rows.append({
            "k": k,
            "zeta_abs": mp.nstr(abs(zeta0), 24),
            "M_G_abs": mp.nstr(abs(M0), 24),
            "product_abs": mp.nstr(h_abs, 24),
            "phi2_abs": mp.nstr(abs(phi2), 24),
        })
        pred_rows.append({
            "k": k,
            "certified_delta_abs": f"{float(certified):.16e}",
            "R_abs": mp.nstr(R, 24),
            "h_abs": mp.nstr(h_abs, 24),
            "phi2_abs": mp.nstr(abs(phi2), 24),
            "refined_predicted_abs": mp.nstr(refined, 24),
            "relative_error": mp.nstr(rel_err, 16),
            "step297_relative_error": f"{old_err.get(k, float('nan')):.16e}",
            "improved_vs_step297": str(float(rel_err) < old_err.get(k, float("inf"))),
        })
        output.append(
            f"k={k} |zeta*M|={mp.nstr(h_abs, 10)} R={mp.nstr(R, 10)} "
            f"pred={mp.nstr(refined, 10)} cert={mp.nstr(certified, 10)} rel={mp.nstr(rel_err, 8)}"
        )

    write_csv(ART / "zeta_M_G_at_saddle_step298.csv", product_rows)
    write_csv(ART / "refined_prediction_step298.csv", pred_rows)
    (ART / "compute_step298_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")

    max_rel = max(float(r["relative_error"]) for r in pred_rows)
    improved_count = sum(1 for r in pred_rows if r["improved_vs_step297"] == "True")
    assessment = "improves" if improved_count >= 3 else "degrades"
    summary = (
        "# Step 298 Results Summary\n\n"
        "Computed saddle locations, direct `|zeta(z*) M(G)(z*)|`, curvature, and the refined Cauchy-saddle prediction. "
        f"The refined formula improves {improved_count}/4 points versus Step 297 and has max relative error {max_rel:.3g}; it {assessment} the Step 297 calibrated saddle-escape fit and is not theorem-grade.\n"
    )
    (ART / "step298_results_summary.md").write_text(summary, encoding="utf-8")
    (ART / "nonclaim_boundary_step298.md").write_text(
        "# Step 298 Nonclaim Boundary\n\n"
        "- Direct Branch C asymptotic refinement only; no RH claim and no Branch C closure claim.\n"
        "- Refined prediction evaluates the saddle formula numerically; it is not a proof of an all-k asymptotic.\n",
        encoding="utf-8",
    )
    schema = {
        "step": 298,
        "orientation": "direct_branch_C_saddle_refinement",
        "dps": MP_DPS,
        "refined_prediction": pred_rows,
        "improved_points_vs_step297": improved_count,
        "max_relative_error": max_rel,
        "final_verdict": "V_refined_saddle_prediction_worse_branch_mismatch",
    }
    (ART / "step298_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
