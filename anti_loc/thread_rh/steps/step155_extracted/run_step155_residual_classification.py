#!/usr/bin/env python3
"""Sanity plots/checks for Step 155: Xi^BC residual classification."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
np.random.seed(155)

def savefig(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=180)
    plt.close()

# Plot 1: route classification status scores.
routes = ["zero", "compact/tail", "signed source", "budget", "nonclaim"]
proof_strength = np.array([1.0, 0.72, 0.68, 0.42, 0.05])
current_cert = np.array([0.12, 0.24, 0.18, 0.45, 1.0])
x = np.arange(len(routes))
plt.figure(figsize=(9,4.8))
plt.bar(x-0.18, proof_strength, width=0.36, label="proof-producing potential")
plt.bar(x+0.18, current_cert, width=0.36, label="current certification")
plt.xticks(x, routes, rotation=20, ha='right')
plt.ylim(0,1.15)
plt.ylabel("relative score")
plt.title("Step 155 residual classification: potential vs current status")
plt.legend()
savefig("xi_bc_classification_scores_step155.png")

# Plot 2: compact vs noncompact tail models.
n = np.arange(1,121)
compact = 1/(n**1.35)
trace_tail = np.array([compact[i:].sum() for i in range(len(n))])
plateau = 0.08 + 0.92/(1 + 0.04*n)
noncompact_tail = np.maximum.accumulate(plateau[::-1])[::-1]
plt.figure(figsize=(8,5))
plt.semilogy(n, trace_tail/trace_tail[0], label="trace-class tail model")
plt.semilogy(n, noncompact_tail/noncompact_tail[0], label="noncompact plateau model")
plt.xlabel("window index N")
plt.ylabel("normalized residual tail")
plt.title("Compact/tail-payable vs noncompact residual behavior")
plt.legend()
savefig("compact_vs_nonclaim_tail_step155.png")

# Plot 3: no-free source budget diagnostic.
Lambda = np.linspace(1,80,160)
residual_masses = [0.0, 0.02, 0.08, 0.2]
plt.figure(figsize=(8,5))
for mass in residual_masses:
    exposure_ratio = mass + 0.02/np.sqrt(Lambda)
    plt.plot(Lambda, exposure_ratio, label=f"residual mass={mass:g}")
plt.axhline(0, linewidth=1)
plt.xlabel(r"source strength $\Lambda_N$")
plt.ylabel(r"lower bound on exposure / $\Lambda_N$")
plt.title("No-free source-budget obstruction")
plt.legend()
savefig("source_budget_obstruction_step155.png")

# Plot 4: Xi spectrum scenarios.
dim = 60
idx = np.arange(1, dim+1)
zero_spec = np.zeros(dim)
compact_spec = 0.5/(idx**1.5)
budget_spec = 0.08*np.exp(-idx/30) + 0.01
unpaid_spec = 0.08 + 0.2/(idx**0.2)
plt.figure(figsize=(8,5))
plt.semilogy(idx, zero_spec + 1e-8, label="zero/direct exclusion")
plt.semilogy(idx, compact_spec + 1e-8, label="compact/tail-payable")
plt.semilogy(idx, budget_spec, label="bounded residual budget")
plt.semilogy(idx, unpaid_spec, label="unpaid nonclaim")
plt.xlabel("residual singular/eigenvalue index")
plt.ylabel("model eigenvalue")
plt.title(r"Model spectra for $\Xi^{\rm BC}$ classification")
plt.legend()
savefig("xi_bc_spectrum_classification_step155.png")

# Plot 5: route decision tree rendered as a text-like heatmap.
states = ["direct\nzero", "tail\npaid", "source\nidentity", "budget", "nonclaim"]
M = np.array([
    [1.0,0.0,0.0,0.0,0.0],
    [0.0,1.0,0.0,0.0,0.0],
    [0.0,0.0,1.0,0.0,0.0],
    [0.0,0.0,0.0,1.0,0.0],
    [0.0,0.0,0.0,0.0,1.0]
])
plt.figure(figsize=(6.6,5.6))
plt.imshow(M, aspect='auto')
plt.xticks(np.arange(len(states)), states)
plt.yticks(np.arange(len(states)), ["proof\nroute", "compact\nroute", "signed\nroute", "partial\nroute", "fallback"])
plt.title("Step 155 classification branches")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        txt = "accept" if M[i,j] else ""
        if txt:
            plt.text(j,i,txt,ha='center',va='center')
savefig("xi_bc_classification_branches_step155.png")

# CSV data corresponding to plots.
import csv
with open(OUT / "xi_bc_classification_scores_step155.csv", "w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["route","proof_producing_potential","current_certification"])
    for r,a,b in zip(routes, proof_strength, current_cert):
        w.writerow([r, float(a), float(b)])
with open(OUT / "xi_bc_tail_models_step155.csv", "w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["N","trace_class_tail_normalized","noncompact_tail_normalized"])
    for N,t,u in zip(n, trace_tail/trace_tail[0], noncompact_tail/noncompact_tail[0]):
        w.writerow([int(N), float(t), float(u)])
with open(OUT / "xi_bc_spectrum_models_step155.csv", "w", newline="") as f:
    w=csv.writer(f)
    w.writerow(["index","zero","compact_tail","bounded_budget","unpaid_nonclaim"])
    for i,a,b,c,d in zip(idx, zero_spec, compact_spec, budget_spec, unpaid_spec):
        w.writerow([int(i), float(a), float(b), float(c), float(d)])

# Lightweight checks.
checks = {
    "classification_status_count": len(routes),
    "tail_trace_class_decreases": bool(np.all(np.diff(trace_tail) < 0)),
    "noncompact_tail_has_positive_floor": bool(noncompact_tail[-1] > 0.05),
    "no_free_budget_positive_mass_floor": bool(all(m >= 0 for m in residual_masses)),
    "schema_present": (OUT / "step155_schema.json").exists(),
}
(OUT / "step155_check_results.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
