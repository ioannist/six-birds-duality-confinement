#!/usr/bin/env python3
"""Step 395: high-T close-pair foreclosure systematic check."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step395_high_T_close_pair_foreclosure_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 80
J_LO = 400
J_HI = 800
K = 5
THRESHOLD = mp.mpf("0.034")
CLOSE_THRESHOLD = mp.mpf("1.0")
NON_CLOSE_THRESHOLD = mp.mpf("1.5")
BASELINE_N = 20
WORKERS = int(os.environ.get("STEP395_WORKERS", "4"))

_MOD: Any = None
_GEN: Any = None


def init_worker() -> None:
    global _MOD, _GEN
    spec = importlib.util.spec_from_file_location("step292_for_step395", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    _MOD = mod
    _GEN = mod.GENERATORS["G_star"]


def compute_delta(args: tuple[int, str, str, str]) -> dict[str, object]:
    if _MOD is None:
        init_worker()
    j, T_str, s_min_str, sample_type = args
    mp.mp.dps = DPS
    T = mp.mpf(T_str)
    zds = _MOD.zeta_derivatives(T, K, DPS)
    mds = _MOD.mellin_derivatives(_GEN, T, K, DPS)
    val = abs(_MOD.delta_from_derivatives(zds, mds, K))
    return {
        "j": j,
        "T": mp.nstr(T, 50),
        "s_min": s_min_str,
        "k": K,
        "abs_delta_Dk": mp.nstr(val, 50),
        "threshold": mp.nstr(THRESHOLD, 20),
        "pass_foreclosure": "PASS" if val >= THRESHOLD else "FAIL",
        "sample_type": sample_type,
        "dps": DPS,
        "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho_j)",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or np.std(xs) == 0 or np.std(ys) == 0:
        return float("nan")
    return float(np.corrcoef(np.array(xs), np.array(ys))[0, 1])


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS

    T_by_j: dict[int, mp.mpf] = {}
    for j in range(J_LO - 1, J_HI + 2):
        T_by_j[j] = mp.im(mp.zetazero(j))

    features: list[dict[str, object]] = []
    close_jobs: list[tuple[int, str, str, str]] = []
    nonclose_candidates: list[tuple[int, mp.mpf, mp.mpf]] = []
    for j in range(J_LO, J_HI + 1):
        T = T_by_j[j]
        s_bwd = T - T_by_j[j - 1]
        s_fwd = T_by_j[j + 1] - T
        s_min = min(s_bwd, s_fwd)
        row = {
            "j": j,
            "T": mp.nstr(T, 50),
            "s_bwd": mp.nstr(s_bwd, 40),
            "s_fwd": mp.nstr(s_fwd, 40),
            "s_min": mp.nstr(s_min, 40),
        }
        features.append(row)
        if s_min < CLOSE_THRESHOLD:
            close_jobs.append((j, mp.nstr(T, 80), mp.nstr(s_min, 80), "close_pair_smin_lt_1"))
        elif s_min > NON_CLOSE_THRESHOLD:
            nonclose_candidates.append((j, T, s_min))

    # Deterministic spread across the range.
    if len(nonclose_candidates) <= BASELINE_N:
        selected_nonclose = nonclose_candidates
    else:
        idxs = np.linspace(0, len(nonclose_candidates) - 1, BASELINE_N, dtype=int)
        selected_nonclose = [nonclose_candidates[int(i)] for i in idxs]
    baseline_jobs = [
        (j, mp.nstr(T, 80), mp.nstr(s_min, 80), "non_close_baseline_smin_gt_1p5")
        for j, T, s_min in selected_nonclose
    ]

    all_jobs = close_jobs + baseline_jobs
    computed: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=WORKERS, initializer=init_worker) as ex:
        futs = {ex.submit(compute_delta, job): job[0] for job in all_jobs}
        for fut in as_completed(futs):
            computed.append(fut.result())
    computed.sort(key=lambda r: (str(r["sample_type"]), int(r["j"])))

    close_rows = [r for r in computed if r["sample_type"] == "close_pair_smin_lt_1"]
    base_rows = [r for r in computed if r["sample_type"] == "non_close_baseline_smin_gt_1p5"]
    close_fail = [r for r in close_rows if r["pass_foreclosure"] == "FAIL"]
    base_fail = [r for r in base_rows if r["pass_foreclosure"] == "FAIL"]
    r = pearson([float(x["s_min"]) for x in close_rows], [float(x["abs_delta_Dk"]) for x in close_rows])

    write_csv(ART / "close_pair_list_step395.csv", close_rows)
    write_csv(ART / "non_close_pair_baseline_step395.csv", base_rows)

    corr_md = [
        "# Step 395 Correlation",
        "",
        f"Range: `j={J_LO}..{J_HI}`.",
        f"Close-pair criterion: `s_min < {CLOSE_THRESHOLD}`.",
        f"Close-pair count: `{len(close_rows)}`.",
        f"Close-pair failure count at k=5: `{len(close_fail)}`.",
        f"Close-pair failure fraction: `{len(close_fail) / len(close_rows) if close_rows else float('nan'):.17e}`.",
        f"Pearson r between `|delta_Dk(k=5)|` and `s_min` within CP: `{r:.17e}`.",
        "",
        f"Non-close baseline criterion: `s_min > {NON_CLOSE_THRESHOLD}`.",
        f"Non-close baseline cells: `{len(base_rows)}`.",
        f"Non-close baseline failures: `{len(base_fail)}`.",
    ]
    (ART / "correlation_step395.md").write_text("\n".join(corr_md) + "\n")

    if close_rows and len(close_fail) / len(close_rows) >= 0.80:
        verdict = "systematic_high_T_close_pair_foreclosure_failure"
    elif close_rows and len(close_fail) / len(close_rows) < 0.50:
        verdict = "restricted_j470_471_not_systematic"
    else:
        verdict = "mixed_partial_high_T_close_pair_pattern"

    summary = [
        "# Step 395 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 196: foreclosure threshold `|L_k| >= 0.034`.",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 378: compressed-spacing exceptional-zero context.",
        "- Step 380: close-pair robustness test.",
        "- Step 392: high-j reduced grid found a k=5 failure.",
        "- Step 393: dps=200 confirmed `j=470,471` low-k failures.",
        "- Step 394: `partial_step378_exceptional_low_k_failure_confirmed_pair_reproduced`.",
        "",
        f"Close-pair count: `{len(close_rows)}`.",
        f"Close-pair failures at k=5: `{len(close_fail)}`.",
        f"Close-pair failure fraction: `{len(close_fail) / len(close_rows) if close_rows else float('nan'):.6g}`.",
        f"Pearson r |delta_Dk| vs s_min within CP: `{r:.6g}`.",
        f"Non-close baseline pass/fail: `{len(base_rows) - len(base_fail)}/{len(base_fail)}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step395_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 395,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "dps": DPS,
        "j_range": [J_LO, J_HI],
        "close_pair_threshold": float(CLOSE_THRESHOLD),
        "close_pair_count": len(close_rows),
        "close_pair_fail_count": len(close_fail),
        "close_pair_fail_fraction": len(close_fail) / len(close_rows) if close_rows else None,
        "pearson_abs_delta_vs_s_min": r,
        "non_close_threshold": float(NON_CLOSE_THRESHOLD),
        "non_close_baseline_count": len(base_rows),
        "non_close_fail_count": len(base_fail),
        "verdict": verdict,
    }
    (ART / "step395_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step395.md").write_text(
        "# Nonclaim Boundary - Step 395\n\n"
        "No RH claim is made. This is an empirical raw-proxy check at selected "
        "high-T close-pair and baseline zeros, not a theorem about all zeros and "
        "not a fully projected Burnol/Sonine foreclosure statement.\n"
    )

    print(f"CP={len(close_rows)} fail={len(close_fail)} r={r:.6g}")
    print(f"baseline={len(base_rows)} fail={len(base_fail)}")
    print(verdict)


if __name__ == "__main__":
    main()
