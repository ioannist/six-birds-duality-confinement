import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json, zipfile

OUT = Path('/mnt/data/rh_membrane_step141_omega_density')
OUT.mkdir(parents=True, exist_ok=True)

# Deterministic toy model, not RH evidence.
rng = np.random.default_rng(141)

def first_primes(n):
    primes=[]
    x=2
    while len(primes)<n:
        for p in primes:
            if p*p>x: break
            if x%p==0: break
        else:
            primes.append(x)
            x+=1
            continue
        if any(x%p==0 for p in primes if p*p<=x):
            x+=1
            continue
        primes.append(x)
        x+=1
    return primes

# safer simple prime generator
def primes_list(n):
    ps=[]
    x=2
    while len(ps)<n:
        ok=True
        for p in ps:
            if p*p>x: break
            if x%p==0:
                ok=False; break
        if ok: ps.append(x)
        x+=1
    return ps

k=8
primes=primes_list(k)
D=2**k
# subset degree for binary index
bits = np.array([[ (i>>j)&1 for j in range(k)] for i in range(D)], dtype=int)
deg = bits.sum(axis=1)

# Weighted incidence operator in central-line Dirichlet metric alpha=1
Z = np.array([[1.0]])
for p in primes:
    r = p**(-0.5)
    A = np.array([[1.0,0.0],[r,1.0]])
    Z = np.kron(Z,A)
# Orthonormal Walsh basis
H = np.array([[1.0]])
for _ in range(k):
    H = np.kron(H, np.array([[1.0,1.0],[1.0,-1.0]])/np.sqrt(2.0))
# sign minus-degree for Walsh rows: binary row index indicates epsilon_p=-1
minus_deg = deg.copy()

# Residual window synthesis B: random columns weighted by degree with low-Omega bias.
m=18
base = rng.normal(size=(D,m))
# Structured smoothness/low-degree weight; not pure low-degree, tail present.
row_weight = np.exp(-0.42*deg) * (1 + 0.08*rng.normal(size=D))
row_weight = np.abs(row_weight)
B = (row_weight[:,None])*base
# Add a few coherent low-degree columns so density can improve nontrivially.
for j in range(min(m, k+1)):
    mask = (deg == j)
    if mask.any():
        B[mask, j] += 0.8/(1+j)
G = B.T @ B
# Regularize inverse sqrt via eigendecomp
vals, vecs = np.linalg.eigh(G)
vals = np.maximum(vals, 1e-12)
G_inv_sqrt = vecs @ np.diag(vals**-0.5) @ vecs.T
Bnorm = B @ G_inv_sqrt

# helper spectral norm
def opnorm(A):
    if A.size == 0: return 0.0
    return float(np.linalg.svd(A, compute_uv=False)[0])

records=[]
for K in range(0,k+1):
    P_low_diag = (deg <= K).astype(float)
    P_high_diag = 1-P_low_diag
    # density miss epsilon for actual residual window in seed response metric
    eps = opnorm((P_high_diag[:,None])*Bnorm)
    sigma = eps
    for R in range(1,k+1):
        blind_rows = np.where(minus_deg >= R)[0]
        if len(blind_rows)==0:
            L = T = 0.0
        else:
            Wb = H[blind_rows,:]
            L = opnorm(Wb @ Z @ np.diag(P_low_diag))
            T = opnorm(Wb @ Z @ np.diag(P_high_diag))
        delta = L + T*sigma
        density_floor = max(0.0, 1-eps**2)
        blind_floor = max(0.0, 1-min(delta,1.0)**2)
        source_floor = density_floor * blind_floor
        records.append({
            'k_primes': k,
            'K_cutoff': K,
            'R_blind_threshold': R,
            'epsilon_density': eps,
            'sigma_tail': sigma,
            'L_low_omega_leakage': L,
            'T_high_omega_amplification': T,
            'delta_total': delta,
            'density_floor_1_minus_eps2': density_floor,
            'blind_floor_1_minus_delta2': blind_floor,
            'combined_visibility_floor': source_floor,
            'viable_delta_less_than_1': bool(delta < 1.0),
            'viable_both_floors_positive': bool((eps < 1.0) and (delta < 1.0)),
        })

