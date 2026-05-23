import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path(__file__).resolve().parent

# 1. Weighted Gram scenario: exact frame plus bounded fluctuations.
q = 257
lengths = np.arange(8, 160, 8)
records = []
for d in lengths:
    lam_prim = q - 1 - d
    # toy fluctuation norms as fractions of main term
    for fluct_frac in [0.05, 0.20, 0.50, 0.90, 1.10]:
        certified = lam_prim * (1 - fluct_frac)
        records.append({"d_N": d, "q": q, "lambda_prim": lam_prim, "fluct_frac": fluct_frac, "certified_gamma": certified})
df = pd.DataFrame(records)
df.to_csv(out / "weighted_import_fluctuation_model_step127.csv", index=False)

plt.figure(figsize=(7,4.5))
for frac, grp in df.groupby("fluct_frac"):
    plt.plot(grp["d_N"], grp["certified_gamma"], label=f"fluct={frac}")
plt.axhline(0, linestyle="--", linewidth=1)
plt.xlabel("coefficient dimension d_N")
plt.ylabel("certified lower-frame gamma")
plt.title("Weighted lower frame under fluctuation control")
plt.legend()
plt.tight_layout()
plt.savefig(out / "weighted_import_fluctuation_model_step127.png", dpi=200)
plt.close()

# 2. Platform fit scores (subjective audit categories converted to a finite table).
platforms = pd.DataFrame([
    ["Complete prime characters", 5, 1, 1, 5, 5],
    ["CIS asymptotic large sieve", 4, 2, 3, 4, 3],
    ["Pratt-Robles", 4, 3, 2, 3, 3],
    ["BPRZ twisted second moment", 5, 4, 4, 3, 4],
    ["Tang-Wu mixed moment", 4, 4, 4, 3, 3],
    ["Gao-Wu-Zhao mollified 4th", 3, 5, 3, 2, 4],
    ["Heap-Soundararajan", 2, 4, 1, 3, 5],
], columns=["platform","coefficient_uniformity","source_weight_relevance","q_aspect_fit","shortness_room","import_readiness"])
platforms.to_csv(out / "platform_fit_scores_step127.csv", index=False)
plt.figure(figsize=(8,4.8))
idx = np.arange(len(platforms))
plt.plot(idx, platforms["coefficient_uniformity"], marker="o", label="coeff uniform")
plt.plot(idx, platforms["source_weight_relevance"], marker="o", label="weight relevance")
plt.plot(idx, platforms["q_aspect_fit"], marker="o", label="q-aspect fit")
plt.plot(idx, platforms["import_readiness"], marker="o", label="readiness")
plt.xticks(idx, platforms["platform"], rotation=35, ha="right")
plt.ylabel("audit score (1-5)")
plt.title("Step 127 import-platform audit")
plt.legend()
plt.tight_layout()
plt.savefig(out / "platform_fit_scores_step127.png", dpi=200)
plt.close()

# 3. Effective source strength under visibility floor.
Q = np.logspace(2, 8, 80)
scenarios = []
for c_floor in [0.05, 0.1, 0.25, 0.5]:
    for theta in [0.05, 0.1, 0.25]:
        gamma = Q**theta
        eff = c_floor * gamma
        scenarios.append(pd.DataFrame({"Q": Q, "c_floor": c_floor, "theta_gamma": theta, "effective_strength": eff}))
sc = pd.concat(scenarios, ignore_index=True)
sc.to_csv(out / "effective_source_strength_scenarios_step127.csv", index=False)
plt.figure(figsize=(7,4.5))
for (c_floor, theta), grp in sc.groupby(["c_floor","theta_gamma"]):
    if c_floor in [0.1,0.5] and theta in [0.05,0.25]:
        plt.loglog(grp["Q"], grp["effective_strength"], label=f"c={c_floor}, theta={theta}")
plt.xlabel("source conductor scale Q")
plt.ylabel("gamma * c_hyb")
plt.title("Effective source strength with positive visibility floor")
plt.legend()
plt.tight_layout()
plt.savefig(out / "effective_source_strength_step127.png", dpi=200)
plt.close()

# 4. Main/error matrix import model.
eps_vals = np.linspace(0, 1.2, 100)
main_strength = 1.0
cert = np.maximum(0, (1-eps_vals)*main_strength)
pd.DataFrame({"epsilon_error_ratio": eps_vals, "certified_fraction": cert}).to_csv(out / "main_error_import_model_step127.csv", index=False)
plt.figure(figsize=(6.5,4.2))
plt.plot(eps_vals, cert)
plt.axvline(1, linestyle="--", linewidth=1)
plt.xlabel("uniform error / main ratio epsilon")
plt.ylabel("certified lower-frame fraction")
plt.title("Uniform Main+Err import gate")
plt.tight_layout()
plt.savefig(out / "main_error_import_model_step127.png", dpi=200)
plt.close()

# verification file
checks = {
    "min_certified_gamma_positive_fluct_0.05": float(df[df.fluct_frac==0.05].certified_gamma.min()),
    "platform_count": int(len(platforms)),
    "scenario_rows": int(len(sc)),
    "main_error_threshold_epsilon": 1.0,
}
import json
with open(out / "step127_sanity_checks.json", "w") as f:
    json.dump(checks, f, indent=2)
