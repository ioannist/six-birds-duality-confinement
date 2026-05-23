import os, json, csv, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step99_plancherel_exhaustivity')
out.mkdir(parents=True, exist_ok=True)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,enumitem,booktabs,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\newtheorem{warning}{Warning}
\newcommand{\cH}{\mathcal H}
\newcommand{\cX}{\mathcal X}
\newcommand{\cS}{\mathcal S}
\newcommand{\cP}{\mathcal P}
\newcommand{\eps}{\varepsilon}
\newcommand{\tr}{\operatorname{tr}}
\newcommand{\Ran}{\operatorname{Ran}}
\newcommand{\Fix}{\operatorname{Fix}}
\title{Step 99: Semilocal Plancherel/Exhaustivity Record for the Character-Source Route}
\author{RATCHET working note}
\date{\today}
\begin{document}
\maketitle

\section{Purpose}
Step 98 proved that a complete finite character family is a tight frame on a finite abelian quotient, but that finite character orthogonality is not a completed lower frame.  Step 99 states the exact promotion record needed to turn finite Dirichlet/Hecke windows into a completed semilocal source frame.

The target source inequality is
\[
F_n
=
\sum_{\omega\in\mathcal X_n}
\lambda_{\omega,n} Q_\omega^*\Theta_\omega^{-1}Q_\omega
\succeq
\Lambda_n(\Theta_0^-)^{-1},
\qquad
\Lambda_n\to\infty.
\]
It is this lower frame, not a large-sieve upper bound, that collapses the anti-invariant currency.

\section{Semilocal response spaces}
Let \(S\) be a finite set of places with \(\infty\in S\).  The semilocal Hardy--Titchmarsh formalism gives a response space
\[
Y_S=L^2(\mathbb R,dm_S),
\qquad
 dm_S(s)=\left|\prod_{v\in S}L_v\left(\frac12-is\right)\right|^2ds,
\]
and an anti-invariant subspace
\[
Y_S^-=
\{y\in Y_S:\mathcal J_Sy=-y\},
\qquad
(\mathcal J_Sy)(s)=\overline{y(-s)}.
\]
Finite-place enlargement changes the measure, and therefore changes the response geometry.  Consequently the spaces \(Y_S^-\) are not automatically the same Hilbert space.

\begin{definition}[Completed Plancherel response record]
A completed semilocal/Hecke Plancherel response record consists of:
\[
Y_\infty^-,\quad \Theta_0^-\succ0,\quad
J_S:Y_S^-\to Y_\infty^-,\quad
\Pi_S=J_SJ_S^*,
\]
where each \(J_S\) is a declared isometric or defect-controlled transport, and \(\Pi_S\) is the visible semilocal window in the completed anti-invariant response space.
It also includes a tail record
\[
I_{Y_\infty^-}
\preceq
\Pi_S+T_S,
\qquad
T_S\succeq0,
\]
with an audit norm such as
\[
\tr\left((\Theta_0^-)^{-1/2}T_S(\Theta_0^-)^{-1/2}\right)\to0
\]
or the corresponding zero-ledger tail condition.
\end{definition}

\section{Finite window frames do not promote automatically}
\begin{lemma}[finite-rank lower-frame obstruction]
Let \(Y\) be infinite dimensional.  If \(F\ge0\) has finite rank, then for every \(\Lambda>0\),
\[
F\nsucceq \Lambda I_Y.
\]
\end{lemma}
\begin{proof}
There is a nonzero \(y\in\ker F\).  Then \(\langle y,Fy\rangle=0\) but \(\Lambda\|y\|^2>0\).
\end{proof}

\begin{warning}[finite character windows are support-only]
A complete character family on a finite quotient gives a tight frame on that finite quotient.  After transport to a completed response space it controls only \(\Ran\Pi_S\).  Without a tail/exhaustivity bridge, the hidden complement \((I-\Pi_S)Y_\infty^-\) may contain anti-invariant directions untouched by all finite-window sources.
\end{warning}

