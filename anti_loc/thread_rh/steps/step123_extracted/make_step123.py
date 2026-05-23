from pathlib import Path
import json, csv, math
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step123_balanced_length')
out.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Core scenario calculations
# -----------------------------
# Variables for the balanced-length model:
# M : source family size/conductor/time parameter
# V = M^nu : vertical window
# A = M^alpha : Burnol atom complexity
# R = M^rho : internal Burnol Mellin/Dirichlet length
# X_max = M^theta / R : maximum Müntz length allowed by source shortness
# tau = C A V^B X^{-eta}; at X=X_max, tau ~ M^{alpha+B*nu+eta*(rho-theta)}.

M_vals = np.logspace(2, 9, 220)
eta = 1.0
Bexp = 1.0
# scenario name, theta, alpha, nu, rho, eps_B, eps_Mell, kappa_tail, gamma_power_log
scenarios = [
    ('easy_floored_visibility', 0.45, 0.03, 0.03, 0.05, 0.05, 0.04, 0.03, 1.0),
    ('borderline_positive_floor', 0.28, 0.05, 0.06, 0.10, 0.12, 0.08, 0.06, 1.0),
    ('heap_short_length_strained', 1/9, 0.03, 0.04, 0.04, 0.09, 0.06, 0.05, 1.0),
    ('infeasible_long_shadow', 0.18, 0.08, 0.10, 0.12, 0.12, 0.10, 0.08, 1.0),
]

rows=[]
for name,theta,alpha,nu,rho,epsB,epsM,kappa,gpow in scenarios:
    tau = M_vals**(alpha+Bexp*nu+eta*(rho-theta))
    # normalize tau to be in a visible range at M=1e2 for plots
    tau = 0.18 * tau / tau[0]
    total_err = epsB + epsM + kappa + tau
    c_lower = np.maximum(0, 1 - total_err**2)
    gamma = np.maximum(1, np.log(M_vals))**gpow
    Lambda = gamma * c_lower
    feasible_vanish = alpha+Bexp*nu+eta*rho < eta*theta
    positive_floor = np.nanmin(total_err[-40:]) < 0.95 and np.nanmax(total_err[-40:]) < 1.0
    rows.append({
        'scenario': name,
        'theta_shortness': theta,
        'alpha_atom_complexity': alpha,
        'nu_vertical_window': nu,
        'rho_internal_length': rho,
        'eta_contour_decay': eta,
        'A_contour_T_exponent': Bexp,
        'balance_exponent_alpha_A_nu_eta_rho_minus_eta_theta': alpha+Bexp*nu+eta*rho-eta*theta,
        'vanishing_muntz_error_possible': feasible_vanish,
        'terminal_total_error_proxy': float(total_err[-1]),
        'terminal_visibility_lower_bound': float(c_lower[-1]),
        'terminal_effective_source_strength_proxy': float(Lambda[-1]),
    })

