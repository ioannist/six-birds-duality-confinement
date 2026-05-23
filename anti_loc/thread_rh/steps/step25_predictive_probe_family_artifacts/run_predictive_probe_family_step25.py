"""Small mathematical countermodels for Step 25.
These are not Six Birds simulations. They only visualize finite-matrix theorems.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step25_predictive_family')
OUT.mkdir(parents=True, exist_ok=True)

# Countermodel 1: growing recombination family K_m = 1_m 1_m^T.
rows = []
for m in range(1, 101):
    diag_cap = 1.0
    normalized_all_ones_cap = float(m)
    op_norm = float(m)
    rows.append({
        'm': m,
        'coordinate_capacity': diag_cap,
        'normalized_all_ones_recombination_capacity': normalized_all_ones_cap,
        'operator_norm': op_norm,
    })
with open(OUT/'predictive_recombination_growth_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

plt.figure(figsize=(7,4.5))
plt.plot([r['m'] for r in rows], [r['coordinate_capacity'] for r in rows], label='coordinate capacity')
plt.plot([r['m'] for r in rows], [r['normalized_all_ones_recombination_capacity'] for r in rows], label='all-ones recombination capacity')
plt.xlabel('probe-family size m')
plt.ylabel('capacity')
plt.title('Branchwise bounds do not control predictive recombination')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_recombination_growth_step25.png', dpi=180)
plt.close()

# Countermodel 2: current equivalence, future divergence K_n=diag(1,n).
rows2 = []
for n in range(0,101):
    if n == 0:
        k1 = 1.0; k2 = 1.0
    else:
        k1 = 1.0; k2 = float(n)
    rows2.append({'n': n, 'capacity_e1': k1, 'capacity_e2': k2, 'ratio_e2_over_e1': k2/k1})
with open(OUT/'current_vs_predictive_quotient_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows2[0].keys()))
    writer.writeheader(); writer.writerows(rows2)

plt.figure(figsize=(7,4.5))
plt.plot([r['n'] for r in rows2], [r['capacity_e1'] for r in rows2], label='e1 capacity')
plt.plot([r['n'] for r in rows2], [r['capacity_e2'] for r in rows2], label='e2 capacity')
plt.xlabel('refinement level n')
plt.ylabel('capacity')
plt.title('Current-equivalent probes can become predictively distinct')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'current_vs_predictive_quotient_step25.png', dpi=180)
plt.close()

# Defect propagation example: K_{n+1} <= (1+eps_n)K_n + D_n.
# Use scalar matrices, eps_n = 0.05/(n+1)^2, D_n = 0.2/(n+1)^2.
rows3=[]
K=1.0
prod=1.0
sumD=0.0
Pinf_approx=math.prod([1+0.05/(r+1)**2 for r in range(20000)])
Dinf_approx=sum(0.2/(r+1)**2 for r in range(20000))
Theta=Pinf_approx*(1.0+Dinf_approx)
for n in range(0,200):
    if n>0:
        eps=0.05/(n)**2
        D=0.2/(n)**2
        K=(1+eps)*K+D
    rows3.append({'n':n,'K_n':K,'Theta_bound':Theta,'ratio_K_over_Theta':K/Theta})
with open(OUT/'summable_defect_propagation_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows3[0].keys()))
    writer.writeheader(); writer.writerows(rows3)

plt.figure(figsize=(7,4.5))
plt.plot([r['n'] for r in rows3], [r['K_n'] for r in rows3], label='propagated K_n')
plt.plot([r['n'] for r in rows3], [r['Theta_bound'] for r in rows3], label='uniform predictive bound', linestyle='--')
plt.xlabel('refinement level n')
plt.ylabel('capacity/currency')
plt.title('Summable defects give a predictive budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'summable_defect_propagation_step25.png', dpi=180)
plt.close()

# Non-summable defect example for contrast.
rows4=[]
K=1.0
for n in range(1,201):
    D=0.1/n
    K=K+D
    rows4.append({'n':n,'K_n':K,'defect_D_n':D})
with open(OUT/'nonsummable_defect_failure_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(rows4[0].keys()))
    writer.writeheader(); writer.writerows(rows4)

plt.figure(figsize=(7,4.5))
plt.plot([r['n'] for r in rows4], [r['K_n'] for r in rows4], label='K_n with non-summable defects')
plt.xlabel('refinement level n')
plt.ylabel('capacity/currency')
plt.title('Non-summable defects prevent a uniform predictive budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'nonsummable_defect_failure_step25.png', dpi=180)
plt.close()

# Theorem map and gate tables.
theorem_rows = [
    {'item':'Predictive family currency','claim':'Khat_j = R_j L_j Gamma_j C_j^dagger Gamma_j^* L_j^* R_j^*','status':'proved'},
    {'item':'Predictive anti-localization equivalence','claim':'Khat_j <= Theta for all j iff all transported recombinations have forward capacity <= Theta','status':'proved'},
    {'item':'Summable defect propagation','claim':'K_{j+1} <= (1+eps_j)K_j + D_j with summable eps,D gives uniform Theta','status':'proved'},
    {'item':'Commuting canonical budget','claim':'If all K_j commute, least diagonal predictive budget is coordinatewise sup','status':'proved'},
    {'item':'Current vs predictive quotient','claim':'Current equivalence need not persist under refinement','status':'countermodel'},
    {'item':'Predictive recombination needle','claim':'Branchwise bounds do not control growing recombinations','status':'countermodel'},
]
with open(OUT/'theorem_map_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(theorem_rows[0].keys()))
    writer.writeheader(); writer.writerows(theorem_rows)

gate_rows = [
    {'gate':'formed_closure','requirement':'exact packaged carrier at every accepted level','failure_status':'outside_scope'},
    {'gate':'native_family','requirement':'declared L_j and response transports R_j','failure_status':'undeclared_probe_family'},
    {'gate':'null_mode_legality','requirement':'Ran(L_j Gamma_j)^* subset Ran(C_Gamma,j)','failure_status':'infinite_capacity'},
    {'gate':'matrix_budget','requirement':'Khat_j <= Theta for all j, not just diagonals','failure_status':'recombination_needle'},
    {'gate':'defect_ledger','requirement':'summable Loewner defects or accepted uniform envelope','failure_status':'predictive_failure'},
    {'gate':'scope','requirement':'claim restricted to formed closures and native probes','failure_status':'overread'},
]
with open(OUT/'predictive_gate_table_step25.csv','w',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(gate_rows[0].keys()))
    writer.writeheader(); writer.writerows(gate_rows)

print('Step 25 countermodel artifacts written to', OUT)
