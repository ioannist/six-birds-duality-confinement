from pathlib import Path
import numpy as np, csv, json, zipfile
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step109_matrix_moment_prototype')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(109)

def psd_sqrt_inv(A, tol=1e-12):
    A = (A + A.T.conj())/2
    w, V = np.linalg.eigh(A)
    wc = np.clip(w, tol, None)
    return (V*np.sqrt(wc))@V.T.conj(), (V*(1/np.sqrt(wc)))@V.T.conj(), w

def eigvals_gen(A, B, tol=1e-12):
    _, Binv, _ = psd_sqrt_inv(B, tol)
    M = Binv @ ((A + A.T.conj())/2) @ Binv
    return np.linalg.eigvalsh((M + M.T.conj())/2).real

def min_gen_eig(A, B, tol=1e-12):
    return float(eigvals_gen(A,B,tol)[0])

# Finite boundary dictionary prototype.
D = 18
M = 72
A = rng.normal(size=(D,D))
G_B = A.T @ A + 0.75*np.eye(D)
Dscale = np.diag(1/np.sqrt(np.diag(G_B)))
G_B = Dscale @ G_B @ Dscale
Q, _ = np.linalg.qr(rng.normal(size=(M,D)))
V, _ = np.linalg.qr(rng.normal(size=(D,D)))
B_sqrt, _, _ = psd_sqrt_inv(G_B)
sig_good = np.linspace(1.45, 0.48, D)
sig_bad = sig_good.copy(); sig_bad[-4:] = 0.0
R_good = Q @ np.diag(sig_good) @ V.T @ B_sqrt
R_bad = Q @ np.diag(sig_bad) @ V.T @ B_sqrt

gamma_full = 3.2
G_full = gamma_full*np.eye(M)
rank_part = int(0.56*M)
P_partial = np.zeros((M,M)); P_partial[:rank_part,:rank_part] = np.eye(rank_part)
G_partial = 5.0*P_partial
weights = 3.0*(1 - 0.65*np.exp(-np.arange(M)/12.0))
G_weighted = np.diag(weights)

F_good_full = R_good.T @ G_full @ R_good
F_good_weighted = R_good.T @ G_weighted @ R_good
F_bad_full = R_bad.T @ G_full @ R_bad
F_good_partial = R_good.T @ G_partial @ R_good

c_good = min_gen_eig(R_good.T@R_good, G_B)
c_bad = min_gen_eig(R_bad.T@R_bad, G_B)
gamma_w = float(np.linalg.eigvalsh(G_weighted)[0])
gamma_p = float(np.linalg.eigvalsh(G_partial)[0])

cases=[]
for name,R,G,F in [
    ('good_R_full_character_frame', R_good, G_full, F_good_full),
    ('good_R_weighted_near_frame', R_good, G_weighted, F_good_weighted),
    ('good_R_partial_character_window', R_good, G_partial, F_good_partial),
    ('rank_deficient_R_full_character_frame', R_bad, G_full, F_bad_full),
]:
    c = min_gen_eig(R.T@R, G_B)
    gamma = float(np.linalg.eigvalsh((G+G.T.conj())/2)[0])
    actual = min_gen_eig(F, G_B)
    y = rng.normal(size=D); y = y/np.sqrt(y.T@G_B@y)
    cases.append({
        'case':name,
        'dim_boundary':D,
        'dim_coefficients':M,
        'rank_R':int(np.linalg.matrix_rank(R, tol=1e-10)),
        'rank_G':int(np.linalg.matrix_rank(G, tol=1e-10)),
        'c_N_min_gen_eig_RstarR_vs_GB':c,
        'gamma_N_min_eig_G':gamma,
        'gamma_times_c':gamma*c,
        'actual_min_gen_eig_F_vs_GB':actual,
        'random_scalar_direction_strength':float(y.T@F@y),
        'passes_strict_lower_frame':bool(actual>1e-8),
    })

# Defect theorem sanity.
gamma_target = 3.0
E_G = np.maximum(gamma_target - weights, 0.0)
E_G_mat = np.diag(E_G)
c_target = c_good + 0.12
E_R = c_target*G_B - R_good.T@R_good
w_er,V_er=np.linalg.eigh((E_R+E_R.T)/2)
E_R_plus=(V_er*np.maximum(w_er,0))@V_er.T
cert_bound = gamma_target*c_target*G_B - gamma_target*E_R_plus - R_good.T@E_G_mat@R_good
defect_slack_eigs = eigvals_gen(F_good_weighted-cert_bound, G_B)

