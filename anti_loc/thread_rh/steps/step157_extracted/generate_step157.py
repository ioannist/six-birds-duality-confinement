import os, json, csv, zipfile, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step157_calkin_avoidance')
OUT.mkdir(parents=True, exist_ok=True)

step = 157

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,enumitem,geometry,booktabs}
\geometry{margin=1in}
\title{Step 157: Calkin-Level Pulled-Evaluator Avoidance Audit}
\author{Six Birds / RH Membrane Construction Notes}
\date{}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{definition}{Definition}
\newtheorem{lemma}{Lemma}
\newtheorem{warning}{Warning}
\begin{document}
\maketitle

\section*{Orientation and typed context}
This step is \emph{adequacy-oriented}.  The residual
\[
  \Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}
\]
is bad news unless it is zero, tail-payable, compact/Schatten-payable, or explicitly budgeted.  The typed context is the Burnol/Sonine residual carrier pulled back to the archimedean/Sonin model:
\[
  H_\eta:=\overline{\operatorname{span}\{\eta^a_{\rho,k}:\rho\in Z_\zeta,
  0\leq k<m_\rho\}},\qquad
  \eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}.
\]
The comparison algebra for this step is not the Hilbert-space operator algebra itself, but the Calkin algebra
\[
  \mathcal Q(H):=\mathcal B(H)/\mathcal K(H),
  \qquad q:\mathcal B(H)\to\mathcal Q(H).
\]
The Calkin question is therefore meaningful only after declaring the carrier Hilbert space, the pulled-evaluator projection, and the compact ideal.

\section*{Objects from Steps 153--156}
The projected shifted Sonine block is
\[
  C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
  \qquad m_\ell(s)=e^{-\ell(1/2-s)}.
\]
Let
\[
  P_\eta:\ H\to H_\eta
\]
be the orthogonal projection onto the closed pulled zero-evaluator span.  The Calkin-level residual is
\[
  \mathfrak c_{\ell,\eta}:=q(C_\ell P_\eta)\in \mathcal Q(H),
\]
and its size is the essential norm
\[
  \|C_\ell P_\eta\|_{\rm e}
  :=\inf_{K\in\mathcal K(H)}\|C_\ell P_\eta-K\|.
\]
Exact residual exclusion requires
\[
  C_\ell P_\eta=0.
\]
Compact/tail payment requires the weaker Calkin condition
\[
  \boxed{\mathfrak c_{\ell,\eta}=0.}
\]
If \(\mathfrak c_{\ell,\eta}\neq0\), then \(\Xi^{\rm BC}\) contains a genuinely essential residual and cannot be paid by ordinary compact exhaustion.

\section*{Calkin avoidance theorem}
\begin{theorem}[Calkin-level pulled-evaluator avoidance]
For the declared pulled-evaluator carrier \(H_\eta\), the following are equivalent:
\begin{enumerate}[label=(\roman*)]
  \item \([C_\ell]P_\eta=0\) in the Calkin algebra.
  \item \(C_\ell P_\eta\in\mathcal K(H)\).
  \item For every bounded sequence \(u_n\in H_\eta\) with \(u_n\rightharpoonup0\), one has
  \[
     \|C_\ell u_n\|\to0.
  \]
  \item For one, equivalently every, finite-rank exhaustion \(Q_N\uparrow P_\eta\) strongly,
  \[
     \|C_\ell(P_\eta-Q_N)\|\to0.
  \]
\end{enumerate}
\end{theorem}

\begin{proof}
The equivalence between (i) and (ii) is the definition of the Calkin quotient.  The equivalence between compactness and weak-null sequence decay is a standard characterization of compact operators on Hilbert space.  If \(C_\ell P_\eta\) is compact and \(Q_N\uparrow P_\eta\) strongly, then compactness upgrades strong convergence on bounded sets to norm convergence on the image of the unit ball, hence \(\|C_\ell(P_\eta-Q_N)\|\to0\).  Conversely, if the latter holds for a finite-rank exhaustion, then \(C_\ell Q_N\) is finite-rank and \(C_\ell Q_N\to C_\ell P_\eta\) in norm, so \(C_\ell P_\eta\) is compact.
\end{proof}

