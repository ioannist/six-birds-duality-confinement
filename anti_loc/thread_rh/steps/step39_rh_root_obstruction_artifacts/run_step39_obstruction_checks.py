#!/usr/bin/env python3
"""Small algebraic checks for Step 39 obstruction examples.
These are finite PSD sanity checks, not Six Birds simulations.
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUT=Path(__file__).resolve().parent

def eigmax(A): return float(np.linalg.eigvalsh((A+A.T.conj())/2).max())
def eigmin(A): return float(np.linalg.eigvalsh((A+A.T.conj())/2).min())

def psd_le(A,B,tol=1e-10): return eigmax(A-B) <= tol

rows=[]
# EF domination failure
A=np.eye(2); K=np.zeros((2,2))
rows.append(dict(case='EF_domination_failure', lhs_max=eigmax(A), rhs_max=eigmax(K), domination=psd_le(A,K), status='failed_EF_domination'))
# Incomplete character frame
for lam in [1,10,100,1e4]:
    F=np.diag([lam,0.0])
    rows.append(dict(case='incomplete_character_frame', Lambda_input=lam, frame_min=eigmin(F), uncovered_capacity=1.0, status='failed_character_frame'))
# Bounded source only
for lam in [1,2,5,10]:
    bound=1/lam
    rows.append(dict(case='bounded_source', Lambda_input=lam, budget_bound=bound, exact_confinement=(bound==0), status='finite_source_only'))
# Null-mode fake collapse
C=np.diag([0.,1.]); L=np.array([[1.,0.]])
K_pseudo=L@np.linalg.pinv(C)@L.T
rows.append(dict(case='null_mode_fake_collapse', pseudo_budget=float(K_pseudo[0,0]), variational_capacity='infinite', status='failed_null_legality'))
# Trace shadow failure
A=np.diag([2.,0.]); K=np.eye(2)
rows.append(dict(case='trace_shadow_failure', trace_A=float(np.trace(A)), trace_K=float(np.trace(K)), loewner=psd_le(A,K), status='shadow_overread'))

pd.DataFrame(rows).to_csv(OUT/'obstruction_checks_step39.csv', index=False)

# confinement ladder calculations
rows=[]
Theta_trace=2.0
for n in [1,2,5,10,20,50,100,200,500,1000]:
    Lambda=n
    E_src=1/(n*n)
    E_EF=1/(n*n*n)
    E_vis=1/(n*n)
    t=1.0
    eps=0.1
    trace_bound=(1+t)*(Theta_trace/Lambda+E_src)+(1+1/t)*E_EF+E_vis
    mass_bound=trace_bound/(eps*eps)
    rows.append(dict(n=n,Lambda=Lambda,E_src=E_src,E_EF=E_EF,E_vis=E_vis,trace_bound=trace_bound,mass_bound_eps_0p1=mass_bound))
pd.DataFrame(rows).to_csv(OUT/'obstruction_confinement_ladder_step39.csv', index=False)
print('wrote step39 obstruction checks')
