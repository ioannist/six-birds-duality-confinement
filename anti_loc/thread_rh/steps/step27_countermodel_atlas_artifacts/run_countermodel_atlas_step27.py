import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step27_countermodels')
OUT.mkdir(parents=True, exist_ok=True)


def pinv_psd(C, tol=1e-12):
    w, V = np.linalg.eigh(C)
    wi = np.array([1/x if x>tol else 0.0 for x in w])
    return (V*wi)@V.T


def cap_matrix(C, L):
    # L: m x n, C: n x n
    return L @ pinv_psd(C) @ L.T

rows=[]
controls=[]

def add_case(code, gate, failure, value, threshold, status, matched_control, control_value=None):
    rows.append({
        'code': code, 'gate_under_test': gate, 'failure_mode': failure,
        'diagnostic_value': value, 'safe_threshold': threshold,
        'status': status, 'matched_control': matched_control,
        'control_value': control_value
    })

# CM1 no closure / null-or-slow mode
for eps in [1e-1,1e-2,1e-3,1e-4,1e-5]:
    C=np.diag([eps,1.0]); L=np.array([[1.0,0.0]])
    K=cap_matrix(C,L)
    rows.append({'code':'CM1_slow_mode','gate_under_test':'formed_closure / no slow probe-aligned modes','failure_mode':'passive positive carrier has arbitrarily large capacity','epsilon':eps,'diagnostic_value':float(K[0,0]),'safe_threshold':10.0,'status':'failed_gate','matched_control':'CM1_control_eps1','control_value':1.0})

# Null mode exactly
C=np.diag([0.0,1.0]); L=np.array([[1.0,0.0]])
add_case('CM_null_mode','null_mode_legality','probe sees zero-energy direction; capacity infinite',math.inf,10.0,'failed_gate','null_control_probe_orthogonal',0.0)

# CM3 recombination all-ones
for m in [2,4,8,16,32,64]:
    C=np.array([[1.0]])
    L=np.ones((m,1))
    K=cap_matrix(C,L)
    maxeig=float(np.linalg.eigvalsh(K).max())
    rows.append({'code':'CM_recombination_all_ones','gate_under_test':'recombination_closure / matrix_budget','failure_mode':'all diagonal probe capacities are 1, but all-ones recombination capacity grows as m','m':m,'diagnostic_value':maxeig,'safe_threshold':1.0,'status':'failed_gate','matched_control':'orthogonal_probe_family','control_value':1.0})

# two probe correlation sweep
for rho in [0,0.25,0.5,0.75,0.9,0.99,0.999]:
    K=np.array([[1.0,rho],[rho,1.0]])
    maxeig=float(np.linalg.eigvalsh(K).max())
    rows.append({'code':'CM_two_probe_correlation','gate_under_test':'matrix_budget not diagonal_budget','failure_mode':'diagonal entries fixed at 1 while correlated recombination reaches 1+rho','rho':rho,'diagnostic_value':maxeig,'safe_threshold':1.0,'status':'failed_gate' if maxeig>1.00001 else 'control_ok','matched_control':'rho_zero','control_value':1.0})

# predictive failure
for j in [1,2,4,8,16,32,64]:
    K=np.diag([1.0,float(j)])
    maxeig=float(j)
    rows.append({'code':'CM_predictive_growth','gate_under_test':'predictive_stability / common_budget','failure_mode':'each level finite, no uniform predictive budget','j':j,'diagnostic_value':maxeig,'safe_threshold':4.0,'status':'failed_gate' if j>4 else 'within_current_threshold','matched_control':'summable_defect_or_constant_K','control_value':1.0})

# protocol diagonal vs block
C=np.array([[1.0]])
L_stack=np.array([[1.0],[1.0]])
K=cap_matrix(C,L_stack)
add_case('CM_protocol_block','protocol_honesty / block_route_budget','route-local diagonal checks pass, mixed protocol recombination fails',float(np.linalg.eigvalsh(K).max()),1.0,'failed_gate','protocol_orthogonal_routes',1.0)

