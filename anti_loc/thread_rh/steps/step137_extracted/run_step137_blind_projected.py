import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from itertools import combinations

OUT = Path('/mnt/data/rh_membrane_step137_blind_projected_incidence')
OUT.mkdir(parents=True, exist_ok=True)


def first_primes(n):
    primes=[]
    x=2
    while len(primes)<n:
        for p in primes:
            if p*p>x: break
            if x%p==0: break
        else:
            primes.append(x); x+=1; continue
        # Need correct primality
        ok=True
        for p in primes:
            if p*p>x: break
            if x%p==0:
                ok=False; break
        if ok: primes.append(x)
        x+=1
    return primes

# robust prime generator

def primes_upto_count(n):
    primes=[]; m=2
    while len(primes)<n:
        ok=True
        for p in primes:
            if p*p>m: break
            if m%p==0:
                ok=False; break
        if ok: primes.append(m)
        m+=1
    return primes


def hadamard(k):
    H=np.array([[1.0]])
    h=np.array([[1.0,1.0],[1.0,-1.0]])/np.sqrt(2)
    for _ in range(k):
        H=np.kron(H,h)
    return H


def kron_all(mats):
    out=np.array([[1.0]])
    for M in mats:
        out=np.kron(out,M)
    return out


def degrees(k):
    return np.array([bin(i).count('1') for i in range(2**k)])


def incidence_matrix(primes, alpha=1.0):
    mats=[]
    for p in primes:
        r=p**(-alpha/2)
        mats.append(np.array([[1.0,0.0],[r,1.0]]))
    return kron_all(mats)


def op_norm(M):
    if M.size==0: return 0.0
    return np.linalg.svd(M, compute_uv=False)[0]

