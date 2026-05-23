"""Small PSD sanity checks for Step 39 obstruction alternatives.
These are algebraic checks only, not Six Birds simulations.
"""
import csv
import numpy as np
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step39_obstruction')


def maxeig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[-1])

def mineig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[0])

def witness(A):
    vals, vecs = np.linalg.eigh((A + A.T)/2)
    i = int(np.argmax(vals))
    return float(vals[i]), vecs[:, i]

cases = []

# Case 1: EF domination failure, budget passes
AZ = np.diag([3.0, 0.5])
K = np.diag([1.0, 0.5])
EEF = 0.1*np.eye(2)
Theta = np.eye(2)
Esrc = np.zeros((2,2))
Lam = 1.0
t = 1.0
D_EF = AZ - (1+t)*K - (1+1/t)*EEF
D_B = K - (1/Lam)*Theta - Esrc
lam, y = witness(D_EF)
cases.append({
    'case':'EF_domination_failure',
    'maxeig_D_EF':lam,
    'maxeig_D_budget':maxeig(D_B),
    'obstruction':'failed_explicit_formula_domination',
    'witness_vector':np.array2string(y, precision=4)
})

# Case 2: budget failure, EF passes for selected AZ
K = np.diag([2.0, 0.4])
AZ = K.copy()
EEF = np.zeros((2,2))
Theta = np.eye(2)
Esrc = np.zeros((2,2))
Lam = 1.0
t = 0.5
D_EF = AZ - (1+t)*K - (1+1/t)*EEF
D_B = K - (1/Lam)*Theta - Esrc
lam, y = witness(D_B)
cases.append({
    'case':'budget_failure',
    'maxeig_D_EF':maxeig(D_EF),
    'maxeig_D_budget':lam,
    'obstruction':'failed_anti_invariant_budget',
    'witness_vector':np.array2string(y, precision=4)
})

# Case 3: trace shadow passes, Loewner fails
AZ = np.diag([2.0, 0.25])
K = np.diag([0.25, 2.0])
D = AZ - K
lam, y = witness(D)
cases.append({
    'case':'trace_shadow_overread',
    'maxeig_D_EF':lam,
    'maxeig_D_budget':0.0,
    'obstruction':'overread_trace_equal_not_loewner',
    'witness_vector':np.array2string(y, precision=4)
})

# Case 4: uncovered character direction
Q1 = np.array([[1.0, 0.0]])
Q2 = np.array([[1.0, 0.0]])
F = Q1.T@Q1 + Q2.T@Q2
Theta_inv = np.eye(2)
Dframe = F - 0.5*Theta_inv
# Negative eigenvector of Dframe -> uncovered relative to target lower bound
vals, vecs = np.linalg.eigh(Dframe)
idx = int(np.argmin(vals))
cases.append({
    'case':'uncovered_character',
    'maxeig_D_EF':0.0,
    'maxeig_D_budget':0.0,
    'obstruction':'uncovered_character_direction',
    'witness_vector':np.array2string(vecs[:, idx], precision=4)
})

# Case 5: finite source exact confinement failure
for Lam in [1, 2, 5, 10, 100]:
    B = (1/Lam)*np.eye(2)
    eps = 0.5
    bound = (1/eps**2)*np.trace(B)
    cases.append({
        'case':f'finite_source_bound_Lambda_{Lam}',
        'maxeig_D_EF':0.0,
        'maxeig_D_budget':0.0,
        'obstruction':f'finite_bound_offfixed_mass_bound_{bound:.6g}',
        'witness_vector':'NA'
    })

with open(OUT/'obstruction_case_checks_step39.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['case','maxeig_D_EF','maxeig_D_budget','obstruction','witness_vector'])
    writer.writeheader()
    writer.writerows(cases)

print('wrote', OUT/'obstruction_case_checks_step39.csv')
