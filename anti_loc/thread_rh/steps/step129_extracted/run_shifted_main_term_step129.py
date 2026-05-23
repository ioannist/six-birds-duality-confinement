import os, math, json, csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.special import digamma
except Exception:
    digamma = None

OUT = Path('/mnt/data/rh_membrane_step129_shifted_main_term_audit')
OUT.mkdir(parents=True, exist_ok=True)

gamma_const = 0.5772156649015328606
psi_quarter = float(digamma(0.25)) if digamma else -4.2274535333762655

def Cq(q):
    return math.log(q/math.pi) + 2*gamma_const + psi_quarter

def kernel_matrix(q, N):
    C = Cq(q)
    K = np.zeros((N,N), dtype=float)
    for m in range(1, N+1):
        for n in range(1, N+1):
            g = math.gcd(m,n)
            K[m-1,n-1] = g/(m*n) * (C - math.log((m*n)/(g*g)))
    H = np.diag([1/n for n in range(1,N+1)])
    Hminushalf = np.diag([math.sqrt(n) for n in range(1,N+1)])
    S = Hminushalf @ K @ Hminushalf
    return K,H,(S+S.T)/2

# Formula CSV
formula_rows = [
    ['object','formula','status'],
    ['shifted moment','I_{alpha,beta}=phi_plus(q)^{-1} sum^+ L(1/2+alpha,chi)L(1/2+beta,chibar)|A(chi)|^2','imported from BPRZ'],
    ['Dirichlet polynomial','A(chi)=sum_{n<=q^kappa} alpha_n chi(n)/sqrt(n)','imported from BPRZ'],
    ['length range','kappa < 1/2 + 1/202 = 51/101','imported from BPRZ'],
    ['unshifted main kernel','K_q(m,n)=gcd(m,n)/(mn)*(C_q-log(mn/gcd(m,n)^2))','derived shifted-limit audit'],
    ['constant','C_q=log(q/pi)+2 gamma + psi(1/4)','normalization to verify against source'],
    ['coefficient norm','H_q(alpha)=sum |alpha_n|^2/n','framework source norm'],
    ['lower-frame target','H^{-1/2} M_q H^{-1/2} >= c_0 log(q) I','unearned'],
]
with open(OUT/'shifted_main_kernel_formula_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(formula_rows)

# Gate table
rows = [
    ['gate','statement','status','failure mode'],
    ['M1 shifted-limit legality','alpha,beta -> 0 inside uniform shifted theorem; pole cancellation audited','open','wrong constant or illegal limiting path'],
    ['M2 main-kernel lower eigenvalue','M_q >= c0 log(q) H_q uniformly on residual coefficient class','open','scalar moment but no matrix floor'],
    ['M3 subordinate error','|Err(a)| <= eps c0 log(q)||a||_H^2 uniformly in a','open','asymptotic not uniform enough for eigenvalues'],
    ['M4 sector records','even/odd, primitive, principal removal, parity/root-number recorded','partially imported','hidden rank-one/sector loss'],
    ['M5 visibility coupling','R_N^* H R_N >= c_hyb G_R','carried from Steps 117-124','coefficient blind spot'],
    ['M6 completed promotion','finite residual windows promote by fixed/exhaustive tail','open','moving-window support only'],
]
with open(OUT/'shifted_main_term_gate_table_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)

# Arithmetic input table
inputs = [
    ['input','source/platform','what it supplies','still needed'],
    ['BPRZ twisted second moment','arXiv:1808.10803','arbitrary coefficient shifted second moment up to kappa<51/101','lower-eigenvalue interpretation of main term and uniform error'],
    ['CIS asymptotic large sieve','arXiv:1105.1176','bilinear primitive-character infrastructure','lower-frame formulation with weights'],
    ['Tang-Wu mixed moments','arXiv:2512.09203','hybrid mixed moment with power saving','translation to residual coefficient matrix lower frame'],
    ['Gao-Wu-Zhao/DPR q-aspect mollified fourth moment','arXiv:2509.24690','q-aspect mollified length boundary','compatibility with Burnol/Muentz shadow length'],
    ['Burnol Sonine/co-Poisson','uploaded Burnol papers','carrier and zero-evaluator completeness/minimality','residual visibility and tail promotion'],
]
with open(OUT/'arithmetic_input_table_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(inputs)

# Theorem map
thm = [
    ['theorem/lemma','content','depends on','feeds'],
    ['Shifted-limit kernel lemma','BPRZ shifted main term yields GCD-log kernel at alpha=beta=0','BPRZ theorem and gamma/zeta expansion','main-kernel positivity audit'],
    ['Main-kernel import criterion','M_q >= c0 log(q) H_q plus subordinate error implies weighted source frame','lower eigenvalue + error norm','residual source coercivity'],
    ['Residual coupling lemma','G_q,w >= gamma H and R^*HR >= cG imply R^*G_q,wR >= gamma c G_R','finite operator algebra','completed membrane source route'],
    ['Subcritical heuristic','for kappa<1/2 diagonal log-conductor margin is available','length bound L<sqrt(q)','safe preliminary window'],
    ['Beyond-half warning','for kappa>1/2 offdiagonal main term is load-bearing','BPRZ length range','matrix-lift gap'],
]
with open(OUT/'theorem_map_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(thm)

# Route status
route = [
    ['component','status','comment'],
    ['unweighted finite character frame','settled','prime conductor orthogonality'],
    ['source weighted Gram','active','needs lower eigenvalue'],
    ['BPRZ theorem platform','accepted import platform','arbitrary coefficients and length beyond 1/2'],
    ['shifted main term positivity','active','GCD-log lower eigenvalue unearned'],
    ['operator-norm error','open','published scalar asymptotic must be read uniformly in coefficient vector'],
    ['visibility floor','carried','depends on Burnol-to-Dirichlet angular gap'],
    ['completed residual tail','open','fixed/exhaustive promotion required'],
]
with open(OUT/'route_status_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(route)

# numerical toy checks
q_values = [10**6,10**8,10**10,10**12]
N_values = [10,20,40,80,120]
check_rows = [['q','N','Cq','lambda_min_normalized','lambda_min_over_logq','lambda_max_normalized']]
for q in q_values:
    for N in N_values:
        K,H,S = kernel_matrix(q,N)
        eig = np.linalg.eigvalsh(S)
        check_rows.append([q,N,Cq(q),eig[0],eig[0]/math.log(q),eig[-1]])
with open(OUT/'main_kernel_eigenvalue_toy_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(check_rows)

# length regimes for kappa
length_rows = [['kappa','length_exponent','diagonal_margin_1_minus_2kappa','BPRZ_available','diagonal_dominance_safe']]
for k in np.linspace(0.1,0.55,46):
    length_rows.append([round(float(k),4),round(float(k),4),round(float(1-2*k),4),k<51/101,k<0.5])
with open(OUT/'length_regime_positivity_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(length_rows)

# main/error model
model_rows = [['epsilon','main_c0_logq','error_fraction','certified_gamma_over_logq']]
for eps in np.linspace(0,1.2,49):
    certified = max(0,1-eps)
    model_rows.append([eps,1,eps,certified])
with open(OUT/'main_error_import_gate_step129.csv','w',newline='') as f:
    csv.writer(f).writerows(model_rows)

# plots
# 1 Eigenvalue vs N for q values
plt.figure(figsize=(7,5))
for q in q_values:
    xs=[]; ys=[]
    for N in N_values:
        _,_,S = kernel_matrix(q,N)
        eig=np.linalg.eigvalsh(S)
        xs.append(N); ys.append(eig[0]/math.log(q))
    plt.plot(xs,ys,marker='o',label=f'q={q:.0e}')
plt.xlabel('Coefficient window dimension N')
plt.ylabel('toy min eigenvalue / log(q)')
plt.title('Shifted main-kernel lower-eigenvalue toy audit')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'main_kernel_lower_eigenvalue_toy_step129.png',dpi=160)
plt.close()

# 2 length margin
ks=np.linspace(0.05,0.55,101)
margin=1-2*ks
plt.figure(figsize=(7,5))
plt.plot(ks,margin)
plt.axhline(0, linestyle='--')
plt.axvline(0.5, linestyle='--')
plt.axvline(51/101, linestyle=':')
plt.xlabel('kappa')
plt.ylabel('naive diagonal margin 1-2 kappa')
plt.title('Subcritical diagonal margin versus BPRZ beyond-half range')
plt.tight_layout()
plt.savefig(OUT/'length_window_positivity_step129.png',dpi=160)
plt.close()

# 3 shifted limit components schematic
z=np.linspace(-0.08,0.08,400)
z=z[z!=0]
# simple schematic of pole cancellation: zeta approximations by +-1/(2z)+gamma and q factor constant K for q=1e8
q=1e8; K=math.log(q/math.pi)+psi_quarter
comp1=1/(2*z)+gamma_const
comp2=-(1/(2*z))+gamma_const+K
combined=comp1+comp2
plt.figure(figsize=(7,5))
plt.plot(z, np.clip(comp1,-100,100), label='zeta(1+2z) pole part')
plt.plot(z, np.clip(comp2,-100,100), label='dual shifted pole part')
plt.plot(z, combined, label='finite combined constant')
plt.xlabel('symmetric shift z')
plt.ylabel('schematic contribution')
plt.title('Pole cancellation in the shifted main term')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'shifted_limit_components_step129.png',dpi=160)
plt.close()

# 4 error subordinate model
err=np.linspace(0,1.2,100)
cert=np.maximum(0,1-err)
plt.figure(figsize=(7,5))
plt.plot(err,cert)
plt.xlabel('relative operator error epsilon')
plt.ylabel('certified lower-frame fraction')
plt.title('Main/error import gate: subordinate error required')
plt.tight_layout()
plt.savefig(OUT/'main_error_import_gate_step129.png',dpi=160)
plt.close()

# JSON schema
schema = {
    'step':129,
    'name':'Shifted Main-Term Positivity Audit',
    'main_kernel':'K_q(m,n)=gcd(m,n)/(mn)*(C_q-log(mn/gcd(m,n)^2))',
    'constant':'C_q=log(q/pi)+2 gamma+psi(1/4) under the symmetric shifted-limit normalization',
    'active_gate':'lower eigenvalue of H^{-1/2} M_q H^{-1/2} of order log q',
    'nonclaims':['not an RH proof','toy eigenvalues are not evidence','BPRZ import still requires lower-eigenvalue and error-norm records'],
    'next_step':'GCD-log kernel lower-frame audit'
}
with open(OUT/'step129_schema.json','w') as f:
    json.dump(schema,f,indent=2)

# latex balance simple check
tex=(OUT/'shifted_main_term_positivity_step129.tex').read_text()
checks=[]
for token in ['\\begin{document}','\\end{document}']:
    checks.append([token, tex.count(token)])
for env in ['theorem','proposition','definition','warning','gate']:
    checks.append([env, tex.count('\\begin{'+env+'}'), tex.count('\\end{'+env+'}')])
with open(OUT/'latex_structure_check_step129.csv','w',newline='') as f:
    csv.writer(f).writerows([['item','begin_count','end_count'],*checks])

print('Step 129 artifacts created in', OUT)
