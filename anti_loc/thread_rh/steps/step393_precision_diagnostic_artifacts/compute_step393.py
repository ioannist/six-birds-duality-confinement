#!/usr/bin/env python3
"""Step 393: high-precision diagnostic for Step 392 failure cell."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step393_precision_diagnostic_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 200
J0 = 470
K_SWEEP = list(range(2, 9))
NEIGHBORS = [468, 469, 470, 471, 472]
STEP392_VALUE = mp.mpf("0.0313774613260747500200605119627")
THRESHOLD = mp.mpf("0.034")


def load_step292() -> Any:
    spec = importlib.util.spec_from_file_location("step292_for_step393", STEP292)
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


def compute_abs(mod: Any, T: mp.mpf, max_k: int) -> dict[int, mp.mpf]:
    zds = mod.zeta_derivatives(T, max_k, DPS)
    mds = mod.mellin_derivatives(mod.GENERATORS["G_star"], T, max_k, DPS)
    return {k: abs(mod.delta_from_derivatives(zds, mds, k)) for k in range(max_k + 1)}


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    mod = load_step292()

    rho470 = mp.zetazero(J0)
    T470 = mp.im(rho470)
    vals470 = compute_abs(mod, T470, max(K_SWEEP))
    v5 = vals470[5]
    rel_diff = abs(v5 - STEP392_VALUE) / abs(STEP392_VALUE)
    failure_preserved = v5 < THRESHOLD

    hp_rows: list[dict[str, object]] = []
    for k in K_SWEEP:
        val = vals470[k]
        hp_rows.append({
            "row_type": "k_sweep",
            "j": J0,
            "T": mp.nstr(T470, 80),
            "k": k,
            "abs_delta_Dk_dps200": mp.nstr(val, 80),
            "threshold": mp.nstr(THRESHOLD, 20),
            "pass_foreclosure": "PASS" if val >= THRESHOLD else "FAIL",
            "step392_dps50_value_for_k5": mp.nstr(STEP392_VALUE, 40) if k == 5 else "",
            "relative_difference_vs_step392_k5": mp.nstr(rel_diff, 40) if k == 5 else "",
        })

    neighbor_rows: list[dict[str, object]] = []
    for j in NEIGHBORS:
        rho = mp.zetazero(j)
        T = mp.im(rho)
        val = compute_abs(mod, T, 5)[5]
        neighbor_rows.append({
            "j": j,
            "T": mp.nstr(T, 80),
            "k": 5,
            "abs_delta_Dk_dps200": mp.nstr(val, 80),
            "threshold": mp.nstr(THRESHOLD, 20),
            "pass_foreclosure": "PASS" if val >= THRESHOLD else "FAIL",
            "relative_to_j470": mp.nstr(val / v5, 40),
        })

    min_k_row = min(hp_rows, key=lambda r: mp.mpf(str(r["abs_delta_Dk_dps200"])))
    min_neighbor = min(neighbor_rows, key=lambda r: mp.mpf(str(r["abs_delta_Dk_dps200"])))
    fail_k = [r for r in hp_rows if r["pass_foreclosure"] == "FAIL"]
    fail_neighbors = [r for r in neighbor_rows if r["pass_foreclosure"] == "FAIL"]
    verdict_parts = []
    if failure_preserved and rel_diff < mp.mpf("0.01"):
        verdict_parts.append("genuine_high_precision_failure")
    elif rel_diff > mp.mpf("0.10"):
        verdict_parts.append("low_precision_artifact_possible")
    else:
        verdict_parts.append("high_precision_failure_preserved")
    if len(fail_k) == 1 and int(fail_k[0]["k"]) == 5:
        verdict_parts.append("k5_specific_failure")
    elif len(fail_k) > 1:
        verdict_parts.append("multiple_k_failures")
    if len(fail_neighbors) == 1 and int(fail_neighbors[0]["j"]) == J0:
        verdict_parts.append("local_j470_anomaly")
    elif len(fail_neighbors) > 1:
        verdict_parts.append("neighboring_failures_present")
    verdict = "_and_".join(verdict_parts)

    write_csv(ART / "high_precision_j470_step393.csv", hp_rows)
    write_csv(ART / "neighbor_zeros_step393.csv", neighbor_rows)

    summary = [
        "# Step 393 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 196: foreclosure threshold `|L_k| >= 0.034`.",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 380: `35/35` close-pair cells passed foreclosure.",
        "- Step 392: failure cell `j=470`, `k=5`, `|delta_Dk|=0.0313774613`.",
        "",
        f"dps: `{DPS}`.",
        f"j=470, k=5 high-precision value: `{mp.nstr(v5, 50)}`.",
        f"relative difference vs Step 392 dps50: `{mp.nstr(rel_diff, 30)}`.",
        f"k-sweep failures: `{';'.join('k='+str(r['k']) for r in fail_k) or 'none'}`.",
        f"neighbor failures at k=5: `{';'.join('j='+str(r['j']) for r in fail_neighbors) or 'none'}`.",
        f"k-sweep minimum: k=`{min_k_row['k']}`, value=`{min_k_row['abs_delta_Dk_dps200']}`.",
        f"neighbor minimum: j=`{min_neighbor['j']}`, value=`{min_neighbor['abs_delta_Dk_dps200']}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step393_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 393,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "dps": DPS,
        "j": J0,
        "T470": mp.nstr(T470, 80),
        "k5_abs_delta_Dk_dps200": mp.nstr(v5, 80),
        "step392_dps50_value": mp.nstr(STEP392_VALUE, 40),
        "relative_difference": mp.nstr(rel_diff, 40),
        "failure_preserved": bool(failure_preserved),
        "k_sweep": K_SWEEP,
        "k_sweep_fail_count": len(fail_k),
        "neighbor_js": NEIGHBORS,
        "neighbor_fail_count": len(fail_neighbors),
        "verdict": verdict,
    }
    (ART / "step393_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step393.md").write_text(
        "# Nonclaim Boundary - Step 393\n\n"
        "No RH claim is made. This is a high-precision raw-proxy diagnostic for "
        "one foreclosure failure cell and nearby cells, not a fully projected "
        "Burnol/Sonine theorem or a global statement about all zeros.\n"
    )

    print(f"k5_dps200={mp.nstr(v5, 50)}")
    print(f"rel_diff={mp.nstr(rel_diff, 30)}")
    print(verdict)


if __name__ == "__main__":
    main()
