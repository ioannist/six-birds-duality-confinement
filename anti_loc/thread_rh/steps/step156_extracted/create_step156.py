from pathlib import Path
import json, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base = Path('/mnt/data/rh_membrane_step156_xi_bc_schatten_tail')
base.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}

\title{Step 156: $\Xi^{\rm BC}$ Residual-Kernel Schatten/Tail Audit}
\author{Riemann--membrane construction note}
\date{}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\newtheorem{warning}{Warning}
\newtheorem{audit}{Audit}

\begin{document}
\maketitle

\section{Purpose}
Steps 151--154 reduced direct residual exclusion to the projected Sonine-kernel commutator
\[
        C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
        \qquad
        m_\ell(s)=e^{-\ell(1/2-s)},
\]
acting on the pulled Burnol zero-evaluator family
\[
        \eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}.
\]
The active adequacy residual is
\[
        \Xi^{\rm BC}_{\ell,a}
        =\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]
Step 156 asks whether this residual is compact, Schatten, tail-payable, or genuinely noncompact.

\section{Normalized residual kernel}
Let $\mathcal Z_a$ denote the zero-evaluator index set
\[
        z=(\rho,k),\qquad 0\le k<m_\rho,
\]
and write $\eta_z=\eta^a_{\rho,k}$.  Let
\[
        E:c_{00}(\mathcal Z_a)\to H_\infty,
        \qquad E e_z=\eta_z,
\]
be the pulled-evaluator synthesis map, and let
\[
        G=E^*E
\]
be its Gram operator on finite windows.  On each finite legal window we work after quotienting by
$\ker G$ and use the normalized synthesis
\[
        \widetilde E=E G^{-1/2}.
\]
The normalized residual-kernel operator is
\[
        \boxed{
        \mathcal R_\ell
        =\widetilde E^*C_\ell^*C_\ell\widetilde E.
        }
\]
Equivalently,
\[
        \mathcal R_\ell(z,w)
        =\left\langle C_\ell\widetilde\eta_z,
        C_\ell\widetilde\eta_w\right\rangle,
\]
where $\{\widetilde\eta_z\}$ denotes a Gram-normalized evaluator window.

\section{Schatten/tail classification}
\begin{theorem}[Residual-kernel Schatten reduction]
Let
\[
        A_\ell=C_\ell\widetilde E.
\]
Then
\[
        \mathcal R_\ell=A_\ell^*A_\ell.
\]
Consequently:
\begin{enumerate}[label=(\roman*)]
\item $\mathcal R_\ell=0$ if and only if $A_\ell=0$.
\item $\mathcal R_\ell$ is compact if and only if $A_\ell$ is compact.
\item For $1\le p<\infty$,
\[
        \mathcal R_\ell\in\mathcal S_p
        \quad\Longleftrightarrow\quad
        A_\ell\in\mathcal S_{2p}.
\]
In that case, if $s_n(A_\ell)$ are the singular values of $A_\ell$, then
\[
        \|\mathcal R_\ell\|_{\mathcal S_p}^p
        =\sum_n s_n(A_\ell)^{2p}.
\]
\item In particular, $\mathcal R_\ell$ is trace-class if and only if $A_\ell$ is Hilbert--Schmidt.
\end{enumerate}
\end{theorem}

\begin{proof}
The identity $\mathcal R_\ell=A_\ell^*A_\ell$ is the definition of the normalized residual kernel.  The singular values of $A_\ell^*A_\ell$ are the squares of the singular values of $A_\ell$.  The compact and Schatten equivalences follow immediately from this singular-value relation.
\end{proof}

\begin{corollary}[Trace-class criterion]
Let $\{u_n\}$ be an orthonormal basis of the normalized pulled-evaluator domain.  Then
\[
        \mathcal R_\ell\in\mathcal S_1
        \quad\Longleftrightarrow\quad
        \sum_n\|C_\ell\widetilde E u_n\|^2<\infty.
\]
Moreover,
\[
        \operatorname{tr}\mathcal R_\ell
        =\sum_n\|C_\ell\widetilde E u_n\|^2.
\]
\end{corollary}

\section{Calkin-level obstruction}
Let $P_\eta$ be the orthogonal projection onto the closed span of the pulled evaluator family in the archimedean/Sonin carrier.  Then the residual is compact only if the commutator block is compact after restriction to this pulled-evaluator span.

