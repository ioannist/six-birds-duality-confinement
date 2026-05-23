import numpy as np
import csv
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step125_prime_conductor_frame')

# Model 1: eigenvalues for all/primitive characters as dimension d varies for fixed q.
q = 101
dims = np.arange(1, 121)
all_min = np.where(dims < q, q-1, 0.0)  # aliasing threshold shown schematically
prim_min = np.where(dims < q, q-1-dims, 0.0)
prim_min = np.maximum(prim_min, 0)
with open(OUT/'prime_character_eigenvalues_step125.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['q','dimension_d','all_character_min_eigenvalue','primitive_min_eigenvalue','aliasing_flag'])
    for d,a,p in zip(dims, all_min, prim_min):
        w.writerow([q,int(d),float(a),float(p), bool(d>=q)])
plt.figure(figsize=(7,4.5))
plt.plot(dims, all_min, label='all characters')
plt.plot(dims, prim_min, label='primitive/nonprincipal')
plt.axvline(q, linestyle='--', linewidth=1, label='aliasing threshold d=q')
plt.xlabel('coefficient dimension d')
plt.ylabel('minimum eigenvalue')
plt.title('Prime-conductor finite frame lower bound, q=101')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'prime_character_eigenvalues_step125.png', dpi=200)
plt.close()

# Model 2: primitive lower bound vs conductor ratio q/d.
ratios = np.linspace(1.05, 5, 100)
d = 100
q_vals = ratios * d
prim_norm = 1 - d/(q_vals-1)
prim_norm = np.maximum(prim_norm, 0)
with open(OUT/'primitive_defect_ratio_step125.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['q_over_d','normalized_primitive_lower_bound'])
    for r,v in zip(ratios, prim_norm):
        w.writerow([float(r), float(v)])
plt.figure(figsize=(7,4.5))
plt.plot(ratios, prim_norm)
plt.xlabel('q / d')
plt.ylabel('normalized primitive lower bound')
plt.title('Principal-character removal defect shrinks when q is larger than d')
plt.tight_layout()
plt.savefig(OUT/'primitive_defect_ratio_step125.png', dpi=200)
plt.close()

# Model 3: cumulative source strength under different normalization choices.
N = np.arange(20, 250)
# support dimension grows linearly for toy d_N=N
# source conductors q in [N^omega, 2 N^omega]
scenarios = [
    ('unnormalized_omega_1p2', 1.2, 0.0),
    ('family_normalized_omega_1p2', 1.2, 1.0),
    ('conductor_normalized_omega_1p2', 1.2, 1.2),
    ('unnormalized_omega_2', 2.0, 0.0),
    ('family_normalized_omega_2', 2.0, 1.0),
]
rows=[]
plt.figure(figsize=(7,4.5))
for name, omega, norm_exp in scenarios:
    gamma=[]
    for n in N:
        q0 = n**omega
        # count of primes ~ q/log q in dyadic window; approximate for visualization
        count = max(q0/np.log(max(q0,3)), 1.0)
        avg_q_minus_d = max(1.5*q0 - n, 0)
        # lambda_q ~ q^{-norm_exp}
        lam = q0**(-norm_exp)
        gamma.append(count*lam*avg_q_minus_d)
        rows.append([name,int(n),float(q0),float(gamma[-1])])
    plt.plot(N, gamma, label=name)
with open(OUT/'cumulative_source_strength_scenarios_step125.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['scenario','N','q0_approx','gamma_approx'])
    w.writerows(rows)
plt.yscale('log')
plt.xlabel('N (toy support dimension)')
plt.ylabel('approx cumulative gamma')
plt.title('Cumulative prime-conductor source strength depends on normalization')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'cumulative_source_strength_step125.png', dpi=200)
plt.close()

# Model 4: effective source strength gamma*c_hyb under visibility floors.
N2 = np.arange(10, 300)
gamma = (N2**1.2)  # toy divergent source strength
floors = [0.01, 0.05, 0.2, 0.5]
with open(OUT/'effective_gamma_visibility_floor_step125.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['N','c_floor','gamma_c'])
    for c in floors:
        for n,g in zip(N2,gamma):
            w.writerow([int(n), c, float(c*g)])
plt.figure(figsize=(7,4.5))
for c in floors:
    plt.plot(N2, c*gamma, label=f'c={c}')
plt.yscale('log')
plt.xlabel('N')
plt.ylabel('gamma_N * c_hyb,N')
plt.title('A positive visibility floor suffices if gamma_N diverges')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'effective_gamma_visibility_floor_step125.png', dpi=200)
plt.close()

# Model 5: aliasing rank for support length L and modulus q.
q=31
Ls=np.arange(5, 101)
ranks=[]
for L in Ls:
    residues = {n % q for n in range(1,L+1) if n % q != 0}
    ranks.append(len(residues))
with open(OUT/'aliasing_rank_step125.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['q','support_length_L','coefficient_dimension','rank_seen_by_characters','kernel_dimension'])
    for L,r in zip(Ls,ranks):
        w.writerow([q,int(L),int(L),int(r),int(L-r)])
plt.figure(figsize=(7,4.5))
plt.plot(Ls, ranks, label='rank seen by chars')
plt.plot(Ls, Ls, linestyle='--', label='coefficient dimension')
plt.xlabel('support length L')
plt.ylabel('rank')
plt.title('Aliasing when support reaches conductor, q=31')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'aliasing_rank_step125.png', dpi=200)
plt.close()

print('Step 125 artifacts generated in', OUT)
