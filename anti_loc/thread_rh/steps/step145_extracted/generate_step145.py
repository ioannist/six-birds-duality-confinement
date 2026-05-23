from pathlib import Path
import json, csv, math, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step145_burnol_residual_carrier')
out.mkdir(parents=True, exist_ok=True)

step = 145

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{enumitem}
\geometry{margin=1in}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}

\title{Step 145: Burnol/Sonine Residual Carrier Instantiation}
\author{Six Birds / RH Membrane Working Thread}
\date{}

\begin{document}
\maketitle

\section*{Purpose}
Step 144 gave an abstract completed-tail promotion theorem.  Step 145 instantiates its objects on the Burnol/Sonine residual carrier.  The goal is to replace the formal symbols
\[
H_R,\qquad P_N,\qquad T_N,\qquad K_R
\]
by explicit carrier-native objects.  The step is deliberately conservative: it proves the trace-tail promotion theorem once two records are supplied, and it names the two records that are not supplied automatically.

\section{Burnol/Sonine residual carrier}
Fix a Burnol scale
\[
0<a<1,\qquad A=a^{-1}.
\]
Let
\[
L_a\subset L^2(0,\infty;dt)
\]
be Burnol's extended Sonine space: functions constant on $(0,a)$ whose cosine transform is again constant on $(0,a)$.  Let
\[
Y_a=\overline{\mathrm{span}\{Y^a_{\rho,k}: \rho \in Z_\zeta,
0\le k<m_\rho\}}
\]
be the closed span of the zero-evaluator vectors.  Burnol's theorem gives, for $a<1$,
\[
P_a=Y_a^\perp,
\]
where $P_a$ is the co-Poisson subspace.

Let $P_\infty$ denote the imported archimedean Sonin/prolate projection and let $J_a$ be the declared transport into $L_a$.  For a finite-place log-shift mode $\ell$, define
\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]
The part of the shifted boundary packet seen by the zero-evaluator span is
\[
\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]
Thus the completed residual carrier is the closed subspace
\[
\boxed{
H_R:=\overline{\mathrm{span}\{\operatorname{Ran}\Pi_{Y_a}\mathfrak B_{\ell,a}:
\ell\in\mathcal L\setminus\{0\}\}}\subseteq Y_a\subset L_a.
}
\]
Equivalently, $H_R$ is the completed carrier of the residual
\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]
If all these ranges vanish, then $H_R=0$ and the Burnol/co-Poisson inclusion route closes.  Otherwise $H_R$ is the residual sector that must be source-absorbed.

\section{Finite windows}
A finite residual window must be upstream-declared.  We use a triple window
\[
\mathcal I_N=(\mathcal L_N,T_N^{\rm zero},K_N^{\Omega}),
\]
where
\begin{itemize}[leftmargin=2em]
\item $\mathcal L_N$ is a finite set of finite-place log-shift modes;
\item $T_N^{\rm zero}$ is a zero-evaluator height cutoff;
\item $K_N^{\Omega}$ is the declared Heap--Soundararajan-style block cutoff.
\end{itemize}
Define
\[
\mathcal R_N:=\mathrm{span}\left\{
\Pi_R\Pi_{Y_a}\mathfrak B_{\ell,a}u_j:
\ell\in\mathcal L_N,
\,j\le N
\right\}
\]
with the additional restriction that its regularized Burnol/Muentz shadow lies in the declared $\Omega$-compatible source-readable dictionary at cutoff $K_N^{\Omega}$.  Let
\[
P_N:H_R\to H_R
\]
be the orthogonal projection onto the closed finite-dimensional space
\[
H_{R,N}:=\overline{\mathcal R_N}\subset H_R.
\]
The window ladder is accepted only if
\[
\boxed{P_N\uparrow I_{H_R}\quad\text{strongly}.}
\]
This is the completed residual-exhaustivity record.

\section{Completed residual ledger}
The completed residual ledger is a positive operator
\[
K_R\ge0
\]
on $H_R$.  In the RH application, the intended ledger is the projection of the completed anti-invariant zero ledger to the residual carrier.  Abstractly, we write
\[
K_R=\Pi_RK_Z\Pi_R,
\]
where $K_Z$ is the completed off-critical zero-audit ledger and $\Pi_R$ is the projection to $H_R$.  Its trace-class status is not automatic.

\begin{definition}[Accepted completed residual ledger]
The residual ledger record is accepted if
\[
\boxed{K_R\in\mathcal S_1(H_R),\qquad K_R\ge0.}
\]
If $K_R$ is not trace-class, finite-window source frames remain support-only unless a separate weighted tail theorem is supplied.
\end{definition}

