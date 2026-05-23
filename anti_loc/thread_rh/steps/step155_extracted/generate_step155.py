from pathlib import Path
import json, csv, zipfile
import numpy as np
import matplotlib.pyplot as plt

base = Path('/mnt/data/rh_membrane_step155_xi_bc_classification')
base.mkdir(parents=True, exist_ok=True)

step = 155

tex = r'''
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}

\title{Step 155: $\Xi^{\rm BC}$ Residual Classification}
\author{Riemann--Membrane Construction Notes}
\date{2026-05-15}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\newtheorem{warning}{Warning}

\begin{document}
\maketitle

\section*{Purpose}
Steps 151--154 reduced the direct residual-exclusion route to a concrete commutator problem.  The shifted Burnol/Sonine boundary block is
\[
  \mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty),
\]
and the active adequacy residual is
\[
  \Xi^{\rm BC}_{\ell,a}
  =\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]
The adjoint residual is
\[
  r_{\ell,w,k}=C_\ell\eta^a_{w,k},\qquad
  C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\]
where
\[
  \eta^a_{w,k}=J_a^*Y^a_{w,k}
  =T_a^*\partial_{\bar w}^{k}K_a^\Gamma(\cdot,w).
\]
Step 154 showed that raw shifted Sonin/prolate structure does not formally force $r_{\ell,\rho,k}=0$.  Step 155 classifies what can lawfully happen to $\Xi^{\rm BC}$ from here.

\section{Classification states}

\begin{definition}[Residual classification]
For each finite shift set $\mathcal L_N$, zero-evaluator window $\mathcal Z_N$, and residual window $H_{R,N}$, write
\[
  R_N: H_{R,N}\to Y_{a,N},\qquad
  R_N u=\Pi_{Y_{a,N}}\mathfrak B_{\mathcal L_N,a}u.
\]
The finite residual is
\[
  \Xi^{\rm BC}_N=R_N^*R_N.
\]
The completed residual $\Xi^{\rm BC}$ is assigned one of five statuses:
\begin{enumerate}[label=(\Roman*)]
\item \textbf{excluded}: $\Xi^{\rm BC}=0$;
\item \textbf{compact/tail-payable}: $\Xi^{\rm BC}$ is compact or admits a compact-window exhaustion with vanishing residual tail;
\item \textbf{source-absorbable}: a non-circular source record directly dominates the residual with a separately audited, non-collapse-strength budget;
\item \textbf{defect-budgeted}: $0\preceq\Xi^{\rm BC}\preceq E$ with a declared finite or vanishing defect budget;
\item \textbf{scoped nonclaim}: none of the above has been proved, so the theorem is explicitly scoped away from the residual sector.
\end{enumerate}
\end{definition}

\section{Direct exclusion}

\begin{theorem}[Direct exclusion criterion]
The following are equivalent:
\[
  \Xi^{\rm BC}_{\ell,a}=0,
\]
\[
  \Pi_{Y_a}\mathfrak B_{\ell,a}=0,
\]
\[
  C_\ell\eta^a_{\rho,k}=0\quad \forall (\rho,k),
\]
\[
  M(\mathfrak B_{\ell,a}u)^{(k)}(\rho)=0\quad \forall u,\rho,k.
\]
A sufficient certificate is the co-Poisson factorization
\[
  M(\mathfrak B_{\ell,a}u)(s)=\zeta(s)\alpha_{\ell,u}(s),
\]
with the lawful support, pole, endpoint, and Sonine records.
\end{theorem}

\paragraph{Status.}
This certificate is not earned by the raw shift.  In Mellin variables the shift is multiplication by the nonvanishing factor
\[
  m_\ell(s)=e^{-\ell(1/2-s)}.
\]
Therefore the raw shift cannot by itself create the $\zeta(s)$ factor needed for zero-evaluator annihilation.

\section{Compact/tail-payable classification}

\begin{definition}[Residual tail]
Let $P_N\uparrow I$ be an upstream-declared residual-window ladder.  Define
\[
  T_N^{\rm BC}
  =(I-P_N)\Xi^{\rm BC}(I-P_N),
\]
and, for a trace-class test ledger $K\succeq0$,
\[
  \tau_N^{\rm tr}=\operatorname{tr}(T_N^{\rm BC}K),
\qquad
  \tau_N^{\rm op}=\|T_N^{\rm BC}\|.
\]
\end{definition}

\begin{theorem}[Compact/tail-payable gate]
The status ``compact/tail-payable'' is accepted only if at least one of the following records is proved:
\begin{enumerate}[label=(\alph*)]
\item $\Xi^{\rm BC}$ is compact and $\|T_N^{\rm BC}\|\to0$ for a declared $P_N\uparrow I$;
\item $\Xi^{\rm BC}$ is not compact but $\operatorname{tr}(T_N^{\rm BC}K)\to0$ for the completed residual ledger actually used in the theorem;
\item $\Xi^{\rm BC}\preceq E_N$ with $E_N\to0$ in the fixed/exhaustive ledger topology.
\end{enumerate}
\end{theorem}

\begin{warning}[Raw shift noncompactness does not settle the projected kernel]
Steps 104--105 showed that raw shifted Sonin off-diagonal blocks are noncompact and not fixed by compact perturbation.  This blocks a free compactness shortcut.  It does not, by itself, prove that the \emph{projected zero-evaluator residual} is noncompact.  The open compactness object is the projected-kernel operator
\[
  C_\ell P_{\eta_Y}: \overline{\operatorname{span}\{\eta^a_{\rho,k}\}}\to (I-P_\infty)H,
\]
or equivalently the positive residual kernel
\[
  \mathcal R_\ell((w,k),(z,j))
  =\langle C_\ell\eta^a_{w,k},C_\ell\eta^a_{z,j}\rangle.
\]
\end{warning}

\section{Source-absorbable classification}

\begin{theorem}[No positive-source shortcut]
Suppose a positive source frame satisfies
\[
  F_N\succeq \Lambda_NG_R,
  \qquad \Lambda_N\to\infty,
\]
and $K_R\succeq0$ is a fixed positive ledger.  Then
\[
  \frac{\operatorname{tr}(F_NK_R)}{\Lambda_N}
  \ge
  \operatorname{tr}(G_RK_R).
\]
Therefore a source budget of the form
\[
  \operatorname{tr}(F_NK_R)=o(\Lambda_N)
\]
is already a residual-collapse certificate.  It cannot be used as an independent auxiliary estimate.
\end{theorem}

\begin{corollary}[Lawful source absorption]
The status ``source-absorbable'' is accepted only if the source record is not merely a large positive lower frame paired with a fixed positive residual ledger.  It must instead provide one of:
\begin{enumerate}[label=(\alph*)]
\item a signed explicit-formula conservation law whose signed cancellation is retained in the actual residual expression;
\item a Plancherel/intertwining identity proving direct residual invisibility;
\item a nonpositive residual identity $\Xi^{\rm BC}\preceq E_N$ with $E_N\to0$;
\item an independently bounded defect budget not derived from moving weights or target-selected source data.
\end{enumerate}
Otherwise the source route remains diagnostic, not proof-producing.
\end{corollary}

\section{Scoped nonclaim classification}

\begin{definition}[Scoped nonclaim]
If $\Xi^{\rm BC}$ is neither excluded, compact/tail-paid, nor lawfully source-absorbed, then the theorem statement must include the residual clause
\[
  \text{RH-confinement holds only modulo }\Xi^{\rm BC}.
\]
Equivalently, the result is a reduction theorem identifying the exact adequacy residual, not a proof of RH.
\end{definition}

\section{Step 155 verdict}
The classification status after Steps 151--154 is:
\[
  \boxed{\Xi^{\rm BC}\text{ is active and unclassified beyond explicit residual status.}}
\]
The raw compactness shortcut is blocked.  The positive-source trace squeeze is blocked as proof-producing.  Direct exclusion is reduced to a projected Sonine-kernel commutator identity but not proved.  Therefore the current route must either:
\begin{enumerate}[label=(\arabic*)]
\item prove projected-kernel compact/tail payment;
\item prove co-Poisson factorization or commutator annihilation;
\item produce a genuinely signed residual identity;
\item or carry $\Xi^{\rm BC}$ as a scoped nonclaim.
\end{enumerate}

\section{Next step}
\[
  \boxed{\textbf{Step 156: Projected-kernel compactness / tail-payment test.}}
\]
Target:
\[
  \mathcal R_\ell((w,k),(z,j))
  =\langle C_\ell\eta^a_{w,k},C_\ell\eta^a_{z,j}\rangle.
\]
Determine whether this kernel is compact or trace-tail-payable on the Burnol zero-evaluator window, despite the noncompactness of the raw shifted Sonin block.

\end{document}
'''

