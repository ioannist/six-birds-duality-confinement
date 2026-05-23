import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step90_source_family_audit')

# Toy source-frame models illustrating the gates, not zeta simulations.
N = 64
stages = np.arange(1, 65)

# Full orthogonal character coverage: all N directions get strength n.
full_lambda = stages.astype(float)
full_budget = 1.0 / full_lambda

# Partial coverage: first half charged, second half not; full lower frame remains zero.
partial_lower = np.zeros_like(stages, dtype=float)
partial_budget = np.full_like(stages, np.inf, dtype=float)

# Moving window: finite prefix charged, no tail bridge; local lower frame grows, global remains zero.
window_size = np.minimum(stages, N)
window_local_lambda = stages.astype(float)
window_global_lower = np.where(window_size == N, stages.astype(float), 0.0)

# Exhaustive tail bridge toy: window grows and tail mass decays.
tail = np.exp(-stages / 12.0)
exhaustive_bound = 1.0 / full_lambda + tail

pd.DataFrame({
    'stage': stages,
    'full_frame_lambda': full_lambda,
    'full_frame_budget': full_budget,
    'partial_frame_lower_bound': partial_lower,
    'moving_window_size': window_size,
    'moving_window_local_lambda': window_local_lambda,
    'moving_window_global_lower_without_tail': window_global_lower,
    'exhaustive_tail': tail,
    'exhaustive_total_bound': exhaustive_bound,
}).to_csv(out/'source_frame_toy_models_step90.csv', index=False)

# Candidate scoring table purely qualitative numerical display
candidates = ['prime', 'Dirichlet/Hecke', 'trace formula', 'automorphic', 'de Branges', 'trace-only']
coverage = np.array([0.45, 0.85, 0.70, 0.80, 0.65, 0.15])
upstream = np.array([0.95, 0.85, 0.60, 0.65, 0.55, 0.90])
carrier_burden = np.array([0.25, 0.65, 0.80, 0.95, 0.85, 0.15])
status_score = coverage * upstream * (1 - 0.35*carrier_burden)
pd.DataFrame({
    'candidate': candidates,
    'qualitative_coverage_score': coverage,
    'upstream_visibility_score': upstream,
    'carrier_burden_score': carrier_burden,
    'illustrative_status_score': status_score,
}).to_csv(out/'source_candidate_scores_step90.csv', index=False)

# Plots
plt.figure(figsize=(6,4))
plt.plot(stages, full_budget, label='full-sector budget 1/Lambda')
plt.plot(stages, exhaustive_bound, label='exhaustive bound 1/Lambda + tail')
plt.yscale('log')
plt.xlabel('stage')
plt.ylabel('certified obstruction budget')
plt.title('Full-sector source ladder vs exhaustive tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'source_ladder_budget_step90.png', dpi=180)
plt.close()

plt.figure(figsize=(6,4))
plt.plot(stages, partial_lower, label='partial character lower frame')
plt.plot(stages, window_global_lower, label='moving-window global lower frame')
plt.plot(stages, full_lambda, label='full-sector lower frame')
plt.xlabel('stage')
plt.ylabel('full-space lower-frame constant')
plt.title('Partial/moving-window sources do not give full frame')
plt.legend()
plt.tight_layout()
plt.savefig(out/'partial_moving_frame_failure_step90.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4))
x = np.arange(len(candidates))
plt.bar(x, status_score)
plt.xticks(x, candidates, rotation=30, ha='right')
plt.ylabel('illustrative structural score')
plt.title('Candidate source-family audit (illustrative only)')
plt.tight_layout()
plt.savefig(out/'source_candidate_scores_step90.png', dpi=180)
plt.close()

print('wrote step90 artifacts')
