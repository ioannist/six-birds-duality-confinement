from pathlib import Path
import json, csv, math, zipfile
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step155_xi_bc_classification')
out.mkdir(parents=True, exist_ok=True)

step = 155

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{hyperref}
\geometry{margin=1in}

\title{Step 155: $\Xi^{\mathrm{BC}}$ Residual Classification}
\author{RH Membrane Construction Notes}
\date{}

\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}

\begin{document}
\maketitle

\section{Purpose}
Steps 151--154 reduced the direct residual-exclusion route to the projected Sonine-kernel commutator
\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad m_\ell(s)=e^{-\ell(1/2-s)},
\]
acting on pulled Burnol zero-evaluator kernels
\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}.
\]
The direct exclusion target is
\[
C_\ell\eta^a_{\rho,k}=0\quad \forall \ell,\rho,k.
\]
Step 154 did not earn this vanishing.  The active residual is therefore
\[
\Xi^{\mathrm{BC}}_{\ell,a}
=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}
\succeq 0,
\qquad
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]
This note classifies what can lawfully be done with this residual.

\section{Kernel form of the residual}
Let
\[
z=(\rho,k),\qquad \eta_z=\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}.
\]
The pulled-evaluator residual kernel is
\[
\mathcal R_\ell(z,z')
=
\langle C_\ell\eta_z,C_\ell\eta_{z'}\rangle.
\]
Thus, for any finite coefficient vector $c=(c_z)$,
\[
\sum_{z,z'}\overline{c_z}c_{z'}\mathcal R_\ell(z,z')
=\left\|C_\ell\sum_z c_z\eta_z\right\|^2\ge0.
\]
So $\Xi^{\mathrm{BC}}$ is a positive adequacy residual, not a signed error.

\begin{definition}[Classification gates]
A residual $\Xi^{\mathrm{BC}}$ is classified by four possible lawful records:
\begin{enumerate}
\item \textbf{Zero/direct-exclusion record:} $C_\ell\eta_z=0$ for every visible zero-evaluator index $z$.
\item \textbf{Compact/tail record:} $\Xi^{\mathrm{BC}}$ is compact or trace-class relative to a fixed/exhaustive residual ledger and its tail is paid.
\item \textbf{Non-circular source-absorption record:} a declared source family charges $\Xi^{\mathrm{BC}}$ with a lower frame and a source audit that is independent of the same positive ledger pairing.
\item \textbf{Scoped nonclaim record:} the theorem statement carries $\Xi^{\mathrm{BC}}$ as an explicit adequacy residual and does not claim off-critical-zero exclusion through it.
\end{enumerate}
\end{definition}

\section{Direct zero record}
\begin{proposition}[Direct zero criterion]
For fixed $\ell,a$,
\[
\Xi^{\mathrm{BC}}_{\ell,a}=0
\iff
\Pi_{Y_a}\mathfrak B_{\ell,a}=0
\iff
C_\ell\eta^a_{\rho,k}=0\quad \forall \rho,k.
\]
\end{proposition}

\noindent The strongest sufficient certificate remains a co-Poisson/Mellin factorization
\[
M(\mathfrak B_{\ell,a}u)(s)=\zeta(s)\alpha_{\ell,u}(s).
\]
A raw log-shift does not create this factorization; it only multiplies Mellin transforms by a nonvanishing factor.  Therefore the zero record is not earned by shift structure alone.

\section{Compact/tail-payable record}
A compact/tail-payable classification requires one of the following fixed/exhaustive records:
\[
\Xi^{\mathrm{BC}}\in \mathcal K(H_R),
\qquad
P_N\uparrow I,
\qquad
\|(I-P_N)\Xi^{\mathrm{BC}}(I-P_N)\|\to0,
\]
or, for a trace ledger $K_R$,
\[
\operatorname{tr}((I-P_N)\Xi^{\mathrm{BC}}K_R\Xi^{\mathrm{BC}}(I-P_N))\to0.
\]
Raw shifted Sonin blocks are noncompact; compact perturbations of the projection do not remove the essential off-diagonal sector.  Hence compactness is possible only after a genuine evaluator-specific projection cancellation or a new semilocal prolate identity.

\section{Source-absorption record}
A positive lower frame
\[
F_N\succeq \Lambda_N G_R,
\qquad \Lambda_N\to\infty,
\]
combined with a fixed positive ledger $K_R\ge0$ gives
\[
\operatorname{tr}(F_NK_R)\ge \Lambda_N\operatorname{tr}(G_RK_R).
\]
Therefore a source audit budget
\[
\operatorname{tr}(F_NK_R)=o(\Lambda_N)
\]
is already a residual-collapse certificate.  It cannot be treated as an auxiliary estimate.

\begin{theorem}[No-free positive source absorption]
Let $F_N\succeq \Lambda_N G_R$ with $\Lambda_N\to\infty$ and let $K_R\ge0$ be a fixed positive trace-class ledger.  If
\[
\frac{\operatorname{tr}(F_NK_R)}{\Lambda_N}\to0,
\]
then
\[
\operatorname{tr}(G_RK_R)=0.
\]
Thus any non-circular source-absorption theorem must either use a signed conservation identity, a direct residual invisibility theorem, or a source audit independent of the positive trace squeeze.
\end{theorem}

\section{Scoped nonclaim record}
If none of the preceding records is earned, the correct theorem statement is conditional:
\[
\mathrm{RH\text{-}membrane\ conclusion}
\quad\text{holds only modulo}\quad
\Xi^{\mathrm{BC}}.
\]
Equivalently, the framework proves a residual-classified statement:
\[
\Xi^{\mathrm{BC}}=0
\quad\text{or}\quad
\Xi^{\mathrm{BC}}\preceq E_{\mathrm{budget}}
\quad\Rightarrow\quad
\text{residual off-critical mass collapses.}
\]
Without such a record, the result is a scoped nonclaim against the dissolving probe family.

\section{Step 155 verdict}
The current classification is:
\[
\boxed{\Xi^{\mathrm{BC}}\text{ is active and not yet compact-paid, source-absorbed, or zero.}}
\]
The positive source-frame route remains diagnostically useful because it identifies the residual and its possible blind sectors, but it does not by itself prove residual collapse.  The proof-producing routes are now:
\begin{enumerate}
\item prove a genuine co-Poisson factorization or projected commutator vanishing;
\item prove compact/tail payment for the evaluator-projected commutator kernel;
\item develop a signed explicit-formula conservation theorem that directly excludes the residual;
\item scope the theorem with an explicit $\Xi^{\mathrm{BC}}$ nonclaim.
\end{enumerate}

\end{document}
'''
(out / 'xi_bc_residual_classification_step155.tex').write_text(tex)

summary = r'''
# Step 155: \(\Xi^{\rm BC}\) Residual Classification

## Main verdict

\[
\boxed{\Xi^{\rm BC}\text{ remains active.}}
\]

The residual has not been proved zero, compact/tail-payable, or source-absorbable in a non-circular way.

The direct residual-exclusion route reduced to the projected commutator

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad
m_\ell(s)=e^{-\ell(1/2-s)}.
\]

For pulled Burnol zero-evaluator kernels

\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

the residual is controlled by

\[
r_{\ell,\rho,k}=C_\ell\eta^a_{\rho,k}.
\]

So

\[
H_R=0
\iff
C_\ell\eta^a_{\rho,k}=0
\quad\forall \ell,\rho,k.
\]

That vanishing is not earned by the raw log-shift.

---

## Classification

### 1. Zero / direct exclusion

Accepted only if

\[
C_\ell\eta^a_{\rho,k}=0
\quad\forall \ell,\rho,k.
\]

A lawful sufficient certificate would be

\[
M(\mathfrak B_{\ell,a}u)(s)=\zeta(s)\alpha_{\ell,u}(s).
\]

This is not produced by a raw shift.

### 2. Compact / tail-payable

Accepted only if \(\Xi^{\rm BC}\) is compact or trace/tail-controlled on a fixed/exhaustive residual ledger.

Raw shifted Sonin blocks were already shown noncompact in earlier steps, so compactness cannot be assumed.

### 3. Source-absorbable

Positive source frames do not by themselves close the residual. If

\[
F_N\succeq \Lambda_NG_R,
\qquad \Lambda_N\to\infty,
\]

then for a fixed positive ledger \(K_R\),

\[
\operatorname{tr}(F_NK_R)
\ge
\Lambda_N\operatorname{tr}(G_RK_R).
\]

Therefore a sublinear source budget is already collapse-strength.

### 4. Scoped nonclaim

If no zero, compact, or non-circular source record is proved, the theorem must explicitly carry

\[
\Xi^{\rm BC}
\]

as an adequacy residual.

---

## Bottom line

\[
\boxed{
\text{The route is now residual-classified rather than closed.}
}
\]

The next proof-producing move is not another positive source frame. It is either:

\[
\boxed{\text{co-Poisson factorization / commutator vanishing}}
\]

or

\[
\boxed{\text{compactness or signed conservation for }\Xi^{\rm BC}.}
\]

## Next step

\[
\boxed{\textbf{Step 156: signed explicit-formula conservation audit for }\Xi^{\rm BC}.}
\]

Target: determine whether the explicit formula supplies a signed conservation identity that directly cancels or excludes the residual, rather than trying to absorb it with a positive source frame.
'''
(out / 'step155_results_summary.md').write_text(summary)

# Tables
classification_rows = [
    ["zero_direct_exclusion", "C_l eta_z = 0 for every pulled zero evaluator", "not earned", "requires co-Poisson factorization or projected commutator identity", "proof-producing if closed"],
    ["compact_tail_payable", "Xi_BC compact or trace/tail-controlled on fixed ledger", "not earned", "raw shifted Sonin block noncompact; evaluator-projected compactness remains open", "conditional proof if tail paid"],
    ["positive_source_absorption", "F_N >= Lambda_N G_R plus source budget", "blocked as shortcut", "source budget is collapse-strength by positivity", "diagnostic unless independent signed audit exists"],
    ["signed_conservation", "explicit-formula signed identity cancels/excludes residual", "open", "must avoid positive trace no-free theorem", "best next proof-producing target"],
    ["scoped_nonclaim", "Xi_BC carried explicitly in theorem statement", "available", "honest scope discipline", "conditional/nonclaim boundary"],
]
with open(out / 'xi_bc_classification_gate_table_step155.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["classification", "acceptance_condition", "current_status", "obstruction_or_need", "route_consequence"])
    w.writerows(classification_rows)

theorem_rows = [
    ["T155.1", "Residual kernel positivity", "R_l(z,z')=<C_l eta_z,C_l eta_z'> is positive semidefinite", "proved algebraically", "defines Xi_BC as adequacy residual"],
    ["T155.2", "Zero/direct criterion", "Xi_BC=0 iff C_l eta_z=0 for all visible zero evaluators", "proved algebraically", "direct route target"],
    ["T155.3", "No-free positive source budget", "F_N >= Lambda_N G_R implies tr(F_N K)/Lambda_N >= tr(G_R K)", "proved algebraically", "positive source squeeze is diagnostic"],
    ["T155.4", "Compact/tail promotion criterion", "compact or trace-class residual plus exhaustive windows implies tail payment", "conditional", "requires new compactness theorem"],
    ["T155.5", "Scoped residual theorem", "final claim must include Xi_BC unless a record closes it", "methodological", "prevents smuggling"],
]
with open(out / 'theorem_map_step155.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["id", "name", "statement", "status", "role"])
    w.writerows(theorem_rows)

route_rows = [
    ["positive_trace_squeeze", "diagnostic", "blocked by no-free budget", "do not pursue as proof-producing without independent signed budget"],
    ["direct_commutator_vanishing", "open", "requires C_l eta_z=0", "keep as proof-producing target"],
    ["copoisson_factorization", "open", "requires zeta multiplier for shifted boundary packets", "best clean certificate if found"],
    ["compact_tail_payment", "open-low confidence", "raw shifted block noncompact", "only viable after evaluator-specific projection cancellation"],
    ["signed_conservation", "open", "requires explicit-formula cancellation not positive trace", "recommended Step 156"],
    ["scoped_nonclaim", "available", "declare Xi_BC residual", "honest fallback"],
]
with open(out / 'route_status_step155.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["route", "status", "reason", "recommendation"])
    w.writerows(route_rows)

construction_rows = [
    ["C1", "Compute C_l eta_z in a faithful Burnol/Sonin model", "projected kernel formula", "numerical/formal sanity only unless exact P_La known"],
    ["C2", "Search for co-Poisson factorization of B_l,a", "M(Bu)=zeta alpha", "proof-producing if exact"],
    ["C3", "Audit compactness of evaluator-projected residual kernel", "singular values/tail of R_l(z,z')", "compact-tail route"],
    ["C4", "Audit signed explicit-formula conservation", "signed residual cancellation identity", "recommended next step"],
    ["C5", "Write scoped theorem with Xi_BC budget", "nonclaim ledger", "publication honesty"],
]
with open(out / 'construction_tasks_step155.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["task_id", "task", "object", "purpose"])
    w.writerows(construction_rows)

nonclaim = r'''
# Step 155 nonclaim boundary

Step 155 does not prove RH.

It does not prove:

- \(H_R=0\),
- \(\Xi^{\rm BC}=0\),
- compactness of \(\Xi^{\rm BC}\),
- source absorption of \(\Xi^{\rm BC}\),
- or completed off-critical-zero exclusion.

It proves a classification theorem:

\[
\Xi^{\rm BC}
\]

must be closed by a direct zero record, compact/tail record, non-circular source/signed conservation record, or else carried as a scoped residual.

The positive source-frame trace squeeze is diagnostic only. The missing source budget is collapse-strength and cannot be supplied by fixed positive weights or normalization.
'''
(out / 'nonclaim_boundary_step155.md').write_text(nonclaim)

schema = {
    "step": 155,
    "name": "Xi^BC residual classification",
    "active_residual": "Xi_BC = B^* Pi_Y B",
    "decision": "active_not_closed",
    "classification": ["zero_direct", "compact_tail", "noncircular_source_or_signed_conservation", "scoped_nonclaim"],
    "next_step": 156,
    "next_target": "signed explicit-formula conservation audit for Xi_BC",
    "created_files": []
}
(out / 'step155_schema.json').write_text(json.dumps(schema, indent=2))

# Check script
check_script = r'''#!/usr/bin/env python3
from pathlib import Path
import json, csv
base = Path(__file__).resolve().parent
required = [
    'xi_bc_residual_classification_step155.tex',
    'step155_results_summary.md',
    'xi_bc_classification_gate_table_step155.csv',
    'theorem_map_step155.csv',
    'route_status_step155.csv',
    'construction_tasks_step155.csv',
    'nonclaim_boundary_step155.md',
    'step155_schema.json',
]
missing = [f for f in required if not (base/f).exists()]
print(json.dumps({"missing": missing, "ok": not missing}, indent=2))
for csv_name in ['xi_bc_classification_gate_table_step155.csv','theorem_map_step155.csv','route_status_step155.csv']:
    with open(base/csv_name, newline='') as f:
        rows = list(csv.reader(f))
    print(csv_name, 'rows=', len(rows)-1, 'cols=', len(rows[0]))
'''
(out / 'run_step155_classification_check.py').write_text(check_script)
(out / 'run_step155_classification_check.py').chmod(0o755)

# Plots
plt.rcParams.update({'figure.dpi': 160})

# 1 classification scores
labels = ['zero\nrecord', 'compact\ntail', 'positive\nsource', 'signed\nconservation', 'scoped\nnonclaim']
proof_score = np.array([0.15,0.20,0.05,0.35,0.95])
fig, ax = plt.subplots(figsize=(8,4.5))
ax.bar(labels, proof_score)
ax.set_ylim(0,1)
ax.set_ylabel('current lawful availability')
ax.set_title('Step 155 residual classification status')
for i,v in enumerate(proof_score):
    ax.text(i, v+0.03, f'{v:.2f}', ha='center')
fig.tight_layout()
fig.savefig(out/'xi_bc_classification_status_step155.png')
plt.close(fig)

# 2 no free budget: normalized exposure ratio >= residual mass
Lambda = np.logspace(0, 4, 200)
residual_masses = [1.0, 0.3, 0.05, 0.0]
fig, ax = plt.subplots(figsize=(8,4.5))
for m in residual_masses:
    exposure = Lambda * m
    ax.plot(Lambda, exposure/Lambda, label=f'residual mass={m:g}')
ax.set_xscale('log')
ax.set_xlabel('source lower-frame strength Lambda')
ax.set_ylabel('tr(FK)/Lambda lower bound')
ax.set_title('No-free source-budget obstruction')
ax.legend()
fig.tight_layout()
fig.savefig(out/'no_free_budget_residual_mass_step155.png')
plt.close(fig)

# 3 hypothetical compact tails vs noncompact plateau
n = np.arange(1,151)
compact_tail = 1/(1+n/8)**1.5
trace_tail = np.exp(-n/35)
noncompact_plateau = 0.35 + 0.05*np.sin(n/9)**2
fig, ax = plt.subplots(figsize=(8,4.5))
ax.plot(n, compact_tail, label='compact tail model')
ax.plot(n, trace_tail, label='trace-class tail model')
ax.plot(n, noncompact_plateau, label='noncompact plateau')
ax.set_xlabel('window index')
ax.set_ylabel('tail norm / singular value proxy')
ax.set_title('Compact/tail-payable versus active residual scenarios')
ax.legend()
fig.tight_layout()
fig.savefig(out/'compact_tail_vs_active_residual_step155.png')
plt.close(fig)

# 4 residual classification flow Sankey-like custom lines
fig, ax = plt.subplots(figsize=(9,5))
ax.axis('off')
boxes = {
    'Xi active': (0.08,0.5),
    'zero\nrecord': (0.35,0.8),
    'compact\ntail': (0.35,0.6),
    'signed\nsource': (0.35,0.4),
    'scoped\nnonclaim': (0.35,0.2),
    'closed': (0.68,0.72),
    'conditional': (0.68,0.2),
}
for text,(x,y) in boxes.items():
    ax.text(x,y,text,ha='center',va='center',bbox=dict(boxstyle='round,pad=0.35',fc='white',ec='black'))
for target in ['zero\nrecord','compact\ntail','signed\nsource','scoped\nnonclaim']:
    x0,y0 = boxes['Xi active']; x1,y1 = boxes[target]
    ax.annotate('', xy=(x1-0.09,y1), xytext=(x0+0.08,y0), arrowprops=dict(arrowstyle='->'))
for src in ['zero\nrecord','compact\ntail','signed\nsource']:
    x0,y0 = boxes[src]; x1,y1=boxes['closed']
    ax.annotate('', xy=(x1-0.08,y1), xytext=(x0+0.09,y0), arrowprops=dict(arrowstyle='->'))
x0,y0=boxes['scoped\nnonclaim']; x1,y1=boxes['conditional']
ax.annotate('', xy=(x1-0.1,y1), xytext=(x0+0.1,y0), arrowprops=dict(arrowstyle='->'))
ax.set_title('Step 155 classification flow')
fig.tight_layout()
fig.savefig(out/'xi_bc_classification_flow_step155.png')
plt.close(fig)

# CSV data for plots
with open(out/'classification_status_step155.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['route','availability_score'])
    for lab,val in zip(labels, proof_score): w.writerow([lab.replace('\n',' '),val])
with open(out/'no_free_budget_residual_mass_step155.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Lambda','mass_1','mass_0_3','mass_0_05','mass_0'])
    for L in Lambda[::5]: w.writerow([L,1,0.3,0.05,0])
with open(out/'compact_tail_vs_active_residual_step155.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['n','compact_tail','trace_tail','noncompact_plateau'])
    for i,a,b,c in zip(n,compact_tail,trace_tail,noncompact_plateau): w.writerow([i,a,b,c])

# zip artifacts
schema['created_files'] = sorted([p.name for p in out.iterdir() if p.is_file() and p.name != 'step155_xi_bc_classification_artifacts.zip'])
(out / 'step155_schema.json').write_text(json.dumps(schema, indent=2))
zip_path = out/'step155_xi_bc_classification_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != zip_path.name:
            z.write(p, arcname=p.name)
print('created', out)
print('files', len(list(out.iterdir())))