# readout agreement transfer failure: Lp zero, Lq sees slow/different direction
C=np.eye(2)
Lp=np.array([[1.0,0.0]])
Lq=np.array([[1.0,3.0]])
Kp=cap_matrix(C,Lp)[0,0]
Kq=cap_matrix(C,Lq)[0,0]
D=cap_matrix(C,Lq-Lp)[0,0]
rows.append({'code':'CM_readout_disagreement','gate_under_test':'readout_agreement','failure_mode':'protocol q claims same readout as p but disagreement defect is large','Kp':Kp,'Kq':Kq,'defect':D,'diagnostic_value':Kq,'safe_threshold':Kp+1.0,'status':'failed_gate','matched_control':'readout_same_Lq_eq_Lp','control_value':Kp})

# compressed vs ambient overread example
C=np.diag([1.0,100.0])
g=np.array([1.0,0.0])
Gamma=np.array([[1.0/math.sqrt(2)],[1.0/math.sqrt(2)]])
Cgam=Gamma.T@C@Gamma
ggam=Gamma.T@g
cap_correct=float(ggam.T@pinv_psd(Cgam)@ggam)
P=Gamma@Gamma.T
ambient=float((P@g).T@pinv_psd(C)@(P@g))
rows.append({'code':'CM_public_shadow','gate_under_test':'lawful_witness_not_public_shadow','failure_mode':'ambient/public-shadow capacity is not the compressed carrier capacity','correct_compressed_cap':cap_correct,'ambient_shadow_cap':ambient,'diagnostic_value':ambient/cap_correct,'safe_threshold':1.0,'status':'overread_if_used_as_exact','matched_control':'reducing_subspace_Gamma_e1','control_value':1.0})

# approximate fallback source misses slow tail
for eps in [1e-2,1e-4,1e-6]:
    alpha=math.sqrt(eps)*10 # exact extra cap 100 independent; finite sees zero
    C=np.diag([1.0,eps]); L=np.array([[0.0,alpha]])
    K=cap_matrix(C,L)[0,0]
    rows.append({'code':'CM_fallback_tail','gate_under_test':'finite_to_exact / fallback_source_realness','failure_mode':'finite carrier omits a tiny slow tail that carries large capacity','epsilon':eps,'alpha':alpha,'diagnostic_value':float(K),'safe_threshold':1.0,'status':'failed_gate','matched_control':'tail_budget_included','control_value':float(K)})

# gating destroys cycle-supported drive / cancellation channels
for eps in [1e-1,1e-2,1e-3,1e-4,1e-5]:
    a=math.sqrt(1-eps**2)
    Gamma=np.array([[a,a],[eps,-eps]])
    C=np.eye(2)
    g=np.array([0.0,1.0])
    Cgam=Gamma.T@C@Gamma
    ggam=Gamma.T@g
    cap=float(ggam.T@pinv_psd(Cgam)@ggam)
    branch_sum=float((eps**2)+(eps**2))
    cond=float(np.linalg.cond(Gamma.T@Gamma))
    rows.append({'code':'CM_cancellation_cycle','gate_under_test':'P2 conditioning / recombination witness','failure_mode':'two harmless-looking branches recombine into a needle through ill-conditioning','epsilon':eps,'branchwise_trace':branch_sum,'conditioning':cond,'diagnostic_value':cap,'safe_threshold':branch_sum,'status':'failed_gate','matched_control':'orthogonal_branches','control_value':branch_sum})

# noncommuting completions order dependence
sqrt2=math.sqrt(2)
e1=np.array([[1.0],[0.0]])
v=np.array([[1.0/sqrt2],[1.0/sqrt2]])
P1=e1@e1.T; P2=v@v.T
E21=P2@P1; E12=P1@P2
# compare induced public signature on probe g=e2? or Frobenius order defect
order_def=float(np.linalg.norm(E21-E12,'fro'))
rows.append({'code':'CM_noncommuting_completion','gate_under_test':'P5 packaging / completion_order','failure_mode':'two idempotent completions do not commute; capacity depends on order unless ledger records it','diagnostic_value':order_def,'safe_threshold':0.0,'status':'failed_gate','matched_control':'commuting_projections','control_value':0.0})

# same level self-audit/post-hoc selection status diagnostic
rows.append({'code':'CM_posthoc_selector','gate_under_test':'no_smuggling / no_same_level_self_audit','failure_mode':'selector optimizes S6 margin and then claims S6 acceptance','diagnostic_value':1.0,'safe_threshold':0.0,'status':'support_only_or_smuggled','matched_control':'upstream_declared_selector','control_value':0.0})

