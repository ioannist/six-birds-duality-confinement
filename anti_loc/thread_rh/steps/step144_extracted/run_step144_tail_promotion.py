import os, json, csv, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step144_completed_tail_promotion')
OUT.mkdir(parents=True, exist_ok=True)

N = np.arange(10, 401, 10)
gamma = 0.35 * (N ** 0.55)
epsilon = 0.48 * np.exp(-0.011 * N) + 0.08
delta = 0.35 * np.exp(-0.0075 * N) + 0.18
floor = (1 - epsilon**2) * (1 - delta**2)
Lambda = gamma * floor
tail_good = N**(-1.25)
tail_marginal = 1/np.log(N+2)
tail_bad = 0.18 + 0.08*np.exp(-0.004*N)
scaled_good = Lambda * tail_good
scaled_marginal = Lambda * tail_marginal
scaled_bad = Lambda * tail_bad
Csrc = 1.0
collapse_good = Csrc/np.maximum(Lambda,1e-12) + tail_good
collapse_marginal = Csrc/np.maximum(Lambda,1e-12) + tail_marginal
collapse_bad = Csrc/np.maximum(Lambda,1e-12) + tail_bad

with open(OUT/'completed_tail_promotion_scenarios_step144.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['N','gamma_source','epsilon_density','delta_blind','visibility_floor','Lambda_eff','tail_good','tail_marginal','tail_bad','scaled_tail_good','scaled_tail_marginal','scaled_tail_bad','collapse_good','collapse_marginal','collapse_bad'])
    for row in zip(N,gamma,epsilon,delta,floor,Lambda,tail_good,tail_marginal,tail_bad,scaled_good,scaled_marginal,scaled_bad,collapse_good,collapse_marginal,collapse_bad):
        w.writerow([float(x) for x in row])

def save_plot(filename, x, ys, labels, xlabel, ylabel, title):
    plt.figure(figsize=(8,5))
    for y,l in zip(ys, labels):
        plt.plot(x,y,label=l)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT/filename, dpi=180)
    plt.close()

save_plot('effective_source_strength_step144.png', N, [gamma, Lambda], ['raw $\\gamma_N$', '$\\Lambda_N^\\Omega$ after floors'], 'window index $N$', 'source strength', 'Effective source strength after density and blind-sector floors')
save_plot('completed_tail_promotion_model_step144.png', N, [collapse_good, collapse_marginal, collapse_bad], ['good exhaustive tail', 'marginal tail', 'failed tail floor'], 'window index $N$', 'residual budget upper bound', 'Completed residual-ledger squeeze scenarios')
save_plot('scaled_tail_gate_step144.png', N, [scaled_good, scaled_marginal, scaled_bad], ['good: $\\Lambda_N T_N$', 'marginal: $\\Lambda_N T_N$', 'failed: $\\Lambda_N T_N$'], 'window index $N$', 'scaled lifted-tail term', 'Lifted lower-frame tail term')
save_plot('moving_window_failure_step144.png', N, [tail_good, tail_bad], ['exhaustive tail tends to 0', 'moving-window blind tail persists'], 'window index $N$', 'tail mass', 'Moving-window support evidence versus exhaustive ledger')
save_plot('finite_vs_completed_ledger_step144.png', N, [floor, 1-tail_good, 1-tail_bad], ['finite visibility floor', 'completed coverage: exhaustive', 'completed coverage: failed'], 'window index $N$', 'coverage/floor', 'Finite source floors do not imply completed coverage')