\begin{theorem}[Essential residual criterion]
If
\[
        [C_\ell P_\eta]\ne 0
        \qquad\text{in the Calkin algebra }\mathcal B(H_\infty)/\mathcal K(H_\infty),
\]
then the residual kernel $\mathcal R_\ell$ is not compact on the completed pulled-evaluator sector.  Hence $\Xi^{\rm BC}$ is not tail-payable by compact exhaustion alone.
\end{theorem}

\begin{proof}
If $\mathcal R_\ell$ were compact, then $A_\ell=C_\ell\widetilde E$ would be compact by the Schatten reduction theorem.  On the closed pulled-evaluator span this is precisely compactness of $C_\ell P_\eta$ after quotienting null modes.  Thus a nonzero Calkin class blocks compactness.
\end{proof}

\begin{warning}[Raw shift does not remove the Calkin sector]
The multiplier $m_\ell$ is nonvanishing.  Thus the shift alone does not produce a $\zeta$-factor and does not force $C_\ell\eta_z=0$.  Any compactness or trace-class result must come from one of the following additional records:
\begin{enumerate}[label=(\alph*)]
\item the pulled zero-evaluator span avoids the essential sector of $C_\ell$;
\item the projected Sonine kernel provides a smoothing envelope strong enough to make $C_\ell\widetilde E$ compact or Schatten;
\item a separate tail/exhaustivity theorem shows the residual kernel has vanishing completed tail.
\end{enumerate}
None of these records is currently earned by the raw commutator formula.
\end{warning}

\section{Tail-payability criterion}
Let $\Pi_N$ be an upstream-declared increasing projection ladder on the pulled-evaluator domain, and let $A_\ell=C_\ell\widetilde E$.

\begin{theorem}[Compact tail criterion]
If $A_\ell$ is compact and $\Pi_N\uparrow I$ strongly, then
\[
        \|A_\ell(I-\Pi_N)\|\to0.
\]
Equivalently, the normalized residual tails satisfy
\[
        \|(I-\Pi_N)\mathcal R_\ell(I-\Pi_N)\|\to0.
\]
If $A_\ell$ is Hilbert--Schmidt, then the trace tails also vanish:
\[
        \operatorname{tr}\big((I-\Pi_N)\mathcal R_\ell(I-\Pi_N)\big)\to0.
\]
\end{theorem}

\begin{proof}
Compact operators send strongly convergent projection tails to norm-zero tails.  The trace statement follows from Hilbert--Schmidt tail convergence.
\end{proof}

\section{Classification status after Step 156}
The residual has four possible lawful statuses:
\[
\begin{array}{lll}
\mathsf E & \text{exact} & C_\ell\eta_z=0\text{ for all zero evaluators};\\
\mathsf K & \text{compact/tail-payable} & C_\ell P_\eta\in\mathcal K;\\
\mathsf S_p & \text{Schatten-payable} & C_\ell\widetilde E\in\mathcal S_{2p};\\
\mathsf N & \text{active nonclaim residual} & \text{none of the above has been earned.}
\end{array}
\]
The current status is $\mathsf N$ with exact criteria for promotion to $\mathsf E$, $\mathsf K$, or $\mathsf S_p$.

\section{Nonclaim boundary}
Step 156 does not prove RH, does not prove $H_R=0$, and does not prove compactness of $\Xi^{\rm BC}$.  It proves the exact operator-theoretic classification gate.  The active next object is the Calkin interaction
\[
        \boxed{[C_\ell P_\eta]}
\]
and its finite-window singular-value tails.

\section{Next step}
Step 157 should audit the Calkin-level pulled-evaluator avoidance condition:
\[
        [C_\ell]P_\eta\stackrel{?}{=}0.
\]
If this fails, $\Xi^{\rm BC}$ is not compact/tail-payable and must remain as a scoped adequacy residual unless a genuinely new signed or co-Poisson mechanism is introduced.

\end{document}
'''

summary = r'''# Step 156: \(\Xi^{\rm BC}\) residual-kernel Schatten/tail audit

## Main object

The active Burnol/co-Poisson adequacy residual is

\[
\Xi^{\rm BC}_{\ell,a}
=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]

Using the projected commutator from Step 154,

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad
m_\ell(s)=e^{-\ell(1/2-s)},
\]

and the pulled zero-evaluators

\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

the residual kernel is