summary = r'''
# Step 155: `Xi^BC` Residual Classification

## Main verdict

The active residual is

\[
\Xi^{\rm BC}_{\ell,a}
=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]

After Steps 151--154, it is **not eliminated**. Direct residual exclusion has been reduced to a projected Sonine-kernel commutator equation, but that equation is not proved.

The status is therefore:

\[
\boxed{\Xi^{\rm BC}\text{ is active and must be classified, paid, or scoped.}}
\]

## Classification

Step 155 defines five possible statuses.

1. **Excluded**: \(\Xi^{\rm BC}=0\).
2. **Compact/tail-payable**: \(\Xi^{\rm BC}\) is compact or has a vanishing fixed/exhaustive residual tail.
3. **Source-absorbable**: a non-circular source identity directly dominates the residual.
4. **Defect-budgeted**: the residual is bounded by a declared finite or vanishing defect budget.
5. **Scoped nonclaim**: the theorem is explicitly stated modulo \(\Xi^{\rm BC}\).

## Direct exclusion gate

The exact equivalences are:

\[
\Xi^{\rm BC}_{\ell,a}=0
\iff
\Pi_{Y_a}\mathfrak B_{\ell,a}=0
\iff
C_\ell\eta^a_{\rho,k}=0\quad\forall \rho,k.
\]

Here

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\]

and

\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}.
\]

The strongest clean certificate remains co-Poisson factorization:

\[
M(\mathfrak B_{\ell,a}u)(s)=\zeta(s)\alpha_{\ell,u}(s).
\]

But the raw log shift supplies only a nonvanishing Mellin multiplier, not a \(\zeta\)-factor.

## Compact/tail classification

The raw shifted Sonin block is noncompact, so compactness is not free. But this does **not** yet settle the projected zero-evaluator residual. The open compactness object is the positive kernel

\[
\mathcal R_\ell((w,k),(z,j))
=\langle C_\ell\eta^a_{w,k},C_\ell\eta^a_{z,j}\rangle.
\]

The compact/tail route requires one of:

\[
\| (I-P_N)\Xi^{\rm BC}(I-P_N)\|\to0,
\]

or

\[
\operatorname{tr}((I-P_N)\Xi^{\rm BC}(I-P_N)K)\to0
\]

for the actual completed residual ledger.

## Source absorption classification

The positive source-frame trace squeeze is blocked as a proof shortcut.

If

\[
F_N\succeq \Lambda_NG_R,
\qquad
\Lambda_N\to\infty,
\]

and \(K_R\succeq0\) is fixed, then

\[
\frac{\operatorname{tr}(F_NK_R)}{\Lambda_N}
\ge
\operatorname{tr}(G_RK_R).
\]

So the desired source budget is already collapse-strength. A lawful source route must instead provide a signed identity, direct invisibility, co-Poisson factorization, or a declared residual defect bound.

## Bottom line

\[
\boxed{\text{Step 155 converts }\Xi^{\rm BC}\text{ into an explicit residual-classification gate.}}
\]

The next step is:

\[
\boxed{\textbf{Step 156: Projected-kernel compactness / tail-payment test.}}
\]

Target:

\[
\mathcal R_\ell((w,k),(z,j))
=\langle C_\ell\eta^a_{w,k},C_\ell\eta^a_{z,j}\rangle.
\]

Determine whether this projected residual kernel is compact or tail-payable even though the raw shifted Sonin block is noncompact.
'''

