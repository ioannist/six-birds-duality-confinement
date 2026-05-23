import numpy as np
import csv, json, math
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data/rh_membrane_step98_character_lower_frame')
OUT.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Helpers
# ----------------------------
def dft_matrix(n):
    j=np.arange(n)[:,None]
    k=np.arange(n)[None,:]
    return np.exp(2j*np.pi*j*k/n)/np.sqrt(n)

def frame_operator_from_rows(U, rows):
    A=U[rows,:]
    return A.conj().T @ A

def eigvals_herm(A):
    return np.linalg.eigvalsh((A+A.conj().T)/2).real

# 1. Full character tight frame checks for cyclic groups
full_rows=[]
for n in [3,4,5,7,8,11,16,24,32]:
    U=dft_matrix(n)
    F=frame_operator_from_rows(U, list(range(n)))
    ev=eigvals_herm(F)
    full_rows.append({
        'group':'C_%d'%n,
        'dimension':n,
        'min_eigenvalue':ev.min(),
        'max_eigenvalue':ev.max(),
        'fro_error_from_identity':np.linalg.norm(F-np.eye(n),'fro'),
        'status':'tight_frame_exact_up_to_roundoff'
    })
with open(OUT/'finite_group_frame_checks_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(full_rows[0].keys()))
    w.writeheader(); w.writerows(full_rows)

# 2. Partial character failures: use low-frequency character subsets of C_n
partial_rows=[]
for n in [16,32,64]:
    U=dft_matrix(n)
    for m in [1,2,4,8, min(12,n-1)]:
        rows=list(range(min(m,n)))
        F=frame_operator_from_rows(U, rows)
        ev=eigvals_herm(F)
        partial_rows.append({
            'group':'C_%d'%n,
            'dimension':n,
            'characters_used':len(rows),
            'min_eigenvalue':ev.min(),
            'max_eigenvalue':ev.max(),
            'rank_estimate':int((ev>1e-9).sum()),
            'nullity_estimate':int((ev<=1e-9).sum()),
            'status':'fails_full_lower_frame' if ev.min()<1e-9 else 'passes'
        })
with open(OUT/'partial_subset_eigenvalues_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(partial_rows[0].keys()))
    w.writeheader(); w.writerows(partial_rows)

# 3. Moving window tail requirement model
# Completed response is l^2 sequence with weights. Finite character window controls first N coords.
# Tail T_N is sum_{k>N} weights_k for several decay laws.
Nvals=np.arange(1,121)
tail_rows=[]
for law in ['p=1.5','p=2.0','p=3.0','flat_bad']:
    if law=='flat_bad':
        weights=np.ones(200000)
    else:
        p=float(law.split('=')[1])
        ks=np.arange(1,200001)
        weights=ks**(-p)
        weights=weights/weights.sum()
    for N in Nvals:
        tail=float(weights[N:].sum())
        tail_rows.append({'N':int(N),'tail_law':law,'tail_trace':tail,'status':'vanishing_tail' if law!='flat_bad' else 'nontrace_tail'})
with open(OUT/'moving_window_tail_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(tail_rows[0].keys()))
    w.writeheader(); w.writerows(tail_rows)

# 4. Lower-frame budget collapse toy: Lambda_N with vanishing/nonvanishing defects
budget_rows=[]
for scenario in ['full_frame_vanishing_tail','full_frame_fixed_defect','moving_window_no_tail','partial_frame_hole']:
    for N in Nvals:
        if scenario=='full_frame_vanishing_tail':
            Lambda=N
            defect=1/N**1.3
            hole=0
        elif scenario=='full_frame_fixed_defect':
            Lambda=N
            defect=0.05
            hole=0
        elif scenario=='moving_window_no_tail':
            Lambda=N
            defect=1/N
            hole=0.25
        else:
            Lambda=N
            defect=1/N
            hole=1.0
        budget=1/Lambda + defect + hole
        budget_rows.append({'N':int(N),'scenario':scenario,'Lambda':Lambda,'defect':defect,'hidden_tail_or_hole':hole,'certified_budget':budget})
with open(OUT/'completed_lower_frame_budget_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(budget_rows[0].keys()))
    w.writeheader(); w.writerows(budget_rows)

# Plots
plt.figure(figsize=(6,4))
plt.plot([r['dimension'] for r in full_rows],[r['fro_error_from_identity'] for r in full_rows],marker='o')
plt.xlabel('dimension of cyclic group C_n')
plt.ylabel('Frobenius error from I')
plt.title('Full character family gives tight frame')
plt.tight_layout(); plt.savefig(OUT/'full_character_tight_frame_step98.png',dpi=160); plt.close()

plt.figure(figsize=(6,4))
for n in [16,32,64]:
    xs=[r['characters_used'] for r in partial_rows if r['dimension']==n]
    ys=[r['nullity_estimate'] for r in partial_rows if r['dimension']==n]
    plt.plot(xs,ys,marker='o',label=f'C_{n}')
plt.xlabel('characters used')
plt.ylabel('nullity of partial source frame')
plt.title('Partial character windows leave hidden directions')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'partial_character_failure_step98.png',dpi=160); plt.close()

plt.figure(figsize=(6,4))
for law in ['p=1.5','p=2.0','p=3.0']:
    xs=[r['N'] for r in tail_rows if r['tail_law']==law]
    ys=[r['tail_trace'] for r in tail_rows if r['tail_law']==law]
    plt.loglog(xs,ys,label=law)
plt.xlabel('finite window N')
plt.ylabel('tail trace')
plt.title('Finite windows need vanishing tail')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'moving_windows_tail_requirement_step98.png',dpi=160); plt.close()

plt.figure(figsize=(6,4))
for scenario in ['full_frame_vanishing_tail','full_frame_fixed_defect','moving_window_no_tail','partial_frame_hole']:
    xs=[r['N'] for r in budget_rows if r['scenario']==scenario]
    ys=[r['certified_budget'] for r in budget_rows if r['scenario']==scenario]
    plt.plot(xs,ys,label=scenario.replace('_',' '))
plt.yscale('log')
plt.xlabel('stage N')
plt.ylabel('certified anti-invariant budget')
plt.title('Completed lower frame: budget collapse vs support-only')
plt.legend(fontsize=7); plt.tight_layout(); plt.savefig(OUT/'completed_lower_frame_budget_step98.png',dpi=160); plt.close()

# Tables
gate_rows=[
    {'gate':'finite quotient tight frame','condition':'complete character family of finite abelian quotient G','output':'sum_chi P_chi = I on l2(G)','status':'proved in Step 98'},
    {'gate':'Dirichlet unit group scope','condition':'characters modulo q are full on G_q=(Z/qZ)^x','output':'tight frame only on unit quotient readout','status':'accepted finite window'},
    {'gate':'primitive-only warning','condition':'primitive characters or selected characters only','output':'may leave imprimitive/invariant directions uncharged','status':'support-only unless completion proof'},
    {'gate':'completed lower frame','condition':'sum over windows/sources dominates full Y^- with Lambda_n -> infinity','output':'anti-invariant currency collapse','status':'open RH source obligation'},
    {'gate':'tail/exhaustivity','condition':'I_Y <= Pi_n^*Pi_n + T_n and tr(T_n)->0','output':'finite windows promote to completed ledger','status':'required'},
    {'gate':'no-smuggling','condition':'source windows declared by conductor/Hecke carrier, not target-selected','output':'upstream-visible source ladder','status':'required'}
]
with open(OUT/'finite_character_gate_table_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(gate_rows[0].keys()))
    w.writeheader(); w.writerows(gate_rows)

theorem_rows=[
    {'theorem':'Finite character tight frame','statement':'For finite abelian G, normalized characters form an orthonormal basis of l2(G); the full character analysis operator is unitary.'},
    {'theorem':'Partial character no-go','statement':'A proper character subset has zero lower frame on the orthogonal complement of its span.'},
    {'theorem':'Window-to-completed promotion','statement':'Finite-window lower frames promote only with reconstruction/tail bridge I <= Pi_n^*Pi_n + T_n and tail -> 0.'},
    {'theorem':'Completed source-collapse','statement':'If F_n >= Lambda_n Theta^{-1} with Lambda_n -> infinity and defects vanish, then K_n^- <= Lambda_n^{-1}Theta + defects -> 0.'},
    {'theorem':'Large-sieve warning','statement':'Upper frame/average bounds do not provide the lower frame required by membrane budget collapse.'}
]
with open(OUT/'theorem_map_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(theorem_rows[0].keys()))
    w.writeheader(); w.writerows(theorem_rows)

status_rows=[
    {'object':'complete characters of fixed finite quotient','frame_status':'tight on finite quotient','promotion_status':'finite-window only'},
    {'object':'Dirichlet characters modulo q','frame_status':'tight on unit group','promotion_status':'requires readout map and tail'},
    {'object':'primitive characters only','frame_status':'not complete in general','promotion_status':'support-only unless missing sectors handled'},
    {'object':'conductor ladder q<=Q','frame_status':'candidate exhausting family','promotion_status':'requires Plancherel/exhaustivity'},
    {'object':'Hecke/idèle class characters','frame_status':'candidate completed Plancherel family','promotion_status':'strongest route, still carrier-dependent'},
    {'object':'trace-only averages','frame_status':'upper/statistical shadow','promotion_status':'not a lower frame'}
]
with open(OUT/'character_window_status_table_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(status_rows[0].keys()))
    w.writeheader(); w.writerows(status_rows)

arith_rows=[
    {'input':'finite orthogonality','needed_form':'sum_chi chi(a)conj(chi(b)) = |G| 1_{a=b} on G','why':'gives tight finite source frame'},
    {'input':'semilocal readout map','needed_form':'R_S:Y^- -> l2(G_S) or L2(character window)','why':'connects finite quotient source to zeta response'},
    {'input':'Plancherel/exhaustivity','needed_form':'integral/sum over characters reconstructs full response modulo tail','why':'promotes finite windows to completed lower frame'},
    {'input':'tail decay','needed_form':'tr T_n -> 0 or operator-norm defect -> 0','why':'turns moving finite windows into exact squeeze'},
    {'input':'lower frame, not upper average','needed_form':'F_n >= Lambda_n Theta^{-1}','why':'collapses budget rather than merely bounding averages'},
    {'input':'all-six source record','needed_form':'declared conductor/order, route, packaging, audit, defects','why':'prevents target-selected source smuggling'}
]
with open(OUT/'arithmetic_input_table_step98.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(arith_rows[0].keys()))
    w.writeheader(); w.writerows(arith_rows)

# Schema
schema={
    'step':'98',
    'title':'Finite Character Orthogonality versus Completed Lower-Frame Audit',
    'objects':['finite abelian quotient G','character family Ghat','finite frame operator F_G','completed response space Y_minus','window projection Pi_n','tail operator T_n','source frame F_n'],
    'main_implication':'finite tight frame + exhaustive tail + full lower frame growth => completed anti-invariant budget collapse',
    'nonclaims':['finite character orthogonality alone proves RH','primitive characters alone are complete','moving finite windows promote without tail','large-sieve upper bounds imply lower frame']
}
with open(OUT/'step98_schema.json','w') as f:
    json.dump(schema,f,indent=2)

print('Step 98 artifacts written to',OUT)
