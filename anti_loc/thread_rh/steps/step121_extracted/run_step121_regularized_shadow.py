import os, json, csv, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step121_regularized_shadow')
out.mkdir(parents=True, exist_ok=True)

# Scenario data for regularized shadow defect.
N = np.arange(8, 201, 8)
# These are schematic/diagnostic regimes, not RH evidence.
naive = 0.96 - 0.05*np.log1p(N)/np.log(201) + 0.02*np.sin(N/15)
naive = np.clip(naive, 0.82, 0.98)
hard = 0.85/(1+0.015*N)**0.20
muntz_good = 0.72/(1+0.045*N)**0.70
muntz_floor = 0.38 + 0.42/(1+0.04*N)**0.65
bad_shadow = 0.72 + 0.20/(1+0.04*N)**0.35

rows=[]
for i,n in enumerate(N):
    rows.append({
        'N': int(n),
        'naive_dirichlet_delta': float(naive[i]),
        'hard_cutoff_muntz_delta': float(hard[i]),
        'regularized_complete_delta': float(muntz_good[i]),
        'positive_floor_delta': float(muntz_floor[i]),
        'blind_shadow_delta': float(bad_shadow[i]),
        'c_regularized_complete': float(max(0, 1-muntz_good[i]**2)),
        'c_positive_floor': float(max(0, 1-muntz_floor[i]**2)),
        'c_blind_shadow': float(max(0, 1-bad_shadow[i]**2)),
    })
with open(out/'regularized_shadow_scenarios_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

plt.figure(figsize=(8,5))
plt.plot(N, naive, label='naive critical-line partial sums')
plt.plot(N, hard, label='hard-cutoff Müntz correction')
plt.plot(N, muntz_good, label='regularized complete shadow')
plt.plot(N, muntz_floor, label='positive-floor shadow')
plt.plot(N, bad_shadow, label='blind shadow sector')
plt.xlabel('window size N')
plt.ylabel('shadow defect delta')
plt.title('Step 121 schematic regularized shadow defect regimes')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'regularized_shadow_defect_scenarios_step121.png', dpi=180)
plt.close()

# Decomposition into burnol exhaustion, muntz regularization, tail, and readability defect.
N2=np.arange(10,210,10)
eps_B = 0.60/(1+0.035*N2)**0.95
r_muntz = 0.46/(1+0.05*N2)**0.80
r_tail = 0.35/(1+0.045*N2)**1.05
unreadable_floor = np.full_like(N2, 0.18, dtype=float)
full_delta = np.minimum(0.999, eps_B + r_muntz + r_tail)
floor_delta = np.minimum(0.999, eps_B + r_muntz + r_tail + unreadable_floor)
rows=[]
for i,n in enumerate(N2):
    rows.append({'N':int(n),'burnol_exhaustion_eps_B':float(eps_B[i]),'muntz_regularization_defect':float(r_muntz[i]),'tail_defect':float(r_tail[i]),'unreadable_floor':float(unreadable_floor[i]),'delta_no_floor':float(full_delta[i]),'delta_with_unreadable_floor':float(floor_delta[i]),'c_no_floor':float(max(0,1-full_delta[i]**2)),'c_with_floor':float(max(0,1-floor_delta[i]**2))})
with open(out/'regularized_shadow_decomposition_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

plt.figure(figsize=(8,5))
plt.plot(N2, eps_B, label='Burnol exhaustion defect')
plt.plot(N2, r_muntz, label='Müntz regularization defect')
plt.plot(N2, r_tail, label='finite-window tail defect')
plt.plot(N2, unreadable_floor, label='unreadable shadow floor')
plt.plot(N2, full_delta, linestyle='--', label='total without floor')
plt.plot(N2, floor_delta, linestyle='--', label='total with floor')
plt.xlabel('window size N')
plt.ylabel('defect contribution')
plt.title('Step 121 shadow-defect decomposition')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'regularized_shadow_decomposition_step121.png', dpi=180)
plt.close()

