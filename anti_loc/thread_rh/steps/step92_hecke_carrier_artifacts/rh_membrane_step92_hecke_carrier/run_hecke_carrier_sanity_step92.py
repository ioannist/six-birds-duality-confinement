import numpy as np
import pandas as pd
from pathlib import Path

out=Path('/mnt/data/rh_membrane_step92_hecke_carrier')
out.mkdir(parents=True, exist_ok=True)

# Finite cyclic group character frame: full characters give tight frame, incomplete set has zero lower frame on full space.
rows=[]
for N in [4,8,16,32]:
    xs=np.arange(N)
    Ch=np.exp(2j*np.pi*np.outer(np.arange(N), xs)/N)/np.sqrt(N) # rows characters as ONB
    full=Ch.conj().T@Ch
    evals=np.linalg.eigvalsh(full.real)
    for m in [1, max(1,N//4), max(1,N//2), N-1, N]:
        S=Ch[:m]
        F=S.conj().T@S
        ev=np.linalg.eigvalsh(F.real)
        rows.append({
            'N':N,'num_chars':m,
            'lambda_min_full_space':float(ev.min()),
            'lambda_max_full_space':float(ev.max()),
            'rank':int(np.linalg.matrix_rank(F,tol=1e-10)),
            'status':'full_frame' if m==N else 'projection_only'
        })
pd.DataFrame(rows).to_csv(out/'finite_character_frame_checks_step92.csv',index=False)

# Window/tail toy: P_n window on l2-weighted ledger tail. If weights tail vanish then exhaustive, otherwise support-only.
rows=[]
for n in [5,10,20,50,100,200,500]:
    tail_summable=sum([1/k**2 for k in range(n+1,50000)])
    tail_nonsummable=sum([1/k for k in range(n+1,50000)])
    Lambda=n
    window_budget=(n/Lambda) # trace Lambda^-1 P_n for n-dimensional window = 1, not vanishing unless normalized/weighted
    weighted_window_budget=sum([1/(Lambda*k**2) for k in range(1,n+1)])
    rows.append({
        'n':n,
        'Lambda_n':Lambda,
        'unweighted_window_trace_budget':window_budget,
        'weighted_window_trace_budget':weighted_window_budget,
        'summable_tail_approx':tail_summable,
        'nonsummable_tail_truncated_approx':tail_nonsummable,
        'weighted_total_budget_plus_tail':weighted_window_budget+tail_summable
    })
pd.DataFrame(rows).to_csv(out/'window_tail_toy_step92.csv',index=False)

# Source candidate qualitative score table in numeric form for quick plotting.
rows=[
    ('prime_by_prime', 0.9, 0.3, 0.7, 0.4, 'positive but low-frequency soft'),
    ('dirichlet_characters', 0.8, 0.7, 0.6, 0.7, 'plausible finite windows need tail'),
    ('hecke_idele_characters', 0.8, 0.9, 0.8, 0.9, 'strongest but enlarged carrier'),
    ('selberg_trace', 0.5, 0.8, 0.5, 0.8, 'carrier dependent'),
    ('automorphic_representations', 0.6, 0.95, 0.4, 0.95, 'largest program'),
    ('trace_only', 0.9, 0.1, 0.9, 0.2, 'fails anti-invariant frame')
]
pd.DataFrame(rows,columns=['source_family','upstream_visibility','sector_coverage','concreteness','carrier_cost','comment']).to_csv(out/'source_candidate_scores_step92.csv',index=False)

# Create plots if matplotlib is available.
try:
    import matplotlib.pyplot as plt
    df=pd.read_csv(out/'finite_character_frame_checks_step92.csv')
    plt.figure()
    for N,g in df.groupby('N'):
        plt.plot(g['num_chars'],g['lambda_min_full_space'],marker='o',label=f'N={N}')
    plt.xlabel('number of characters included')
    plt.ylabel('lower frame bound on full space')
    plt.title('Finite character windows: full frame only when complete')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/'finite_character_frame_step92.png',dpi=180)
    plt.close()

    df=pd.read_csv(out/'window_tail_toy_step92.csv')
    plt.figure()
    plt.loglog(df['n'],df['weighted_total_budget_plus_tail'],marker='o',label='summable weighted tail + budget')
    plt.loglog(df['n'],df['nonsummable_tail_truncated_approx'],marker='s',label='non-summable tail (truncated)')
    plt.xlabel('window n')
    plt.ylabel('tail/budget')
    plt.title('Exhaustive tail requirement for moving character windows')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/'window_tail_toy_step92.png',dpi=180)
    plt.close()

    df=pd.read_csv(out/'source_candidate_scores_step92.csv')
    x=np.arange(len(df))
    width=0.2
    plt.figure(figsize=(10,4))
    for i,col in enumerate(['upstream_visibility','sector_coverage','concreteness','carrier_cost']):
        plt.bar(x+(i-1.5)*width,df[col],width,label=col)
    plt.xticks(x,df['source_family'],rotation=35,ha='right')
    plt.ylim(0,1.1)
    plt.ylabel('qualitative score')
    plt.title('Hecke-source route audit: qualitative candidate scores')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/'source_candidate_scores_step92.png',dpi=180)
    plt.close()
except Exception as e:
    print('plot failed:',e)
