import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step106_boundary_source_absorption')
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(106)

# Toy model: completed response space with boundary sector of rank b inside N-dimensional truncations.
# Delta^+ acts as identity on boundary sector plus compact tail on complement.
N = 240
b = 90
ranks = np.arange(10, N + 1, 10)

boundary = np.zeros(N)
boundary[:b] = 1.0
compact_tail = np.exp(-np.arange(N) / 28.0) * 0.22
Delta_diag = boundary + compact_tail

# Full source frame charges all boundary modes with Lambda_n.
Lambda = np.log1p(ranks) ** 1.6
full_residual_norm = []
partial_residual_norm = []
moving_window_residual_norm = []
compact_tail_norm = []

for r, lam in zip(ranks, Lambda):
    # Full coverage frame: lam on every boundary mode up to N, plus none on compact complement.
    source_full = lam * boundary
    residual_full = np.maximum(Delta_diag - source_full, 0.0)
    full_residual_norm.append(residual_full.max())

    # Partial coverage: misses the last 25 boundary modes.
    partial_mask = np.zeros(N)
    partial_mask[: max(0, b - 25)] = 1.0
    source_partial = lam * partial_mask
    residual_partial = np.maximum(Delta_diag - source_partial, 0.0)
    partial_residual_norm.append(residual_partial.max())

    # Moving window: covers only first r modes; if r < b, boundary tail remains.
    moving_mask = np.zeros(N)
    moving_mask[:min(r, N)] = 1.0
    source_moving = lam * moving_mask
    residual_moving = np.maximum(Delta_diag - source_moving, 0.0)
    moving_window_residual_norm.append(residual_moving.max())

    # Compact tail after projection to r modes.
    compact_tail_norm.append(compact_tail[min(r, N-1):].max() if r < N else 0.0)

# Boundary absorption CSV
import csv
with open(OUT / 'boundary_source_absorption_model_step106.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank_window', 'Lambda', 'full_residual_norm', 'partial_residual_norm', 'moving_window_residual_norm', 'compact_tail_norm'])
    for row in zip(ranks, Lambda, full_residual_norm, partial_residual_norm, moving_window_residual_norm, compact_tail_norm):
        w.writerow(row)

plt.figure(figsize=(7, 4.5))
plt.plot(ranks, full_residual_norm, marker='o', label='full boundary source coverage')
plt.plot(ranks, partial_residual_norm, marker='s', label='partial source coverage')
plt.plot(ranks, moving_window_residual_norm, marker='^', label='moving window without tail')
plt.xlabel('finite window rank')
plt.ylabel('residual positive norm after source payment')
plt.title('Boundary-packet source absorption model')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'boundary_source_absorption_model_step106.png', dpi=160)
plt.close()

plt.figure(figsize=(7, 4.5))
plt.semilogy(ranks, compact_tail_norm, marker='o')
plt.xlabel('finite window rank')
plt.ylabel('compact tail norm')
plt.title('Compact tail vanishes under exhaustive windows')
plt.tight_layout()
plt.savefig(OUT / 'compact_tail_vanishing_step106.png', dpi=160)
plt.close()

# Mollifier strength toy based on cumulative sum over prime bands.
# Use actual primes up to a moderate size; lambda model ~ sum 1/p by source blocks, slow divergence.
def primes_upto(n):
    sieve = np.ones(n+1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5)+1):
        if sieve[p]:
            sieve[p*p:n+1:p] = False
    return np.nonzero(sieve)[0]

ps = primes_upto(20000)
cutoffs = np.array([50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
lam_moll = []
for c in cutoffs:
    psel = ps[ps <= c]
    lam_moll.append(float(np.sum(1.0 / psel)))
lam_moll = np.array(lam_moll)
# A more optimistic weighted/source-replicated ladder multiplies by number of lawful independent character shells.
replication = np.log1p(cutoffs) / np.log(10)
lam_replicated = lam_moll * replication

with open(OUT / 'mollifier_source_strength_model_step106.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['cutoff', 'sum_1_over_p', 'replication_factor', 'replicated_strength'])
    for row in zip(cutoffs, lam_moll, replication, lam_replicated):
        w.writerow(row)

plt.figure(figsize=(7, 4.5))
plt.plot(cutoffs, lam_moll, marker='o', label='prime-band scalar strength sum 1/p')
plt.plot(cutoffs, lam_replicated, marker='s', label='toy replicated character-shell strength')
plt.xscale('log')
plt.xlabel('prime cutoff')
plt.ylabel('source strength proxy')
plt.title('Scalar-to-operator source strength proxy')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'mollifier_source_strength_model_step106.png', dpi=160)
plt.close()

# Finite character tight frame vs partial subset check.
mods = [5, 7, 11, 13, 17, 19]
rows = []
for q in mods:
    # Use cyclic group of order q-1 as toy for unit group if q prime.
    m = q - 1
    j = np.arange(m)
    chars = []
    for k in range(m):
        chars.append(np.exp(2j * np.pi * k * j / m) / np.sqrt(m))
    U = np.vstack(chars)
    F_full = U.conj().T @ U
    full_err = np.linalg.norm(F_full - np.eye(m), 2)
    subset = max(1, m // 2)
    F_partial = U[:subset].conj().T @ U[:subset]
    eig_partial = np.linalg.eigvalsh(F_partial).min()
    rows.append((q, m, full_err, subset, eig_partial))
with open(OUT / 'finite_character_frame_toy_step106.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['prime_modulus_q', 'group_order', 'full_frame_identity_error', 'partial_subset_size', 'partial_min_eigenvalue'])
    for row in rows:
        w.writerow(row)

plt.figure(figsize=(7,4.5))
plt.plot([r[0] for r in rows], [r[2] for r in rows], marker='o', label='full frame identity error')
plt.plot([r[0] for r in rows], [max(r[4], 1e-16) for r in rows], marker='s', label='partial min eigenvalue')
plt.yscale('log')
plt.xlabel('prime modulus q')
plt.ylabel('error / min eigenvalue')
plt.title('Finite character frame: full exact, partial fails')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'finite_character_frame_toy_step106.png', dpi=160)
plt.close()

# Write compact verification JSON
verification = {
    'full_residual_norm_final': float(full_residual_norm[-1]),
    'partial_residual_norm_final': float(partial_residual_norm[-1]),
    'moving_residual_norm_final': float(moving_window_residual_norm[-1]),
    'compact_tail_norm_final': float(compact_tail_norm[-1]),
    'max_full_frame_identity_error': float(max(r[2] for r in rows)),
    'min_partial_eigenvalue_across_examples': float(min(r[4] for r in rows)),
    'note': 'Toy algebra only; not RH evidence.'
}
with open(OUT / 'verification_step106.json', 'w') as f:
    json.dump(verification, f, indent=2)
print(json.dumps(verification, indent=2))
