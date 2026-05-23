import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json, math, zipfile

out = Path('/mnt/data/rh_membrane_step152_adjoint_transport')
out.mkdir(parents=True, exist_ok=True)

def unitary_dft(N):
    n = np.arange(N)
    return np.exp(-2j*np.pi*np.outer(n,n)/N)/np.sqrt(N)

def projection_intersection_kernel(Pt, Pf, tol=1e-9):
    C = np.vstack([Pt, Pf])
    _, s, Vh = np.linalg.svd(C, full_matrices=True)
    rank = int((s > tol).sum())
    B = Vh.conj().T[:, rank:]
    return B @ B.conj().T

def cyclic_shift(N, m):
    return np.roll(np.eye(N, dtype=complex), m, axis=0)

N = 96
F = unitary_dft(N)
time_width = 18
freq_width = 18
Pt = np.zeros((N,N), dtype=complex); Pt[:time_width,:time_width] = np.eye(time_width)
mask = np.zeros(N); half=freq_width//2; mask[:half]=1; mask[-half:]=1
Pf = F.conj().T @ np.diag(mask) @ F
P = projection_intersection_kernel(Pt, Pf)
I = np.eye(N, dtype=complex)
idem_err = float(np.linalg.norm(P@P-P))
herm_err = float(np.linalg.norm(P-P.conj().T))

xs = np.arange(N)
eta_cols=[]
for c,sg,fr in zip(np.linspace(10,74,6), np.linspace(4,10,6), np.linspace(.07,.41,6)):
    v=np.exp(-0.5*((xs-c)/sg)**2)*np.exp(2j*np.pi*fr*xs)
    v += 0.20*np.exp(-0.5*((xs-(time_width-1))/2.5)**2)*np.exp(2j*np.pi*.46*xs)
    v=v/np.linalg.norm(v)
    eta_cols.append(v)
eta=np.array(eta_cols).T

rows=[]
for shift in range(1,25):
    Tm=cyclic_shift(N, -shift)
    B=(I-P)@Tm@P
    svals=np.linalg.svd(B, compute_uv=False)
    norms=[]
    for k in range(eta.shape[1]):
        denom=np.linalg.norm(P@eta[:,k])+1e-15
        norms.append(np.linalg.norm(B@eta[:,k])/denom)
    rows.append({'shift':shift,'operator_norm':float(svals[0]),'hs_norm':float(np.sqrt(np.sum(svals**2))),
                 'mean_eval_residual':float(np.mean(norms)),'max_eval_residual':float(np.max(norms)),
                 'min_eval_residual':float(np.min(norms)),'rank_gt_1e-8':int(np.sum(svals>1e-8))})