\section{Tail form}
With $G_R=I_{H_R}$ and $P_N$ orthogonal, the canonical tail form is
\[
\boxed{T_N=I_{H_R}-P_N.}
\]
Then
\[
G_R=P_N^*G_{R,N}P_N+T_N
\]
with $G_{R,N}=I_{H_{R,N}}$.

\begin{theorem}[Burnol/Sonine completed-tail promotion]
Assume
\[
P_N\uparrow I_{H_R}\quad\text{strongly},
\qquad
K_R\in\mathcal S_1(H_R),
\qquad K_R\ge0.
\]
Then
\[
\boxed{
\operatorname{tr}(T_NK_R)=\operatorname{tr}((I-P_N)K_R)\to0.
}
\]
Consequently, any finite-window source frame satisfying
\[
F_N^{\Omega,\rm win}\succeq \Lambda_N^\Omega G_{R,N}
\]
lifts to the completed residual carrier as
\[
F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R,
\]
and the completed residual squeeze is
\[
\boxed{
\operatorname{tr}(G_RK_R)
\le
\frac{C_{\rm src}}{\Lambda_N^\Omega}
+\operatorname{tr}(T_NK_R).
}
\]
Thus completed residual mass collapses if
\[
\Lambda_N^\Omega\to\infty
\qquad\text{and}\qquad
\operatorname{tr}(T_NK_R)\to0.
\]
\end{theorem}

\begin{proof}
For positive trace-class $K_R$, finite-rank projections $P_N\uparrow I$ strongly imply
\[
\operatorname{tr}((I-P_N)K_R)\to0.
\]
This follows by approximating $K_R$ in trace norm by a finite-rank positive operator and using strong convergence on the finite-dimensional range.  The lifted frame inequality is the Step 144 promotion identity specialized to $G_R=I$ and $T_N=I-P_N$.  The squeeze follows by pairing the lifted inequality with $K_R$ and using the source-audit bound.
\end{proof}

\section{What is now instantiated}
The abstract Step 144 symbols become:
\[
\boxed{H_R=\overline{\mathrm{span}\,\operatorname{Ran}\Pi_{Y_a}\mathfrak B_{\ell,a}}\subset L_a,}
\]
\[
\boxed{P_N=\text{orthogonal projection onto the finite declared residual window }H_{R,N},}
\]
\[
\boxed{T_N=I_{H_R}-P_N,}
\]
\[
\boxed{K_R=\Pi_RK_Z\Pi_R\text{, accepted only with positive trace-class record.}}
\]

\section{Remaining obligations}
The instantiation does not prove RH.  It names the remaining carrier-side records:
\begin{enumerate}[leftmargin=2em]
\item strong exhaustivity of the declared residual windows: $P_N\uparrow I_{H_R}$;
\item trace-class status of the completed residual ledger: $K_R\in\mathcal S_1$;
\item source strength: $\Lambda_N^\Omega\to\infty$;
\item no-smuggling of $\mathcal I_N=(\mathcal L_N,T_N^{\rm zero},K_N^\Omega)$;
\item compatibility with the restricted BPRZ source frame and source shortness;
\item fixed/exhaustive promotion of the off-critical zero ledger.
\end{enumerate}

\section{Nonclaim boundary}
If $P_N\not\uparrow I_{H_R}$, the result is finite-window support evidence only.  If $K_R$ is not trace-class, $\operatorname{tr}(T_NK_R)\to0$ is not automatic and becomes a separate zero-density/regularity theorem.  If $H_R$ has a component outside the regularized Dirichlet-readable closure, that component remains an adequacy residual and is not source-absorbed by the present ladder.

\end{document}
'''
(out/'burnol_residual_carrier_step145.tex').write_text(tex)

summary = r'''
# Step 145: Burnol/Sonine residual carrier instantiation

## Main result

Step 145 instantiates the abstract completed-tail promotion objects from Step 144 on the actual Burnol/Sonine residual carrier.

The completed residual carrier is

\[
H_R=\overline{\operatorname{span}\{\operatorname{Ran}\Pi_{Y_a}\mathfrak B_{\ell,a}:\ell\in\mathcal L\setminus\{0\}\}}\subseteq Y_a\subset L_a.
\]

Here

\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty)
\]

is the shifted Sonin/prolate boundary block transported into Burnol's \(L_a\)-carrier, and \(\Pi_{Y_a}\) projects onto Burnol's zero-evaluator span.

Burnol supplies the backbone: for \(a<1\), the co-Poisson subspace satisfies