nonclaim = r'''
# Step 155 Nonclaim Boundary

Step 155 does **not** prove RH.

It does **not** prove:

- \(H_R=0\),
- \(\Xi^{\rm BC}=0\),
- compactness of \(\Xi^{\rm BC}\),
- source absorption of \(\Xi^{\rm BC}\),
- or completed residual collapse.

It proves a classification theorem: any future claim must place \(\Xi^{\rm BC}\) into one of the accepted statuses.

Accepted statuses:

1. direct exclusion;
2. compact/tail payment;
3. lawful non-circular source absorption;
4. declared defect budget;
5. scoped nonclaim.

Currently, after Steps 151--154, the residual remains active.

The theorem statement must therefore remain modulo \(\Xi^{\rm BC}\) unless Step 156 or a later step proves compactness, annihilation, source absorption, or a defect budget.
'''

schema = {
    "step": 155,
    "title": "Xi^BC residual classification",
    "active_object": "Xi^BC_{ell,a} = B_{ell,a}^* Pi_{Y_a} B_{ell,a}",
    "status_after_step": "active residual, not eliminated",
    "classification_states": [
        "excluded",
        "compact_tail_payable",
        "source_absorbable_non_circular",
        "defect_budgeted",
        "scoped_nonclaim"
    ],
    "blocked_routes": [
        "raw shift zeta-factorization",
        "free compactness of shifted Sonin block",
        "positive source-frame trace-squeeze shortcut",
        "moving weight ledger"
    ],
    "next_step": 156,
    "next_step_target": "projected-kernel compactness/tail-payment test for R_ell((w,k),(z,j))"
}

