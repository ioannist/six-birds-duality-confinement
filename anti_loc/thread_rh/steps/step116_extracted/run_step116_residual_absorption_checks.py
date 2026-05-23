
import numpy as np

def min_eig(A):
    A=(A+A.conj().T)/2
    return np.linalg.eigvalsh(A).min()

rng=np.random.default_rng(116)
for d in [4,8,12,16]:
    A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    G=A.conj().T@A+np.eye(d)
    c=0.25
    gamma=2.0
    C=c*G+0.1*np.eye(d)
    F=gamma*C
    assert min_eig(F-gamma*c*G) > -1e-9
    Xi=0.5*G
    assert min_eig((0.5/(gamma*c))*F-Xi) > -1e-9
print('Step 116 finite residual absorption checks passed.')
