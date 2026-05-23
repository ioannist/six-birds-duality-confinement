
import numpy as np
from pathlib import Path

def rand_spd(n, eps=0.5, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n,n))
    return A.T @ A + eps*np.eye(n)

def min_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

rng = np.random.default_rng(116)
out = Path(__file__).resolve().parent
n=12
Theta_inv = rand_spd(n, eps=1.0, seed=1)
C=2.5
# Xi <= C Theta_inv by construction
S = rand_spd(n, eps=0.1, seed=2)
scale = np.linalg.eigvalsh(np.linalg.solve(Theta_inv, S)).max()
Xi = C * Theta_inv * 0.5 + 0.1 * S / (scale+1)
# check residual absorption for several Lambdas
rows=[['Lambda','min_eig_source_minus_lower','min_eig_absorption_slack']]
for Lam in [1,2,4,8,16,32,64]:
    PSD = rand_spd(n, eps=0.0, seed=Lam)
    F = Lam*Theta_inv + PSD
    # Xi <= C/Lambda F should hold if Xi <= C Theta_inv and F >= Lambda Theta_inv; our Xi <= ~C Theta_inv.
    slack = (C/Lam)*F - Xi
    rows.append([Lam, min_eig(F - Lam*Theta_inv), min_eig(slack)])
with open(out/'residual_absorption_checks_step116.csv','w') as f:
    for r in rows:
        f.write(','.join(map(str,r))+'\n')
print(rows[-1])
