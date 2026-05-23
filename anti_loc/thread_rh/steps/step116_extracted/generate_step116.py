import os, json, csv, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step116_xi_bc_source_absorption')
out.mkdir(parents=True, exist_ok=True)

# -------------------------
# Toy finite source absorption model
# -------------------------
rng = np.random.default_rng(116)

def psd_from_rank(n, rank, decay=1.0):
    U, _ = np.linalg.qr(rng.normal(size=(n, n)))
    vals = np.zeros(n)
    vals[:rank] = np.array([(j+1)**(-decay) for j in range(rank)])
    return U @ np.diag(vals) @ U.T, vals, U

n = 28
rank_res = 9
Xi, vals, U = psd_from_rank(n, rank_res, decay=0.35)
# support projection for Xi
P_R = U[:, :rank_res] @ U[:, :rank_res].T
# full coverage sources on residual sector
lambdas = np.array([0.8, 1.2, 1.8, 2.7, 4.0, 6.0, 8.8, 13.0, 19.0, 28.0, 42.0])
full_min = []
partial_min = []
res_capacity_full = []
res_capacity_partial = []
identity = np.eye(n)
# baseline metric (just I for toy)
Theta_inv = P_R + 1e-6*(identity-P_R)
for L in lambdas:
    # full source frame covers residual support
    F_full = L*P_R + 0.05*(identity-P_R)
    # partial source frame misses the last residual vector
    P_partial = U[:, :rank_res-1] @ U[:, :rank_res-1].T
    F_part = L*P_partial + 0.05*(identity-P_partial)
    full_eigs = np.linalg.eigvalsh(P_R @ F_full @ P_R + 1e-12*identity)
    part_eigs = np.linalg.eigvalsh(P_R @ F_part @ P_R + 1e-12*identity)
    full_min.append(np.min(full_eigs[-rank_res:]))
    partial_min.append(np.min(part_eigs[-rank_res:]))
    # residual capacity Xi^{1/2}(I+F)^{-1}Xi^{1/2}: trace proxy
    vals_x, vecs_x = np.linalg.eigh(Xi)
    Xi_half = vecs_x @ np.diag(np.sqrt(np.clip(vals_x,0,None))) @ vecs_x.T
    cap_full = np.trace(Xi_half @ np.linalg.inv(identity+F_full) @ Xi_half)
    cap_part = np.trace(Xi_half @ np.linalg.inv(identity+F_part) @ Xi_half)
    res_capacity_full.append(cap_full)
    res_capacity_partial.append(cap_part)

# Matrix lift constants model
Nvals = np.arange(1, 13)
gamma = 0.9*np.log(Nvals+2)**2  # source strength growth
c_good = 0.55 + 0.35*(1-np.exp(-Nvals/4))
c_bad = np.exp(-Nvals/4)
beta = 1.25
Lambda_good = gamma*c_good/beta
Lambda_bad = gamma*c_bad/beta

# visibility residual model epsilon_N^2 = residual_norm^2
atom_counts = np.arange(4, 100, 4)
eps_good = 0.85*np.exp(-atom_counts/40) + 0.05
eps_bad = 0.92 - 0.08*(1-np.exp(-atom_counts/60))
c_vis_good = 1-np.minimum(eps_good, 0.999)**2
c_vis_bad = 1-np.minimum(eps_bad, 0.999)**2

# finite residual sector source eigenvalues toy
# simulate full vs partial source matrix eigenvalues on residual support as function of number of characters
chars = np.arange(2, 34, 2)
eigs_full = 1 - np.exp(-chars/7)
eigs_partial = np.concatenate([1 - np.exp(-chars[:8]/7), np.full(len(chars)-8, 0.05)])

# Write CSVs
with open(out/'residual_absorption_ladder_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Lambda','full_source_min_eig_on_residual','partial_source_min_eig_on_residual','trace_capacity_full','trace_capacity_partial'])
    for row in zip(lambdas, full_min, partial_min, res_capacity_full, res_capacity_partial): w.writerow(row)
