from pathlib import Path
import json, csv, math
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step116_xi_bc_source_absorption')
out.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{geometry}
\usepackage{enumitem}
\geometry{margin=1in}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}

\newcommand{\XiBC}{\Xi^{\mathrm{BC}}}
\newcommand{\HB}{\mathcal H_{\mathcal B}}
\newcommand{\HR}{\mathcal H_{\mathcal R}}
\newcommand{\calB}{\mathcal B}
\newcommand{\calR}{\mathcal R}
\newcommand{\calX}{\mathcal X}
\newcommand{\pre}{\preceq}
\newcommand{\suc}{\succeq}
\newcommand{\Ran}{\operatorname{Ran}}
\newcommand{\Ker}{\operatorname{Ker}}
\newcommand{\tr}{\operatorname{tr}}

\title{Step 116: Residual-Specific Hecke/Dirichlet Source Absorption for $\Xi^{\mathrm{BC}}$}
\author{RATCHET RH Membrane Program}
\date{}

\begin{document}
\maketitle

\section{Purpose}
Steps 104--105 showed that the raw shifted Sonin/prolate off-diagonal block
\[
P_\infty\tau_\ell(I-P_\infty)
\]
contains a noncompact boundary-packet sector. Step 115 then tested the clean
Burnol/co-Poisson shortcut and reduced it to the zero-evaluator residual
\[
\XiBC_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]
The present step states the source-coercivity theorem that must pay this residual
when zeta-factorization or direct zero-evaluator annihilation is not available.

\section{Residual sector}
Let $L_a$ be Burnol's extended Sonine carrier, $Y_a\subset L_a$ the closed span of
zeta-zero evaluator vectors, and $P_a=Y_a^\perp$ the co-Poisson complement for
$a<1$. For a finite-place log-shift mode $\ell$, define the transported boundary block
\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]
The boundary-to-co-Poisson residual is
\[
\boxed{\XiBC_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.}
\]
For a finite set of modes $\mathcal L_N$ with nonnegative weights $w_\ell$, set
\[
\XiBC_N=\sum_{\ell\in\mathcal L_N}w_\ell\XiBC_{\ell,a}.
\]
Let $\Pi_{\mathcal R,N}$ denote the projection onto the finite residual sector
\[
\mathcal R_N=\overline{\Ran(\XiBC_N)^{1/2}}.
\]

\section{Direct residual absorption}
\begin{definition}[Residual source frame]
A residual-specific source frame is a positive form
\[
F_n=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_\omega^*\Theta_\omega^{-1}Q_\omega
\]
on the completed anti-invariant response space. The family $\mathcal X_n$ must be
declared upstream: conductor windows, character families, weights, and coefficient
maps are fixed before looking at the residual eigenvectors.
\end{definition}

\begin{theorem}[Direct source absorption]
If
\[
\XiBC\preceq F_n+E_n,
\]
then every estimate of the form
\[
q_Z\le q_{\mathrm{pos}}+\XiBC+e
\]
promotes to
\[
q_Z\le q_{\mathrm{pos}}+F_n+E_n+e.
\]
Thus the boundary-to-co-Poisson residual is lawful if $E_n$ is an accepted defect
or tends to zero in a fixed/exhaustive ledger.
\end{theorem}

\begin{proof}
Immediate by Loewner monotonicity. The point is not algebraic difficulty but audit:
$F_n$ must be an upstream-visible source frame and $E_n$ must be recorded as a
residual defect.
\end{proof}

\section{Metric lower-frame absorption}
The direct inequality $\XiBC\preceq F_n$ may be too strong at a finite stage. The useful version is metric.