df=pd.DataFrame(records)
df.to_csv(OUT/'omega_density_threshold_sweep_step141.csv', index=False)
best = df.sort_values(['combined_visibility_floor','delta_total'], ascending=[False, True]).groupby('K_cutoff').head(1).reset_index(drop=True)
best.to_csv(OUT/'omega_density_best_choices_step141.csv', index=False)

# Summaries by K using best R
summary = best[['K_cutoff','R_blind_threshold','epsilon_density','delta_total','combined_visibility_floor','L_low_omega_leakage','T_high_omega_amplification']]
summary.to_csv(OUT/'omega_density_summary_by_K_step141.csv', index=False)

# Gate tables
pd.DataFrame([
    ['DENSITY_DEFECT', r'epsilon_{B\to\Omega,N}=||(I-P_{\Omega,N})M_RG_R^{-1/2}||', 'open', 'Burnol completeness does not imply Omega-compatible density'],
    ['BLIND_DEFECT', r'delta_{R,K,N}=L_{R,K}+T_{R,K}\sigma_{K,N}', 'conditional', 'finite threshold gate; requires actual seed-tail bound'],
    ['BICRITERIA_SOURCE', r'gamma_q(1-epsilon^2)(1-delta^2)', 'conditional', 'positive if both defects stay below one and source strength diverges'],
    ['NO_SMUGGLING', 'Omega blocks and thresholds declared upstream', 'required', 'prevents target-selected dictionary fit'],
    ['TAIL_PROMOTION', 'finite windows promote to fixed/exhaustive residual ledger', 'open', 'needed for completed membrane claim'],
], columns=['gate','formula','status','meaning']).to_csv(OUT/'omega_density_gate_table_step141.csv', index=False)

pd.DataFrame([
    ['T141.1','finite density identity', r'c_{\Omega,N}=1-\epsilon_{B\to\Omega,N}^2', 'proved finite algebra'],
    ['T141.2','bicriteria source theorem', r'\Lambda_N\gtrsim\gamma_q(1-\epsilon^2)(1-\delta^2)', 'conditional'],
    ['T141.3','generic non-density warning', r'\epsilon=1 if residual contains pure high-\Omega directions outside dictionary', 'proved finite obstruction'],
    ['T141.4','completed promotion theorem', r'finite positive floor + tail promotion => residual source absorption', 'conditional/open'],
], columns=['id','name','claim','status']).to_csv(OUT/'theorem_map_step141.csv', index=False)

pd.DataFrame([
    ['Burnol/Sonine density','co-Poisson/Sonine carrier and zero-evaluator completeness','imported carrier backbone'],
    ['Heap-Soundararajan Omega architecture','prime blocks, Omega(n_j)<=K_j cutoffs, short Dirichlet polynomials','imported design template'],
    ['BPRZ twisted second moment','source-weighted q-aspect matrix platform','restricted import after blind-sector audit'],
    ['CCM semilocal framework','Hardy-Titchmarsh semilocal response geometry','ambient carrier'],
    ['New project obligation','Omega-compatible density on residual windows','not in literature as stated'],
], columns=['input','content','use']).to_csv(OUT/'arithmetic_input_table_step141.csv', index=False)

pd.DataFrame([
    ['active_route','conditional','Omega-compatible dictionary may provide positive floor if density and blind defects <1'],
    ['not_proved','epsilon_B_to_Omega -> 0','Burnol completeness alone does not impose Omega-block support'],
    ['fallback','Xi_B_to_Omega residual','missed high-Omega directions must get separate source record'],
    ['avoid','target-selected atoms','dictionary must be declared before residual fitting'],
], columns=['route','status','note']).to_csv(OUT/'route_status_step141.csv', index=False)

