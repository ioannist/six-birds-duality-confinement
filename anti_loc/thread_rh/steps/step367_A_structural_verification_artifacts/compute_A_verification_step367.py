#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

mp.mp.dps = 80

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step367_A_structural_verification_artifacts")

GAMMA = {
    "G_star": {
        1: 0.2046, 2: 0.1379, 3: 0.1002, 4: 0.0819, 5: 0.0521,
        6: 0.0738, 7: 0.0087, 8: 0.0353, 9: 0.0459, 10: 0.0461,
        11: 0.0163, 12: 0.0012, 13: 0.0316, 14: 0.0236, 15: 0.0167,
    },
    "G_prime": {
        1: 0.2590, 2: 0.1751, 3: 0.1307, 4: 0.0533, 5: 0.0130,
        6: -0.0187, 7: 0.0269, 8: 0.0403, 9: 0.0449, 10: 0.0418,
        11: 0.0040, 12: 0.0129, 13: 0.0465, 14: 0.0428, 15: 0.0627,
    },
}


def band(k):
    if 1 <= k <= 5:
        return "low_1_5"
    if 6 <= k <= 10:
        return "mid_6_10"
    return "high_11_15"


def stats(values):
    arr = np.array(values, dtype=float)
    return {
        "count": len(arr),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr, ddof=0)),
    }


def main():
    rows = []
    for k in range(1, 16):
        rho = mp.zetazero(k)
        T = float(abs(mp.im(rho)))
        A_pred = math.pi / math.log(T / (2 * math.pi))
        for G, gammas in GAMMA.items():
            gamma = gammas[k]
            A_eff = gamma * T
            rel_err = abs(A_pred - A_eff) / abs(A_pred)
            rows.append({
                "rho_index": k,
                "T": f"{T:.15g}",
                "G": G,
                "gamma": f"{gamma:.15g}",
                "A_predicted_pi_over_log": f"{A_pred:.15g}",
                "A_effective_gamma_times_T": f"{A_eff:.15g}",
                "relative_error": f"{rel_err:.15g}",
                "position_band": band(k),
            })

    with (OUT / "A_predicted_vs_effective_step367.csv").open("w", newline="") as f:
        fields = ["rho_index", "T", "G", "gamma", "A_predicted_pi_over_log", "A_effective_gamma_times_T", "relative_error", "position_band"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    stats_rows = []
    groups = {
        "all_30": rows,
        "G_star_all": [r for r in rows if r["G"] == "G_star"],
        "G_prime_all": [r for r in rows if r["G"] == "G_prime"],
    }
    for name, grp in groups.items():
        st = stats([float(r["relative_error"]) for r in grp])
        stats_rows.append({"group": name, **{k: f"{v:.15g}" for k, v in st.items()}})

    with (OUT / "relative_errors_step367.csv").open("w", newline="") as f:
        fields = ["group", "count", "mean", "median", "max", "std"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(stats_rows)

    strat_rows = []
    for G in ["G_star", "G_prime", "combined"]:
        for b in ["low_1_5", "mid_6_10", "high_11_15"]:
            if G == "combined":
                grp = [r for r in rows if r["position_band"] == b]
            else:
                grp = [r for r in rows if r["position_band"] == b and r["G"] == G]
            st = stats([float(r["relative_error"]) for r in grp])
            strat_rows.append({"G": G, "position_band": b, **{k: f"{v:.15g}" for k, v in st.items()}})

    with (OUT / "position_stratification_step367.csv").open("w", newline="") as f:
        fields = ["G", "position_band", "count", "mean", "median", "max", "std"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(strat_rows)

    schema = {
        "step": 367,
        "orientation": "A(T) structural verification across 15 zeta zeros and two test functions",
        "prediction": "A(T)=pi/log(T/(2*pi))",
        "cell_count": 30,
        "all_30_mean_relative_error": float(stats_rows[0]["mean"]),
        "all_30_median_relative_error": float(stats_rows[0]["median"]),
        "G_star_mean_relative_error": float(stats_rows[1]["mean"]),
        "G_prime_mean_relative_error": float(stats_rows[2]["mean"]),
        "verdict": "leading_low_T_scale_only_not_universal_across_15_by_2",
    }
    (OUT / "step367_schema.json").write_text(json.dumps(schema, indent=2) + "\n")


if __name__ == "__main__":
    main()
