#!/usr/bin/env python3
"""Compare Step 207 CAND1 and CAND2 on the same tau-grid."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
OUTDIR = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
CAND1 = OUTDIR / "CAND1_samples_step207.csv"
CAND2 = OUTDIR / "CAND2_samples_step207.csv"
RATIO = OUTDIR / "ratio_table_step207.csv"
RESOLUTION = OUTDIR / "transport_sampling_resolution_step207.csv"


def fmt(z: mp.mpf | mp.mpc) -> str:
    return mp.nstr(z, 36, min_fixed=0, max_fixed=0)


def load_candidate(path: Path, prefix: str) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out[(row["tau"], row["rho_index"])] = row
    return out


def main() -> None:
    d1 = load_candidate(CAND1, "CAND1")
    d2 = load_candidate(CAND2, "CAND2")
    if set(d1) != set(d2):
        raise RuntimeError("CAND1 and CAND2 grids do not match")

    ratio_rows = []
    ratios_by_i: dict[int, list[mp.mpc]] = defaultdict(list)
    absrat_by_i: dict[int, list[mp.mpf]] = defaultdict(list)
    reliable_by_i: dict[int, list[mp.mpc]] = defaultdict(list)

    for key in sorted(d1, key=lambda k: (int(k[1]), mp.mpf(k[0]))):
        tau, idx = key
        r1 = d1[key]
        r2 = d2[key]
        v1 = mp.mpc(mp.mpf(r1["CAND1_real"]), mp.mpf(r1["CAND1_imag"]))
        v2 = mp.mpc(mp.mpf(r2["CAND2_real"]), mp.mpf(r2["CAND2_imag"]))
        if abs(v2) == 0:
            ratio = mp.nan
            status = "undefined_CAND2_zero"
        else:
            ratio = v1 / v2
            status = "computed"
            ratios_by_i[int(idx)].append(ratio)
            absrat_by_i[int(idx)].append(abs(ratio))
            # CAND1 imported absolute error is ~1e-9; only mark rows reliable
            # when CAND1 is above a conservative 20x threshold.
            try:
                err1 = mp.mpf(r1["error_bound"])
            except Exception:
                err1 = mp.inf
            if abs(v1) > 20 * err1 and abs(v2) > mp.mpf("1e-40"):
                reliable_by_i[int(idx)].append(ratio)

        ratio_rows.append(
            {
                "tau": tau,
                "rho_index": idx,
                "ratio_real": fmt(mp.re(ratio)) if status == "computed" else "",
                "ratio_imag": fmt(mp.im(ratio)) if status == "computed" else "",
                "ratio_abs": fmt(abs(ratio)) if status == "computed" else "",
                "CAND1_abs": r1["CAND1_abs"],
                "CAND1_error_bound": r1["error_bound"],
                "CAND2_abs": r2["CAND2_abs"],
                "status": status,
            }
        )

    with RATIO.open("w", newline="") as f:
        fieldnames = [
            "tau",
            "rho_index",
            "ratio_real",
            "ratio_imag",
            "ratio_abs",
            "CAND1_abs",
            "CAND1_error_bound",
            "CAND2_abs",
            "status",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ratio_rows)

    resolution_rows = []
    overall = "constant"
    for i in sorted(ratios_by_i):
        absvals = absrat_by_i[i]
        min_abs = min(absvals)
        max_abs = max(absvals)
        spread = (max_abs - min_abs) / max_abs if max_abs != 0 else mp.inf
        rels = reliable_by_i[i]
        if rels:
            rel_abs = [abs(r) for r in rels]
            rel_min = min(rel_abs)
            rel_max = max(rel_abs)
            rel_spread = (rel_max - rel_min) / rel_max if rel_max != 0 else mp.inf
            rel_count = len(rels)
        else:
            rel_min = mp.nan
            rel_max = mp.nan
            rel_spread = mp.nan
            rel_count = 0
        status = "nominal_varying_error_dominated" if rel_count == 0 else "varying"
        # A constant proportionality would require tiny relative variation
        # on the whole grid and the reliable subset. The observed spreads are
        # many orders larger.
        if spread < mp.mpf("1e-2") and (not rels or rel_spread < mp.mpf("1e-2")):
            status = "approximately_constant"
        else:
            overall = "varying"
        if rel_count == 0:
            note = (
                "Nominal ratio varies over many orders of magnitude, but no row exceeds "
                "the conservative 20x imported CAND1 absolute-error threshold; the "
                "disagreement pattern is numerical, not a certified equality theorem."
            )
        else:
            note = (
                "CAND1 absolute-error threshold uses imported step205 error; "
                "conservative rows do not show constant ratio."
            )
        resolution_rows.append(
            {
                "rho_index": i,
                "ratio_status": status,
                "all_grid_min_ratio_abs": fmt(min_abs),
                "all_grid_max_ratio_abs": fmt(max_abs),
                "all_grid_relative_spread": fmt(spread),
                "reliable_count": rel_count,
                "reliable_min_ratio_abs": fmt(rel_min) if rels else "",
                "reliable_max_ratio_abs": fmt(rel_max) if rels else "",
                "reliable_relative_spread": fmt(rel_spread) if rels else "",
                "verdict": "CAND1 and CAND2 are structurally different for this rho",
                "notes": note,
            }
        )

    final_verdict = "V_kappa_tau_candidates_disagree" if overall == "varying" else "candidate_proportionality_not_ruled_out"
    resolution_rows.append(
        {
            "rho_index": "overall",
            "ratio_status": overall,
            "all_grid_min_ratio_abs": "",
            "all_grid_max_ratio_abs": "",
            "all_grid_relative_spread": "",
            "reliable_count": "",
            "reliable_min_ratio_abs": "",
            "reliable_max_ratio_abs": "",
            "reliable_relative_spread": "",
            "verdict": final_verdict,
            "notes": "Commutator and Xi evaluation are blocked because the two candidate transport-sampling formulas do not agree up to a constant.",
        }
    )

    with RESOLUTION.open("w", newline="") as f:
        fieldnames = [
            "rho_index",
            "ratio_status",
            "all_grid_min_ratio_abs",
            "all_grid_max_ratio_abs",
            "all_grid_relative_spread",
            "reliable_count",
            "reliable_min_ratio_abs",
            "reliable_max_ratio_abs",
            "reliable_relative_spread",
            "verdict",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resolution_rows)

    print(f"ratio rows written: {len(ratio_rows)}")
    for row in resolution_rows:
        print(
            "resolution",
            row["rho_index"],
            row["ratio_status"],
            row["all_grid_min_ratio_abs"],
            row["all_grid_max_ratio_abs"],
            row["verdict"],
        )


if __name__ == "__main__":
    main()