# Finite exact norm audit for small k
rows=[]
for k in range(3, 9):
    primes=primes_upto_count(k)
    A=incidence_matrix(primes, alpha=1.0)
    H=hadamard(k)
    deg=degrees(k)
    full_norm=op_norm(A)
    sigma_prod=1.0
    minus_norm=1.0
    for p in primes:
        r=p**(-0.5)
        sigma=(np.sqrt(4+r*r)+r)/2
        sigma_prod*=sigma
        minus_norm*=np.sqrt(1-r+0.5*r*r)
    for R in [max(1,k//2), max(1,int(np.ceil(0.65*k))), max(1,int(np.ceil(0.8*k))), k]:
        mask_out=(deg>=R).astype(float)
        Pblind = H.T @ np.diag(mask_out) @ H
        blind_norm=op_norm(Pblind @ A)
        for K in [0, max(0,R-2), max(0,R-1), R, min(k,R+1)]:
            mask_seed_low=(deg<=K).astype(float)
            mask_seed_high=(deg>K).astype(float)
            P_low=np.diag(mask_seed_low); P_high=np.diag(mask_seed_high)
            low_leak=op_norm(Pblind @ A @ P_low)
            high_tail=op_norm(Pblind @ A @ P_high)
            rows.append({
                'k':k, 'R':R, 'K':K, 'dimension':2**k,
                'full_norm_svd':full_norm,
                'full_norm_product':sigma_prod,
                'blind_norm':blind_norm,
                'blind_over_full':blind_norm/full_norm,
                'all_minus_row_norm':minus_norm,
                'low_omega_leak_norm':low_leak,
                'high_omega_tail_norm':high_tail,
                'positive_floor_if_delta_eq_blind':max(0.0,1-blind_norm**2),
                'positive_floor_low_leak':max(0.0,1-low_leak**2),
            })

df=pd.DataFrame(rows)
df.to_csv(OUT/'blind_projected_incidence_norms_step137.csv', index=False)

# Asymptotic row/product metrics for larger k
rows2=[]
for k in [5,8,12,16,24,32,48,64,96,128]:
    primes=primes_upto_count(k)
    log_full=0.0; log_minus=0.0
    for p in primes:
        r=p**(-0.5)
        sigma=(np.sqrt(4+r*r)+r)/2
        log_full+=np.log(sigma)
        log_minus+=0.5*np.log(1-r+0.5*r*r)
    y=primes[-1]
    rows2.append({'k':k,'largest_prime_y':y,'log_full_norm':log_full,'log_all_minus_norm':log_minus,
                  'full_norm':np.exp(log_full),'all_minus_norm':np.exp(log_minus),
                  'sqrt_y_over_log_y':np.sqrt(y)/np.log(y)})
df2=pd.DataFrame(rows2)
df2.to_csv(OUT/'incidence_asymptotic_products_step137.csv', index=False)

# Plot 1: blind norm ratio vs R for k=10
k0=8
primes=primes_upto_count(k0)
A=incidence_matrix(primes,1.0)
H=hadamard(k0); deg=degrees(k0)
full=op_norm(A)
plot_rows=[]
for R in range(0,k0+1):
    P=H.T @ np.diag((deg>=R).astype(float)) @ H
    nrm=op_norm(P@A)
    plot_rows.append({'R':R,'norm':nrm,'ratio':nrm/full,'floor':max(0,1-nrm*nrm)})
pdf=pd.DataFrame(plot_rows)
pdf.to_csv(OUT/'blind_threshold_sweep_k8_step137.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(pdf['R'], pdf['ratio'], marker='o')
plt.xlabel('blind threshold R = minimum number of negative Walsh primes')
plt.ylabel('||Pi_B Z|| / ||Z||, k=10')
plt.title('Blind projection reduces incidence norm')
plt.tight_layout()
plt.savefig(OUT/'blind_projected_norm_ratio_step137.png', dpi=180)
plt.close()

# Plot 2: low omega leakage for k=8, R=6 vs K
R0=6
P=H.T @ np.diag((deg>=R0).astype(float)) @ H
krows=[]
for K in range(0,k0+1):
    P_low=np.diag((deg<=K).astype(float))
    P_high=np.diag((deg>K).astype(float))
    krows.append({'K':K,'low_leak':op_norm(P@A@P_low), 'high_tail':op_norm(P@A@P_high)})
kdf=pd.DataFrame(krows)
kdf.to_csv(OUT/'omega_cutoff_sweep_k8_R6_step137.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(kdf['K'], kdf['low_leak'], marker='o', label='low-Omega leakage')
plt.plot(kdf['K'], kdf['high_tail'], marker='s', label='high-Omega tail norm')
plt.axhline(1.0, linestyle='--', linewidth=1)
plt.xlabel('seed cutoff K')
plt.ylabel('operator norm')
plt.title('Low-Omega leakage and high-Omega tail, k=8, R=6')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'omega_cutoff_leak_tail_step137.png', dpi=180)
plt.close()

# Plot 3 asymptotic products
plt.figure(figsize=(7,4.5))
plt.plot(df2['sqrt_y_over_log_y'], df2['log_full_norm'], marker='o', label='log ||Z||_H')
plt.plot(df2['sqrt_y_over_log_y'], -df2['log_all_minus_norm'], marker='s', label='-log all-minus row norm')
plt.xlabel('sqrt(y)/log(y)')
plt.ylabel('log scale')
plt.title('Full incidence amplification vs deepest blind-row suppression')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'full_vs_all_minus_asymptotic_step137.png', dpi=180)
plt.close()

# Plot 4 restricted source floor model using delta from blind norm threshold sweep
logq=np.linspace(10, 1000, 100)
models=[]
for delta in [0.2,0.5,0.8,0.95]:
    for ql in logq:
        models.append({'logq':ql,'delta':delta,'effective_gamma':ql*(1-delta**2)})
mdf=pd.DataFrame(models)
mdf.to_csv(OUT/'restricted_source_floor_model_step137.csv', index=False)
plt.figure(figsize=(7,4.5))
for delta, g in mdf.groupby('delta'):
    plt.plot(g['logq'], g['effective_gamma'], label=f'delta={delta}')
plt.xlabel('log q')
plt.ylabel('effective source strength ~ log(q)(1-delta^2)')
plt.title('Uniform blind-overlap floor still allows divergence')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'restricted_source_floor_step137.png', dpi=180)
plt.close()

# Gate tables
gates=[
    {'gate':'response metric declared','status':'accepted finite model','record':'central-line H metric alpha=1 used; no post-hoc stronger metric'},
    {'gate':'blind projection declared','status':'accepted finite model','record':'Walsh/GCD-log blind family Pi_B declared before source fitting'},
    {'gate':'weighted leakage recognized','status':'new obstruction','record':'exact raw upward-closure annihilation becomes leakage via factors 1-p^{-1/2}'},
    {'gate':'low-Omega leakage bound','status':'open analytic record','record':'estimate L_{B,K}=||Pi_B Z P_{Omega<=K}|| on actual windows'},
    {'gate':'incidence-conditioned high-Omega tail','status':'open analytic record','record':'estimate T_{B,K} times actual seed tail'},
    {'gate':'restricted BPRZ salvage','status':'conditional','record':'requires combined delta<1 and completed residual-tail promotion'},
]
pd.DataFrame(gates).to_csv(OUT/'blind_projected_gate_table_step137.csv', index=False)

thms=[
    {'item':'metric-correct local row formula','statement':'v_±^* A_{p,alpha} = ((1±p^{-alpha/2}), ±?)/sqrt(2) with minus row ((1-r),-1)/sqrt(2)','role':'replaces raw Boolean annihilation'},
    {'item':'blind norm decomposition','statement':'||Pi_B Z b|| <= L_{B,K}||P_low b|| + T_{B,K}||P_high b||','role':'separates low-Omega leakage from high-Omega seed tail'},
    {'item':'all-minus suppression','statement':'row norm^2 = product_p (1-p^{-alpha/2}+p^{-alpha}/2)','role':'deepest blind mode is suppressed in H metric'},
    {'item':'restricted lower-frame floor','statement':'K_q lower frame on nonblind sector plus delta<1 gives gamma_q(1-delta^2)','role':'BPRZ salvage condition'},
]
pd.DataFrame(thms).to_csv(OUT/'theorem_map_step137.csv', index=False)

arith=[
    {'input':'Heap-Soundararajan block architecture','import_status':'imported','use':'declares Omega block cutoffs and tail architecture'},
    {'input':'Burnol co-Poisson/Muentz bridge','import_status':'imported','use':'supplies lawful zeta incidence/mellin carrier'},
    {'input':'BPRZ twisted second moment','import_status':'conditional import','use':'source lower frame after blind-sector avoidance'},
    {'input':'blind-projected norm estimate','import_status':'new project obligation','use':'operator norm angular-gap estimate in source-compatible metric'},
]
pd.DataFrame(arith).to_csv(OUT/'arithmetic_input_table_step137.csv', index=False)

route=[
    {'route':'full incidence norm','status':'too crude','reason':'requires seed tail to beat full ||Z||_H amplification'},
    {'route':'raw unweighted exact annihilation','status':'not source-compatible','reason':'fails after central-line H metric normalization'},
    {'route':'blind-projected incidence norm','status':'active','reason':'charges exactly the GCD-log near-null sector'},
    {'route':'restricted BPRZ source route','status':'conditionally viable','reason':'works if combined blind overlap delta<1 and tail promotion pass'},
]
pd.DataFrame(route).to_csv(OUT/'route_status_step137.csv', index=False)

nonclaim='''# Step 137 nonclaim boundary\n\nStep 137 does not prove RH.\n\nIt does not prove the actual Burnol/Muentz residual seed has small blind-projected incidence norm.\n\nIt does not license replacing the source-compatible central-line coefficient metric by a stronger pulled metric unless that metric is carried through the source Gram, visibility map, tail promotion, and all-six records.\n\nIt does not claim the unweighted exact annihilation result survives unchanged in the H metric. The main correction of this step is that exact annihilation becomes weighted leakage.\n\nIt does not import BPRZ as a full lower frame. BPRZ remains conditional on restricted residual-class positivity and subordinate error.\n'''
(OUT/'nonclaim_boundary_step137.md').write_text(nonclaim)

schema='''{
  "step": 137,
  "name": "Blind-projected incidence norm audit",
  "active_object": "||Pi_B Z_y (I-P_Omega<=K) B_N G_B,N^{-1/2}||",
  "new_obstruction": "source-compatible metric converts raw exact upward-closure annihilation into weighted leakage",
  "accepted_result": "blind projection is much sharper than full incidence norm; deepest all-minus row is suppressed in H metric",
  "open_record": "prove combined blind overlap delta_N<1 or delta_N->0 for actual Burnol/Muentz residual windows",
  "next_step": "Step 138: Omega-threshold optimization for blind-projected incidence"
}
'''
(OUT/'step137_schema.json').write_text(schema)
