import numpy as np
import csv, json, os
import matplotlib.pyplot as plt

outdir = "/mnt/data/rh_membrane_step86_lowfreq_resolution"
os.makedirs(outdir, exist_ok=True)

# 1. No-gap packets for Psi=xi^2
Ns = np.array([10,20,50,100,200,500,1000], dtype=float)
eps = 1/Ns
energy = eps**2/3  # uniform packet on [-eps, eps], average xi^2 = eps^2/3
with open(os.path.join(outdir,"lowfreq_no_gap_packets_step86.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["N","epsilon","energy_average_xi2"])
    for N,e,en in zip(Ns,eps,energy): w.writerow([int(N),e,en])
plt.figure(figsize=(6,4))
plt.loglog(eps, energy, marker='o')
plt.xlabel('epsilon')
plt.ylabel('energy of normalized packet for Psi=xi^2')
plt.title('Low-frequency packets destroy coercivity')
plt.grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(outdir,"lowfreq_no_gap_packets_step86.png"), dpi=180); plt.close()

# 2. Cancellation criterion integral for Psi=xi^2, g=xi^s, integrate [eps,1]
s_values = [0.0,0.25,0.49,0.5,0.51,0.75,1.0,1.5]
eps_values = np.logspace(-5,-1,20)
rows=[]
for s in s_values:
    p = 2*s-2
    for e in eps_values:
        if abs(p+1)<1e-12:
            val = np.log(1/e)
        else:
            val = (1-e**(p+1))/(p+1)
        rows.append([s,e,val])
with open(os.path.join(outdir,"cancellation_integral_step86.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["s","epsilon","integral_eps_to_1_xi_2s_minus_2"]); w.writerows(rows)
plt.figure(figsize=(6,4))
for s in [0.25,0.5,0.51,0.75,1.0]:
    vals=[r[2] for r in rows if r[0]==s]
    plt.loglog(eps_values, vals, label=f's={s}')
plt.gca().invert_xaxis()
plt.xlabel('lower cutoff epsilon')
plt.ylabel('local capacity integral')
plt.title('Cancellation threshold for Psi~xi^2')
plt.legend(); plt.grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(outdir,"cancellation_threshold_step86.png"), dpi=180); plt.close()

# 3. Source coercivity: capacity low <= norm^2/lambda
lams = np.logspace(0,6,50)
cap = 1/lams
with open(os.path.join(outdir,"source_coercivity_collapse_step86.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["lambda","lowfreq_capacity_bound"])
    for lam,c in zip(lams,cap): w.writerow([lam,c])
plt.figure(figsize=(6,4))
plt.loglog(lams, cap)
plt.xlabel('source strength lambda')
plt.ylabel('low-frequency capacity bound')
plt.title('Source coercivity collapses low-frequency budget')
plt.grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(outdir,"source_coercivity_collapse_step86.png"), dpi=180); plt.close()

# 4. Wrong-sector source: one dimension hardened, one remains capacity 1
lams2=np.logspace(0,5,40)
cap1=1/(1+lams2); cap2=np.ones_like(lams2)
with open(os.path.join(outdir,"wrong_sector_lowfreq_source_step86.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["lambda","covered_capacity","uncovered_capacity","max_capacity"])
    for lam,c1,c2 in zip(lams2,cap1,cap2): w.writerow([lam,c1,c2,max(c1,c2)])
plt.figure(figsize=(6,4))
plt.loglog(lams2, cap1, label='covered direction')
plt.loglog(lams2, cap2, label='uncovered direction')
plt.xlabel('source strength lambda')
plt.ylabel('capacity')
plt.title('Wrong-sector source does not collapse full budget')
plt.legend(); plt.grid(True, which='both', alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(outdir,"wrong_sector_source_step86.png"), dpi=180); plt.close()

# summary
summary = {
  "max_no_gap_energy_at_smallest_epsilon": float(energy[-1]),
  "cancellation_threshold_s_gt_0_5_for_Psi_xi2": True,
  "source_capacity_at_lambda_1e6": float(cap[-1]),
  "wrong_sector_uncovered_capacity_at_lambda_1e5": float(cap2[-1])
}
with open(os.path.join(outdir,"step86_check_summary.json"),"w") as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
