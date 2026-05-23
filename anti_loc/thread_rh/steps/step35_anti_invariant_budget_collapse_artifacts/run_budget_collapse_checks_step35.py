import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step35_budgetcollapse')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Coercive collapse scalar model C_lambda = 1 + lambda, L^- = 1, Theta0=1.
# K_lambda = 1/(1+lambda) <= 1/lambda for lambda>0.
lambdas = np.logspace(-3, 4, 120)
rows = []
for lam in lambdas:
    K = 1.0/(1.0 + lam)
    bound = 1.0/lam
    rows.append({
        'lambda': lam,
        'K_minus': K,
        'coercive_bound': bound,
        'ratio_K_to_bound': K/bound,
        'status': 'passes' if K <= bound + 1e-12 else 'fails'
    })
coercive_df = pd.DataFrame(rows)
coercive_df.to_csv(OUT/'coercive_budget_collapse_step35.csv', index=False)

plt.figure(figsize=(7,5))
plt.loglog(coercive_df['lambda'], coercive_df['K_minus'], label='actual K^-')
plt.loglog(coercive_df['lambda'], coercive_df['coercive_bound'], linestyle='--', label='1/lambda bound')
plt.xlabel('anti-invariant coercivity lambda')
plt.ylabel('anti-invariant budget')
plt.title('Coercive audit collapses anti-invariant budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'coercive_budget_collapse_step35.png', dpi=180)
plt.close()

# 2. Off-fixed mass bound for epsilon collapse. Theta trace set to 3, delta=0.1,0.25,0.5.
epsilons = np.logspace(-6, 0, 100)
deltas = [0.1, 0.25, 0.5]
trace_theta = 3.0
mass_rows = []
for eps in epsilons:
    for delta in deltas:
        mass_bound = eps * trace_theta/(delta**2)
        mass_rows.append({
            'epsilon': eps,
            'delta': delta,
            'trace_theta0': trace_theta,
            'off_fixed_mass_bound': mass_bound,
        })
mass_df = pd.DataFrame(mass_rows)
mass_df.to_csv(OUT/'offfixed_mass_collapse_bound_step35.csv', index=False)

plt.figure(figsize=(7,5))
for delta in deltas:
    sub = mass_df[mass_df['delta']==delta]
    plt.loglog(sub['epsilon'], sub['off_fixed_mass_bound'], label=f'delta={delta}')
plt.xlabel('epsilon in K^- <= epsilon Theta0')
plt.ylabel('off-fixed mass bound')
plt.title('Budget collapse forces fixed-locus confinement')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'offfixed_mass_collapse_bound_step35.png', dpi=180)
plt.close()

# 3. Symmetry no-go: anti-linear splitting with invariant block controlled but anti-invariant block not.
no_go_rows = []
for kminus in [0.01, 0.1, 1.0, 10.0, 100.0]:
    K = np.diag([0.0, kminus])
    theta_zero = np.zeros((2,2))
    theta_unit = np.diag([0.0, 1.0])
    no_go_rows.append({
        'case': 'symmetry_only',
        'K_plus': K[0,0],
        'K_minus': K[1,1],
        'invariant_zero_budget_passes': bool(K[0,0] <= 1e-12),
        'anti_invariant_zero_budget_passes': bool(K[1,1] <= 1e-12),
        'anti_invariant_unit_budget_passes': bool(K[1,1] <= 1.0 + 1e-12),
    })
no_go_df = pd.DataFrame(no_go_rows)
no_go_df.to_csv(OUT/'symmetry_only_no_collapse_step35.csv', index=False)

# 4. Finite-dimensional random check of theorem: C >= lambda L^T Theta^-1 L.
rng = np.random.default_rng(35)
rand_rows = []
for trial in range(50):
    n = 6
    m = 3
    L = rng.normal(size=(m,n))
    A = rng.normal(size=(n,n))
    R = A.T @ A + 0.5*np.eye(n)
    B = rng.normal(size=(m,m))
    Theta = B.T @ B + 0.5*np.eye(m)
    lam = 10**rng.uniform(-1,2)
    theta_inv = np.linalg.inv(Theta)
    C = R + lam * L.T @ theta_inv @ L
    K = L @ np.linalg.inv(C) @ L.T
    bound = (1.0/lam)*Theta
    eig_min_bound_minus_K = np.linalg.eigvalsh(bound-K).min()
    rand_rows.append({
        'trial': trial,
        'lambda': lam,
        'min_eig_bound_minus_K': eig_min_bound_minus_K,
        'passes': bool(eig_min_bound_minus_K >= -1e-9),
        'max_eig_relative': float(np.linalg.eigvalsh(np.linalg.solve(bound, K)).max()) if np.linalg.cond(bound) < 1e12 else np.nan
    })
