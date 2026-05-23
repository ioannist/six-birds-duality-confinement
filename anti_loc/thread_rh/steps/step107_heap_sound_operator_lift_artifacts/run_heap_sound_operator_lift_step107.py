import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json, zipfile, math

OUT = Path('/mnt/data/rh_membrane_step107_heap_sound_operator_lift')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20260513)

# 1. Finite character tight-frame checks for cyclic finite group G = Z/NZ.
rows=[]
for N in [16, 32, 64, 96, 128]:
    j = np.arange(N)[:,None]
    n = np.arange(N)[None,:]
    Q = np.exp(2j*np.pi*j*n/N)/np.sqrt(N)
    F = Q.conj().T @ Q
    eig = np.linalg.eigvalsh(F).real
    rows.append({'N':N,'scenario':'full_character_family','rank':np.linalg.matrix_rank(F, tol=1e-10),'min_eig':eig[0],'max_eig':eig[-1],'condition_number':eig[-1]/max(eig[0],1e-300),'fro_error_to_identity':np.linalg.norm(F-np.eye(N),'fro')})
    # partial characters first N/2: rank deficient
    m=N//2
    Qp=Q[:m,:]
    Fp=Qp.conj().T@Qp
    eigp=np.linalg.eigvalsh(Fp).real
    rows.append({'N':N,'scenario':'partial_character_half','rank':np.linalg.matrix_rank(Fp, tol=1e-10),'min_eig':eigp[0],'max_eig':eigp[-1],'condition_number':np.inf if eigp[0]<1e-12 else eigp[-1]/eigp[0],'fro_error_to_identity':np.linalg.norm(Fp-np.eye(N),'fro')})

pd.DataFrame(rows).to_csv(OUT/'finite_character_frame_checks_step107.csv', index=False)

# 2. Scalar lower-bound vs operator lower-frame countermodel.
# A scalar mollifier vector a has positive quadratic mass a^* a but rank-one frame.
rows=[]
for d in [8,16,32,64,128]:
    a = np.exp(-np.arange(d)/max(5,d/8))
    a = a/np.linalg.norm(a)
    F = np.outer(a,a)
    eig=np.linalg.eigvalsh(F).real
    rows.append({'dimension':d,'scenario':'single_scalar_mollifier','scalar_strength_on_a':float(a@F@a),'rank':np.linalg.matrix_rank(F, tol=1e-10),'min_eig':eig[0],'max_eig':eig[-1]})
    # Build d cyclic shifts of a: positive dictionary that spans all directions.
    F2=np.zeros((d,d))
    for s in range(d):
        b=np.roll(a,s)
        F2+=np.outer(b,b)
    F2=F2/d
    eig2=np.linalg.eigvalsh(F2).real
    rows.append({'dimension':d,'scenario':'cyclic_shift_mollifier_dictionary','scalar_strength_on_a':float(a@F2@a),'rank':np.linalg.matrix_rank(F2, tol=1e-10),'min_eig':eig2[0],'max_eig':eig2[-1]})

pd.DataFrame(rows).to_csv(OUT/'scalar_vs_operator_lift_checks_step107.csv', index=False)

# 3. Boundary-packet source absorption model.
# Boundary sector dimension d, sources added cumulatively; compare full coverage versus missing tail.
d=80
Theta_inv=np.diag(1+0.02*np.arange(d))
scenarios=[]
for m in range(1,d+1):
    # full ordered coverage: first m coordinate sensors, with strength Lambda=log(2+m)
    Lam=np.log(2+m)
    F=np.zeros((d,d))
    for i in range(m):
        F[i,i]+=Lam*Theta_inv[i,i]
    eig=np.linalg.eigvalsh(F - Lam*Theta_inv).real
    # we measure min eig of F relative to Theta_inv on covered subspace and full space
    covered_min = min([F[i,i]/Theta_inv[i,i] for i in range(m)]) if m>0 else 0
    full_generalized_min = min([F[i,i]/Theta_inv[i,i] for i in range(d)])
    scenarios.append({'m_sources':m,'scenario':'ordered_coordinate_sources','Lambda':Lam,'covered_min':covered_min,'full_min':full_generalized_min,'full_gate_pass': full_generalized_min>=Lam-1e-12})
    # random dense sources, normalized; cumulative frame scaled to produce increasing coverage
    # Generate m random sensors and frame; normalize by d/m to compare.
    R=rng.normal(size=(m,d))
    R=R/np.linalg.norm(R,axis=1,keepdims=True)
    Fr=(R.T@R)*(d/m)*Lam
    # generalized eig approximate by Theta^{-1/2} F Theta^{-1/2}
    Dinv_sqrt=np.diag(1/np.sqrt(np.diag(Theta_inv)))
    G=Dinv_sqrt@Fr@Dinv_sqrt
    eigg=np.linalg.eigvalsh(G).real
    scenarios.append({'m_sources':m,'scenario':'random_dense_sources','Lambda':Lam,'covered_min':np.nan,'full_min':eigg[0],'full_gate_pass':eigg[0]>=Lam-1e-12})