\section{Completed lower-frame promotion}
\begin{theorem}[Plancherel/exhaustivity promotion: fixed completed frame version]
Let \(Y_\infty^-\) be the completed anti-invariant response space.  Suppose a completed character/Hecke Plancherel measure \(\mu_{\rm Pl}\) and readouts \(Q_\omega:Y_\infty^-\to Y_\omega\) satisfy the tight-frame identity
\[
\int_\Omega Q_\omega^*\Theta_\omega^{-1}Q_\omega\,d\mu_{\rm Pl}(\omega)
=
(\Theta_0^-)^{-1}.
\]
If a declared source ladder weights the whole Plancherel spectrum by \(a_n(\omega)\ge \Lambda_n\) almost everywhere, with \(\Lambda_n\to\infty\), then
\[
F_n
=
\int_\Omega a_n(\omega)Q_\omega^*\Theta_\omega^{-1}Q_\omega\,d\mu_{\rm Pl}(\omega)
\succeq
\Lambda_n(\Theta_0^-)^{-1}.
\]
Consequently the anti-invariant currency satisfies
\[
K_n^-
\preceq
\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n},
\]
and collapses if \(E_{{\rm src},n}\to0\) in the fixed/exhaustive ledger sense.
\end{theorem}

\begin{theorem}[Plancherel/exhaustivity promotion: finite-window version]
Let \(\Pi_n\) be finite or semilocal conductor-window visibility operators in \(Y_\infty^-\).  Suppose the finite-window character frame satisfies
\[
F_n^{\rm win}\succeq \lambda_n\Pi_n(\Theta_0^-)^{-1}\Pi_n
\]
on the visible window.  Then the full completed lower-frame claim follows only if there is either:
\begin{enumerate}[label=(\alph*)]
\item a tail source \(G_n\succeq \lambda_n T_n^{\rm src}\) charging the hidden complement so that
\[
F_n^{\rm win}+G_n\succeq\Lambda_n(\Theta_0^-)^{-1},
\]
with \(\Lambda_n\to\infty\); or
\item a zero-ledger exhaustivity bridge
\[
\mathsf A_Z\preceq \iota_n\mathsf A_{Z,n}\iota_n^*+R_n,
\qquad
\mathsf A_{Z,n}\preceq B_n,
\qquad
\tr(B_n)+\tr(R_n)\to0.
\]
\end{enumerate}
Without (a) or (b), finite-window character orthogonality remains support-only.
\end{theorem}