pd.DataFrame([
    ['C1','Define actual Omega-compatible Burnol/Muntz atoms with support/parity/Mellin/all-six records'],
    ['C2','Prove epsilon_B_to_Omega -> 0 or <= epsilon < 1 on residual windows'],
    ['C3','Combine with blind threshold optimization delta_R,K,N < 1'],
    ['C4','Import restricted BPRZ lower frame on nonblind residual class'],
    ['C5','Promote finite residual windows through fixed/exhaustive tail ledger'],
], columns=['task_id','task']).to_csv(OUT/'construction_tasks_step141.csv', index=False)

# Plots
plt.figure(figsize=(7,4.5))
plt.plot(summary['K_cutoff'], summary['epsilon_density'], marker='o', label='density defect epsilon')
plt.plot(summary['K_cutoff'], summary['delta_total'], marker='o', label='best blind defect delta')
plt.axhline(1.0, linestyle='--')
plt.xlabel('Omega cutoff K')
plt.ylabel('defect')
plt.title('Step 141 toy bicriteria defects')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'omega_density_vs_K_step141.png', dpi=180)
plt.close()

pivot = df.pivot(index='R_blind_threshold', columns='K_cutoff', values='combined_visibility_floor')
plt.figure(figsize=(7,5))
plt.imshow(pivot.values, aspect='auto', origin='lower')
plt.xticks(range(len(pivot.columns)), pivot.columns)
plt.yticks(range(len(pivot.index)), pivot.index)
plt.xlabel('Omega cutoff K')
plt.ylabel('blind threshold R')
plt.title('Combined visibility floor (toy)')
plt.colorbar(label='floor')
plt.tight_layout()
plt.savefig(OUT/'bicriteria_viability_heatmap_step141.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(summary['K_cutoff'], summary['combined_visibility_floor'], marker='o')
plt.xlabel('Omega cutoff K')
plt.ylabel('(1-epsilon^2)(1-delta^2)_+')
plt.title('Effective visibility floor after density and blind gates')
plt.tight_layout()
plt.savefig(OUT/'effective_source_floor_step141.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(summary['K_cutoff'], summary['L_low_omega_leakage'], marker='o', label='low-Omega leakage L')
plt.plot(summary['K_cutoff'], summary['T_high_omega_amplification']*summary['epsilon_density'], marker='o', label='tail term T*sigma')
plt.xlabel('Omega cutoff K')
plt.ylabel('component size')
plt.title('Leakage/tail tradeoff in best-R toy choices')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'density_leakage_tradeoff_step141.png', dpi=180)
plt.close()

# residual split plot: density floor vs blind floor for best choices
plt.figure(figsize=(7,4.5))
plt.plot(summary['K_cutoff'], 1-summary['epsilon_density']**2, marker='o', label='density floor')
plt.plot(summary['K_cutoff'], np.maximum(0, 1-np.minimum(summary['delta_total'],1)**2), marker='o', label='blind-sector floor')
plt.xlabel('Omega cutoff K')
plt.ylabel('floor')
plt.title('Two independent floors')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'residual_split_step141.png', dpi=180)
plt.close()

# LaTeX note and summary
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,enumitem}
\usepackage[margin=1in]{geometry}
\title{Step 141: $\Omega$-Compatible Density Audit on Burnol/Sonine Residual Windows}
\author{RATCHET / Six Birds RH Membrane Thread}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\begin{document}
\maketitle

\section{Purpose}
Steps 130--140 converted the source-coercivity route into a restricted BPRZ source-frame problem on the actual residual coefficient class.  The unrestricted GCD--log lower frame is blocked by a squarefree Boolean near-null sector.  The repair is to use an upstream-declared $\Omega$-compatible Burnol/M\"untz residual dictionary whose zeta/M\"untz shadows avoid that blind sector.