pd.DataFrame(scenarios).to_csv(OUT/'boundary_source_absorption_ladder_step107.csv', index=False)

# 4. Model of HS block prime intervals: source strength grows like product over blocks exp(k^2 sum 1/p) ~ (log T)^k^2.
# We use simplified P_j sequence and source strength accumulation.
rows=[]
for k in [0.25,0.5,1.0,2.0]:
    for J in range(2,15):
        Pj=np.array([2*np.log((j+1)/j) + 0.1/(j+1) for j in range(2,J+1)])
        log_strength=(k**2)*Pj.sum()
        strength=np.exp(log_strength)
        rows.append({'k':k,'blocks':J,'sum_Pj':Pj.sum(),'lambda_model':strength,'budget_model':1/strength})
pd.DataFrame(rows).to_csv(OUT/'heap_sound_source_strength_model_step107.csv', index=False)

# 5. Tables: gate statuses and construction tasks.
gate_rows=[
    {'gate':'HS scalar positive bilinear form','status':'accepted as scalar template','meaning':'The dual mollifier proof supplies positive short-Dirichlet-polynomial mean values and divergent scalar strength.'},
    {'gate':'operator-valued lift','status':'unearned','meaning':'Need a matrix lower bound uniformly for all boundary-sector recombinations, not just one mollifier direction.'},
    {'gate':'finite character orthogonality','status':'accepted locally','meaning':'Complete characters give exact tight frames on finite quotients.'},
    {'gate':'completed Burnol/Sonine carrier','status':'plausible / imported from Burnol','meaning':'Use Burnol La/Ka/Sonine spaces and zero evaluators as the carrier and ledger backbone.'},
    {'gate':'boundary-packet source coverage','status':'active target','meaning':'Show character/mollifier sources charge the noncompact sector generated by shifted Sonin blocks.'},
    {'gate':'tail/exhaustivity','status':'required','meaning':'Finite conductor/source windows promote only with a vanishing completed-tail record.'},
    {'gate':'Conrey-Li survival','status':'active warning','meaning':'Do not collapse the construction into de Branges/RKHS shift positivity.'}
]
pd.DataFrame(gate_rows).to_csv(OUT/'operator_lift_gate_table_step107.csv', index=False)

input_rows=[
    {'input':'Mean value of L(1/2) times short Dirichlet polynomials','source':'Heap--Soundararajan template','needed_for':'scalar source strength and diagonal main terms'},
    {'input':'Second / weighted moment control','source':'Heap--Soundararajan Propositions 2--3 template','needed_for':'Holder/duality bounds and defect control'},
    {'input':'Matrix moment asymptotics for a family of mollifier coefficient vectors','source':'new required lift','needed_for':'operator lower frame on boundary sector'},
    {'input':'Finite character orthogonality on conductor quotients','source':'standard character theory','needed_for':'local tight frame before promotion'},
    {'input':'Burnol Sonine completeness/minimality','source':'Burnol','needed_for':'fixed/exhaustive zero ledger and carrier identification'},
    {'input':'Semilocal Hardy--Titchmarsh transport','source':'CCM semilocal framework','needed_for':'placing sources and boundary packets in common response geometry'}
]
pd.DataFrame(input_rows).to_csv(OUT/'arithmetic_input_table_step107.csv', index=False)