# Rank-one scalar lower moment countermodel.
a0 = rng.normal(size=M); a0 = a0/np.linalg.norm(a0)
G_rank1 = 50*np.outer(a0,a0)
F_rank1 = R_good.T@G_rank1@R_good
rank1_eigs = eigvals_gen(F_rank1, G_B)
scalar_vec = R_good.T@a0
if np.linalg.norm(scalar_vec)>1e-12:
    y0 = np.linalg.solve(G_B, scalar_vec)
    y0 = y0/np.sqrt(y0.T@G_B@y0)
    rank1_scalar_strength = float(y0.T@F_rank1@y0)
else:
    rank1_scalar_strength = 0.0

# Write CSVs.
def write_csv(path, rows, fields):
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
write_csv(OUT/'matrix_lower_frame_cases_step109.csv', cases, list(cases[0].keys()))

eig_rows=[]
for name,F in [('full',F_good_full),('weighted',F_good_weighted),('partial',F_good_partial),('rank_deficient',F_bad_full),('rank_one_scalar',F_rank1)]:
    for i,e in enumerate(eigvals_gen(F,G_B)):
        eig_rows.append({'case':name,'eigen_index':i+1,'generalized_eigenvalue':float(e)})
write_csv(OUT/'source_frame_eigenvalues_step109.csv', eig_rows, ['case','eigen_index','generalized_eigenvalue'])

write_csv(OUT/'matrix_moment_gate_table_step109.csv', [
    {'gate':'G1 finite boundary Hilbert record','mathematical_record':'G_B positive definite on Y_{B,N}; null quotient applied','status':'accepted in finite prototype','failure_if_missing':'pseudoinverse can hide zero-cost boundary directions'},
    {'gate':'G2 coefficient observability','mathematical_record':'R_N^*R_N >= c_N G_B - E_R','status':'tested; c_N computed','failure_if_missing':'characters cannot charge directions invisible to coefficients'},
    {'gate':'G3 character/mollifier matrix moment','mathematical_record':'G_X >= gamma_N I - E_G','status':'formal theorem plus toy cases','failure_if_missing':'scalar moment can be rank-one and miss recombinations'},
    {'gate':'G4 lower-frame transfer','mathematical_record':'R_N^*G_XR_N >= gamma_N c_N G_B - defects','status':'proved finite theorem','failure_if_missing':'no source absorption of boundary packets'},
    {'gate':'G5 completed promotion','mathematical_record':'finite Y_{B,N} exhausts completed Burnol/Sonine boundary sector','status':'not earned here','failure_if_missing':'moving-window support only'},
    {'gate':'G6 all-six no-smuggling','mathematical_record':'source family declared upstream, not target-selected','status':'recorded as obligation','failure_if_missing':'post-hoc source choices invalidate proof'},
], ['gate','mathematical_record','status','failure_if_missing'])

write_csv(OUT/'arithmetic_input_table_step109.csv', [
    {'input':'Heap-Soundararajan scalar lower moments','what_it_must_supply':'source strength and short Dirichlet polynomial mean-value template','current_status':'scalar only; operator lift still open','literature_source':'2007.13154'},
    {'input':'finite character orthogonality','what_it_must_supply':'local coefficient-space Gram lower frame','current_status':'exact on finite quotient only','literature_source':'finite abelian character theory'},
    {'input':'Burnol Sonine carrier','what_it_must_supply':'boundary/zero evaluator space and exhaustivity language','current_status':'structural carrier adopted; finite dictionary model only','literature_source':'0203120 / 0112254 / AIF 2007'},
    {'input':'CCM semilocal Hardy-Titchmarsh','what_it_must_supply':'common semilocal response geometry','current_status':'ambient room adopted; no compact repair assumed','literature_source':'2310.18423'},
    {'input':'Conrey-Li survival test','what_it_must_supply':'avoid RKHS/de Branges shift-positivity collapse','current_status':'active warning','literature_source':'9812166'},
], ['input','what_it_must_supply','current_status','literature_source'])

write_csv(OUT/'theorem_map_step109.csv', [
    {'label':'T109.1','statement':'If G_X >= gamma I and R^*R >= c G_B, then R^*G_XR >= gamma c G_B.','role':'finite transfer theorem','status':'proved'},
    {'label':'T109.2','statement':'With defects G_X >= gamma I - E_G and R^*R >= cG_B - E_R, lower frame holds modulo gamma E_R + R^*E_G R.','role':'defect-paid transfer','status':'proved'},
    {'label':'T109.3','statement':'A scalar/rank-one source can be positive on one direction but have zero lower-frame constant on dim>1 spaces.','role':'scalar insufficiency','status':'proved/countermodel'},
    {'label':'T109.4','statement':'Finite character tight frames supply G_X locally; completed RH use requires Burnol/Sonine exhaustivity and tail promotion.','role':'promotion obligation','status':'stated'},
], ['label','statement','role','status'])

