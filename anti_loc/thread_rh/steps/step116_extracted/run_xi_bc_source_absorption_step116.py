#!/usr/bin/env python3
"""Finite sanity checks for Step 116."""
import numpy as np
rng = np.random.default_rng(116)
for d in [4,8,16,32]:
    A = rng.standard_normal((d,d))
    Gamma = A.T@A + np.eye(d)
    B = rng.standard_normal((d,d))
    Xi = B.T@B
    # scale Xi so Xi <= Gamma
    vals = np.linalg.eigvalsh(np.linalg.solve(np.linalg.cholesky(Gamma), Xi) @ np.linalg.inv(np.linalg.cholesky(Gamma)).T)
    scale = max(vals.max(),1e-9)
    Xi = Xi/(1.5*scale)
    assert np.linalg.eigvalsh(Gamma-Xi).min() > -1e-7
    Lambda = 10.0
    R = np.zeros_like(Gamma)
    F = Lambda*Gamma
    slack = (1/Lambda)*F - Xi
    assert np.linalg.eigvalsh(slack).min() > -1e-7
print('Step 116 finite source absorption checks passed.')
