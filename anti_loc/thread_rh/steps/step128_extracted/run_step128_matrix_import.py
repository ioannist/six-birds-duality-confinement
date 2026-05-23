#!/usr/bin/env python3
"""Step 128 sanity checks: theorem algebra only, not RH evidence."""
import numpy as np
rng = np.random.default_rng(128)
for d in [8, 16, 32]:
    X = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    Q, _ = np.linalg.qr(X)
    weights = np.exp(0.3*rng.normal(size=d))
    G = Q.conj().T @ np.diag(weights) @ Q
    lam_min = np.linalg.eigvalsh((G+G.conj().T)/2).min()
    assert lam_min > 0
print('Step 128 weighted-Gram PSD sanity checks passed.')
