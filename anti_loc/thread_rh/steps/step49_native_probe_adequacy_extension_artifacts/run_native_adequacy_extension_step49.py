import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step49_adequacy_extension')
OUT.mkdir(parents=True, exist_ok=True)

def pinv_psd(C, tol=1e-12):
    w, V = np.linalg.eigh((C + C.T)/2)
    wi = np.array([1/x if x > tol else 0.0 for x in w])
    return (V * wi) @ V.T

def currency(L, C):
    return L @ pinv_psd(C) @ L.T

def maxeig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).max())

def mineig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

def psd_sqrt(A):
    w, V = np.linalg.eigh((A + A.T)/2)
    return (V * np.sqrt(np.maximum(w,0))) @ V.T

rng = np.random.default_rng(4917)

# 1. Exact adequacy checks D = A L => K_D = A K_L A^T
rows = []
for trial in range(80):
    n = rng.integers(3, 8)
    ydim = rng.integers(2, min(5,n)+1)
    zdim = rng.integers(2, 6)
    X = rng.normal(size=(n,n))
    C = X.T@X + 0.5*np.eye(n)
    L = rng.normal(size=(ydim,n))
    A = rng.normal(size=(zdim,ydim))
    D = A @ L
    KL = currency(L,C)
    KD = currency(D,C)
    target = A@KL@A.T
    err = np.linalg.norm(KD-target, ord=2)
    rows.append(dict(trial=trial,n=n,ydim=ydim,zdim=zdim,op_error=err,max_abs=float(np.max(np.abs(KD-target)))))
pd.DataFrame(rows).to_csv(OUT/'exact_adequacy_extension_checks_step49.csv', index=False)

# 2. Defective adequacy bound KD <= (1+t) A KL A^T + (1+t^-1) Xi
rows = []
for trial in range(80):
    n = rng.integers(4, 9)
    ydim = rng.integers(2, min(5,n)+1)
    zdim = rng.integers(2, 6)
    X = rng.normal(size=(n,n))
    C = X.T@X + np.eye(n)
    L = rng.normal(size=(ydim,n))
    A = rng.normal(size=(zdim,ydim))
    R = 0.15 * rng.normal(size=(zdim,n))
    D = A@L + R
    KL = currency(L,C)
    KD = currency(D,C)
    Xi = currency(R,C)
    # choose t from trace optimum-ish
    a = np.trace(A@KL@A.T)
    b = np.trace(Xi)
    t = np.sqrt(b/a) if a>1e-12 and b>1e-12 else 1.0
    Bound = (1+t)*A@KL@A.T + (1+1/t)*Xi
    rows.append(dict(trial=trial,n=n,ydim=ydim,zdim=zdim,t=t,
                     min_eig_bound_minus_KD=mineig(Bound-KD),
                     trace_KD=float(np.trace(KD)), trace_bound=float(np.trace(Bound)),
                     ratio=float(np.trace(KD)/np.trace(Bound)) if np.trace(Bound)>0 else np.nan))
pd.DataFrame(rows).to_csv(OUT/'defective_adequacy_extension_checks_step49.csv', index=False)

# 3. Hidden blind spot growth
rows=[]
for M in np.logspace(0,5,80):
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,M]])
    KL=currency(L,C)
    KD=currency(D,C)
    rows.append(dict(M=M, native_capacity=float(KL[0,0]), dissolving_capacity=float(KD[0,0])))
df_blind=pd.DataFrame(rows)
df_blind.to_csv(OUT/'strict_extension_blind_spot_growth_step49.csv', index=False)
plt.figure(figsize=(6,4))
plt.loglog(df_blind['M'], df_blind['native_capacity'], label='native capacity')
plt.loglog(df_blind['M'], df_blind['dissolving_capacity'], label='dissolving blind-spot capacity')
plt.xlabel('blind-spot amplification M')
plt.ylabel('capacity')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'strict_extension_blind_spot_growth_step49.png', dpi=160)
plt.close()

# 4. Residual contraction ladder: Xi_{j+1}=q Xi_j + g_j with decaying g
rows=[]
q=0.65
xi=1.0
for j in range(80):
    g=0.03/(j+1)**2
    rows.append(dict(j=j, residual_budget=xi, source_increment=g))
    xi=q*xi+g
