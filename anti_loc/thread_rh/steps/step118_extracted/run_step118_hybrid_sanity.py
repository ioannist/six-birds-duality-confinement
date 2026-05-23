#!/usr/bin/env python3
"""
Step 118 sanity checks.

These checks are finite-dimensional algebra only. They do not simulate Six Birds and are not RH evidence.
They verify the identities:
  c_N = 1 - ||E G^{-1/2}||^2
and the qualitative effect of Burnol-to-Dirichlet shadow defects.
"""
import numpy as np

def projection(A):
    Q, _ = np.linalg.qr(A)
    return Q @ Q.T

def visibility_constant(M, D):
    G = M.T @ M + 1e-10*np.eye(M.shape[1])
    P = projection(D)
    E = (np.eye(M.shape[0]) - P) @ M
    vals = np.linalg.eigvalsh(np.linalg.solve(G, E.T @ E))
    eps2 = max(vals)
    return max(0.0, 1.0 - eps2), eps2

if __name__ == "__main__":
    rng = np.random.default_rng(118)
    H, R, B, C = 48, 10, 16, 32
    M = rng.normal(size=(H, R))
    Burnol = rng.normal(size=(H, B))
    Dir = rng.normal(size=(H, C))
    A = np.linalg.lstsq(Dir, Burnol, rcond=None)[0]
    Shadow = Dir @ A
    Hybrid = np.concatenate([Dir, Shadow], axis=1)

    c_dir, eps2_dir = visibility_constant(M, Dir)
    c_hyb, eps2_hyb = visibility_constant(M, Hybrid)
    delta = np.linalg.norm(Burnol - Shadow, 2) / (np.linalg.norm(Burnol, 2) + 1e-12)

    print({"c_dir": c_dir, "c_hybrid": c_hyb, "shadow_defect": delta})