\[
P_a=Y_a^\perp.
\]

Thus \(H_R\) is exactly the residual sector not hidden inside the co-Poisson complement.

## Instantiated objects

\[
H_R=\text{completed residual carrier},
\]

\[
P_N=\text{orthogonal projection onto an upstream-declared finite residual window},
\]

\[
T_N=I_{H_R}-P_N,
\]

\[
K_R=\Pi_RK_Z\Pi_R,
\]

where \(K_Z\) is the completed off-critical zero-audit ledger and \(\Pi_R\) projects to \(H_R\).

## Completed-tail theorem

If

\[
P_N\uparrow I_{H_R}\quad\text{strongly}
\]

and

\[
K_R\in\mathcal S_1(H_R),\qquad K_R\ge0,
\]

then

\[
\operatorname{tr}((I-P_N)K_R)\to0.
\]

So the Step 144 completed residual squeeze becomes

\[
\operatorname{tr}(G_RK_R)
\le
\frac{C_{\rm src}}{\Lambda_N^\Omega}
+\operatorname{tr}((I-P_N)K_R).
\]

Completed residual mass collapses if

\[
\Lambda_N^\Omega\to\infty
\]

and the tail vanishes.

## Remaining obligations

Step 145 does not prove RH. It reduces the completed carrier side to two exact records:

1. residual-window exhaustivity: \(P_N\uparrow I_{H_R}\);
2. trace-class residual ledger: \(K_R\in\mathcal S_1\).

If either fails, finite \(\Omega\)-compatible source frames remain moving-window evidence.

## Bottom line

\[
\boxed{\text{Step 145 turns the completed residual-tail gate into a concrete Burnol/Sonine carrier theorem.}}
\]

The next step is Step 146: prove or refute the trace-class residual ledger record for \(K_R\) on \(H_R\).
'''
(out/'step145_results_summary.md').write_text(summary)

# CSVs

def write_csv(path, rows, fieldnames):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)

carrier_rows = [
    {"object":"H_R","definition":"closed span of ranges of Pi_Ya B_{ell,a}","status":"instantiated","gate":"Burnol residual carrier declared","failure_mode":"boundary residual not represented"},
    {"object":"P_N","definition":"orthogonal projection onto declared finite residual window","status":"conditional","gate":"P_N strong-to-I","failure_mode":"moving-window support only"},
    {"object":"T_N","definition":"I_HR - P_N","status":"instantiated","gate":"tail form accepted after P_N declared","failure_mode":"tail not decreasing if windows not exhaustive"},
    {"object":"K_R","definition":"Pi_R K_Z Pi_R","status":"conditional","gate":"positive trace-class ledger","failure_mode":"zero-density/regularity obligation"},
    {"object":"Lambda_N^Omega","definition":"restricted source strength times density and blind-sector floors","status":"conditional","gate":"diverges","failure_mode":"source ladder finite support only"},
]
write_csv(out/'burnol_residual_carrier_gate_table_step145.csv', carrier_rows, ["object","definition","status","gate","failure_mode"])

theorem_rows = [
    {"theorem":"Carrier instantiation","input":"Burnol L_a, Y_a, shifted blocks B_{ell,a}","output":"H_R subset Y_a subset L_a","status":"defined"},
    {"theorem":"Window exhaustivity","input":"P_N increasing declared windows","output":"P_N -> I_HR strongly","status":"record required"},
    {"theorem":"Trace-class tail lemma","input":"K_R positive trace-class and P_N -> I","output":"tr((I-P_N)K_R)->0","status":"standard functional analysis"},
    {"theorem":"Completed residual squeeze","input":"finite source frame plus tail lemma","output":"tr(G_R K_R) <= C/Lambda + tail","status":"conditional"},
    {"theorem":"Moving-window obstruction","input":"tail nonzero or nontrace ledger","output":"support-only nonclaim","status":"warning"},
]
write_csv(out/'theorem_map_step145.csv', theorem_rows, ["theorem","input","output","status"])

route_rows = [
    {"route_component":"Burnol carrier","status":"active","comment":"H_R is defined in L_a via zero-evaluator-visible boundary residual"},
    {"route_component":"Omega-compatible dictionary","status":"active conditional","comment":"feeds the finite windows H_R,N"},
    {"route_component":"restricted BPRZ source frame","status":"active conditional","comment":"provides gamma_q on nonblind residual class"},
    {"route_component":"completed tail","status":"new active gate","comment":"requires P_N strong-exhaustive and K_R trace-class"},
    {"route_component":"RH conclusion","status":"not claimed","comment":"requires all carrier, source, adequacy, and tail records"},
]
write_csv(out/'route_status_step145.csv', route_rows, ["route_component","status","comment"])

arith_rows = [
    {"input":"Burnol completeness/minimality","role":"defines L_a, Y_a, P_a=Y_a^perp","needed_record":"carrier identification"},
    {"input":"co-Poisson/Muentz structure","role":"defines lawful residual seed/shadow","needed_record":"regularized shadow adequacy"},
    {"input":"semilocal Hardy-Titchmarsh","role":"transport of local factors into response geometry","needed_record":"semilocal compatibility"},
    {"input":"BPRZ twisted second moment","role":"restricted source lower frame candidate","needed_record":"matrix lower-frame on residual class"},
    {"input":"zero-density or trace regularity","role":"trace-class K_R or tail bound","needed_record":"completed ledger promotion"},
]
write_csv(out/'arithmetic_input_table_step145.csv', arith_rows, ["input","role","needed_record"])

construct_rows = [
    {"task":"Define H_R precisely for chosen a and shift ladder","owner":"framework/analysis","priority":"high","done_in_step145":"yes"},
    {"task":"Declare finite windows P_N without target selection","owner":"framework","priority":"high","done_in_step145":"yes, abstract schema"},
    {"task":"Prove P_N -> I_HR strongly","owner":"Burnol/Sonine analysis","priority":"high","done_in_step145":"no"},
    {"task":"Prove K_R positive trace-class","owner":"zero-ledger analysis","priority":"highest","done_in_step145":"no"},
    {"task":"Couple restricted source frame to completed ledger","owner":"source-frame analysis","priority":"high","done_in_step145":"conditional theorem"},
]
write_csv(out/'construction_tasks_step145.csv', construct_rows, ["task","owner","priority","done_in_step145"])

nonclaim = r'''
# Step 145 nonclaim boundary