\[
\mathcal R_\ell((w,k),(z,j))
=\langle C_\ell\eta^a_{w,k},C_\ell\eta^a_{z,j}\rangle.
\]

Burnol's framework is the reason this is the correct carrier object: for \(a<1\), the co-Poisson subspace is the orthogonal complement of the zero-evaluator span, so \(\Pi_{Y_a}\mathfrak B_{\ell,a}=0\) is exactly the desired boundary-to-co-Poisson inclusion. Burnol's co-Poisson/Müntz formulas also explain why a genuine \(\zeta\)-multiplier would annihilate zero evaluators, but the raw shift alone does not supply such a factor.

## Main theorem

Let \(E\) synthesize the pulled evaluator family and \(\widetilde E=EG^{-1/2}\) be the Gram-normalized synthesis map. Define

\[
A_\ell=C_\ell\widetilde E.
\]

Then

\[
\boxed{\mathcal R_\ell=A_\ell^*A_\ell.}
\]

Therefore:

\[
\mathcal R_\ell=0\iff A_\ell=0,
\]

\[
\mathcal R_\ell\text{ compact}\iff A_\ell\text{ compact},
\]

and, for \(1\le p<\infty\),

\[
\boxed{\mathcal R_\ell\in\mathcal S_p
\iff
A_\ell\in\mathcal S_{2p}.}
\]

So \(\mathcal R_\ell\) is trace-class exactly when \(C_\ell\widetilde E\) is Hilbert--Schmidt.

## Calkin obstruction

Let \(P_\eta\) project onto the closed pulled-evaluator span. If

\[
\boxed{[C_\ell P_\eta]\ne0}
\]

in the Calkin algebra, then \(\Xi^{\rm BC}\) is not compact/tail-payable by a compact exhaustion theorem.

This is the key Step 156 reduction:

\[
\boxed{
\text{compactness of }\Xi^{\rm BC}
\text{ requires pulled-evaluator avoidance of the essential shifted Sonin sector.}
}
\]

The semilocal CCM framework supplies the correct Hardy--Titchmarsh/Sonin ambient geometry, but it does not by itself prove this Calkin avoidance or the commutator annihilation.

## Tail-payability criterion

If

\[
A_\ell=C_\ell\widetilde E
\]

is compact and \(\Pi_N\uparrow I\), then

\[
\|A_\ell(I-\Pi_N)\|\to0.
\]

If \(A_\ell\) is Hilbert--Schmidt, then

\[
\operatorname{tr}\big((I-\Pi_N)\mathcal R_\ell(I-\Pi_N)\big)\to0.
\]

Thus compactness gives norm-tail payment; Hilbert--Schmidt gives trace-tail payment.

## Verdict

\[
\boxed{
\Xi^{\rm BC}\text{ is not yet exact, compact, or Schatten-certified.}
}
\]

The residual is now classified by exact operator criteria:

| status | condition | current state |
|---|---|---|
| exact | \(C_\ell\eta_z=0\) for every zero evaluator | not proved |
| compact/tail-payable | \(C_\ell P_\eta\in\mathcal K\) | not proved |
| Schatten-payable | \(C_\ell\widetilde E\in\mathcal S_{2p}\) | not proved |
| active nonclaim | no exact/compact/Schatten record | active |

## Bottom line

\[
\boxed{
\text{Step 156 turns }\Xi^{\rm BC}\text{ into a Calkin/Schatten/tail classification problem.}
}
\]

The next step is:

\[
\boxed{\textbf{Step 157: Calkin-level pulled-evaluator avoidance audit.}}
\]

Target:

\[
[C_\ell]P_\eta\stackrel{?}{=}0.
\]

If this fails, \(\Xi^{\rm BC}\) is a genuinely noncompact adequacy residual and must remain in the theorem statement unless a new signed, co-Poisson, or semilocal cancellation mechanism is introduced.
'''

nonclaim = r'''# Nonclaim boundary — Step 156

Step 156 does not prove RH.

It does not prove:

- \(H_R=0\),
- \(\Xi^{\rm BC}=0\),
- compactness of \(\Xi^{\rm BC}\),
- trace-classness of \(\Xi^{\rm BC}\),
- source absorption of \(\Xi^{\rm BC}\).

It proves a classification theorem:

\[
\mathcal R_\ell=A_\ell^*A_\ell,
\qquad
A_\ell=C_\ell\widetilde E.
\]

Thus:

\[
\mathcal R_\ell\in\mathcal S_p
\iff
A_\ell\in\mathcal S_{2p}.
\]

The active unresolved object is the Calkin class

\[
[C_\ell P_\eta].
\]

If this class is nonzero, the residual is not compact/tail-payable by ordinary compact exhaustion.
'''

(base/'xi_bc_schatten_tail_step156.tex').write_text(tex)
(base/'step156_results_summary.md').write_text(summary)
(base/'nonclaim_boundary_step156.md').write_text(nonclaim)

# CSV tables
classification = pd.DataFrame([
    {"status":"E_exact", "criterion":"C_l eta_z = 0 for all pulled zero-evaluators", "operator_form":"A_l=0; R_l=0", "current_state":"not earned", "next_record":"co-Poisson factorization or projected-kernel cancellation"},
    {"status":"K_compact_tail", "criterion":"C_l P_eta is compact", "operator_form":"[C_l P_eta]=0 in Calkin", "current_state":"not earned", "next_record":"Calkin avoidance theorem"},
    {"status":"S_p_schatten", "criterion":"C_l E_tilde in S_{2p}", "operator_form":"R_l in S_p", "current_state":"not earned", "next_record":"Schatten envelope for pulled evaluators"},
    {"status":"N_active_nonclaim", "criterion":"no exact/compact/Schatten record", "operator_form":"Xi_BC remains active", "current_state":"active", "next_record":"scope as adequacy residual"},
])
classification.to_csv(base/'xi_bc_schatten_classification_step156.csv', index=False)

gates = pd.DataFrame([
    {"gate":"G_exact", "test":"C_l eta_z = 0 for all z", "passes_now":"no", "failure_mode":"raw shift does not create zeta factor"},
    {"gate":"G_calkin", "test":"[C_l P_eta]=0 in B(H)/K(H)", "passes_now":"unknown", "failure_mode":"essential shifted Sonin sector may survive"},
    {"gate":"G_compact_tail", "test":"||A_l(I-Pi_N)|| -> 0", "passes_now":"unknown", "failure_mode":"requires compactness of A_l"},
    {"gate":"G_trace_tail", "test":"sum s_n(A_l)^2 < infinity", "passes_now":"unknown", "failure_mode":"requires Hilbert-Schmidt residual synthesis"},
    {"gate":"G_source_absorb", "test":"non-circular signed/direct budget", "passes_now":"no", "failure_mode":"positive source-budget route blocked in Step 150"},
    {"gate":"G_scope", "test":"Xi_BC explicitly retained as residual", "passes_now":"yes", "failure_mode":"none; current lawful status"},
])
gates.to_csv(base/'xi_bc_schatten_gate_table_step156.csv', index=False)

theorem_map = pd.DataFrame([
    {"item":"Residual kernel identity", "statement":"R_l=A_l^*A_l", "dependency":"definitions of C_l and normalized pulled evaluator synthesis", "output":"Schatten reduction"},
    {"item":"Schatten reduction", "statement":"R_l in S_p iff A_l in S_{2p}", "dependency":"singular values of A^*A", "output":"trace/compact criteria"},
    {"item":"Calkin obstruction", "statement":"[C_l P_eta] != 0 blocks compactness", "dependency":"compactness equivalence", "output":"essential residual gate"},
    {"item":"Tail criterion", "statement":"compact A_l implies norm tails vanish; HS A_l implies trace tails vanish", "dependency":"compact operator tail convergence", "output":"completed tail-payability record"},
])
theorem_map.to_csv(base/'theorem_map_step156.csv', index=False)

route_status = pd.DataFrame([
    {"route":"co-Poisson factorization", "status":"open", "comment":"would make Xi_BC exact by zeta-divisibility"},
    {"route":"projected-kernel commutator cancellation", "status":"open", "comment":"requires C_l eta_z=0 for all pulled zero evaluators"},
    {"route":"compact/tail payment", "status":"open", "comment":"requires [C_l P_eta]=0 and compact tail"},
    {"route":"positive source-frame absorption", "status":"blocked", "comment":"source budget is collapse-strength"},
    {"route":"scoped residual", "status":"active", "comment":"Xi_BC remains explicit adequacy residual"},
])
route_status.to_csv(base/'route_status_step156.csv', index=False)

construction_tasks = pd.DataFrame([
    {"task_id":"T156.1", "task":"Define P_eta on completed pulled-evaluator span", "deliverable":"Calkin-domain projection record", "risk":"Gram-normalization / non-Riesz evaluator family"},
    {"task_id":"T156.2", "task":"Audit [C_l P_eta] in Calkin algebra", "deliverable":"essential avoidance or nonzero essential residual", "risk":"requires actual Sonine projection, not Hardy shadow"},
    {"task_id":"T156.3", "task":"Estimate singular values of A_l=C_l E_tilde", "deliverable":"compact / Schatten / noncompact classification", "risk":"finite windows may overstate decay"},
    {"task_id":"T156.4", "task":"If compact, prove fixed/exhaustive tail promotion", "deliverable":"norm-tail or trace-tail theorem", "risk":"moving-window support only"},
    {"task_id":"T156.5", "task":"If noncompact, update theorem scope", "deliverable":"Xi_BC active nonclaim record", "risk":"RH route cannot claim full adequacy"},
])
construction_tasks.to_csv(base/'construction_tasks_step156.csv', index=False)

# numerical toy data and plots
n = np.arange(1, 301)
profiles = pd.DataFrame({
    'n': n,
    'compact_fast_singular': np.exp(-n/35),
    'hilbert_schmidt_singular': n**(-0.9),
    'compact_not_hs_singular': n**(-0.35),
    'noncompact_floor_singular': 0.18 + 0.65*np.exp(-n/45),
})
profiles.to_csv(base/'xi_bc_singular_value_profiles_step156.csv', index=False)

plt.figure(figsize=(8,5))
for col in profiles.columns[1:]:
    plt.plot(n, profiles[col], label=col.replace('_',' '))
plt.yscale('log')
plt.xlabel('singular value index n')
plt.ylabel('singular value proxy')
plt.title('Step 156 residual singular-value classification profiles')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(base/'xi_bc_singular_value_profiles_step156.png', dpi=180)
plt.close()

# tail norms for scenarios
# operator norm tail is s_{N+1}; trace tail is sum s_n^2 tail
Ns = np.arange(10, 301, 10)
def trace_tail(arr, N):
    return np.sum(arr[N:]**2)

tail = []
for N in Ns:
    row={'N':int(N)}
    for col in profiles.columns[1:]:
        arr = profiles[col].values
        row[f'{col}_op_tail'] = arr[N] if N < len(arr) else 0.0
        row[f'{col}_trace_tail'] = trace_tail(arr, N)
    tail.append(row)
tail_df=pd.DataFrame(tail)
tail_df.to_csv(base/'xi_bc_tail_payability_step156.csv', index=False)

plt.figure(figsize=(8,5))
for col in ['compact_fast_singular','hilbert_schmidt_singular','compact_not_hs_singular','noncompact_floor_singular']:
    plt.plot(tail_df['N'], tail_df[f'{col}_op_tail'], label=col.replace('_',' ')+' op tail')
plt.yscale('log')
plt.xlabel('window N')
plt.ylabel('operator tail proxy')
plt.title('Step 156 norm-tail payability proxy')
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(base/'xi_bc_tail_payability_step156.png', dpi=180)
plt.close()

# Calkin obstruction plot: essential floor vs compact part
x = np.linspace(0,1,101)
calkin_df = pd.DataFrame({
    'essential_overlap': x,
    'compact_status_score': 1-x,
    'tail_payable_score': np.maximum(0,1-x)**2,
    'active_residual_score': x**0.5,
})
calkin_df.to_csv(base/'calkin_obstruction_scenarios_step156.csv', index=False)
plt.figure(figsize=(7,5))
plt.plot(x, calkin_df['tail_payable_score'], label='tail-payable score')
plt.plot(x, calkin_df['active_residual_score'], label='active residual score')
plt.xlabel('essential overlap proxy ||[C_l]P_eta||')
plt.ylabel('classification proxy')
plt.title('Step 156 Calkin obstruction classification')
plt.legend()
plt.tight_layout()
plt.savefig(base/'calkin_obstruction_classification_step156.png', dpi=180)
plt.close()

# Toy finite residual kernel eigenvalues
rng = np.random.default_rng(156)
dims = [20,40,80,120]
records=[]
for d in dims:
    # compact-like singular values and noncompact-like
    s_comp = np.exp(-np.arange(d)/20)
    s_floor = 0.2 + 0.8*np.exp(-np.arange(d)/20)
    records.append({'dimension':d, 'scenario':'compact_like', 'min_eigen':float(np.min(s_comp**2)), 'trace':float(np.sum(s_comp**2)), 'top_eigen':float(np.max(s_comp**2))})
    records.append({'dimension':d, 'scenario':'floor_noncompact_like', 'min_eigen':float(np.min(s_floor**2)), 'trace':float(np.sum(s_floor**2)), 'top_eigen':float(np.max(s_floor**2))})
eig_df=pd.DataFrame(records)
eig_df.to_csv(base/'xi_bc_kernel_spectrum_step156.csv', index=False)

plt.figure(figsize=(7,5))
for scen in eig_df['scenario'].unique():
    sub=eig_df[eig_df['scenario']==scen]
    plt.plot(sub['dimension'], sub['min_eigen'], marker='o', label=scen.replace('_',' '))
plt.yscale('log')
plt.xlabel('finite window dimension')
plt.ylabel('minimum residual-kernel eigenvalue proxy')
plt.title('Step 156 finite residual-kernel spectrum proxy')
plt.legend()
plt.tight_layout()
plt.savefig(base/'xi_bc_kernel_spectrum_step156.png', dpi=180)
plt.close()

# classification status bar
status_df = pd.DataFrame({
    'status':['exact','compact','Schatten','source_absorbed','scoped_residual'],
    'score':[0.05,0.15,0.15,0.0,1.0],
})
status_df.to_csv(base/'xi_bc_classification_status_step156.csv', index=False)
plt.figure(figsize=(8,4))
plt.bar(status_df['status'], status_df['score'])
plt.ylabel('current support score')
plt.title('Step 156 current residual classification status')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig(base/'xi_bc_classification_status_step156.png', dpi=180)
plt.close()

schema = {
    "step": 156,
    "title": "Xi^BC residual-kernel Schatten/tail audit",
    "main_residual": "Xi_BC_{ell,a}=B_{ell,a}^* Pi_{Y_a} B_{ell,a}",
    "commutator_block": "C_ell=(I-P_infty) M_{m_ell} P_infty",
    "normalized_kernel": "R_ell=E_tilde^* C_ell^* C_ell E_tilde",
    "main_reduction": "R_ell in S_p iff C_ell E_tilde in S_{2p}",
    "calkin_gate": "[C_ell P_eta]=0 required for compact/tail route",
    "current_status": "active nonclaim residual; compact/Schatten not earned",
    "next_step": 157,
    "next_target": "Calkin-level pulled-evaluator avoidance audit"
}
(base/'step156_schema.json').write_text(json.dumps(schema, indent=2))

check_script = r'''#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