with open(out/'matrix_lift_constants_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['N','gamma_N','c_N_good','c_N_bad','beta_R','Lambda_good','Lambda_bad'])
    for row in zip(Nvals,gamma,c_good,c_bad,[beta]*len(Nvals),Lambda_good,Lambda_bad): w.writerow(row)
with open(out/'visibility_residual_scenarios_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['atom_count','epsilon_good','epsilon_bad','c_visibility_good','c_visibility_bad'])
    for row in zip(atom_counts, eps_good, eps_bad, c_vis_good, c_vis_bad): w.writerow(row)
with open(out/'residual_source_eigenvalues_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['num_sources','full_coverage_min_eig','partial_coverage_min_eig'])
    for row in zip(chars,eigs_full,eigs_partial): w.writerow(row)

# Plots
plt.figure(figsize=(7,4.5))
plt.plot(lambdas, res_capacity_full, marker='o', label='full residual coverage')
plt.plot(lambdas, res_capacity_partial, marker='s', label='partial coverage')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('source lower-frame scale $\\Lambda_n$')
plt.ylabel('trace residual capacity proxy')
plt.title('Residual-specific source absorption')
plt.legend(); plt.tight_layout()
plt.savefig(out/'xi_bc_source_absorption_step116.png', dpi=200); plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(Nvals, Lambda_good, marker='o', label='$\\gamma_N c_N/\\beta_R$ good visibility')
plt.plot(Nvals, Lambda_bad, marker='s', label='$\\gamma_N c_N/\\beta_R$ collapsing visibility')
plt.axhline(1, linestyle='--')
plt.xlabel('finite stage $N$'); plt.ylabel('effective residual-frame scale')
plt.title('Matrix moment lift: source strength times visibility')
plt.legend(); plt.tight_layout()
plt.savefig(out/'matrix_lift_effective_scale_step116.png', dpi=200); plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(atom_counts, c_vis_good, marker='o', label='declared atoms exhaust residual')
plt.plot(atom_counts, c_vis_bad, marker='s', label='persistent blind spot')
plt.xlabel('declared atom count')
plt.ylabel('$c_N=1-\\epsilon_N^2$')
plt.title('Visibility as spanning residual, not column norm')
plt.legend(); plt.tight_layout()
plt.savefig(out/'visibility_spanning_residual_step116.png', dpi=200); plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(chars, eigs_full, marker='o', label='full residual-sector source family')
plt.plot(chars, eigs_partial, marker='s', label='partial source family')
plt.xlabel('number of source characters/modes')
plt.ylabel('min source eigenvalue on residual sector')
plt.title('Residual source coverage: full vs partial')
plt.legend(); plt.tight_layout()
plt.savefig(out/'residual_source_coverage_step116.png', dpi=200); plt.close()

# Tables
boundary_source_gate = [
    ['G1_residual_support','Define support projection P_R=s(Xi^BC) and residual sector Y_R=Ran P_R','required','load-bearing'],
    ['G2_non_smuggled_sources','Character/Hecke family declared upstream, not selected by residual eigenvectors','required','no-smuggling'],
    ['G3_source_readouts','Define Q_omega on the residual sector and prove carrier-native legality','required','construction'],
    ['G4_residual_lower_frame','P_R F_n P_R >= Lambda_n P_R B_R P_R - R_n with Lambda_n -> infinity','required','hard analytic'],
    ['G5_matrix_lift','Finite version factors through R_N^* G_X,N R_N with gamma_N c_N / beta_R -> infinity','required','operator-valued lift'],
    ['G6_tail_exhaustivity','Finite residual windows promote to completed residual ledger with vanishing tail','required','fixed/exhaustive'],
    ['G7_defect_accounting','Uncharged residual recorded as E_n, not hidden in positivity claim','required','audit'],
    ['G8_all_six_records','P1-P6 statuses attached to source family, residual readout, transport, and audit','required','Six Birds'],
]
with open(out/'xi_bc_source_absorption_gate_table_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['gate','statement','status','note']); w.writerows(boundary_source_gate)

arithmetic_input = [
    ['Burnol/Sonine carrier','Y_a, P_a=Y_a^perp, co-Poisson subspaces, zero evaluator span','used for residual definition and tail/exhaustivity'],
    ['Boundary residual','Xi^BC=B^* Pi_Ya B','operator-valued adequacy residual to be absorbed'],
    ['Heap-Soundararajan mechanism','short Dirichlet polynomial mean values','template for gamma_N source strength'],
    ['Matrix moment lift','uniform lower bound for all coefficient vectors','required; scalar moment lower bounds alone are insufficient'],
    ['Coefficient visibility','R_N^* H_N R_N >= c_N G_B,N','separate Burnol-native spanning gate'],
    ['Semilocal CCM carrier','finite local factors inside Hardy-Titchmarsh response geometry','ambient space for finite-place residual'],
    ['Conrey-Li survival','avoid de Branges/RKHS positivity collapse','negative control'],
]
with open(out/'arithmetic_input_table_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['input','role','status']); w.writerows(arithmetic_input)

theorem_map = [
    ['T116.1','Residual support decomposition','Xi^BC decomposes into support projection plus null sector; only support needs source charging'],
    ['T116.2','Residual source-capacity collapse','If F_n >= Lambda_n Xi^BC on residual support then Xi^BC-capacity relative to C+F_n collapses like Lambda_n^{-1}'],
    ['T116.3','Finite matrix moment absorption','G_X>=gamma H and R^*HR>=cG_B and Xi_N<=beta G_B imply source absorption with Lambda=gamma c/beta'],
    ['T116.4','Partial coverage obstruction','If a residual vector lies in intersection of kernels of Q_omega R_N, source absorption fails'],
    ['T116.5','Tail-promotion condition','Finite residual absorption promotes only with fixed/exhaustive tail record'],
]
with open(out/'theorem_map_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','name','claim']); w.writerows(theorem_map)

construction_tasks = [
    ['C1','Define the completed residual sector Y_R=s(Xi^BC)Y_B and its finite windows Y_R,N'],
    ['C2','Build non-smuggled Hecke/Dirichlet readouts Q_omega restricted to Y_R'],
    ['C3','Prove finite matrix moment lower bounds on R_R,N^*G_X,N R_R,N'],
    ['C4','Prove coefficient visibility c_R,N for the residual dictionary, not just the full boundary dictionary'],
    ['C5','Show gamma_N c_R,N / beta_R,N -> infinity after tail promotion'],
    ['C6','Record any residual miss as Xi-tail or scoped nonclaim'],
]
with open(out/'construction_tasks_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','task']); w.writerows(construction_tasks)

route_status = [
    ['compactness_shortcut','blocked for raw shifted Sonin block; only essential semilocal prolate repair could revive it'],
    ['zeta_factorization_shortcut','not earned by raw log shift; residual Xi^BC remains'],
    ['Burnol_atom_visibility','reduces c_N to spanning residual; useful but not enough for zero-evaluator visible component'],
    ['residual_source_absorption','active route; requires lower frame on support of Xi^BC'],
]
with open(out/'route_status_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['route','status']); w.writerows(route_status)

# LaTeX note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,enumitem,booktabs,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{warning}{Warning}
\title{Step 116: Residual-Specific Hecke/Dirichlet Source Absorption for $\Xi^{\rm BC}$}
\author{RATCHET RH Membrane Program}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Steps 114--115 reduced the boundary-to-co-Poisson shortcut to the residual
\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq 0.
\]
This is the part of the shifted Sonin/prolate boundary packet that is visible to the zero-evaluator sector and therefore not accounted for by the declared Burnol/co-Poisson atom span.  The present step formulates the residual-specific source absorption theorem: instead of asking character/Hecke sources to cover the entire boundary sector, ask first that they cover the support of $\Xi^{\rm BC}$.

\section{Residual support}
Let $Y_{\mathcal B}$ be the boundary-packet response space and let
\[
X:=\Xi^{\rm BC}\in\mathcal B(Y_{\mathcal B})_+.
\]
Define the residual support projection
\[
P_R=s(X)=\text{orthogonal projection onto }\overline{\operatorname{Ran}X}.
\]
The source route is accepted only on the residual support.  Any vector in $\ker X$ does not need to be charged for this residual, while any vector in $P_RY_{\mathcal B}$ must be charged by upstream-visible sources or carried as a defect.

\section{Residual-specific source frame}
Let $\mathcal X_n$ be an upstream-visible Dirichlet/Hecke character family and let
\[
Q_{\omega,R}:P_RY_{\mathcal B}\to Z_\omega
\]
be the residual-sector readout associated to $\omega$.  Set
\[
F_{R,n}=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_{\omega,R}^{*}\Theta_{\omega}^{-1}Q_{\omega,R}.
\]
The target lower-frame condition is
\[
P_R F_{R,n}P_R\succeq \Lambda_n P_R B_R P_R-R_n^{R},\qquad \Lambda_n\to\infty,
\]
where $B_R$ is the chosen residual baseline form and $R_n^R$ is a declared source-defect form.

\begin{theorem}[Residual source-capacity collapse]
Assume $X\preceq \beta_R B_R$ on $P_RY_{\mathcal B}$ and
\[
P_RF_{R,n}P_R\succeq \Lambda_n P_RB_RP_R-R_n^R.
\]
If $R_n^R\preceq \epsilon_n\Lambda_n B_R$ with $\epsilon_n<1$, then
\[
X\preceq \frac{\beta_R}{(1-\epsilon_n)\Lambda_n}F_{R,n}
\]
on the residual support.  Consequently, for the sourced energy $C_n=C_0+F_{R,n}$,
\[
X^{1/2}C_n^{-1}X^{1/2}\preceq O(\Lambda_n^{-1})
\]
whenever $C_0\succeq0$ and the inverse is read on the legal quotient.
\end{theorem}

\section{Finite matrix-moment prototype}
Let $Y_{R,N}$ be a finite residual-sector window with Gram form $G_{R,N}$.  Let
\[
R_{R,N}:Y_{R,N}\to\mathbb C^{\mathcal N_N}
\]
be the residual coefficient map into a short Dirichlet-polynomial coefficient space with coefficient metric $H_N$.  Let
\[
G_{\mathcal X,N}(m,n)=\sum_{\omega\in\mathcal X_N}\lambda_{\omega,N}\omega(n)\overline{\omega(m)}
\]
be the character/source Gram matrix.

\begin{theorem}[Finite residual absorption]
Assume
\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\qquad
R_{R,N}^{*}H_NR_{R,N}\succeq c_{R,N}G_{R,N},
\]
and
\[
X_N\preceq \beta_{R,N}G_{R,N}.
\]
Then
\[
R_{R,N}^{*}G_{\mathcal X,N}R_{R,N}\succeq
\frac{\gamma_Nc_{R,N}}{\beta_{R,N}}X_N.
\]
Thus the finite residual source scale is
\[
\Lambda_{R,N}=\frac{\gamma_Nc_{R,N}}{\beta_{R,N}}.
\]
The residual source route needs $\Lambda_{R,N}\to\infty$ after fixed/exhaustive promotion.
\end{theorem}

\section{Obstruction}
If there exists a nonzero $y\in P_RY_{R,N}$ such that
\[
Q_{\omega,R}y=0\qquad\forall\omega\in\mathcal X_N,
\]
then $F_{R,N}$ has a residual kernel and no source-strength growth can absorb $X_N$ along $y$.  This is the residual-specific version of the partial character coverage obstruction.

\section{Interpretation}
The residual $\Xi^{\rm BC}$ is not a nuisance term.  It is the exact blind spot left when the shifted boundary packets fail to land in the Burnol/co-Poisson complement.  The proof must either make it vanish, prove it has a vanishing tail, or show that a non-smuggled Hecke/Dirichlet source family charges its support with a lower frame whose scale diverges.

\section{Nonclaim boundary}
This step does not prove RH, does not prove the required Hecke lower frame, and does not prove that Heap--Soundararajan scalar lower moments imply an operator-valued lower frame.  It only formulates the exact residual-sector source-absorption theorem and finite matrix-moment gate.

\end{document}
'''
(out/'xi_bc_source_absorption_step116.tex').write_text(tex)

summary = r'''
# Step 116: Residual-Specific Hecke/Dirichlet Source Absorption for \(\Xi^{\rm BC}\)

This step makes the residual from Step 115 load-bearing:

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]

The compactness shortcut and raw zeta-factorization shortcut are not earned.  Therefore the active route is source absorption on the support of \(\Xi^{\rm BC}\).

## Main theorem

Let

\[
X=\Xi^{\rm BC}\succeq0,
\qquad P_R=s(X).
\]

Let

\[
F_{R,n}=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_{\omega,R}^{*}\Theta_\omega^{-1}Q_{\omega,R}
\]

be the residual-specific Hecke/Dirichlet source frame.  If

\[
X\preceq \beta_R B_R
\]

and

\[
P_RF_{R,n}P_R\succeq \Lambda_nP_RB_RP_R-R_n^R,
\qquad \Lambda_n\to\infty,
\]

with \(R_n^R\) negligible relative to \(\Lambda_nB_R\), then the residual capacity collapses like

\[
X^{1/2}(C_0+F_{R,n})^{-1}X^{1/2}=O(\Lambda_n^{-1}).
\]

## Finite matrix-moment gate

For a finite residual window:

\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\]