\begin{theorem}[Metric residual absorption]
Let $\Theta_0^-$ be the baseline anti-invariant response budget and suppose on the residual sector
\[
\boxed{\XiBC\preceq C_R(\Theta_0^-)^{-1}+T_R.}
\]
Assume that the source family satisfies the full residual lower-frame bound
\[
\boxed{\Pi_{\mathcal R}F_n\Pi_{\mathcal R}\succeq
\Lambda_n\Pi_{\mathcal R}(\Theta_0^-)^{-1}\Pi_{\mathcal R}-R_n,\qquad \Lambda_n\to\infty.}
\]
Then
\[
\boxed{\XiBC\preceq {C_R\over \Lambda_n}F_n+T_R+{C_R\over\Lambda_n}R_n.}
\]
Consequently the residual is absorbed if $T_R\to0$ and $\Lambda_n^{-1}R_n\to0$ in the fixed/exhaustive ledger sense.
\end{theorem}

\begin{proof}
On $\mathcal R$, the lower-frame inequality gives
\[
(\Theta_0^-)^{-1}\preceq \Lambda_n^{-1}F_n+\Lambda_n^{-1}R_n.
\]
Multiplying by $C_R$ and using $\XiBC\preceq C_R(\Theta_0^-)^{-1}+T_R$ yields the result.
\end{proof}

\section{Finite matrix source theorem}
Let $M_N:Y_{\mathcal R,N}\to H_N$ synthesize a finite residual dictionary with Gram
$G_{\mathcal R,N}=M_N^*M_N$. Let $D_N:\mathbb C^{I_N}\to H_N$ be a declared coefficient synthesis family and
$R_N=D_N^\dagger M_N$ its coefficient map. Let $H_N=D_N^*D_N$.

\begin{theorem}[Finite matrix lower-frame prototype]
If
\[
G_{\mathcal X,N}\succeq \gamma_NH_N
\]
and
\[
R_N^*H_NR_N\succeq c_NG_{\mathcal R,N},
\]
then
\[
\boxed{R_N^*G_{\mathcal X,N}R_N\succeq \gamma_Nc_NG_{\mathcal R,N}.}
\]
Thus the effective finite residual source strength is
\[
\boxed{\Lambda_N^{\mathrm{eff}}=\gamma_Nc_N.}
\]
\end{theorem}

\begin{proof}
By the first hypothesis,
\[
R_N^*G_{\mathcal X,N}R_N\succeq \gamma_NR_N^*H_NR_N.
\]
The second hypothesis gives the stated bound.
\end{proof}

\begin{remark}[Two independent hard pieces]
The Heap--Soundararajan mechanism targets $\gamma_N$: character/source strength on coefficient space.
The Burnol/co-Poisson visibility problem targets $c_N$: whether the residual boundary sector is visible to those coefficients.
Both are necessary; a scalar mollifier lower bound alone does not imply a matrix lower frame.
\end{remark}

\section{Completed promotion}
A finite residual absorption theorem is not an RH theorem unless the finite residual windows exhaust the completed ledger.
The required promotion record is
\[
\XiBC\preceq \iota_N\XiBC_N\iota_N^*+T_N,
\qquad \tr(T_N)\to0.
\]
Together with
\[
R_N^*G_{\mathcal X,N}R_N\succeq \Lambda_N^{\mathrm{eff}}G_{\mathcal R,N},
\qquad \Lambda_N^{\mathrm{eff}}\to\infty,
\]
this gives completed absorption of $\XiBC$.

\section{All-six record}
The residual source route requires the following six-channel record.
\begin{enumerate}[label=P\arabic*]
\item Rewrite/gauge: the residual block $\mathfrak B_{\ell,a}$ and projection $\Pi_{Y_a}$ are fixed before source selection.
\item Feasibility/null legality: null directions of $\XiBC$ and source kernels are quotiented or recorded.
\item Route/holonomy: log-shift modes $\ell$ from finite local factors are declared as the route family.
\item Staging/refinement: finite residual windows, conductor windows, and character windows carry tail records.
\item Packaging: Burnol/Sonine/co-Poisson carrier and semilocal Hardy--Titchmarsh transport are declared.
\item Audit/currency: Loewner source domination, lower-frame growth, and $\Xi$ residuals are audited.
\end{enumerate}

\section{Nonclaims}
This step does not prove RH. It does not prove $\XiBC=0$. It does not prove the Heap--Soundararajan operator lift, the Burnol residual visibility theorem, or the completed Plancherel tail theorem. It states the exact theorem shape that would make residual-specific source absorption lawful.

