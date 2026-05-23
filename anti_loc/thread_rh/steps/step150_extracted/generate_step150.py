from pathlib import Path
import csv, json, math, zipfile
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step150_source_budget_mechanism')
out.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{enumitem}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{corollary}{Corollary}
\newtheorem{obstruction}{Obstruction}
\title{Step 150: Source-Budget Mechanism Audit}
\author{RATCHET / RH Membrane Route Working Note}
\date{May 15, 2026}
\begin{document}
\maketitle

\section{Purpose}
Step 149 showed that the desired source audit budget
\[
  \frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}\to 0
\]
is not a harmless side estimate.  Under a positive lower frame it is already a collapse-strength
statement.  Step 150 audits whether any lawful \emph{a priori} mechanism can nevertheless supply
this budget: explicit-formula conservation, Plancherel identity, trace cancellation, compact-tail
payment, or direct residual invisibility.

\section{Standing objects}
Let $H_R$ be the Burnol/Sonine residual carrier, $G_R\succeq0$ the completed residual metric, and
$K_R^\omega\succeq0$ the fixed positive weighted residual zero ledger.  Let $F_N^\Omega\succeq0$ be the
finite-window lifted source frame and $\Lambda_N^\Omega\to\infty$ its effective lower-frame strength.
The ideal completed lower frame is
\[
  F_N^\Omega\succeq \Lambda_N^\Omega G_R.
\]
The defect version is
\[
  F_N^\Omega+E_N^{\rm lf}\succeq \Lambda_N^\Omega G_R,\qquad E_N^{\rm lf}\succeq0.
\]

\section{No-free-source-budget theorem}
\begin{theorem}[no free source budget]
Assume $F_N^\Omega\succeq \Lambda_N^\Omega G_R$ with $\Lambda_N^\Omega\to\infty$ and fix
$K_R^\omega\succeq0$, $K_R^\omega\in\mathcal S_1(H_R)$.  Then
\[
  \frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}
  \ge
  \operatorname{tr}(G_RK_R^\omega).
\]
Consequently, if the source budget is sublinear,
\[
  \frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}\to0,
\]
then
\[
  \operatorname{tr}(G_RK_R^\omega)=0.
\]
If $K_R^\omega$ is separating on $H_R$, this is already residual exclusion.
\end{theorem}

\begin{proof}
Because $F_N^\Omega-\Lambda_N^\Omega G_R\succeq0$ and $K_R^\omega\succeq0$ is trace-class,
\[
 \operatorname{tr}((F_N^\Omega-\Lambda_N^\Omega G_R)K_R^\omega)\ge0.
\]
Rearranging gives the displayed inequality.  Dividing by $\Lambda_N^\Omega$ and passing to the
limit gives the conclusion.
\end{proof}

\begin{corollary}[defect-normalized version]
If
\[
 F_N^\Omega+E_N^{\rm lf}\succeq\Lambda_N^\Omega G_R,
\]
then
\[
 \operatorname{tr}(G_RK_R^\omega)
 \le
 \frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}
 +
 \frac{\operatorname{tr}(E_N^{\rm lf}K_R^\omega)}{\Lambda_N^\Omega}.
\]
Thus a defect-paid source budget requires both normalized terms on the right to vanish.
\end{corollary}

\section{Mechanism audit}
\subsection{Plancherel conservation}
A Plancherel identity can normalize a source family to an identity resolution,
\[
  \int Q_\omega^*Q_\omega\,d\mu(\omega)=I.
\]
But this gives a bounded frame, not a diverging lower frame.  Repeating or enlarging the source
family to obtain $\Lambda_N^\Omega\to\infty$ multiplies the positive exposure against a positive
ledger.  Therefore Plancherel alone cannot supply a sublinear source budget.  It can supply the
\emph{lower-frame side} or a tail/exhaustivity record, but not the budget against a nonzero fixed
positive ledger.

\subsection{Explicit-formula conservation}
The explicit formula has signed cancellation among zero, prime, pole, and archimedean terms.
The source frame $F_N^\Omega$ is positive.  Once the signed expression is replaced by a positive
coercive frame, trace cancellation against $K_R^\omega\succeq0$ is lost.  A signed conservation law can
only help if it is kept as a separate signed ledger
\[
  S_N = F_N^\Omega - C_N
\]
with a declared negative/compensating part $C_N\succeq0$ and a proof that the cancellation survives
on $K_R^\omega$.  That is a new theorem, not a free consequence of the lower frame.

\subsection{Trace cancellation}
There is no trace cancellation between positive operators:
\[
  F_N^\Omega\succeq0,
  \quad K_R^\omega\succeq0
  \quad\Longrightarrow\quad
  \operatorname{tr}(F_N^\Omega K_R^\omega)\ge0.
\]
Any cancellation mechanism must occur before positivity is imposed, in a signed representation,
and must be audited as a separate channel.