summary = {
    'step':109,
    'title':'Finite Matrix Moment Lower-Bound Prototype',
    'dimensions':{'boundary_dim':D,'coefficient_dim':M},
    'constants':{
        'c_good':float(c_good), 'c_bad':float(c_bad), 'gamma_full':float(gamma_full),
        'gamma_weighted':float(gamma_w), 'gamma_partial':float(gamma_p),
        'min_defect_slack':float(np.min(defect_slack_eigs)),
        'rank_one_min_generalized_eigenvalue':float(np.min(rank1_eigs)),
        'rank_one_scalar_strength':rank1_scalar_strength,
    },
    'main_formula':'R_N^* G_{X,N} R_N >= gamma_N c_N G_{B,N} minus declared defects',
    'nonclaim':'No RH proof; no completed Burnol/Sonine exhaustivity; no actual Heap-Soundararajan matrix moment estimate yet.'
}
with open(OUT/'finite_matrix_moment_sanity_step109.json','w') as f: json.dump(summary,f,indent=2)

# Plots.
plt.figure(figsize=(7,4.5))
for name in ['full','weighted','partial','rank_deficient','rank_one_scalar']:
    eigs=[r['generalized_eigenvalue'] for r in eig_rows if r['case']==name]
    plt.plot(range(1,len(eigs)+1), eigs, marker='o', markersize=3, linewidth=1, label=name)