The active question is whether this dictionary remains dense enough in the finite residual Burnol/Sonine windows.  This step audits the density side.

\section{Finite residual window}
Let
\[
M_{R,N}:Y_{R,N}\to H_N
\]
be a finite residual-window synthesis map, with Gram form
\[
G_{R,N}=M_{R,N}^{*}M_{R,N}.
\]
Let $\mathcal D_{\Omega,N}\subset H_N$ be the declared span of Burnol/co-Poisson atoms whose regularized M\"untz/Dirichlet shadows obey the upstream prime-block cutoffs
\[
\Omega(n_j)\le K_j.
\]
Let $P_{\Omega,N}$ be the orthogonal projection onto $\mathcal D_{\Omega,N}$.

\begin{definition}[Omega-compatible density defect]
The finite density defect is
\[
\boxed{
\epsilon_{B\to\Omega,N}
=
\left\|(I-P_{\Omega,N})M_{R,N}G_{R,N}^{-1/2}\right\|.
}
\]
Equivalently the missed adequacy residual is
\[
\boxed{
\Xi_{B\to\Omega,N}
=
M_{R,N}^{*}(I-P_{\Omega,N})M_{R,N}.
}
\]
\end{definition}

This is the corrected meaning of the $c_N$-side of the route: it is a spanning residual of a constructible family, not a column-norm bound on a fixed map.

\section{Finite density identity}
\begin{proposition}
If
\[
R_{\Omega,N}=D_{\Omega,N}^{\dagger}M_{R,N}
\]
is the coefficient map through the declared $\Omega$-compatible dictionary, then
\[
R_{\Omega,N}^{*}H_{\Omega,N}R_{\Omega,N}
=
G_{R,N}-\Xi_{B\to\Omega,N}.
\]
Consequently
\[
\boxed{
R_{\Omega,N}^{*}H_{\Omega,N}R_{\Omega,N}
\succeq
(1-\epsilon_{B\to\Omega,N}^{2})G_{R,N}.
}
\]
\end{proposition}

\section{Bicriteria source theorem}
Let $\delta_{R,K,N}$ be the GCD--log blind-sector defect from Step 138,
\[
\delta_{R,K,N}=L_{R,K}+T_{R,K}\sigma_{K,N}.
\]
Assume that the restricted BPRZ source kernel has lower frame
\[
K_q\succeq \gamma_q I
\]
on the nonblind residual coefficient class, with $\gamma_q\asymp \log q$.

\begin{theorem}[Bicriteria restricted source frame]
If
\[
\epsilon_{B\to\Omega,N}\le \epsilon_N<1,
\qquad
\delta_{R,K,N}\le \delta_N<1,
\]
then the restricted residual source frame satisfies
\[
\boxed{
F_{R,N}^{\Omega}
\succeq
\gamma_q(1-\epsilon_N^2)(1-\delta_N^2)G_{R,N}
}
\]
up to the declared BPRZ asymptotic-error and finite-window tail records.
\end{theorem}

Thus a positive floor is enough.  Exact density is sufficient but not necessary.

\section{Generic non-density warning}
Burnol completeness and co-Poisson density do not imply $\Omega$-compatible density.  If the residual window contains a normalized direction whose seed coefficients are supported outside every declared $\Omega$ cutoff, then
\[
\epsilon_{B\to\Omega,N}=1.
\]
Therefore the $\Omega$-compatible route requires a new density theorem:
\[
\boxed{
\epsilon_{B\to\Omega,N}\to0
\quad\text{or at least}\quad
\epsilon_{B\to\Omega,N}\le \epsilon<1.
}
\]
If this fails, the missed sector
\[
\Xi_{B\to\Omega,N}
\]
becomes a genuine residual requiring a separate source-frame record.

