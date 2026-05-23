import json
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import zipfile

OUT = Path('/mnt/data/rh_membrane_step156_xi_bc_schatten_tail')
OUT.mkdir(parents=True, exist_ok=True)

N = 240
n = np.arange(1, N+1, dtype=float)
profiles = {
    'exact_or_finite_rank': np.r_[np.linspace(1.0, 0.2, 12), np.zeros(N-12)],
    'trace_payable_compact': n**(-1.20),
    'compact_not_trace_by_square_tail': n**(-0.35),
    'noncompact_floor': 0.18 + 0.82*n**(-0.45),
}

singular_csv = OUT/'xi_bc_singular_value_scenarios_step156.csv'
with singular_csv.open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['index'] + list(profiles.keys()))
    for i in range(N):
        writer.writerow([i+1] + [profiles[k][i] for k in profiles])

plt.figure(figsize=(8,5))
for k,s in profiles.items():
    plt.loglog(n, np.maximum(s, 1e-16), label=k.replace('_',' '))
plt.xlabel('singular-value index n')
plt.ylabel('s_n proxy')
plt.title('Step 156: Xi^BC residual-kernel singular profiles')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_residual_kernel_singular_profiles_step156.png', dpi=180)
plt.close()

tail_csv = OUT/'xi_bc_schatten_tail_payability_step156.csv'
rows=[]
for k,s in profiles.items():
    tail2 = np.array([np.sum(s[i:]**2) for i in range(N)])
    tail1 = np.array([np.sum(s[i:]) for i in range(N)])
    for cutoff in [1,5,10,20,40,80,120,180,220]:
        rows.append({
            'profile': k,
            'cutoff_N': cutoff,
            'tail_sum_singular_values': float(tail1[cutoff-1]),
            'tail_sum_squares': float(tail2[cutoff-1]),
            'status_proxy': 'trace_tail_payable' if tail1[cutoff-1] < 0.05 else ('HS_tail_payable' if tail2[cutoff-1] < 0.05 else 'not_paid_at_this_cutoff')
        })
with tail_csv.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

plt.figure(figsize=(8,5))
for k,s in profiles.items():
    tail2 = np.array([np.sum(s[i:]**2) for i in range(N)])
    plt.semilogy(n, np.maximum(tail2,1e-18), label=k.replace('_',' '))
plt.xlabel('window cutoff N')
plt.ylabel('tail energy proxy sum_{n>N} s_n^2')
plt.title('Step 156: residual-tail payability proxy')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_schatten_tail_payability_step156.png', dpi=180)
plt.close()

