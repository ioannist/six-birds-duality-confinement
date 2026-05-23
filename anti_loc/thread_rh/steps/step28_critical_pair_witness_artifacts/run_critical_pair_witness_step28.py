#!/usr/bin/env python3
"""Small finite examples for Step 28 critical-pair/recombination witnesses.
These are not Six Birds simulations; they are sanity checks for the matrix witness theorems.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def eigmax(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((A + A.conj().T) / 2)[-1])


def eigvals(A: np.ndarray):
    return np.linalg.eigvalsh((A + A.conj().T) / 2)


def support_minimal(D: np.ndarray):
    n = D.shape[0]
    witnesses = []
    for mask in range(1, 1 << n):
        S = [i for i in range(n) if (mask >> i) & 1]
        DS = D[np.ix_(S, S)]
        if eigmax(DS) <= 1e-10:
            continue
        minimal = True
        for j in S:
            T = [i for i in S if i != j]
            if T and eigmax(D[np.ix_(T, T)]) > 1e-10:
                minimal = False
                break
        if minimal:
            w, V = np.linalg.eigh(DS)
            v = V[:, -1]
            y = np.zeros(n)
            for idx, i in enumerate(S):
                y[i] = v[idx]
            witnesses.append((S, eigmax(DS), y))
    return witnesses


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def two_anchor_sweep():
    rows = []
    a = b = -1.0
    cs = np.linspace(0.0, 1.5, 61)
    for c in cs:
        D = np.array([[a, c], [c, b]], dtype=float)
        rows.append({
            'c': c,
            'determinant': float(np.linalg.det(D)),
            'lambda_max': eigmax(D),
            'is_witness': bool(eigmax(D) > 1e-10),
            'criterion_c2_gt_ab': bool(c * c > a * b),
        })
    write_csv(OUT / 'two_anchor_sweep_step28.csv', rows)
    plt.figure(figsize=(7, 4))
    plt.plot([r['c'] for r in rows], [r['lambda_max'] for r in rows])
    plt.axhline(0, linestyle='--')
    plt.xlabel('off-diagonal coupling c')
    plt.ylabel('largest eigenvalue of D')
    plt.title('Two-anchor critical-pair threshold')
    plt.tight_layout()
    plt.savefig(OUT / 'two_anchor_threshold_step28.png', dpi=160)
    plt.close()


def minimal_cycle_table(max_k: int = 10):
    rows = []
    for k in range(2, max_k + 1):
        if k == 2:
            c = 1.1
        else:
            c = 0.5 * (1.0 / (k - 1) + 1.0 / (k - 2))
        J = np.ones((k, k))
        D = -np.eye(k) + c * (J - np.eye(k))
        witnesses = support_minimal(D)
        max_proper = max(eigmax(D[np.ix_([i for i in range(k) if i != j], [i for i in range(k) if i != j])]) for j in range(k)) if k > 1 else np.nan
        rows.append({
            'k': k,
            'c': c,
            'lambda_max_full': eigmax(D),
            'lambda_max_largest_proper': max_proper,
            'num_minimal_witnesses': len(witnesses),
            'support_sizes': ';'.join(str(len(w[0])) for w in witnesses),
        })
    write_csv(OUT / 'minimal_cycle_family_step28.csv', rows)
    plt.figure(figsize=(7, 4))
    plt.plot([r['k'] for r in rows], [r['lambda_max_full'] for r in rows], marker='o', label='full support')
    plt.plot([r['k'] for r in rows], [r['lambda_max_largest_proper'] for r in rows], marker='o', label='largest proper support')
    plt.axhline(0, linestyle='--')
    plt.xlabel('cycle/support size k')
    plt.ylabel('largest eigenvalue')
    plt.title('Support-minimal k-anchor witnesses')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / 'minimal_cycle_witness_step28.png', dpi=160)
    plt.close()


def protocol_mixed_example():
    # Two route/protocol blocks, each individually safe, with cross-block coupling.
    D = np.array([[-1.0, 0.0, 1.25, 0.0],
                  [0.0, -1.0, 0.0, 0.6],
                  [1.25, 0.0, -1.0, 0.0],
                  [0.0, 0.6, 0.0, -1.0]], dtype=float)
    rows = []
    blocks = {'p1': [0, 1], 'p2': [2, 3]}
    for name, idx in blocks.items():
        rows.append({'case': name, 'lambda_max': eigmax(D[np.ix_(idx, idx)]), 'status': 'local_pass' if eigmax(D[np.ix_(idx, idx)]) <= 0 else 'local_fail'})
    rows.append({'case': 'stacked_protocol_union', 'lambda_max': eigmax(D), 'status': 'global_fail' if eigmax(D) > 0 else 'global_pass'})
    witnesses = support_minimal(D)
    for n, (S, lam, y) in enumerate(witnesses):
        rows.append({'case': f'minimal_witness_{n}', 'lambda_max': lam, 'status': 'support=' + ','.join(map(str, S))})
    write_csv(OUT / 'protocol_marked_witness_step28.csv', rows)


def predictive_example():
    rows = []
    for j in range(1, 51):
        D = np.diag([-0.1, j / 10.0 - 1.0])
        rows.append({'j': j, 'lambda_max': eigmax(D), 'is_predictive_witness': bool(eigmax(D) > 0)})
    write_csv(OUT / 'predictive_witness_growth_step28.csv', rows)
    plt.figure(figsize=(7, 4))
    plt.plot([r['j'] for r in rows], [r['lambda_max'] for r in rows])
    plt.axhline(0, linestyle='--')
    plt.xlabel('refinement level j')
    plt.ylabel('largest eigenvalue of K_j - Theta')
    plt.title('Predictive witness emergence')
    plt.tight_layout()
    plt.savefig(OUT / 'predictive_witness_growth_step28.png', dpi=160)
    plt.close()


def schema():
    data = {
        'record': 'CriticalPairWitness',
        'fields': {
            'response_space': 'finite native response family Y',
            'currency_matrix': 'K = L_Gamma C_Gamma^dagger L_Gamma^*',
            'budget': 'Theta',
            'defect': 'D = K - Theta',
            'witness': 'y with y^* D y > 0',
            'support': 'minimal support S when coordinate/frame is declared',
            'type': ['scalar', 'two_anchor', 'cyclic', 'protocol_marked', 'predictive', 'shadow', 'post_hoc'],
            'lawful_actions': ['rewrite_probe_family', 'rewrite_carrier_or_audit', 'raise_budget_or_weaken_claim', 'downgrade_status'],
        },
        'accepted_gate': 'No critical-pair witnesses: K <= Theta',
    }
    (OUT / 'critical_pair_witness_schema_step28.json').write_text(json.dumps(data, indent=2))


def theorem_map():
    rows = [
        {'theorem': 'Witness theorem', 'input': 'K,Theta finite Hermitian', 'output': 'K not <= Theta iff exists y with positive excess', 'role': 'complete obstruction record'},
        {'theorem': 'Minimal witness existence', 'input': 'declared coordinate/frame', 'output': 'support-minimal witness; exactly one positive eigenvalue on minimal support', 'role': 'critical pair localization'},
        {'theorem': 'Two-anchor criterion', 'input': '2x2 defect block with safe diagonals', 'output': '|c|^2 > ab iff cancellation witness', 'role': 'relative-cycle / cancellation needle'},
        {'theorem': 'Minimal k-cycle family', 'input': 'D=-I+c(J-I)', 'output': 'minimal k-anchor witness', 'role': 'higher recombination cycle'},
        {'theorem': 'Protocol-marked theorem', 'input': 'safe protocol diagonal blocks, unsafe full block', 'output': 'minimal witness crosses protocols', 'role': 'route-local overclaim'},
        {'theorem': 'Predictive witness theorem', 'input': 'K_j sequence, common Theta', 'output': 'predictive failure iff exists future witness', 'role': 'current-only overclaim'},
        {'theorem': 'Completion obligation', 'input': 'accepted claim plus witness', 'output': 'must rewrite, raise budget, exclude, or downgrade', 'role': 'Knuth-Bendix / closure discipline'},
    ]
    write_csv(OUT / 'theorem_map_step28.csv', rows)


def main():
    two_anchor_sweep()
    minimal_cycle_table()
    protocol_mixed_example()
    predictive_example()
    schema()
    theorem_map()

if __name__ == '__main__':
    main()
