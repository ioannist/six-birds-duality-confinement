from pathlib import Path
import json, csv, math, zipfile
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step123_balanced_length')
out.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage[margin=1in]{geometry}
\title{Step 123: Balanced-Length Theorem for the Regularized Co-Poisson/M\"untz Shadow}
\author{RH Membrane Construction Notes}
\date{May 14, 2026}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\newtheorem{warning}{Warning}
\newcommand{\eps}{\varepsilon}
\newcommand{\cH}{\mathcal H}
\newcommand{\cB}{\mathcal B}
\newcommand{\cX}{\mathcal X}
\newcommand{\cN}{\mathcal N}
\newcommand{\cD}{\mathcal D}
\newcommand{\cC}{\mathcal C}
\newcommand{\tr}{\operatorname{tr}}
\newcommand{\Ran}{\operatorname{Ran}}
\newcommand{\dist}{\operatorname{dist}}

\begin{document}
\maketitle

\section{Purpose}
Step 122 replaced naive critical-line Dirichlet partial sums by a regularized M\"untz/co-Poisson shadow.  The new visibility-side obstruction is
\[
\eps_{\rm vis,N}
=\eps_{B,N}+\eps_{\rm Mell,N}+\tau_{M,N}+\kappa_{\rm tail,N},
\]
with
\[
c_{{\rm hyb},N}\ge 1-\eps_{\rm vis,N}^2.
\]
The source-side obstruction is still the Heap--Soundararajan style lower-frame strength
\[
G_{\cX,N}\succeq \gamma_N H_N.
\]
The RH membrane route requires
\[
\gamma_N c_{{\rm hyb},N}\to\infty
\]
with fixed/exhaustive ledger promotion.  Step 123 formulates the growth-rate compatibility condition under which the M\"untz shadow is accurate while the Dirichlet polynomial remains short enough for the source moment estimates.

\section{Parameters}
Let $Q_N$ be the source-family size parameter.  Depending on the source family, $Q_N$ may be a height $T$, a conductor bound, a family cardinality, or an adelic conductor window.  Let
\[
T_N=\text{vertical/spectral window},
\qquad
A_N=\text{Burnol atom complexity},
\]
and let $X_N$ be the length of the regularized Dirichlet shadow
\[
Z_{X_N}^{\omega}(s)
=\sum_{n\ge1}\omega(n/X_N)n^{-s}-X_N^{1-s}\Omega(1-s).
\]
Assume the M\"untz contour residual obeys, on the declared Burnol window,
\[
\tau_{M,N}
\le C_M A_N (1+T_N)^A X_N^{-\eta},
\qquad \eta>0.
\]
Assume the source/moment technology is valid for Dirichlet shadows of length
\[
X_N\le Q_N^{\theta_*},
\qquad \theta_*>0.
\]
For Heap--Soundararajan's zeta-height version, the short-polynomial proof uses a length bounded by a fixed positive power of the height, schematically $X\le T^{\theta_*}$; in their displayed construction one has a support bound of the form $n\le T^{k/9}$.

\section{The balanced-length cone}
\begin{definition}[Balance exponent]
For a requested residual decay buffer $r_N\ge0$, define
\[
\theta_{\min,N}
=
\frac{
\log A_N+A\log(1+T_N)+r_N
}{
\eta\log Q_N
}.
\]
The \emph{balanced-length cone} is nonempty at stage $N$ if
\[
\boxed{\theta_{\min,N}<\theta_*.}
\]
\end{definition}

\begin{theorem}[Balanced-length theorem]
Suppose there exists $\theta_N$ such that
\[
\theta_{\min,N}<\theta_N<\theta_*.
\]
Set
\[
X_N=Q_N^{\theta_N}.
\]
Then
\[
A_N(1+T_N)^A X_N^{-\eta}
\le e^{-r_N}.
\]
Consequently, if
\[
\eps_{B,N}+\eps_{\rm Mell,N}+\kappa_{\rm tail,N}\to0,
\qquad r_N\to\infty,
\]
then
\[
\tau_{M,N}\to0,
\qquad
c_{{\rm hyb},N}\to1.
\]
If additionally
\[
G_{\cX,N}\succeq\gamma_NH_N,
\qquad \gamma_N\to\infty,
\]
then the effective source strength diverges:
\[
\boxed{\gamma_Nc_{{\rm hyb},N}\to\infty.}
\]
\end{theorem}

\begin{proof}
The choice $X_N=Q_N^{\theta_N}$ gives
\[
\log\bigl(A_N(1+T_N)^A X_N^{-\eta}\bigr)
=\log A_N+A\log(1+T_N)-\eta\theta_N\log Q_N.
\]
Since $\theta_N>\theta_{\min,N}$,
\[
\eta\theta_N\log Q_N
>
\log A_N+A\log(1+T_N)+r_N,
\]
and hence
\[
A_N(1+T_N)^A X_N^{-\eta}<e^{-r_N}.
\]
The visibility conclusion follows from Step 122's bound
\[
c_{{\rm hyb},N}\ge1-(\eps_{B,N}+\eps_{\rm Mell,N}+\tau_{M,N}+\kappa_{\rm tail,N})^2.
\]
If the total visibility error tends to zero, then $c_{{\rm hyb},N}\to1$.  Multiplication by any divergent source lower-frame strength $\gamma_N$ gives the last assertion.
\end{proof}

\begin{corollary}[Sub-polynomial atom/window growth]
Assume
\[
\log A_N+A\log(1+T_N)=o(\log Q_N).
\]
Then for every fixed $0<\theta<\theta_*$, choosing $X_N=Q_N^{\theta}$ and any buffer $r_N=o(\log Q_N)$ gives the balanced-length condition.  Thus the M\"untz shadow can be accurate while remaining short for the source estimates.
\end{corollary}

\begin{corollary}[Polynomial regime]
Assume
\[
A_N\ll Q_N^{\alpha},
\qquad
1+T_N\ll Q_N^{\beta}.
\]
Then the balanced-length cone is nonempty provided
\[
\boxed{\alpha+A\beta<\eta\theta_*.}
\]
If this strict inequality holds, choose $\theta$ such that
\[
\frac{\alpha+A\beta}{\eta}<\theta<\theta_*.
\]
\end{corollary}

\section{Positive visibility floor}
Even if the shadow error does not vanish, the route can remain alive.  If
\[
\limsup_N\eps_{\rm vis,N}\le e_*<1,
\]
then
\[
\liminf_N c_{{\rm hyb},N}
\ge1-e_*^2>0.
\]
Therefore any divergent source strength $\gamma_N\to\infty$ still gives
\[
\gamma_Nc_{{\rm hyb},N}\to\infty.
\]
This is weaker than shadow completeness but still adequate for source-coercivity if all finite-window tails are promoted lawfully.

\section{Failure theorem}
\begin{theorem}[Length incompatibility obstruction]
Suppose that for every admissible source technology there is a fixed $\theta_*>0$ such that $X_N\le Q_N^{\theta_*}$, and suppose
\[
\liminf_N
\frac{\log A_N+A\log(1+T_N)}{\eta\log Q_N}
\ge\theta_*.
\]
Then no choice of $X_N$ both remains short for the source moment estimates and drives the M\"untz contour residual to zero.  The route must then supply one of:
\begin{enumerate}[label=(\roman*)]
\item a stronger regularization with larger $\eta$ or smaller complexity exponent $A$;
\item a source technology valid for longer polynomials, i.e. larger $\theta_*$;
\item a positive visibility floor plus source growth strong enough to compensate;
\item a scoped nonclaim / tail-defect record for the missed shadow sector.
\end{enumerate}
\end{theorem}

\section{Interpretation in the membrane route}
The active RH source route now has five independent terms:
\[
\gamma_N
\left[
1-(\eps_{B,N}+\eps_{\rm Mell,N}+\tau_{M,N}+\kappa_{\rm tail,N})^2
\right]
\to\infty.
\]
Here
\[
\gamma_N=\text{arithmetic source strength},
\]
\[
\eps_{B,N}=\text{Burnol geometric exhaustion defect},
\]
\[
\eps_{\rm Mell,N}=\text{Mellin/Dirichlet modeling defect},
\]
\[
\tau_{M,N}=\text{M\"untz contour residual},
\]
\[
\kappa_{\rm tail,N}=\text{finite-window support/tail defect}.
\]
Step 123 shows that the M\"untz residual is not the main obstacle if the balanced-length cone is open.  The real load-bearing tasks become:
\begin{enumerate}[label=O\arabic*.]
\item prove Burnol/co-Poisson exhaustion: $\eps_{B,N}\to0$ or positive floor;
\item prove regularized shadow angular-gap control: $\eps_{\rm Mell,N}+\tau_{M,N}+\kappa_{\rm tail,N}<1$ with adequate decay;
\item prove a matrix source lower-frame: $G_{\cX,N}\succeq\gamma_NH_N$ with $\gamma_N\to\infty$;
\item promote finite windows by fixed/exhaustive ledger tails.
\end{enumerate}

\section{No-smuggling record}
The parameters $Q_N,T_N,A_N,X_N,\omega_N$ must be selected by upstream carrier and source rules, not by observing which choices make the zero-confinement bound pass.  If a parameter is adjusted after seeing the target zero residual, it is a smuggled source record.

\section{Status}
The balanced-length gate is conditionally open whenever
\[
\exists \theta<\theta_*:
\quad
A_N(1+T_N)^AQ_N^{-\eta\theta}\to0.
\]
It is conditionally blocked if the Burnol atom complexity and vertical window grow too fast relative to the source conductor/height.

\end{document}
'''
(tex_path := out/'muntz_shadow_balanced_length_step123.tex').write_text(tex)

summary = r'''
# Step 123 — Balanced-Length Theorem

This step chooses growth regimes for the regularized Müntz/co-Poisson shadow length, the Burnol atom complexity, the vertical window, and the Hecke/Dirichlet source family.

The source route now has the form

\[
\gamma_N c_{\mathrm{hyb},N}\to\infty,
\]

with

\[
c_{\mathrm{hyb},N}\ge
1-(\epsilon_{B,N}+\epsilon_{\mathrm{Mell},N}+\tau_{M,N}+\kappa_{\mathrm{tail},N})^2.
\]

The new balance is between:

\[
\tau_{M,N}\lesssim A_N(1+T_N)^A X_N^{-\eta}
\]

and the source/moment shortness condition

\[
X_N\le Q_N^{\theta_*}.
\]

## Main criterion

Define

\[
\theta_{\min,N}
=
\frac{\log A_N+A\log(1+T_N)+r_N}{\eta\log Q_N}.
\]

The balanced-length cone is open when

\[
\boxed{\theta_{\min,N}<\theta_*}.
\]

Then one may choose

\[
X_N=Q_N^{\theta_N},
\qquad
\theta_{\min,N}<\theta_N<\theta_*.
\]

This gives

\[
A_N(1+T_N)^AX_N^{-\eta}\le e^{-r_N}.
\]

So if the other visibility defects vanish and \(r_N\to\infty\), then

\[
c_{\mathrm{hyb},N}\to1.
\]

If also

\[
G_{\mathcal X,N}\succeq\gamma_NH_N,
\qquad
\gamma_N\to\infty,
\]

then

\[
\boxed{\gamma_Nc_{\mathrm{hyb},N}\to\infty.}
\]

## Polynomial form

If

\[
A_N\ll Q_N^{\alpha},
\qquad
1+T_N\ll Q_N^{\beta},
\]

then the balance condition is

\[
\boxed{\alpha+A\beta<\eta\theta_*}.
\]

This is the clean growth-rate version of the gate.

## Positive floor version

The route does not require perfect visibility if source strength diverges.

If

\[
\limsup_N
(\epsilon_{B,N}+\epsilon_{\mathrm{Mell},N}+\tau_{M,N}+\kappa_{\mathrm{tail},N})
<1,
\]

then \(c_{\mathrm{hyb},N}\) has a positive floor. Any divergent \(\gamma_N\) then still gives effective source growth.

## Failure mode

If

\[
\liminf_N
\frac{\log A_N+A\log(1+T_N)}{\eta\log Q_N}
\ge\theta_*,
\]

then no choice of \(X_N\) can both:

1. be long enough for the Müntz shadow accuracy;
2. remain short enough for the available Heap–Soundararajan-style source estimates.

Then the route needs a stronger regularization, longer-polynomial moment technology, source absorption of the missed sector, or a scoped nonclaim.

## Interpretation

Step 123 shows that the Müntz regularization is not automatically fatal. It is viable whenever source height/conductor grows faster than the Burnol atom complexity and vertical window.

The active proof obligations become:

- Burnol/co-Poisson exhaustion: \(\epsilon_{B,N}\to0\) or a positive floor;
- regularized shadow angular-gap control;
- matrix Hecke/Dirichlet lower-frame growth \(\gamma_N\to\infty\);
- fixed/exhaustive tail promotion.
'''
(out/'step123_results_summary.md').write_text(summary)

rows = [
    ['Gate','Mathematical condition','Status after Step 123','Failure if absent'],
    ['Short-source admissibility','X_N <= Q_N^{theta_*}','parameterized, source-technology dependent','Mollifier/source moment estimates no longer apply'],
    ['Müntz accuracy','A_N(1+T_N)^A X_N^{-eta} -> 0','reduced to theta_min < theta_*','Dirichlet shadow remains unreadable/tail-dominated'],
    ['Balanced cone','theta_min,N < theta_*','main gate','no compatible length scale'],
    ['Positive visibility floor','epsilon_total < 1 eventually','sufficient with gamma_N -> infinity','visibility collapses despite source strength'],
    ['Source lower frame','G_X,N >= gamma_N H_N','external arithmetic input','scalar lower moments overread as matrix frame'],
    ['Tail promotion','fixed/exhaustive ledger tail -> 0','required','finite windows support-only'],
]
with open(out/'balanced_length_gate_table_step123.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

rows = [
    ['Object','Formula','Role'],
    ['source scale','Q_N','height/conductor/family size parameter'],
    ['vertical window','T_N','response window in critical-line or semilocal spectral coordinate'],
    ['atom complexity','A_N','uniform complexity of Burnol/co-Poisson atom family'],
    ['shadow length','X_N','regularized Dirichlet length in Muntz shadow'],
    ['source shortness exponent','theta_*','max length exponent for source estimates'],
    ['Muntz decay exponent','eta','contour shift decay exponent'],
    ['complexity exponent','A','vertical-window growth loss in contour estimate'],
    ['balance exponent','theta_min,N','minimum length exponent to control Muntz residual'],
    ['effective source strength','gamma_N c_hyb,N','quantity that must diverge'],
]
with open(out/'arithmetic_input_table_step123.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

rows = [
    ['Theorem','Statement','Depends on'],
    ['Balanced-length theorem','theta_min,N < theta_N < theta_* implies Muntz residual <= e^{-r_N}','Muntz contour estimate and source shortness bound'],
    ['Sub-polynomial corollary','log A_N + A log(1+T_N) = o(log Q_N) opens cone','growth separation'],
    ['Polynomial corollary','alpha + A beta < eta theta_*','polynomial scaling laws'],
    ['Positive-floor corollary','visibility error <1 and gamma_N -> infinity suffices','source divergence'],
    ['Failure theorem','theta_min >= theta_* blocks compatible length','no longer-polynomial source technology'],
]
with open(out/'theorem_map_step123.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

rows = [
    ['Route','Step 123 status','Next obligation'],
    ['Muntz shadow route','conditionally viable when balanced cone open','prove actual estimates for A_N,T_N,eta,A'],
    ['Burnol visibility','not addressed by length balance','prove epsilon_B,N -> 0 or positive floor'],
    ['Heap-Soundararajan source strength','length-constrained input','lift scalar estimates to matrix lower frame'],
    ['Hecke/Dirichlet source ladder','still load-bearing','prove gamma_N -> infinity on coefficient space'],
    ['Finite window evidence','support only','fixed/exhaustive tail promotion'],
]
with open(out/'route_status_step123.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

rows = [
    ['Task','Description','Priority'],
    ['Estimate A_N','Define Burnol atom complexity and prove growth relative to Q_N','high'],
    ['Estimate T_N','Tie vertical response window to source conductor/height','high'],
    ['Fix theta_*','Identify maximum admissible Dirichlet length for chosen source estimates','high'],
    ['Prove Muntz residual bound','Derive tau_M <= A_N(1+T_N)^A X_N^{-eta} in actual norm','high'],
    ['Lift source moments','Convert scalar lower moments into G_X,N >= gamma_N H_N','high'],
    ['Tail promotion','Build fixed/exhaustive residual ledger','high'],
]
with open(out/'construction_tasks_step123.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

nonclaim = r'''
# Step 123 nonclaim boundary

Step 123 does not prove RH.

It does not prove the Heap–Soundararajan operator-valued lower-frame lift.

It does not prove Burnol/co-Poisson exhaustion.

It does not prove the regularized shadow angular gap for the actual completed carrier.

It proves a conditional balancing theorem: if the Müntz contour residual has decay

\[
A_N(1+T_N)^A X_N^{-\eta},
\]

and if source estimates are valid up to length

\[
X_N\le Q_N^{\theta_*},
\]

then the compatibility gate is exactly

\[
\frac{\log A_N+A\log(1+T_N)}{\eta\log Q_N}<\theta_*.
\]

Any choice of \(X_N,T_N,Q_N,A_N\) made after seeing the zero residual is a smuggled parameter choice.

Finite-window success remains support-only unless there is fixed/exhaustive tail promotion.
'''
(out/'nonclaim_boundary_step123.md').write_text(nonclaim)

schema = {
    'step': 123,
    'title': 'Balanced-Length Theorem for the Regularized Co-Poisson/Müntz Shadow',
    'inputs': ['Q_N', 'T_N', 'A_N', 'theta_*', 'eta', 'A', 'gamma_N', 'epsilon_B,N', 'epsilon_Mell,N', 'kappa_tail,N'],
    'main_gate': 'theta_min,N < theta_*',
    'theta_min': '(log A_N + A log(1+T_N) + r_N)/(eta log Q_N)',
    'conclusion': 'If balanced cone is open and source strength diverges, gamma_N c_hyb,N -> infinity',
    'failure_mode': 'No compatible length if theta_min >= theta_* eventually',
    'next_step': 'Step 124: instantiate exponents for one source family and one Burnol atom growth model'
}
(out/'step123_schema.json').write_text(json.dumps(schema, indent=2))

# Generate data/plots
Ns = np.arange(10, 301)
Q = np.exp(Ns**0.9)  # abstract source scale
eta = 0.6
A_exp = 2.0
theta_star = 0.11 # reminiscent of a short-polynomial exponent, not asserted universal
r = np.log(Ns)
# scenarios (log A_N, log T_N)
scenarios = {
    'subpolynomial': (Ns**0.25, np.log(Ns)**2),
    'moderate polynomial': (0.015*np.log(Q), 0.015*np.log(Q)),
    'near boundary': (0.03*np.log(Q), 0.015*np.log(Q)),
    'blocked': (0.08*np.log(Q), 0.03*np.log(Q)),
}

scenario_rows=[]
for name,(logA,logT) in scenarios.items():
    theta_min = (logA + A_exp*np.log1p(np.exp(logT)) + r)/(eta*np.log(Q))
    # stable computation for log(1+T) = log(1+exp(logT))
    theta_min = (logA + A_exp*np.logaddexp(0, logT) + r)/(eta*np.log(Q))
    margin = theta_star-theta_min
    # choose theta midway if possible
    theta_choice = np.where(margin>0, theta_min + 0.5*margin, np.nan)
    tau_log = logA + A_exp*np.logaddexp(0, logT) - eta*theta_choice*np.log(Q)
    tau = np.where(margin>0, np.exp(np.minimum(tau_log,50)), np.nan)
    for i,N in enumerate(Ns):
        scenario_rows.append([int(N), name, float(theta_min[i]), float(margin[i]), float(theta_choice[i]) if margin[i]>0 else '', float(tau[i]) if margin[i]>0 else ''])
with open(out/'balanced_length_scenarios_step123.csv','w',newline='') as f:
    csv.writer(f).writerows([['N','scenario','theta_min','margin_to_theta_star','theta_choice','tau_proxy']]+scenario_rows)

plt.figure(figsize=(8,5))
for name,(logA,logT) in scenarios.items():
    theta_min = (logA + A_exp*np.logaddexp(0,logT) + r)/(eta*np.log(Q))
    plt.plot(Ns, theta_min, label=name)
plt.axhline(theta_star, linestyle='--', label='theta_*')
plt.xlabel('N')
plt.ylabel('minimum exponent theta_min')
plt.title('Balanced-length cone: theta_min < theta_*')
plt.legend()
plt.tight_layout()
plt.savefig(out/'balanced_length_cone_step123.png', dpi=160)
plt.close()

# visibility and source strength under scenarios
beta = 1.0
# gamma = (log Q)^beta
logQ = np.log(Q)
gamma = logQ**beta
vis_rows=[]
plt.figure(figsize=(8,5))
for name,(logA,logT) in scenarios.items():
    theta_min = (logA + A_exp*np.logaddexp(0,logT) + r)/(eta*np.log(Q))
    margin = theta_star-theta_min
    # Assume other errors = N^-0.2; tau = e^-r if cone open else 1
    other = Ns**(-0.2)
    total_err = np.where(margin>0, other + np.exp(-r), 1.0)
    c = np.maximum(0, 1-total_err**2)
    eff = gamma*c
    plt.plot(Ns, eff, label=name)
    for i,N in enumerate(Ns):
        if N in [10,25,50,100,200,300]:
            vis_rows.append([int(N), name, float(total_err[i]), float(c[i]), float(gamma[i]), float(eff[i])])
plt.xlabel('N')
plt.ylabel('effective source strength gamma_N c_N')
plt.title('Effective source strength under balanced-length scenarios')
plt.legend()
plt.tight_layout()
plt.savefig(out/'effective_source_strength_step123.png', dpi=160)
plt.close()
with open(out/'effective_source_strength_scenarios_step123.csv','w',newline='') as f:
    csv.writer(f).writerows([['N','scenario','visibility_error_proxy','c_lower_bound','gamma_proxy','effective_strength']]+vis_rows)

# Length choice chart for moderate scenario
name='moderate polynomial'
logA,logT = scenarios[name]
theta_min = (logA + A_exp*np.logaddexp(0,logT) + r)/(eta*np.log(Q))
margin = theta_star-theta_min
theta_choice=np.where(margin>0, theta_min+0.5*margin, np.nan)
X_log = theta_choice*logQ
plt.figure(figsize=(8,5))
plt.plot(Ns, theta_min, label='theta_min')
plt.plot(Ns, theta_choice, label='chosen theta')
plt.axhline(theta_star, linestyle='--', label='theta_*')
plt.xlabel('N')
plt.ylabel('exponent')
plt.title('Example admissible length choice')
plt.legend()
plt.tight_layout()
plt.savefig(out/'admissible_length_choice_step123.png', dpi=160)
plt.close()

# Failure plot: minimum residual at max length
fail_rows=[]
plt.figure(figsize=(8,5))
for name,(logA,logT) in scenarios.items():
    tau_best_log = logA + A_exp*np.logaddexp(0,logT) - eta*theta_star*logQ
    tau_best = np.exp(np.clip(tau_best_log, -20, 20))
    plt.plot(Ns, tau_best, label=name)
    for i,N in enumerate(Ns):
        if N in [10,50,100,200,300]:
            fail_rows.append([int(N), name, float(tau_best_log[i]), float(tau_best[i])])
plt.yscale('log')
plt.xlabel('N')
plt.ylabel('best possible Muntz residual proxy')
plt.title('Residual at maximal admissible length X=Q^{theta_*}')
plt.legend()
plt.tight_layout()
plt.savefig(out/'max_length_residual_step123.png', dpi=160)
plt.close()
with open(out/'max_length_residual_step123.csv','w',newline='') as f:
    csv.writer(f).writerows([['N','scenario','log_best_residual_proxy','best_residual_proxy']]+fail_rows)

# Finite angular gap toy sanity, carried from step concept
rng = np.random.default_rng(123)
rows=[]
for dim in [10,20,40,80]:
    # construct target subspace and approximating subspace with decreasing miss
    Hdim = 4*dim
    k = dim
    U,_ = np.linalg.qr(rng.normal(size=(Hdim,k)))
    noise_scale = dim**-0.35
    V,_ = np.linalg.qr(U + noise_scale*rng.normal(size=(Hdim,k)))
    PU = U@U.T
    PV = V@V.T
    delta = np.linalg.norm((np.eye(Hdim)-PV)@U,2)
    rows.append([dim, Hdim, float(noise_scale), float(delta), float(1-delta**2)])
with open(out/'finite_angular_gap_toy_step123.csv','w',newline='') as f:
    csv.writer(f).writerows([['target_dim','ambient_dim','noise_scale','delta','c_lower']]+rows)

plt.figure(figsize=(7,5))
plt.plot([r[0] for r in rows], [r[3] for r in rows], marker='o')
plt.xlabel('target dimension')
plt.ylabel('angular-gap defect delta')
plt.title('Toy angular-gap defect')
plt.tight_layout()
plt.savefig(out/'finite_angular_gap_toy_step123.png', dpi=160)
plt.close()

# write check script
check = r'''
from pathlib import Path
import re, csv, json
root = Path(__file__).resolve().parent
tex = (root/'muntz_shadow_balanced_length_step123.tex').read_text()
checks = []
checks.append(('has_balanced_length_theorem', 'Balanced-length theorem' in tex))
checks.append(('has_failure_theorem', 'Length incompatibility obstruction' in tex))
checks.append(('has_theta_min', '\\theta_{\\min,N}' in tex))
checks.append(('has_gamma_c_condition', '\\gamma_Nc_{{\\rm hyb},N}\\to\\infty' in tex))
# simple brace balance ignoring escaped braces is overkill; count raw braces
checks.append(('brace_balance', tex.count('{') == tex.count('}')))
checks.append(('begin_end_document', tex.count('\\begin{document}') == tex.count('\\end{document}') == 1))
with open(root/'latex_structure_check_step123.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['check','passed']); w.writerows(checks)
print(checks)
'''
(out/'run_balanced_length_checks_step123.py').write_text(check)

# Run check script
exec(open(out/'run_balanced_length_checks_step123.py').read(), {'__file__': str(out/'run_balanced_length_checks_step123.py')})

# Zip artifacts
zip_path = out/'step123_balanced_length_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name or p.name == 'generate_step123.py':
            continue
        z.write(p, arcname=p.name)
print('wrote', zip_path)
