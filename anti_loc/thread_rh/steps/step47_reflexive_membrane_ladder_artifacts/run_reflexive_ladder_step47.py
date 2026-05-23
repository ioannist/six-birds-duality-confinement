#!/usr/bin/env python3
"""Small sanity checks for Step 47. These are algebra checks, not Six Birds simulations."""
from pathlib import Path
import csv, math, json
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step47_reflexive_ladder')
OUT.mkdir(parents=True, exist_ok=True)

def write_csv(name, rows, fields):
    with open(OUT/name, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

# 1. Summable defect propagation.
rows=[]
K=0.20
Theta=1.0
P=1.0
upper=K
for j in range(1,101):
    eps = 0.02/(j*j)
    E = 0.003/(j*j)
    K = (1+eps)*K + E
    P *= (1+eps)
    rows.append({
        'stage':j,'epsilon':eps,'defect_E':E,'K':K,'Theta':Theta,
        'passes': K <= Theta, 'product_P':P
    })
write_csv('summable_propagation_step47.csv', rows, ['stage','epsilon','defect_E','K','Theta','passes','product_P'])

# 2. Non-summable defect failure.
rows2=[]
K=0.0
for j in range(1,401):
    E = 1.0/j
    K += E
    rows2.append({'stage':j,'defect_E':E,'K':K,'Theta':4.0,'passes':K<=4.0})
write_csv('nonsummable_failure_step47.csv', rows2, ['stage','defect_E','K','Theta','passes'])

# 3. Monotone asymptotic non-completion.
rows3=[]
for n in range(1,401):
    K=1+1/(n+1)
    rows3.append({'stage':n,'K':K,'Theta':1.0,'positive_defect':K-1.0,'complete':K<=1.0})
write_csv('monotone_noncompletion_step47.csv', rows3, ['stage','K','Theta','positive_defect','complete'])

# 4. Well-founded finite completion: number of unresolved critical pairs.
rows4=[]
mu=7
for j in range(0,8):
    rows4.append({'stage':j,'mu_unresolved_witnesses':mu,'complete':mu==0})
    if mu>0: mu-=1
write_csv('well_founded_completion_step47.csv', rows4, ['stage','mu_unresolved_witnesses','complete'])

# 5. Same-package saturation: random orthogonal relabeling preserves eigenvalues.
rng=np.random.default_rng(47)
rows5=[]
for trial in range(50):
    A=rng.normal(size=(4,4)); K=A@A.T
    Q,_=np.linalg.qr(rng.normal(size=(4,4)))
    K2=Q@K@Q.T
    err=float(np.max(np.abs(np.sort(np.linalg.eigvalsh(K))-np.sort(np.linalg.eigvalsh(K2)))))
    rows5.append({'trial':trial,'eigenvalue_error':err})
write_csv('same_package_saturation_step47.csv', rows5, ['trial','eigenvalue_error'])

# 6. All-six missing channel illustrative violation sizes.
rows6=[
 {'missing_channel':'P1 rewrite/gauge','countermodel':'hidden gauge-aligned slow mode','violation':1000.0,'downgrade':'failed_gauge_or_support_only'},
 {'missing_channel':'P2 feasibility/channel','countermodel':'ill-conditioned cancellation pair','violation':100.0,'downgrade':'failed_feasibility'},
 {'missing_channel':'P3 route/holonomy','countermodel':'route-local duplicated protocol','violation':2.0,'downgrade':'local_only'},
 {'missing_channel':'P4 staging/refinement','countermodel':'future predictive needle K_j=j','violation':50.0,'downgrade':'current_only'},
 {'missing_channel':'P5 packaging/canonicalization','countermodel':'public shadow hides carrier needle','violation':25.5,'downgrade':'overread'},
 {'missing_channel':'P6 audit/currency','countermodel':'diagonal-only recombination witness','violation':10.0,'downgrade':'failed_audit'},
]
write_csv('all_six_ladder_countermodels_step47.csv', rows6, ['missing_channel','countermodel','violation','downgrade'])

# Plots.
plt.figure()
plt.plot([r['stage'] for r in rows],[r['K'] for r in rows], label='K_j')
plt.axhline(Theta, linestyle='--', label='Theta')
plt.xlabel('stage'); plt.ylabel('currency'); plt.title('Summable defects preserve membrane')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'summable_propagation_step47.png', dpi=180); plt.close()

plt.figure()
plt.plot([r['stage'] for r in rows2],[r['K'] for r in rows2], label='K_j')
plt.axhline(4.0, linestyle='--', label='Theta=4')
plt.xlabel('stage'); plt.ylabel('currency'); plt.title('Non-summable defects eventually break budget')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'nonsummable_failure_step47.png', dpi=180); plt.close()

plt.figure()
plt.plot([r['stage'] for r in rows3],[r['positive_defect'] for r in rows3])
plt.xlabel('stage'); plt.ylabel('positive defect')
plt.title('Monotone improvement without finite completion')
plt.tight_layout(); plt.savefig(OUT/'monotone_noncompletion_step47.png', dpi=180); plt.close()

plt.figure()
plt.step([r['stage'] for r in rows4],[r['mu_unresolved_witnesses'] for r in rows4], where='post')
plt.xlabel('stage'); plt.ylabel('unresolved witnesses')
plt.title('Well-founded finite completion')
plt.tight_layout(); plt.savefig(OUT/'well_founded_completion_step47.png', dpi=180); plt.close()

print(json.dumps({
    'summable_final_K': rows[-1]['K'],
    'nonsummable_final_K': rows2[-1]['K'],
    'monotone_defect_stage_400': rows3[-1]['positive_defect'],
    'max_same_package_eig_error': max(r['eigenvalue_error'] for r in rows5),
}, indent=2))
