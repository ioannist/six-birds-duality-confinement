import csv, json, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step45_all_six_record')
OUT.mkdir(parents=True, exist_ok=True)

def eigmax(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[-1])

def eigmin(A):
    return float(np.linalg.eigvalsh((A + A.T)/2)[0])

# Six omitted-channel countermodels. These are illustrative finite witnesses, not simulations.
rows = []
# P1 rewrite/gauge hidden slow mode
for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    cap = 1/eps
    budget = 1.0
    rows.append({
        'channel_omitted':'P1_rewrite_gauge',
        'parameter':eps,
        'claimed_local_budget':budget,
        'actual_family_or_predictive_capacity':cap,
        'violation':cap-budget,
        'witness':'slow gauge-aligned probe e1 for C=diag(eps,1)',
        'matched_repair':'rewrite/quotient gauge direction or add audit strength on e1'
    })
# P2 channel/feasibility conditioning cancellation
for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    actual = 1.0
    naive = 2*eps*eps
    budget = max(0.1, 10*naive)
    rows.append({
        'channel_omitted':'P2_feasibility_frame',
        'parameter':eps,
        'claimed_local_budget':naive,
        'actual_family_or_predictive_capacity':actual,
        'violation':actual-naive,
        'witness':'psi_plus - psi_minus recovers e2 needle despite tiny branch responses',
        'matched_repair':'lower frame/Riesz bound or support conditioning record'
    })
# P3 route/holonomy route-local vs stacked protocol
m=2
K=np.ones((m,m)); Theta=np.eye(m)
rows.append({
    'channel_omitted':'P3_route_holonomy',
    'parameter':m,
    'claimed_local_budget':1.0,
    'actual_family_or_predictive_capacity':eigmax(K),
    'violation':eigmax(K-Theta),
    'witness':'mixed-route recombination (1,1)/sqrt(2)',
    'matched_repair':'route-union/block protocol currency matrix'
})
# P4 staging/refinement current-only vs predictive
for n in [2,5,10,50]:
    cap = n
    budget = 1
    rows.append({
        'channel_omitted':'P4_staging_refinement',
        'parameter':n,
        'claimed_local_budget':budget,
        'actual_family_or_predictive_capacity':cap,
        'violation':cap-budget,
        'witness':'future probe e2 in K_n=diag(1,n)',
        'matched_repair':'predictive transport and summable defect budget'
    })
# P5 packaging/canonicalization public shadow
for M in [2,10,100,1000]:
    shadow=1.0
    rows.append({
        'channel_omitted':'P5_packaging_canonicalization',
        'parameter':M,
        'claimed_local_budget':shadow,
        'actual_family_or_predictive_capacity':M,
        'violation':M-shadow,
        'witness':'hidden response direction forgotten by public shadow F=[1,0]',
        'matched_repair':'lawful package/canonicalization and faithful reconstruction bridge'
    })
# P6 audit/currency diagonal-only all-ones family
for m in [2,5,10,20]:
    K=np.ones((m,m)); Theta=np.eye(m)
    rows.append({
        'channel_omitted':'P6_audit_currency',
        'parameter':m,
        'claimed_local_budget':1.0,
        'actual_family_or_predictive_capacity':eigmax(K),
        'violation':eigmax(K-Theta),
        'witness':'all-ones recombination across m declared probes',
        'matched_repair':'full Loewner matrix budget K <= Theta, not diagonal-only audit'
    })

