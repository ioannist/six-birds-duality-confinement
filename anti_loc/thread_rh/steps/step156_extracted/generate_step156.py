import os, csv, json, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step156_xi_bc_schatten_tail')
out.mkdir(parents=True, exist_ok=True)

step = 156

# --- synthetic models for the audit ---
n = np.arange(1, 401)
profiles = {
    'finite_rank_paid': np.where(n <= 18, 1/(1+0.07*n), 0.0),
    'trace_class_fast': n**(-1.35),
    'compact_not_trace': n**(-0.35),
    'noncompact_floor': 0.18 + 0.65*np.exp(-n/45),
    'oscillatory_floor': 0.12 + 0.08*np.abs(np.sin(n/9))*np.exp(-n/300),
}

# singular values plot
plt.figure(figsize=(8,5))
for label, s in profiles.items():
    plt.loglog(n, np.maximum(s, 1e-12), label=label.replace('_',' '))
plt.xlabel('index n')
plt.ylabel('singular value proxy s_n(A_ell)')
plt.title('Step 156: residual operator singular-value regimes')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'xi_bc_schatten_singular_profiles_step156.png', dpi=180)
plt.close()

# tail norm plot: operator tail and trace tail for profiles
rows_tail=[]
cutoffs = np.array([5,10,20,40,80,120,200,300])
plt.figure(figsize=(8,5))
for label, s in profiles.items():
    op_tail=[]
    for c in cutoffs:
        tail = s[c:]
        op = float(np.max(tail)) if len(tail)>0 else 0.0
        tr = float(np.sum(tail**2))
        op_tail.append(op)
        rows_tail.append({'profile':label,'cutoff_N':int(c),'operator_tail_norm':op,'trace_tail_proxy':tr})
    plt.plot(cutoffs, op_tail, marker='o', label=label.replace('_',' '))
plt.xlabel('finite window cutoff N')
plt.ylabel('operator tail norm proxy ||A(I-P_N)||')
plt.title('Step 156: compact/tail-payability proxy')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'xi_bc_tail_payability_step156.png', dpi=180)
plt.close()

