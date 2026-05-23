#!/usr/bin/env python3
"""Finite sanity checks for Step 37 character-source frame theorem.
These checks verify elementary PSD inequalities and illustrate no-go cases.
They are not Six Birds simulations.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step37_characterframe')
OUT.mkdir(parents=True, exist_ok=True)

def min_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((A + A.T.conj()) / 2.0)[0].real)

def max_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((A + A.T.conj()) / 2.0)[-1].real)

# 1. Orthogonal character-source coverage.
rows=[]
for m in [2,3,4,5,8,12]:
    for missing in [0,1,2]:
        if missing >= m:
            continue
        strengths = np.linspace(1.0, 3.0, m)
        active = np.ones(m, dtype=bool)
        if missing > 0:
            active[-missing:] = False
        F = np.diag(strengths * active)
        Lambda = min_eig(F)
        if Lambda > 1e-12:
            K_bound = 1.0/Lambda
            status = 'covered'
        else:
            K_bound = np.inf
            status = 'missing_character'
        rows.append({
            'model':'orthogonal_character_coverage',
            'dimension':m,
            'missing_blocks':missing,
            'lambda_min_frame':Lambda,
            'certified_budget_bound':K_bound,
            'status':status,
        })
orth_df=pd.DataFrame(rows)
orth_df.to_csv(OUT/'orthogonal_character_coverage_step37.csv', index=False)

# 2. Uniform character source growth ladder: all character strengths grow.
rows=[]
for n in range(1,101):
    m=6
    strengths = n*np.ones(m)
    F=np.diag(strengths)
    Lambda=min_eig(F)
    rows.append({'stage':n,'lambda_min_frame':Lambda,'budget_bound':1.0/Lambda})
ladder_df=pd.DataFrame(rows)
ladder_df.to_csv(OUT/'character_source_growth_ladder_step37.csv', index=False)

# 3. Partial source growth: one character never hardens.
rows=[]
for n in range(1,101):
    strengths = np.array([n,n,n,n,n,1.0], dtype=float)
    Lambda=min_eig(np.diag(strengths))
    rows.append({'stage':n,'lambda_min_frame':Lambda,'budget_bound':1.0/Lambda,'uncovered_or_bounded_block':'last_block_strength_1'})
partial_df=pd.DataFrame(rows)
partial_df.to_csv(OUT/'partial_character_source_no_collapse_step37.csv', index=False)

# 4. Nonorthogonal source-frame checks: random Q_s vectors form frame.
rng=np.random.default_rng(37)
rows=[]
for trial in range(80):
    d=5
    num=9
    # scalar source readouts q_s^T y, Q_s row vector
    qs = rng.normal(size=(num,d))
    # normalize rows
    qs = qs / np.linalg.norm(qs, axis=1, keepdims=True)
    lambdas = rng.uniform(0.5,3.0,size=num)
    thetas = rng.uniform(0.7,2.0,size=num)
    F=sum((lambdas[i]/thetas[i])*np.outer(qs[i],qs[i]) for i in range(num))
    Lambda=min_eig(F)
    cmin=float(np.min(lambdas/thetas))
    frame_lower=min_eig(sum(np.outer(qs[i],qs[i]) for i in range(num)))
    theoretical_lower=cmin*frame_lower
    rows.append({
        'trial':trial,
        'lambda_frame_actual':Lambda,
        'lower_bound_c_m':theoretical_lower,
        'ratio_actual_to_bound':Lambda/theoretical_lower if theoretical_lower>1e-12 else np.nan,
        'status':'pass' if Lambda+1e-9>=theoretical_lower else 'fail'
    })
rand_df=pd.DataFrame(rows)
rand_df.to_csv(OUT/'random_nonorthogonal_frame_checks_step37.csv', index=False)

# 5. Trace/invariant-only source no-collapse: source on first coord only, anti-invariant includes rest.
rows=[]
for lam in np.logspace(-2,4,25):
    d=4
    F=np.diag([lam,0,0,0])
    rows.append({'lambda_trace_source':lam,'relative_lower_frame_constant':min_eig(F),'covered_dimension':1,'anti_invariant_dimension':d})
trace_df=pd.DataFrame(rows)
trace_df.to_csv(OUT/'trace_source_no_collapse_step37.csv', index=False)

# 6. Character eigenvalue budget example with circulant currency.
# K = (1-c)I + cJ. The Fourier/character eigenvalues are 1-c (nontrivial) and 1+(m-1)c (trivial).
rows=[]
for c in np.linspace(-0.3,0.3,61):
    m=8
    lam_triv=1+(m-1)*c
    lam_non=1-c
    rows.append({'c':c,'lambda_trivial':lam_triv,'lambda_nontrivial':lam_non,'nontrivial_budget_pass_I':lam_non<=1.0,'trace_budget_pass_I':lam_triv<=1.0})
char_df=pd.DataFrame(rows)
char_df.to_csv(OUT/'circulant_character_budget_step37.csv', index=False)

# Plots
plt.figure(figsize=(6,4))
plt.plot(ladder_df['stage'], ladder_df['budget_bound'], label='all character blocks harden')
plt.plot(partial_df['stage'], partial_df['budget_bound'], label='one block bounded')
plt.xlabel('strict-extension stage')
plt.ylabel('certified anti-invariant budget bound')
plt.title('Character-source growth: full vs partial coverage')
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'character_source_growth_step37.png', dpi=180)
plt.close()

plt.figure(figsize=(6,4))
plt.plot(char_df['c'], char_df['lambda_trivial'], label='trivial/trace character')
plt.plot(char_df['c'], char_df['lambda_nontrivial'], label='nontrivial characters')
plt.axhline(1.0, linestyle='--')
plt.xlabel('correlation c')
plt.ylabel('character eigenvalue')
plt.title('Trace shadow can pass while nontrivial characters fail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'character_budget_trace_shadow_step37.png', dpi=180)
plt.close()

plt.figure(figsize=(6,4))
plt.scatter(rand_df['lower_bound_c_m'], rand_df['lambda_frame_actual'])
mx=max(rand_df['lambda_frame_actual'].max(), rand_df['lower_bound_c_m'].max())
plt.plot([0,mx],[0,mx], linestyle='--')
plt.xlabel('theorem lower bound')
plt.ylabel('actual lower frame constant')
plt.title('Nonorthogonal source-frame lower bound checks')
plt.tight_layout()
plt.savefig(OUT/'nonorthogonal_frame_checks_step37.png', dpi=180)
plt.close()

# Write a summary JSON with max/min stats.
stats={
    'orthogonal_missing_status_counts': orth_df['status'].value_counts().to_dict(),
    'growth_final_full_budget_bound': float(ladder_df['budget_bound'].iloc[-1]),
    'growth_final_partial_budget_bound': float(partial_df['budget_bound'].iloc[-1]),
    'random_frame_all_pass': bool((rand_df['status']=='pass').all()),
    'random_frame_min_ratio_actual_to_bound': float(rand_df['ratio_actual_to_bound'].min()),
    'trace_source_min_frame_constant': float(trace_df['relative_lower_frame_constant'].min()),
}
(OUT/'character_source_frame_stats_step37.json').write_text(json.dumps(stats, indent=2))
print(json.dumps(stats, indent=2))