\[
R_{R,N}^{*}H_NR_{R,N}\succeq c_{R,N}G_{R,N},
\]

\[
X_N\preceq \beta_{R,N}G_{R,N},
\]

imply

\[
R_{R,N}^{*}G_{\mathcal X,N}R_{R,N}
\succeq
\frac{\gamma_Nc_{R,N}}{\beta_{R,N}}X_N.
\]

So the residual source scale is

\[
\Lambda_{R,N}=\frac{\gamma_Nc_{R,N}}{\beta_{R,N}}.
\]

The RH source route needs \(\Lambda_{R,N}\to\infty\) after fixed/exhaustive promotion.

## Interpretation

\(\Xi^{\rm BC}\) is the part of the shifted boundary packets that remains visible to the zero-evaluator sector and therefore is not covered by Burnol/co-Poisson atoms.  The proof must either make this residual vanish or charge it with non-smuggled Hecke/Dirichlet sources.

## Next step

Step 117 should specialize this theorem to one concrete source family: Dirichlet conductor windows or Hecke/idèle characters.  The immediate target is to define \(Q_{\omega,R}\) and determine whether finite conductor orthogonality can lower-bound the residual sector, not merely the full finite quotient.
'''
(out/'step116_results_summary.md').write_text(summary)

nonclaim = r'''
# Nonclaim Boundary — Step 116

