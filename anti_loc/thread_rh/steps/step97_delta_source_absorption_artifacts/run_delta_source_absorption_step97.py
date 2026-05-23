import csv, json, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step97_delta_source_absorption')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(97)

def eigmin(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[0])

def eigmax(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[-1])

# Full-sector source absorption model.
d = 8
A = rng.normal(size=(d,d))
Delta = A.T @ A
Delta = Delta / eigmax(Delta)  # ||Delta|| = 1
rows=[]
for n in range(1,41):
    Lambda = 0.15*n
    F = Lambda*np.eye(d)
    slack = F - Delta
    rows.append({
        'n': n,
        'Lambda_n': Lambda,
        'min_eig_F_minus_Delta': eigmin(slack),
        'trace_budget_d_over_Lambda': d/Lambda,
        'absorbs_delta': eigmin(slack) >= -1e-10,
    })
with open(OUT/'full_sector_absorption_ladder_step97.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(6,4))
plt.plot([r['Lambda_n'] for r in rows],[r['trace_budget_d_over_Lambda'] for r in rows], marker='o')
plt.xlabel('source lower-frame strength $\\Lambda_n$')
plt.ylabel('certified trace budget $d/\\Lambda_n$')
plt.title('Full-sector source absorption: budget collapse')
plt.tight_layout(); plt.savefig(OUT/'full_sector_absorption_budget_step97.png', dpi=180); plt.close()
plt.figure(figsize=(6,4))
plt.plot([r['Lambda_n'] for r in rows],[r['min_eig_F_minus_Delta'] for r in rows], marker='o')
plt.axhline(0, linestyle='--')
plt.xlabel('source lower-frame strength $\\Lambda_n$')
plt.ylabel('min eig$(F_n-\\Delta^+)$')
plt.title('Full-sector absorption threshold')
plt.tight_layout(); plt.savefig(OUT/'full_sector_absorption_slack_step97.png', dpi=180); plt.close()

# Partial source coverage failure.
d=8
Delta_partial = np.zeros((d,d)); Delta_partial[-1,-1] = 1.0
rows=[]
P = np.diag([1]*(d-1)+[0])
for n in range(1,41):
    Lambda = n
    F = Lambda*P
    rows.append({
        'n': n,
        'Lambda_n': Lambda,
        'uncovered_delta_weight': Delta_partial[-1,-1],
        'min_eig_F_minus_Delta': eigmin(F-Delta_partial),
        'absorbs_delta': eigmin(F-Delta_partial)>=-1e-10,
    })
with open(OUT/'partial_coverage_failure_step97.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(6,4))
plt.plot([r['Lambda_n'] for r in rows],[r['min_eig_F_minus_Delta'] for r in rows], marker='o')
plt.axhline(0, linestyle='--')
plt.xlabel('visible source strength')
plt.ylabel('min eig$(F_n-\\Delta^+)$')
plt.title('Partial character/source coverage cannot absorb hidden direction')
plt.tight_layout(); plt.savefig(OUT/'partial_coverage_failure_step97.png', dpi=180); plt.close()

# Moving finite window and tail requirement.
d=200
Delta_diag = np.array([1.0/(k+1)**1.1 for k in range(d)])  # summable-ish finite truncation
rows=[]
for n in [5,10,20,30,50,75,100,150,200]:
    Fdiag = np.zeros(d)
    Fdiag[:n] = 2.0  # absorbs first n entries
    residual_tail_trace = float(np.sum(np.maximum(Delta_diag - Fdiag,0)))
    hidden_tail_trace = float(np.sum(Delta_diag[n:]))
    rows.append({
        'window_n': n,
        'hidden_tail_trace': hidden_tail_trace,
        'residual_unabsorbed_trace': residual_tail_trace,
        'status_if_no_tail_bridge': 'support_only' if n<d else 'finite_full_model',
    })
with open(OUT/'moving_window_tail_requirement_step97.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(6,4))
plt.plot([r['window_n'] for r in rows],[r['hidden_tail_trace'] for r in rows], marker='o')
plt.xlabel('finite source window size')
plt.ylabel('hidden tail trace')
plt.title('Moving-window source absorption needs tail/exhaustivity')
plt.tight_layout(); plt.savefig(OUT/'moving_window_tail_requirement_step97.png', dpi=180); plt.close()

# Defect budget and optimized obstruction demonstration.
rows=[]
for n in range(1,101):
    Lambda = n**0.75
    e_delta = 1/(n**1.2)
    e_tail = 1/(n**0.9)
    bound = d/Lambda + e_delta + e_tail
    rows.append({'n':n,'Lambda_n':Lambda,'source_trace_budget':d/Lambda,'E_delta_trace':e_delta,'E_tail_trace':e_tail,'total_trace_bound':bound})
with open(OUT/'defect_budget_collapse_step97.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(6,4))
plt.plot([r['n'] for r in rows],[r['total_trace_bound'] for r in rows])
plt.xlabel('stage n')
plt.ylabel('trace bound')
plt.title('Source + defect budget collapse model')
plt.tight_layout(); plt.savefig(OUT/'defect_budget_collapse_step97.png', dpi=180); plt.close()

# Random source-frame checks: F >= Lambda*I implies budget collapse; Delta absorption threshold.
check_rows=[]
for trial in range(60):
    d=6
    X=rng.normal(size=(d,d))
    U,_=np.linalg.qr(X)
    eigs=np.linspace(0.2,2.0,d)
    Delta=U@np.diag(eigs)@U.T
    Lambda=2.5+0.1*trial
    F=Lambda*np.eye(d)
    check_rows.append({'trial':trial,'lambda_max_delta':eigmax(Delta),'Lambda':Lambda,'min_eig_F_minus_Delta':eigmin(F-Delta),'trace_bound_d_over_Lambda':d/Lambda})
with open(OUT/'random_source_absorption_checks_step97.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(check_rows[0].keys())); w.writeheader(); w.writerows(check_rows)

# Schema manifest.
schema = {
    'step': 97,
    'title': 'Hecke/Dirichlet source absorption theorem for Delta_S^+',
    'objects': ['semilocal cross-term Delta_S^+', 'source frame F_n', 'character readouts Q_omega', 'source defects E_abs,n', 'tail/exhaustivity bridge'],
    'main_gate': 'Delta_S^+ <= F_n + E_abs,n and F_n >= Lambda_n Theta_0^{-1} with Lambda_n -> infinity',
    'failure_modes': ['partial character coverage', 'bounded source strength', 'moving finite window without tail bridge', 'target-selected/smuggled source', 'auxiliary carrier without descent'],
}
with open(OUT/'source_absorption_schema_step97.json','w') as f:
    json.dump(schema, f, indent=2)