\end{document}
'''
(out/'xi_bc_source_absorption_step116.tex').write_text(tex)

summary = r'''
# Step 116: Residual-Specific Hecke/Dirichlet Source Absorption for \(\Xi^{\rm BC}\)

## Main output

Step 116 formalizes the fallback after the zeta-factorization shortcut failed in Step 115.

The active residual is

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]

This measures the part of a shifted boundary packet that is seen by Burnol's zero-evaluator sector rather than landing invisibly in the co-Poisson complement.

## Source absorption theorem

If

\[
\Xi^{\rm BC}\preceq F_n+E_n,
\]

then any bridge

\[
q_Z\le q_{\rm pos}+\Xi^{\rm BC}+e
\]

promotes to

\[
q_Z\le q_{\rm pos}+F_n+E_n+e.
\]

So the boundary residual is lawful only if it is directly dominated by an upstream-visible source frame, or if the remaining defect is explicitly carried.

## Metric lower-frame version

If

\[
\Xi^{\rm BC}\preceq C_R(\Theta_0^-)^{-1}+T_R
\]

and

\[
\Pi_{\mathcal R}F_n\Pi_{\mathcal R}
\succeq
\Lambda_n\Pi_{\mathcal R}(\Theta_0^-)^{-1}\Pi_{\mathcal R}-R_n,
\qquad \Lambda_n\to\infty,
\]

then

\[
\Xi^{\rm BC}
\preceq
{C_R\over\Lambda_n}F_n+T_R+{C_R\over\Lambda_n}R_n.
\]

This is the precise source-coercive payment rule for the residual sector.

## Finite matrix prototype

For a finite residual dictionary and coefficient map \(R_N\), if

\[
G_{\mathcal X,N}\succeq \gamma_NH_N
\]

and

\[
R_N^*H_NR_N\succeq c_NG_{\mathcal R,N},
\]

then

\[
R_N^*G_{\mathcal X,N}R_N\succeq \gamma_Nc_NG_{\mathcal R,N}.
\]

So the effective finite source strength is

\[
\Lambda_N^{\rm eff}=\gamma_Nc_N.
\]

The Heap--Soundararajan side targets \(\gamma_N\). The Burnol/co-Poisson visibility side targets \(c_N\). Both must survive promotion.

## Completed promotion

A finite residual result becomes load-bearing only with a fixed/exhaustive tail record:

\[
\Xi^{\rm BC}\preceq \iota_N\Xi^{\rm BC}_N\iota_N^*+T_N,
\qquad \operatorname{tr}T_N\to0.
\]

Without this, the result is finite-window support only.

## Bottom line

Step 116 turns the post-factorization residual into a precise source-coercivity obligation:

\[
\boxed{
\Xi^{\rm BC}\preceq F_n+E_n,
\quad
F_n\succeq\Lambda_n(\Theta_0^-)^{-1},
\quad
\Lambda_n\to\infty.
}
\]

