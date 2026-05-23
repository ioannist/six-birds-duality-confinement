import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step49_adequacy_extension')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Exact adequacy with unbounded selector A_j: no residual, but target budget grows.
rows = []
for j in range(1, 51):
    K_native = 1.0
    A = float(j)
    K_resid = 0.0
    K_dissolve = A*A*K_native + K_resid
    rows.append({
        'j': j,
        'K_native': K_native,
        'A_norm': A,
        'K_residual': K_resid,
        'K_dissolving': K_dissolve,
        'status': 'exact_adequacy_but_no_uniform_budget' if K_dissolve > 100 else 'finite_stage_only'
    })
pd.DataFrame(rows).to_csv(OUT/'exact_adequacy_unbounded_A_step49.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot([r['j'] for r in rows], [r['K_dissolving'] for r in rows], marker='o', markersize=3)
plt.xlabel('stage j')
plt.ylabel('dissolving currency K_D = j^2')
plt.title('Exact adequacy is not enough if A_j is unbounded')
plt.tight_layout()
plt.savefig(OUT/'exact_adequacy_unbounded_A_step49.png', dpi=180)
plt.close()

# 2. Residual blind spot grows: native remains safe, but residual adequacy defect grows.
rows = []
for j in range(1, 51):
    K_native = 1.0
    A = 1.0
    M = float(j)
    K_resid = M*M
    # optimized t for trace scalar: (sqrt(a)+sqrt(b))^2 with a=A^2 K_native, b=K_resid
    a = A*A*K_native
    b = K_resid
    opt_bound = (np.sqrt(a)+np.sqrt(b))**2
    rows.append({
        'j': j,
        'K_native': K_native,
        'A_norm': A,
        'residual_amplitude': M,
        'K_residual': K_resid,
        'optimized_bound': opt_bound,
        'status': 'failed_predictive_adequacy'
    })
pd.DataFrame(rows).to_csv(OUT/'growing_blind_spot_step49.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot([r['j'] for r in rows], [r['K_residual'] for r in rows], label='residual currency $K_R$')
plt.plot([r['j'] for r in rows], [r['optimized_bound'] for r in rows], label='optimized dissolving bound')
plt.xlabel('stage j')
plt.ylabel('currency')
plt.title('Growing adequacy blind spot destroys predictive layer membrane')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'growing_blind_spot_step49.png', dpi=180)
plt.close()

# 3. Summable/contracting adequacy residuals: predictive budget remains bounded and may vanish.
rows = []
xi = 1.0
q = 0.72
for j in range(0, 80):
    f = 1.0/(j+2)**3
    if j > 0:
        xi = q*xi + f
    native_budget = 1.0
    A_norm_sq = 1.5
    # optimize scalar bound with t: (sqrt(a)+sqrt(b))^2 where a=A^2 theta, b=xi
    a = A_norm_sq*native_budget
    b = xi
    bound = (np.sqrt(a)+np.sqrt(b))**2
    rows.append({'j':j,'q':q,'new_defect_f_j':f,'Xi_j':xi,'AThetaA':a,'optimized_bound':bound})
pd.DataFrame(rows).to_csv(OUT/'contracting_adequacy_defect_step49.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot([r['j'] for r in rows], [r['Xi_j'] for r in rows], label='adequacy residual $\Xi_j$')
plt.plot([r['j'] for r in rows], [r['optimized_bound'] for r in rows], label='optimized dissolving budget')
plt.xlabel('stage j')
plt.ylabel('currency')
plt.title('Contracting adequacy residual gives stable dissolving budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'contracting_adequacy_defect_step49.png', dpi=180)
plt.close()

# 4. Random finite exact and defective adequacy checks.
rng = np.random.default_rng(49)
rows = []
for trial in range(80):
    n=5; y=3; z=4
    X = rng.normal(size=(n,n)); C = X.T@X + 0.5*np.eye(n)
    Cinv = np.linalg.inv(C)
    L = rng.normal(size=(y,n))
    A = rng.normal(size=(z,y))
    R = 0.05*rng.normal(size=(z,n))
    D = A@L + R
    K_L = L@Cinv@L.T
    K_D = D@Cinv@D.T
    K_R = R@Cinv@R.T
    # exact bound with t=1: K_D <= 2 A K_L A^T + 2 K_R
    B = 2*A@K_L@A.T + 2*K_R
    mineig = np.linalg.eigvalsh(B-K_D).min()
    # optimized trace bound scalar
    trA = np.trace(A@K_L@A.T)
    trR = np.trace(K_R)
    opt = (np.sqrt(max(trA,0))+np.sqrt(max(trR,0)))**2
    rows.append({'trial':trial,'min_eig_bound_minus_actual':mineig,'trace_actual':np.trace(K_D),'trace_optimized_bound':opt,'trace_bound_gap':opt-np.trace(K_D)})
pd.DataFrame(rows).to_csv(OUT/'random_defective_adequacy_checks_step49.csv', index=False)

# theorem map, gate table, schema
pd.DataFrame([
    {'id':'T49.1','name':'Exact adequacy transfer','statement':'D=A L implies K_D=A K_L A^*','depends_on':'Step23, Step42, Step48'},
    {'id':'T49.2','name':'Defective adequacy transfer','statement':'D=A L+R implies K_D <= (1+t)AK_LA^*+(1+t^{-1})K_R','depends_on':'Step42, Step48'},
    {'id':'T49.3','name':'Predictive adequacy propagation','statement':'Native predictive membrane plus budgeted adequacy residuals yields dissolving predictive membrane','depends_on':'Step25, Step41'},
    {'id':'T49.4','name':'Adequacy under strict extension','statement':'Summable/contracting residual recurrence preserves or collapses adequacy defects','depends_on':'Step30, Step47'},
    {'id':'NG49.1','name':'Exact adequacy not enough without bounded A_j','statement':'D_j=A_j L_j with ||A_j|| unbounded can destroy uniform membrane','depends_on':'Countermodel'},
    {'id':'NG49.2','name':'Growing blind-spot no-go','statement':'Residual adequacy defect can grow while native membrane stays safe','depends_on':'Countermodel'},
]).to_csv(OUT/'theorem_map_step49.csv', index=False)

pd.DataFrame([
    {'gate':'formed_closure','requirement':'Claim is only for formed closure/layer','failure_status':'outside_scope'},
    {'gate':'native_membrane','requirement':'K_L,j <= Theta_Y,j predictively','failure_status':'failed_native_membrane'},
    {'gate':'adequacy_factor','requirement':'D_j = A_j L_j + R_j declared before test','failure_status':'failed_adequacy'},
    {'gate':'A_budget','requirement':'A_j Theta_Y,j A_j^* controlled by dissolving budget','failure_status':'unbounded_selector'},
    {'gate':'residual_currency','requirement':'K_R,j <= Xi_j with Xi controlled/summable/contracting','failure_status':'hidden_blind_spot'},
    {'gate':'strict_extension_record','requirement':'adequacy changes only via accepted strict all-six extension','failure_status':'smuggled_repair'},
    {'gate':'predictive_transport','requirement':'A_j,R_j,D_j,L_j transported into common response ledger','failure_status':'current_only'},
    {'gate':'null_legality','requirement':'residuals/probes annihilate legal null modes','failure_status':'fake_zero_budget'},
]).to_csv(OUT/'adequacy_extension_gate_table_step49.csv', index=False)

import json
schema = {
    'record':'NativeProbeAdequacyExtensionRecord',
    'objects':['formed_closure','E_j','C_Gamma_j','L_Gamma_j','D_Gamma_j','A_j','R_j','Theta_Y_j','Xi_j','Omega_Z_j','response_transports','strict_extension_record'],
    'currencies':{
        'native':'K_L_j = L_Gamma_j C_Gamma_j^dagger L_Gamma_j^*',
        'dissolving':'K_D_j = D_Gamma_j C_Gamma_j^dagger D_Gamma_j^*',
        'residual':'K_R_j = R_j C_Gamma_j^dagger R_j^*'
    },
    'exact_adequacy':'D_Gamma_j = A_j L_Gamma_j',
    'defective_adequacy':'D_Gamma_j = A_j L_Gamma_j + R_j with K_R_j <= Xi_j',
    'accepted_if':['native predictive membrane accepted','A_j Theta_Y_j A_j^* controlled','residual Xi_j controlled','null legality','strict extension / transport defects recorded','no smuggling / no overreading'],
    'conclusion':'K_D_j <= Omega_Z_j for all accepted stages; no hidden layer-dissolving predictive needles'
}
(OUT/'native_probe_adequacy_extension_schema_step49.json').write_text(json.dumps(schema, indent=2))