This step does not claim:

- RH is proved.
- \(\Xi^{\rm BC}=0\).
- Burnol/co-Poisson atoms cover the boundary-packet sector.
- Heap--Soundararajan scalar moment lower bounds automatically imply operator-valued lower frames.
- Finite character orthogonality is a completed lower frame.
- A de Branges/RKHS positivity condition is being adopted.

It claims only:

- If the residual support of \(\Xi^{\rm BC}\) is charged by a non-smuggled Hecke/Dirichlet source lower frame with diverging scale, then the residual capacity collapses.
- In finite windows, this reduces to a matrix moment lower-bound problem with constants \(\gamma_N\), \(c_{R,N}\), and \(\beta_{R,N}\).
'''
(out/'nonclaim_boundary_step116.md').write_text(nonclaim)

schema = {
    'step': 116,
    'title': 'Residual-specific Hecke/Dirichlet source absorption for Xi^BC',
    'objects': {
        'Xi_BC': 'boundary-to-co-Poisson adequacy residual B^* Pi_Ya B',
        'P_R': 'support projection of Xi_BC',
        'F_R_n': 'residual-specific source frame from Hecke/Dirichlet readouts',
        'R_R_N': 'finite residual coefficient map',
        'gamma_N': 'source Gram lower-frame strength',
        'c_R_N': 'residual coefficient visibility',
        'beta_R_N': 'residual size relative to finite Gram'
    },
    'main_condition': 'gamma_N * c_R_N / beta_R_N -> infinity with fixed/exhaustive promotion',
    'status': 'theorem schema and finite algebra prototype; analytic lower-frame proof still open'
}
(out/'step116_schema.json').write_text(json.dumps(schema, indent=2))

# README-like summary of checks
check_summary = {
    'identity': 'finite residual source absorption and matrix lower-frame checks generated as toy sanity checks only',
    'not_evidence': 'plots are algebraic finite models, not numerical evidence for RH',
    'active_gate': 'prove residual-specific operator-valued lower frame on support of Xi^BC'
}
(out/'finite_check_summary_step116.json').write_text(json.dumps(check_summary, indent=2))

# Zip all artifacts
zip_path = out/'step116_xi_bc_source_absorption_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name and p.is_file():
            z.write(p, arcname=p.name)

print('created', len(list(out.iterdir())), 'files in', out)