df=pd.DataFrame(rows); df.to_csv(out/'adjoint_transport_residual_sweep_step152.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(df['shift'], df['operator_norm'], label='operator norm')
plt.plot(df['shift'], df['mean_eval_residual'], label='mean evaluator residual')
plt.plot(df['shift'], df['max_eval_residual'], label='max evaluator residual')
plt.xlabel('shift m'); plt.ylabel('residual norm'); plt.title('Adjoint zero-evaluator transport residual'); plt.legend(); plt.tight_layout()
plt.savefig(out/'adjoint_transport_residual_sweep_step152.png', dpi=160); plt.close()

shift=8
B=(I-P)@cyclic_shift(N,-shift)@P
svals=np.linalg.svd(B, compute_uv=False)
pd.DataFrame({'index':np.arange(len(svals)),'singular_value':svals}).to_csv(out/'transport_block_singular_values_step152.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.semilogy(np.arange(1, min(60,len(svals))+1), svals[:min(60,len(svals))], marker='o', markersize=3)
plt.xlabel('singular-value index'); plt.ylabel('singular value'); plt.title('Shifted Sonin/prolate off-diagonal block spectrum'); plt.tight_layout()
plt.savefig(out/'transport_block_singular_values_step152.png', dpi=160); plt.close()

K=7; ell=np.log(2.0); rho=0.5+14.134725j
mix=np.zeros((K+1,K+1), dtype=complex)
for k in range(K+1):
    for r in range(k+1):
        mix[r,k]=np.exp(ell*(0.5-rho))*math.comb(k,r)*((-ell)**(k-r))
mix_abs=np.abs(mix)
pd.DataFrame(mix_abs, columns=[f'Y{k}' for k in range(K+1)]).to_csv(out/'raw_shift_triangular_mixing_abs_step152.csv', index=False)
plt.figure(figsize=(6,5))
plt.imshow(mix_abs, aspect='auto')
plt.colorbar(label='absolute coefficient')
plt.xlabel('input derivative evaluator order k'); plt.ylabel('output derivative evaluator order r'); plt.title('Raw Mellin shift: triangular evaluator mixing')
plt.tight_layout(); plt.savefig(out/'raw_shift_triangular_mixing_step152.png', dpi=160); plt.close()

checks=[]
for shift in [1,2,3,5,8,13,21]:
    Tm=cyclic_shift(N,-shift)
    left=(I-P)@Tm@P@eta
    right=(I-P)@(Tm@P-P@Tm)@eta
    checks.append({'shift':shift,'commutator_identity_error':float(np.linalg.norm(left-right)),
                   'left_norm':float(np.linalg.norm(left)),'right_norm':float(np.linalg.norm(right))})
pd.DataFrame(checks).to_csv(out/'commutator_identity_checks_step152.csv', index=False)

Ngrid=np.arange(1,80)
scenario=pd.DataFrame({'N':Ngrid,'tail_controlled':np.exp(-Ngrid/15),'positive_floor':0.22+0.12*np.exp(-Ngrid/25),'nonzero_residual':0.65+0.08*np.sin(Ngrid/8)})
scenario.to_csv(out/'direct_exclusion_scenarios_step152.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(Ngrid, scenario['tail_controlled'], label='tail-controlled residual')
plt.plot(Ngrid, scenario['positive_floor'], label='positive floor')
plt.plot(Ngrid, scenario['nonzero_residual'], label='nonzero residual')
plt.xlabel('window N'); plt.ylabel('normalized residual'); plt.title('Direct residual-exclusion trichotomy'); plt.legend(); plt.tight_layout()
plt.savefig(out/'direct_exclusion_scenarios_step152.png', dpi=160); plt.close()

pd.DataFrame([
    {'gate':'adjoint_transport_formula','status':'proved_formally','record':'B^*Y=(I-P)tau_-ell P J_a^*Y'},
    {'gate':'mellin_shift_triangularity','status':'proved_under_declared_convention','record':'raw log-shift mixes derivative evaluators at same zero by triangular matrix'},
    {'gate':'sonin_projection_commutator','status':'active_obstruction','record':'residual equals (I-P)[tau_-ell,P] applied to pulled evaluator'},
    {'gate':'direct_exclusion','status':'not_earned','record':'requires shifted projected evaluator to remain in Ran P'},
    {'gate':'xi_bc_residual','status':'active','record':'Xi^{BC}=B^*Pi_YB remains if commutator vector nonzero'},
]).to_csv(out/'adjoint_transport_gate_table_step152.csv', index=False)

pd.DataFrame([
    {'item':'T152.1','statement':'Ran B_{ell,a} subset P_a iff B_{ell,a}^*Y^a_{rho,k}=0 for all zero evaluators.','status':'proved from Burnol complement'},
    {'item':'T152.2','statement':'B_{ell,a}^*Y^a_{rho,k}=(I-P_infty) tau_{-ell} P_infty J_a^*Y^a_{rho,k}.','status':'proved formal adjoint identity'},
    {'item':'T152.3','statement':'Residual vector equals (I-P_infty)[tau_{-ell},P_infty]J_a^*Y^a_{rho,k}.','status':'proved commutator reduction'},
    {'item':'T152.4','statement':'Raw Mellin shifts preserve zero-evaluator span by triangular same-zero derivative mixing.','status':'proved convention-dependent formula'},
    {'item':'T152.5','statement':'Raw shift alone does not create a zeta factor or force annihilation.','status':'diagnostic theorem'},
]).to_csv(out/'theorem_map_step152.csv', index=False)

pd.DataFrame([
    {'route':'direct co-Poisson factorization','status':'not_earned','next_record':'prove zeta factorization of transported boundary block'},
    {'route':'adjoint evaluator annihilation','status':'reduced_to_commutator','next_record':'estimate r_{ell,rho,k}=(I-P)tau_-ell P J_a^*Y'},
    {'route':'positive source trace squeeze','status':'diagnostic_not_proof_producing','next_record':'do not pursue without new signed/conservation mechanism'},
    {'route':'residual budgeting','status':'fallback','next_record':'carry Xi^{BC} as explicit adequacy residual if nonzero'},
]).to_csv(out/'route_status_step152.csv', index=False)

pd.DataFrame([
    {'task':'Identify exact transported evaluator J_a^*Y^a_{rho,k} in chosen archimedean/Sonin model','priority':'high','result_needed':'explicit kernel or Mellin formula'},
    {'task':'Test whether P_infty J_a^*Y^a_{rho,k} is invariant under tau_-ell modulo Ran P_infty','priority':'high','result_needed':'vanishing or lower bound for commutator residual'},
    {'task':'If nonzero, define Xi^{BC}_{ell,a} as accepted residual and stop trying direct inclusion','priority':'high','result_needed':'nonclaim/residual budget record'},
    {'task':'Check whether semilocal prolate replacement P_S changes commutator at essential level','priority':'medium','result_needed':'essential cancellation theorem or obstruction'},
]).to_csv(out/'construction_tasks_step152.csv', index=False)

pd.DataFrame([
    {'claim':'RH','status':'not_claimed'},
    {'claim':'H_R=0','status':'not_claimed'},
    {'claim':'Xi^{BC}=0','status':'not_claimed'},
    {'claim':'raw log-shift creates zeta factor','status':'rejected'},
    {'claim':'adjoint transport criterion','status':'claimed_formally'},
]).to_csv(out/'nonclaim_boundary_step152.csv', index=False)

summary = r'''# Step 152: Adjoint zero-evaluator transport formula

## Main object

The shifted residual block is

\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]

The direct Burnol/co-Poisson exclusion target is

\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0.
\]

Equivalently, for every zero evaluator,

\[
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}=0.
\]

## Adjoint transport formula

Assuming \(P_\infty=P_\infty^*\) and \(\tau_\ell^*=\tau_{-\ell}\),

\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}.
}
\]

Equivalently,

\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
}
\]

So direct residual exclusion is a commutator-vanishing theorem.

## Mellin shift formula

Under the right-Mellin convention

\[
\widehat f(s)=\int_0^\infty f(t)t^{-s}\,dt,
\]

the unitary log-shift \(\tau_\ell\) acts as

\[
\widehat{\tau_\ell f}(s)=e^{\ell(1/2-s)}\widehat f(s).
\]

Therefore raw shifts act on zero-evaluator derivatives by triangular same-zero mixing:

\[
(\tau_\ell^*Y_{\rho,k})(f)
=
 e^{\ell(1/2-\rho)}
\sum_{r=0}^k {k\choose r}(-\ell)^{k-r}Y_{\rho,r}(f).
\]

This preserves the zero-evaluator span, but it does not annihilate it.

## Verdict

A raw log-shift does not create a \(\zeta\)-factor and does not force

\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0.
\]

The obstruction is exactly the Sonin/prolate projection commutator

\[
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
\]

Thus \(H_R=0\) is not earned. The active residual remains

\[
\Xi^{\rm BC}_{\ell,a}
=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]
'''
(out/'step152_results_summary.md').write_text(summary)

tex = r'''
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\newtheorem{theorem}{Theorem}
\title{Step 152: Adjoint Zero-Evaluator Transport Formula}
\author{RH Membrane / Burnol--Sonine Residual Route}
\date{Step 152}
\begin{document}
\maketitle

\section{Purpose}
Step 150 blocked the positive source-frame/fixed positive ledger squeeze as a proof-producing route: the missing source-budget condition is already collapse-strength. Step 151 therefore pivoted to direct residual exclusion. The present step computes the exact adjoint transport formula for the shifted boundary block
\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]
The target is to decide whether
\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0
\]
has a structural cancellation mechanism.

\section{Burnol criterion}
Let \(Y_a\subset L_a\) be the closed span of Burnol zero-evaluator vectors \(Y^a_{\rho,k}\), and let \(P_a=Y_a^\perp\) be the co-Poisson complement for \(a<1\). Then
\[
\operatorname{Ran}\mathfrak B_{\ell,a}\subseteq P_a
\quad\Longleftrightarrow\quad
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}=0
\quad\forall \rho,k.
\]

\section{Adjoint transport formula}
Assume \(P_\infty=P_\infty^*\) and \(\tau_\ell^*=\tau_{-\ell}\). Then
\begin{theorem}[Adjoint transport]
For every zero evaluator \(Y^a_{\rho,k}\),
\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}.
}
\]
Equivalently,
\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
}
\]
\end{theorem}
\begin{proof}
Taking the adjoint of \(J_aP_\infty\tau_\ell(I-P_\infty)\) gives
\[
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*.
\]
The commutator form follows since \((I-P_\infty)P_\infty=0\):
\[
(I-P_\infty)[\tau_{-\ell},P_\infty]
=(I-P_\infty)\tau_{-\ell}P_\infty.
\]
\end{proof}

\section{Mellin convention and triangular raw shift}
Use the right Mellin transform
\[
\widehat f(s)=\int_0^\infty f(t)t^{-s}\,dt.
\]
The unitary log-shift \(\tau_\ell\) is normalized so that in logarithmic coordinates it is ordinary translation. In \(t\)-coordinates,
\[
(\tau_\ell f)(t)=e^{-\ell/2}f(e^{-\ell}t),
\]
and hence
\[
\widehat{\tau_\ell f}(s)=e^{\ell(1/2-s)}\widehat f(s).
\]
Thus raw shifts act on derivative evaluators by
\[
(\tau_\ell^*Y_{\rho,k})(f)
=e^{\ell(1/2-\rho)}\sum_{r=0}^k {k\choose r}(-\ell)^{k-r}Y_{\rho,r}(f).
\]
This is triangular same-zero mixing. It preserves the zero-evaluator span but does not annihilate it.

\section{Diagnostic verdict}
A raw log-shift does not create a \(\zeta\)-factor. Direct exclusion requires
\[
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}=0.
\]
This is a Sonin/prolate projection commutator theorem, not a consequence of Burnol completeness or of the semilocal Hardy--Titchmarsh transport alone. If the commutator vector is nonzero, the active residual is
\[
\Xi^{\rm BC}_{\ell,a}
=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]

\section{Nonclaim boundary}
This note does not prove RH, does not prove \(H_R=0\), and does not prove \(\Xi^{\rm BC}=0\). It gives the exact formula whose vanishing must be established or explicitly budgeted.

\end{document}
'''
(out/'adjoint_zero_evaluator_transport_step152.tex').write_text(tex)

schema={'step':152,'title':'Adjoint zero-evaluator transport formula','main_object':'r_{ell,rho,k}=(I-P_infty)tau_{-ell}P_infty J_a^*Y^a_{rho,k}','main_verdict':'direct residual exclusion reduces to a Sonin/prolate projection commutator; no automatic cancellation is earned','idempotent_error':idem_err,'hermitian_error':herm_err}
(out/'step152_schema.json').write_text(json.dumps(schema, indent=2))

zip_path=out/'step152_adjoint_transport_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        if p.name != zip_path.name:
            z.write(p, arcname=p.name)
print(json.dumps({'out':str(out),'idempotent_error':idem_err,'hermitian_error':herm_err,'file_count':len(list(out.iterdir()))}, indent=2))