with open(out/'balanced_length_scenarios_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# Data tables for plots
plot_rows=[]
for name,theta,alpha,nu,rho,epsB,epsM,kappa,gpow in scenarios:
    tau = M_vals**(alpha+Bexp*nu+eta*(rho-theta))
    tau = 0.18 * tau / tau[0]
    total_err = epsB + epsM + kappa + tau
    c_lower = np.maximum(0, 1-total_err**2)
    gamma = np.maximum(1, np.log(M_vals))**gpow
    Lambda = gamma*c_lower
    for M,t,e,c,Lam in zip(M_vals,tau,total_err,c_lower,Lambda):
        plot_rows.append({'scenario':name,'M':M,'muntz_error_proxy':t,'total_error_proxy':e,'visibility_lower_bound':c,'effective_source_strength_proxy':Lam})
with open(out/'balanced_length_plot_data_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['scenario','M','muntz_error_proxy','total_error_proxy','visibility_lower_bound','effective_source_strength_proxy'])
    w.writeheader(); w.writerows(plot_rows)

# Plots
plt.figure(figsize=(8,5))
for name,theta,alpha,nu,rho,epsB,epsM,kappa,gpow in scenarios:
    exponent = alpha+Bexp*nu+eta*rho-eta*theta
    tau = M_vals**exponent
    tau = 0.18*tau/tau[0]
    plt.loglog(M_vals, tau, label=name)
plt.axhline(1, linestyle='--')
plt.xlabel('source scale M')
plt.ylabel('Müntz error proxy at max admissible length')
plt.title('Step 123: balanced-length error under source shortness')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'balanced_length_error_step123.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name,theta,alpha,nu,rho,epsB,epsM,kappa,gpow in scenarios:
    tau = M_vals**(alpha+Bexp*nu+eta*(rho-theta))
    tau = 0.18*tau/tau[0]
    total_err = epsB+epsM+kappa+tau
    c_lower=np.maximum(0,1-total_err**2)
    plt.semilogx(M_vals,c_lower,label=name)
plt.xlabel('source scale M')
plt.ylabel('lower bound for c_hyb')
plt.title('Step 123: visibility floor after length balancing')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'visibility_floor_step123.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name,theta,alpha,nu,rho,epsB,epsM,kappa,gpow in scenarios:
    tau = M_vals**(alpha+Bexp*nu+eta*(rho-theta))
    tau = 0.18*tau/tau[0]
    total_err = epsB+epsM+kappa+tau
    c_lower=np.maximum(0,1-total_err**2)
    gamma=np.maximum(1,np.log(M_vals))**gpow
    Lambda=gamma*c_lower
    plt.semilogx(M_vals,Lambda,label=name)
plt.xlabel('source scale M')
plt.ylabel('effective source strength proxy gamma_N c_N')
plt.title('Step 123: effective source strength after visibility loss')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'effective_source_strength_step123.png', dpi=180)
plt.close()

# Feasibility cone plot: x-axis rho+alpha, y-axis theta; feasible if theta > alpha+nu+rho (eta=B=1)
alpha_grid=np.linspace(0,0.25,120)
theta_grid=np.linspace(0,0.5,120)
Agrid,Tgrid=np.meshgrid(alpha_grid,theta_grid)
# fix nu=0.05, rho encoded in alpha_grid label? Let's set x=alpha+nu+rho.
feasible=Tgrid>Agrid
plt.figure(figsize=(7,5))
plt.contourf(alpha_grid,theta_grid,feasible,levels=[-0.5,0.5,1.5],alpha=0.55)
plt.plot(alpha_grid,alpha_grid, linestyle='--')
plt.xlabel('aggregate shadow-growth exponent (alpha + A nu + rho)')
plt.ylabel('available source-shortness exponent theta')
plt.title('Step 123: feasibility cone for vanishing Müntz error')
plt.tight_layout()
plt.savefig(out/'feasibility_cone_step123.png', dpi=180)
plt.close()

# Theorem/gate tables
ble_rows=[
    {'gate':'G1_muntz_accuracy','statement':'tau_M,N(X_N) <= C A_N (1+V_N)^A X_N^{-eta}','accepted_if':'contour shift, cutoff Mellin decay, and atom-complexity record are proved uniformly on Burnol windows','failure_status':'regularization_tail_defect'},
    {'gate':'G2_source_shortness','statement':'X_N R_N <= M_N^theta','accepted_if':'the chosen source/moment technology is valid for Dirichlet length X_N R_N','failure_status':'source_estimate_not_applicable'},
    {'gate':'G3_length_overlap','statement':'X_req(N) <= X_max(N)','accepted_if':'there exists a length X_N satisfying both G1 and G2','failure_status':'balanced_length_obstruction'},
    {'gate':'G4_visibility_floor','statement':'epsilon_B,N + epsilon_Mell,N + tau_M,N + kappa_tail,N < 1','accepted_if':'c_hyb,N >= 1-total_error^2 is positive','failure_status':'missed_shadow_sector'},
    {'gate':'G5_effective_source_growth','statement':'gamma_N c_hyb,N -> infinity','accepted_if':'source strength beats visibility loss','failure_status':'no_budget_collapse'},
    {'gate':'G6_fixed_exhaustive_tail','statement':'finite windows promote to completed residual ledger','accepted_if':'tail trace/Plancherel/exhaustivity record vanishes','failure_status':'moving_window_support_only'},
    {'gate':'G7_no_smuggling','statement':'omega, X_N rule, atom family, source family, weights declared upstream','accepted_if':'no target-selected cutoffs or zero-dependent source choices','failure_status':'smuggled_source'},
]
with open(out/'balanced_length_gate_table_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(ble_rows[0].keys()))
    w.writeheader(); w.writerows(ble_rows)

theorem_rows=[
    {'name':'Muntz shadow error lemma','inputs':'smooth cutoff omega; vertical window V_N; atom complexity A_N; cutoff length X_N','conclusion':'tau_M,N <= C A_N (1+V_N)^A X_N^{-eta}','status':'conditional analytic estimate'},
    {'name':'Balanced length theorem','inputs':'X_req from error budget; X_max=M_N^theta/R_N from source shortness','conclusion':'length exists iff X_req <= X_max','status':'proved algebraically'},
    {'name':'Polynomial exponent corollary','inputs':'A_N~M^alpha, V_N~M^nu, R_N~M^rho','conclusion':'vanishing shadow possible if (alpha+A nu)/eta + rho < theta','status':'proved asymptotic criterion'},
    {'name':'Positive visibility floor theorem','inputs':'total regularized shadow error E_N<1','conclusion':'c_hyb,N >= 1-E_N^2>0','status':'proved from angular-gap identity'},
    {'name':'Effective source criterion','inputs':'G_X,N >= gamma_N H_N and c_hyb,N visibility','conclusion':'Lambda_N >= gamma_N c_hyb,N; budget collapse requires gamma_N c_hyb,N -> infinity','status':'conditional source-frame theorem'},
]
with open(out/'theorem_map_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(theorem_rows[0].keys()))
    w.writeheader(); w.writerows(theorem_rows)

arithmetic_rows=[
    {'input':'Uniform Müntz contour bound','needed_for':'tau_M,N <= C A_N(1+V_N)^A X_N^{-eta}','likely_source':'Burnol/Müntz/co-Poisson plus cutoff Mellin decay','risk':'growth in V_N or atom complexity can force X_N too long'},
    {'input':'Short-polynomial moment validity','needed_for':'source Gram lower bound gamma_N for length X_N R_N','likely_source':'Heap--Soundararajan dual mollifier or character-family analogue','risk':'available theta may be too small'},
    {'input':'Burnol geometric exhaustion','needed_for':'epsilon_B,N -> 0 or positive floor','likely_source':'Burnol Sonine/co-Poisson completeness/minimality','risk':'boundary sector may have residual outside declared atom span'},
    {'input':'Regularized shadow completeness','needed_for':'delta_BD,N^reg -> 0 or positive floor','likely_source':'smooth Müntz/co-Poisson shadow / approximate functional equation','risk':'angular gap on growing windows may fail despite pointwise convergence'},
    {'input':'Completed tail promotion','needed_for':'finite-window source frame to completed residual ledger','likely_source':'Plancherel/exhaustivity record on semilocal or Hecke carrier','risk':'moving-window support-only evidence'},
]
with open(out/'arithmetic_input_table_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(arithmetic_rows[0].keys()))
    w.writeheader(); w.writerows(arithmetic_rows)

route_rows=[
    {'case':'vanishing_shadow_feasible','conditions':'length overlap with total error -> 0 and gamma_N -> infinity','status':'source route viable after tail promotion'},
    {'case':'positive_floor_only','conditions':'length overlap gives total error <= e < 1 and gamma_N -> infinity','status':'viable if gamma_N c_floor -> infinity; no need delta->0'},
    {'case':'shortness_failure','conditions':'X_req > X_max','status':'Heap--Soundararajan-style source cannot read the regularized shadow at required accuracy'},
    {'case':'visibility_collapse','conditions':'total error approaches >=1','status':'missed shadow residual Xi_BD^reg must be separately source-absorbed or scoped out'},
    {'case':'tail_failure','conditions':'finite windows improve but no completed tail','status':'moving_window_support_only'},
]
with open(out/'route_status_step123.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(route_rows[0].keys()))
    w.writeheader(); w.writerows(route_rows)

nonclaim = '''# Step 123 nonclaim boundary

This step does not prove RH.

It does not prove the Burnol-to-Dirichlet angular gap, the Heap--Soundararajan operator-valued lower frame, or completed tail promotion.

It proves the balanced-length criterion that any such route must satisfy:

- the Müntz/co-Poisson shadow length must be long enough for regularized accuracy;
- the same Dirichlet length must remain short enough for the source moment technology;
- the resulting visibility floor must not collapse;
- source strength must beat any residual visibility loss;
- finite windows must promote through a fixed/exhaustive ledger.

A failure of the length overlap is not a proof of RH failure. It says that this particular regularized-shadow + short-source route is underpowered and must be repaired by longer moment technology, a different regularization, a Hecke/idèle carrier source frame, or an explicit residual/nonclaim record.
'''
(out/'nonclaim_boundary_step123.md').write_text(nonclaim)

summary = '''# Step 123 summary: Balanced-length theorem

Step 123 studies whether the smooth Müntz/co-Poisson shadow can be accurate while remaining short enough for Heap--Soundararajan-style source estimates.

The active error is

    E_N = epsilon_B,N + epsilon_Mell,N + tau_M,N + kappa_tail,N.

The Müntz contour estimate has the form

    tau_M,N(X_N) <= C A_N (1+V_N)^A X_N^{-eta}.

The source shortness constraint has the form

    X_N R_N <= M_N^theta.

Thus an admissible length exists iff

    [C A_N (1+V_N)^A / e_N]^{1/eta} <= M_N^theta / R_N.

Equivalently, in polynomial exponent form with A_N~M^alpha, V_N~M^nu, R_N~M^rho,

    (alpha + A nu)/eta + rho < theta

is sufficient for vanishing Müntz error while preserving source shortness.

A weaker positive-floor route only requires total error < 1, because

    c_hyb,N >= 1 - E_N^2.

The effective source strength is

    Lambda_N >= gamma_N c_hyb,N.

The route closes only if Lambda_N -> infinity after fixed/exhaustive tail promotion.
'''
(out/'step123_results_summary.md').write_text(summary)

schema = {
    'step': 123,
    'title': 'Balanced-length theorem for regularized co-Poisson/Müntz shadow and source shortness',
    'objects': {
        'V_N': 'vertical/semilocal response window',
        'A_N': 'Burnol atom complexity budget',
        'X_N': 'Müntz regularization cutoff length',
        'R_N': 'internal Burnol-to-Dirichlet coefficient length',
        'M_N': 'source family size/conductor/time parameter',
        'theta': 'admissible short Dirichlet length exponent for source estimates',
        'gamma_N': 'arithmetic source lower-frame strength',
        'c_hyb_N': 'hybrid visibility lower bound',
        'Lambda_N': 'effective residual source strength gamma_N c_hyb_N'
    },
    'main_inequalities': [
        'tau_M,N <= C A_N (1+V_N)^A X_N^{-eta}',
        'X_N R_N <= M_N^theta',
        'X_req <= X_max',
        'c_hyb,N >= 1 - E_N^2',
        'Lambda_N >= gamma_N c_hyb,N'
    ],
    'acceptance_status': 'conditional routing theorem; analytic estimates and source frame remain open',
    'next_step': 'Step 124: quantify theta and gamma_N for concrete source families'
}
(out/'step123_schema.json').write_text(json.dumps(schema, indent=2))

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,enumitem,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}
\title{Step 123: Balanced-Length Theorem for the Regularized Co-Poisson/M\"untz Shadow}
\author{RATCHET RH Membrane Notes}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Step 122 made the Burnol-to-Dirichlet shadow lawful by replacing naive critical-line partial sums with a smooth M\"untz/co-Poisson shadow.  Step 123 asks whether this lawful shadow can be made accurate while remaining short enough for the source moment technology.

The central issue is a length conflict:
\[
\text{M\"untz accuracy wants } X_N \text{ large},
\qquad
\text{Heap--Soundararajan source estimates want } X_N R_N \text{ short}.
\]

\section{Data}
Let
\begin{itemize}[leftmargin=2em]
\item $V_N$ be the vertical/semilocal response window;
\item $A_N$ be the uniform complexity of the Burnol atom family on this window;
\item $R_N$ be the internal Dirichlet/Mellin length needed to model the Burnol atoms;
\item $X_N$ be the smooth M\"untz cutoff length;
\item $M_N$ be the source-family size, conductor, or time parameter;
\item $\theta>0$ be the admissible shortness exponent for the chosen source estimates;
\item $\gamma_N$ be the coefficient-space source lower-frame strength.
\end{itemize}

The regularized shadow error from Step 122 has the form
\[
E_N(X_N)=\epsilon_{B,N}+\epsilon_{{\rm Mell},N}+\tau_{{\rm M},N}(X_N)+\kappa_{{\rm tail},N}.
\]
The visibility bound is
\[
 c_{{\rm hyb},N}\ge 1-E_N(X_N)^2.
\]

\section{M\"untz accuracy and source shortness}
\begin{lemma}[M\"untz contour estimate]
Assume the smooth cutoff admits a contour shift to $\Re w=-\eta<0$ and the Burnol atoms satisfy the uniform complexity bound $A_N$ on $|\Im s|\le V_N$.  Then
\[
\tau_{{\rm M},N}(X_N)
\le
C_\omega A_N(1+V_N)^{A_\omega}X_N^{-\eta}.
\]
\end{lemma}

\begin{definition}[Source shortness]
The regularized shadow is source-admissible if
\[
X_N R_N\le M_N^\theta.
\]
Here $R_N$ accounts for the internal Burnol-to-Dirichlet coefficient length, and $X_N$ for the zeta/M\"untz convolution length.
\end{definition}

\section{Balanced-length theorem}
Fix an error budget $0<e_N<1$ for the M\"untz part after the non-M\"untz defects have been reserved.  Define
\[
X_{\rm req}(N)
=
\left(\frac{C_\omega A_N(1+V_N)^{A_\omega}}{e_N}\right)^{1/\eta},
\qquad
X_{\rm max}(N)=\frac{M_N^\theta}{R_N}.
\]

\begin{theorem}[Balanced-length criterion]
There exists a choice of $X_N$ satisfying both
\[
\tau_{{\rm M},N}(X_N)\le e_N
\]
and the source shortness condition
\[
X_NR_N\le M_N^\theta
\]
if and only if
\[
\boxed{X_{\rm req}(N)\le X_{\rm max}(N).}
\]
Equivalently,
\[
\boxed{
C_\omega A_N(1+V_N)^{A_\omega}
\left(\frac{R_N}{M_N^\theta}\right)^\eta
\le e_N.
}
\]
\end{theorem}

\begin{corollary}[Polynomial exponent version]
Assume
\[
A_N\asymp M_N^\alpha,
\qquad
V_N\asymp M_N^\nu,
\qquad
R_N\asymp M_N^\rho.
\]
Then a vanishing M\"untz error is compatible with source shortness whenever
\[
\boxed{
\frac{\alpha+A_\omega\nu}{\eta}+\rho<\theta.
}
\]
If the inequality is replaced by a non-strict bounded version, one may still obtain a positive visibility floor, but not necessarily $\delta_{BD,N}^{\rm reg}\to0$.
\end{corollary}

\section{Effective source strength}
Suppose the source Gram satisfies
\[
G_{\mathcal X,N}\succeq \gamma_N H_N.
\]
If the regularized hybrid visibility obeys
\[
R_N^*H_NR_N\succeq c_{{\rm hyb},N}G_{R,N},
\]
then
\[
R_N^*G_{\mathcal X,N}R_N
\succeq
\gamma_Nc_{{\rm hyb},N}G_{R,N}.
\]
Thus the effective source strength is
\[
\boxed{\Lambda_{R,N}=\gamma_Nc_{{\rm hyb},N}.}
\]
A completed residual membrane requires
\[
\boxed{\gamma_Nc_{{\rm hyb},N}\to\infty}
\]
plus fixed/exhaustive tail promotion.

\section{Route trichotomy}
\begin{enumerate}[leftmargin=2em]
\item \textbf{Vanishing shadow.} If $X_{\rm req}\le X_{\rm max}$ with $e_N\to0$, then the regularized Burnol-to-Dirichlet shadow can be complete in principle.
\item \textbf{Positive floor.} If the total error is bounded by $E_N\le e<1$, then $c_{{\rm hyb},N}\ge 1-e^2>0$.  This may still suffice if $\gamma_N\to\infty$.
\item \textbf{Missed shadow.} If the error reaches $1$, the limiting residual $\Xi_{BD}^{\rm reg}$ must be separately source-absorbed, tail-paid, or scoped out.
\end{enumerate}

\section{Nonclaim}
This step does not prove RH and does not prove the Burnol-to-Dirichlet angular gap.  It proves the length-compatibility criterion that any regularized-shadow plus short-source route must satisfy.

\end{document}
'''
(out/'muntz_shadow_balanced_length_step123.tex').write_text(tex)

# script copy to reproduce core plots
script = Path(__file__).read_text()
(out/'run_balanced_length_step123.py').write_text(script)

# zip artifacts
import zipfile
zip_path = out/'step123_balanced_length_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name:
            continue
        z.write(p, arcname=p.name)
print('created', out)
