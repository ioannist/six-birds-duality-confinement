#!/usr/bin/env python3
"""Step 396: multi-variable predictors of close-pair foreclosure failure."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp
import numpy as np


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step396_failure_predictor_identification_artifacts")
STEP395 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step395_high_T_close_pair_foreclosure_artifacts/close_pair_list_step395.csv")
DPS = 50


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


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def try_logistic(X: np.ndarray, y: np.ndarray) -> tuple[str, float, float, np.ndarray]:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import balanced_accuracy_score
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
        clf = LogisticRegression(max_iter=10000, class_weight="balanced", solver="lbfgs")
        clf.fit(Xs, y)
        pred = clf.predict(Xs)
        acc = float(np.mean(pred == y))
        bal = float(balanced_accuracy_score(y, pred))
        coefs = clf.coef_[0]
        return "sklearn_logistic_class_weight_balanced_in_sample", acc, bal, coefs
    except Exception:
        X1 = np.column_stack([np.ones(len(y)), X])
        beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
        score = X1 @ beta
        pred = (score >= 0.5).astype(int)
        acc = float(np.mean(pred == y))
        # Balanced accuracy manual.
        pos = y == 1
        neg = y == 0
        tpr = float(np.mean(pred[pos] == 1)) if np.any(pos) else float("nan")
        tnr = float(np.mean(pred[neg] == 0)) if np.any(neg) else float("nan")
        bal = (tpr + tnr) / 2
        return "numpy_linear_probability_in_sample", acc, bal, beta[1:]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    base_rows = read_csv(STEP395)
    js = [int(r["j"]) for r in base_rows]
    j_min, j_max = min(js), max(js)

    # Need +/- 5 windows and adjacent s_min.
    T_by_j: dict[int, mp.mpf] = {}
    for j in range(j_min - 6, j_max + 7):
        if j > 0:
            T_by_j[j] = mp.im(mp.zetazero(j))

    smin_by_j: dict[int, mp.mpf] = {}
    for j in range(j_min - 5, j_max + 6):
        if j - 1 in T_by_j and j + 1 in T_by_j:
            smin_by_j[j] = min(T_by_j[j] - T_by_j[j - 1], T_by_j[j + 1] - T_by_j[j])

    rows: list[dict[str, object]] = []
    for r in base_rows:
        j = int(r["j"])
        T = mp.mpf(r["T"])
        rho = mp.mpc(mp.mpf("0.5"), T)
        s_min = mp.mpf(r["s_min"])
        mean_spacing = 2 * mp.pi / mp.log(T / (2 * mp.pi))
        rel_compression = (mean_spacing - s_min) / mean_spacing
        pair_density = sum(1 for jj in range(j - 5, j + 6) if smin_by_j.get(jj, mp.inf) < 1)
        zp = mp.zeta(rho, derivative=1)
        zpp = mp.zeta(rho, derivative=2)
        fail = 1 if r["pass_foreclosure"] == "FAIL" else 0
        rows.append({
            "j": j,
            "T": mp.nstr(T, 30),
            "s_min": mp.nstr(s_min, 30),
            "s_min_prev": mp.nstr(smin_by_j.get(j - 1, mp.nan), 30),
            "s_min_next": mp.nstr(smin_by_j.get(j + 1, mp.nan), 30),
            "pair_density_window_j_minus5_to_plus5": pair_density,
            "mean_spacing": mp.nstr(mean_spacing, 30),
            "relative_compression": mp.nstr(rel_compression, 30),
            "abs_zeta_prime": mp.nstr(abs(zp), 30),
            "Re_zeta_double_prime": mp.nstr(mp.re(zpp), 30),
            "Im_zeta_double_prime": mp.nstr(mp.im(zpp), 30),
            "abs_delta_Dk_k5": r["abs_delta_Dk"],
            "fail": fail,
        })

    y = np.array([int(r["fail"]) for r in rows], dtype=int)
    abs_delta = np.array([float(r["abs_delta_Dk_k5"]) for r in rows], dtype=float)
    feature_names = [
        "T",
        "s_min",
        "s_min_prev",
        "s_min_next",
        "pair_density_window_j_minus5_to_plus5",
        "relative_compression",
        "abs_zeta_prime",
        "Re_zeta_double_prime",
        "Im_zeta_double_prime",
    ]
    corr_rows: list[dict[str, object]] = []
    for name in feature_names:
        x = np.array([float(r[name]) for r in rows], dtype=float)
        corr_rows.append({
            "feature": name,
            "pearson_vs_fail": f"{pearson(x, y):.17e}",
            "abs_pearson_vs_fail": f"{abs(pearson(x, y)):.17e}",
            "pearson_vs_abs_delta_Dk": f"{pearson(x, abs_delta):.17e}",
            "abs_pearson_vs_abs_delta_Dk": f"{abs(pearson(x, abs_delta)):.17e}",
        })
    corr_rows.sort(key=lambda r: float(r["abs_pearson_vs_fail"]), reverse=True)

    top_names = [r["feature"] for r in corr_rows[:5]]
    X = np.column_stack([np.array([float(row[name]) for row in rows], dtype=float) for name in top_names])
    model_name, acc, bal_acc, coefs = try_logistic(X, y)
    baseline_acc = float(max(np.mean(y == 0), np.mean(y == 1)))
    verdict = (
        "dominant_predictor_identified"
        if float(corr_rows[0]["abs_pearson_vs_fail"]) > 0.5
        else "multi_feature_pattern_no_single_dominant_predictor"
        if bal_acc > 0.65
        else "weak_predictors_failure_largely_unexplained"
    )

    write_csv(ART / "extended_features_step396.csv", rows)
    write_csv(ART / "correlations_step396.csv", corr_rows)

    md = [
        "# Step 396 Logistic / Linear Fit",
        "",
        f"Model: `{model_name}`.",
        f"Top features used: `{', '.join(top_names)}`.",
        f"In-sample accuracy: `{acc:.17e}`.",
        f"Balanced accuracy: `{bal_acc:.17e}`.",
        f"Majority-class baseline accuracy: `{baseline_acc:.17e}`.",
        "",
        "| feature | coefficient |",
        "|---|---:|",
    ]
    for name, coef in zip(top_names, coefs):
        md.append(f"| {name} | {coef:.17e} |")
    md += ["", f"Verdict: `{verdict}`."]
    (ART / "logistic_or_linear_fit_step396.md").write_text("\n".join(md) + "\n")

    summary = [
        "# Step 396 Results Summary",
        "",
        "Citations from inherited cascade records used verbatim:",
        "- Step 196: foreclosure threshold `|L_k| >= 0.034`.",
        "- Step 292: `delta_Dk=(zeta*M(G))^(k)(rho)` raw proxy methodology.",
        "- Step 378: compressed-spacing exceptional-zero context.",
        "- Step 392: high-j reduced grid found k=5 failure.",
        "- Step 393: high-precision `j=470,471` low-k failures.",
        "- Step 394: partial close-pair foreclosure failure pattern.",
        "- Step 395: `s_min` alone weak predictor with Pearson r about 0.09.",
        "",
        "Top 5 features by |Pearson r| vs fail:",
    ]
    for r in corr_rows[:5]:
        summary.append(f"- `{r['feature']}`: r=`{r['pearson_vs_fail']}`.")
    summary += [
        f"Fit accuracy: `{acc:.6g}`.",
        f"Balanced accuracy: `{bal_acc:.6g}`.",
        f"Baseline accuracy: `{baseline_acc:.6g}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step396_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 396,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "dps": DPS,
        "rows": len(rows),
        "fail_count": int(np.sum(y)),
        "pass_count": int(len(y) - np.sum(y)),
        "top_feature": corr_rows[0]["feature"],
        "top_abs_pearson_vs_fail": float(corr_rows[0]["abs_pearson_vs_fail"]),
        "model": model_name,
        "fit_accuracy": acc,
        "balanced_accuracy": bal_acc,
        "baseline_accuracy": baseline_acc,
        "verdict": verdict,
    }
    (ART / "step396_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step396.md").write_text(
        "# Nonclaim Boundary - Step 396\n\n"
        "No RH claim is made. This is an empirical feature-analysis diagnostic "
        "on the Step 395 raw-proxy close-pair dataset, not a theorem about all "
        "zeros or a fully projected Burnol/Sonine foreclosure statement.\n"
    )

    print(f"top={corr_rows[0]['feature']} r={corr_rows[0]['pearson_vs_fail']}")
    print(f"acc={acc:.6g} bal={bal_acc:.6g} baseline={baseline_acc:.6g}")
    print(verdict)


if __name__ == "__main__":
    main()