\subsection{Compact/tail payment}
Compact defects and completed tails can pay
\[
  \operatorname{tr}(T_NK_R^\omega)\to0
\]
and can make finite windows exhaustive.  They do not reduce the leading source exposure
\[
  \Lambda_N^\Omega\operatorname{tr}(G_RK_R^\omega)
\]
unless the residual mass is already zero or the tail contains the entire residual, which is just the
moving-window failure mode.

\subsection{Direct residual invisibility}
The only currently lawful collapse-producing mechanism is direct invisibility or adequacy:
\[
  G_RK_R^\omega=0
  \quad\text{or}\quad
  \operatorname{tr}(G_RK_R^\omega)=0.
\]
For a separating positive ledger, this says that the residual zero-evaluator directions visible in
$H_R$ carry no off-critical displacement.  This is not a budget estimate; it is the theorem itself.

\section{Route consequence}
The source-squeeze branch has become diagnostic.  It can organize what would be required for a
proof, but it does not by itself produce the missing source budget.  A proof-producing route must
pivot to one of the following direct tasks:
\begin{enumerate}[label=(\roman*)]
\item prove $H_R=0$, i.e. shifted semilocal boundary packets lie in Burnol's co-Poisson complement;
\item prove direct residual invisibility $\Pi_RY^a_{\rho,k}=0$ for off-critical directions;
\item prove a signed explicit-formula conservation theorem that survives the positive-frame lower
      bound with a paid negative part;
\item change the theorem statement to a scoped nonclaim if a residual adequacy blind spot remains.
\end{enumerate}

\section{Conclusion}
The source budget cannot be obtained by Plancherel, positivity, trace-class weighting, or moving
weights.  Any valid source-budget proof is already a residual-collapse proof.  Therefore the next
productive step is a direct residual-exclusion / adequacy theorem for $H_R$.

\end{document}
'''
(out/'source_budget_mechanism_step150.tex').write_text(tex)

summary = r'''
# Step 150: Source-Budget Mechanism Audit

## Purpose

Step 149 showed that the desired source audit budget

\[
\frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}\to0
\]

is not a harmless estimate. Step 150 audits whether any lawful a priori mechanism can supply it.

## Main verdict

\[
\boxed{\text{No free source-budget mechanism is available.}}
\]

If

\[
F_N^\Omega\succeq \Lambda_N^\Omega G_R,
\qquad \Lambda_N^\Omega\to\infty,
\]

and

\[
K_R^\omega\succeq0
\]

is a fixed positive trace-class ledger, then

\[
\frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}
\ge
\operatorname{tr}(G_RK_R^\omega).
\]

Therefore a sublinear source budget already implies

\[
\operatorname{tr}(G_RK_R^\omega)=0.
\]

So the source-budget estimate is collapse-strength.

## Mechanism audit

| Mechanism | Verdict |
|---|---|
| Plancherel identity | Supplies identity resolution or lower-frame normalization, but not sublinear exposure against a nonzero positive ledger. |
| Explicit-formula conservation | Signed cancellation is lost after replacing the expression by a positive source frame unless a separate signed ledger is proved. |
| Trace cancellation | Impossible for positive source frame and positive ledger. |
| Compact/tail payment | Pays completed finite-window tails, but not the leading source exposure. |
| Moving weights | Invalid as a fixed completed ledger; status becomes moving-window support-only. |
| Direct residual invisibility | Lawful, but it is the theorem itself: residual exclusion or adequacy. |

## Route consequence

The source-squeeze branch is now diagnostic rather than proof-producing unless a new signed conservation theorem is supplied.

The proof-producing target should pivot to direct residual exclusion:

\[
H_R=0,
\]

or

\[
\Pi_RY^a_{\rho,k}=0
\]

for off-critical residual directions, or an explicit \(\Xi\)-adequacy theorem showing the residual is empty/paid.

## Next step

\[
\boxed{\textbf{Step 151: direct residual-exclusion / adequacy theorem for }H_R.}
\]

Target: decide whether the Burnol/Sonine residual carrier

\[
H_R=\overline{\operatorname{span}\operatorname{Ran}\Pi_{Y_a}\mathfrak B_{\ell,a}}
\]