# strict extension without macro closure
rows.append({'code':'CM_strict_without_closure','gate_under_test':'strict_extension_plus_macro_closure','failure_mode':'new predicate/layer added, but no family budget or transport; anti-loc does not follow','diagnostic_value':math.nan,'safe_threshold':math.nan,'status':'outside_claim_or_support_only','matched_control':'strict_extension_with_budget','control_value':math.nan})

# artifact / calibrated null controls row list
control_rows = [
    {'control_code':'CM1_control_eps1','matched_failure':'CM1_slow_mode','control_property':'same dimension and probe, but no slow mode; capacity = 1'},
    {'control_code':'null_control_probe_orthogonal','matched_failure':'CM_null_mode','control_property':'probe annihilates kernel; finite capacity on quotient'},
    {'control_code':'orthogonal_probe_family','matched_failure':'CM_recombination_all_ones','control_property':'same number of probes, orthogonal representers; K=I'},
    {'control_code':'rho_zero','matched_failure':'CM_two_probe_correlation','control_property':'same diagonal entries, zero off-diagonal; no recombination amplification'},
    {'control_code':'summable_defect_or_constant_K','matched_failure':'CM_predictive_growth','control_property':'uniform/summable defect gives common predictive budget'},
    {'control_code':'protocol_orthogonal_routes','matched_failure':'CM_protocol_block','control_property':'stacked protocol block is identity, not all-ones'},
    {'control_code':'readout_same_Lq_eq_Lp','matched_failure':'CM_readout_disagreement','control_property':'zero readout disagreement defect transfers budget exactly'},
    {'control_code':'reducing_subspace_Gamma_e1','matched_failure':'CM_public_shadow','control_property':'compressed and ambient capacities agree when the subspace reduces C'},
    {'control_code':'tail_budget_included','matched_failure':'CM_fallback_tail','control_property':'tail term explicitly charged in exact budget'},
    {'control_code':'orthogonal_branches','matched_failure':'CM_cancellation_cycle','control_property':'frame lower bound prevents cancellation needle'},
    {'control_code':'commuting_projections','matched_failure':'CM_noncommuting_completion','control_property':'commuting completions give order-independent packaging'},
    {'control_code':'upstream_declared_selector','matched_failure':'CM_posthoc_selector','control_property':'selector is declared before S6 and uses no S6 margin'},
]

pd.DataFrame(rows).to_csv(OUT/'countermodel_atlas_step27.csv', index=False)
pd.DataFrame(control_rows).to_csv(OUT/'matched_control_atlas_step27.csv', index=False)

# Gate table mapping
atlas = [
    ('G0 formed closure','CM1_slow_mode / CM_strict_without_closure','Unformed or merely strict artifact can have unpriced native needles.','Closure/layer first; claim outside scope otherwise.'),
    ('G1 exact package','CM_fallback_tail','Approximate/fallback carrier misses slow tail.','Use exact carrier or explicit tail budget.'),
    ('G2 null-mode legality','CM_null_mode','Probe sees zero-energy direction; capacity infinite.','Quotient/annihilate legal null modes.'),
    ('G3 declared native family','CM4 single-probe omission','Undeclared probe can be a needle.','Declare finite native family and scope.'),
    ('G4 recombination closure','CM_recombination_all_ones / CM_two_probe_correlation','Diagonal bounds miss mixed probes.','Matrix budget K ⪯ Θ.'),
    ('G5 route/protocol honesty','CM_protocol_block','Route-local budgets miss cross-route recombinations.','Stack protocols and certify block budget.'),
    ('G6 readout agreement','CM_readout_disagreement','Budgets cannot transfer across protocols without defect.','Pay readout disagreement defect.'),
    ('G7 predictive stability','CM_predictive_growth','Current finite budgets do not imply common future budget.','Uniform predictive budget or summable defects.'),
    ('G8 lawful witness','CM_public_shadow','Ambient/public shadow differs from compressed carrier witness.','Use compressed Schur witness or audited bridge.'),
    ('G9 packaging order','CM_noncommuting_completion','Completion order changes carrier/capacity.','Record order or prove commutation/confluence.'),
    ('G10 no-smuggling','CM_posthoc_selector','S6-optimized selector is circular.','Upstream-visible selector only.'),
    ('G11 conditioning/control','CM_cancellation_cycle','Branchwise delocalization can cancel into a needle.','Frame/conditioning/recombination control.'),
]
pd.DataFrame(atlas, columns=['gate','minimal_countermodel','what_fails','matched_control_principle']).to_csv(OUT/'gate_necessity_atlas_step27.csv', index=False)