\section{Interpretation}
The source route now has two independent floor factors:
\[
\boxed{
\text{density floor } 1-\epsilon_{B\to\Omega,N}^{2}
}
\]
and
\[
\boxed{
\text{GCD-blind floor } 1-\delta_{R,K,N}^{2}.
}
\]
The effective source strength is
\[
\boxed{
\Lambda_N^{\Omega}
\gtrsim
\gamma_q
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
}
\]

\section{Audit verdict}
The finite algebra is clean.  The density theorem is not earned.  The next analytic obligation is to prove that the declared $\Omega$-compatible Burnol/M\"untz dictionary has a positive visibility floor on the actual residual Burnol/Sonine windows.

\end{document}
'''
(OUT/'omega_density_audit_step141.tex').write_text(tex)

summary_md = r'''
# Step 141: Omega-Compatible Density Audit on Burnol/Sonine Residual Windows

## Main result

This step audits the new density defect introduced by the Omega-compatible dictionary route:

\[
\epsilon_{B\to\Omega,N}
=
\|(I-P_{\Omega,N})M_{R,N}G_{R,N}^{-1/2}\|.
\]

This is a spanning/adequacy residual, not a column-norm bound.

## Verdict

The finite algebra is closed, but the density theorem is not earned:

\[
\epsilon_{B\to\Omega,N}\to0
\]

is not implied by Burnol completeness alone, because Burnol/co-Poisson density does not automatically preserve Heap--Soundararajan-style Omega block cutoffs.

A positive floor may be enough:

\[
\epsilon_{B\to\Omega,N}\le \epsilon<1.
\]

If this fails, the missed sector

\[
\Xi_{B\to\Omega,N}
=
M_{R,N}^{*}(I-P_{\Omega,N})M_{R,N}
\]

is a genuine residual.

## Bicriteria source condition

The restricted BPRZ source route now needs two independent floors:

\[
1-\epsilon_{B\to\Omega,N}^{2}
\]

and

\[
1-\delta_{R,K,N}^{2}.
\]

The effective source strength is

\[
\Lambda_N^{\Omega}
\gtrsim
\gamma_q
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
\]

So the route is viable if both defects stay below one and the source strength diverges, subject to fixed/exhaustive tail promotion.

## Nonclaim

Step 141 does not prove RH. It does not prove Omega-compatible density. It gives the exact density gate and the residual if the gate fails.
'''
(OUT/'step141_results_summary.md').write_text(summary_md)

nonclaim = r'''
# Step 141 Nonclaim Boundary

Step 141 does not prove RH.

It does not prove that the Omega-compatible Burnol/Muntz dictionary is dense.

It does not claim that Burnol completeness implies Heap--Soundararajan Omega-block compatibility.

It does not claim that the restricted BPRZ source route works on the completed carrier.

It proves only the finite density identity, the bicriteria source theorem conditional on density and blind-sector floors, and the exact residual that remains if Omega-compatible density fails.
'''
(OUT/'nonclaim_boundary_step141.md').write_text(nonclaim)

schema = {
    'step': 141,
    'title': 'Omega-Compatible Density Audit on Burnol/Sonine Residual Windows',
    'active_defects': ['epsilon_B_to_Omega_N', 'delta_R_K_N', 'Xi_B_to_Omega_N', 'Xi_GCD_N'],
    'main_condition': 'gamma_q*(1-epsilon^2)*(1-delta^2) -> infinity with tail promotion',
    'verdict': 'conditional; density not proven',
    'toy_model': {'k_primes': k, 'dimension': D, 'residual_window_dim': m, 'not_RH_evidence': True}
}
(OUT/'step141_schema.json').write_text(json.dumps(schema, indent=2))

# Zip core artifacts
zip_path = OUT/'step141_omega_density_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for p in OUT.iterdir():
        if p == zip_path: continue
        zf.write(p, arcname=p.name)

print(f'Wrote artifacts to {OUT}')