The next hard step is to construct this source frame on the actual residual sector.
'''
(out/'step116_results_summary.md').write_text(summary)

# Gate table
rows = [
    ['gate','object','accepted_if','failure_status'],
    ['G1 residual definition','Xi^BC = B^* Pi_Y B','B, Pi_Y, and carrier maps are declared before sources','ambiguous residual / smuggled target'],
    ['G2 residual localization','R = closure Ran (Xi^BC)^{1/2}','finite windows approximate residual sector with tail','moving residual window only'],
    ['G3 direct absorption','Xi^BC <= F_n + E_n','source frame upstream-visible and E_n declared','unpaid boundary residual'],
    ['G4 lower-frame growth','F_n >= Lambda_n Theta^{-1} - R_n','Lambda_n -> infinity and scaled R_n vanishes','bounded or partial source strength'],
    ['G5 coefficient visibility','R_N^* H_N R_N >= c_N G_R','c_N not too small and tail promoted','coefficient blind spot'],
    ['G6 character/source strength','G_X,N >= gamma_N H_N','matrix lower moment estimate, not scalar only','scalar support evidence'],
    ['G7 product growth','gamma_N c_N -> infinity','effective source strength diverges','source unable to collapse budget'],
    ['G8 fixed/exhaustive ledger','Xi^BC <= iota_N Xi_N iota_N^* + T_N','tr(T_N)->0 or equivalent tail','finite-window support only'],
    ['G9 no-smuggling','source family and weights declared upstream','no residual-eigenvector/zero-selected sources','target-selected source'],
]
with open(out/'xi_bc_source_absorption_gate_table_step116.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

# theorem map
theorem_rows = [
    ['label','statement','depends_on','status'],
    ['T116.1','Direct residual absorption Xi^BC <= F_n + E_n promotes q_Z <= q_pos + F_n + defects','Loewner monotonicity','proved algebraically'],
    ['T116.2','Metric absorption from residual boundedness plus source lower-frame growth','positive baseline budget; residual lower frame','proved algebraically'],
    ['T116.3','Finite matrix moment lower-frame prototype: G_X >= gamma H and visibility c imply source lower frame gamma c','finite matrix positivity','proved algebraically'],
    ['T116.4','Completed promotion requires fixed/exhaustive tail Xi <= iota Xi_N iota^* + T_N','Steps 65--67 ledger criterion','theorem schema'],
    ['O116.1','Construct Hecke/Dirichlet source frame for residual sector','Heap--Soundararajan operator lift','open'],
    ['O116.2','Prove Burnol/co-Poisson residual visibility c_N does not collapse','Burnol density and boundary inclusion/residual visibility','open'],
]
with open(out/'theorem_map_step116.csv','w',newline='') as f:
    csv.writer(f).writerows(theorem_rows)

# arithmetic input table
input_rows = [
    ['input','purpose','literature_anchor','status'],
    ['Burnol Sonine/co-Poisson carrier','defines L_a, Y_a, P_a and residual Xi^BC','Burnol 2004; Burnol 2007','carrier backbone'],
    ['Boundary residual Xi^BC','isolates part of shifted boundary packets seen by zero evaluators','Steps 114--115','defined'],
    ['Dirichlet/Hecke character family','source sensors Q_omega','finite character orthogonality; Hecke Plancherel','needs completed lower frame'],
    ['Heap--Soundararajan dual mollifier','source strength gamma_N via matrix moment lift','Heap--Soundararajan 2022','scalar template only'],
    ['Burnol/co-Poisson atom family','coefficient visibility c_N','Burnol co-Poisson density/exhaustivity','needs theorem'],
    ['Semilocal Hardy--Titchmarsh carrier','ambient response geometry for finite local factors','CCM semilocal prolate','declared Tier-1 carrier'],
    ['Fixed/exhaustive tail','promote finite residual windows to completed ledger','framework Steps 65--67','required'],
]
with open(out/'arithmetic_input_table_step116.csv','w',newline='') as f:
    csv.writer(f).writerows(input_rows)

# route status
status_rows = [
    ['route','status','reason'],
    ['zeta-factorization shortcut','not earned','raw log shift does not create a zeta factor'],
    ['compactness shortcut','blocked for raw shifted Sonin block','Step 104 noncompactness and Step 105 compact-repair no-go'],
    ['Burnol atom visibility','partially viable','works for component inside P_a but residual outside P_a remains Xi^BC'],
    ['residual-specific source absorption','active route','directly targets Xi^BC with lower-frame sources'],
    ['zero-simplicity shortcut','out of scope','would be a smuggled gate under framework discipline'],
]
with open(out/'route_status_step116.csv','w',newline='') as f:
    csv.writer(f).writerows(status_rows)

nonclaim = r'''
# Step 116 nonclaim boundary

Step 116 does not prove RH.

It does not prove that \(\Xi^{\rm BC}=0\).

It does not prove zeta-factorization of shifted boundary packets.

It does not prove compactness of the semilocal residual.

It does not prove the Heap--Soundararajan scalar method lifts to an operator-valued matrix lower frame.