rows = [
    ['G1', 'Finite source frame', r'$F_{N}^{\Omega,\mathrm{win}}\succeq \Lambda_N^\Omega G_{R,N}$', 'Needed before any promotion; supplied only conditionally by restricted BPRZ plus gates.'],
    ['G2', 'Visibility floors', r'$\Lambda_N^\Omega=\gamma_{q_N}(1-\epsilon_{B\to\Omega,N}^2)(1-\delta_{R,K,N}^2)$', 'Density and GCD-blind suppression must both leave a positive floor.'],
    ['G3', 'Shortness', r'$L_{\mathrm{eff}}(N,K_N)\le q_N^{\theta_{\mathrm{src}}-o(1)}$', 'Keeps the restricted twisted-second-moment import lawful.'],
    ['G4', 'Window embedding', r'$P_N:H_R\to H_R,\;P_N\uparrow I$', 'Declares the finite residual windows inside the completed carrier.'],
    ['G5', 'Plancherel/exhaustivity', r'$G_R\preceq P_N^*G_{R,N}P_N+T_N$', 'The bridge from finite-window frame to completed lower frame.'],
    ['G6', 'Tail payment', r'$\mathrm{tr}(K_RT_N)\to0$ or stronger', 'Prevents moving-window support-only evidence.'],
    ['G7', 'Source-budget boundedness', r'$\sup_N\mathrm{tr}(F_N^\Omega K_R)\le C_{\rm src}$', 'Converts lower-frame growth into residual budget collapse.'],
    ['G8', 'Completed ledger squeeze', r'$\mathrm{tr}(G_RK_R)\le C_{\rm src}/\Lambda_N^\Omega+\mathrm{tail}_N+o(1)$', 'Accepted only if the right-hand side tends to zero.'],
]
with open(OUT/'completed_tail_gate_table_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['gate','name','formal_record','status_or_risk']); w.writerows(rows)

thm_rows = [
    ['T144.1', 'Finite-to-completed lower-frame lift', r'$F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R$', 'Algebraic promotion from window frame plus Plancherel/exhaustivity.'],
    ['T144.2', 'Completed residual budget squeeze', r'$\mathrm{tr}(G_RK_R)\le C_{\rm src}/\Lambda_N^\Omega+\mathrm{tr}(T_NK_R)$', 'If source budget is bounded and tail vanishes, completed residual mass collapses.'],
    ['T144.3', 'Moving-window non-promotion', r'$\liminf\mathrm{tr}(T_NK_R)>0$', 'Finite frames may pass but completed theorem remains support-only.'],
    ['T144.4', 'Omega-compatible promotion criterion', r'$\gamma_q(1-\epsilon^2)(1-\delta^2)\to\infty$ plus tail', 'The restricted source route advances exactly under this criterion.'],
]
with open(OUT/'theorem_map_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','theorem','formula','role']); w.writerows(thm_rows)

