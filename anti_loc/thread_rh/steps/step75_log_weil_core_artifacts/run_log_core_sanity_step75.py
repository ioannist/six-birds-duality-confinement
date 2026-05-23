import numpy as np
import pandas as pd
from pathlib import Path
out=Path('/mnt/data/rh_membrane_step75_log_weil_core')
# Check positivity of finite prime shift symbol Psi(xi)=sum w_n |e^{i a_n xi}-1|^2
xis=np.linspace(-20,20,2001)
# toy prime-power shifts (not exact primes; only feature positivity sanity)
shifts=np.log(np.array([2,3,4,5,7,8,9,11],dtype=float))
weights=np.array([np.log(2)/np.sqrt(2), np.log(3)/np.sqrt(3), np.log(2)/2, np.log(5)/np.sqrt(5), np.log(7)/np.sqrt(7), np.log(2)/np.sqrt(8), np.log(3)/3, np.log(11)/np.sqrt(11)])
Psi=np.zeros_like(xis)
for a,w in zip(shifts,weights):
    Psi += w*np.abs(np.exp(1j*a*xis)-1)**2
pd.DataFrame({'xi':xis,'prime_shift_symbol':Psi}).to_csv(out/'prime_shift_symbol_step75.csv',index=False)
# Archimedean kernel sample: symmetric positive kernel k(a)=1/(2sinh(|a|/2)) cutoff near zero with difference symbol
agrid=np.linspace(1e-4,20,5000)
da=agrid[1]-agrid[0]
k=1/(2*np.sinh(agrid/2))
Psi_inf=[]
for xi in xis[::10]:
    # symmetric integral 2 * int_0 inf k(a) |e^{iaxi}-1|^2 da approx
    Psi_inf.append(2*np.sum(k*(2-2*np.cos(agrid*xi)))*da)
Psi_inf=np.array(Psi_inf)
pd.DataFrame({'xi':xis[::10],'arch_symbol_cutoff':Psi_inf}).to_csv(out/'arch_symbol_cutoff_step75.csv',index=False)
# Trace equality not domination counterexample
A=np.diag([2.0,0.0]); K=np.diag([1.0,1.0])
eigs=np.linalg.eigvalsh(K-A)
pd.DataFrame([{'trace_A':np.trace(A),'trace_K':np.trace(K),'min_eig_K_minus_A':eigs.min(),'Loewner_dominates':bool(eigs.min()>=-1e-12)}]).to_csv(out/'trace_not_domination_step75.csv',index=False)
# Core finite subspace insufficiency toy: inequality on first coordinate only, fails second
rows=[]
for n in range(1,11):
    # on subspace first n coordinates of N=n+1, choose fail hidden last coord
    N=n+1
    A=np.zeros((N,N)); K=np.eye(N)
    A[:n,:n]=0.5*np.eye(n)
    A[-1,-1]=2.0
    # core sees only first n
    core_ok=np.all(np.linalg.eigvalsh(K[:n,:n]-A[:n,:n])>=-1e-12)
    full_ok=np.all(np.linalg.eigvalsh(K-A)>=-1e-12)
    rows.append({'core_dim':n,'full_dim':N,'core_ok':core_ok,'full_ok':full_ok,'hidden_violation':2.0-1.0})
pd.DataFrame(rows).to_csv(out/'core_subspace_insufficiency_step75.csv',index=False)
print('wrote sanity artifacts')