Step 145 does not prove RH.

It does not prove that the residual carrier is zero.

It does not prove that the finite residual windows are exhaustive.

It does not prove that the completed residual zero ledger is trace-class.

It does not prove the restricted BPRZ matrix lower frame.

It proves the carrier-level promotion theorem conditional on:

\[
P_N\uparrow I_{H_R}
\]

and

\[
K_R\in\mathcal S_1(H_R),\quad K_R\ge0.
\]

If either condition fails, finite \(\Omega\)-compatible windows are moving-window support evidence only.
'''
(out/'nonclaim_boundary_step145.md').write_text(nonclaim)

schema = {
    "step": 145,
    "name": "Burnol/Sonine residual carrier instantiation",
    "objects": {
        "H_R": "closed span of zero-evaluator-visible shifted boundary residuals",
        "P_N": "orthogonal projection onto declared finite residual windows",
        "T_N": "I - P_N",
        "K_R": "Pi_R K_Z Pi_R, accepted only if positive trace-class",
        "Lambda_N_Omega": "restricted source strength after density and blind-sector floors"
    },
    "main_conditions": ["P_N strong convergence to identity", "K_R positive trace-class", "Lambda_N^Omega diverges", "fixed/exhaustive residual-tail promotion"],
    "main_theorem": "tr((I-P_N)K_R) -> 0 under strong projection convergence and trace-class ledger",
    "next_step": 146
}
(out/'step145_schema.json').write_text(json.dumps(schema, indent=2))

# Generate plots and data
N = np.arange(1, 121)
# trace class eigenvalue decay scenarios
rates = {
    'trace_class_fast_n^-2': 1/(N**2),
    'trace_class_exp': np.exp(-N/18),
    'borderline_n^-1': 1/N,
    'nontrace_flat': np.ones_like(N)*0.02
}
rows = []
plt.figure(figsize=(8,5))
for label, eigs in rates.items():
    # tail from N onward for an infinite-ish finite grid approximation; use full 120 tail for demo
    tails = np.array([np.sum(eigs[i:]) for i in range(len(N))])
    tails = tails/tails[0]
    for n,t in zip(N,tails): rows.append({'N':int(n),'scenario':label,'normalized_tail':float(t)})
    plt.plot(N,tails,label=label)
plt.yscale('log')
plt.xlabel('window N')
plt.ylabel('normalized trace tail')
plt.title('Completed residual-tail scenarios')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'completed_residual_tail_scenarios_step145.png', dpi=180)
plt.close()
pd.DataFrame(rows).to_csv(out/'completed_residual_tail_scenarios_step145.csv', index=False)

# source strength vs tail squeeze
N2 = np.arange(10, 1000, 10)
gamma = np.log(N2+2)
visibility_good = 0.85
visibility_mid = 0.35
tail_fast = 1/(N2**0.7)
tail_slow = 1/np.log(N2+3)
C=1.0
squeeze_good = C/(gamma*visibility_good) + tail_fast
squeeze_mid = C/(gamma*visibility_mid) + tail_slow
plt.figure(figsize=(8,5))
plt.plot(N2,squeeze_good,label='good visibility + fast tail')
plt.plot(N2,squeeze_mid,label='mid visibility + slow tail')
plt.xlabel('source/window scale')
plt.ylabel('residual mass upper bound proxy')
plt.title('Completed residual squeeze: source term plus tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'completed_residual_squeeze_step145.png', dpi=180)
plt.close()
pd.DataFrame({
    'N': N2,
    'gamma_log': gamma,
    'squeeze_good_fast_tail': squeeze_good,
    'squeeze_mid_slow_tail': squeeze_mid
}).to_csv(out/'completed_residual_squeeze_step145.csv', index=False)

# moving window failure
N3=np.arange(1,151)
fixed_tail=np.exp(-N3/25)
moving_tail=0.25+0.02*np.sin(N3/8)
plt.figure(figsize=(8,5))
plt.plot(N3,fixed_tail,label='fixed/exhaustive ledger tail')
plt.plot(N3,moving_tail,label='moving-window tail floor')
plt.xlabel('window N')
plt.ylabel('tail contribution')
plt.title('Moving-window support-only failure')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_window_tail_failure_step145.png', dpi=180)
plt.close()
pd.DataFrame({'N':N3,'fixed_exhaustive_tail':fixed_tail,'moving_window_tail_floor':moving_tail}).to_csv(out/'moving_window_tail_failure_step145.csv', index=False)

# projection ladder visualization: cumulative trace captured
N4=np.arange(1,121)
eigs=1/(N4**1.6)
capture=np.cumsum(eigs)/np.sum(eigs)
plt.figure(figsize=(8,5))
plt.plot(N4,capture)
plt.xlabel('window N')
plt.ylabel('fraction of residual trace captured')
plt.title('Strong-exhaustive projection ladder with trace-class ledger')
plt.tight_layout()
plt.savefig(out/'projection_ladder_trace_capture_step145.png', dpi=180)
plt.close()
pd.DataFrame({'N':N4,'trace_captured_fraction':capture}).to_csv(out/'projection_ladder_trace_capture_step145.csv', index=False)

# effective source strength
qscale=np.logspace(2,8,120)
gamma=np.log(qscale)
eps=np.array([0.15,0.45,0.75])
delta=np.array([0.2,0.55,0.85])
plt.figure(figsize=(8,5))
for e,d in [(0.15,0.2),(0.45,0.55),(0.75,0.85)]:
    lam=gamma*(1-e**2)*(1-d**2)
    plt.plot(qscale,lam,label=f'eps={e}, delta={d}')
plt.xscale('log')
plt.xlabel('source conductor q')
plt.ylabel('effective Lambda^Omega')
plt.title('Effective restricted source strength after carrier floors')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'effective_restricted_source_strength_step145.png', dpi=180)
plt.close()

# Check script
check = r'''
import json
from pathlib import Path
p=Path('/mnt/data/rh_membrane_step145_burnol_residual_carrier')
required=[
 'burnol_residual_carrier_step145.tex',
 'step145_results_summary.md',
 'burnol_residual_carrier_gate_table_step145.csv',
 'theorem_map_step145.csv',
 'route_status_step145.csv',
 'arithmetic_input_table_step145.csv',
 'construction_tasks_step145.csv',
 'nonclaim_boundary_step145.md',
 'step145_schema.json'
]
missing=[x for x in required if not (p/x).exists()]
print(json.dumps({'missing':missing,'ok':not missing},indent=2))
'''
(out/'run_step145_tail_promotion_check.py').write_text(check)

# structure check csv
tex_text = tex
balance_rows=[]
for sym_open, sym_close, name in [('{','}','braces'), ('[',']','brackets'), ('(',')','parens')]:
    balance_rows.append({'symbol':name,'open_count':tex_text.count(sym_open),'close_count':tex_text.count(sym_close),'balanced':tex_text.count(sym_open)==tex_text.count(sym_close)})
pd.DataFrame(balance_rows).to_csv(out/'latex_structure_check_step145.csv', index=False)

# Zip
zip_path = out/'step145_burnol_residual_carrier_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for file in out.iterdir():
        if file.name != zip_path.name:
            z.write(file, arcname=file.name)

print('created', len(list(out.iterdir())), 'files in', out)