\section*{Finite-section warning}
Finite sections cannot certify Calkin vanishing by themselves.  A sequence of finite matrices can have small bottom singular values and still converge to an operator with nonzero essential norm.  Conversely, finite sections can show persistent plateaux that suggest essential mass but do not prove it unless promoted to a Weyl sequence or an accepted symbol theorem.

\begin{definition}[Weyl-sequence certificate]
A Calkin obstruction certificate for \(C_\ell P_\eta\) is a sequence \(u_n\in H_\eta\) such that
\[
  \|u_n\|=1,
  \qquad u_n\rightharpoonup0,
  \qquad \liminf_n\|C_\ell u_n\|>0.
\]
Such a certificate proves
\[
  \|C_\ell P_\eta\|_{\rm e}>0.
\]
\end{definition}

\section*{Hardy-shadow lane and status}
There is a useful public-shadow comparison.  If \(P_\infty\) is replaced by a Hardy projection \(P_+\), then the block
\[
  (I-P_+)M_mP_+
\]
is a classical Hankel operator, and compactness can often be studied by symbol theorems.  But this is only a shadow lane.  To import it into the Burnol/Sonine carrier one must supply a bridge
\[
  P_\infty-P_+\in\mathcal K(H)
  \quad\text{or another Calkin-faithful comparison,}
\]
plus a transport record for \(P_\eta\).  Without that bridge, Hardy compactness or noncompactness is \texttt{public\_shadow}, not an accepted Burnol/Sonine certificate.

\section*{Classification after Step 157}
The residual now has the following status taxonomy.
\[
\begin{array}{lll}
\mathsf E & \text{Exact} & C_\ell P_\eta=0.\\
\mathsf K & \text{Compact/tail-payable} & C_\ell P_\eta\in\mathcal K(H).\\
\mathsf S_p & \text{Schatten-payable} & C_\ell\widetilde E\in\mathcal S_{2p}.\\
\mathsf C & \text{Calkin obstruction} & \|C_\ell P_\eta\|_{\rm e}>0.\\
\mathsf N & \text{Active residual} & \text{no accepted exact, compact, or essential record.}
\end{array}
\]
Step 157 does not prove \(\mathsf K\), and it does not prove \(\mathsf C\).  It identifies the certificate required for either status.

\section*{No-go scope}
This step forecloses the following route only:
\[
  \text{finite singular-value decay or finite-window evidence}
  \Rightarrow
  \text{completed compact/tail payment.}
\]
That route is invalid without a Calkin promotion.  The step does \emph{not} foreclose co-Poisson factorization, a semilocal prolate symbol theorem, a signed trace mechanism, or a genuine Weyl-sequence proof.

\section*{Next theorem leaf}
The next proof-producing object is the Weyl/symbol alternative:
\[
  \boxed{\text{prove }C_\ell P_\eta\in\mathcal K(H)\text{ by a Sonine/prolate compactness theorem,}}
\]
or
\[
  \boxed{\text{prove }\|C_\ell P_\eta\|_{\rm e}>0\text{ by a pulled-evaluator Weyl sequence.}}
\]
The recommended next step is therefore \textbf{Step 158: pulled-evaluator Weyl sequence / essential-symbol test}.

\end{document}
'''
(OUT/'calkin_pulled_evaluator_avoidance_step157.tex').write_text(tex)

summary = r'''
# Step 157: Calkin-Level Pulled-Evaluator Avoidance Audit

## Orientation

Adequacy-oriented.  The residual

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}
\]

is bad news unless it is exact, compact/tail-paid, Schatten-paid, or explicitly budgeted.

## Main object

The shifted Sonine/prolate commutator block is

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad m_\ell(s)=e^{-\ell(1/2-s)}.
\]

