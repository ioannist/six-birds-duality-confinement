import os, json, math, csv, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base = Path('/mnt/data/rh_membrane_step120_shadow_asymptotic')
base.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Synthetic / sanity models
# -----------------------------
N = np.arange(8, 161, 8)
# scenarios for epsilon_B and delta_BD
scenarios = []
for n in N:
    eps_good = 0.9*np.exp(-n/38.0)
    delta_good = 0.75*np.exp(-n/42.0)
    eps_slow = 0.8/np.sqrt(n/8)
    delta_slow = 0.88/(1+0.04*(n-8))**0.35
    eps_floor = 0.2 + 0.5*np.exp(-n/30.0)
    delta_floor = 0.55 + 0.25*np.exp(-n/30.0)
    eps_bad = 0.55 + 0.15*np.exp(-n/40.0)
    delta_bad = 0.98 - 0.08*np.exp(-n/30.0)
    for name, eps, delta in [
        ('shadow_complete_fast', eps_good, delta_good),
        ('slow_but_compensable', eps_slow, delta_slow),
        ('positive_shadow_floor', eps_floor, delta_floor),
        ('near_invisible_bad_shadow', eps_bad, delta_bad),
    ]:
        c_lower = max(0.0, 1 - min(1.5, eps+delta)**2)
        gamma = np.log(max(n,2))**2
        Lambda = gamma*c_lower
        scenarios.append({
            'N': int(n), 'scenario': name, 'epsilon_B': float(eps), 'delta_BD': float(delta),
            'epsilon_hyb_bound': float(eps+delta), 'c_hyb_lower_bound': float(c_lower),
            'gamma_model_log2': float(gamma), 'effective_Lambda_model': float(Lambda)
        })
scen_df = pd.DataFrame(scenarios)
scen_df.to_csv(base/'shadow_asymptotic_scenarios_step120.csv', index=False)

# Missed shadow residual spectrum proxy
k = np.arange(1, 121)
residual_spectra = pd.DataFrame({
    'mode': k,
    'compact_tail': 1/(k**1.6),
    'slow_tail': 1/(k**0.55),
    'nonzero_floor': 0.12 + 0.7/(1+k/4),
    'rank_like': np.where(k <= 12, np.linspace(1, 0.1, len(k)), 0)
})
residual_spectra.to_csv(base/'missed_shadow_spectrum_step120.csv', index=False)

