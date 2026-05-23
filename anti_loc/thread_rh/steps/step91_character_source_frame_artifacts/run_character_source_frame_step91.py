import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step91_character_source')
out.mkdir(parents=True, exist_ok=True)

# 1. Full finite character frame over C_m with normalized Fourier basis.
rows=[]
for m in [8,16,32,64]:
    # normalized DFT matrix unitary: full frame lower=1 if weight=1; with lambda=n style choose multiple strengths
    for lam in [1,2,5,10,20,50]:
        lower_full=lam
        budget=1/lam
        rows.append({'model':'full_finite_character_frame','dimension':m,'lambda_min':lam,'lower_frame':lower_full,'certified_budget':budget})
pd.DataFrame(rows).to_csv(out/'full_finite_character_frame_step91.csv',index=False)

# 2. Partial coverage failure in m-dimensional orthonormal character basis.
rows=[]
for m in [32,64,128]:
    for k in [1,2,4,8,16,32,64,128]:
        if k>m: continue
        lower_full=1.0 if k==m else 0.0
        uncovered=m-k
        rows.append({'dimension':m,'covered_characters':k,'uncovered':uncovered,'lower_frame_full_space':lower_full,'status':'accepted_full' if k==m else 'support_only_partial'})
pd.DataFrame(rows).to_csv(out/'partial_character_coverage_step91.csv',index=False)

# 3. Moving window: dimension increases, coverage window also increases but full infinite lower frame remains zero; tail mass model.
rows=[]
for n in range(1,101):
    cover=n
    moving_budget=1/(n)  # covered lower frame if lambda=n
    # tail model: if tail decays like 1/n^p, exact/exhaustive possible only p>0 and source budget also shrinks
    tail_good=1/(n**2)
    tail_bad=1/np.log(n+1)
    rows.append({'stage':n,'covered_window':cover,'covered_budget':moving_budget,'good_tail':tail_good,'bad_tail':tail_bad,'good_total':moving_budget+tail_good,'bad_total':moving_budget+tail_bad})
pd.DataFrame(rows).to_csv(out/'moving_window_tail_step91.csv',index=False)

# 4. Candidate source score table as CSV
candidate_rows=[
    {'candidate':'prime-by-prime paired shifts','upstream_visible':5,'full_character_coverage':1,'low_frequency_strength':1,'requires_larger_carrier':1,'risk':'low-frequency softness; not full character frame','status':'canonical_support_not_sufficient'},
    {'candidate':'Dirichlet characters conductor ladder','upstream_visible':4,'full_character_coverage':3,'low_frequency_strength':3,'requires_larger_carrier':3,'risk':'finite conductor windows need tail/exhaustivity; primitive/imprimitive defects','status':'plausible_if_completed'},
    {'candidate':'Hecke/idele-class characters','upstream_visible':4,'full_character_coverage':4,'low_frequency_strength':4,'requires_larger_carrier':5,'risk':'requires adelic/Hecke carrier and Plancherel/explicit-formula records','status':'strongest_character_route'},
    {'candidate':'trace-only/invariant character','upstream_visible':5,'full_character_coverage':0,'low_frequency_strength':1,'requires_larger_carrier':1,'risk':'misses nontrivial anti-invariant sectors','status':'failed_full_gate'},
    {'candidate':'target-selected residual characters','upstream_visible':0,'full_character_coverage':5,'low_frequency_strength':5,'requires_larger_carrier':2,'risk':'smuggled selection','status':'inadmissible'},
    {'candidate':'automorphic representation sources','upstream_visible':3,'full_character_coverage':5,'low_frequency_strength':4,'requires_larger_carrier':5,'risk':'major carrier construction; not small add-on','status':'broad_program'},
]
pd.DataFrame(candidate_rows).to_csv(out/'source_candidate_audit_step91.csv',index=False)

# plots
# Full finite frame budget collapse
fig,ax=plt.subplots(figsize=(6,4))
lam=np.arange(1,101)
ax.plot(lam,1/lam)
ax.set_xlabel('lower-frame strength $\\Lambda$')
ax.set_ylabel('certified budget $1/\\Lambda$')
ax.set_title('Full character-source frame: budget collapse')
ax.grid(True,alpha=.3)
fig.tight_layout()
fig.savefig(out/'full_character_budget_collapse_step91.png',dpi=160)
plt.close(fig)

# partial coverage failure
fig,ax=plt.subplots(figsize=(6,4))
m=64
ks=np.arange(1,m+1)
lower=np.where(ks==m,1,0)
ax.step(ks,lower,where='post')
ax.set_xlabel('covered character blocks out of 64')
ax.set_ylabel('lower frame on full space')
ax.set_title('Partial character coverage leaves lower frame zero')
ax.set_ylim(-0.05,1.05)
ax.grid(True,alpha=.3)
fig.tight_layout()
fig.savefig(out/'partial_character_failure_step91.png',dpi=160)
plt.close(fig)

# moving window tail
df=pd.read_csv(out/'moving_window_tail_step91.csv')
fig,ax=plt.subplots(figsize=(6,4))
ax.loglog(df['stage'],df['covered_budget'],label='covered-window budget')
ax.loglog(df['stage'],df['good_total'],label='with vanishing tail')
ax.loglog(df['stage'],df['bad_total'],label='slow tail')
ax.set_xlabel('stage n')
ax.set_ylabel('obstruction budget')
ax.set_title('Moving windows need tail/exhaustivity')
ax.grid(True,which='both',alpha=.3)
ax.legend()
fig.tight_layout()
fig.savefig(out/'moving_window_tail_requirement_step91.png',dpi=160)
plt.close(fig)

# source candidate scores
scores=pd.DataFrame(candidate_rows)
fig,ax=plt.subplots(figsize=(8,4))
labels=scores['candidate']
x=np.arange(len(labels))
score=scores[['upstream_visible','full_character_coverage','low_frequency_strength']].mean(axis=1)
ax.bar(x,score)
ax.set_xticks(x)
ax.set_xticklabels(labels,rotation=35,ha='right')
ax.set_ylim(0,5)
ax.set_ylabel('rough structural score')
ax.set_title('Candidate source-family structural audit')
fig.tight_layout()
fig.savefig(out/'source_candidate_scores_step91.png',dpi=160)
plt.close(fig)

print('generated')