\section{Semilocal transport gate}
For \(S\subset S'\), finite local factors deform the semilocal measure by
\[
\frac{dm_{S'}(s)}{dm_S(s)}
=
\left|\prod_{p\in S'\setminus S}L_p\left(\frac12-is\right)\right|^2.
\]
Thus a character-source lower frame on \(Y_S^-\) does not automatically compare to one on \(Y_{S'}^-\) unless the transport map and Radon--Nikodym distortion are audited.  The semilocal Plancherel record must therefore include:
\[
J_{S\to S'},\quad
\beta_{S,S'},\quad
E_{S,S'},
\]
with
\[
\|J_{S\to S'}y\|_{S'}^2
\ge \beta_{S,S'}\|y\|_S^2 - E_{S,S'}[y]
\]
or an equivalent exact unitary identification.

\section{Obstruction alternatives}
If the completed source route fails, the failure must be charged to one of:
\[
\text{no completed Plancherel measure},
\quad
\text{finite window only},
\quad
\text{tail not vanishing},
\quad
\text{transport distortion},
\]
\[
\text{partial character coverage},
\quad
\text{upper bound but no lower frame},
\quad
\text{target-selected/smuggled sources},
\quad
\text{Hecke-to-zeta descent missing}.
\]

\section{Consequence for the hybrid RH route}
The hybrid program now needs one of two exact records:
\[
\boxed{\text{completed Hecke/Plancherel lower frame with }\Lambda_n\to\infty}
\]
or
\[
\boxed{\text{finite conductor windows plus fixed/exhaustive zero-ledger tail control}.}
\]
The first is a full-source route.  The second is a finite-window promotion route.  Finite character orthogonality alone is neither.

\end{document}
'''
(out/'semilocal_plancherel_exhaustivity_step99.tex').write_text(tex)

summary = r'''
# Step 99: Semilocal Plancherel/Exhaustivity Record

This step formulates the exact promotion theorem needed to turn finite Dirichlet/Hecke character windows into a completed source lower frame.

Main distinction:

\[
\text{finite character tight frame}
\neq
\text{completed anti-invariant lower frame}.
\]

Finite character orthogonality is exact on a finite quotient, but after transport to the completed response space it controls only a visible window. A full RH source route needs either:

\[
F_n\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty,
\]

on the completed anti-invariant response space, or finite-window control plus a vanishing zero-ledger tail.

## Core theorem

If a completed Plancherel source family satisfies

\[
\int Q_\omega^*\Theta_\omega^{-1}Q_\omega\,d\mu_{\rm Pl}(\omega)
=(\Theta_0^-)^{-1},
\]

and source weights satisfy \(a_n(\omega)\ge\Lambda_n\) almost everywhere, then

\[
F_n=\int a_n(\omega)Q_\omega^*\Theta_\omega^{-1}Q_\omega\,d\mu_{\rm Pl}(\omega)
\succeq \Lambda_n(\Theta_0^-)^{-1}.
\]

This yields

\[
K_n^-\preceq \Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n}.
\]

## Finite-window warning

If \(F_n\) is finite rank on an infinite completed response space, then

\[
F_n\nsucceq \Lambda I
\]

for every \(\Lambda>0\). Therefore finite conductor windows are support-only unless they come with either hidden-complement source control or a zero-ledger tail/exhaustivity bridge.

## Semilocal transport issue

The semilocal response spaces are

\[
Y_S=L^2(\mathbb R,dm_S),
\qquad
 dm_S(s)=\left|\prod_{v\in S}L_v(1/2-is)\right|^2ds.
\]

Adding finite places changes the measure. Thus source frames on different semilocal spaces cannot be compared without a transport/Radon--Nikodym audit.

## Bottom line

The RH source route now requires:

\[
\boxed{\text{completed Hecke/Plancherel lower frame}}
\]

or

\[
\boxed{\text{finite windows plus fixed/exhaustive zero-ledger tail}.}
\]

Finite character orthogonality alone is not enough.
'''
(out/'step99_results_summary.md').write_text(summary)

# CSVs
plancherel_gate = [
    ['gate','accepted_record','failure_status'],
    ['Completed response space','Y_infty^- with budget Theta_0^-','finite window only'],
    ['Semilocal transport','isometries or defect-controlled J_S into Y_infty^-','measure deformation overread'],
    ['Plancherel identity','integral Q_omega^*Theta_omega^{-1}Q_omega dmu = Theta_0^{-1}','trace/upper bound only'],
    ['Full lower frame','F_n >= Lambda_n Theta_0^{-1}, Lambda_n -> infinity','partial character coverage'],
    ['Finite-window promotion','tail source or zero-ledger exhaustivity','moving_window_support_only'],
    ['Defect control','E_src,n and transport defects vanish','support_only/nonclaim'],
    ['No-smuggling','source family declared upstream','target-selected sources'],
]
with (out/'semilocal_plancherel_gate_table_step99.csv').open('w', newline='') as f:
    csv.writer(f).writerows(plancherel_gate)

construction_tasks = [
    ['task','mathematical object','needed proof'],
    ['Common response space','Y_infty^-','define completed Hecke/semilocal anti-invariant response Hilbert space'],
    ['Transport maps','J_S:Y_S^- -> Y_infty^-','unitary or defect-controlled embedding including Radon-Nikodym distortion'],
    ['Plancherel measure','mu_Pl on character/Hecke spectrum','tight-frame identity on completed response space'],
    ['Finite conductor windows','Pi_n or R_n','tail/exhaustivity bridge to completed ledger'],
    ['Lower-frame growth','Lambda_n','source weights cover every anti-invariant direction'],
    ['Delta absorption','Delta_S^+ <= F_n + E_n','operator inequality on common response core'],
    ['Zeta descent','Hecke/source carrier -> zeta zero ledger','lawful bridge, no public-shadow overread'],
]
with (out/'construction_tasks_step99.csv').open('w', newline='') as f:
    csv.writer(f).writerows(construction_tasks)

status_table = [
    ['source_record','status','why'],
    ['Complete characters on finite abelian quotient','accepted finite tight frame','orthogonality gives identity on finite quotient'],
    ['Finite Dirichlet conductor window','support-only','finite-rank/finite-window unless tail/exhaustivity bridge'],
    ['Completed Hecke Plancherel source','load-bearing if proven','can provide full lower frame on Y_infty^-'],
    ['Large sieve upper bound','insufficient','upper frame does not charge every hidden direction'],
    ['Primitive-only character family','partial unless complement accounted','may miss imprimitive/local sectors'],
    ['Semilocal spaces without transport','not comparable','dm_S changes with local factors'],
    ['Finite spectral triples','strong finite evidence','still need determinant/ledger convergence to Xi'],
]
with (out/'source_status_step99.csv').open('w', newline='') as f:
    csv.writer(f).writerows(status_table)

theorem_map = [
    ['theorem','statement','depends_on','use'],
    ['Finite-rank no full lower frame','finite rank F cannot dominate Lambda I on infinite Y','linear algebra','blocks overreading finite character windows'],
    ['Completed Plancherel promotion','tight Plancherel frame plus weights >= Lambda_n gives lower frame','Plancherel identity','source-coercivity route'],
    ['Finite-window promotion','window lower frame needs tail source or zero-ledger tail','fixed/exhaustive ledger theorem','finite-to-completed promotion'],
    ['Semilocal transport gate','Y_S spaces require transport/RN audit','Hardy-Titchmarsh semilocal measure','avoid comparing different measures illegally'],
    ['Obstruction alternative','failure charged to named records','all-six/no-smuggling','diagnostics'],
]
with (out/'theorem_map_step99.csv').open('w', newline='') as f:
    csv.writer(f).writerows(theorem_map)

nonclaim = r'''
# Nonclaim boundary — Step 99

This step does not prove RH.

It does not prove that finite Dirichlet character windows form a completed lower frame.

It does not prove a Hecke Plancherel theorem for the required anti-invariant response space.

It does not prove that semilocal conductor windows have vanishing tail.

It does not prove that large-sieve or zero-density estimates supply the lower frame. Upper bounds are not lower frames.

It states the exact promotion theorem that would be needed:

- completed response space;
- transport from semilocal windows;
- Plancherel/tight-frame identity;
- lower-frame growth;
- tail/exhaustivity or hidden-complement source;
- no-smuggling source declaration;
- zeta descent bridge.
'''
(out/'nonclaim_boundary_step99.md').write_text(nonclaim)

schema = {
    'step': 99,
    'title': 'Semilocal Plancherel/Exhaustivity Record',
    'main_objects': {
        'Y_S_minus': 'L^2(R, dm_S)^- with dm_S=|prod_{v in S} L_v(1/2-is)|^2 ds',
        'Y_infty_minus': 'completed anti-invariant response space',
        'J_S': 'transport from semilocal response to completed response',
        'Pi_S': 'visible semilocal window in completed response',
        'T_S': 'tail/exhaustivity defect',
        'F_n': 'character/Hecke source frame',
        'Lambda_n': 'lower-frame growth constant'
    },
    'accepted_route': [
        'completed Plancherel identity',
        'source weights cover full Plancherel spectrum with Lambda_n -> infinity',
        'defects vanish',
        'fixed or exhaustive zero ledger'
    ],
    'support_only_routes': [
        'finite conductor window without tail',
        'trace-only character average',
        'large-sieve upper bound only',
        'semilocal spaces compared without transport'
    ]
}
(out/'step99_schema.json').write_text(json.dumps(schema, indent=2))

# check script
script = r'''#!/usr/bin/env python3
"""Finite sanity models for Step 99.
These are algebra illustrations only, not RH evidence.
"""
import numpy as np

# finite rank cannot dominate identity on a larger space
N=20
rank=6
F=np.zeros((N,N))
F[:rank,:rank]=np.eye(rank)
eig=np.linalg.eigvalsh(F-np.eye(N))
print('min eig(F-I)=', eig[0])

# full repeated Plancherel frames collapse budget like 1/n
for n in [1,2,5,10,50]:
    Lambda=n
    print(n, 1.0/Lambda)
'''
(out/'run_plancherel_exhaustivity_step99.py').write_text(script)
os.chmod(out/'run_plancherel_exhaustivity_step99.py', 0o755)

# Numerical sanity data + plots
N=80
ranks=np.arange(1,N+1)
min_eigs=[]
for r in ranks:
    # finite window projection minus identity on N-dimensional stand-in
    F=np.zeros((N,N)); F[:r,:r]=np.eye(r)
    min_eigs.append(np.linalg.eigvalsh(F-np.eye(N))[0])
with (out/'finite_window_no_full_frame_step99.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['rank','min_eig_projection_minus_identity'])
    for r,e in zip(ranks,min_eigs): w.writerow([int(r),float(e)])
plt.figure(figsize=(6,4)); plt.plot(ranks,min_eigs); plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('visible window rank r in an N-dimensional stand-in'); plt.ylabel('min eig(P_r - I_N)')
plt.title('Finite windows do not dominate the full identity')
plt.tight_layout(); plt.savefig(out/'finite_window_no_full_frame_step99.png', dpi=160); plt.close()

n=np.arange(1,101)
# tail models
tail_good=np.exp(-n/15)
tail_bad=1/(1+np.log(n+1))
with (out/'plancherel_tail_models_step99.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['n','vanishing_tail','slow_tail'])
    for i,a,b in zip(n,tail_good,tail_bad): w.writerow([int(i),float(a),float(b)])
plt.figure(figsize=(6,4)); plt.semilogy(n,tail_good,label='vanishing tail'); plt.semilogy(n,tail_bad,label='slow/non-summable-looking tail')
plt.xlabel('window n'); plt.ylabel('tail budget')
plt.legend(); plt.title('Finite windows need a tail bridge')
plt.tight_layout(); plt.savefig(out/'plancherel_tail_models_step99.png', dpi=160); plt.close()

Lambda=np.arange(1,101,dtype=float)
budget=1/Lambda
with (out/'completed_lower_frame_budget_step99.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['Lambda_n','currency_bound'])
    for L,b in zip(Lambda,budget): w.writerow([float(L),float(b)])
plt.figure(figsize=(6,4)); plt.plot(Lambda,budget)
plt.xlabel('lower-frame constant Lambda_n'); plt.ylabel('budget bound 1/Lambda_n')
plt.title('Completed lower-frame growth collapses currency')
plt.tight_layout(); plt.savefig(out/'completed_lower_frame_budget_step99.png', dpi=160); plt.close()

# measure deformation for local factors small primes as function xi
xis=np.linspace(-20,20,801)
primes=[2,3,5,7]
rows=[]
prod=np.ones_like(xis)
for p in primes:
    Lp=1/np.abs(1 - p**(-0.5+1j*xis))**2 # |(1-p^{-1/2+i xi})^{-1}|^2
    prod*=Lp
    rows.append((p, float(np.min(Lp)), float(np.max(Lp))))
with (out/'semilocal_measure_deformation_step99.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['prime','min_local_factor_weight','max_local_factor_weight'])
    for row in rows: w.writerow(row)
plt.figure(figsize=(6,4)); plt.plot(xis,prod)
plt.xlabel('xi'); plt.ylabel('product local factor weight for p<=7')
plt.title('Semilocal measure changes with finite places')
plt.tight_layout(); plt.savefig(out/'semilocal_measure_deformation_step99.png', dpi=160); plt.close()

# Structural LaTeX balance check
text=tex
checks=[]
for env in ['theorem','lemma','definition','warning','proof','enumerate']:
    checks.append([env, text.count('\\begin{'+env+'}'), text.count('\\end{'+env+'}')])
with (out/'latex_structure_check_step99.csv').open('w', newline='') as f:
    w=csv.writer(f); w.writerow(['environment','begin_count','end_count']); w.writerows(checks)

# Zip all artifacts
zip_path=out/'step99_plancherel_exhaustivity_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, p.name)
print('created', zip_path)
