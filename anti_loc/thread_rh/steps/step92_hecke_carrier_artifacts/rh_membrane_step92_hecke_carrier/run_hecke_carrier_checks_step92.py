import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step92_hecke_carrier')
out.mkdir(parents=True, exist_ok=True)

# Finite cyclic character frames: complete and partial.
rows=[]
for N in [4,6,8,12,16,24,32,48,64]:
    g=np.arange(N)
    chars=[]
    for k in range(N):
        chars.append(np.exp(2j*np.pi*k*g/N)/np.sqrt(N))
    E=np.vstack(chars) # N x N, rows characters
    F_full=E.conj().T@E
    eig=np.linalg.eigvalsh(F_full).real
    # partial half characters
    m=max(1,N//2)
    F_part=E[:m].conj().T@E[:m]
    eigp=np.linalg.eigvalsh(F_part).real
    rows.append(dict(N=N, kind='full', num_chars=N, min_eig=eig.min(), max_eig=eig.max(), rank=np.linalg.matrix_rank(F_full, tol=1e-8)))
    rows.append(dict(N=N, kind='partial_first_half', num_chars=m, min_eig=eigp.min(), max_eig=eigp.max(), rank=np.linalg.matrix_rank(F_part, tol=1e-8)))
    # random half characters average over trials
    vals=[]
    ranks=[]
    rng=np.random.default_rng(1234+N)
    for _ in range(20):
        idx=rng.choice(N,size=m,replace=False)
        Fr=E[idx].conj().T@E[idx]
        vals.append(np.linalg.eigvalsh(Fr).real.min())
        ranks.append(np.linalg.matrix_rank(Fr, tol=1e-8))
    rows.append(dict(N=N, kind='partial_random_half_mean', num_chars=m, min_eig=float(np.mean(vals)), max_eig=np.nan, rank=float(np.mean(ranks))))
pd.DataFrame(rows).to_csv(out/'finite_character_frame_checks_step92.csv', index=False)

# Toy conductor/frequency window: full finite frames but tail uncovered.
rows=[]
for n in range(1,31):
    Lambda=n
    tail_defect=1/(1+n/5)  # toy tail decays slowly
    trace_bound=1/Lambda + tail_defect
    rows.append(dict(stage=n, Lambda=Lambda, collapse_term=1/Lambda, tail_defect=tail_defect, total_bound=trace_bound))
pd.DataFrame(rows).to_csv(out/'exhaustive_tail_model_step92.csv', index=False)

# Candidate route score table.
candidates=[
 ('Dirichlet finite conductor windows','finite arithmetic characters','strong finite frames','needs tail/exhaustivity; finite windows support-only',3,2),
 ('Hecke/idele-class characters','full character dual with Plancherel','best full-sector fit','requires enlarged carrier and auxiliary EF records',5,4),
 ('Prime-by-prime paired shifts','canonical zeta-native features','positive and upstream-visible','low-frequency soft; not full character frame',3,3),
 ('Selberg/trace-formula sources','spectral trace carrier','powerful if carrier-native','shadow unless carrier chosen that way',4,4),
 ('Automorphic representation sources','broad representation spectrum','maximal sector coverage potential','major enlarged program; many auxiliary records',5,5),
 ('de Branges kernel sources','reproducing-kernel Hilbert space','carrier-native if chosen','no free source ladder; depends on kernel positivity',3,4),
]
pd.DataFrame(candidates, columns=['candidate','source_object','strength','main_gap','coverage_score','construction_cost']).to_csv(out/'hecke_source_candidate_scores_step92.csv', index=False)

# Plots
frame_df=pd.read_csv(out/'finite_character_frame_checks_step92.csv')
plt.figure(figsize=(7,4))
for kind in ['full','partial_first_half','partial_random_half_mean']:
    d=frame_df[frame_df.kind==kind]
    plt.plot(d.N, d.min_eig, marker='o', label=kind)
plt.axhline(0,color='k',lw=0.7)
plt.xlabel('finite cyclic quotient size N')
plt.ylabel('minimum eigenvalue of source frame')
plt.title('Complete character families are frames; partial families leave holes')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'finite_character_frame_checks_step92.png', dpi=180)
plt.close()

tail_df=pd.read_csv(out/'exhaustive_tail_model_step92.csv')
plt.figure(figsize=(7,4))
plt.plot(tail_df.stage, tail_df.collapse_term, label='source collapse term 1/Lambda')
plt.plot(tail_df.stage, tail_df.tail_defect, label='tail/exhaustivity defect')
plt.plot(tail_df.stage, tail_df.total_bound, label='total obstruction bound')
plt.xlabel('stage')
plt.ylabel('toy bound')
plt.title('Finite-window frames need a tail bridge')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'exhaustive_tail_model_step92.png', dpi=180)
plt.close()

cand=pd.read_csv(out/'hecke_source_candidate_scores_step92.csv')
plt.figure(figsize=(8,4.5))
x=np.arange(len(cand))
plt.scatter(cand.coverage_score, cand.construction_cost, s=80)
for i,row in cand.iterrows():
    plt.annotate(row.candidate.split()[0], (row.coverage_score+0.03, row.construction_cost+0.03), fontsize=8)
plt.xlabel('sector coverage potential (toy score)')
plt.ylabel('construction cost (toy score)')
plt.title('Character-source route: coverage vs construction cost')
plt.xlim(2.5,5.5); plt.ylim(1.5,5.5)
plt.tight_layout()
plt.savefig(out/'hecke_source_candidate_scores_step92.png', dpi=180)
plt.close()

print('wrote step92 checks')