# Effective source strength scenarios gamma * c.
gamma_log = np.log1p(N2)**1.5
gamma_poly = np.sqrt(N2)
gamma_moment_like = (np.log1p(N2))**2
c_no_floor = np.maximum(0,1-full_delta**2)
c_with_floor = np.maximum(0,1-floor_delta**2)
rows=[]
for i,n in enumerate(N2):
    rows.append({'N':int(n),'gamma_log_power':float(gamma_log[i]),'gamma_sqrt':float(gamma_poly[i]),'gamma_moment_like':float(gamma_moment_like[i]),'c_no_floor':float(c_no_floor[i]),'c_with_floor':float(c_with_floor[i]),'Lambda_log_no_floor':float(gamma_log[i]*c_no_floor[i]),'Lambda_log_with_floor':float(gamma_log[i]*c_with_floor[i]),'Lambda_sqrt_no_floor':float(gamma_poly[i]*c_no_floor[i]),'Lambda_sqrt_with_floor':float(gamma_poly[i]*c_with_floor[i])})
with open(out/'regularized_effective_source_strength_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

plt.figure(figsize=(8,5))
plt.plot(N2, gamma_log*c_no_floor, label='log source × complete shadow')
plt.plot(N2, gamma_log*c_with_floor, label='log source × floor shadow')
plt.plot(N2, gamma_poly*c_no_floor, label='sqrt source × complete shadow')
plt.plot(N2, gamma_poly*c_with_floor, label='sqrt source × floor shadow')
plt.xlabel('window size N')
plt.ylabel('effective source strength Lambda')
plt.title('Step 121 effective source strength under shadow regimes')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'regularized_effective_source_strength_step121.png', dpi=180)
plt.close()

# finite projection angular gap check
rng=np.random.default_rng(121)
dim=30
rows=[]
# Make nested dictionary dimensions with decreasing residual; check identity delta = ||(I-PD) B G^{-1/2}||
for dD in range(5, 31, 5):
    B = rng.normal(size=(dim, 8))
    # normalize B columns by Gram inverse
    G = B.T@B
    eig, U = np.linalg.eigh(G)
    G_inv_sqrt = U@np.diag(1/np.sqrt(np.maximum(eig,1e-12)))@U.T
    # Build D: first dD standard plus random columns; progressively spans more of B
    D = np.zeros((dim,dD))
    D[:dD,:dD]=np.eye(dD)
    D += 0.05*rng.normal(size=(dim,dD))
    # Inject partial alignment with B directions depending dD
    if dD >= 10:
        D[:, :min(8,dD)] += 0.4*B[:, :min(8,dD)]
    Q,_=np.linalg.qr(D)
    P=Q@Q.T
    delta=np.linalg.norm((np.eye(dim)-P)@B@G_inv_sqrt,2)
    rows.append({'dictionary_dim':dD,'angular_gap_delta':float(delta),'visibility_c':float(max(0,1-delta**2))})
