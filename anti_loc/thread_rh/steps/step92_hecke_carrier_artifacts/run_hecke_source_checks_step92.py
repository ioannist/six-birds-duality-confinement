import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out=Path('/mnt/data/rh_membrane_step92_hecke_carrier')

# Finite abelian toy: cyclic group C_m characters form tight frame.
rows=[]
for m in [4,8,16,32,64]:
    j=np.arange(m)
    k=np.arange(m)
    F=np.exp(-2j*np.pi*np.outer(k,j)/m)  # char matrix rows k, cols j
    frame=F.conj().T @ F
    err=np.linalg.norm(frame - m*np.eye(m), ord=2)
    rows.append({'m':m,'frame_bound':m,'operator_error':float(err)})
pd.DataFrame(rows).to_csv(out/'finite_character_tight_frame_step92.csv', index=False)

# Multiplier lower-frame toy: full vs finite window. Response dimension N, weights lambda on subset.
N=200
ns=np.arange(1,N+1)
rows=[]
for n in [5,10,20,40,80,120,160,200]:
    Lambda=float(np.log(n+1))
    lam=np.zeros(N)
    lam[:n]=Lambda
    full_lower=lam.min()
    window_lower=lam[:n].min()
    uncovered=N-n
    rows.append({'window_n':n,'Lambda_declared':Lambda,'full_lower_frame':full_lower,'window_lower_frame':window_lower,'uncovered_dim':uncovered})
pd.DataFrame(rows).to_csv(out/'finite_window_source_frame_step92.csv', index=False)

# Tail model: if tail mass decays, finite windows can promote; else not.
rows=[]
for n in range(1,101):
    B=1/(n+1)**2
    tail_good=1/(n+1)**2
    tail_bad=0.1
    rows.append({'n':n,'B_n':B,'tail_good':tail_good,'total_good':B+tail_good,'tail_bad':tail_bad,'total_bad':B+tail_bad})
pd.DataFrame(rows).to_csv(out/'tail_exhaustivity_model_step92.csv', index=False)

# Candidate source scores: illustrative qualitative table already in CSV; make numeric score plot.
candidates=['prime-by-prime','Dirichlet windows','Hecke idele','Selberg trace','Automorphic','de Branges']
full_frame=[1,3,5,4,5,3]
tail_need=[3,4,5,4,5,2]
carrier_cost=[1,3,5,4,5,4]
rows=[]
for c,a,b,d in zip(candidates,full_frame,tail_need,carrier_cost):
    rows.append({'candidate':c,'full_frame_potential':a,'tail_record_need':b,'carrier_construction_cost':d})
pd.DataFrame(rows).to_csv(out/'candidate_score_model_step92.csv', index=False)

# Plots
plt.figure(figsize=(6,4))
df=pd.read_csv(out/'finite_window_source_frame_step92.csv')
plt.plot(df['window_n'], df['Lambda_declared'], label='declared window strength')
plt.plot(df['window_n'], df['full_lower_frame'], label='full-space lower frame')
plt.xlabel('window size')
plt.ylabel('lower frame')
plt.legend()
plt.title('Finite conductor window: full-frame failure')
plt.tight_layout()
plt.savefig(out/'finite_window_full_frame_failure_step92.png', dpi=180)
plt.close()

plt.figure(figsize=(6,4))
df=pd.read_csv(out/'tail_exhaustivity_model_step92.csv')
plt.semilogy(df['n'], df['total_good'], label='exhaustive tail total')
plt.semilogy(df['n'], df['total_bad'], label='nonvanishing tail total')
plt.xlabel('stage n')
plt.ylabel('bound + tail')
plt.legend()
plt.title('Finite windows need vanishing tails')
plt.tight_layout()
plt.savefig(out/'tail_exhaustivity_model_step92.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4))
df=pd.read_csv(out/'candidate_score_model_step92.csv')
x=np.arange(len(df))
w=0.25
plt.bar(x-w, df['full_frame_potential'], width=w, label='full-frame potential')
plt.bar(x, df['tail_record_need'], width=w, label='tail-record need')
plt.bar(x+w, df['carrier_construction_cost'], width=w, label='carrier cost')
plt.xticks(x, df['candidate'], rotation=30, ha='right')
plt.ylabel('qualitative score')
plt.legend(fontsize=8)
plt.title('Candidate source-family audit profile')
plt.tight_layout()
plt.savefig(out/'candidate_score_model_step92.png', dpi=180)
plt.close()

print('wrote step92 checks')
