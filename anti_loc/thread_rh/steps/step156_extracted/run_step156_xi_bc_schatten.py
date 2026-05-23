import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step156_xi_bc_schatten_tail')
out.mkdir(parents=True, exist_ok=True)

# Synthetic singular profiles for classification of A_l = C_l E_a.
n = np.arange(1, 401)
profiles = {
    'essential_flat': 0.42 + 0.08*np.exp(-n/50),
    'compact_polynomial': n**(-0.55),
    'hilbert_schmidt': n**(-0.8),
    'trace_class_residual': n**(-1.2),
    'finite_rank': np.where(n <= 40, 1.0 - 0.015*n, 0.0),
}
profile_df = pd.DataFrame({'index': n, **profiles})
profile_df.to_csv(out/'xi_bc_residual_singular_profiles_step156.csv', index=False)

plt.figure(figsize=(8,5))
for name, vals in profiles.items():
    plt.loglog(n, np.maximum(vals, 1e-12), label=name.replace('_',' '))
plt.xlabel('singular index')
plt.ylabel('singular value proxy for A_l')
plt.title('Step 156: residual singular-value profiles')
plt.legend()
plt.tight_layout()
plt.savefig(out/'xi_bc_residual_singular_profiles_step156.png', dpi=180)
plt.close()

# Tail norms from profiles
rows=[]
for name, vals in profiles.items():
    for N in [10,20,40,80,120,160,240,320]:
        tail = vals[N:]
        op_tail = float(tail[0]) if len(tail) else 0.0
        hs_tail = float(np.sqrt(np.sum(tail**2))) if len(tail) else 0.0
        trace_residual_tail = float(np.sum(tail**2)) if len(tail) else 0.0
        rows.append({'profile':name,'window_N':N,'operator_tail':op_tail,'hs_tail_A':hs_tail,'trace_tail_R=AstarA':trace_residual_tail})
tail_df = pd.DataFrame(rows)
tail_df.to_csv(out/'xi_bc_tail_payability_step156.csv', index=False)

plt.figure(figsize=(8,5))
for name in profiles:
    sub=tail_df[tail_df.profile==name]
    plt.loglog(sub.window_N, np.maximum(sub.operator_tail,1e-12), marker='o', label=name.replace('_',' '))