# Angular gap / projection identity finite check
rng = np.random.default_rng(120)
records = []
for dimH in [24, 36, 48, 64]:
    for dimB in [4, 8, 12]:
        if dimB >= dimH: continue
        # construct random orthonormal Burnol range B
        X = rng.normal(size=(dimH, dimB))
        QB, _ = np.linalg.qr(X)
        # construct D spaces by adding noisy B plus independent directions
        for quality in [0.05, 0.15, 0.35, 0.65]:
            Y = QB + quality*rng.normal(size=(dimH, dimB))
            # add a few extra columns
            extra = rng.normal(size=(dimH, max(1, dimB//2)))
            Dmat = np.concatenate([Y, extra], axis=1)
            QD, _ = np.linalg.qr(Dmat)
            P_D = QD @ QD.T
            E = (np.eye(dimH)-P_D) @ QB
            delta = np.linalg.svd(E, compute_uv=False)[0]
            c = max(0.0, 1-delta**2)
            records.append({'dimH':dimH,'dimB':dimB,'quality_noise':quality,'delta_gap':delta,'c_visibility':c})
check_df = pd.DataFrame(records)
check_df.to_csv(base/'finite_projection_gap_checks_step120.csv', index=False)

# Plots
plt.figure(figsize=(8,5))
for name, sub in scen_df.groupby('scenario'):
    plt.plot(sub['N'], sub['delta_BD'], label=name)
plt.xlabel('finite window N')
plt.ylabel(r'$\delta_{BD,N}$')
plt.title('Burnol-to-Dirichlet shadow defect scenarios')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'shadow_defect_scenarios_step120.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name, sub in scen_df.groupby('scenario'):
    plt.plot(sub['N'], sub['c_hyb_lower_bound'], label=name)
plt.xlabel('finite window N')
plt.ylabel(r'$c_{\mathrm{hyb},N}$ lower bound')
plt.title('Hybrid visibility lower-bound scenarios')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'hybrid_visibility_asymptotic_step120.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name, sub in scen_df.groupby('scenario'):
    plt.plot(sub['N'], sub['effective_Lambda_model'], label=name)
plt.xlabel('finite window N')
plt.ylabel(r'$\gamma_N c_{\mathrm{hyb},N}$ model')
plt.title('Effective source strength under shadow scenarios')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'effective_source_shadow_scenarios_step120.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for col in ['compact_tail','slow_tail','nonzero_floor','rank_like']:
    plt.plot(residual_spectra['mode'], residual_spectra[col], label=col)
plt.xlabel('mode index')
plt.ylabel('singular value / residual weight proxy')
plt.title('Missed shadow residual spectrum regimes')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'missed_shadow_spectrum_step120.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for dimB, sub in check_df.groupby('dimB'):
    grp = sub.groupby('quality_noise')['c_visibility'].mean().reset_index()
    plt.plot(grp['quality_noise'], grp['c_visibility'], marker='o', label=f'dimB={dimB}')
plt.xlabel('shadow noise / angle proxy')
plt.ylabel('mean visibility constant')
plt.title('Finite angular-gap sanity check')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'finite_projection_gap_checks_step120.png', dpi=180)
plt.close()

# Tables
shadow_gate_rows = [
    ['S120.G1', 'Declare Burnol target range', 'B_N and G_B,N are fixed before testing zeros/residuals', 'prevents target-selected atoms'],
    ['S120.G2', 'Declare Dirichlet-readable subspaces', 'D_N is generated by arithmetic/refinement rules, not residual fitting', 'prevents smuggled supports'],
    ['S120.G3', 'Angular gap criterion', '|| (I-P_D,N) B_N G_B,N^{-1/2} || -> 0 or controlled floor', 'defines delta_BD,N'],
    ['S120.G4', 'Müntz/co-Poisson regularization', 'critical-line shadow uses regularized co-Poisson/Müntz synthesis, not naive ζ partial sums', 'prevents false Dirichlet approximation'],
    ['S120.G5', 'Missed-shadow residual', 'Xi_BD = B^*(I-P_D)B is zero, compact/tail, or source-absorbed', 'if not, hybrid route has blind spot'],
    ['S120.G6', 'Effective strength', 'gamma_N * c_hyb,N -> infinity after tails', 'links readability to source ladder'],
    ['S120.G7', 'Fixed/exhaustive promotion', 'finite windows promote to completed ledger with vanishing tail', 'prevents moving-window overread'],
    ['S120.G8', 'All-six record', 'rewrite, feasibility, route, staging, packaging, audit declared', 'keeps membrane framework native'],
]
pd.DataFrame(shadow_gate_rows, columns=['gate','name','acceptance_condition','failure_meaning']).to_csv(base/'shadow_asymptotic_gate_table_step120.csv', index=False)

criterion_rows = [
    ['shadow_complete', 'delta_BD,N -> 0', 'Burnol atoms are geometrically visible and Dirichlet-readable', 'hybrid dictionary can deliver c_hyb,N -> 1 if epsilon_B,N -> 0'],
    ['positive_floor', 'limsup delta_BD,N < 1 and epsilon_B,N + delta_BD,N < 1', 'not complete, but still enough if gamma_N c_hyb,N -> infinity', 'requires quantitative source compensation'],
    ['compact_missed_shadow', 'Xi_BD compact/tail with finite-window approximation', 'Dirichlet dictionary misses only compact/tail directions', 'absorbed by finite windows plus tail'],
    ['nonzero_blind_sector', '|| (I-P_D)B G_B^{-1/2} || = 1 on some sector', 'some Burnol directions are unreadable by Dirichlet/Hecke coefficients', 'needs separate source frame or nonclaim'],
]
pd.DataFrame(criterion_rows, columns=['status','criterion','interpretation','route_effect']).to_csv(base/'shadow_asymptotic_criterion_table_step120.csv', index=False)

arith_rows = [
    ['Burnol/co-Poisson carrier', 'supply B_N and geometric exhaustion epsilon_B,N', 'Burnol density/completeness and co-Poisson synthesis'],
    ['Müntz/co-Poisson shadow', 'justify ζ(s)g_hat(s) in critical strip as regularized response', 'avoid naive Dirichlet-series overread on Re(s)=1/2'],
    ['Dirichlet support/refinement', 'define D_N by arithmetic support rules', 'non-smuggled coefficient dictionary'],
    ['Shadow asymptotic', 'prove delta_BD,N -> 0 or identify Xi_BD', 'new bridge between Burnol atoms and Hecke-readable coefficients'],
    ['Heap-Soundararajan lift', 'prove gamma_N lower frame on coefficient space', 'operator-valued matrix moment estimates'],
    ['Tail/exhaustivity', 'promote finite windows to completed residual ledger', 'fixed/exhaustive squeeze gate'],
]
pd.DataFrame(arith_rows, columns=['input','role','hard_obligation']).to_csv(base/'arithmetic_input_table_step120.csv', index=False)

route_rows = [
    ['compactness shortcut', 'blocked for raw shifted Sonin blocks', 'only revived by essential semilocal prolate cancellation'],
    ['Burnol inclusion shortcut', 'not automatic', 'requires zeta-factorization or annihilation of zero-evaluators'],
    ['hybrid source route', 'active', 'requires epsilon_B,N, delta_BD,N, gamma_N and tails'],
    ['enlarged adelic route', 'backup', 'if semilocal/Burnol-to-Dirichlet bridge fails'],
]
pd.DataFrame(route_rows, columns=['route','status','condition']).to_csv(base/'route_status_step120.csv', index=False)

theorem_rows = [
    ['T120.1', 'Projection identity for shadow defect', 'delta_BD,N^2 = ||G_B^{-1/2} B_N^*(I-P_D,N)B_N G_B^{-1/2}||'],
    ['T120.2', 'Angular-gap criterion', 'delta_BD,N -> 0 iff declared Dirichlet-readable subspaces approximate Burnol target ranges uniformly on normalized windows'],
    ['T120.3', 'Missed-shadow residual theorem', 'limiting failure is Xi_BD = B^*(I-P_D)B'],
    ['T120.4', 'Hybrid source theorem', 'gamma_N c_hyb,N -> infinity gives residual absorption after tails'],
    ['T120.5', 'Regularization warning', 'naive zeta Dirichlet partial sums on critical line are not lawful shadows without Muntz/co-Poisson regularization'],
]
pd.DataFrame(theorem_rows, columns=['id','name','content']).to_csv(base/'theorem_map_step120.csv', index=False)

# Latex note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{booktabs}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{warning}{Warning}
\newtheorem{corollary}{Corollary}
\title{Step 120: Burnol--to--Dirichlet Shadow Asymptotic Criterion}
\author{RATCHET RH Membrane Program}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Step 119 introduced the Burnol--to--Dirichlet shadow map.  A Burnol/co-Poisson atom is geometrically natural, but it is useful for the Hecke/Dirichlet source ladder only if it has a source-readable Dirichlet shadow.  This step states the exact asymptotic criterion for the shadow defect
\[
\delta_{BD,N}=\|(B_N-D_NA_N)G_{B,N}^{-1/2}\|
\]
to vanish, or, if it does not vanish, for the missed shadow subspace to be declared as a new residual.

\section{Finite setup}
Let $H_N$ be a finite response window.  Let
\[
B_N:Y_{B,N}\to H_N
\]
be the finite Burnol/co-Poisson response synthesis map, with Gram form
\[
G_{B,N}=B_N^*B_N.
\]
Let
\[
D_N:\mathbb C^{I_N}\to H_N
\]
be the declared Dirichlet-readable synthesis map.  Let $P_{D,N}$ be the orthogonal projection onto $\operatorname{Ran}D_N$.  The optimal shadow map is
\[
A_N=(D_N^*W_ND_N)^\dagger D_N^*W_NB_N
\]
for the declared window weight $W_N$; in the unweighted Hilbert model this is simply $A_N=D_N^\dagger B_N$.

\begin{definition}[Burnol--to--Dirichlet shadow defect]
The normalized shadow defect is
\[
\delta_{BD,N}
=
\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|.
\]
Equivalently, the shadow adequacy residual is
\[
\Xi_{BD,N}=B_N^*(I-P_{D,N})B_N.
\]
\end{definition}

\begin{lemma}[Projection identity]
One has
\[
B_N^*P_{D,N}B_N
=G_{B,N}-\Xi_{BD,N}.
\]
Hence the source-readable visibility constant is
\[
c_{BD,N}=1-\delta_{BD,N}^2.
\]
\end{lemma}

\section{Asymptotic criterion}
Let $H$ be the completed response space.  Let $\mathcal D_N=\operatorname{Ran}D_N$ and let $P_{D,N}$ be their projections.  Let $B_N$ be an exhausting sequence of finite Burnol windows for a completed Burnol target operator $B:Y_B\to H$.

\begin{theorem}[Uniform angular-gap criterion]
Assume the finite Burnol windows exhaust the completed target in the fixed/exhaustive sense.  Then
\[
\delta_{BD,N}\to0
\]
if and only if the declared Dirichlet-readable subspaces approximate the Burnol target ranges uniformly on normalized finite windows:
\[
\sup_{0\ne y\in Y_{B,N}}
\frac{\operatorname{dist}(B_Ny,\mathcal D_N)}{\|B_Ny\|}
\to0.
\]
Equivalently, the operator-norm gap
\[
\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|
\]
tends to zero.
\end{theorem}

\begin{warning}[Strong convergence is not enough]
It is not enough that $P_{D,N}\to I$ strongly on each fixed Burnol atom.  The windows $Y_{B,N}$ grow.  The needed statement is a uniform gap estimate on the whole current window, plus a tail record.
\end{warning}

\begin{theorem}[Missed-shadow residual]
Suppose the projections $P_{D,N}$ converge strongly to $P_D$, the projection onto the completed Dirichlet-readable closure $\mathcal D$.  Then any nonzero limiting defect is exactly
\[
\Xi_{BD}=B^*(I-P_D)B.
\]
If
\[
\Xi_{BD}\ne0,
\]
then the hybrid route has a Burnol-to-Dirichlet readability blind spot.  This blind spot must be source-absorbed, compact/tail-promoted, or declared as a scoped nonclaim.
\end{theorem}

\section{Regularized shadow requirement}
Burnol's co-Poisson/Müntz formula gives the native target
\[
M(\mathcal Cg)(s)=\zeta(s)\widehat g(s).
\]
However, ordinary Dirichlet series for $\zeta(s)$ converge only in the half-plane $\operatorname{Re}s>1$.  Therefore, on critical-line response windows, a lawful shadow map cannot be merely a naive partial sum
\[
\sum_{n\le X}n^{-s}.
\]
It must be a declared regularized shadow, for example through co-Poisson/Müntz synthesis, approximate functional equations, smoothed Euler products, or another audited response-space approximation.

\begin{definition}[Regularized Dirichlet-readable shadow]
A Dirichlet-readable shadow family is accepted if the maps $D_NA_N$ are produced from declared arithmetic/refinement rules and satisfy
\[
\|(B_N-D_NA_N)G_{B,N}^{-1/2}\|\le \delta_{BD,N}
\]
with a stated asymptotic status: vanishing, bounded below one, compact/tail, or nonzero blind sector.
\end{definition}

\section{Hybrid source consequence}
Let $\epsilon_{B,N}$ be the Burnol geometric exhaustion defect for the residual sector, and let $\delta_{BD,N}$ be the Dirichlet shadow defect.  Then
\[
\epsilon_{\mathrm{hyb},N}\le \epsilon_{B,N}+\delta_{BD,N}
\]
and hence
\[
c_{\mathrm{hyb},N}\ge 1-(\epsilon_{B,N}+\delta_{BD,N})^2.
\]
If the Hecke/Dirichlet source Gram satisfies
\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\]
then the effective residual source strength obeys
\[
\Lambda_{R,N}=\gamma_Nc_{\mathrm{hyb},N}.
\]
Thus the route needs
\[
\gamma_Nc_{\mathrm{hyb},N}\to\infty
\]
after fixed/exhaustive tail promotion.

\section{Status trichotomy}
The Burnol-to-Dirichlet bridge now has three lawful outcomes.

\begin{enumerate}[label=(\alph*)]
\item \textbf{Shadow complete.}  $\delta_{BD,N}\to0$.  Then Burnol visibility becomes Dirichlet/Hecke-readable.
\item \textbf{Positive floor.}  $\delta_{BD,N}$ does not vanish, but $\epsilon_{B,N}+\delta_{BD,N}<1$ quantitatively.  Then the source route may still close if $\gamma_Nc_{\mathrm{hyb},N}\to\infty$.
\item \textbf{Blind shadow sector.}  $\Xi_{BD}=B^*(I-P_D)B\ne0$ and the lower bound for $c_{\mathrm{hyb},N}$ collapses.  Then the missed shadow sector needs a separate source-frame record or must become a nonclaim.
\end{enumerate}

\section{Conclusion}
The active gate is no longer a vague readability question.  It is the angular-gap estimate
\[
\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|\to0
\]
or its exact residual replacement
\[
\Xi_{BD}=B^*(I-P_D)B.
\]
The next construction should derive a lawful regularized Dirichlet shadow family from the co-Poisson/Müntz formula, rather than using naive critical-line Dirichlet partial sums.
\end{document}
'''
(base/'burnol_dirichlet_shadow_asymptotic_step120.tex').write_text(tex)

# Summary markdown
summary = r'''
# Step 120: Burnol-to-Dirichlet Shadow Asymptotic Criterion

## Result
The Burnol-to-Dirichlet readability problem is now an angular-gap problem. For a Burnol/co-Poisson synthesis map

\[
B_N:Y_{B,N}\to H_N
\]

and a declared Dirichlet-readable synthesis map

\[
D_N:\mathbb C^{I_N}\to H_N,
\]

with \(P_{D,N}\) the projection onto \(\operatorname{Ran}D_N\), the shadow defect is

\[
\delta_{BD,N}=\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|.
\]

Equivalently,

\[
\Xi_{BD,N}=B_N^*(I-P_{D,N})B_N
\]

is the Burnol-to-Dirichlet adequacy residual.

## Criterion
The shadow defect tends to zero precisely when the declared Dirichlet-readable subspaces approximate the Burnol target ranges uniformly on normalized growing windows:

\[
\sup_{0\ne y\in Y_{B,N}}
\frac{\operatorname{dist}(B_Ny,\operatorname{Ran}D_N)}{\|B_Ny\|}\to0.
\]

Strong convergence on each fixed atom is not enough because the Burnol windows grow.

## If the criterion fails
The limiting missed shadow is

\[
\Xi_{BD}=B^*(I-P_D)B.
\]

If this is nonzero, the hybrid dictionary has a readability blind spot. That blind spot must be absorbed by a separate source frame, shown compact/tail, or declared as a scoped nonclaim.

## Regularization warning
Burnol/co-Poisson gives the target

\[
M(\mathcal Cg)(s)=\zeta(s)\widehat g(s),
\]

but naive partial sums of \(\zeta(s)\) are not lawful shadows on the critical line. The Dirichlet shadow must be regularized by a declared co-Poisson/Müntz, approximate-functional-equation, smoothed Euler, or equivalent audited construction.

## Source consequence
If

\[
\epsilon_{B,N}=\text{Burnol geometric exhaustion defect},
\]

and

\[
\delta_{BD,N}=\text{Dirichlet readability defect},
\]

then

\[
c_{\mathrm{hyb},N}\ge 1-(\epsilon_{B,N}+\delta_{BD,N})^2.
\]

With a source lower frame

\[
G_{\mathcal X,N}\succeq\gamma_NH_N,
\]

the effective residual source strength is

\[
\Lambda_{R,N}=\gamma_Nc_{\mathrm{hyb},N}.
\]

The route needs

\[
\gamma_Nc_{\mathrm{hyb},N}\to\infty
\]

after fixed/exhaustive tail promotion.

## Next step
Step 121 should construct the actual regularized co-Poisson/Müntz Dirichlet shadow family and determine whether it gives \(\delta_{BD,N}\to0\), a positive visibility floor, or a nonzero missed shadow sector.
'''
(base/'step120_results_summary.md').write_text(summary)

nonclaim = r'''
# Step 120 Nonclaim Boundary

Step 120 does not prove RH.

It does not prove that \(\delta_{BD,N}\to0\).

It does not prove that Burnol/co-Poisson atoms are Dirichlet-readable.

It does not license naive critical-line Dirichlet partial sums as a lawful shadow of \(\zeta(s)\widehat g(s)\).

It proves an asymptotic criterion:

\[
\delta_{BD,N}\to0
\iff
\operatorname{gap}(B_NY_{B,N},\operatorname{Ran}D_N)\to0
\]

in the normalized operator-norm sense, subject to fixed/exhaustive window promotion.

If the criterion fails, the missed shadow residual is

\[
\Xi_{BD}=B^*(I-P_D)B.
\]

That residual must be separately absorbed, shown compact/tail, or recorded as a nonclaim.
'''
(base/'nonclaim_boundary_step120.md').write_text(nonclaim)

schema = {
    'step': 120,
    'title': 'Burnol-to-Dirichlet Shadow Asymptotic Criterion',
    'active_objects': ['B_N','D_N','A_N','delta_BD_N','Xi_BD_N','c_hyb_N','gamma_N'],
    'main_criterion': 'delta_BD_N = ||(I-P_D_N) B_N G_B_N^{-1/2}|| -> 0',
    'statuses': ['shadow_complete','positive_floor','compact_missed_shadow','nonzero_blind_sector'],
    'next_step': 'Regularized co-Poisson/Müntz Dirichlet shadow construction'
}
(base/'step120_schema.json').write_text(json.dumps(schema, indent=2))

# Add small run/check script
check_py = r'''
import numpy as np

def shadow_defect(B, D):
    # B: H x d Burnol synthesis with full column rank
    # D: H x m Dirichlet synthesis
    QD, _ = np.linalg.qr(D)
    PD = QD @ QD.T
    G = B.T @ B
    vals, vecs = np.linalg.eigh(G)
    invsqrt = vecs @ np.diag(1/np.sqrt(np.maximum(vals, 1e-14))) @ vecs.T
    E = (np.eye(B.shape[0])-PD) @ B @ invsqrt
    s = np.linalg.svd(E, compute_uv=False)[0]
    return s, 1-s*s

if __name__ == '__main__':
    rng = np.random.default_rng(120)
    H, d, m = 32, 6, 12
    B, _ = np.linalg.qr(rng.normal(size=(H,d)))
    D, _ = np.linalg.qr(np.concatenate([B + 0.1*rng.normal(size=(H,d)), rng.normal(size=(H,m-d))], axis=1))
    delta, c = shadow_defect(B, D)
    print({'delta_BD': float(delta), 'c_visibility': float(c)})
'''
(base/'run_shadow_asymptotic_step120.py').write_text(check_py)

# structural latex check
tex_text = tex
balance = []
for env in ['theorem','lemma','proposition','definition','warning','corollary','enumerate','document']:
    balance.append({'environment':env, 'begin':tex_text.count('\\begin{'+env+'}'), 'end':tex_text.count('\\end{'+env+'}')})
pd.DataFrame(balance).to_csv(base/'latex_structure_check_step120.csv', index=False)

# Zip selected artifacts
zip_path = base/'step120_shadow_asymptotic_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in base.iterdir():
        if path.name == zip_path.name: continue
        z.write(path, arcname=path.name)

print('created', base)
print('files', len(list(base.iterdir())))