status_rows = [
    ['finite prime-conductor frame', 'closed algebraically', 'complete/primitive character orthogonality; no-aliasing required'],
    ['source-weighted lower frame', 'conditional import', 'restricted BPRZ route must be restricted away from GCD-log blind sector'],
    ['GCD-log obstruction', 'conditionally controlled', 'Omega-compatible dictionary plus blind-projected incidence floor'],
    ['Omega-compatible density', 'open/conditional', 'only relative to Dirichlet-readable shadow closure so far'],
    ['completed residual-tail promotion', 'new Step 144 gate', 'requires fixed/exhaustive ledger, not moving-window evidence'],
    ['RH consequence', 'not claimed', 'would require all gates plus zeta carrier discharge'],
]
with open(OUT/'route_status_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['component','status','note']); w.writerows(status_rows)

arith_rows = [
    ['BPRZ twisted second moment', 'source-weighted restricted frame', 'Needs lower-eigenvalue import on nonblind residual class; length < q^{51/101}.'],
    ['Heap-Soundararajan Omega blocks', 'non-smuggled cutoff architecture', 'Controls high-divisibility design, not operator density by itself.'],
    ['Burnol co-Poisson/Sonine', 'completed carrier and residual windows', 'Supplies L_a,K_a,P_a,Y_a language and zero-evaluator exhaustivity backbone.'],
    ['CCM semilocal Hardy-Titchmarsh', 'ambient response geometry', 'Supplies local-factor insertion and semilocal Sonin transport.'],
    ['Completed tail estimate', 'load-bearing open input', 'Must show the finite windows exhaust the fixed residual ledger.'],
]
with open(OUT/'arithmetic_input_table_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['input','framework_role','needed_record']); w.writerows(arith_rows)

construct_rows = [
    ['C1', 'Declare completed residual carrier H_R and ledger K_R/A_R', 'fixed object, not selected by finite-window success'],
    ['C2', 'Define residual window projections P_N', 'must increase or exhaust in an audited order'],
    ['C3', 'Prove Plancherel/exhaustivity tail G_R <= P_N^*G_{R,N}P_N + T_N', 'tail form T_N declared'],
    ['C4', 'Lift finite Omega-compatible source frame', 'F_N^Omega = P_N^* F_N^{win} P_N'],
    ['C5', 'Bound source audit budget', 'sup_N tr(F_N^Omega K_R) <= C_src'],
    ['C6', 'Show tail payment', 'tr(T_N K_R) -> 0 or budgeted by audited defect'],
    ['C7', 'Only then claim completed residual absorption', 'avoid moving-window support-only overread'],
]
with open(OUT/'construction_tasks_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['task','description','acceptance_condition']); w.writerows(construct_rows)

nonclaim = r"""# Step 144 nonclaim boundary

Step 144 does not prove RH and does not prove that the \(\Omega\)-compatible ladder is dense in the completed Burnol/Sonine residual carrier.

It also does not license the claim that finite-window source frames settle the completed residual problem. Finite windows are support evidence unless a fixed or exhaustive residual ledger is declared and the tail is paid.

The accepted claim is conditional:

\[
\text{finite \(\Omega\)-compatible lower frame}
+\text{Plancherel/exhaustivity tail}
+\text{source-budget bound}
\Rightarrow
\text{completed residual squeeze}.
\]

If the tail form has nonvanishing mass on the completed residual ledger, the status remains `moving_window_support_only`.
"""
(OUT/'nonclaim_boundary_step144.md').write_text(nonclaim)

summary = r"""# Step 144: Completed residual-tail promotion for the Omega-compatible ladder

## Main purpose

Step 144 promotes the finite \(\Omega\)-compatible source-frame certificates to the completed residual ledger, or else marks them as moving-window support evidence.

The active finite source strength is

\[
\Lambda_N^\Omega
=
\gamma_{q_N}
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
\]

The finite lower frame is

\[
F_N^{\Omega,\mathrm{win}}\succeq \Lambda_N^\Omega G_{R,N}.
\]

The completed promotion requires a residual carrier \(H_R\), a fixed residual ledger \(K_R\) or \(A_R\), window projections \(P_N\), and a tail form \(T_N\) such that

\[
G_R\preceq P_N^*G_{R,N}P_N+T_N.
\]

Then the lifted source frame satisfies

\[
F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R.
\]

## Completed budget squeeze

If

\[
\sup_N \operatorname{tr}(F_N^\Omega K_R)\le C_{\rm src},
\]

and

\[
\operatorname{tr}(T_NK_R)\to0,
\]

then

\[
\operatorname{tr}(G_RK_R)
\le
\frac{C_{\rm src}}{\Lambda_N^\Omega}
+
\operatorname{tr}(T_NK_R).
\]

Thus the completed residual budget collapses if \(\Lambda_N^\Omega\to\infty\) and the tail is exhaustive.

## Moving-window warning

If the finite windows pass but

\[
\liminf_N\operatorname{tr}(T_NK_R)>0,
\]

then the result remains support-only:

\[
\boxed{\texttt{moving\_window\_support\_only}.}
\]

This is the same fixed/exhaustive discipline established earlier in the membrane framework.

## Status

Step 144 does not close the RH route. It states the exact promotion gate needed after the finite \(\Omega\)-compatible restricted BPRZ source frame.

The next step is to instantiate \(H_R\), \(P_N\), \(T_N\), and \(K_R\) on the actual Burnol/Sonine residual carrier.
"""
(OUT/'step144_results_summary.md').write_text(summary)

latex = r"""
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage[margin=1in]{geometry}
\title{Step 144: Completed Residual-Tail Promotion for the \texorpdfstring{$\Omega$}{Omega}-Compatible Ladder}
\author{Six Birds / Membrane--\texorpdfstring{$\Xi$}{Xi} RH Construction Notes}
\date{}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{warning}{Warning}

\begin{document}
\maketitle

\section{Purpose}
The previous steps reduced the residual source route to a finite \(\Omega\)-compatible lower-frame statement.  Step 144 asks whether those finite certificates promote to the completed residual ledger, or whether they remain moving-window support evidence.

The finite effective source strength has the form
\begin{equation}
\Lambda_N^\Omega
=
\gamma_{q_N}
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
\end{equation}
Here \(\gamma_{q_N}\) is the restricted source-weighted lower-frame strength, \(\epsilon_{B\to\Omega,N}\) is the \(\Omega\)-compatible density defect, and \(\delta_{R,K,N}\) is the GCD-log blind-sector defect.

\section{Completed residual carrier}
Let \(H_R\) be the completed residual Hilbert carrier, and let \(G_R\) be the completed residual metric.  Let \(P_N\) be finite-window projections or window maps, with finite metric \(G_{R,N}\).  The finite window source frame is accepted only if
\begin{equation}
F_N^{\Omega,\mathrm{win}}\succeq \Lambda_N^\Omega G_{R,N}.
\end{equation}

\begin{definition}[Plancherel/exhaustivity tail]
A completed Plancherel/exhaustivity record is a positive form \(T_N\succeq0\) such that
\begin{equation}
G_R\preceq P_N^*G_{R,N}P_N+T_N.
\end{equation}
The form \(T_N\) is the completed residual tail missed by the finite window.
\end{definition}

\section{Finite-to-completed promotion}
\begin{theorem}[Lifted lower frame]
Assume
\[
F_N^{\Omega,\mathrm{win}}\succeq \Lambda_N^\Omega G_{R,N}
\]
and
\[
G_R\preceq P_N^*G_{R,N}P_N+T_N.
\]
Let
\[
F_N^\Omega=P_N^*F_N^{\Omega,\mathrm{win}}P_N.
\]
Then
\begin{equation}
F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R.
\end{equation}
\end{theorem}

\begin{proof}
By the finite window lower frame,
\[
P_N^*F_N^{\Omega,\mathrm{win}}P_N\succeq \Lambda_N^\Omega P_N^*G_{R,N}P_N.
\]
By the Plancherel/exhaustivity record,
\[
P_N^*G_{R,N}P_N\succeq G_R-T_N.
\]
Combining gives
\[
F_N^\Omega\succeq \Lambda_N^\Omega(G_R-T_N),
\]
which is equivalent to
\[
F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R.
\]
\end{proof}

\section{Completed residual budget squeeze}
Let \(K_R\succeq0\) be the completed residual ledger/covariance to be confined.

\begin{theorem}[Completed residual squeeze]
Assume the lifted lower frame of the previous theorem.  Suppose the source audit budget is bounded:
\begin{equation}
\sup_N\operatorname{tr}(F_N^\Omega K_R)\le C_{\rm src}<\infty,
\end{equation}
and the completed tail is paid:
\begin{equation}
\operatorname{tr}(T_NK_R)\to0.
\end{equation}
Then
\begin{equation}
\operatorname{tr}(G_RK_R)
\le
\frac{C_{\rm src}}{\Lambda_N^\Omega}
+
\operatorname{tr}(T_NK_R).
\end{equation}
In particular, if \(\Lambda_N^\Omega\to\infty\), then \(\operatorname{tr}(G_RK_R)\to0\).
\end{theorem}

\begin{proof}
Taking the trace of
\[
\Lambda_N^\Omega G_R\preceq F_N^\Omega+\Lambda_N^\Omega T_N
\]
against \(K_R\succeq0\) gives
\[
\Lambda_N^\Omega\operatorname{tr}(G_RK_R)
\le
\operatorname{tr}(F_N^\Omega K_R)+
\Lambda_N^\Omega\operatorname{tr}(T_NK_R).
\]
Divide by \(\Lambda_N^\Omega\) and use the source budget bound.
\end{proof}

\section{Moving-window non-promotion}
\begin{warning}[Finite windows are not completed evidence]
If the finite source frames pass but
\[
\liminf_N\operatorname{tr}(T_NK_R)>0,
\]
then the result is only a moving-window certificate.  Its honest status is
\[
\boxed{\texttt{moving\_window\_support\_only}.}
\]
No completed residual confinement follows.
\end{warning}

\section{Omega-compatible route status}
The restricted source route now requires all four records:
\begin{enumerate}
\item \(\epsilon_{B\to\Omega,N}<1\) or preferably \(\to0\),
\item \(\delta_{R,K,N}<1\) or preferably \(\to0\),
\item \(\Lambda_N^\Omega=\gamma_{q_N}(1-\epsilon^2)(1-\delta^2)\to\infty\),
\item completed tail payment \(\operatorname{tr}(T_NK_R)\to0\).
\end{enumerate}
Only then does the finite \(\Omega\)-compatible ladder become a completed source absorption theorem.

\section{Next target}
The next construction target is to instantiate the completed residual carrier, window maps, and tail form in the actual Burnol/Sonine residual model:
\[
H_R,
\quad
P_N,
\quad
T_N,
\quad
K_R.
\]
This is the point at which Burnol completeness, co-Poisson support, and the semilocal Hardy--Titchmarsh response geometry must become a fixed/exhaustive ledger rather than a moving finite-window ladder.

\end{document}
"""
(OUT/'completed_tail_promotion_step144.tex').write_text(latex)

schema = {
    'step': 144,
    'name': 'Completed residual-tail promotion for the Omega-compatible ladder',
    'main_objects': ['H_R','G_R','P_N','T_N','K_R','F_N^Omega','Lambda_N^Omega'],
    'finite_source_strength': 'Lambda_N^Omega = gamma_q (1-epsilon^2)(1-delta^2)',
    'promotion_gate': 'F_N^Omega + Lambda_N^Omega T_N >= Lambda_N^Omega G_R',
    'budget_squeeze': 'tr(G_R K_R) <= C_src/Lambda_N^Omega + tr(T_N K_R)',
    'status_if_tail_fails': 'moving_window_support_only',
    'next_step': 'Instantiate H_R, P_N, T_N, K_R on actual Burnol/Sonine residual carrier'
}
(OUT/'step144_schema.json').write_text(json.dumps(schema, indent=2))

check = {
    'file': 'completed_tail_promotion_step144.tex',
    'dollar_balance': latex.count('$') % 2 == 0,
    'begin_document': '\\begin{document}' in latex,
    'end_document': '\\end{document}' in latex,
    'theorem_count': latex.count('\\begin{theorem}'),
    'warning_count': latex.count('\\begin{warning}')
}
with open(OUT/'latex_structure_check_step144.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['field','value']); w.writerows(check.items())

zip_path = OUT/'step144_completed_tail_promotion_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print('Created Step 144 artifacts in', OUT)
