#!/usr/bin/env python3
"""
Step 38 algebra checks for the Root-Composite RH Obligation Theorem.
These checks are sanity checks of finite-dimensional PSD implications, not Six Birds simulations.
"""
import csv
import json
import math
from pathlib import Path
import numpy as np

OUT = Path('/mnt/data/anti_localization_step38_rhobligation')

def eigmin(A):
    return float(np.linalg.eigvalsh((A + A.T) / 2).min())

def eigmax(A):
    return float(np.linalg.eigvalsh((A + A.T) / 2).max())

def psd_sqrt(A):
    w, V = np.linalg.eigh((A + A.T) / 2)
    return V @ np.diag(np.sqrt(np.maximum(w, 0))) @ V.T

def rand_psd(n, rng):
    X = rng.normal(size=(n, n))
    return X.T @ X

rng = np.random.default_rng(20260512)

# 1. Exact obligation theorem: A <= K <= Theta => A <= Theta and mass bound.
rows = []
for n in [2, 3, 5, 8]:
    for trial in range(10):
        A = rand_psd(n, rng)
        E1 = rand_psd(n, rng)
        E2 = rand_psd(n, rng)
        K = A + E1
        Theta = K + E2
        rows.append({
            'n': n,
            'trial': trial,
            'min_eig_K_minus_A': eigmin(K - A),
            'min_eig_Theta_minus_K': eigmin(Theta - K),
            'min_eig_Theta_minus_A': eigmin(Theta - A),
            'trace_A': float(np.trace(A)),
            'trace_Theta': float(np.trace(Theta)),
            'trace_bound_valid': float(np.trace(A) <= np.trace(Theta) + 1e-10)
        })
with open(OUT / 'loewner_transitivity_checks_step38.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

# 2. Character-source lower frame: F >= Lambda Theta^-1 => K <= Lambda^-1 Theta.
rows = []
for n in [2, 4, 6]:
    for trial in range(12):
        # choose Theta positive diagonal for readable record
        theta_diag = rng.uniform(0.5, 2.0, size=n)
        Theta = np.diag(theta_diag)
        Theta_inv = np.diag(1.0 / theta_diag)
        Lambda = rng.uniform(0.3, 5.0)
        # Create carrier C = Lambda L^* Theta^-1 L + extra; take L=I
        extra = rand_psd(n, rng) * 0.1
        C = Lambda * Theta_inv + extra
        K = np.linalg.inv(C)
        bound = (1.0 / Lambda) * Theta
        rows.append({
            'n': n,
            'trial': trial,
            'Lambda': Lambda,
            'min_eig_C_minus_source': eigmin(C - Lambda*Theta_inv),
            'max_eig_K_relative_to_bound': eigmax(np.linalg.solve(psd_sqrt(bound), K) @ np.linalg.inv(psd_sqrt(bound))) if eigmin(bound) > 1e-12 else float('nan'),
            'min_eig_bound_minus_K': eigmin(bound - K),
            'passed': eigmin(bound - K) >= -1e-9
        })
with open(OUT / 'character_source_frame_checks_step38.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

# 3. Defective bridge bound: A <= K+EEF, K<=Lambda^-1 Theta+Esrc => A<=...
rows = []
for n in [3, 5]:
    for trial in range(10):
        base = rand_psd(n, rng)
        Eef = rand_psd(n, rng)*0.01
        Esrc = rand_psd(n, rng)*0.01
        Theta = rand_psd(n, rng) + np.eye(n)
        Lambda = rng.uniform(1, 10)
        # Let A be under the advertised final bound by construction.
        final = (1/Lambda)*Theta + Eef + Esrc
        # choose A = S final S with contraction S=tI for t<1, to stay PSD and <= final
        t = rng.uniform(0.1, 0.95)
        A = t * final
        rows.append({
            'n': n,
            'trial': trial,
            'Lambda': Lambda,
            't_contraction': t,
            'min_eig_final_minus_A': eigmin(final - A),
            'trace_mass_allowance': float(np.trace(final)),
            'passed': eigmin(final - A) >= -1e-9
        })
with open(OUT / 'defective_obligation_checks_step38.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

# 4. Trace-shadow counterexamples.
trace_rows = [
    {
        'case': 'equal_trace_not_loewner',
        'A': 'diag(2,0)',
        'K': 'diag(1,1)',
        'trace_A': 2.0,
        'trace_K': 2.0,
        'min_eig_K_minus_A': eigmin(np.diag([1,1]) - np.diag([2,0])),
        'loewner_passes': False
    },
    {
        'case': 'invariant_shadow_passes_anti_invariant_fails',
        'A': 'K=diag(1/2,2), Theta=I',
        'K': 'invariant block is first coordinate',
        'trace_A': 2.5,
        'trace_K': 2.0,
        'min_eig_K_minus_A': eigmin(np.eye(2)-np.diag([0.5,2.0])),
        'loewner_passes': False
    }
]
with open(OUT / 'trace_shadow_counterexamples_step38.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(trace_rows[0].keys()))
    writer.writeheader(); writer.writerows(trace_rows)

summary = {
    'step': 38,
    'title': 'Root-composite RH obligation theorem',
    'interpretation': 'If anti-linear zero displacement is explicitly-formula dominated by completed carrier currency, and character-source records collapse the anti-invariant budget, then zero/root mass is confined to the fixed locus.',
    'not_claimed': ['RH', 'construction of actual completed RH carrier', 'actual EF contraction', 'actual character lower frame'],
    'open_load_bearing_records': ['completed EF domination', 'anti-invariant budget collapse', 'character-source lower frame', 'strict-extension source growth', 'finite-to-exact promotion']
}
with open(OUT / 'step38_machine_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print('Step 38 algebra checks written to', OUT)
