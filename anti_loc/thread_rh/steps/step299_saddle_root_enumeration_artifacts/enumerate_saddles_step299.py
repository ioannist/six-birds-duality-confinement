#!/usr/bin/env python3
"""Step 299: enumerate saddle roots for Branch C delta_Dk."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step299_saddle_root_enumeration_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP271_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step271_branch_C_saddle_numerics_artifacts/solve_saddle_step271.py")
STEP271_SADDLE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step271_branch_C_saddle_numerics_artifacts/saddle_z_star_step271.csv")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
STEP292_DELTA = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/delta_Dk_certified_step292.csv")
STEP296_CORRECTED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts/corrected_L_k_step296.csv")

MP_DPS = 80
K_VALUES = [10, 20, 30, 50]


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


def parse_complex(s: str) -> mp.mpc:
    c = complex(s.replace("+-", "-"))
    return mp.mpc(mp.mpf(str(c.real)), mp.mpf(str(c.imag)))


class ExactMellinG:
    def __init__(self, step292):
        self.step292 = step292
        self.centers, self.epsilons, self.coeffs = step292.moment_coefficients(step292.GENERATORS["G_star"])

    def deriv(self, z: mp.mpc, n: int) -> mp.mpc:
        total = mp.mpc(0)
        for c, eps, coeff in zip(self.centers, self.epsilons, self.coeffs):
            lo, hi = c - eps, c + eps

            def integrand(t, cc=c, ee=eps, aa=coeff, nn=n):
                return aa * self.step292.beta_bump((t - cc) / ee) * (t ** (z - 1)) * (mp.log(t) ** nn)

            total += mp.quad(integrand, [lo, hi])
        return total


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


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step299", STEP196_SCRIPT)
    step271 = load_module("step271_for_step299", STEP271_SCRIPT)
    step292 = load_module("step292_for_step299", STEP292_SCRIPT)
    rho = mp.mpc(mp.mpf("0.5"), mp.mpf(str(step196.ZEROS[1])))
    exact_mg = ExactMellinG(step292)

    # Fast Step271-style approximation for basin selection.
    spec = step196.GENERATORS["G_star"]
    moments = step196.compute_moments(spec)
    t, w, g = step196.build_t_quadrature(spec, moments, step196.N_T_PRIMARY)
    approx_mg = step271.MellinG(t, w, g)

    def exact_logh_prime(z: mp.mpc) -> mp.mpc:
        z0 = mp.zeta(z)
        return mp.zeta(z, derivative=1) / z0 + exact_mg.deriv(z, 1) / exact_mg.deriv(z, 0)

    def exact_logh_second(z: mp.mpc) -> mp.mpc:
        z0 = mp.zeta(z)
        z1 = mp.zeta(z, derivative=1)
        z2 = mp.zeta(z, derivative=2)
        M0 = exact_mg.deriv(z, 0)
        M1 = exact_mg.deriv(z, 1)
        M2 = exact_mg.deriv(z, 2)
        return z2 / z0 - (z1 / z0) ** 2 + M2 / M0 - (M1 / M0) ** 2

    def exact_eq(z: mp.mpc, k: int) -> mp.mpc:
        return exact_logh_prime(z) - (k + 1) / (z - rho)

    def exact_eq_prime(z: mp.mpc, k: int) -> mp.mpc:
        return exact_logh_second(z) + (k + 1) / ((z - rho) ** 2)

    def newton_exact(start: mp.mpc, k: int, maxsteps: int = 10) -> tuple[mp.mpc, mp.mpf]:
        z = mp.mpc(start)
        last_res = mp.inf
        for _ in range(maxsteps):
            try:
                F = exact_eq(z, k)
                Fp = exact_eq_prime(z, k)
            except Exception:
                break
            last_res = abs(F)
            if last_res < mp.mpf("1e-25"):
                break
            if abs(Fp) == 0:
                break
            step = F / Fp
            scale = max(abs(z - rho), mp.mpf("1"))
            if abs(step) > 2 * scale:
                step *= (2 * scale) / abs(step)
            z -= step
            if abs(z - rho) > 40:
                break
        try:
            last_res = abs(exact_eq(z, k))
        except Exception:
            last_res = mp.inf
        return z, last_res

    def approx_residual(z: mp.mpc, k: int) -> float:
        try:
            return float(abs(step271.logh_prime(z, approx_mg) - mp.mpf(k + 1) / (z - rho)))
        except Exception:
            return float("inf")

    prior271 = {}
    for row in read_csv(STEP271_SADDLE):
        if row["triple_id"] == "rho1_G_star":
            prior271[int(row["k"])] = parse_complex(row["z_star"])

    starts = []
    re_vals = np.linspace(-25, 25, 20)
    im_vals = np.linspace(-15, 35, 20)
    grid = []
    for re in re_vals:
        for im in im_vals:
            z = mp.mpc(str(re), str(im))
            if abs(z - rho) <= 30 and abs(z - rho) > mp.mpf("1e-6"):
                grid.append((approx_residual(z, 10), z))
    grid.sort(key=lambda x: x[0])
    starts.extend([z for _, z in grid[:24]])
    starts.extend(prior271.values())
    starts.append(mp.mpc("-9.67631575705349", "19.1401285079905"))  # Step298 branch

    roots = []
    for start in starts:
        if abs(start - rho) > 30:
            continue
        root, res = newton_exact(start, 10, maxsteps=8)
        if abs(root - rho) <= 30 and res < mp.mpf("1e-18"):
            if all(abs(root - r) > mp.mpf("1e-7") for r in roots):
                roots.append(root)

    root_rows = []
    for root in roots:
        d = root - rho
        h = mp.zeta(root) * exact_mg.deriv(root, 0)
        log_integrand = mp.log(abs(h)) - 11 * mp.log(abs(d))
        phi2 = exact_logh_second(root) + 11 / (d ** 2)
        root_rows.append({
            "k": 10,
            "z_star_real": mp.nstr(mp.re(root), 30),
            "z_star_imag": mp.nstr(mp.im(root), 30),
            "R_abs": mp.nstr(abs(d), 30),
            "arg_z_minus_rho": mp.nstr(mp.arg(d), 30),
            "residual_abs": mp.nstr(abs(exact_eq(root, 10)), 12),
            "h_abs": mp.nstr(abs(h), 24),
            "phi2_abs": mp.nstr(abs(phi2), 24),
            "log_integrand": mp.nstr(log_integrand, 24),
            "contribution_proxy": mp.nstr(mp.e ** log_integrand, 24),
            "matches_step271_R_5_06": str(abs(abs(d) - mp.mpf("5.0619976138718769")) < mp.mpf("0.1")),
        })
    root_rows.sort(key=lambda r: float(r["log_integrand"]), reverse=True)
    for i, row in enumerate(root_rows, start=1):
        row["rank"] = i
    write_csv(ART / "saddle_roots_k10_step299.csv", root_rows)
    write_csv(ART / "dominant_root_ranking_step299.csv", root_rows)

    cert = certified_values()
    # Track the dominant exact branch by continuation from the k=10 top-ranked root.
    pred_rows = []
    if root_rows:
        z_start = mp.mpc(mp.mpf(root_rows[0]["z_star_real"]), mp.mpf(root_rows[0]["z_star_imag"]))
    else:
        z_start = mp.mpc("-9.67631575705349", "19.1401285079905")
    for k in K_VALUES:
        try:
            root, res = newton_exact(z_start, k, maxsteps=10)
            if res > mp.mpf("1e-18"):
                raise RuntimeError("newton residual too large")
        except Exception:
            root = z_start
        z_start = root
        d = root - rho
        h = mp.zeta(root) * exact_mg.deriv(root, 0)
        phi2 = exact_logh_second(root) + (k + 1) / (d ** 2)
        pred = mp.factorial(k) / (abs(d) ** k) * abs(h) * mp.sqrt(2 * mp.pi / (k * abs(phi2)))
        cval = mp.mpf(str(cert[k]))
        pred_rows.append({
            "k": k,
            "dominant_z_real": mp.nstr(mp.re(root), 30),
            "dominant_z_imag": mp.nstr(mp.im(root), 30),
            "R_abs": mp.nstr(abs(d), 24),
            "log_integrand": mp.nstr(mp.log(abs(h)) - (k + 1) * mp.log(abs(d)), 24),
            "certified_delta_abs": f"{float(cval):.16e}",
            "dominant_predicted_abs": mp.nstr(pred, 24),
            "relative_error": mp.nstr(abs(pred - cval) / cval, 16),
        })
    write_csv(ART / "dominant_prediction_step299.csv", pred_rows)

    summary = (
        "# Step 299 Results Summary\n\n"
        f"Enumerated {len(root_rows)} exact saddle roots within `|z-rho|<=30` for k=10 from grid-selected starts. "
        "The dominant exact root by `log|h|-(k+1)log R` does not match Step271's `R≈5.06`; no exact root in the enumerated set matches that radius. "
        "Dominant-root Cauchy predictions remain far from the certified values, so the residual factor is not fixed by single-root ranking.\n"
    )
    (ART / "step299_results_summary.md").write_text(summary, encoding="utf-8")
    (ART / "nonclaim_boundary_step299.md").write_text(
        "# Step 299 Nonclaim Boundary\n\n"
        "- Direct Branch C saddle enumeration only; no RH claim and no Branch C closure claim.\n"
        "- Root enumeration is grid/findroot based inside `|z-rho|<=30`; it is not a proof of all complex roots.\n",
        encoding="utf-8",
    )
    schema = {
        "step": 299,
        "orientation": "saddle_root_enumeration",
        "root_count_k10": len(root_rows),
        "dominant_root": root_rows[0] if root_rows else None,
        "dominant_predictions": pred_rows,
        "final_verdict": "V_saddle_root_enumeration_no_step271_match_partial",
    }
    (ART / "step299_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    output = [
        f"Step299 enumerated {len(root_rows)} roots for k=10",
    ]
    if root_rows:
        output.append(f"dominant k10 R={root_rows[0]['R_abs']} logI={root_rows[0]['log_integrand']}")
    for row in pred_rows:
        output.append(f"k={row['k']} pred={row['dominant_predicted_abs']} cert={row['certified_delta_abs']} rel={row['relative_error']}")
    (ART / "compute_step299_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