status_rows=[
    {'claim':'Scalar lower moments imply source strength','verdict':'yes, scalar only','reason':'The method gives large positive scalar means for selected mollifiers.'},
    {'claim':'Scalar lower moments imply operator lower frame','verdict':'no','reason':'A rank-one positive form can have large scalar value but zero minimum eigenvalue.'},
    {'claim':'Full finite character family gives finite lower frame','verdict':'yes locally','reason':'Orthogonality gives identity on the finite quotient.'},
    {'claim':'Finite windows give completed RH lower frame','verdict':'no without tail','reason':'The window may miss an infinite-dimensional complement.'},
    {'claim':'Operator-valued HS lift is plausible','verdict':'yes but new','reason':'Requires matrix moment estimates for a spanning dictionary of mollifiers/sources.'}
]
pd.DataFrame(status_rows).to_csv(OUT/'route_status_step107.csv', index=False)

# plots
plt.figure(figsize=(6,4))
df=pd.read_csv(OUT/'scalar_vs_operator_lift_checks_step107.csv')
for scen in df['scenario'].unique():
    sub=df[df.scenario==scen]
    plt.plot(sub['dimension'], sub['min_eig'], marker='o', label=scen)
plt.yscale('symlog', linthresh=1e-12)
plt.xlabel('boundary model dimension')
plt.ylabel('minimum eigenvalue of source frame')
plt.title('Scalar mollifier strength vs operator lower frame')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'scalar_vs_operator_lift_step107.png', dpi=200)
plt.close()

plt.figure(figsize=(6,4))
df=pd.read_csv(OUT/'boundary_source_absorption_ladder_step107.csv')
for scen in ['ordered_coordinate_sources','random_dense_sources']:
    sub=df[df.scenario==scen]
    plt.plot(sub['m_sources'], sub['full_min'], label=scen)
plt.xlabel('number of source records')
plt.ylabel('full-sector generalized lower bound')
plt.title('Boundary-sector source coverage requires full lower frame')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'boundary_source_absorption_ladder_step107.png', dpi=200)
plt.close()

plt.figure(figsize=(6,4))
df=pd.read_csv(OUT/'heap_sound_source_strength_model_step107.csv')
for k in sorted(df.k.unique()):
    sub=df[df.k==k]
    plt.plot(sub['blocks'], sub['lambda_model'], marker='o', label=f'k={k}')
plt.yscale('log')
plt.xlabel('number of prime blocks')
plt.ylabel('toy scalar strength Λ')
plt.title('Heap--Soundararajan-style cumulative source strength')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'heap_sound_source_strength_model_step107.png', dpi=200)
plt.close()

plt.figure(figsize=(6,4))
df=pd.read_csv(OUT/'finite_character_frame_checks_step107.csv')
for scen in ['full_character_family','partial_character_half']:
    sub=df[df.scenario==scen]
    plt.plot(sub['N'], sub['min_eig'], marker='o', label=scen)
plt.xlabel('finite group size')
plt.ylabel('minimum eigenvalue')
plt.title('Finite character orthogonality is local, partial families fail')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'finite_character_frame_step107.png', dpi=200)
plt.close()

# JSON schema
schema={
    'step':107,
    'title':'Heap--Soundararajan operator-valued lift test',
    'objects':{
        'Y_B_N':'finite Burnol/Sonine boundary-packet model',
        'Q_omega':'character/source readout on boundary sector',
        'F_n':'sum lambda_omega Q_omega^* Theta_omega^{-1} Q_omega',
        'HS_scalar_form':'short-Dirichlet-polynomial positive bilinear form from dual mollifier method',
        'operator_lift_gate':'F_n >= Lambda_n Theta_0^{-1} on all native boundary recombinations'
    },
    'verdict':'Scalar HS lower bounds are a source-strength template but do not by themselves imply an operator lower frame. The lift needs matrix moment estimates or exact finite-character tight frames plus completed tail/exhaustivity.',
    'next_step':'Build a concrete finite Burnol/Sonine boundary dictionary and define the mollifier coefficient map R_N whose matrix moments must be estimated.'
}
with open(OUT/'step107_schema.json','w') as f:
    json.dump(schema,f,indent=2)

