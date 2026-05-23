import numpy as np
import pandas as pd
from pathlib import Path

out = Path('/mnt/data/anti_localization_step43_taxonomy')
rows=[]
# Protocol diagonal failure
K = np.array([[1.,1.],[1.,1.]])
rows.append({
    'case':'protocol_diagonal_failure',
    'diag_max':float(np.max(np.diag(K))),
    'lambda_max':float(np.linalg.eigvalsh(K).max()),
    'identity_budget_pass': bool(np.linalg.eigvalsh(np.eye(2)-K).min() >= -1e-12)
})
# Public shadow overread
K2=np.diag([0.5,2.0])
F=np.array([[1.,0.]])
shadow=F@K2@F.T
rows.append({
    'case':'public_shadow_pass_hidden_fail',
    'shadow_currency':float(shadow[0,0]),
    'lambda_max_full':float(np.linalg.eigvalsh(K2).max()),
    'identity_budget_pass': bool(np.linalg.eigvalsh(np.eye(2)-K2).min() >= -1e-12)
})
# Exact sectioned direct sum
Ksec=np.diag([0.2,0.7,0.5])
Theta=np.eye(3)
rows.append({
    'case':'exact_sectioned_gluing_pass',
    'diag_max':float(np.max(np.diag(Ksec))),
    'lambda_max':float(np.linalg.eigvalsh(Ksec).max()),
    'identity_budget_pass': bool(np.linalg.eigvalsh(Theta-Ksec).min() >= -1e-12)
})
# Bundle divergence partial sums
for n in [1,2,4,8,16,32]:
    rows.append({
        'case':f'bundle_partial_sum_{n}',
        'diag_max':1.0,
        'lambda_max':float(n),
        'identity_budget_pass': False if n>1 else True
    })
pd.DataFrame(rows).to_csv(out/'taxonomy_countermodel_checks_step43.csv', index=False)
print('wrote checks')
