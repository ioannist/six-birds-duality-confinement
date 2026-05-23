
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent

def psd_sqrt_inv(mat, tol=1e-10):
    vals, vecs = np.linalg.eigh(mat)
    inv = np.zeros_like(vals)
    for i,v in enumerate(vals):
        if v > tol:
            inv[i] = 1.0/np.sqrt(v)
    return (vecs * inv) @ vecs.T

def pinv_psd(mat, tol=1e-10):
    vals, vecs = np.linalg.eigh(mat)
    inv = np.array([1/v if v>tol else 0 for v in vals])
    return (vecs * inv) @ vecs.T

def eigmax(mat):
    return float(np.linalg.eigvalsh((mat+mat.T)/2).max())

def eigmin(mat):
    return float(np.linalg.eigvalsh((mat+mat.T)/2).min())

rows = []

# Hidden blind spot: L sees x1, D sees M x2.
Ms = np.logspace(0, 4, 30)
for M in Ms:
    C = np.eye(2)
    L = np.array([[1.0, 0.0]])
    D = np.array([[0.0, M]])
    K_L = L @ np.linalg.inv(C) @ L.T
    K_D = D @ np.linalg.inv(C) @ D.T
    rows.append({
        "case": "hidden_blind_spot",
        "parameter": M,
        "native_capacity": float(K_L[0,0]),
        "dissolving_capacity": float(K_D[0,0]),
        "adequacy": False,
        "notes": "Lv=0 but Dv !=0 for v=e2"
    })

pd.DataFrame(rows).to_csv(BASE/"hidden_blind_spot_step48.csv", index=False)

# Defective adequacy exact algebra checks
rng = np.random.default_rng(48)
defect_rows=[]
for trial in range(80):
    n=5; y=3; z=2
    A0 = rng.normal(size=(n,n))
    C = A0.T@A0 + 0.5*np.eye(n)
    L = rng.normal(size=(y,n))
    A = rng.normal(size=(z,y))
    R = 0.1*rng.normal(size=(z,n))
    D = A@L + R
    Cinv = np.linalg.inv(C)
    K_L = L@Cinv@L.T
    K_R = R@Cinv@R.T
    K_D = D@Cinv@D.T
    t=1.0
    Bound = (1+t)*A@K_L@A.T + (1+1/t)*K_R
    defect_rows.append({
        "trial": trial,
        "min_eig_bound_minus_KD": eigmin(Bound-K_D),
        "max_eig_KD": eigmax(K_D),
        "max_eig_bound": eigmax(Bound)
    })
pd.DataFrame(defect_rows).to_csv(BASE/"defective_adequacy_checks_step48.csv", index=False)

# Exact adequacy checks
exact_rows=[]
for trial in range(80):
    n=6; y=4; z=3
    A0 = rng.normal(size=(n,n))
    C = A0.T@A0 + 0.5*np.eye(n)
    L = rng.normal(size=(y,n))
    A = rng.normal(size=(z,y))
    D = A@L
    Cinv=np.linalg.inv(C)
    K_L=L@Cinv@L.T
    K_D=D@Cinv@D.T
    K_exact=A@K_L@A.T
    exact_rows.append({
        "trial": trial,
        "operator_error": float(np.linalg.norm(K_D-K_exact, ord=2)),
        "max_eig_KD": eigmax(K_D)
    })
pd.DataFrame(exact_rows).to_csv(BASE/"exact_adequacy_checks_step48.csv", index=False)

# Null-mode fake zero
C = np.diag([1.0,0.0])
Cdag = np.diag([1.0,0.0])
L = np.array([[1.0,0.0]])
D = np.array([[0.0,1.0]])
pd.DataFrame([{
    "case":"null_mode_fake_zero",
    "native_pseudoinverse_capacity": float((L@Cdag@L.T)[0,0]),
    "dissolving_pseudoinverse_value": float((D@Cdag@D.T)[0,0]),
    "true_variational_dissolving_capacity": "infinite",
    "reason": "D sees e2 in ker C"
}]).to_csv(BASE/"null_mode_fake_zero_step48.csv", index=False)

# plots
df=pd.read_csv(BASE/"hidden_blind_spot_step48.csv")
plt.figure(figsize=(6,4))
plt.loglog(df["parameter"], df["dissolving_capacity"], label="dissolving capacity")
plt.loglog(df["parameter"], df["native_capacity"], label="native capacity")
plt.xlabel("hidden readout scale M")
plt.ylabel("capacity")
plt.title("Native membrane can miss hidden dissolving capacity")
plt.legend()
plt.tight_layout()
plt.savefig(BASE/"hidden_blind_spot_step48.png", dpi=160)
plt.close()

df2=pd.read_csv(BASE/"defective_adequacy_checks_step48.csv")
plt.figure(figsize=(6,4))
plt.plot(df2["trial"], df2["min_eig_bound_minus_KD"], marker="o", markersize=3, linestyle="")
plt.axhline(0, color="black", linewidth=1)
plt.xlabel("trial")
plt.ylabel("min eig(bound - K_D)")
plt.title("Defective adequacy bound checks")
plt.tight_layout()
plt.savefig(BASE/"defective_adequacy_bound_step48.png", dpi=160)
plt.close()

print("wrote step 48 checks")