rand_df = pd.DataFrame(rand_rows)
rand_df.to_csv(OUT/'random_coercive_domination_checks_step35.csv', index=False)

# 5. Schema and theorem map
schema = {
    'step': 35,
    'name': 'Anti-Invariant Budget Collapse',
    'objects': {
        'J': 'anti-linear involution; fixed locus is the symmetry line/surface',
        'Y_minus': 'anti-invariant response sector after realification',
        'L_minus_Gamma': 'declared native anti-invariant probe family on the exact package',
        'C_Gamma': 'exact packaged audit operator/form',
        'K_minus': 'L_minus_Gamma C_Gamma^dagger L_minus_Gamma^*',
        'A_Z': 'zero/root-side anti-invariant displacement matrix',
        'Theta_minus': 'accepted anti-invariant budget'
    },
    'accepted_routes': [
        'exact fixed-layer readout L_minus Gamma = 0',
        'coercive anti-invariant audit C_Gamma >= lambda L_minus^* Theta0^{-1} L_minus with lambda large or diverging',
        'explicit-formula domination A_Z <= K_minus plus K_minus <= Theta_minus'
    ],
    'nonclaims': [
        'anti-linear symmetry alone does not imply budget collapse',
        'invariant trace control does not imply anti-invariant control',
        'zero budget requires exact fixed readout or coercive audit; it cannot be assumed from RH target'
    ]
}
(OUT/'anti_invariant_budget_collapse_schema_step35.json').write_text(json.dumps(schema, indent=2))

theorem_map = pd.DataFrame([
    {'theorem':'Zero anti-invariant budget','claim':'K^- = 0 iff L^- vanishes on the legal energy quotient','use':'exact fixed-layer confinement route'},
    {'theorem':'Coercive budget bound','claim':'C >= lambda L^-* Theta0^-1 L^- implies K^- <= lambda^-1 Theta0','use':'tighter anti-invariant audit yields small budget'},
    {'theorem':'Budget collapse gives zero confinement','claim':'A_Z <= K^- <= epsilon Theta0 implies off-fixed mass <= epsilon tr(Theta0)/delta^2','use':'RH-facing zero-confinement bridge'},
    {'theorem':'Symmetry no-go','claim':'anti-linear symmetry alone allows K^- > 0','use':'blocks symmetry-only overread'},
    {'theorem':'Invariant trace no-go','claim':'invariant sector collapse does not control anti-invariant sector','use':'blocks trace-shadow overread'},
])
theorem_map.to_csv(OUT/'theorem_map_step35.csv', index=False)

status = pd.DataFrame([
    {'gate':'formed closure/exact package','status_needed':'accepted','failure':'raw substrate or unformed layer outside claim'},
    {'gate':'anti-linear involution declared','status_needed':'accepted','failure':'no fixed-locus meaning'},
    {'gate':'anti-invariant readout declared','status_needed':'accepted','failure':'hidden probe smuggling'},
    {'gate':'null-mode legality','status_needed':'accepted','failure':'infinite capacity or false zero budget'},
    {'gate':'explicit-formula domination A_Z <= K^-','status_needed':'accepted or defect-recorded','failure':'zero-side displacement not charged by carrier'},
    {'gate':'budget collapse K^- <= epsilon Theta0','status_needed':'accepted','failure':'anti-invariant displacement remains affordable'},
    {'gate':'strict-extension/coercivity growth','status_needed':'accepted if epsilon -> 0 claimed','failure':'fixed-package positivity tightening overread'},
])
status.to_csv(OUT/'budget_collapse_gate_table_step35.csv', index=False)

# Zip selected artifacts
zip_path = OUT/'step35_anti_invariant_budget_collapse_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in OUT.iterdir():
        if p.name != zip_path.name and p.is_file():
            zf.write(p, arcname=p.name)

print('Wrote artifacts to', OUT)