is zero, tail-small, or a genuine adequacy residual.
'''
(out/'step150_results_summary.md').write_text(summary)

mechanisms = [
    ['mechanism','input','would_need','verdict','status'],
    ['Plancherel identity','identity resolution or spectral decomposition','sublinear trace exposure against fixed positive ledger','cannot supply; repeated sources scale exposure with Lambda','diagnostic_not_closing'],
    ['Explicit-formula conservation','signed zero/prime/pole/archimedean balance','signed cancellation after positive-frame conversion','not automatic; requires new signed ledger with paid negative part','new_theorem_required'],
    ['Trace cancellation','positive source frame and positive ledger','cancellation in trace','impossible for positive-positive trace','blocked'],
    ['Compact/tail payment','trace-class ledger and exhaustive windows','leading exposure reduction','pays tails only, not source exposure','partial_only'],
    ['Moving weights','weights depending on N','bounded exposure','invalid fixed ledger; moving-window support only','invalid_for_completed_claim'],
    ['Direct residual invisibility','G_R K_R^omega = 0','residual exclusion','lawful but equals theorem/collapse certificate','proof_target'],
    ['Signed source ledger','S_N = F_N - C_N','cancellation plus positive lower frame with negative part paid','possible but new source theorem; not inherited from BPRZ/large sieve','possible_new_route'],
]
with open(out/'source_budget_mechanism_table_step150.csv','w',newline='') as f:
    csv.writer(f).writerows(mechanisms)

route_status = [
    ['gate','status','reason','next_action'],
    ['positive lower frame','conditional','restricted BPRZ route may give finite lower frame on residual class','keep as conditional imported source platform'],
    ['omega-compatible density','open','density after Omega restrictions not proved by Burnol alone','carry epsilon_B_to_Omega'],
    ['GCD-log blind suppression','conditional','requires blind-projected incidence floor','carry delta_RKN'],
    ['trace-class ledger','closed under weighted envelope','positive fixed weights can make ledger trace-class and separating','use weighted ledger only'],
    ['source audit budget','blocked as free estimate','sublinear budget implies residual collapse already','pivot to direct residual exclusion'],
    ['completed tail','conditional','requires P_N upward to identity and trace-class ledger','keep as promotion gate'],
    ['proof-producing branch','pivot needed','source-squeeze is diagnostic unless signed conservation theorem is found','Step 151 direct residual exclusion/adequacy'],
]
with open(out/'route_status_step150.csv','w',newline='') as f:
    csv.writer(f).writerows(route_status)

thmap = [
    ['item','statement','depends_on','status'],
    ['Theorem 150.1','If F_N >= Lambda_N G_R then tr(F_N K)/Lambda_N >= tr(G_R K)','positivity and trace-class K','proved'],
    ['Corollary 150.2','Sublinear source exposure implies tr(G_R K)=0','Theorem 150.1','proved'],
    ['Corollary 150.3','Defect lower frame gives normalized exposure + normalized defect bound','positive defect E_N','proved'],
    ['Obstruction 150.4','Plancherel/normalization cannot supply source budget while preserving growth','Theorem 150.1','diagnostic'],
    ['Obstruction 150.5','Moving weights invalidate fixed completed ledger','fixed-ledger discipline','diagnostic'],
    ['Pivot 150.6','Direct residual exclusion/adequacy is next proof-producing target','failure of free budget','recommended'],
]
with open(out/'theorem_map_step150.csv','w',newline='') as f:
    csv.writer(f).writerows(thmap)

nonclaim = r'''
# Step 150 Nonclaim Boundary

Step 150 does not prove RH.

Step 150 does not prove that the restricted BPRZ source frame fails. It proves that even a successful lower frame does not by itself provide the source audit budget against a fixed positive residual ledger.

Step 150 does not claim that no signed explicit-formula mechanism can ever work. It claims only that such a mechanism is not inherited from the positive source-frame inequality and would require a separate signed-ledger theorem.

Step 150 does not allow moving weights depending on the finite window to replace a fixed completed ledger.