# Operator scenario table
scenarios = [
    {'scenario':'exact exclusion', 'condition':'C_l E_Z = 0', 'Schatten_status':'zero', 'tail_status':'closed', 'route_status':'proof-producing if earned'},
    {'scenario':'Hilbert-Schmidt residual', 'condition':'C_l E_Z in S_2', 'Schatten_status':'compact and trace-tail payable for Xi', 'tail_status':'closed with fixed/exhaustive ledger', 'route_status':'proof-producing if source budget not needed'},
    {'scenario':'compact non-trace residual', 'condition':'C_l E_Z compact but not sufficiently summable', 'Schatten_status':'compact only', 'tail_status':'requires separate weighted trace ledger', 'route_status':'partial diagnostic'},
    {'scenario':'Calkin noncompact residual', 'condition':'limsup s_n(C_l E_Z)>0', 'Schatten_status':'noncompact', 'tail_status':'not tail-payable by compact windows', 'route_status':'active nonclaim or new mechanism required'},
]
with (OUT/'xi_bc_schatten_classification_step156.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=scenarios[0].keys())
    writer.writeheader(); writer.writerows(scenarios)

# Simple bar/status plot
labels=[r['scenario'] for r in scenarios]
score=[1.0,0.75,0.35,0.0]
plt.figure(figsize=(8,4.8))
plt.barh(labels, score)
plt.xlabel('route closure score proxy')
plt.title('Step 156: Xi^BC residual classification')
plt.xlim(0,1.05)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_residual_route_status_step156.png', dpi=180)
plt.close()

# finite toy block: P as prolate-ish projection via time/freq cutoffs, shift, singular profiles.
# Keep simple deterministic matrices.
def dft_matrix(n):
    j,k=np.meshgrid(np.arange(n),np.arange(n), indexing='ij')
    return np.exp(-2j*np.pi*j*k/n)/np.sqrt(n)
M=96
F=dft_matrix(M)
# time projection to central region and freq projection to low frequencies, Sonin-like intersection via SVD of constraints
Tmask=np.zeros(M); Tmask[24:72]=1
P_T=np.diag(Tmask)
Fmask=np.zeros(M); Fmask[:16]=1; Fmask[-16:]=1
P_F=F.conj().T@np.diag(Fmask)@F
# Projection onto intersection of kernels of P_T and P_F
A=np.vstack([P_T, P_F])
U,Sv,Vh=np.linalg.svd(A, full_matrices=True)
rank=(Sv>1e-8).sum()
Null=Vh.conj().T[:, rank:]
P=Null@Null.conj().T

def shift_matrix(n, sh):
    S=np.zeros((n,n), dtype=complex)
    for i in range(n):
        S[(i+sh)%n,i]=1
    return S
shifts=[1,2,4,8,12]
sv_rows=[]
plt.figure(figsize=(8,5))
for sh in shifts:
    T=shift_matrix(M, sh)
    C=(np.eye(M)-P)@T@P
    sv=np.linalg.svd(C, compute_uv=False)
    for i,val in enumerate(sv[:40],1):
        sv_rows.append({'shift': sh, 'index': i, 'singular_value': float(val)})
    plt.semilogy(np.arange(1,41), sv[:40], label=f'shift {sh}')
plt.xlabel('singular index')
plt.ylabel('singular value')
plt.title('Toy shifted Sonin/prolate commutator block singular values')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_toy_commutator_singular_values_step156.png', dpi=180)
plt.close()
with (OUT/'xi_bc_toy_commutator_singular_values_step156.csv').open('w', newline='') as f:
    writer=csv.DictWriter(f, fieldnames=['shift','index','singular_value'])
    writer.writeheader(); writer.writerows(sv_rows)

# Gate tables
gate_rows=[
    {'gate':'E_exact', 'test':'C_l eta_{rho,k}=0 for all visible zero evaluators', 'current_status':'not earned', 'failure_residual':'Xi_BC active'},
    {'gate':'T_compact', 'test':'C_l E_Z compact / singular values -> 0', 'current_status':'not earned; toy nonzero', 'failure_residual':'Calkin component possible'},
    {'gate':'T_trace_tail', 'test':'C_l E_Z in S_2 or Xi_BC trace-class under fixed ledger', 'current_status':'not earned', 'failure_residual':'moving-window only'},
    {'gate':'S_source', 'test':'non-circular source budget avoiding positive trace obstruction', 'current_status':'blocked in ordinary positive-frame form', 'failure_residual':'source-budget collapse circularity'},
    {'gate':'N_scope', 'test':'carry Xi_BC explicitly as adequacy residual', 'current_status':'active', 'failure_residual':'not a proof of RH'},
]
with (OUT/'xi_bc_schatten_gate_table_step156.csv').open('w', newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(gate_rows[0].keys()))
    writer.writeheader(); writer.writerows(gate_rows)

thm_rows=[
    {'item':'Residual operator', 'formula':'A_l = C_l E_Z, C_l=(I-P_inf)M_{m_l}P_inf', 'meaning':'operator taking zero-evaluator coefficients to shifted off-Sonin residuals'},
    {'item':'Kernel', 'formula':'R_l(z,w)=<A_l e_z,A_l e_w>', 'meaning':'positive Xi_BC Gram kernel'},
    {'item':'Compactness criterion', 'formula':'Xi_BC compact iff A_l^*A_l compact; sufficient A_l compact', 'meaning':'tail payability requires spectral decay'},
    {'item':'Noncompact obstruction', 'formula':'exists weak-null unit u_n with ||A_l u_n|| >= c >0', 'meaning':'Calkin sector survives; compact tail cannot pay'},
    {'item':'Trace tail criterion', 'formula':'sum s_n(A_l)^2 < infinity', 'meaning':'Xi_BC trace-class and completed trace-tail payable'},
]
with (OUT/'theorem_map_step156.csv').open('w', newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(thm_rows[0].keys()))
    writer.writeheader(); writer.writerows(thm_rows)

task_rows=[
    {'task':'Identify exact pulled evaluator synthesis E_Z', 'owner':'framework/RH', 'status':'open', 'next_evidence':'Burnol kernel formula plus semilocal transport'},
    {'task':'Prove compactness or noncompactness of A_l=C_l E_Z', 'owner':'operator theory', 'status':'open', 'next_evidence':'weak-null sequence or compact smoothing envelope'},
    {'task':'If compact, prove trace-tail summability', 'owner':'operator theory', 'status':'open', 'next_evidence':'Schatten p estimate for Hankel/projection square'},
    {'task':'If noncompact, carry Xi_BC as scoped residual', 'owner':'manuscript', 'status':'active fallback', 'next_evidence':'nonclaim theorem statement'},
]
with (OUT/'construction_tasks_step156.csv').open('w', newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(task_rows[0].keys()))
    writer.writeheader(); writer.writerows(task_rows)

route_rows=[
    {'route':'Direct exclusion', 'status':'not earned', 'reason':'raw shift does not create zeta factor and commutator does not vanish formally'},
    {'route':'Compact/tail payment', 'status':'open', 'reason':'requires Schatten/tail estimate for pulled residual kernel'},
    {'route':'Positive source absorption', 'status':'blocked as shortcut', 'reason':'source-budget condition is collapse-strength'},
    {'route':'Scoped residual theorem', 'status':'active', 'reason':'Xi_BC remains explicit adequacy residual'},
]
with (OUT/'route_status_step156.csv').open('w', newline='') as f:
    writer=csv.DictWriter(f, fieldnames=list(route_rows[0].keys()))
    writer.writeheader(); writer.writerows(route_rows)

# Markdown / TeX / schema
summary = r'''# Step 156: Xi^BC Residual-Kernel Schatten/Tail Audit

## Verdict

The active Burnol/co-Poisson adequacy residual

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}
\]

is not yet classified as exact, compact/tail-payable, or non-circularly source-absorbed.
The correct operator to audit is

\[
A_\ell=C_\ell E_Z,
\qquad
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\]

where \(E_Z\) synthesizes the pulled Burnol zero-evaluator family
\(\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}\).

## Main criteria

* exact exclusion: \(A_\ell=0\);
* compact/tail-payable: \(A_\ell\) compact, with stronger trace-tail payoff if \(A_\ell\in\mathcal S_2\);
* noncompact obstruction: a weak-null unit sequence \(u_n\) with \(\|A_\ell u_n\|\ge c>0\);
* source absorption: blocked in the ordinary positive-frame/fixed-ledger route by the Step 149--150 source-budget obstruction;
* scoped residual: currently active.

## Bottom line

The residual is now a projected Sonine-kernel Hankel square.  A compactness theorem for
\(C_\ell E_Z\) would make it tail-payable.  A weak-null lower-bound theorem would show a genuine
Calkin residual.  Neither is currently earned.
'''
(OUT/'step156_results_summary.md').write_text(summary)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\title{Step 156: $\Xi^{\rm BC}$ Residual-Kernel Schatten/Tail Audit}
\author{Riemann Membrane Construction Log}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\begin{document}
\maketitle

\section{Active residual}
The direct residual-exclusion route has reduced the remaining Burnol/co-Poisson adequacy
obstruction to
\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0,
\qquad
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]
For $a<1$, Burnol's carrier theorem gives $P_a=Y_a^\perp$, so $\Xi^{\rm BC}=0$ is equivalent to
$\operatorname{Ran}\mathfrak B_{\ell,a}\subseteq P_a$.