It does not prove the Burnol/co-Poisson coefficient visibility constant \(c_N\) stays bounded below.

It states the exact residual-specific source absorption theorem:

\[
\Xi^{\rm BC}\preceq F_n+E_n
\]

and the exact finite matrix prototype:

\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\qquad
R_N^*H_NR_N\succeq c_NG_{\mathcal R,N}
\Rightarrow
R_N^*G_{\mathcal X,N}R_N\succeq \gamma_Nc_NG_{\mathcal R,N}.
\]

All claims remain finite-window/support-only unless paired with fixed/exhaustive residual-tail promotion.
'''
(out/'nonclaim_boundary_step116.md').write_text(nonclaim)

schema = {
    'step': 116,
    'title': 'Residual-Specific Hecke/Dirichlet Source Absorption for Xi^BC',
    'central_object': 'Xi^BC_{ell,a} = B_{ell,a}^* Pi_{Y_a} B_{ell,a}',
    'active_route': 'source-coercivity on boundary-to-co-Poisson residual sector',
    'theorems': [
        'direct residual absorption',
        'metric lower-frame residual absorption',
        'finite matrix moment lower-frame prototype',
        'fixed/exhaustive residual-tail promotion schema'
    ],
    'hard_inputs': ['operator-valued Heap-Soundararajan lift', 'Burnol residual visibility', 'completed Plancherel/exhaustivity tail'],
    'nonclaims': ['RH not proved', 'Xi^BC not shown zero', 'compactness shortcut not recovered']
}
(out/'step116_schema.json').write_text(json.dumps(schema, indent=2))

# Python check script with actual calculations
check_script = r'''
import numpy as np
from pathlib import Path

def rand_spd(n, eps=0.5, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n,n))
    return A.T @ A + eps*np.eye(n)

def min_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

rng = np.random.default_rng(116)
out = Path(__file__).resolve().parent
n=12
Theta_inv = rand_spd(n, eps=1.0, seed=1)
C=2.5
# Xi <= C Theta_inv by construction
S = rand_spd(n, eps=0.1, seed=2)
scale = np.linalg.eigvalsh(np.linalg.solve(Theta_inv, S)).max()
Xi = C * Theta_inv * 0.5 + 0.1 * S / (scale+1)
# check residual absorption for several Lambdas
rows=[['Lambda','min_eig_source_minus_lower','min_eig_absorption_slack']]
for Lam in [1,2,4,8,16,32,64]:
    PSD = rand_spd(n, eps=0.0, seed=Lam)
    F = Lam*Theta_inv + PSD
    # Xi <= C/Lambda F should hold if Xi <= C Theta_inv and F >= Lambda Theta_inv; our Xi <= ~C Theta_inv.
    slack = (C/Lam)*F - Xi
    rows.append([Lam, min_eig(F - Lam*Theta_inv), min_eig(slack)])
with open(out/'residual_absorption_checks_step116.csv','w') as f:
    for r in rows:
        f.write(','.join(map(str,r))+'\n')
