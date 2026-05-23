import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step92_hecke_carrier')

rows=[]
for N in [4,8,16,32,64]:
    x=np.arange(N)
    chis=[]
    for k in range(N):
        chis.append(np.exp(2j*np.pi*k*x/N)/np.sqrt(N))
    F=np.vstack(chis)
    frame=F.conj().T@F
    eig=np.linalg.eigvalsh(frame.real)
    rows.append({'N':N,'min_eig':eig.min(),'max_eig':eig.max(),'frame_error':np.linalg.norm(frame-np.eye(N))})
pd.DataFrame(rows).to_csv(out/'finite_character_frame_checks_step92.csv',index=False)

# partial character coverage failure on cyclic group
N=64
x=np.arange(N)
rows=[]
for m in [1,2,4,8,16,32,64]:
    F=[]
    for k in range(m):
        F.append(np.exp(2j*np.pi*k*x/N)/np.sqrt(N))
    F=np.vstack(F)
    frame=(F.conj().T@F).real
    eig=np.linalg.eigvalsh(frame)
    rows.append({'N':N,'m_chars':m,'min_eig':eig.min(),'rank':np.linalg.matrix_rank(frame,tol=1e-10),'max_eig':eig.max()})
pd.DataFrame(rows).to_csv(out/'partial_character_coverage_step92.csv',index=False)

# toy source budget for increasing full finite quotient dimension, lambda growth
rows=[]
for N in [4,8,16,32,64,128]:
    for lam in [1,2,4,8]:
        # with full normalized character basis frame=I; source frame=lam I
        budget=1/lam
        rows.append({'N':N,'lambda':lam,'Lambda':lam,'budget_bound':budget})
pd.DataFrame(rows).to_csv(out/'toy_source_budget_step92.csv',index=False)

# plots
plt.figure()
df=pd.read_csv(out/'partial_character_coverage_step92.csv')
plt.plot(df['m_chars'], df['min_eig'], marker='o', label='min eigenvalue')
plt.plot(df['m_chars'], df['rank']/N, marker='s', label='rank/N')
plt.xscale('log', base=2)
plt.xlabel('number of characters used')
plt.ylabel('coverage metric')
plt.title('Partial character families do not cover full quotient')
plt.legend()
plt.tight_layout()
plt.savefig(out/'partial_character_coverage_step92.png', dpi=180)
plt.close()

plt.figure()
for N in [4,16,64,128]:
    d=pd.read_csv(out/'toy_source_budget_step92.csv')
    dd=d[d.N==N]
    plt.plot(dd['lambda'], dd['budget_bound'], marker='o', label=f'N={N}')
plt.xscale('log', base=2)
plt.yscale('log', base=2)
plt.xlabel('source strength lambda')
plt.ylabel('budget bound 1/lambda')
plt.title('Full character-frame source strength collapses budget')
plt.legend()
plt.tight_layout()
plt.savefig(out/'toy_source_budget_step92.png', dpi=180)
plt.close()

print('created step92 checks')
