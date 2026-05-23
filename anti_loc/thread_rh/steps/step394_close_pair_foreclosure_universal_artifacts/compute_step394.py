#!/usr/bin/env python3
"""Step 394: universalize close-pair low-k foreclosure failure."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step394_close_pair_foreclosure_universal_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 80
EXCEPTIONAL = [34, 41, 64, 71, 79, 80, 92]
CONFIRMED = [470, 471]
K_VALUES = [2, 3, 4, 5]
THRESHOLD = mp.mpf("0.034")


def load_step292() -> Any:
    spec = importlib.util.spec_from_file_location("step292_for_step394", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compute_for_j(mod: Any, j: int) -> tuple[mp.mpf, dict[int, mp.mpf]]:
    rho = mp.zetazero(j)
    T = mp.im(rho)
    zds = mod.zeta_derivatives(T, max(K_VALUES), DPS)
    mds = mod.mellin_derivatives(mod.GENERATORS["G_star"], T, max(K_VALUES), DPS)
    vals = {k: abs(mod.delta_from_derivatives(zds, mds, k)) for k in K_VALUES}
    return T, vals


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    mod = load_step292()

    target_js = EXCEPTIONAL + CONFIRMED
    all_needed = set(target_js)
    for j in target_js:
        for nb in [j - 1, j + 1]:
            if nb > 0 and nb not in target_js:
                all_needed.add(nb)

    cache: dict[int, tuple[mp.mpf, dict[int, mp.mpf]]] = {}
    for j in sorted(all_needed):
        cache[j] = compute_for_j(mod, j)

    rows: list[dict[str, object]] = []
    for j in target_js:
        T, vals = cache[j]
        category = "step378_exceptional" if j in EXCEPTIONAL else "step393_confirmed_pair"
        for k in K_VALUES:
            val = vals[k]
            rows.append({
                "j": j,
                "category": category,
                "T": mp.nstr(T, 50),
                "k": k,
                "abs_delta_Dk": mp.nstr(val, 50),
                "threshold": mp.nstr(THRESHOLD, 20),
                "pass_foreclosure": "PASS" if val >= THRESHOLD else "FAIL",
                "dps": DPS,
                "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho_j)",
            })

    comp_rows: list[dict[str, object]] = []
    for j in target_js:
        Tj, valsj = cache[j]
        neighbor_candidates = [nb for nb in [j - 1, j + 1] if nb in cache and nb not in target_js]
        for nb in neighbor_candidates:
            Tn, valsn = cache[nb]
            for k in K_VALUES:
                comp_rows.append({
                    "target_j": j,
                    "target_category": "step378_exceptional" if j in EXCEPTIONAL else "step393_confirmed_pair",
                    "neighbor_j": nb,
                    "target_T": mp.nstr(Tj, 40),
                    "neighbor_T": mp.nstr(Tn, 40),
                    "k": k,
                    "target_abs_delta_Dk": mp.nstr(valsj[k], 40),
                    "neighbor_abs_delta_Dk": mp.nstr(valsn[k], 40),
                    "target_over_neighbor": mp.nstr(valsj[k] / valsn[k], 30) if valsn[k] else "",
                    "target_status": "PASS" if valsj[k] >= THRESHOLD else "FAIL",
                    "neighbor_status": "PASS" if valsn[k] >= THRESHOLD else "FAIL",
                })

    step378_rows = [r for r in rows if r["category"] == "step378_exceptional"]
    step378_fail = [r for r in step378_rows if r["pass_foreclosure"] == "FAIL"]
    confirmed_rows = [r for r in rows if r["category"] == "step393_confirmed_pair"]
    confirmed_fail = [r for r in confirmed_rows if r["pass_foreclosure"] == "FAIL"]
    failing_by_j: dict[int, list[int]] = {}
    for r in rows:
        if r["pass_foreclosure"] == "FAIL":
            failing_by_j.setdefault(int(r["j"]), []).append(int(r["k"]))

    if len({int(r["j"]) for r in step378_fail}) == len(EXCEPTIONAL):
        verdict = "uniform_step378_exceptional_low_k_failure"
    elif step378_fail:
        verdict = "partial_step378_exceptional_low_k_failure"
    else:
        verdict = "step378_exceptionals_pass_j470_pair_special"
    if confirmed_fail:
        verdict += "_confirmed_pair_reproduced"

    write_csv(ART / "exceptional_low_k_step394.csv", rows)
    write_csv(ART / "comparison_to_neighbor_baseline_step394.csv", comp_rows)

    summary = [
        "# Step 394 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 196: foreclosure threshold `|L_k| >= 0.034`.",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 378: exceptional zeros `j in {34,41,64,71,79,80,92}`.",
        "- Step 380: close-pair robustness test on exceptional zeros.",
        "- Step 392: high-j reduced grid found failure at `j=470,k=5`.",
        "- Step 393: `j=470,471` fail at low k under dps=200.",
        "",
        f"Step378 exceptional cells: `{len(step378_rows)}`.",
        f"Step378 exceptional failures: `{len(step378_fail)}`.",
        f"Confirmed-pair cells: `{len(confirmed_rows)}`.",
        f"Confirmed-pair failures: `{len(confirmed_fail)}`.",
        "Failing cells by j: " + "; ".join(f"j={j}: k={ks}" for j, ks in sorted(failing_by_j.items())),
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step394_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 394,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "dps": DPS,
        "threshold": float(THRESHOLD),
        "step378_exceptional_js": EXCEPTIONAL,
        "confirmed_js": CONFIRMED,
        "k_values": K_VALUES,
        "step378_exceptional_cells": len(step378_rows),
        "step378_exceptional_failures": len(step378_fail),
        "confirmed_pair_cells": len(confirmed_rows),
        "confirmed_pair_failures": len(confirmed_fail),
        "verdict": verdict,
    }
    (ART / "step394_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step394.md").write_text(
        "# Nonclaim Boundary - Step 394\n\n"
        "No RH claim is made. This is an empirical raw-proxy low-k foreclosure "
        "test for selected close-pair/exceptional zeros, not a proof about all "
        "zeros and not a fully projected Burnol/Sonine theorem.\n"
    )

    print(f"step378_failures={len(step378_fail)}/{len(step378_rows)}")
    print(f"confirmed_failures={len(confirmed_fail)}/{len(confirmed_rows)}")
    print(verdict)


if __name__ == "__main__":
    main()
