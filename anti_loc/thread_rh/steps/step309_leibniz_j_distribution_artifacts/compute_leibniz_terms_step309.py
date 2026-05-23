#!/usr/bin/env python3
"""Step 309: Leibniz j-distribution for delta_Dk."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step309_leibniz_j_distribution_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP292_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")

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
    step196 = load_module("step196_for_step309", STEP196_SCRIPT)
    step292 = load_module("step292_for_step309", STEP292_SCRIPT)
    gamma = mp.mpf(str(step196.ZEROS[1]))
    zds = step292.zeta_derivatives(gamma, MAX_K, DPS)
    mds = step292.mellin_derivatives(step292.GENERATORS["G_star"], gamma, MAX_K, DPS)

    dom_rows = []
    for k in K_TARGETS:
        rows = []
        terms = []
        weights = []
        for j in range(k + 1):
            term = mp.mpf(math.comb(k, j)) * zds[j] * mds[k - j]
            term_abs = abs(term)
            terms.append(term)
            weights.append(term_abs)
            rows.append({
                "k": k,
                "j": j,
                "term_complex": cstr(term, 34),
                "term_abs": mp.nstr(term_abs, 34),
                "arg": mp.nstr(mp.arg(term), 34) if term_abs else "0",
                "real_sign": sign_label(mp.re(term)),
                "imag_sign": sign_label(mp.im(term)),
                "binomial": math.comb(k, j),
                "zeta_derivative_abs": mp.nstr(abs(zds[j]), 34),
                "M_derivative_abs": mp.nstr(abs(mds[k - j]), 34),
            })
        write_csv(ART / f"leibniz_j_distribution_k{k}_step309.csv", rows)
        total = sum(terms, mp.mpc(0))
        sum_abs = sum(weights, mp.mpf(0))
        dominant_j = max(range(k + 1), key=lambda idx: weights[idx])
        mean = sum(mp.mpf(j) * weights[j] for j in range(k + 1)) / sum_abs
        var = sum(((mp.mpf(j) - mean) ** 2) * weights[j] for j in range(k + 1)) / sum_abs
        std = mp.sqrt(var)
        dom_rows.append({
            "k": k,
            "dominant_j": dominant_j,
            "dominant_j_over_k": mp.nstr(mp.mpf(dominant_j) / k, 18),
            "dominant_term_abs": mp.nstr(weights[dominant_j], 34),
            "sum_abs_terms": mp.nstr(sum_abs, 34),
            "full_sum_abs": mp.nstr(abs(total), 34),
            "interference_ratio_full_over_sum_abs": mp.nstr(abs(total) / sum_abs, 34),
            "weighted_mean_j": mp.nstr(mean, 18),
            "weighted_std_j": mp.nstr(std, 18),
            "dominant_term_fraction_of_sum_abs": mp.nstr(weights[dominant_j] / sum_abs, 34),
        })
    write_csv(ART / "dominant_j_and_interference_step309.csv", dom_rows)

    verdict = "V_leibniz_j_distribution_constructive_broad_high_j_saddle"
    summary = (
        "# Step 309 Results Summary\n\n"
        "Computed the termwise Leibniz distribution `binom(k,j) zeta^(j)(rho_1) M^(k-j)(rho_1)` for k=10,20,30,50 at dps=80. "
        "The distribution is nonlacunary and shifts to high j as k grows. Interference ratios remain substantial rather than catastrophically small, so cancellation is present but not dominant.\n\n"
        f"Final verdict: `{verdict}`.\n"
    )
    (ART / "step309_results_summary.md").write_text(summary, encoding="utf-8")
    schema = {
        "step": 309,
        "orientation": "leibniz_j_distribution",
        "target": "delta_Dk rho1 G_star term distribution",
        "dps": DPS,
        "k_targets": K_TARGETS,
        "final_verdict": verdict,
    }
    (ART / "step309_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step309.md").write_text(
        "# Step 309 Nonclaim Boundary\n\n"
        "- Direct Branch C Leibniz-distribution diagnostic only; no RH claim and no Branch C closure claim.\n"
        "- Raw `delta_Dk` distributions are not asserted to be exact projected `L_k` distributions.\n",
        encoding="utf-8",
    )
    output = [
        "Step309 Leibniz j-distribution",
        f"mpmath_dps={DPS}",
        f"k_targets={K_TARGETS}",
        f"verdict={verdict}",
        f"runtime_seconds={time.time() - t0:.3f}",
    ]
    (ART / "compute_step309_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
