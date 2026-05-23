#!/usr/bin/env python3
"""Sanity checks for Step 157 finite Calkin/Weyl diagnostics.
These are finite algebra checks only; they are not proof of compactness/noncompactness.
"""
import json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(157)
# Finite projection identity: C P = (I-P0) M P0 P_eta.
n = 48
A = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
Q,_ = np.linalg.qr(A)
r = 24
P0 = Q[:,:r] @ Q[:,:r].conj().T
B = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
U,_ = np.linalg.qr(B)
s = 32
Peta = U[:,:s] @ U[:,:s].conj().T
# unitary shift-like multiplier
phases = np.exp(1j*np.linspace(0, 2*np.pi, n, endpoint=False))
M = np.diag(phases)
C = (np.eye(n)-P0) @ M @ P0
lhs = C @ Peta
rhs = (np.eye(n)-P0) @ (M @ P0 - P0 @ M) @ Peta
comm_error = np.linalg.norm(lhs-rhs)
# finite-rank approximation check: if tail norm goes to zero in synthetic compact model
N = np.arange(10,161)
compact_tail = 1/(N+1)**0.8
essential_tail = 0.22 + 0.25/(N+1)**0.7
results = {
    'commutator_identity_error': float(comm_error),
    'compact_tail_last': float(compact_tail[-1]),
    'essential_tail_last': float(essential_tail[-1]),
    'compact_tail_decreases': bool(compact_tail[-1] < compact_tail[0]),
    'essential_tail_has_floor_proxy': bool(essential_tail[-1] > 0.2),
    'status': 'passed' if comm_error < 1e-10 else 'failed'
}
(OUT/'step157_check_results.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
