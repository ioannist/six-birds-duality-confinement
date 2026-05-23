"""Step 40 finite checks for the obstruction-to-repair calculus.
These are PSD algebra sanity checks, not Six Birds simulations.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(4040)


def psd(n, scale=1.0):
    A = rng.normal(size=(n, n))
    return scale * (A.T @ A) / n


def mineig(A):
    return float(np.linalg.eigvalsh((A + A.T) / 2).min())


def budget(Lam, Theta, Eef, Esrc, t):
    return (1 + t) * ((1 / Lam) * Theta + Esrc) + (1 + 1 / t) * Eef

# 1. Monotone repair checks
rows = []
for trial in range(80):
    n = 4
    Theta = np.eye(n)
    Eef = psd(n, scale=0.1)
    Esrc = psd(n, scale=0.1)
    dEef = psd(n, scale=0.02)
    dEsrc = psd(n, scale=0.02)
    # ensure new defects are PSD smaller
    Eef_old = Eef + dEef
    Esrc_old = Esrc + dEsrc
    Lam_old = 1.0 + rng.random() * 3
    Lam_new = Lam_old + rng.random() * 5
    t = 0.1 + rng.random() * 4
    Bold = budget(Lam_old, Theta, Eef_old, Esrc_old, t)
    Bnew = budget(Lam_new, Theta, Eef, Esrc, t)
    rows.append({
        "trial": trial,
        "lambda_old": Lam_old,
        "lambda_new": Lam_new,
        "t": t,
        "min_eig_budget_decrease": mineig(Bold - Bnew),
        "trace_old": float(np.trace(Bold)),
        "trace_new": float(np.trace(Bnew)),
        "trace_decrease": float(np.trace(Bold - Bnew)),
    })
pd.DataFrame(rows).to_csv(OUT / "monotone_repair_checks_step40.csv", index=False)

# 2. Optimized t check
rows = []
for trial in range(50):
    a = 10 ** rng.uniform(-3, 2)
    b = 10 ** rng.uniform(-3, 2)
    tstar = np.sqrt(b / a)
    fstar = (np.sqrt(a) + np.sqrt(b)) ** 2
    grid = np.logspace(-4, 4, 4000)
    fgrid = (1 + grid) * a + (1 + 1 / grid) * b
    rows.append({
        "trial": trial,
        "a": a,
        "b": b,
        "t_star_formula": tstar,
        "trace_bound_formula": fstar,
        "t_star_grid": float(grid[np.argmin(fgrid)]),
        "trace_bound_grid": float(fgrid.min()),
        "rel_error": float(abs(fgrid.min() - fstar) / fstar),
    })
pd.DataFrame(rows).to_csv(OUT / "optimized_t_checks_step40.csv", index=False)

# 3. Character-frame repair: cover missing direction progressively
rows = []
Theta = np.eye(2)
for lam2 in np.logspace(-3, 3, 80):
    F = np.diag([5.0, lam2])
    Lambda = mineig(Theta ** 0.5 @ F @ Theta ** 0.5)
    K_bound = 1 / Lambda
    rows.append({"lambda_missing_character": lam2, "frame_lower_bound": Lambda, "budget_bound": K_bound})
pd.DataFrame(rows).to_csv(OUT / "character_frame_repair_step40.csv", index=False)

# 4. Non-repair examples
rows = []
# Trace/invariant repair: no anti-invariant coverage
for strength in np.logspace(-3, 3, 30):
    F_on_Yminus = np.zeros((2, 2))  # source lives outside Y^-
    rows.append({"case": "trace_only_source", "strength": strength, "frame_lower_bound_on_Yminus": mineig(F_on_Yminus), "effective_budget_bound": np.inf})
# Visibility repair: old A hidden, new A visible
for visible_mass in np.linspace(0, 2, 21):
    A_old = np.zeros((1, 1))
    A_new = np.array([[visible_mass]])
    B = np.array([[1.0]])
    rows.append({"case": "visibility_extension", "visible_mass": visible_mass, "old_violation": float((A_old-B)[0,0]), "new_violation": float((A_new-B)[0,0])})
pd.DataFrame(rows).to_csv(OUT / "nonrepair_or_scope_repair_examples_step40.csv", index=False)

# 5. Null-mode cases
pd.DataFrame([
    {"case":"null_probe_unrepaired", "C":"diag(0,1)", "L":"[1,0]", "pseudoinverse_value":0.0, "true_variational_capacity":"infinite", "status":"failed_null_mode"},
    {"case":"lawful_quotient_removes_null", "C":"[1] on quotient", "L":"[0] on quotient", "pseudoinverse_value":0.0, "true_variational_capacity":0.0, "status":"scope_narrowing_unless_zero_displacement_absent"},
    {"case":"annihilating_probe", "C":"diag(0,1)", "L":"[0,1]", "pseudoinverse_value":1.0, "true_variational_capacity":1.0, "status":"accepted_null_legal"},
]).to_csv(OUT / "null_mode_repair_cases_step40.csv", index=False)

# Plots
char = pd.read_csv(OUT / "character_frame_repair_step40.csv")
plt.figure(figsize=(6,4))
plt.loglog(char["lambda_missing_character"], char["budget_bound"])
plt.xlabel("new missing-character source strength")
plt.ylabel("certified anti-invariant budget bound")
plt.title("Character-frame repair decreases budget only by covering missing direction")
plt.tight_layout()
plt.savefig(OUT / "character_frame_repair_step40.png", dpi=180)
plt.close()

mon = pd.read_csv(OUT / "monotone_repair_checks_step40.csv")
plt.figure(figsize=(6,4))
plt.scatter(mon["trace_old"], mon["trace_new"], s=12)
lim = [min(mon["trace_old"].min(), mon["trace_new"].min()), max(mon["trace_old"].max(), mon["trace_new"].max())]
plt.plot(lim, lim)
plt.xlabel("old obstruction trace bound")
plt.ylabel("new obstruction trace bound")
plt.title("Proof-strengthening repairs lower obstruction budget")
plt.tight_layout()
plt.savefig(OUT / "monotone_repair_trace_step40.png", dpi=180)
plt.close()

# Write a small JSON report
report = {
    "monotone_trials": len(mon),
    "min_eig_budget_decrease_min": float(mon["min_eig_budget_decrease"].min()),
    "trace_decrease_min": float(mon["trace_decrease"].min()),
    "optimized_t_max_relative_error": float(pd.read_csv(OUT / "optimized_t_checks_step40.csv")["rel_error"].max()),
    "character_repair_final_bound": float(char["budget_bound"].iloc[-1]),
}
(OUT / "step40_check_report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