df_con=pd.DataFrame(rows)
df_con.to_csv(OUT/'adequacy_residual_contraction_step49.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(df_con['j'], df_con['residual_budget'])
plt.xlabel('stage j')
plt.ylabel('adequacy residual budget')
plt.tight_layout()
plt.savefig(OUT/'adequacy_residual_contraction_step49.png', dpi=160)
plt.close()

# 5. Nonsummable residual failure: Xi_j harmonic growth
rows=[]
xi=0.0
for j in range(1,201):
    xi += 1/j
    rows.append(dict(j=j, residual_budget=xi))
df_non=pd.DataFrame(rows)
df_non.to_csv(OUT/'nonsummable_adequacy_residual_failure_step49.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(df_non['j'], df_non['residual_budget'])
plt.xlabel('stage j')
plt.ylabel('residual budget')
plt.tight_layout()
plt.savefig(OUT/'nonsummable_adequacy_residual_failure_step49.png', dpi=160)
plt.close()

# 6. Null-mode fake zero: pseudoinverse says zero but variational capacity infinite
rows=[]
for eps in [0.0, 1e-8, 1e-6, 1e-4, 1e-2, 1.0]:
    C=np.diag([eps,1.0])
    D=np.array([[1.0,0.0]])
    pseudo=currency(D,C)[0,0]
    true='infinite' if eps == 0.0 else 1/eps
    rows.append(dict(epsilon=eps,pseudoinverse_expression=pseudo,true_variational_capacity=true))
pd.DataFrame(rows).to_csv(OUT/'null_mode_adequacy_extension_failure_step49.csv', index=False)

# 7. Dissolving budget traces under defective adequacy with t optimized for trace
rows=[]
Omega=np.eye(2)
Xi0_base=np.diag([1.0, 0.2])
for scale in np.logspace(-4,2,100):
    Xi=scale*Xi0_base
    a=np.trace(Omega); b=np.trace(Xi)
    t=np.sqrt(b/a)
    bound=(1+t)*Omega + (1+1/t)*Xi
    rows.append(dict(residual_scale=scale,t=t,trace_budget=float(np.trace(bound)),max_eig_budget=maxeig(bound)))
df_budget=pd.DataFrame(rows)
df_budget.to_csv(OUT/'defect_paid_dissolving_budget_step49.csv', index=False)
plt.figure(figsize=(6,4))
plt.loglog(df_budget['residual_scale'], df_budget['trace_budget'])
plt.xlabel('residual scale')
plt.ylabel('optimized trace budget')
plt.tight_layout()
plt.savefig(OUT/'defect_paid_dissolving_budget_step49.png', dpi=160)
plt.close()

# metadata schema and theorem map
schema = {
    "step": 49,
    "name": "Native probe adequacy under strict extension",
    "objects": {
        "native_probe_family": "L_j Gamma_j",
        "dissolving_probe_family": "D_j Gamma_j",
        "adequacy_factorization": "D_j Gamma_j = A_j L_j Gamma_j + R_j",
        "native_currency": "K^L_j = L_Gamma C_Gamma^dagger L_Gamma^*",
        "dissolving_currency": "K^D_j = D_Gamma C_Gamma^dagger D_Gamma^*",
        "residual_currency": "Xi_j = R_j C_Gamma^dagger R_j^*"
    },
    "accepted_claim": "native predictive membrane promotes to layer-dissolving membrane when adequacy residual currencies are transported and bounded",
    "nonclaims": [
        "native-only membrane does not imply full layer membrane without adequacy",
        "small residual norm is insufficient without residual currency control",
        "pseudoinverse zero is not legal if null-mode legality fails"
    ]
}
(OUT/'native_adequacy_extension_schema_step49.json').write_text(json.dumps(schema, indent=2))

map_rows = [
    dict(result='defect-paid adequacy transfer', input='D=AL+R, KL budget, residual currency Xi', output='KD <= (1+t) A KL A* + (1+t^-1) Xi', status='proved'),
    dict(result='predictive adequacy promotion', input='native membrane ladder + transported adequacy residual budgets', output='dissolving membrane ladder', status='proved'),
    dict(result='residual propagation', input='Xi_{j+1} <= q_j Xi_j + G_j', output='explicit Loewner bound on Xi_n', status='proved'),
    dict(result='blind-spot criterion', input='ker L subset ker D', output='exact adequacy iff inclusion holds', status='proved'),
    dict(result='blind-spot no-go', input='native membrane but D grows on ker L', output='dissolving capacity unbounded', status='countermodel'),
    dict(result='null-mode failure', input='D sees ker C', output='true variational capacity infinite', status='countermodel')
]
pd.DataFrame(map_rows).to_csv(OUT/'theorem_map_step49.csv', index=False)

gates = [
    dict(gate='formed closure', requirement='native and dissolving families are declared for the same formed layer', failure='outside scope / provisional'),
    dict(gate='exact package', requirement='C_Gamma and probe families live on lawful packaged carrier', failure='public-shadow overread'),
    dict(gate='null-mode legality', requirement='L,D,R annihilate legal null directions', failure='fake zero / infinite variational capacity'),
    dict(gate='stagewise adequacy', requirement='D_Gamma = A L_Gamma + R', failure='failed adequacy'),
    dict(gate='residual currency', requirement='R C_Gamma^dagger R* <= Xi', failure='small-norm residual overread'),
    dict(gate='transport square', requirement='S A = B T or defect paid in residual', failure='route/refinement mismatch'),
    dict(gate='predictive residual control', requirement='Xi_j bounded/summable/contracting', failure='blind spots reappear under refinement'),
    dict(gate='all-six status', requirement='P1-P6 records compose', failure='support-only / channel downgrade')
]
pd.DataFrame(gates).to_csv(OUT/'adequacy_extension_gate_table_step49.csv', index=False)