# summary md and latex
summary = r"""
# Step 107 — Heap--Soundararajan operator-valued lift test

This step tests whether the Heap--Soundararajan dual mollifier mechanism can be promoted from scalar lower-moment strength to the operator-valued lower frame needed by the boundary-packet source route.

## Verdict

The scalar mechanism is a strong template, but it is not yet an operator lower frame.

A single positive mollifier direction can have large scalar strength while the associated source matrix is rank one. Therefore it cannot charge every recombination in the Burnol/Sonine boundary sector.

The accepted lift would require a matrix moment theorem:

```math
F_n=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_\omega^*\Theta_\omega^{-1}Q_\omega
\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty .
```

The Heap--Soundararajan proof supplies the scalar prototype for the growth of `Lambda_n`; finite character orthogonality supplies the local tight-frame mechanism. The missing work is the uniform operator-valued lift on the completed boundary-packet carrier.

## Key no-go

A scalar lower bound on one chosen mollifier vector does not imply a lower frame. In finite dimensions,

```math
F=a a^*
```

has positive value on `a`, but zero minimum eigenvalue on every dimension greater than one.

## What would work

A family of mollifiers/source readouts whose coefficient vectors span the boundary model, with matrix moment asymptotics proving a uniform lower eigenvalue.

## Next target

Build a concrete finite Burnol/Sonine boundary dictionary and define the coefficient map `R_N` so that the operator-valued moment problem becomes explicit.
"""
(OUT/'step107_results_summary.md').write_text(summary)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,enumitem,geometry}
\geometry{margin=1in}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}
\newcommand{\cX}{\mathcal X}
\newcommand{\cB}{\mathcal B}
\newcommand{\cN}{\mathcal N}
\newcommand{\cS}{\mathcal S}
\newcommand{\eps}{\varepsilon}
\newcommand{\Ran}{\operatorname{Ran}}
\newcommand{\diag}{\operatorname{diag}}
\title{Step 107: Heap--Soundararajan Operator-Valued Lift Test}
\author{Six Birds RH Membrane Program}
\date{}
\begin{document}
\maketitle

\section{Purpose}
Steps 104--106 identified a noncompact boundary-packet sector generated by shifted Sonin/prolate off-diagonal blocks.  Compact repair cannot remove this sector.  The current route is therefore a source-coercivity route: construct lawful Hecke/Dirichlet sources charging the full boundary sector.

This note tests whether the Heap--Soundararajan dual mollifier mechanism can be lifted from scalar lower moment estimates to the operator-valued lower-frame inequality required by the membrane theorem.

\section{The required operator inequality}
Let $Y_{\cB,N}$ be a finite boundary-packet model for the Burnol/Sonine boundary sector.  A source family consists of response maps
\[
        Q_\omega:Y_{\cB,N}\to Z_\omega,
        \qquad \omega\in\cX_n,
\]
with positive weights $\lambda_{\omega,n}$ and budgets $\Theta_\omega$.  The source frame is
\[
        F_n=\sum_{\omega\in\cX_n}\lambda_{\omega,n}
        Q_\omega^*\Theta_\omega^{-1}Q_\omega.
\]
The accepted lower-frame gate is
\begin{equation}\label{eq:lower-frame}
        F_n\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty.
\end{equation}
This is a matrix inequality.  It is stronger than any scalar lower moment estimate along a single vector.

\section{Heap--Soundararajan scalar template}
The Heap--Soundararajan construction chooses short Dirichlet polynomials
\[
        \mathcal N(s,\alpha)=\sum_{n\in\mathcal N}
        \frac{\alpha^{\Omega(n)}g(n)}{n^s},
\]
where $\mathcal N$ is built from prime blocks and has length short enough to permit mean-value computation.  The scalar proof estimates three quantities: a main twisted first moment, a mollified second moment, and a weighted mollifier moment, then applies Holder.

The membrane interpretation is:
\[
        \text{short mollifier mean values}
        \quad\leadsto\quad
        \text{positive scalar source strength.}
\]
The desired lift is:
\[
        \text{matrix moment estimates for a family of mollifier directions}
        \quad\leadsto\quad
        \text{operator lower frame.}
\]