print(rows[-1])
'''
(out/'run_xi_bc_source_absorption_checks_step116.py').write_text(check_script)

# Generate numerical artifacts/plots
def min_eig(A):
    import numpy as np
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

rng = np.random.default_rng(116)
# 1. Residual absorption ladder
lams = np.arange(1,101)
C_R = 3.0
R_tail = 0.15*np.exp(-lams/25)
bound_coeff = C_R/lams + R_tail
plt.figure(figsize=(6,4))
plt.plot(lams, bound_coeff, label='residual allowance')
plt.xlabel(r'$\Lambda_n$')
plt.ylabel('allowance')
plt.title(r'Residual source absorption: $C_R/\Lambda_n$ plus tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'xi_bc_residual_absorption_step116.png', dpi=180)
plt.close()
with open(out/'xi_bc_residual_absorption_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Lambda','C_over_Lambda_plus_tail'])
    for L,b in zip(lams,bound_coeff): w.writerow([L,b])

# 2. product gamma*c scenarios
gamma = np.log1p(lams)**2
c_good = 0.5 + 0*lams
c_poly = 1/np.sqrt(lams)
c_bad = np.exp(-lams/20)
plt.figure(figsize=(6,4))
plt.plot(lams, gamma*c_good, label='c bounded')
plt.plot(lams, gamma*c_poly, label='c ~ n^-1/2')
plt.plot(lams, gamma*c_bad, label='c exponential decay')
plt.axhline(1,color='black',linewidth=.8)
plt.xlabel('stage n')
plt.ylabel(r'$\gamma_n c_n$')
plt.title('Effective source strength depends on visibility')
plt.legend()
plt.tight_layout()
plt.savefig(out/'effective_source_strength_step116.png', dpi=180)
plt.close()
with open(out/'effective_source_strength_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['n','gamma','c_bounded_product','c_poly_product','c_exp_product'])
    for n0,g,a,b,c in zip(lams,gamma,gamma*c_good,gamma*c_poly,gamma*c_bad): w.writerow([n0,g,a,b,c])

# 3. matrix lower frame random checks
rows=[['trial','n','gamma','c','min_slack']]
mins=[]
for trial in range(30):
    n=8
    A=rng.normal(size=(n,n)); GB=A.T@A+np.eye(n)
    R=rng.normal(size=(n,n))
    # normalize R to have visibility c relative to GB with H=I
    evals=np.linalg.eigvalsh(np.linalg.solve(GB, R.T@R))
    c=max(0.01, evals.min())
    gamma=1.0+0.1*trial
    GX=gamma*np.eye(n)+0.2*(rng.normal(size=(n,n))@rng.normal(size=(n,n)).T)
    # ensure GX >= gamma I by making PSD
    B=rng.normal(size=(n,n)); GX=gamma*np.eye(n)+B.T@B
    F=R.T@GX@R
    slack=F-gamma*c*GB
    me=min_eig(slack)
    mins.append(me); rows.append([trial,n,gamma,c,me])
with open(out/'matrix_lower_frame_checks_step116.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)
plt.figure(figsize=(6,4))
plt.plot(range(len(mins)), mins, marker='o')
plt.axhline(0,color='black',linewidth=.8)
plt.xlabel('trial')
plt.ylabel('min eigenvalue of certified slack')
plt.title('Finite matrix lower-frame sanity checks')
plt.tight_layout()
plt.savefig(out/'matrix_lower_frame_checks_step116.png', dpi=180)
plt.close()

# 4. partial coverage failure eigenvalues
n=20
rank=12
Q=np.zeros((n,n)); Q[:rank,:rank]=np.eye(rank)
eigs=np.linalg.eigvalsh(Q)
plt.figure(figsize=(6,4))
plt.step(np.arange(n), eigs, where='mid')
plt.xlabel('eigenvalue index')
plt.ylabel('source-frame eigenvalue')
plt.title('Partial residual source coverage leaves hidden kernel')
plt.tight_layout()
plt.savefig(out/'partial_residual_coverage_failure_step116.png', dpi=180)
plt.close()
with open(out/'partial_residual_coverage_failure_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['index','eigenvalue'])
    for i,e in enumerate(eigs): w.writerow([i,e])

# 5. finite window tail promotion
N=np.arange(1,101)
trace_tail=1/(N**1.1)
moving_no_tail=np.ones_like(N)*0.25
plt.figure(figsize=(6,4))
plt.loglog(N,trace_tail,label='accepted tail')
plt.loglog(N,moving_no_tail,label='uncontrolled moving-window tail')
plt.xlabel('window N')
plt.ylabel('tail trace')
plt.title('Residual finite-window promotion needs vanishing tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'residual_tail_promotion_step116.png', dpi=180)
plt.close()
with open(out/'residual_tail_promotion_step116.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['N','accepted_tail','uncontrolled_tail'])
    for i,a,b in zip(N,trace_tail,moving_no_tail): w.writerow([i,a,b])

# Zip artifacts
import zipfile
zip_path=out/'step116_xi_bc_source_absorption_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print('created', zip_path)