with open(OUT/'all_six_channel_countermodels_step45.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# Gate table
channel_gates = [
    ('P1','rewrite/gauge','carrier rewrites, gauges, and operator repairs declared; hidden gauge defects priced','hidden slow gauge-aligned needle or illegal carrier rewrite'),
    ('P2','feasibility/channel','exact feasible package, null-mode legality, frame/conditioning or channel bounds','cancellation needle / ill-conditioned channelization'),
    ('P3','route/holonomy','route-union or protocol block matrix, readout agreement defects','route-local certificate overread'),
    ('P4','staging/refinement','predictive transport, summable defect or common future budget','current-only certificate becomes future needle'),
    ('P5','packaging/canonicalization','idempotent/confluent package, lawful witness not public shadow, selector before test','post-hoc package or public-shadow overread'),
    ('P6','audit/currency','matrix currency K, threshold Theta, monotonicity/no diagonal-only audit','unpriced recombination / audit proxy failure'),
]
with open(OUT/'all_six_channel_gate_table_step45.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['channel','role','required_record','failure_if_missing'])
    w.writerows(channel_gates)

status_rows = [
    ('accepted','all six channels active/accepted and K_j <= Theta with completed witness ledger','accepted membrane claim'),
    ('support_only','mathematical bound exists but one or more channel records missing','evidence, not accepted anti-loc'),
    ('local_only','P3/P4/P43 block/gluing missing','local/section/protocol claim only'),
    ('failed_rewrite','P1 rewrite/gauge record fails','carrier claim not lawful'),
    ('failed_feasibility','P2 package/frame/null legality fails','feasible class admits needles or capacity infinite'),
    ('failed_route','P3 route-union/readout agreement fails','route-local overread'),
    ('failed_predictive','P4 refinement stability fails','current-depth only'),
    ('failed_packaging','P5 package/canonicalization fails','post-hoc or public-shadow overread'),
    ('failed_audit','P6 currency/budget fails','unpriced recombination witness'),
    ('overread','claim exceeds declared scope/nonclaim','downgrade or repair'),
]
with open(OUT/'all_six_channel_status_table_step45.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['status','condition','meaning'])
    w.writerows(status_rows)

# Create plot of maximum violation by omitted channel
summary = {}
for r in rows:
    c = r['channel_omitted']
    summary[c] = max(summary.get(c,0), float(r['violation']))
labels=list(summary.keys())
vals=[summary[k] for k in labels]
plt.figure(figsize=(11,5))
plt.bar(range(len(labels)), vals)
plt.yscale('log')
plt.xticks(range(len(labels)), [l.replace('_','\n') for l in labels], fontsize=8)
plt.ylabel('maximum violation in finite countermodel (log scale)')
plt.title('Omitting any Six Birds channel permits an anti-localization overclaim')
plt.tight_layout()
plt.savefig(OUT/'all_six_channel_countermodel_violations_step45.png', dpi=200)
plt.close()

# Plot representative pathways P4 and P6 for simple growth
p4_ns = np.arange(1,51)
p4_caps = p4_ns
p6_ms = np.arange(1,31)
p6_caps = p6_ms
plt.figure(figsize=(7,5))
plt.plot(p4_ns, p4_caps, label='P4 missing: predictive K_j = j')
plt.plot(p6_ms, p6_caps, label='P6 missing: all-ones recombination capacity = m')
plt.axhline(1, linestyle='--', label='diagonal/current budget')
plt.xlabel('stage j or family size m')
plt.ylabel('capacity of hidden witness')
plt.title('Current/diagonal certificates miss predictive and recombination witnesses')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_and_recombination_growth_step45.png', dpi=200)
plt.close()

# Theorem map and schema
theorem_map = [
    ('T45.1','All-six anti-localization record','Defines ALRecord with P1--P6 records and statuses','formed closure, exact package, declared native predictive family'),
    ('T45.2','All-six acceptance theorem','All six accepted + K_j <= Theta implies accepted membrane','Step41 membrane theorem plus all-channel audit'),
    ('T45.3','Channel necessity/separation theorem','Omitting any one channel admits a finite overclaim countermodel','countermodel atlas'),
    ('T45.4','Downgrade theorem','Missing channel forces support-only/local-only/failed status unless nonclaim narrows scope','status semantics'),
]
with open(OUT/'theorem_map_step45.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','name','content','depends_on']); w.writerows(theorem_map)

schema = {
  'ALRecord': {
    'formed_closure': 'closure/layer status and scope',
    'P1_rewrite_gauge': {'objects':['carrier rewrite maps','gauge quotient','operator repair'], 'accepted_if':'all carrier changes are bridged or defect-priced'},
    'P2_feasibility_channel': {'objects':['Gamma','C_Gamma','null quotient','frame/conditioning'], 'accepted_if':'exact feasible package and null-mode legality pass'},
    'P3_route_holonomy': {'objects':['route family','stacked protocol matrix','readout defects'], 'accepted_if':'route-union/block matrix controlled'},
    'P4_staging_refinement': {'objects':['stages j','response transports R_j','summable defects'], 'accepted_if':'predictive family budget persists'},
    'P5_packaging_canonicalization': {'objects':['packaging endomap','canonical selector','lawful witness'], 'accepted_if':'package is declared, idempotent/confluent enough, not post-hoc'},
    'P6_audit_currency': {'objects':['K_j','Theta','audit monotonicity','nonclaim ledger'], 'accepted_if':'full Loewner matrix budget and critical-pair ledger complete'},
    'outcome': 'accepted membrane iff all six channels accepted and no unresolved native predictive witness'
  },
  'currency': 'K_hat_j = R_j L_j Gamma_j (Gamma_j^* C_j Gamma_j)^dagger Gamma_j^* L_j^* R_j^*',
  'witness': 'y^*(K_hat_j-Theta)y > 0',
  'statuses': [r[0] for r in status_rows]
}
with open(OUT/'all_six_record_schema_step45.json','w') as f:
    json.dump(schema,f,indent=2)

print('Step 45 artifacts generated in', OUT)
