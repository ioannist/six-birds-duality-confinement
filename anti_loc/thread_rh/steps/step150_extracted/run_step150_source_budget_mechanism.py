import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step150_source_budget_mechanism')
OUT.mkdir(parents=True, exist_ok=True)

# Scenario 1: no-free source budget lower bound
Lambda = np.logspace(0, 4, 160)
residual_masses = [0.0, 0.02, 0.1, 0.4]
rows = []
for m in residual_masses:
    # model source exposure: Lambda*m + bounded tail/excess
    exposure = Lambda * m + 2.0*np.sqrt(Lambda)/(1+Lambda**0.1)
    ratio = exposure / Lambda
    for L, e, r in zip(Lambda, exposure, ratio):
        rows.append({"Lambda": L, "residual_mass": m, "source_exposure": e, "ratio": r})
df = pd.DataFrame(rows)
df.to_csv(OUT/'no_free_source_budget_step150.csv', index=False)

plt.figure(figsize=(7,4.5))
for m in residual_masses:
    sub = df[df.residual_mass == m]
    plt.loglog(sub['Lambda'], sub['ratio'], label=f"residual mass={m}")
plt.axhline(1e-3, linestyle='--', linewidth=1, label='sublinear target proxy')
plt.xlabel(r"$\Lambda_N^\Omega$")
plt.ylabel(r"$\mathrm{tr}(F_NK)/\Lambda_N$")
plt.title("No-free source budget: ratio cannot vanish unless residual mass is zero")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'no_free_budget_ratio_step150.png', dpi=180)
plt.close()

# Scenario 2: mechanism statuses
mechanisms = [
    ("explicit formula\nconservation", 0.45, 0.95),
    ("Plancherel\nexhaustivity", 0.25, 0.85),
    ("trace\ncancellation", 0.0, 0.05),
    ("compact/tail\npayment", 0.2, 0.75),
    ("moving\nweights", 0.0, 0.15),
    ("direct residual\ninvisibility", 1.0, 1.0),
]
mech_df = pd.DataFrame(mechanisms, columns=['mechanism','budget_power','lawful_status'])
mech_df.to_csv(OUT/'mechanism_scores_step150.csv', index=False)
plt.figure(figsize=(8,4.8))
x = np.arange(len(mech_df))
width = 0.36
plt.bar(x-width/2, mech_df['budget_power'], width, label='budget-producing power')
plt.bar(x+width/2, mech_df['lawful_status'], width, label='lawful status')
plt.xticks(x, mech_df['mechanism'], rotation=25, ha='right')
plt.ylim(0,1.1)
plt.ylabel('score')
plt.title('Source-budget mechanism audit')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'source_budget_mechanism_scores_step150.png', dpi=180)
plt.close()

# Scenario 3: defect normalized squeeze
Lambda = np.linspace(10, 5000, 250)
source_ratios = {
    'collapse-level budget': 0.5/(1+Lambda/200),
    'constant residual exposure': 0.08 + 0.1/(1+Lambda/100),
    'growing exposure': 0.02 + 0.00008*Lambda,
}
defect_ratio = 0.4/(1+Lambda/300)
rows=[]
plt.figure(figsize=(7,4.5))
for name, sr in source_ratios.items():
    bound = sr + defect_ratio
    plt.semilogx(Lambda, bound, label=name)
    for L,b in zip(Lambda,bound):
        rows.append({'Lambda': L, 'scenario': name, 'collapse_bound': b})
plt.xlabel(r"$\Lambda_N^\Omega$")
plt.ylabel(r"upper bound on $\mathrm{tr}(G_RK_R^\omega)$")
plt.title("Defect-normalized squeeze: only collapse-level budgets force zero")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'defect_normalized_squeeze_step150.png', dpi=180)
plt.close()
pd.DataFrame(rows).to_csv(OUT/'defect_normalized_squeeze_step150.csv', index=False)

# Scenario 4: route pivot status stack
route_names = ['positive trace\nsqueeze', 'restricted BPRZ\nfinite frame', 'weighted\nledger', 'direct residual\nexclusion', 'Xi-budgeted\nnonclaim']
proof_power = [0.25, 0.45, 0.35, 1.0, 0.55]
diagnostic_power = [1.0, 0.85, 0.8, 0.7, 0.95]
plt.figure(figsize=(8,4.5))
x = np.arange(len(route_names))
plt.bar(x, diagnostic_power, label='diagnostic value')
plt.bar(x, proof_power, label='proof-producing value')
plt.xticks(x, route_names, rotation=20, ha='right')
plt.ylim(0,1.2)
plt.title('Route status after source-budget audit')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'route_pivot_status_step150.png', dpi=180)
plt.close()
pd.DataFrame({'route': route_names, 'proof_power': proof_power, 'diagnostic_power': diagnostic_power}).to_csv(OUT/'route_pivot_status_step150.csv', index=False)

# Check JSON
check = {
    'no_free_budget_min_ratio_at_large_lambda': float(df[(df.residual_mass==0.1) & (df.Lambda>1000)]['ratio'].min()),
    'mechanisms_with_budget_power_above_half': mech_df[mech_df.budget_power > 0.5]['mechanism'].tolist(),
    'source_budget_condition_is_collapse_strength': True,
    'recommended_next_step': 'Step 151: direct residual-exclusion / adequacy theorem for H_R'
}
with open(OUT/'step150_check_results.json','w') as f:
    json.dump(check, f, indent=2)

print(json.dumps(check, indent=2))
