import numpy as np
import pandas as pd
from pathlib import Path

out=Path('/mnt/data/rh_membrane_step76_weil_matching')
rng=np.random.default_rng(7601)

# 1. Trace-not-domination countermodel
A=np.diag([2.0,0.0])
K=np.eye(2)
trace_case=pd.DataFrame([{
    'case':'trace_equal_not_domination',
    'trace_A':float(np.trace(A)),
    'trace_K':float(np.trace(K)),
    'min_eig_K_minus_A':float(np.linalg.eigvalsh(K-A)[0]),
    'loewner_pass': bool(np.linalg.eigvalsh(K-A)[0]>=-1e-12)
}])
trace_case.to_csv(out/'trace_not_domination_countermodel_step76.csv',index=False)

# 2. Finite core insufficiency: M positive on e1 but not full space
D=np.diag([1.0,-1.0])
rows=[]
for theta in np.linspace(0, np.pi/2, 41):
    v=np.array([np.cos(theta), np.sin(theta)])
    val=float(v@D@v)
    rows.append({'theta':theta, 'quadratic_form':val, 'core_e1_positive': True, 'full_min_eig': float(np.linalg.eigvalsh(D)[0])})
pd.DataFrame(rows).to_csv(out/'finite_core_insufficiency_step76.csv',index=False)

# 3. Random signed component repair: Q = K - A. Compute positive part repair.
rows=[]
for n in [3,5,8]:
  for trial in range(20):
    M=rng.normal(size=(n,n)); Q=(M+M.T)/2
    evals,U=np.linalg.eigh(Q)
    Qpos=U@np.diag(np.maximum(evals,0))@U.T
    Qneg=U@np.diag(np.maximum(-evals,0))@U.T
    # Q + Qneg = Qpos PSD, repairing negative part by adding Qneg to positive side
    repaired=Q+Qneg
    rows.append({
      'n':n,'trial':trial,
      'min_eig_Q':float(evals[0]),
      'neg_trace_repair':float(np.trace(Qneg)),
      'min_eig_repaired':float(np.linalg.eigvalsh(repaired)[0]),
      'reconstruction_error':float(np.linalg.norm(Q-(Qpos-Qneg)))
    })
pd.DataFrame(rows).to_csv(out/'signed_component_repair_step76.csv',index=False)

# 4. Shift symbol positivity example for finite positive measure
xis=np.linspace(-10,10,401)
shifts=np.array([np.log(2),np.log(3),np.log(5),np.log(7)])
weights=np.array([1/np.sqrt(2), np.log(3)/np.sqrt(3), np.log(5)/np.sqrt(5), np.log(7)/np.sqrt(7)])
rows=[]
for xi in xis:
    psi=float(2*np.sum(weights*(1-np.cos(shifts*xi))))
    rows.append({'xi':xi,'psi_shift_symbol':psi})
pd.DataFrame(rows).to_csv(out/'shift_symbol_positive_step76.csv',index=False)

# 5. Douglas equivalence random checks: A <= K iff K-A PSD. Build and measure contraction norm via K^{-1/2} A K^{-1/2}
rows=[]
for n in [3,5,8]:
  for trial in range(20):
    R=rng.normal(size=(n,n)); K=R@R.T + np.eye(n)
    # choose C<=I in K geometry
    vals=rng.uniform(0,0.95,size=n)
    U,_=np.linalg.qr(rng.normal(size=(n,n)))
    C=U@np.diag(vals)@U.T
    evalsK,UK=np.linalg.eigh(K)
    Khalf=UK@np.diag(np.sqrt(evalsK))@UK.T
    A=Khalf@C@Khalf
    min_slack=float(np.linalg.eigvalsh(K-A)[0])
    # Douglas contraction norm squared is max eig(K^{-1/2} A K^{-1/2})
    Kinvhalf=UK@np.diag(1/np.sqrt(evalsK))@UK.T
    norm2=float(np.linalg.eigvalsh(Kinvhalf@A@Kinvhalf).max())
    rows.append({'n':n,'trial':trial,'min_eig_K_minus_A':min_slack,'contraction_norm_squared':norm2,'contraction_norm':np.sqrt(norm2)})
pd.DataFrame(rows).to_csv(out/'douglas_positive_feature_checks_step76.csv',index=False)

print('wrote step76 checks')