Let
\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}
\]
be the pulled zero evaluators and define the synthesis map $E_Z$ by
\[
E_Z c=\sum_{(\rho,k)} c_{\rho,k}\eta^a_{\rho,k}.
\]
Let
\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad
m_\ell(s)=e^{-\ell(1/2-s)}.
\]
Then the residual on the zero-evaluator side is represented by
\[
A_\ell=C_\ell E_Z,
\qquad
\mathcal R_\ell(z,w)=\langle A_\ell e_z,A_\ell e_w\rangle.
\]

\section{Schatten and tail criteria}
\begin{proposition}[Residual-kernel criteria]
Let $A_\ell=C_\ell E_Z$ be the closed residual synthesis operator on its natural domain.
Then
\[
\Xi^{\rm BC}_\ell=E_Z^*C_\ell^*C_\ell E_Z=A_\ell^*A_\ell.
\]
Consequently:
\begin{enumerate}
\item exact exclusion holds iff $A_\ell=0$;
\item compact tail-payment is available if $A_\ell$ is compact;
\item trace-tail payment for the positive residual is available if $A_\ell\in\mathcal S_2$;
\item noncompactness is certified by a weak-null unit sequence $u_n$ with $\|A_\ell u_n\|\ge c>0$.
\end{enumerate}
\end{proposition}

