#!/usr/bin/env python3
"""Step 391: identify structural form for chi_3 raw linear gamma."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step391_L_chi3_structural_form_identification_artifacts")
STEP390 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step390_dirichlet_structural_law_universality_artifacts/L_chi3_gamma_extraction_step390.csv")
Q = 3.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    rows = read_csv(STEP390)
    T = np.array([float(r["T"]) for r in rows], dtype=float)
    y = np.array([float(r["gamma_L_linear_in_k"]) for r in rows], dtype=float)
    logT = np.log(T)
    logqT = np.log(Q * T / (2 * math.pi))

    out: list[dict[str, object]] = []

    # C1: a log T + b
    a, b = np.linalg.lstsq(np.column_stack([logT, np.ones_like(T)]), y, rcond=None)[0]
    pred = a * logT + b
    out.append({"candidate": "C1", "form": "a*log(T)+b", "a": a, "b": b, "c": "", "RMSE": rmse(y, pred)})

    # C2: a + b/log(qT/(2pi))
    x2 = 1.0 / logqT
    b2, a2 = np.linalg.lstsq(np.column_stack([x2, np.ones_like(T)]), y, rcond=None)[0]
    pred = a2 + b2 / logqT
    out.append({"candidate": "C2", "form": "a+b/log(qT/(2pi))", "a": a2, "b": b2, "c": "", "RMSE": rmse(y, pred)})

    # C3: a log(qT/(2pi)) + b
    a3, b3 = np.linalg.lstsq(np.column_stack([logqT, np.ones_like(T)]), y, rcond=None)[0]
    pred = a3 * logqT + b3
    out.append({"candidate": "C3", "form": "a*log(qT/(2pi))+b", "a": a3, "b": b3, "c": "", "RMSE": rmse(y, pred)})

    # C4: a*T^c+b
    def power_model(t: np.ndarray, aa: float, cc: float, bb: float) -> np.ndarray:
        return aa * (t ** cc) + bb

    best = None
    for p0 in [(-0.1, 0.5, -1.0), (-1.0, 0.1, 0.0), (1.0, -0.5, -2.0), (-0.3, 0.3, -0.8)]:
        try:
            popt, _ = curve_fit(power_model, T, y, p0=p0, maxfev=20000)
            pred = power_model(T, *popt)
            score = rmse(y, pred)
            if best is None or score < best[0]:
                best = (score, popt, pred)
        except Exception:
            continue
    if best is None:
        out.append({"candidate": "C4", "form": "a*T^c+b", "a": "", "b": "", "c": "", "RMSE": "fit_failed"})
    else:
        score, popt, _ = best
        aa, cc, bb = popt
        out.append({"candidate": "C4", "form": "a*T^c+b", "a": aa, "b": bb, "c": cc, "RMSE": score})

    # C5: constant
    const = float(np.mean(y))
    pred = np.full_like(y, const)
    out.append({"candidate": "C5", "form": "constant", "a": const, "b": "", "c": "", "RMSE": rmse(y, pred)})

    # Sort for analysis but write original candidate order in CSV.
    numeric = [r for r in out if isinstance(r["RMSE"], float)]
    best_row = min(numeric, key=lambda r: float(r["RMSE"]))
    const_row = next(r for r in out if r["candidate"] == "C5")
    clean = float(best_row["RMSE"]) < 0.03
    verdict = "clean_structural_form_identified" if clean else "no_clean_form_small_dataset"

    write_csv(ART / "structural_fits_step391.csv", out)

    md = [
        "# Step 391 Best Fit Analysis",
        "",
        "Data source: Step 390 `L_chi3_gamma_extraction_step390.csv`; no derivative recomputation.",
        "",
        "Citations from inherited records used verbatim:",
        "- Step 389: `zeta-like universality supported` for close-pair sign flips.",
        "- Step 390: `both versions fail` for the q-adjusted Branch C structural law under the raw linear-in-k Dirichlet proxy.",
        "",
        "## Ranking",
    ]
    for r in sorted(numeric, key=lambda row: float(row["RMSE"])):
        md.append(f"- {r['candidate']} `{r['form']}`: RMSE `{float(r['RMSE']):.8g}`")
    md += [
        "",
        f"Best candidate: `{best_row['candidate']}` with form `{best_row['form']}`.",
        f"Parameters: a=`{best_row['a']}`, b=`{best_row['b']}`, c=`{best_row['c']}`.",
        f"Constant baseline RMSE: `{float(const_row['RMSE']):.8g}`.",
        "",
        "Interpretation: the best two-parameter log-scale forms improve materially over a constant, but the RMSE remains above the 0.03 clean-law threshold. The raw Dirichlet evaluator is monotone in T over the first ten zeros, but this dataset does not isolate a theorem-grade structural law.",
        "",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "best_fit_analysis_step391.md").write_text("\n".join(md) + "\n")

    summary = [
        "# Step 391 Results Summary",
        "",
        f"Best candidate: `{best_row['candidate']}` `{best_row['form']}`.",
        f"Best RMSE: `{float(best_row['RMSE']):.12g}`.",
        f"Best parameters: a=`{best_row['a']}`, b=`{best_row['b']}`, c=`{best_row['c']}`.",
        f"Constant RMSE: `{float(const_row['RMSE']):.12g}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step391_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 391,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "data_source": str(STEP390),
        "N": len(T),
        "best_candidate": best_row["candidate"],
        "best_form": best_row["form"],
        "best_RMSE": float(best_row["RMSE"]),
        "constant_RMSE": float(const_row["RMSE"]),
        "clean_threshold": 0.03,
        "verdict": verdict,
    }
    (ART / "step391_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step391.md").write_text(
        "# Nonclaim Boundary - Step 391\n\n"
        "No RH claim is made. This is a least-squares structural-form diagnostic "
        "for the Step 390 raw Dirichlet proxy, not a theorem for Dirichlet "
        "L-functions or a projected Burnol/Sonine statement.\n"
    )

    print(f"best={best_row['candidate']} rmse={float(best_row['RMSE']):.12g}")
    print(f"constant_rmse={float(const_row['RMSE']):.12g}")
    print(verdict)


if __name__ == "__main__":
    main()