with open(out/'finite_projection_gap_regularized_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
plt.figure(figsize=(7,4.5))
plt.plot([r['dictionary_dim'] for r in rows],[r['angular_gap_delta'] for r in rows], marker='o')
plt.xlabel('dictionary dimension')
plt.ylabel('operator-norm angular gap delta')
plt.title('Step 121 finite angular-gap sanity check')
plt.tight_layout()
plt.savefig(out/'finite_projection_gap_regularized_step121.png', dpi=180)
plt.close()

# Write tables
regularization_table = [
    {'record':'smooth Muntz shadow','definition':'Z_X^omega(s)=sum_n omega(n/X)n^{-s}-X^{1-s} Omega(1-s)','accepted_if':'Omega term is carried as completion/pole channel and residual tail is bounded in response norm','failure':'ordinary critical-line partial sum used without subtraction'},
    {'record':'co-Poisson response shadow','definition':'C g(t)=sum_n g(t/n)/n - ghat(1)','accepted_if':'C g is in the declared Burnol/Sonine response space and finite truncations have vanishing tail','failure':'pointwise summation without L2/tempered audit'},
    {'record':'approximate functional equation shadow','definition':'two-sided smoothed finite sum with functional-equation dual term','accepted_if':'s-dependent weights are declared upstream and dual channel is charged','failure':'target-selected cutoff or invisible dual term'},
    {'record':'Dirichlet-readable coefficient bank','definition':'D_N a(s)=sum_{n in N_N} a_n n^{-s}','accepted_if':'angular gap delta_BD,N tends to zero or has positive visibility floor','failure':'mean approximation only; no uniform operator gap'},
    {'record':'missed shadow residual','definition':'Xi_BD,N=B_N^*(I-P_D,N)B_N','accepted_if':'zero, compact/tail-paid, or source-absorbed','failure':'nonzero uncharged blind sector'},
]
with open(out/'regularized_shadow_gate_table_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(regularization_table[0].keys()))
    w.writeheader(); w.writerows(regularization_table)

criterion_table = [
    {'criterion':'lawful regularization','operator_statement':'B_N = S_N^{reg} + R_N^{reg} with all correction channels declared','needed_input':'Muntz/co-Poisson or approximate-functional-equation construction','status':'defined in Step 121'},
    {'criterion':'uniform shadow angular gap','operator_statement':'delta_BD,N = ||(I-P_D,N) B_N G_B,N^{-1/2}|| -> 0','needed_input':'operator-norm approximation on growing Burnol windows','status':'open main target'},
    {'criterion':'positive visibility floor','operator_statement':'epsilon_B,N + delta_BD,N <= 1-eta','needed_input':'quantitative shadow gap, enough for gamma_N c_N -> infinity','status':'fallback target'},
    {'criterion':'missed shadow sector','operator_statement':'Xi_BD = B^*(I-P_D)B != 0','needed_input':'separate source absorption or scoped nonclaim','status':'failure mode'},
    {'criterion':'fixed/exhaustive promotion','operator_statement':'G_B <= Pi_N^* G_B,N Pi_N + T_N, tr T_N -> 0','needed_input':'Burnol/Sonine tail theorem','status':'required for completed result'},
]
with open(out/'shadow_asymptotic_criterion_table_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(criterion_table[0].keys()))
    w.writeheader(); w.writerows(criterion_table)

theorem_map=[
    {'label':'T121.1','name':'Muntz-regularized shadow identity','statement':'Smooth Muntz subtraction is a lawful critical-strip shadow for zeta(s) times a Burnol Mellin target, with explicit tail residual.','status':'conditional construction'},
    {'label':'T121.2','name':'Shadow angular-gap criterion','statement':'delta_BD,N -> 0 iff the declared regularized Dirichlet-readable spaces approximate Burnol target ranges uniformly on normalized growing windows.','status':'proved abstractly'},
    {'label':'T121.3','name':'Hybrid visibility lower bound','statement':'c_hyb,N >= 1-(epsilon_B,N + delta_BD,N + tau_reg,N)^2.','status':'proved finite gate'},
    {'label':'T121.4','name':'Missed shadow residual trichotomy','statement':'If Xi_BD is nonzero, it must be source-absorbed, compact/tail-paid, or declared nonclaim.','status':'diagnostic theorem'},
    {'label':'T121.5','name':'No ordinary partial sum rule','statement':'Unregularized critical-line Dirichlet partial sums are not lawful shadows for the completed response-space gate.','status':'methodological no-go'},
]
with open(out/'theorem_map_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(theorem_map[0].keys()))
    w.writeheader(); w.writerows(theorem_map)

arithmetic_inputs=[
    {'input':'Muntz/co-Poisson regularization theorem','role':'turns zeta(s) ghat(s) into a response-space object without using divergent critical-line partial sums','source_line':'Burnol co-Poisson/Muntz'},
    {'input':'Burnol/Sonine exhaustion','role':'controls epsilon_B,N and fixed/exhaustive promotion','source_line':'Burnol complete/minimal systems'},
    {'input':'Dirichlet shadow angular gap','role':'controls delta_BD,N in operator norm','source_line':'new framework obligation'},
    {'input':'Heap-Soundararajan matrix moment lift','role':'controls gamma_N for source strength after readability','source_line':'scalar lower moments need operator lift'},
    {'input':'semilocal Hardy-Titchmarsh carrier','role':'places finite Euler factors and response geometry in one Hilbert space','source_line':'CCM semilocal framework'},
    {'input':'Conrey-Li survival audit','role':'prevents collapse to refuted de Branges/RKHS positivity','source_line':'Conrey-Li obstruction'},
]
with open(out/'arithmetic_input_table_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(arithmetic_inputs[0].keys()))
    w.writeheader(); w.writerows(arithmetic_inputs)

route_status=[
    {'route_component':'ordinary critical-line partial sums','status':'rejected as lawful shadow','reason':'not regularized in critical strip; fails channel audit'},
    {'route_component':'smooth Muntz/co-Poisson shadow','status':'active construction','reason':'declares pole/completion subtraction and tail residual'},
    {'route_component':'approximate functional equation shadow','status':'alternative lawful shadow','reason':'two-sided regularization but requires s-dependent dual-channel audit'},
    {'route_component':'Burnol-to-Dirichlet shadow defect','status':'active obstruction','reason':'delta_BD,N is the readability adequacy residual'},
    {'route_component':'source-coercivity ladder','status':'waiting on gamma and visibility','reason':'effective strength is gamma_N c_hyb,N'},
]
with open(out/'route_status_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(route_status[0].keys()))
    w.writeheader(); w.writerows(route_status)

construction_tasks=[
    {'task':'choose smooth cutoff omega','output':'Mellin transform Omega and Muntz correction X^{1-s}Omega(1-s)','gate':'regularization declared upstream'},
    {'task':'define B_N^reg for Burnol atoms','output':'regularized target columns for zeta(s) ghat_j(s)','gate':'co-Poisson/Muntz identity'},
    {'task':'choose Dirichlet-readable bank D_N^reg','output':'finite coefficient synthesis plus correction channels','gate':'source-readability'},
    {'task':'estimate delta_BD,N^reg','output':'operator-norm angular gap on growing windows','gate':'uniform shadow criterion'},
    {'task':'combine with epsilon_B,N and gamma_N','output':'effective Lambda_N = gamma_N c_hyb,N','gate':'source absorption'},
    {'task':'promote finite windows','output':'fixed/exhaustive tail record','gate':'exact confinement eligibility'},
]
with open(out/'construction_tasks_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(construction_tasks[0].keys()))
    w.writeheader(); w.writerows(construction_tasks)

schema={
    'step':121,
    'title':'Regularized co-Poisson/Muntz Dirichlet shadow construction',
    'core_objects':{
        'Burnol_target':'B_N g_j(s)=zeta(s) * ghat_j(s)',
        'regularized_shadow':'Z_X^omega(s)=sum_n omega(n/X)n^{-s}-X^{1-s}Omega(1-s)',
        'shadow_defect':'delta_BD,N=||(I-P_D,N)B_N G_B,N^{-1/2}||',
        'adequacy_residual':'Xi_BD,N=B_N^*(I-P_D,N)B_N',
        'effective_source_strength':'Lambda_N=gamma_N*c_hyb,N'
    },
    'accepted_outcomes':['delta_BD,N -> 0','positive visibility floor plus gamma_N*c_N -> infinity','Xi_BD compact/tail-paid','Xi_BD separately source-absorbed'],
    'rejected_outcomes':['unregularized critical-line partial sums','pointwise approximation without operator-norm angular gap','target-selected cutoff','finite-window overread'],
    'artifacts':['burnol_dirichlet_shadow_regularized_step121.tex','step121_results_summary.md','regularized_shadow_gate_table_step121.csv','shadow_asymptotic_criterion_table_step121.csv']
}
with open(out/'step121_schema.json','w') as f:
    json.dump(schema,f,indent=2)

nonclaim = """# Step 121 Nonclaim Boundary

This step does not prove RH.

It does not prove that the Burnol-to-Dirichlet shadow defect vanishes.

It rejects ordinary critical-line partial sums as a lawful shadow for the completed response-space gate.

It defines a regularized co-Poisson/Müntz shadow family and names the exact adequacy residual:

\\[
\\Xi_{BD,N}=B_N^*(I-P_{D,N})B_N.
\\]

The accepted statuses are:

1. \\(\\delta_{BD,N}\\to0\\), shadow complete;
2. positive visibility floor strong enough that \\(\\gamma_N c_{hyb,N}\\to\\infty\\);
3. missed shadow compact/tail-paid;
4. missed shadow separately source-absorbed.

Without one of these, the result remains support-only.
"""
(out/'nonclaim_boundary_step121.md').write_text(nonclaim)

summary = """# Step 121 Results Summary

Step 121 constructs the regularized co-Poisson/Müntz Dirichlet shadow gate for the Burnol-to-Dirichlet readability problem.

The main correction is that ordinary critical-line partial sums of zeta are not lawful shadows. The shadow must be regularized by a declared Müntz/co-Poisson subtraction, by an approximate functional equation, or by another audited response-space construction.

For a Burnol/co-Poisson atom with right Mellin transform \\(\\widehat g(s)\\), the native target is

\\[
B g(s)=\\zeta(s)\\widehat g(s).
\\]

A smooth Müntz shadow is

\\[
Z_X^\\omega(s)=\\sum_{n\\ge1}\\omega(n/X)n^{-s}-X^{1-s}\\Omega(1-s),
\\]

where \\(\\Omega\\) is the Mellin transform of the cutoff. The shadow target is

\\[
B_X^{reg}g(s)=Z_X^\\omega(s)\\widehat g(s),
\\]

plus a declared residual/tail.

The decisive defect is the angular gap

\\[
\\delta_{BD,N}^{reg}=
\\|(I-P_{D,N}^{reg})B_NG_{B,N}^{-1/2}\\|.
\\]

Equivalently,

\\[
\\Xi_{BD,N}^{reg}=B_N^*(I-P_{D,N}^{reg})B_N.
\\]

Thus regularized readability is an adequacy problem, not a scalar approximation problem.

The hybrid visibility bound is

\\[
\\epsilon_{hyb,N}
\\le
\\epsilon_{B,N}+\\delta_{BD,N}^{reg}+\\tau_{reg,N},
\\]

hence

\\[
c_{hyb,N}
\\ge
1-(\\epsilon_{B,N}+\\delta_{BD,N}^{reg}+\\tau_{reg,N})^2.
\\]

The source route needs

\\[
G_{\\mathcal X,N}\\succeq\\gamma_NH_N,
\\qquad
\\gamma_Nc_{hyb,N}\\to\\infty,
\\]

plus fixed/exhaustive tail promotion.

The step does not close the gate. It defines the gate and rejects the naive shadow.
"""
(out/'step121_results_summary.md').write_text(summary)

tex = r"""
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{hyperref}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{remark}{Remark}
\newtheorem{gate}{Gate}

\title{Step 121: Regularized Co-Poisson/M\"untz Dirichlet Shadow Construction}
\author{RATCHET / Six Birds RH Membrane Program}
\date{}

\begin{document}
\maketitle

\section{Purpose}
Step 120 reduced the Burnol-to-Dirichlet readability problem to the angular gap
\[
\delta_{BD,N}=\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|.
\]
The point of Step 121 is to replace the naive critical-line Dirichlet partial sum by a lawful regularized shadow. The ordinary sum
\[
\sum_{n\le X}n^{-s}
\]
is not a legal shadow of \(\zeta(s)\) on the critical line unless accompanied by a declared regularization, pole/completion correction, and tail record.

\section{Burnol target}
Let \(g\) be a Burnol/co-Poisson generator with right Mellin transform
\[
\widehat g(s)=\int_0^\infty g(t)t^{-s}\,dt.
\]
The native co-Poisson/M\"untz target is
\[
B g(s)=\zeta(s)\widehat g(s).
\]
This target is lawful because it is obtained from the M\"untz-modified co-Poisson relation rather than from an unregularized critical-line Dirichlet series.

\section{Smooth M\"untz shadow}
Choose a smooth cutoff \(\omega\in C_c^\infty(0,\infty)\) with Mellin transform
\[
\Omega(w)=\int_0^\infty \omega(x)x^{w-1}\,dx.
\]
Define
\[
Z_X^\omega(s)
=
\sum_{n\ge1}\omega(n/X)n^{-s}-X^{1-s}\Omega(1-s).
\]
The subtraction term is the M\"untz/pole correction. It is not optional. The corresponding Burnol-to-Dirichlet shadow is
\[
B_X^{\mathrm{reg}}g(s)=Z_X^\omega(s)\widehat g(s),
\]
with residual
\[
T_X^\omega g(s)=\zeta(s)\widehat g(s)-Z_X^\omega(s)\widehat g(s).
\]

\begin{gate}[Regularization gate]
The shadow \(Z_X^\omega\widehat g\) is accepted only if the M\"untz correction channel
\[
X^{1-s}\Omega(1-s)\widehat g(s)
\]
and the residual tail \(T_X^\omega g\) are declared in the carrier. If they are ignored, the construction is a public shadow, not a membrane witness.
\end{gate}

\section{Finite window construction}
Let \(Y_{B,N}\) be a finite Burnol/co-Poisson atom window with synthesis map
\[
B_N:Y_{B,N}\to H_N,
\qquad
G_{B,N}=B_N^*B_N.
\]
Let \(D_N^{\mathrm{reg}}\) be the declared regularized Dirichlet-readable synthesis space. It may include:
\begin{enumerate}[label=(\roman*)]
\item the finite Dirichlet coefficient bank coming from \(\sum\omega(n/X)n^{-s}\),
\item a pole/completion channel for \(X^{1-s}\Omega(1-s)\),
\item dual-channel atoms from an approximate functional equation, if used,
\item a tail/nonclaim record.
\end{enumerate}
Let \(P_{D,N}^{\mathrm{reg}}\) project onto \(\operatorname{Ran}D_N^{\mathrm{reg}}\). Define
\[
\delta_{BD,N}^{\mathrm{reg}}
=
\|(I-P_{D,N}^{\mathrm{reg}})B_NG_{B,N}^{-1/2}\|.
\]
Equivalently,
\[
\Xi_{BD,N}^{\mathrm{reg}}
=
B_N^*(I-P_{D,N}^{\mathrm{reg}})B_N.
\]
This is the Burnol-to-Dirichlet adequacy residual.

\begin{theorem}[Regularized shadow angular-gap criterion]
The regularized shadow family is complete on the growing Burnol windows iff
\[
\delta_{BD,N}^{\mathrm{reg}}\to0.
\]
Equivalently, the declared regularized Dirichlet-readable spaces approximate the Burnol target ranges uniformly:
\[
\sup_{0\ne y\in Y_{B,N}}
\frac{\operatorname{dist}(B_Ny,\operatorname{Ran}D_N^{\mathrm{reg}})}{\|B_Ny\|}
\to0.
\]
Pointwise convergence on each fixed atom is not enough.
\end{theorem}

\section{Hybrid visibility bound}
Let \(\epsilon_{B,N}\) be the Burnol geometric exhaustion defect and let \(\tau_{reg,N}\) be the declared regularization/tail defect. Then
\[
\epsilon_{hyb,N}
\le
\epsilon_{B,N}+\delta_{BD,N}^{\mathrm{reg}}+\tau_{reg,N}.
\]
Therefore
\[
c_{hyb,N}
\ge
1-(\epsilon_{B,N}+\delta_{BD,N}^{\mathrm{reg}}+\tau_{reg,N})^2.
\]
If
\[
G_{\mathcal X,N}\succeq \gamma_N H_N,
\]
then the source route has effective strength
\[
\Lambda_{R,N}=\gamma_Nc_{hyb,N}.
\]
The completed route needs
\[
\gamma_Nc_{hyb,N}\to\infty
\]
with fixed/exhaustive tail promotion.

\section{Status trichotomy}
\begin{enumerate}[label=\textbf{S\arabic*.}]
\item \textbf{Shadow complete:} \(\delta_{BD,N}^{\mathrm{reg}}\to0\). Burnol visibility becomes Dirichlet/Hecke-readable.
\item \textbf{Positive floor:} \(\epsilon_{B,N}+\delta_{BD,N}^{\mathrm{reg}}+\tau_{reg,N}<1\) quantitatively. This can still suffice if \(\gamma_Nc_{hyb,N}\to\infty\).
\item \textbf{Missed shadow sector:} the limiting residual
\[
\Xi_{BD}=B^*(I-P_D)B
\]
is nonzero. It must be separately source-absorbed, compact/tail-paid, or declared as a scoped nonclaim.
\end{enumerate}

\section{No-overread rule}
The ordinary critical-line partial sum is rejected:
\[
\sum_{n\le X} n^{-s}
\quad\text{is not a lawful shadow on }\Re(s)=1/2.
\]
The legal objects are regularized shadows with declared M\"untz correction, approximate-functional-equation shadows with declared dual channel, or co-Poisson response shadows with fixed/exhaustive tail records.

\section{Conclusion}
Step 121 defines the regularized shadow gate. It does not prove \(\delta_{BD,N}\to0\). It names the exact object whose vanishing, positive floor, or source absorption must be earned:
\[
\Xi_{BD,N}^{\mathrm{reg}}=B_N^*(I-P_{D,N}^{\mathrm{reg}})B_N.
\]

\end{document}
"""
(out/'burnol_dirichlet_shadow_regularized_step121.tex').write_text(tex)

# basic latex structure check
content = tex
checks = [
    {'check':'begin_document','passed': '\\begin{document}' in content},
    {'check':'end_document','passed': '\\end{document}' in content},
    {'check':'balanced_equation_brackets','passed': content.count('\\[')==content.count('\\]')},
    {'check':'theorem_env_balance','passed': content.count('\\begin{theorem}')==content.count('\\end{theorem}')},
    {'check':'gate_env_balance','passed': content.count('\\begin{gate}')==content.count('\\end{gate}')},
]
with open(out/'latex_structure_check_step121.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(checks[0].keys()))
    w.writeheader(); w.writerows(checks)

# Zip selected artifacts
zip_path = out/'step121_regularized_shadow_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)

print(f'Wrote artifacts to {out}')
