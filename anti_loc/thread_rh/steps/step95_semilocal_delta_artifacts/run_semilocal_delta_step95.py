"""Toy sanity checks for Step 95: semilocal cross-term extraction.
These checks are not RH evidence. They only verify matrix identities matching the form logic.
"""
from pathlib import Path
import json
import numpy as np
import csv
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step95_semilocal_delta')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20260513)

def psd(n, scale=1.0):
    A = rng.normal(size=(n,n))
    return scale*(A.T @ A)/n

def sym(n, scale=1.0):
    A = rng.normal(size=(n,n))
    return scale*(A + A.T)/2

def eigmin(A): return float(np.linalg.eigvalsh((A+A.T)/2).min())
def eigmax(A): return float(np.linalg.eigvalsh((A+A.T)/2).max())
def pospart(A):
    vals, vecs = np.linalg.eigh((A+A.T)/2)
    vals = np.maximum(vals,0)
    return (vecs*vals) @ vecs.T

# Random extraction checks: K_weil = K_pos + Delta
rows=[]
for trial in range(60):
    n=8
    K_inf=psd(n,0.8)
    K_pr=psd(n,0.6)
    K_pole=psd(n,0.2)
    K_tail=psd(n,0.1)
    K_pos=K_inf+K_pr+K_pole+K_tail
    Delta=sym(n,0.25)
    K_weil=K_pos+Delta
    # source absorption by alpha I
    Delta_plus=pospart(Delta)
    lam_needed=eigmax(Delta_plus)
    alpha=lam_needed+0.05
    slack=eigmin(alpha*np.eye(n)-Delta_plus)
    identity_error=np.linalg.norm((K_weil-K_pos)-Delta,ord='fro')
    rows.append({
        'trial':trial,
        'dimension':n,
        'delta_min_eig':eigmin(Delta),
        'delta_max_eig':eigmax(Delta),
        'delta_positive_part_trace':float(np.trace(Delta_plus)),
        'source_alpha':alpha,
        'source_absorption_min_eig':slack,
        'identity_error_fro':identity_error
    })
with open(OUT/'semilocal_delta_random_checks_step95.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# Partial source coverage failure: projection onto first k dims misses hidden sector
rows=[]
n=10
# choose a cross-term positive on all dimensions, larger hidden sector for last components
Delta_plus=np.diag(np.linspace(0.2,2.0,n))
for k in range(1,n+1):
    P=np.zeros((n,n)); P[:k,:k]=np.eye(k)
    alpha=3.0
    F=alpha*P
    slack=eigmin(F-Delta_plus)
    covered_trace=float(np.trace(P@Delta_plus@P))
    hidden_trace=float(np.trace((np.eye(n)-P)@Delta_plus@(np.eye(n)-P)))
    rows.append({'covered_dimensions':k,'dimension':n,'source_alpha':alpha,'min_eig_F_minus_delta_plus':slack,'covered_trace':covered_trace,'hidden_trace':hidden_trace})
with open(OUT/'partial_source_coverage_failure_step95.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

plt.figure(figsize=(6,4))
plt.plot([r['covered_dimensions'] for r in rows],[r['min_eig_F_minus_delta_plus'] for r in rows],marker='o')
plt.axhline(0, linewidth=1)
plt.xlabel('covered dimensions')
plt.ylabel('min eigenvalue of F - Delta_+')
plt.title('Partial source coverage fails until full sector is covered')
plt.tight_layout()
plt.savefig(OUT/'partial_source_coverage_failure_step95.png',dpi=160)
plt.close()

# Toy semilocal local factor weight showing measure deformation by finite primes
xis=np.linspace(-30,30,1201)
primes=[2,3,5,7,11]
rows=[]
for m in range(0,len(primes)+1):
    ps=primes[:m]
    weight=np.ones_like(xis)
    for p in ps:
        # |1 - p^{-1/2+i xi}|^{-2}
        a=p**(-0.5)
        weight *= 1.0/(1 + a*a - 2*a*np.cos(xis*np.log(p)))
    rows.append({'num_primes':m,'min_weight':float(weight.min()),'max_weight':float(weight.max()),'mean_weight':float(weight.mean()),'std_weight':float(weight.std())})
    if m in (0,1,3,5):
        plt.plot(xis,weight,label=f'{m} primes')
plt.xlabel('xi')
plt.ylabel('finite local factor weight')
plt.title('Semilocal response-measure deformation')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'semilocal_measure_deformation_step95.png',dpi=160)
plt.close()
with open(OUT/'semilocal_measure_deformation_step95.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# Budget absorption ladder model
rows=[]
Delta_norm=1.0
for nstage in range(1,101):
    Lambda=nstage**0.75
    E=1/(nstage**1.2)
    budget=Delta_norm/(1+Lambda)+E
    rows.append({'stage':nstage,'Lambda':Lambda,'source_budget_bound':budget,'tail_defect':E})
with open(OUT/'source_absorption_ladder_step95.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(6,4))
plt.plot([r['stage'] for r in rows],[r['source_budget_bound'] for r in rows])
plt.plot([r['stage'] for r in rows],[r['tail_defect'] for r in rows],linestyle='--')
plt.xlabel('stage')
plt.ylabel('bound')
plt.title('Toy source absorption + vanishing defect')
plt.tight_layout()
plt.savefig(OUT/'source_absorption_ladder_step95.png',dpi=160)
plt.close()

schema={
    'step':95,
    'object':'semilocal cross-term operator Delta_S',
    'core':'C_S^- = V_S eta_S(S_0(R)^ev) cap Y_S^-',
    'actual_form':'q_Weil,S = QW_S pulled to semilocal response core',
    'positive_form':'q_pos,S = q_infty^CC + q_pr,S^pair + q_pole,S^+ + q_tail,S^+',
    'cross_term':'Delta_S = q_Weil,S - q_pos,S',
    'acceptance':['Delta_S <= 0','Delta_S <= E_Delta,S with vanishing fixed/exhaustive tail','Delta_S^+ <= source frame + defect with Lambda_n -> infinity'],
    'nonclaims':['not an RH proof','not a proof of semilocal positivity','finite S is support-only without tail/exhaustivity','not a de Branges/RKHS positivity ansatz']
}
(OUT/'semilocal_delta_schema_step95.json').write_text(json.dumps(schema,indent=2))