Step 150 does not close the Burnol/Sonine residual adequacy problem. It identifies direct residual exclusion or a signed conservation theorem as the next proof-producing target.
'''
(out/'nonclaim_boundary_step150.md').write_text(nonclaim)

construction_tasks = [
    ['task','description','priority','output'],
    ['Direct residual exclusion','Test whether H_R = 0 or Pi_Ya B_{ell,a}=0','highest','Step 151'],
    ['Signed conservation audit','Search for an explicit-formula conservation law that survives positive lower-frame conversion','medium','alternative Step 151b'],
    ['Defect source theorem','If lower-frame defects are present, prove tr(E_N K)/Lambda -> 0','medium','defect-paid variant'],
    ['Adequacy residual ledger','If H_R nonzero, define Xi_R and decide source/tail/nonclaim status','highest','route fork'],
    ['Completed tail record','Keep P_N upward I and trace-class tail promotion as standing gate','ongoing','promotion theorem'],
]
with open(out/'construction_tasks_step150.csv','w',newline='') as f:
    csv.writer(f).writerows(construction_tasks)

schema = {
    'step':150,
    'name':'Source-Budget Mechanism Audit',
    'main_verdict':'No free source-budget mechanism; source budget is collapse-strength under positive lower frame.',
    'key_inequality':'tr(F_N^Omega K_R^omega)/Lambda_N^Omega >= tr(G_R K_R^omega)',
    'route_status':'source-squeeze branch diagnostic unless new signed conservation theorem is supplied',
    'next_step':'Step 151: direct residual-exclusion / adequacy theorem for H_R',
    'artifacts':['source_budget_mechanism_step150.tex','step150_results_summary.md','source_budget_mechanism_table_step150.csv','route_status_step150.csv','theorem_map_step150.csv','nonclaim_boundary_step150.md']
}
(out/'step150_schema.json').write_text(json.dumps(schema,indent=2))

# plots
N = np.arange(1,101)
Lambda = np.log(N+2)**2 + 0.3*N**0.4
residual_masses = [0.0, 0.02, 0.1, 0.4]
plt.figure(figsize=(7,4.5))
for m in residual_masses:
    exposure = Lambda*m
    plt.plot(N, exposure/(Lambda+1e-12), label=f'mass={m}')
plt.xlabel('window N')
plt.ylabel('normalized exposure lower bound')
plt.title('No-free source budget: normalized exposure floor')
plt.legend()
plt.tight_layout()
plt.savefig(out/'no_free_budget_floor_step150.png', dpi=160)
plt.close()

# source budget mechanisms bar-like scenario
labels = ['Plancherel','Explicit\nformula','Trace\ncancel','Compact\ntail','Moving\nweights','Direct\ninvisibility']
# scores: 0 blocked, .5 partial, 1 proof target
scores = [0.2,0.45,0.0,0.45,0.0,1.0]
plt.figure(figsize=(7.2,4.5))
plt.bar(labels, scores)
plt.ylim(0,1.1)
plt.ylabel('lawful closing score (schematic)')
plt.title('Source-budget mechanism audit')
plt.tight_layout()
plt.savefig(out/'mechanism_audit_scores_step150.png', dpi=160)
plt.close()

# defect-normalized squeeze
defect_rates = [0.0, 0.05, 0.2]
mass = 0.1
plt.figure(figsize=(7,4.5))
for d in defect_rates:
    rhs = mass + d/(np.sqrt(N)+1)
    plt.plot(N, rhs, label=f'defect scale={d}')
plt.xlabel('window N')
plt.ylabel('upper bound only collapses if mass=0')
plt.title('Defect-normalized squeeze still requires residual collapse')
plt.legend()
plt.tight_layout()
plt.savefig(out/'defect_normalized_budget_step150.png', dpi=160)
plt.close()

# pivot diagram data plot
x = np.linspace(0,1,101)
diagnostic = 1-x
proof = x**2
plt.figure(figsize=(7,4.5))
plt.plot(x, diagnostic, label='source-squeeze as diagnostic')
plt.plot(x, proof, label='direct residual exclusion')
plt.xlabel('direct adequacy/invisibility progress')
plt.ylabel('route utility (schematic)')
plt.title('Route pivot after Step 150')
plt.legend()
plt.tight_layout()
plt.savefig(out/'route_pivot_step150.png', dpi=160)
plt.close()

# data csv for plots
with open(out/'source_budget_floor_model_step150.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['N','Lambda','mass','normalized_floor'])
    for n, lam in zip(N,Lambda):
        for m in residual_masses:
            w.writerow([int(n), float(lam), float(m), float(m)])

with open(out/'mechanism_audit_scores_step150.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['mechanism','score'])
    for l,s in zip(labels,scores):
        w.writerow([l.replace('\n',' '),s])

# write check script
check = r'''#!/usr/bin/env python3
from pathlib import Path
required = [
 'source_budget_mechanism_step150.tex','step150_results_summary.md',
 'source_budget_mechanism_table_step150.csv','route_status_step150.csv',
 'theorem_map_step150.csv','nonclaim_boundary_step150.md','step150_schema.json'
]
base = Path(__file__).resolve().parent
missing = [x for x in required if not (base/x).exists()]
if missing:
    raise SystemExit('Missing: '+', '.join(missing))
tex = (base/'source_budget_mechanism_step150.tex').read_text()
for token in ['No-free-source-budget theorem','Plancherel conservation','Explicit-formula conservation','Route consequence']:
    if token not in tex:
        raise SystemExit(f'Missing token in tex: {token}')
print('Step 150 structural check passed.')
'''
(out/'run_step150_source_budget_mechanism_check.py').write_text(check)

# zip
zip_path = out/'step150_source_budget_mechanism_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name and p.is_file():
            z.write(p, p.name)
print('wrote', zip_path)