\section{Scalar strength does not imply a lower frame}
\begin{lemma}[rank-one obstruction]
Let $Y$ be a Hilbert space with $\dim Y>1$, and let $a\in Y$ be nonzero.  The form
\[
        F=aa^*
\]
has positive scalar strength in the direction $a$, namely
\[
        \langle a,Fa\rangle=\|a\|^4>0,
\]
but it is not a lower frame on $Y$:
\[
        \lambda_{\min}(F)=0.
\]
\end{lemma}
\begin{proof}
Every vector orthogonal to $a$ lies in $\ker F$.  Thus no positive multiple of the identity is dominated by $F$.
\end{proof}

\begin{remark}
This is the finite-dimensional version of the main warning.  A scalar lower bound for one dual mollifier cannot certify the boundary-sector membrane.  It certifies only one source direction.
\end{remark}

\section{Finite character orthogonality gives the local model}
Let $G$ be a finite abelian group and $\widehat G$ its character group.  With normalized characters,
\[
        Q_\chi f=|G|^{-1/2}\sum_{x\in G}f(x)\overline{\chi(x)},
\]
one has
\[
        \sum_{\chi\in\widehat G}Q_\chi^*Q_\chi=I_{\ell^2(G)}.
\]
Thus complete character families are exact finite tight frames.

The completed RH source route needs this local statement promoted to the completed boundary-sector carrier with tail/exhaustivity.  Finite conductor windows alone remain support-only.

\section{Operator-valued Heap--Soundararajan lift}
Let $R_N:Y_{\cB,N}\to \mathbb C^{\cN_N}$ be the coefficient map that assigns to a boundary recombination $y$ the Dirichlet-polynomial coefficients
\[
        a_y(n),\qquad n\in\cN_N.
\]
For a character family $\cX_n$, define
\[
        Q_\omega y=\sum_{n\in\cN_N}a_y(n)\omega(n).
\]
Then
\[
        F_n=R_N^*G_nR_N,
        \qquad
        G_n(m,n)=\sum_{\omega\in\cX_n}\lambda_{\omega,n}\omega(n)\overline{\omega(m)}.
\]

\begin{proposition}[finite operator-lift gate]
Assume
\[
        G_n\succeq \gamma_n I_{\mathbb C^{\cN_N}}
        \quad\text{on the no-aliasing coefficient window}
\]
and
\[
        R_N^*R_N\succeq c_N(\Theta_{0,N}^-)^{-1}.
\]
Then
\[
        F_n\succeq \gamma_n c_N(\Theta_{0,N}^-)^{-1}.
\]
Thus $\Lambda_n=\gamma_n c_N$ is an accepted finite-window source lower frame.
\end{proposition}

\begin{proof}
For every $y\in Y_{\cB,N}$,
\[
        \langle y,F_ny\rangle
        =\langle R_Ny,G_nR_Ny\rangle
        \ge \gamma_n\|R_Ny\|^2
        \ge \gamma_n c_N\langle y,(\Theta_{0,N}^-)^{-1}y\rangle.
\]
\end{proof}

\section{What remains analytic}
The Heap--Soundararajan method supplies a scalar model for $\gamma_n$-growth through short Dirichlet-polynomial mean values.  To make it an operator-valued source frame one needs:
\begin{enumerate}[label=(\alph*)]
\item a boundary dictionary $R_N$ for Burnol/Sonine packets;
\item matrix moment estimates for $G_n(m,n)$, not only a single scalar moment;
\item a no-aliasing or tail-defect record for the finite coefficient window;
\item completed Plancherel/exhaustivity as $N,n\to\infty$;
\item all-six records forbidding target-selected mollifiers.
\end{enumerate}

\section{Conclusion}
The operator-valued lift is plausible but unearned.  The scalar dual-mollifier lower bounds are not enough.  The next concrete construction is the coefficient map $R_N$ from a finite Burnol/Sonine boundary-packet dictionary into the short Dirichlet-polynomial coefficient window.

\end{document}
'''
(OUT/'heap_sound_operator_lift_step107.tex').write_text(tex)

# zip
zip_path=OUT/'step107_heap_sound_operator_lift_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, p.name)
print('created', OUT)
