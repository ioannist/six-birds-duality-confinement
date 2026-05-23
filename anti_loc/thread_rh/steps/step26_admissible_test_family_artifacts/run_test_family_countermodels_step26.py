#!/usr/bin/env python3
"""Small algebraic countermodels for Step 26.

These are not Six Birds simulations. They only illustrate the finite-dimensional
matrix statements in the proof note.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

out = Path(__file__).resolve().parent

# Diagonal route-local budgets vs block-union budget: K=1_r 1_r^T.
with open(out / "protocol_diagonal_vs_block_countermodel_step26.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["num_protocols", "max_diagonal_capacity", "block_top_eigenvalue", "overread_factor"])
    for r in [1,2,3,4,5,8,10,16,32,64]:
        max_diag = 1.0
        top = float(r)
        w.writerow([r, max_diag, top, top / max_diag])

# Readout transfer bound: Kq <= (1+t)Kp + (1+1/t)D in scalar case.
# Let Kp=1, D=delta. Minimize over t: (sqrt(Kp)+sqrt(D))^2.
with open(out / "readout_transfer_bound_step26.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["defect_delta", "best_t", "optimal_transfer_bound", "naive_sum_bound"])
    for delta in [0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.25, 1.0]:
        if delta == 0:
            best_t = "infty"
            opt = 1.0
        else:
            # minimize (1+t)K + (1+1/t)D => t=sqrt(D/K)
            t = math.sqrt(delta)
            best_t = t
            opt = (1 + math.sqrt(delta))**2
        naive = 1.0 + delta
        w.writerow([delta, best_t, opt, naive])

print("Wrote Step 26 countermodel CSVs.")