plt.xlabel('Generalized eigenvalue index'); plt.ylabel('Eigenvalue relative to boundary Gram')
plt.title('Finite boundary source-frame spectra'); plt.legend(fontsize=8); plt.tight_layout()
plt.savefig(OUT/'source_frame_spectra_step109.png', dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
labels=[c['case'].replace('_','\n') for c in cases]
actual=[c['actual_min_gen_eig_F_vs_GB'] for c in cases]
bound=[c['gamma_times_c'] for c in cases]
x=np.arange(len(labels)); width=0.35
plt.bar(x-width/2, actual, width, label='actual min eig')
plt.bar(x+width/2, bound, width, label='gamma*c bound')
plt.xticks(x, labels, fontsize=7); plt.ylabel('Lower-frame constant')
plt.title('Finite matrix lower-bound prototype'); plt.legend(fontsize=8); plt.tight_layout()
plt.savefig(OUT/'matrix_lower_bound_cases_step109.png', dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(range(1,len(rank1_eigs)+1), np.sort(rank1_eigs), marker='o', markersize=3)
plt.axhline(0, linewidth=1); plt.xlabel('Eigenvalue index'); plt.ylabel('Generalized eigenvalue')
plt.title('Scalar/rank-one source: positive direction but no lower frame'); plt.tight_layout()
plt.savefig(OUT/'scalar_rank_one_insufficiency_step109.png', dpi=180); plt.close()

svals_good=np.sqrt(np.clip(eigvals_gen(R_good.T@R_good,G_B),0,None))
svals_bad=np.sqrt(np.clip(eigvals_gen(R_bad.T@R_bad,G_B),0,None))
plt.figure(figsize=(7,4.5))
plt.plot(range(1,D+1), np.sort(svals_good)[::-1], marker='o', label='observable R_N')
plt.plot(range(1,D+1), np.sort(svals_bad)[::-1], marker='o', label='rank-deficient R_N')
plt.xlabel('Singular-value index'); plt.ylabel('Boundary-observability singular value')
plt.title('Coefficient observability: R_N must see every boundary direction')
plt.legend(fontsize=8); plt.tight_layout()
plt.savefig(OUT/'coefficient_observability_step109.png', dpi=180); plt.close()

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{booktabs}
\title{Step 109: Finite Matrix Moment Lower-Bound Prototype}
\author{RATCHET/Six Birds RH Membrane Program}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\begin{document}
\maketitle

\section{Purpose}
Step 108 constructed the finite boundary-packet coefficient problem
\[
Y_{\mathcal B,N},\qquad R_N:Y_{\mathcal B,N}\to \mathbb C^{\mathcal N_N},
\qquad F_{\mathcal B,N}=R_N^*G_{\mathcal X,N}R_N.
\]
Step 109 proves the finite matrix theorem that this construction must satisfy before any Heap--Soundararajan-style source strength can become a boundary-sector membrane.

\section{Finite setup}
Let $(Y,G_B)$ be a finite-dimensional boundary-packet Hilbert space, with
\[
\|y\|_B^2=\langle y,G_By\rangle,\qquad G_B\succ0.
\]
Let $R:Y\to \mathbb C^{\mathcal N}$ be the coefficient map sending a boundary packet to a short Dirichlet-polynomial coefficient vector. Let $G_X\succeq0$ be the character/source Gram matrix
\[
G_X(m,n)=\sum_{\chi\in\mathcal X}\lambda_\chi\chi(n)\overline{\chi(m)}.
\]
The induced source frame on boundary space is
\[
F_B=R^*G_XR.
\]

\section{Main theorem}
\begin{theorem}[Matrix moment lower-frame transfer]
If
\[
G_X\succeq \gamma I_{\mathcal N},\qquad R^*R\succeq cG_B,
\]
then
\[
\boxed{R^*G_XR\succeq \gamma cG_B.}
\]
\end{theorem}
\begin{proof}
For every $y\in Y$,
\[
\langle y,R^*G_XRy\rangle=\langle Ry,G_XRy\rangle\ge \gamma\|Ry\|^2=\gamma\langle y,R^*Ry\rangle\ge \gamma c\langle y,G_By\rangle.
\]
\end{proof}

\begin{theorem}[Defect-paid transfer]
If
\[
G_X\succeq \gamma I-E_G,\qquad R^*R\succeq cG_B-E_R,
\]
then
\[
\boxed{R^*G_XR\succeq\gamma cG_B-\gamma E_R-R^*E_GR.}
\]
\end{theorem}

\section{What Heap--Soundararajan must supply}
Heap--Soundararajan give a scalar source-strength template through short Dirichlet polynomials and mean-value estimates. The framework translation is the operator-valued matrix moment bound
\[
G_X\succeq \gamma I-E_G.
\]
This is stronger than one scalar lower moment: it must charge every coefficient recombination visible from the boundary-packet sector.

\section{Coefficient observability}
The second needed input is
\[
R^*R\succeq cG_B-E_R.
\]
If $\ker R\neq0$, no character Gram matrix can charge the invisible boundary directions through this route. Thus coefficient visibility is an adequacy gate.

\section{Scalar lower moment is insufficient}
\begin{proposition}[Rank-one scalar source obstruction]
If $\dim Y>1$ and $G_X=aa^*$ has rank one, then $R^*G_XR$ has rank at most one. Hence it cannot dominate $cG_B$ for any $c>0$ unless the boundary space is one-dimensional in the visible sector.
\end{proposition}

\section{Status}
Step 109 proves the finite matrix transfer theorem. It does not prove the arithmetic lower-frame estimate. The next target is to construct matrix moment estimates for $G_X$ and coefficient observability estimates for $R_N$ on genuine Burnol/Sonine boundary dictionaries.
\end{document}
'''
(OUT/'finite_matrix_moment_lower_bound_step109.tex').write_text(tex)

summary_md = f"""# Step 109: Finite Matrix Moment Lower-Bound Prototype

## Main theorem

Let `R_N:Y_B,N -> C^N` be the boundary coefficient map and let `G_X,N` be the character/mollifier source Gram. If

```math
G_{{X,N}} \\succeq \\gamma_N I,\\qquad R_N^*R_N \\succeq c_NG_{{B,N}},
```

then

```math
R_N^*G_{{X,N}}R_N \\succeq \\gamma_Nc_NG_{{B,N}}.
```

With defects, `G_X >= gamma I - E_G` and `R^*R >= cG_B - E_R` imply

```math
R^*G_XR \\succeq \\gamma cG_B-\\gamma E_R-R^*E_GR.
```

## Finite toy checks

Boundary dimension: `{D}`. Coefficient dimension: `{M}`.

Observable coefficient map constant: `c_N ≈ {c_good:.6g}`.

Rank-deficient coefficient map constant: `c_N ≈ {c_bad:.6g}`.

Full coefficient-frame lower constant: `gamma = {gamma_full:.6g}`.

Defect theorem minimum slack: `{float(np.min(defect_slack_eigs)):.6g}`.

Rank-one scalar-source minimum generalized eigenvalue: `{float(np.min(rank1_eigs)):.6g}`.

## Nonclaim

This is not RH evidence. It is a finite algebraic prototype identifying exactly what arithmetic estimates must supply.
"""
(OUT/'step109_results_summary.md').write_text(summary_md)

(OUT/'nonclaim_boundary_step109.md').write_text('''# Nonclaim Boundary — Step 109

This step does not prove RH.

It does not prove a Heap--Soundararajan operator-valued moment theorem.

It does not prove completed Burnol/Sonine exhaustivity.

It proves only the finite matrix transfer theorem.
''')

zip_path=OUT/'step109_matrix_moment_prototype_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print(json.dumps(summary, indent=2))
