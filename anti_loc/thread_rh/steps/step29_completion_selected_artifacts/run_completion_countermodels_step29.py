#!/usr/bin/env python3
"""
Step 29 local checks for anti-localization completion.
These are not Six Birds simulations. They are finite examples illustrating
completion theorems: budget repair, nonterminating monotone defects, cycles,
and rank-one audit updates.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step29_completion')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Monotone but nonterminating defects K_n = 1 + 1/n, Theta = 1
rows = []
for n in range(1, 101):
    K = 1 + 1/n
    theta = 1.0
    defect = K - theta
    rows.append({'n': n, 'K': K, 'Theta': theta, 'defect': defect, 'complete': defect <= 0})
pd.DataFrame(rows).to_csv(OUT / 'monotone_nonterminating_defect_step29.csv', index=False)

plt.figure(figsize=(6,4))
plt.plot([r['n'] for r in rows], [r['defect'] for r in rows], marker='o', markersize=2)
plt.xlabel('completion step n')
plt.ylabel('positive defect 1/n')
plt.title('Monotone defect can converge without terminating')
plt.tight_layout()
plt.savefig(OUT / 'monotone_nonterminating_defect_step29.png', dpi=180)
plt.close()

# 2. Cycle example DA <-> DB
cycle_rows = []
D_A = np.diag([1.0, -1.0])
D_B = np.diag([-1.0, 1.0])
for step in range(12):
    D = D_A if step % 2 == 0 else D_B
    vals, vecs = np.linalg.eigh(D)
    y = vecs[:, -1]
    cycle_rows.append({
        'step': step,
        'state': 'A' if step % 2 == 0 else 'B',
        'lambda_max_defect': vals[-1],
        'witness_y0': y[0],
        'witness_y1': y[1],
        'complete': vals[-1] <= 0
    })
pd.DataFrame(cycle_rows).to_csv(OUT / 'two_witness_cycle_step29.csv', index=False)

# 3. Budget completion example for random PSD K and Theta = I
rng = np.random.default_rng(2929)
A = rng.normal(size=(5,5))
K = A @ A.T
Theta = np.eye(5) * np.trace(K) / 8.0  # intentionally too small
D = K - Theta
vals, U = np.linalg.eigh(D)
Dplus = U @ np.diag(np.maximum(vals, 0)) @ U.T
Theta_prime = Theta + Dplus
post = K - Theta_prime
budget_rows = []
for name, mat in [('K', K), ('Theta', Theta), ('D', D), ('D_plus', Dplus), ('Theta_prime', Theta_prime), ('K_minus_Theta_prime', post)]:
    ev = np.linalg.eigvalsh((mat + mat.T)/2)
    budget_rows.append({
        'matrix': name,
        'min_eig': ev.min(),
        'max_eig': ev.max(),
        'trace': np.trace(mat),
        'fro_norm': np.linalg.norm(mat, 'fro')
    })
pd.DataFrame(budget_rows).to_csv(OUT / 'budget_completion_spectral_summary_step29.csv', index=False)

# 4. Rank-one audit update: K(mu) = L(C+mu rr^T)^-1 L^T
m = 4
n = 6
B = rng.normal(size=(n,n))
C = B.T @ B + np.eye(n) * 0.5
L = rng.normal(size=(m,n))
r = rng.normal(size=(n,1))
mu_values = np.logspace(-3, 3, 80)
rank_rows = []
for mu in mu_values:
    Cp = C + mu * (r @ r.T)
    Kp = L @ np.linalg.inv(Cp) @ L.T
    ev = np.linalg.eigvalsh((Kp + Kp.T)/2)
    rank_rows.append({'mu': mu, 'lambda_max_K': ev[-1], 'trace_K': np.trace(Kp), 'min_eig_K': ev[0]})
pd.DataFrame(rank_rows).to_csv(OUT / 'rank_one_audit_update_step29.csv', index=False)

plt.figure(figsize=(6,4))
plt.loglog([r['mu'] for r in rank_rows], [r['lambda_max_K'] for r in rank_rows], marker='o', markersize=2)
plt.xlabel('rank-one audit strength mu')
plt.ylabel('largest currency eigenvalue')
plt.title('Audit strengthening lowers capacity')
plt.tight_layout()
plt.savefig(OUT / 'rank_one_audit_update_step29.png', dpi=180)
plt.close()

# 5. Completion move and theorem tables
completion_moves = [
    {'move':'exclusion_nonclaim','changes':'Y or native family', 'effect':'narrows claim', 'terminates_one_witness':'yes', 'claim_strength':'weaker scope', 'risk':'overclaim if nonclaim omitted'},
    {'move':'budget_repair','changes':'Theta increases', 'effect':'prices witness', 'terminates_one_witness':'yes', 'claim_strength':'weaker budget', 'risk':'vacuous anti-loc if budget inflated'},
    {'move':'audit_carrier_repair','changes':'C or exact carrier strengthened', 'effect':'lowers K by Loewner monotonicity', 'terminates_one_witness':'maybe', 'claim_strength':'preserves or strengthens if lawful', 'risk':'can open new witnesses'},
    {'move':'package_family_completion','changes':'L/protocol/transport family completed', 'effect':'exposes hidden recombinations', 'terminates_one_witness':'no', 'claim_strength':'stronger test', 'risk':'reveals failure; not a repair by itself'},
    {'move':'status_downgrade','changes':'status only', 'effect':'prevents false acceptance', 'terminates_one_witness':'yes by refusing claim', 'claim_strength':'no accepted claim', 'risk':'none if honest'}
]
pd.DataFrame(completion_moves).to_csv(OUT / 'completion_moves_step29.csv', index=False)

theorems = [
    {'id':'T29.1','name':'Witness completeness','statement':'K <= Theta iff every native recombination is within budget','status':'proved'},
    {'id':'T29.2','name':'Monotone audit strengthening','statement':'Cprime >= C implies Kprime <= K on legal quotient','status':'proved'},
    {'id':'T29.3','name':'Trivial budget completion','statement':'Theta + (K-Theta)_+ completes in one step','status':'proved but weakens claim'},
    {'id':'T29.4','name':'Termination under well-founded descent','statement':'strict descent in well-founded order implies finite termination','status':'proved'},
    {'id':'T29.5','name':'No monotone-only termination','statement':'weak/real monotonicity does not imply finite completion','status':'proved by countermodel'},
    {'id':'T29.6','name':'Termination + local confluence','statement':'terminating locally confluent completion has unique normal forms','status':'proved abstractly'},
    {'id':'T29.7','name':'Rank-one audit update','statement':'C+mu rr* subtracts PSD term from K','status':'proved'}
]
pd.DataFrame(theorems).to_csv(OUT / 'theorem_map_step29.csv', index=False)

schema = {
    'step':'29',
    'object':'AntiLocalizationCompletionState',
    'fields':['E','H','Gamma','C','L','Theta','status_sigma','currency_K','defect_D','witness_set','completion_log'],
    'witness_condition':'y^*(K-Theta)y > 0',
    'terminal_acceptance':'K <= Theta plus all exclusions recorded as nonclaims',
    'lawful_moves':['exclusion_nonclaim','budget_repair','audit_carrier_repair','package_family_completion','status_downgrade'],
    'termination_obligation':'well_founded_descent_measure or finite explicit budget repair',
    'nonclaims':['no general termination without descent','budget completion weakens claim','carrier repair may open new witnesses','nonclosed artifacts are outside no-needle theorem']
}
(OUT / 'completion_schema_step29.json').write_text(json.dumps(schema, indent=2))

print('Step 29 artifacts written to', OUT)