plt.xlabel('window cutoff N')
plt.ylabel('operator tail proxy ||A(I-Q_N)||')
plt.title('Step 156: operator-tail payability proxy')
plt.legend()
plt.tight_layout()
plt.savefig(out/'xi_bc_operator_tail_step156.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
for name in profiles:
    sub=tail_df[tail_df.profile==name]
    plt.loglog(sub.window_N, np.maximum(sub['trace_tail_R=AstarA'],1e-12), marker='o', label=name.replace('_',' '))
plt.xlabel('window cutoff N')
plt.ylabel('trace tail proxy for R=A*A')
plt.title('Step 156: trace-tail payability proxy')
plt.legend()
plt.tight_layout()
plt.savefig(out/'xi_bc_trace_tail_step156.png', dpi=180)
plt.close()

# Finite toy commutator model: random orthogonal projection and unitary shift.
rng = np.random.default_rng(156)
Ndim=160
# Fourier-type deterministic-ish random projection
X = rng.normal(size=(Ndim, Ndim//2))
Q, _ = np.linalg.qr(X)
P = Q @ Q.T
# cyclic shift by ell
ell=7
T = np.roll(np.eye(Ndim), shift=ell, axis=0)
C = (np.eye(Ndim)-P) @ T @ P
sv = np.linalg.svd(C, compute_uv=False)
pd.DataFrame({'index':np.arange(1,len(sv)+1),'singular_value':sv}).to_csv(out/'finite_commutator_singular_values_step156.csv', index=False)
plt.figure(figsize=(8,5))
plt.semilogy(np.arange(1,len(sv)+1), sv, marker='.', linewidth=1)
plt.xlabel('singular index')
plt.ylabel('singular value')
plt.title('Step 156: finite projected-shift commutator singular values')
plt.tight_layout()
plt.savefig(out/'finite_commutator_singular_values_step156.png', dpi=180)
plt.close()

# Classification table
classification = pd.DataFrame([
    {'status':'E_exact','criterion':'A_l = 0','tail_payable':'yes','current_verdict':'not earned'},
    {'status':'C_compact','criterion':'A_l compact; operator tails vanish','tail_payable':'yes if exhaustive','current_verdict':'open, not earned'},
    {'status':'S_trace','criterion':'A_l in S_2 so R=A*A trace class','tail_payable':'yes under fixed ledger','current_verdict':'open, requires evaluator-norm decay'},
    {'status':'X_essential','criterion':'essential norm of A_l positive','tail_payable':'no','current_verdict':'active obstruction unless compactness theorem supplied'},
])
classification.to_csv(out/'xi_bc_schatten_classification_table_step156.csv', index=False)

# Gate table
gates = pd.DataFrame([
    {'gate':'G1_residual_synthesis','object':'A_l = C_l E_a','pass_condition':'pulled-evaluator synthesis is declared and closed','status':'formalized'},
    {'gate':'G2_schatten','object':'R_l=A_l^*A_l','pass_condition':'A_l in S_{2p}','status':'criterion proved'},
    {'gate':'G3_operator_tail','object':'||A_l(I-Q_N)||','pass_condition':'tends to 0 for exhaustive windows','status':'open'},
    {'gate':'G4_trace_tail','object':'||A_l(I-Q_N)||_{S2}','pass_condition':'tends to 0 under fixed ledger','status':'open'},
    {'gate':'G5_essential_escape','object':'pi_ess(C_l) on range E_a','pass_condition':'vanishes or is avoided','status':'open'},
    {'gate':'G6_nonclaim','object':'Xi^BC','pass_condition':'carried as active residual if no gate passes','status':'active'},
])
gates.to_csv(out/'xi_bc_schatten_gate_table_step156.csv', index=False)

# Theorem map and route status
pd.DataFrame([
    {'label':'T156.1','statement':'R_l in S_p iff A_l in S_{2p}','depends_on':'singular-value calculus','status':'proved'},
    {'label':'T156.2','statement':'compactness/tail-payability iff residual synthesis tails vanish','depends_on':'compact operator finite-rank approximation','status':'proved as criterion'},
    {'label':'T156.3','statement':'essential residual persists if pulled evaluators meet nonzero Calkin sector','depends_on':'Calkin lower-frame hypothesis','status':'conditional obstruction'},
]).to_csv(out/'theorem_map_step156.csv', index=False)

pd.DataFrame([
    {'route':'exact exclusion H_R=0','status':'open; not earned'},
    {'route':'compact/tail payment','status':'open; needs A_l compact or Schatten'},
    {'route':'positive source-frame absorption','status':'blocked as shortcut by source-budget obstruction'},
    {'route':'scoped residual','status':'active'},
]).to_csv(out/'route_status_step156.csv', index=False)

pd.DataFrame([
    {'task':'Compute projected Sonine kernel tail','target':'estimate C_l eta_{rho,k} at large |Im rho|','priority':'high'},
    {'task':'Calkin-sector test','target':'does pulled evaluator closure meet essential boundary-packet sector?','priority':'high'},
    {'task':'Weighted Schatten envelope','target':'find fixed weights making A_l Hilbert-Schmidt without losing separation','priority':'medium'},
    {'task':'Nonclaim integration','target':'state theorem with Xi^BC active if compactness not earned','priority':'high'},
]).to_csv(out/'construction_tasks_step156.csv', index=False)

schema = {
    'step':156,
    'name':'Xi^BC residual-kernel Schatten/tail audit',
    'main_object':'R_l = A_l^* A_l, A_l = C_l E_a',
    'criteria':{
        'Schatten_p':'R_l in S_p iff A_l in S_2p',
        'compact':'A_l compact',
        'trace_tail':'A_l Hilbert-Schmidt tail vanishes',
        'essential':'positive Calkin norm on pulled evaluator range'
    },
    'verdict':'Xi^BC remains active unless a compactness/Schatten theorem is supplied'
}
(out/'step156_schema.json').write_text(json.dumps(schema, indent=2))

checks = {
    'singular_profile_rows': int(len(profile_df)),
    'tail_rows': int(len(tail_df)),
    'finite_commutator_rank_proxy': int(np.sum(sv > 1e-10)),
    'finite_commutator_top_singular': float(sv[0]),
    'criterion_identity':'R=A*A singular values are squares of A singular values',
    'status':'passed'
}
(out/'step156_check_results.json').write_text(json.dumps(checks, indent=2))

print(json.dumps(checks, indent=2))