base = Path(__file__).resolve().parent
required = [
    'xi_bc_schatten_tail_step156.tex',
    'step156_results_summary.md',
    'xi_bc_schatten_classification_step156.csv',
    'xi_bc_schatten_gate_table_step156.csv',
    'theorem_map_step156.csv',
    'route_status_step156.csv',
    'nonclaim_boundary_step156.md',
    'step156_schema.json'
]
missing = [f for f in required if not (base/f).exists()]
checks = {'missing_required': missing}
tex = (base/'xi_bc_schatten_tail_step156.tex').read_text()
checks['has_main_identity'] = 'mathcal R_\\ell=A_\\ell^*A_\\ell' in tex
checks['has_calkin_gate'] = '[C_\\ell P_\\eta]' in tex
checks['classification_rows'] = len(pd.read_csv(base/'xi_bc_schatten_classification_step156.csv'))
checks['gate_rows'] = len(pd.read_csv(base/'xi_bc_schatten_gate_table_step156.csv'))
checks['passed'] = not missing and checks['has_main_identity'] and checks['has_calkin_gate']
print(json.dumps(checks, indent=2))
'''
(base/'run_step156_xi_bc_schatten_tail.py').write_text(check_script)
(base/'run_step156_xi_bc_schatten_tail.py').chmod(0o755)

# run check, save results
import subprocess, sys
res = subprocess.run([sys.executable, str(base/'run_step156_xi_bc_schatten_tail.py')], capture_output=True, text=True)
(base/'step156_check_results.json').write_text(res.stdout)

# zip artifacts
zip_path = base/'step156_xi_bc_schatten_tail_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for path in base.iterdir():
        if path == zip_path:
            continue
        zf.write(path, path.name)

print(f'created {base}')
print(res.stdout)