with open(out/'xi_bc_tail_payability_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['profile','cutoff_N','operator_tail_norm','trace_tail_proxy'])
    w.writeheader(); w.writerows(rows_tail)

# Schatten classification table for p values
pvals = [0.5,1,2,4]
rows_schatten=[]
for label, s in profiles.items():
    compact = float(s[-1]) < 0.02
    for p in pvals:
        # Xi=A^*A in S_p iff sum s(A)^{2p}<infty; finite proxy
        partial = float(np.sum(np.maximum(s,1e-12)**(2*p)))
        tail_growth = float(np.sum(np.maximum(s[200:],1e-12)**(2*p)))
        if label.startswith('noncompact') or label.startswith('oscillatory'):
            verdict='fails_compactness_proxy'
        elif label == 'trace_class_fast':
            verdict='passes_many_schatten_proxy'
        elif label == 'compact_not_trace' and p <= 1:
            verdict='fails_trace_proxy_but_compact_possible'
        elif label == 'finite_rank_paid':
            verdict='finite_rank_proxy'
        else:
            verdict='conditional'
        rows_schatten.append({'profile':label,'p_for_Xi_Sp':p,'sum_singular_2p_proxy':partial,'tail_after_200_proxy':tail_growth,'verdict':verdict})
with open(out/'xi_bc_schatten_proxy_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['profile','p_for_Xi_Sp','sum_singular_2p_proxy','tail_after_200_proxy','verdict'])
    w.writeheader(); w.writerows(rows_schatten)

# Classification score plot
classes=['Exact','Compact/tail','Trace-class tail','Positive source absorption','Scoped residual']
status_score=[0.05,0.35,0.25,0.10,0.95]  # active residual is current status
plt.figure(figsize=(8,4.5))
plt.bar(classes, status_score)
plt.ylim(0,1.05)
plt.ylabel('current support score (diagnostic)')
plt.title('Step 156: current classification status for Xi^BC')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig(out/'xi_bc_classification_status_step156.png', dpi=180)
plt.close()

# Noncompact witness model
N=160
x=np.arange(N)
# Toeplitz-like shifted projection floor model: singulars near floor for first many modes
sing = 0.15 + 0.85/(1+np.exp((x-75)/10))
plt.figure(figsize=(8,4.5))
plt.plot(x+1, sing, marker='.', linewidth=1)
plt.xlabel('mode index')
plt.ylabel('singular value proxy')
plt.title('Step 156: boundary-packet noncompact witness proxy')
plt.tight_layout()
plt.savefig(out/'boundary_packet_noncompact_witness_step156.png', dpi=180)
plt.close()

with open(out/'boundary_packet_noncompact_witness_step156.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['mode_index','singular_value_proxy'])
    for i,s in enumerate(sing,1): w.writerow([i,float(s)])

# route table
route_rows = [
    {'status':'E_exact_exclusion','criterion':'A_ell=0 equivalently C_ell eta^a_{rho,k}=0 for all visible zero evaluators','current_verdict':'open_not_earned','next_record':'co-Poisson factorization or projected-kernel annihilation'},
    {'status':'T_compact_tail_payable','criterion':'A_ell compact on the pulled zero-evaluator closure; finite windows satisfy ||A_ell(I-Q_N)|| -> 0','current_verdict':'open_not_earned; raw boundary-packet model warns against assuming it','next_record':'prove compactness of restricted commutator or identify compact semilocal correction'},
    {'status':'TC_trace_class_tail','criterion':'Xi^BC=A_ell^*A_ell trace-class iff A_ell is Hilbert-Schmidt','current_verdict':'not_earned','next_record':'square-summable residual kernel diagonal/envelope'},
    {'status':'S_source_absorbable','criterion':'non-circular source record paying Xi^BC without positive fixed-ledger budget shortcut','current_verdict':'ordinary positive source squeeze blocked by Steps 148-150','next_record':'signed conservation/direct cancellation only'},
    {'status':'N_scoped_residual','criterion':'Xi^BC remains explicit adequacy residual in theorem statement','current_verdict':'active','next_record':'state theorem with Xi^BC budget/nonclaim boundary'},
]
with open(out/'xi_bc_schatten_tail_gate_table_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['status','criterion','current_verdict','next_record'])
    w.writeheader(); w.writerows(route_rows)

# theorem map
theorem_rows = [
    {'name':'Residual restriction identity','statement':'Let E_a=closure span{eta^a_{rho,k}} and A_ell=C_ell|_{E_a}. Then Xi^BC_ell=A_ell^*A_ell and R_ell(z,zprime)=<A_ell eta_z,A_ell eta_zprime>.','status':'proved_formal_reduction'},
    {'name':'Schatten equivalence','statement':'Xi^BC_ell in S_p iff A_ell in S_{2p}; in particular Xi trace-class iff A_ell is Hilbert-Schmidt.','status':'proved_functional_analysis'},
    {'name':'Compact tail criterion','statement':'A_ell compact iff for any finite-rank exhausting Q_N on E_a, ||A_ell(I-Q_N)|| -> 0; then Xi tail is operator-norm payable.','status':'proved_functional_analysis'},
    {'name':'Noncompact witness criterion','statement':'If there is an orthonormal sequence e_n in E_a with ||A_ell e_n|| >= c>0, then Xi^BC is not compact/tail-payable in operator norm.','status':'proved_functional_analysis'},
    {'name':'Actual Burnol/Sonin compactness','statement':'C_ell restricted to pulled zero-evaluator closure is compact or Hilbert-Schmidt.','status':'open_load_bearing'},
]
with open(out/'theorem_map_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['name','statement','status'])
    w.writeheader(); w.writerows(theorem_rows)

# route status
status_rows = [
    {'gate':'exact_exclusion','symbol':'A_ell=0','status':'not_proved'},
    {'gate':'compactness','symbol':'A_ell in K(E_a,H)','status':'not_proved'},
    {'gate':'trace_class','symbol':'A_ell in S_2','status':'not_proved'},
    {'gate':'noncompact_obstruction','symbol':'exists boundary orthonormal sequence with residual floor','status':'conditional_if_evaluator_closure_contains_boundary_packets'},
    {'gate':'scoped_residual','symbol':'Xi^BC carried explicitly','status':'active'},
]
with open(out/'route_status_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['gate','symbol','status'])
    w.writeheader(); w.writerows(status_rows)

# construction tasks
construct_rows = [
    {'task':'Define actual pulled evaluator closure E_a','description':'Specify topology/Gram normalization for eta^a_{rho,k}=J_a^*Y^a_{rho,k}.','priority':'high'},
    {'task':'Compute restricted commutator envelope','description':'Bound C_ell eta^a_{rho,k} using projected Sonine kernel, not ambient Hardy shadow.','priority':'high'},
    {'task':'Search for noncompact witness sequence','description':'Construct or refute a boundary-packet orthonormal sequence inside E_a with residual norm floor.','priority':'high'},
    {'task':'Trace/Hilbert-Schmidt diagonal test','description':'Estimate sum ||C_ell eta_z||^2 under a fixed positive evaluator weight schedule.','priority':'medium'},
    {'task':'Scoped residual theorem statement','description':'Prepare RH membrane theorem with Xi^BC as explicit active nonclaim if compactness/exclusion fails.','priority':'medium'},
]
with open(out/'construction_tasks_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['task','description','priority'])
    w.writeheader(); w.writerows(construct_rows)

# Nonclaim boundary
nonclaim = r"""
# Step 156 Nonclaim Boundary

This step does not prove RH, does not prove `H_R=0`, and does not prove `Xi^BC=0`.

It also does not prove that the residual commutator is compact, Hilbert--Schmidt, trace-class, or source-absorbable.

The positive source-frame route remains blocked in the ordinary fixed-positive-ledger form by the Step 148--150 no-free-budget theorem. Step 156 only classifies the residual kernel and states the exact compactness/Schatten/tail criteria.

The active residual remains

```tex
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
```

Any future claim that this residual is paid must provide one of:

1. exact annihilation of the pulled evaluator family;
2. compact/tail payment through a fixed/exhaustive window ladder;
3. Hilbert--Schmidt or trace-class summability of the residual kernel;
4. a non-circular signed/direct source mechanism;
5. an explicit scoped nonclaim record.
""".strip()+"\n"
(out/'nonclaim_boundary_step156.md').write_text(nonclaim)

# LaTeX note
tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{hyperref}
\title{Step 156: $\Xi^{\rm BC}$ Residual-Kernel Schatten/Tail Audit}
\author{RATCHET / Formed-Layer Membrane RH Thread}
\date{}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\newtheorem{warning}{Warning}

\begin{document}
\maketitle

\section{Purpose}
Steps 151--154 reduced the direct residual-exclusion target to the projected Sonine-kernel commutator
\[
  C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
  \qquad m_\ell(s)=e^{-\ell(1/2-s)}.
\]
For pulled zero-evaluators
\[
  \eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]
the remaining residual is generated by
\[
  r_{\ell,\rho,k}=C_\ell \eta^a_{\rho,k}.
\]
This note audits whether the resulting residual can be classified as exact, compact/tail-payable, Schatten-payable, source-absorbable, or scoped.

\section{Residual operator}
Let
\[
  \mathcal E_a=\overline{\operatorname{span}}\{\eta^a_{\rho,k}: \zeta(\rho)=0,\ 0\le k<m_\rho\}
\]
inside the pulled archimedean/Sonine model. Define
\[
  A_\ell := C_\ell\big|_{\mathcal E_a}.
\]
The residual kernel is
\[
  \mathcal R_\ell((w,k),(z,j))
  =\langle A_\ell\eta^a_{w,k}, A_\ell\eta^a_{z,j}\rangle.
\]
Equivalently,
\[
  \mathcal R_\ell((w,k),(z,j))
  =\left\langle
  \eta^a_{w,k},
  P_\infty M_{\overline{m_\ell}}(I-P_\infty)M_{m_\ell}P_\infty
  \eta^a_{z,j}
  \right\rangle.
\]

\begin{proposition}[Residual restriction identity]
On the pulled zero-evaluator closure,
\[
  \Xi^{\rm BC}_{\ell,a}=A_\ell^*A_\ell.
\]
In particular, for all $u\in\mathcal E_a$,
\[
  \langle u,\Xi^{\rm BC}_{\ell,a}u\rangle=\|A_\ell u\|^2.
\]
\end{proposition}

\section{Schatten and compactness gates}
\begin{theorem}[Schatten equivalence]
For $0<p<\infty$,
\[
  \Xi^{\rm BC}_{\ell,a}\in\mathcal S_p(\mathcal E_a)
  \quad\Longleftrightarrow\quad
  A_\ell\in\mathcal S_{2p}(\mathcal E_a,H_\infty).
\]
In particular,
\[
  \Xi^{\rm BC}_{\ell,a}\in\mathcal S_1
  \quad\Longleftrightarrow\quad
  A_\ell\in\mathcal S_2.
\]
When this holds,
\[
  \operatorname{tr}\Xi^{\rm BC}_{\ell,a}=\|A_\ell\|_{\mathcal S_2}^2.
\]
\end{theorem}

\begin{theorem}[Compact tail criterion]
Let $Q_N\uparrow I_{\mathcal E_a}$ be a finite-rank exhausting ladder. If $A_\ell$ is compact, then
\[
  \|A_\ell(I-Q_N)\|\to0,
\]
and hence
\[
  \|(I-Q_N)\Xi^{\rm BC}_{\ell,a}(I-Q_N)\|\to0.
\]
Conversely, if this norm convergence holds for an exhausting ladder whose ranges are accepted as completed residual windows, then the residual is tail-payable along that ladder.
\end{theorem}

\begin{theorem}[Noncompact witness]
If there exists an orthonormal sequence $e_n\in\mathcal E_a$ and a constant $c>0$ such that
\[
  \|A_\ell e_n\|\ge c\qquad\text{for all }n,
\]
then $A_\ell$ is not compact and $\Xi^{\rm BC}_{\ell,a}$ is not compact/tail-payable in operator norm.
\end{theorem}

\section{Interpretation}
The compact/tail route is now reduced to a precise question: does the shifted Sonine/prolate commutator
\[
  (I-P_\infty)M_{m_\ell}P_\infty
\]
become compact after restricting to the pulled Burnol zero-evaluator closure?

The answer is not formal. Raw shifted Sonine blocks are not compact in boundary-packet models, and the log-shift multiplier is nonvanishing on the Mellin line. Therefore compactness must come from a specific Burnol/co-Poisson cancellation, a semilocal prolate projection identity, or a finite-codimension/tail theorem. It cannot be assumed from the shift alone.

\section{Status}
\begin{center}
\begin{tabular}{lll}
\toprule
Status & Criterion & Current verdict\\
\midrule
Exact & $A_\ell=0$ & open, not earned\\
Compact/tail & $A_\ell\in\mathcal K$ & open, not earned\\
Trace-class & $A_\ell\in\mathcal S_2$ & open, not earned\\
Positive source absorption & fixed-ledger source budget & blocked in ordinary form\\
Scoped residual & carry $\Xi^{\rm BC}$ & active\\
\bottomrule
\end{tabular}
\end{center}

\section{Next obligation}
The next load-bearing theorem is an actual compactness or noncompactness test for
\[
  C_\ell\big|_{\mathcal E_a}.
\]
Equivalently, construct or refute a boundary-packet orthonormal sequence inside the pulled zero-evaluator closure.

\end{document}
'''
(out/'xi_bc_schatten_tail_audit_step156.tex').write_text(tex)

# Summary
summary = r'''
# Step 156 Results Summary — $\Xi^{\rm BC}$ Residual-Kernel Schatten/Tail Audit

## Main result

The active residual is

$$
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}.
$$

Using the pulled zero-evaluator family

$$
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
$$

and the shifted projected Sonine commutator

$$
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
$$

Step 156 defines

$$
A_\ell=C_\ell\big|_{\mathcal E_a},
\qquad
\mathcal E_a=\overline{\operatorname{span}}\{\eta^a_{\rho,k}\}.
$$

Then

$$
\boxed{\Xi^{\rm BC}_{\ell,a}=A_\ell^*A_\ell.}
$$

So the residual is compact/tail-payable exactly when the restricted commutator is compact/tail-payable on the pulled zero-evaluator closure.

## Schatten criterion

For every $p>0$,

$$
\boxed{\Xi^{\rm BC}_{\ell,a}\in\mathcal S_p
\iff
A_\ell\in\mathcal S_{2p}.}
$$

In particular,

$$
\boxed{\Xi^{\rm BC}_{\ell,a}\in\mathcal S_1
\iff
A_\ell\in\mathcal S_2.}
$$

Thus trace-class residual payment requires a Hilbert--Schmidt bound on the shifted Sonine/prolate commutator restricted to the actual pulled Burnol evaluator family.

## Verdict

Step 156 does not prove compactness. It classifies the exact gate:

$$
\boxed{C_\ell|_{\mathcal E_a}\stackrel{?}{\in}\mathcal K.}
$$

The current status is:

- exact exclusion: open;
- compact/tail payment: open;
- trace-class payment: open;
- ordinary positive source-frame absorption: blocked by the Step 148--150 no-free-budget theorem;
- scoped residual: active.

## Next step

Step 157 should test whether the pulled zero-evaluator closure contains a boundary-packet noncompact witness sequence. If yes, $\Xi^{\rm BC}$ is genuinely noncompact. If no, compact/tail payment may still be possible.
'''.strip()+"\n"
(out/'step156_results_summary.md').write_text(summary)

# schema
schema = {
    'step': 156,
    'title': 'Xi^BC residual-kernel Schatten/tail audit',
    'main_objects': ['A_ell=C_ell|E_a', 'Xi^BC=A_ell^*A_ell', 'R_ell((w,k),(z,j))=<A eta_wk,A eta_zj>'],
    'verdict': 'classification only; compactness/tail payment not earned; scoped residual active',
    'next_step': 'Step 157: boundary-packet witness test inside pulled zero-evaluator closure',
    'nonclaim': ['RH not proved', 'H_R=0 not proved', 'Xi^BC=0 not proved', 'compactness not proved']
}
(out/'step156_schema.json').write_text(json.dumps(schema, indent=2))

# check script
check_py = r'''#!/usr/bin/env python3
from pathlib import Path
import csv, json
out=Path(__file__).resolve().parent
required=[
 'xi_bc_schatten_tail_audit_step156.tex',
 'step156_results_summary.md',
 'xi_bc_schatten_tail_gate_table_step156.csv',
 'theorem_map_step156.csv',
 'route_status_step156.csv',
 'construction_tasks_step156.csv',
 'nonclaim_boundary_step156.md',
 'step156_schema.json',
 'xi_bc_schatten_singular_profiles_step156.png',
 'xi_bc_tail_payability_step156.png',
 'xi_bc_schatten_proxy_step156.csv',
]
missing=[p for p in required if not (out/p).exists()]
assert not missing, f"Missing files: {missing}"
with open(out/'step156_schema.json') as f:
    data=json.load(f)
assert data['step']==156
with open(out/'xi_bc_schatten_tail_gate_table_step156.csv') as f:
    rows=list(csv.DictReader(f))
assert any(r['status']=='N_scoped_residual' and r['current_verdict']=='active' for r in rows)
print({'status':'ok','checked':len(required),'missing':missing})
'''
(out/'run_step156_schatten_tail_check.py').write_text(check_py)
os.chmod(out/'run_step156_schatten_tail_check.py',0o755)

# run check
import subprocess, sys
res = subprocess.run([sys.executable, str(out/'run_step156_schatten_tail_check.py')], capture_output=True, text=True)
(out/'step156_check_results.json').write_text(json.dumps({'returncode':res.returncode,'stdout':res.stdout,'stderr':res.stderr}, indent=2))
if res.returncode != 0:
    print(res.stdout, res.stderr)
    raise SystemExit(res.returncode)

# zip artifacts
zip_path = out/'step156_xi_bc_schatten_tail_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name == zip_path.name:
            continue
        if p.is_file():
            z.write(p, arcname=p.name)

print('created', out)