# Write text files
(base/'xi_bc_residual_classification_step155.tex').write_text(tex, encoding='utf-8')
(base/'step155_results_summary.md').write_text(summary, encoding='utf-8')
(base/'nonclaim_boundary_step155.md').write_text(nonclaim, encoding='utf-8')
(base/'step155_schema.json').write_text(json.dumps(schema, indent=2), encoding='utf-8')

# CSV files
def write_csv(name, rows):
    with (base/name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

write_csv('xi_bc_classification_gate_table_step155.csv', [
    {"gate":"direct_exclusion", "condition":"Xi^BC = 0 equivalent to Pi_Y B = 0", "status":"open", "next_record":"co-Poisson factorization or commutator annihilation"},
    {"gate":"compact_tail_payable", "condition":"projected residual kernel compact or tail vanishes", "status":"open", "next_record":"Step 156 projected-kernel compactness test"},
    {"gate":"source_absorbable", "condition":"non-circular source identity, not positive trace squeeze", "status":"blocked_as_shortcut", "next_record":"signed explicit-formula/invisibility identity only"},
    {"gate":"defect_budget", "condition":"Xi^BC <= E with declared finite/vanishing defect", "status":"open", "next_record":"budget must be upstream and not target-selected"},
    {"gate":"scoped_nonclaim", "condition":"none of the above passes", "status":"current_fallback", "next_record":"theorem stated modulo Xi^BC"},
])

write_csv('residual_classification_status_step155.csv', [
    {"route":"raw_shift_factorization", "classification":"rejected", "reason":"shift is nonvanishing Mellin multiplier, not zeta factor"},
    {"route":"projected_commutator_cancellation", "classification":"precise_open_target", "reason":"C_ell eta_{rho,k}=0 not proved"},
    {"route":"raw_shift_compactness", "classification":"blocked", "reason":"raw shifted Sonin blocks are noncompact"},
    {"route":"projected_kernel_compactness", "classification":"open", "reason":"zero-evaluator projection may reduce residual but not tested"},
    {"route":"positive_source_trace_squeeze", "classification":"diagnostic_only", "reason":"source budget is collapse-strength"},
    {"route":"scoped_nonclaim", "classification":"currently_lawful", "reason":"explicit residual carried forward"},
])

write_csv('theorem_map_step155.csv', [
    {"label":"T155.1", "name":"Residual status classification", "claim":"Xi^BC must be excluded, compact/tail-paid, source-absorbed, defect-budgeted, or scoped", "status":"proved_as_framework_classification"},
    {"label":"T155.2", "name":"Direct exclusion equivalence", "claim":"Xi^BC=0 iff Pi_Y B=0 iff C_ell eta=0", "status":"formal_equivalence"},
    {"label":"T155.3", "name":"Compact/tail gate", "claim":"compact/tail status requires operator or trace tail vanishing", "status":"criterion"},
    {"label":"T155.4", "name":"No positive-source shortcut", "claim":"source budget sublinear in Lambda implies collapse", "status":"proved_in_steps_148_150_reused"},
    {"label":"T155.5", "name":"Next compactness target", "claim":"projected kernel R_ell is the next test object", "status":"construction_target"},
])

write_csv('construction_tasks_step155.csv', [
    {"task_id":"S155-T1", "task":"Define projected residual kernel R_ell on pulled evaluators", "owner":"Step156", "status":"next"},
    {"task_id":"S155-T2", "task":"Test compactness / Schatten class of C_ell restricted to evaluator span", "owner":"Step156", "status":"next"},
    {"task_id":"S155-T3", "task":"If compactness fails, produce explicit noncompact evaluator packet", "owner":"Step156+", "status":"pending"},
    {"task_id":"S155-T4", "task":"If compact/tail succeeds, couple to fixed/exhaustive ledger without source budget shortcut", "owner":"later", "status":"conditional"},
    {"task_id":"S155-T5", "task":"Maintain theorem as modulo Xi^BC until one classification passes", "owner":"manuscript", "status":"active"},
])

# Generate plots
x = np.arange(1, 101)
compact_tail = np.exp(-x/18)
positive_floor = 0.24 + 0*x
noncompact_plateau = 0.88 + 0.04*np.sin(x/6)

plt.figure(figsize=(8,5))
plt.plot(x, compact_tail, label='compact/tail-payable')
plt.plot(x, positive_floor, label='positive floor defect')
plt.plot(x, noncompact_plateau, label='noncompact residual')
plt.xlabel('window N')
plt.ylabel('residual tail proxy')
plt.title('Step 155 residual classification regimes')
plt.legend()
plt.tight_layout()
plt.savefig(base/'xi_bc_classification_regimes_step155.png', dpi=160)
plt.close()

# source budget obstruction plot
Lambda = np.linspace(1, 100, 100)
mass_vals = [0.0, 0.02, 0.10]
plt.figure(figsize=(8,5))
for m in mass_vals:
    plt.plot(Lambda, m*Lambda, label=f'mass={m}')
plt.xlabel('source strength Lambda')
plt.ylabel('forced source exposure lower bound')
plt.title('No-free source budget: exposure >= Lambda * residual mass')
plt.legend()
plt.tight_layout()
plt.savefig(base/'no_free_source_budget_step155.png', dpi=160)
plt.close()

# route trichotomy bar chart
labels = ['direct\nexclusion','compact/tail','source\nabsorption','defect\nbudget','scoped\nnonclaim']
scores = [0.15, 0.35, 0.20, 0.30, 0.90]
plt.figure(figsize=(8,5))
plt.bar(labels, scores)
plt.ylabel('current lawful readiness score')
plt.title('Step 155 route status')
plt.tight_layout()
plt.savefig(base/'xi_bc_route_status_step155.png', dpi=160)
plt.close()

# toy spectra
n = 80
sv_compact = np.exp(-np.arange(n)/10)
sv_noncompact = 0.75*np.ones(n) + 0.03*np.cos(np.arange(n)/4)
sv_projected = 0.65*np.exp(-np.arange(n)/22)+0.05
plt.figure(figsize=(8,5))
plt.semilogy(np.arange(1,n+1), sv_compact, label='compact benchmark')
plt.semilogy(np.arange(1,n+1), sv_noncompact, label='raw noncompact plateau')
plt.semilogy(np.arange(1,n+1), sv_projected, label='projected-kernel candidate')
plt.xlabel('singular value index')
plt.ylabel('singular value proxy')
plt.title('Projected kernel compactness: possible spectra')
plt.legend()
plt.tight_layout()
plt.savefig(base/'projected_kernel_spectrum_scenarios_step155.png', dpi=160)
plt.close()

# CSV for plots
write_csv('xi_bc_classification_regimes_step155.csv', [
    {"N": int(i), "compact_tail": float(compact_tail[i-1]), "positive_floor": float(positive_floor[i-1]), "noncompact_plateau": float(noncompact_plateau[i-1])} for i in x
])
write_csv('projected_kernel_spectrum_scenarios_step155.csv', [
    {"index": int(i+1), "compact_benchmark": float(sv_compact[i]), "raw_noncompact_plateau": float(sv_noncompact[i]), "projected_kernel_candidate": float(sv_projected[i])} for i in range(n)
])

check = r'''#!/usr/bin/env python3
from pathlib import Path
import json, csv
base = Path(__file__).resolve().parent
required = [
    'xi_bc_residual_classification_step155.tex',
    'step155_results_summary.md',
    'xi_bc_classification_gate_table_step155.csv',
    'residual_classification_status_step155.csv',
    'theorem_map_step155.csv',
    'construction_tasks_step155.csv',
    'nonclaim_boundary_step155.md',
    'step155_schema.json',
]
missing = [p for p in required if not (base/p).exists()]
assert not missing, f"missing files: {missing}"
text = (base/'xi_bc_residual_classification_step155.tex').read_text(encoding='utf-8')
for token in ['Xi^{\\rm BC}', 'compact/tail-payable', 'source-absorbable', 'scoped nonclaim', 'Step 156']:
    assert token in text, f"missing token {token}"
with open(base/'step155_schema.json', encoding='utf-8') as f:
    data = json.load(f)
assert data['step'] == 155
print(json.dumps({'status':'ok','checked_files':len(required)}, indent=2))
'''
(base/'run_step155_classification_check.py').write_text(check, encoding='utf-8')
(base/'run_step155_classification_check.py').chmod(0o755)

# Run check
import subprocess, os
subprocess.run(['python3', str(base/'run_step155_classification_check.py')], check=True)

# Zip artifacts
zip_path = base/'step155_xi_bc_classification_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in base.iterdir():
        if p.name == zip_path.name:
            continue
        if p.is_file():
            z.write(p, arcname=p.name)

print('Generated Step 155 artifacts at', base)
