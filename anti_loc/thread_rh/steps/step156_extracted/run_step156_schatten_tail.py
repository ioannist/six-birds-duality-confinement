import os, json, csv, math, zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step156_xi_bc_schatten_tail')
OUT.mkdir(parents=True, exist_ok=True)

# Singular value scenarios for residual synthesis E; Xi kernel eigenvalues are s^2.
n = np.arange(1, 401)
scenarios = {
    'trace_class_exp': np.exp(-0.025*n),
    'trace_class_power': n**(-0.8),      # E in S2 because sum n^-1.6
    'compact_not_trace': n**(-0.35),     # E compact, E not HS
    'noncompact_plateau': 0.18 + 0.35*n**(-0.5),
    'active_residual_floor': 0.08 + 0.2*np.exp(-0.01*n),
}

# CSV singular profiles
with open(OUT/'xi_bc_singular_value_profiles_step156.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['index']+list(scenarios.keys()))
    for i in range(len(n)):
        w.writerow([int(n[i])] + [float(scenarios[k][i]) for k in scenarios])

plt.figure(figsize=(7,4.5))
for label, vals in scenarios.items():
    plt.plot(n, vals, label=label.replace('_',' '))
plt.yscale('log')
plt.xlabel('singular-value index')
plt.ylabel('s_n(E)')
plt.title('Step 156 residual synthesis singular-value profiles')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_singular_value_profiles_step156.png', dpi=180)
plt.close()

# Tail sums of Xi = E^*E: trace tail sum s_n^2 from N onward.
tail_rows=[]
for N in [5,10,20,40,80,120,160,240,320]:
    row={'window_N':N}
    for label, vals in scenarios.items():
        row[label+'_trace_tail_proxy']=float(np.sum(vals[N:]**2))
        row[label+'_op_tail_proxy']=float(np.max(vals[N:]**2)) if N < len(vals) else 0.0
    tail_rows.append(row)
keys=list(tail_rows[0].keys())
with open(OUT/'xi_bc_tail_payability_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=keys)
    w.writeheader(); w.writerows(tail_rows)

plt.figure(figsize=(7,4.5))
for label, vals in scenarios.items():
    tails=np.array([np.sum(vals[N:]**2) for N in n[:-1]])
    plt.plot(n[:-1], tails, label=label.replace('_',' '))
plt.yscale('log')
plt.xlabel('window cutoff N')
plt.ylabel('trace-tail proxy sum_{n>N} s_n(E)^2')
plt.title('Trace-tail payability proxy for Xi^BC')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'xi_bc_tail_payability_step156.png', dpi=180)
plt.close()

# Schatten p partial sums for p = 1 (Xi trace), p=2 etc.
p_values=[0.5,1.0,2.0]
rows=[]
for label, vals in scenarios.items():
    for p in p_values:
        # Xi in S_p means sum eigenvalues^p = sum (s^2)^p = sum s^(2p)
        partial=np.cumsum(vals**(2*p))
        rows.append({'scenario':label,'p_for_Xi':p,'partial_at_50':float(partial[49]),'partial_at_200':float(partial[199]),'partial_at_400':float(partial[-1])})
with open(OUT/'schatten_partial_sums_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

plt.figure(figsize=(7,4.5))
for label, vals in scenarios.items():
    plt.plot(n, np.cumsum(vals**2), label=label.replace('_',' '))
plt.yscale('log')
plt.xlabel('partial cutoff')
plt.ylabel('partial trace proxy sum_{n<=N} s_n(E)^2')
plt.title('Schatten trace-class diagnostic for Xi^BC')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'schatten_trace_partial_sums_step156.png', dpi=180)
plt.close()

# Essential floor / Calkin witness profiles.
Nvals=np.arange(1,101)
essential_profiles={
    'essential_zero_compact': 1/Nvals,
    'essential_floor_low': 0.04 + 1/(10+Nvals),
    'essential_floor_high': 0.15 + 1/(20+Nvals),
    'unknown_active': 0.08 + 0.02*np.sin(Nvals/10.0)**2,
}
with open(OUT/'calkin_witness_profiles_step156.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['N']+list(essential_profiles.keys()))
    for i,Nv in enumerate(Nvals):
        w.writerow([int(Nv)] + [float(essential_profiles[k][i]) for k in essential_profiles])

plt.figure(figsize=(7,4.5))
for label, vals in essential_profiles.items():
    plt.plot(Nvals, vals, label=label.replace('_',' '))
plt.xlabel('window/cutoff N')
plt.ylabel('essential-norm proxy')
plt.title('Restricted Calkin-class witness profiles')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'restricted_calkin_witness_step156.png', dpi=180)
plt.close()

# Classification status table
classification = [
    {'status':'E_exact_exclusion','criterion':'C_l eta_z = 0 for all pulled zero evaluators','current':'open','consequence':'Xi^BC=0'},
    {'status':'T_compact_tail','criterion':'pi(C_l restricted to E_a)=0 or E_l,a compact','current':'not earned','consequence':'operator-norm tail payment'},
    {'status':'S1_trace_tail','criterion':'E_l,a Hilbert-Schmidt','current':'not earned','consequence':'trace-class Xi^BC and trace-tail payment'},
    {'status':'S_source_absorption','criterion':'non-circular signed/direct source budget','current':'blocked for positive trace squeeze','consequence':'would absorb residual'},
    {'status':'N_scoped_residual','criterion':'Xi^BC carried in theorem statement','current':'active','consequence':'conditional/nonclaim boundary'},
]
with open(OUT/'xi_bc_schatten_classification_table_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(classification[0].keys()))
    w.writeheader(); w.writerows(classification)

# Gate table
rows=[
    {'gate':'bounded residual synthesis','formal_test':'E_l,a extends boundedly from zero-coordinate core','status':'declared obligation','failure_mode':'kernel not even a closed residual operator'},
    {'gate':'compactness','formal_test':'s_n(E_l,a)->0 or pi(C_l|E_a)=0','status':'open','failure_mode':'essential boundary-packet sector survives'},
    {'gate':'trace-class','formal_test':'sum s_n(E_l,a)^2 < infinity','status':'open','failure_mode':'tail cannot be paid by trace ledger'},
    {'gate':'zero-window exhaustivity','formal_test':'Q_N -> I strongly on H_Z','status':'standard but must be declared','failure_mode':'moving-window support only'},
    {'gate':'Calkin inheritance','formal_test':'pulled evaluator closure avoids essential sector','status':'load-bearing next step','failure_mode':'Xi^BC noncompact'},
    {'gate':'nonclaim boundary','formal_test':'state Xi^BC as active residual if gates fail','status':'active','failure_mode':'overclaiming RH'}
]
with open(OUT/'xi_bc_schatten_gate_table_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# theorem map
rows=[
    {'item':'Schatten dictionary','statement':'R=E^*E compact/S_p iff E compact/S_2p','dependency':'basic Hilbert space theory','status':'proved abstractly'},
    {'item':'tail promotion','statement':'compact gives operator-norm tails; trace-class gives trace tails','dependency':'strong projection convergence','status':'proved abstractly'},
    {'item':'essential restriction test','statement':'compactness reduces to pi(C_l|E_a)=0','dependency':'Calkin algebra and pulled evaluator cofinality','status':'open criterion'},
    {'item':'noncompact inheritance','statement':'nonzero essential restriction implies noncompact residual kernel','dependency':'bounded lower Gram on essential sector','status':'conditional theorem'},
    {'item':'route verdict','statement':'Xi^BC remains active unless exact/compact/Schatten gate passes','dependency':'Step 155 classification','status':'active'}
]
with open(OUT/'theorem_map_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# route status
rows=[
    {'route':'direct exclusion','status':'open','note':'requires C_l eta_z=0 for all pulled evaluators'},
    {'route':'compact/tail payment','status':'not earned','note':'requires restricted Calkin class zero'},
    {'route':'trace-class payment','status':'not earned','note':'requires Hilbert-Schmidt residual synthesis'},
    {'route':'positive source-frame trace squeeze','status':'blocked','note':'source budget is collapse-strength'},
    {'route':'scoped residual','status':'active','note':'Xi^BC remains explicit adequacy residual'}
]
with open(OUT/'route_status_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# construction tasks
rows=[
    {'task':'Define zero-coordinate Hilbert model H_Z','target':'make E_l,a a closed/bounded synthesis map','priority':'high'},
    {'task':'Compute restricted Calkin class','target':'pi(C_l|E_a)=0 or nonzero','priority':'highest'},
    {'task':'Establish pulled-evaluator cofinality or avoidance','target':'decide whether evaluators hit boundary-packet essential sector','priority':'highest'},
    {'task':'Try Hilbert-Schmidt envelope','target':'sum ||C_l eta_z||^2 after Gram normalization','priority':'medium'},
    {'task':'If noncompact, write scoped Xi theorem','target':'avoid RH overclaim and publish diagnostic residual','priority':'high'}
]
with open(OUT/'construction_tasks_step156.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# nonclaim boundary
nonclaim='''# Step 156 nonclaim boundary

Step 156 does not prove RH.

It does not prove H_R=0.

It does not prove Xi^BC=0.

It does not prove that Xi^BC is compact, trace-class, Hilbert-Schmidt, or tail-payable.

It proves the abstract Schatten/tail classification of the residual kernel and reduces compactness to the restricted Calkin test

    pi(C_l restricted to E_a) ?= 0.

Until that test passes, Xi^BC remains an active adequacy residual.
'''
(OUT/'nonclaim_boundary_step156.md').write_text(nonclaim)

# schema
schema={
    'step':156,
    'title':'Xi^BC residual-kernel Schatten/tail audit',
    'active_residual':'Xi^BC_{ell,a}=B^* Pi_{Y_a} B',
    'main_operator':'E_{ell,a} e_z = C_ell eta_z',
    'main_kernel':'R_ell=E^*E',
    'verdict':'not classified as compact/tail-payable; restricted Calkin test required',
    'next_step':'Step 157: essential-support test for pulled evaluator family',
    'outputs':[p.name for p in OUT.iterdir() if p.is_file()]
}
(OUT/'step156_schema.json').write_text(json.dumps(schema,indent=2))

# check results
checks={
    'singular_profile_rows':len(n),
    'classification_rows':len(classification),
    'all_key_files_present':all((OUT/name).exists() for name in [
        'xi_bc_schatten_tail_step156.tex','step156_results_summary.md','xi_bc_schatten_gate_table_step156.csv','theorem_map_step156.csv','route_status_step156.csv','nonclaim_boundary_step156.md'
    ]),
    'max_noncompact_plateau_tail':float(np.max(scenarios['noncompact_plateau'][-50:])),
    'trace_class_exp_tail_320':float(np.sum(scenarios['trace_class_exp'][320:]**2)),
}
(OUT/'step156_check_results.json').write_text(json.dumps(checks,indent=2))

# Create zip after all files, excluding zip itself.
zip_path=OUT/'step156_xi_bc_schatten_tail_artifacts.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.is_file() and p.name != zip_path.name:
            z.write(p,arcname=p.name)
print(json.dumps(checks,indent=2))