The pulled evaluator span is

\[
H_\eta=\overline{\operatorname{span}\{\eta^a_{\rho,k}\}},
\qquad \eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

and the Calkin-level object is

\[
\boxed{\mathfrak c_{\ell,\eta}=q(C_\ell P_\eta)\in\mathcal B(H)/\mathcal K(H).}
\]

The active question is

\[
\boxed{[C_\ell]P_\eta\stackrel{?}{=}0.}
\]

## Calkin avoidance theorem

The following are equivalent:

\[
[C_\ell]P_\eta=0,
\]

\[
C_\ell P_\eta\in\mathcal K(H),
\]

\[
\forall u_n\in H_\eta,
\quad \|u_n\|\le1,
\quad u_n\rightharpoonup0
\Rightarrow
\|C_\ell u_n\|\to0,
\]

and for a finite-rank exhaustion \(Q_N\uparrow P_\eta\),

\[
\|C_\ell(P_\eta-Q_N)\|\to0.
\]

So compact/tail-payment of \(\Xi^{\rm BC}\) is exactly a Calkin-vanishing theorem.

## Weyl-sequence obstruction

A noncompactness certificate is a pulled-evaluator Weyl sequence:

\[
\|u_n\|=1,
\qquad u_n\in H_\eta,
\qquad u_n\rightharpoonup0,
\qquad \liminf_n\|C_\ell u_n\|>0.
\]

Such a sequence proves

\[
\|C_\ell P_\eta\|_{\rm e}>0.
\]

## Main verdict

Step 157 does **not** prove compactness and does **not** prove noncompactness.

It converts the question into a precise Calkin alternative:

\[
\boxed{C_\ell P_\eta\in\mathcal K(H)}
\]

or

\[
\boxed{\|C_\ell P_\eta\|_{\rm e}>0.}
\]

Finite-window singular-value plots are diagnostic only.  They are not completed-carrier proof.

## Route status

| status | condition | current state |
|---|---|---|
| exact | \(C_\ell P_\eta=0\) | not proved |
| compact/tail-payable | \(C_\ell P_\eta\in\mathcal K\) | not proved |
| Schatten-payable | \(C_\ell\widetilde E\in\mathcal S_{2p}\) | not proved |
| Calkin obstruction | \(\|C_\ell P_\eta\|_e>0\) | not proved |
| active residual | no accepted exact/compact/obstruction record | active |

## Next step

**Step 158: pulled-evaluator Weyl sequence / essential-symbol test.**

Target: either prove compactness via a Sonine/prolate Calkin theorem or construct a Weyl sequence in the pulled evaluator span showing nonzero essential residual.
'''
(OUT/'step157_results_summary.md').write_text(summary)

# CSV files
def write_csv(name, rows):
    with open(OUT/name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

write_csv('calkin_avoidance_gate_table_step157.csv', [
    {'gate':'orientation','typed_context':'Burnol/Sonine adequacy track','required_record':'Xi^BC should vanish or be paid','status':'accepted_context','next_action':'keep adequacy sign convention active'},
    {'gate':'calkin_object','typed_context':'B(H)/K(H) for pulled evaluator carrier','required_record':'q(C_l P_eta) declared','status':'defined','next_action':'audit compactness or essential norm'},
    {'gate':'exact_exclusion','typed_context':'operator level','required_record':'C_l P_eta = 0','status':'not_proved','next_action':'co-Poisson factorization or projected-kernel cancellation'},
    {'gate':'compact_payment','typed_context':'Calkin level','required_record':'C_l P_eta in K(H)','status':'open','next_action':'finite-rank exhaustion norm tail or compactness theorem'},
    {'gate':'essential_obstruction','typed_context':'Calkin level','required_record':'weak-null Weyl sequence with residual lower bound','status':'open','next_action':'construct pulled-evaluator Weyl sequence'},
    {'gate':'finite_section_evidence','typed_context':'moving windows','required_record':'must promote to Calkin theorem','status':'moving_window_support_only','next_action':'do not promote singular plots'},
    {'gate':'hardy_shadow_import','typed_context':'public shadow Hardy/Hankel model','required_record':'Calkin-faithful bridge from Hardy projection to Sonine projection','status':'public_shadow','next_action':'bridge theorem required before import'},
])

write_csv('calkin_classification_step157.csv', [
    {'label':'E','name':'exact exclusion','criterion':'C_l P_eta = 0','effect':'H_R=0 for this block','status':'not_earned'},
    {'label':'K','name':'compact/tail-payable','criterion':'C_l P_eta in K(H)','effect':'norm tail can vanish under finite-rank exhaustion','status':'open'},
    {'label':'S_p','name':'Schatten-payable','criterion':'C_l \\widetilde E in S_{2p}','effect':'trace/Schatten tail payment','status':'open'},
    {'label':'C','name':'Calkin obstruction','criterion':'||C_l P_eta||_e > 0','effect':'noncompact adequacy residual persists','status':'open'},
    {'label':'N','name':'active residual','criterion':'no accepted E/K/S/C record','effect':'Xi^BC remains in theorem statement','status':'current'},
])

write_csv('theorem_map_step157.csv', [
    {'theorem':'Calkin avoidance equivalence','statement':'[C_l]P_eta=0 iff C_lP_eta compact iff weak-null sequences are killed iff finite-rank tails vanish in norm','status':'framework theorem','depends_on':'declared Hilbert carrier and compact ideal'},
    {'theorem':'Weyl obstruction certificate','statement':'weak-null pulled-evaluator sequence with residual lower bound implies nonzero essential norm','status':'framework theorem','depends_on':'existence of sequence'},
    {'theorem':'Hardy-shadow nonpromotion','statement':'Hardy/Hankel compactness does not transfer without Calkin-faithful bridge','status':'no-overread theorem','depends_on':'typed-context discipline'},
    {'theorem':'Finite-section noncertification','statement':'finite singular values are diagnostic not completed compactness evidence','status':'moving-window warning','depends_on':'fixed/exhaustive ledger discipline'},
])

write_csv('route_status_step157.csv', [
    {'route':'co-Poisson factorization','status':'open','reason':'raw shift does not create zeta factor','residual':'Xi^BC'},
    {'route':'projected-kernel exact cancellation','status':'open','reason':'C_l eta_z = 0 not proved','residual':'Xi^BC'},
    {'route':'compact/tail payment','status':'open','reason':'C_l P_eta compactness not proved','residual':'Calkin residual'},
    {'route':'positive source-frame squeeze','status':'blocked_as_shortcut','reason':'source budget is collapse-strength','residual':'source-budget obstruction'},
    {'route':'scoped residual','status':'active','reason':'no exact/compact/source certificate yet','residual':'Xi^BC remains named'},
])

write_csv('construction_tasks_step157.csv', [
    {'task':'Define P_eta precisely','output':'closed projection onto pulled evaluator span','priority':'high','status':'formalized'},
    {'task':'Prove compactness','output':'C_l P_eta in K(H)','priority':'high','status':'open'},
    {'task':'Construct Weyl sequence','output':'u_n weak-null in H_eta with liminf ||C_l u_n||>0','priority':'high','status':'next'},
    {'task':'Develop Sonine/Hankel symbol theorem','output':'Calkin symbol for C_l on pulled evaluator span','priority':'medium','status':'external theorem leaf'},
    {'task':'Audit Hardy-shadow bridge','output':'P_infty - P_+ compact or declared nonbridge','priority':'medium','status':'open'},
    {'task':'Update residual tree','output':'Xi^BC classified as active Calkin-level residual','priority':'high','status':'done'},
])

# nonclaim markdown
nonclaim = '''# Step 157 nonclaim boundary

Step 157 does not prove RH.

It does not prove \(H_R=0\).

It does not prove \(\Xi^{\rm BC}=0\).

It does not prove that \(C_\ell P_\eta\) is compact.

It also does not prove that \(C_\ell P_\eta\) has nonzero essential norm.

It proves the Calkin equivalence that must be used to classify the residual and blocks promotion of finite-window singular-value evidence to completed compactness.

Hardy/Hankel comparisons are public shadows unless a Calkin-faithful bridge to the actual Burnol/Sonine projection is supplied.
'''
(OUT/'nonclaim_boundary_step157.md').write_text(nonclaim)

schema = {
    'step':157,
    'title':'Calkin-Level Pulled-Evaluator Avoidance Audit',
    'orientation':'adequacy',
    'typed_context':'Burnol/Sonine pulled zero-evaluator carrier; Calkin algebra B(H)/K(H)',
    'main_operator':'C_l P_eta',
    'main_residual':'Xi^BC',
    'accepted_results':['Calkin avoidance equivalence','Weyl-sequence obstruction criterion','finite-section nonpromotion warning'],
    'not_proved':['exact exclusion','compactness','Schatten membership','nonzero essential norm'],
    'next_step':'Step 158: pulled-evaluator Weyl sequence / essential-symbol test'
}
(OUT/'step157_schema.json').write_text(json.dumps(schema, indent=2))

# Generate plots and data
N = np.arange(1, 161)
compact = 1/(1+N)**1.2
hilbert_schmidt = 1/(1+N)**0.75
essential = 0.18 + 0.8/(1+N)**1.0
slow = 1/np.sqrt(np.log(N+3))

plt.figure(figsize=(8,5))
plt.plot(N, compact, label='compact-like decay')
plt.plot(N, hilbert_schmidt, label='Schatten-like slow decay')
plt.plot(N, essential, label='essential plateau')
plt.plot(N, slow, label='inconclusive slow tail')
plt.yscale('log')
plt.xlabel('singular index / finite-section scale')
plt.ylabel('singular-value proxy')
plt.title('Step 157 residual singular-value scenarios')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'calkin_singular_value_scenarios_step157.png', dpi=160)
plt.close()

# tail norms
Q = np.arange(10, 161)
tail_compact = 1/(Q+1)**0.8
tail_essential = 0.22 + 0.25/(Q+1)**0.7
tail_schatten = 1/np.sqrt(Q+1)
plt.figure(figsize=(8,5))
plt.plot(Q, tail_compact, label='compact: tail norm -> 0')
plt.plot(Q, tail_schatten, label='trace/Schatten tail proxy')
plt.plot(Q, tail_essential, label='Calkin obstruction: tail norm floor')
plt.xlabel('finite-rank exhaustion N')
plt.ylabel(r'$\|C_\ell(P_\eta-Q_N)\|$ proxy')
plt.title('Calkin tail-payability criterion')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'calkin_tail_payability_step157.png', dpi=160)
plt.close()

# Weyl residual norm models
Nw = np.arange(1,101)
weyl_compact = 0.9*np.exp(-Nw/20)
weyl_floor = 0.3 + 0.05*np.sin(Nw/7)
weyl_uncertain = 0.2 + 0.45/np.sqrt(Nw)
plt.figure(figsize=(8,5))
plt.plot(Nw, weyl_compact, label='compact-compatible weak-null sequence')
plt.plot(Nw, weyl_floor, label='Weyl obstruction sequence')
plt.plot(Nw, weyl_uncertain, label='inconclusive diagnostic sequence')
plt.xlabel('sequence index')
plt.ylabel(r'$\|C_\ell u_n\|$')
plt.title('Pulled-evaluator Weyl-sequence test scenarios')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'weyl_sequence_residual_test_step157.png', dpi=160)
plt.close()

# classification bar
labels = ['exact','compact','Schatten','Calkin obs.','active']
vals = [0.05,0.15,0.12,0.25,1.0]
plt.figure(figsize=(8,4.5))
plt.bar(labels, vals)
plt.ylim(0,1.1)
plt.ylabel('accepted-status proxy')
plt.title('Step 157 classification status: active residual dominates')
plt.tight_layout()
plt.savefig(OUT/'calkin_classification_status_step157.png', dpi=160)
plt.close()

# Hardy shadow bridge diagram as plot
bridge = np.array([[1.0, 0.45, 0.15],[0.45, 1.0, 0.35],[0.15,0.35,1.0]])
plt.figure(figsize=(5.6,4.8))
plt.imshow(bridge, aspect='auto')
plt.xticks([0,1,2], ['Hardy shadow','Calkin bridge','Sonine target'], rotation=30, ha='right')
plt.yticks([0,1,2], ['Hardy shadow','Calkin bridge','Sonine target'])
plt.colorbar(label='bridge strength proxy')
plt.title('Public-shadow bridge must be earned')
plt.tight_layout()
plt.savefig(OUT/'hardy_shadow_bridge_status_step157.png', dpi=160)
plt.close()

# CSV for plot data
with open(OUT/'calkin_singular_value_scenarios_step157.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['index','compact_decay','s_schatten_slow','essential_plateau','inconclusive_slow'])
    for i,c,h,e,s in zip(N, compact, hilbert_schmidt, essential, slow):
        w.writerow([int(i),float(c),float(h),float(e),float(s)])
with open(OUT/'calkin_tail_payability_step157.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['N','compact_tail','schatten_tail','essential_floor_tail'])
    for i,c,h,e in zip(Q, tail_compact, tail_schatten, tail_essential):
        w.writerow([int(i),float(c),float(h),float(e)])
with open(OUT/'weyl_sequence_residual_test_step157.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['index','compact_compatible','weyl_obstruction','inconclusive'])
    for i,c,e,u in zip(Nw, weyl_compact, weyl_floor, weyl_uncertain):
        w.writerow([int(i),float(c),float(e),float(u)])

# Check script
check_script = r'''#!/usr/bin/env python3
"""Sanity checks for Step 157 finite Calkin/Weyl diagnostics.
These are finite algebra checks only; they are not proof of compactness/noncompactness.
"""
import json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(157)
# Finite projection identity: C P = (I-P0) M P0 P_eta.
n = 48
A = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
Q,_ = np.linalg.qr(A)
r = 24
P0 = Q[:,:r] @ Q[:,:r].conj().T
B = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
U,_ = np.linalg.qr(B)
s = 32
Peta = U[:,:s] @ U[:,:s].conj().T
# unitary shift-like multiplier
phases = np.exp(1j*np.linspace(0, 2*np.pi, n, endpoint=False))
M = np.diag(phases)
C = (np.eye(n)-P0) @ M @ P0
lhs = C @ Peta
rhs = (np.eye(n)-P0) @ (M @ P0 - P0 @ M) @ Peta
comm_error = np.linalg.norm(lhs-rhs)
# finite-rank approximation check: if tail norm goes to zero in synthetic compact model
N = np.arange(10,161)
compact_tail = 1/(N+1)**0.8
essential_tail = 0.22 + 0.25/(N+1)**0.7
results = {
    'commutator_identity_error': float(comm_error),
    'compact_tail_last': float(compact_tail[-1]),
    'essential_tail_last': float(essential_tail[-1]),
    'compact_tail_decreases': bool(compact_tail[-1] < compact_tail[0]),
    'essential_tail_has_floor_proxy': bool(essential_tail[-1] > 0.2),
    'status': 'passed' if comm_error < 1e-10 else 'failed'
}
(OUT/'step157_check_results.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
'''
(OUT/'run_step157_calkin_avoidance.py').write_text(check_script)
os.chmod(OUT/'run_step157_calkin_avoidance.py',0o755)

# Run check
import subprocess, sys
subprocess.run([sys.executable, str(OUT/'run_step157_calkin_avoidance.py')], check=True)

# zip artifacts
zip_path = OUT/'step157_calkin_avoidance_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.name == zip_path.name:
            continue
        z.write(p, arcname=p.name)

print('generated', OUT)