\begin{theorem}[Classification after the audit]
At Step 156, none of the proof-producing statuses is earned automatically:
\[
A_\ell=0 \quad\text{not proved},
\]
\[
A_\ell\in\mathcal K \quad\text{not proved},
\]
\[
A_\ell\in\mathcal S_2 \quad\text{not proved},
\]
while ordinary positive source absorption is blocked as a shortcut by the fixed-ledger source-budget obstruction.
Therefore $\Xi^{\rm BC}$ remains an active adequacy residual unless a new compactness, trace-tail,
or direct co-Poisson factorization theorem is supplied.
\end{theorem}

\section{Next obligation}
The next proof-producing target is a Calkin classification:
\[
[A_\ell]=0 \quad\text{in the Calkin algebra}
\]
or a lower-bound witness showing $[A_\ell]\ne0$.
Equivalently, prove compact smoothing of the pulled zero-evaluator family, or construct a boundary-packet
weak-null sequence seen by the evaluators.

\end{document}
'''
(OUT/'xi_bc_schatten_tail_step156.tex').write_text(tex)

nonclaim = '''# Step 156 nonclaim boundary

Step 156 does not prove RH, does not prove Xi^BC=0, and does not prove that Xi^BC is compact.
It classifies the exact operator-theoretic obligations for making Xi^BC tail-payable or for declaring it a genuine scoped adequacy residual.

Disallowed overreads:
- raw log-shift annihilates Burnol zero evaluators;
- compactness follows from finite-window plots;
- trace-class weighted ledgers automatically imply source compatibility;
- positive source-frame absorption closes the residual without a collapse-strength budget.
'''
(OUT/'nonclaim_boundary_step156.md').write_text(nonclaim)

schema = {
    'step': 156,
    'title': 'Xi^BC residual-kernel Schatten/tail audit',
    'active_residual': 'Xi_BC = B^* Pi_Y B',
    'operator': 'A_l = (I-P_inf) M_m P_inf E_Z',
    'statuses': ['exact_exclusion', 'compact_tail_payable', 'trace_tail_payable', 'noncompact_Calkin_residual', 'scoped_nonclaim'],
    'verdict': 'not yet exact, not yet tail-paid, not source-absorbed; scoped residual active',
    'next_step': 'Step 157: Calkin/noncompactness test for A_l or compact smoothing theorem for pulled evaluators'
}
(OUT/'step156_schema.json').write_text(json.dumps(schema, indent=2))

# zip all selected artifacts
zip_path = OUT/'step156_xi_bc_schatten_tail_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)

checks = {
    'files_created': len(list(OUT.iterdir())),
    'max_commutator_sv_shift1': float(max([r['singular_value'] for r in sv_rows if r['shift']==1])),
    'profiles': list(profiles.keys()),
    'zip': str(zip_path)
}
(OUT/'step156_check_results.json').write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