# Matched-control suite mapping M-E-R benchmarks
benchmarks = [
    ('classical_mixture','orthogonal_probe_family','diagonal and matrix budgets coincide; no recombination needle'),
    ('hidden_predictive_memory_no_recombination','rho_zero_with_hidden_labels','branch labels may exist but no active recombination capacity'),
    ('route_marked_suppression','protocol_orthogonal_routes','route labels prevent mixed-protocol recombination'),
    ('erasure_conditioned_recovery','CM_cancellation_cycle','erasing marks or weakening conditioning recovers cancellation needle'),
    ('cyclic_family_generalization','CM_recombination_all_ones','multi-probe cycle has bounded diagonals but large top eigenvalue'),
    ('dissipative_washout','summable_defect_or_constant_K','refinement defects summable, predictive budget remains bounded'),
    ('artifact_controls','zero_probe_or_identity_control','null configurations should not show recombination growth')
]
pd.DataFrame(benchmarks, columns=['benchmark','model_or_control','anti_loc_interpretation']).to_csv(OUT/'mer_matched_control_suite_step27.csv', index=False)

# Plots
rows_df=pd.DataFrame(rows)
# Recombination growth
rec=rows_df[rows_df['code']=='CM_recombination_all_ones'].copy()
plt.figure(figsize=(6,4))
plt.plot(rec['m'], rec['diagnostic_value'], marker='o', label='top eigenvalue of K')
plt.axhline(1, linestyle='--', label='diagonal bound')
plt.xlabel('number of probes m')
plt.ylabel('capacity of all-ones recombination')
plt.title('Diagonal probe bounds do not control recombination')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'atlas_recombination_growth_step27.png', dpi=200)
plt.close()

# predictive growth
pred=rows_df[rows_df['code']=='CM_predictive_growth'].copy()
plt.figure(figsize=(6,4))
plt.plot(pred['j'], pred['diagnostic_value'], marker='o')
plt.axhline(4, linestyle='--', label='sample finite threshold')
plt.xlabel('refinement level j')
plt.ylabel('top predictive capacity')
plt.title('Finite current capacities need not give predictive budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'atlas_predictive_growth_step27.png', dpi=200)
plt.close()

# slow mode
slow=rows_df[rows_df['code']=='CM1_slow_mode'].copy()
plt.figure(figsize=(6,4))
plt.loglog(slow['epsilon'], slow['diagnostic_value'], marker='o')
plt.gca().invert_xaxis()
plt.xlabel('slow eigenvalue epsilon')
plt.ylabel('capacity')
plt.title('Passivity/positivity alone does not price a slow-mode probe')
plt.tight_layout()
plt.savefig(OUT/'atlas_slow_mode_step27.png', dpi=200)
plt.close()

# two probe rho
rho=rows_df[rows_df['code']=='CM_two_probe_correlation'].copy()
plt.figure(figsize=(6,4))
plt.plot(rho['rho'], rho['diagnostic_value'], marker='o')
plt.axhline(1, linestyle='--', label='diagonal bound')
plt.xlabel('off-diagonal correlation rho')
plt.ylabel('largest family capacity eigenvalue')
plt.title('Off-diagonal currency controls mixed probes')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'atlas_two_probe_correlation_step27.png', dpi=200)
plt.close()

# JSON schema
schema = {
    'name':'AcceptedTestFamilyNecessityAtlas',
    'purpose':'For each gate in AcceptedAntiLocTestFamily, provide a finite countermodel showing the gate is necessary and a matched control isolating the failure.',
    'claim':'Dropping any gate can turn a true-looking scalar/current/route-local certificate into a false family-level predictive anti-localization claim.',
    'gates':[g[0] for g in atlas],
    'countermodels':[g[1] for g in atlas],
    'matched_control_principle':'Every negative instance should be paired with a same-size or same-scope control in which the target gate is restored and the failure disappears.',
    'status':'proof-level necessity atlas; numerical script only verifies finite toy matrices and is support-only for exposition.'
}
(OUT/'countermodel_atlas_schema_step27.json').write_text(json.dumps(schema, indent=2))

print('wrote step27 artifacts to', OUT)
