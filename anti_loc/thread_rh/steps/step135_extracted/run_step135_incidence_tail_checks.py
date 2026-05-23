#!/usr/bin/env python3
import numpy as np
phi=(1+5**0.5)/2
J=np.array([[1,0],[1,1]],float)
for k in range(1,8):
    Z=np.array([[1.0]])
    for _ in range(k):
        Z=np.kron(Z,J)
    s=np.linalg.svd(Z, compute_uv=False)
    assert abs(s[0]-phi**k)/phi**k < 1e-10
    assert abs(s[-1]-phi**(-k))/phi**(-k) < 1e-10
print('incidence singular-value checks passed')
