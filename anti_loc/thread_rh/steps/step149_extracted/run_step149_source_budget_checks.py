#!/usr/bin/env python3
"""Sanity checks for Step 149 no-free source-budget identities."""
import numpy as np

rng = np.random.default_rng(149)
for d in [4, 8, 16]:
    A = rng.normal(size=(d,d))
    G = A.T @ A + np.eye(d)*0.2
    B = rng.normal(size=(d,d))
    P = B.T @ B
    Lam = 7.0
    F = Lam*G + P
    C = rng.normal(size=(d,d))
    K = C.T @ C
    lhs = np.trace(F @ K)/Lam
    rhs = np.trace(G @ K)
    if lhs + 1e-9 < rhs:
        raise SystemExit(f"failed lower-bound check at d={d}: {lhs} < {rhs}")
print("Step 149 checks passed: tr(FK)/Lambda >= tr(GK).")
