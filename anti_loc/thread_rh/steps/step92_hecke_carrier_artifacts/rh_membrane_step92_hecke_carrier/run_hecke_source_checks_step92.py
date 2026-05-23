import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
out=Path('/mnt/data/rh_membrane_step92_hecke_carrier')
rows=[]
# finite cyclic character tight frame check
for m in [4,8,16,32,64]:
    j=np.arange(m)
    F=np.exp(2j*np.pi*np.outer(j,j)/m)/np.sqrt(m)
    full=F.conj().T @ F  # I
    err=np.linalg.norm(full-np.eye(m),2)
    # partial first k chars
    for k in [max(1,m//8), max(1,m//4), max(1,m//2), m]:
        P=F[:k,:].conj().T @ F[:k,:]
        eig=np.linalg.eigvalsh(P)
        rows.append({"m":m,"k":k,"full_frame_error":err,"partial_min_eig":eig[0].real,"partial_max_eig":eig[-1].real,"rank":np.linalg.matrix_rank(P,tol=1e-10)})
pd.DataFrame(rows).to_csv(out/'finite_character_frame_checks_step92.csv',index=False)
# model tail/exhaustivity curves
ns=np.arange(1,201)
B=1/ns
T_good=1/ns**2
T_bad=1/np.sqrt(ns)
df=pd.DataFrame({"n":ns,"window_bound":B,"tail_good":T_good,"total_good":B+T_good,"tail_bad":T_bad,"total_bad":B+T_bad})
df.to_csv(out/'conductor_tail_model_step92.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot(ns,df['window_bound'],label='window bound')
plt.plot(ns,df['total_good'],label='exhaustive total')
plt.plot(ns,df['total_bad'],label='bad tail total')
plt.yscale('log')
plt.xlabel('refinement n')
plt.ylabel('trace budget model')
plt.title('Finite character windows need a tail record')
plt.legend()
plt.tight_layout()
plt.savefig(out/'conductor_tail_model_step92.png',dpi=180)
plt.close()
# candidate scores schematic (not evidence)
candidates=['prime','Dirichlet','Hecke','Selberg','automorphic','de Branges']
# subjective audit dimensions: upstream, coverage, carrier-native, tail difficulty inverted
scores=np.array([
    [5,2,5,3],
    [4,3,3,2],
    [4,5,3,1],
    [3,4,2,2],
    [3,5,2,1],
    [4,3,5,3],
],dtype=float)
pd.DataFrame(scores,columns=['upstream_visibility','sector_coverage','carrier_native','tail_feasibility'],index=candidates).to_csv(out/'candidate_source_scorecard_step92.csv')
plt.figure(figsize=(7,4))
plt.imshow(scores,aspect='auto')
plt.xticks(range(4),['upstream','coverage','carrier','tail'],rotation=20)
plt.yticks(range(len(candidates)),candidates)
plt.colorbar(label='schematic score')
plt.title('Qualitative source-family audit scorecard')
plt.tight_layout()
plt.savefig(out/'candidate_source_scorecard_step92.png',dpi=180)
plt.close()
print('done')
