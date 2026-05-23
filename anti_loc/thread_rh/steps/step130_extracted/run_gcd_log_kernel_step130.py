import math, csv, json, os, zipfile
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step130_gcd_log_kernel')
OUT.mkdir(parents=True, exist_ok=True)

def primes_upto(n):
    if n < 2:
        return []
    sieve = [True]*(n+1)
    sieve[0]=sieve[1]=False
    for p in range(2,int(n**0.5)+1):
        if sieve[p]:
            step=p
            start=p*p
            sieve[start:n+1:step]=[False]*(((n-start)//step)+1)
    return [i for i in range(2,n+1) if sieve[i]]

def squarefree_minus_eigenvalue(y, kappa=0.5, const=0.0):
    ps = primes_upto(int(y))
    # choose q so q^kappa ~ exp(y), hence log q = y/kappa
    logq = y / kappa
    C = logq + const
    log_prod = 0.0
    correction = 0.0
    for p in ps:
        rho = p**-0.5
        log_prod += math.log1p(-rho)
        correction += rho*math.log(p)/(1-rho)
    lam = math.exp(log_prod)*(C + correction)
    return {
        'y': y,
        'num_primes': len(ps),
        'kappa': kappa,
        'log_q': logq,
        'C_q_model': C,
        'log_product': log_prod,
        'product_minus': math.exp(log_prod),
        'correction_sum': correction,
        'lambda_minus': lam,
        'lambda_over_logq': lam/logq if logq else None,
        'primorial_log': sum(math.log(p) for p in ps),
        'support_condition_margin_log': kappa*logq - sum(math.log(p) for p in ps),
    }

def K_norm_initial(L, kappa=0.5, const=0.0):
    logq = math.log(L)/kappa
    C = logq + const
    K = np.empty((L,L), dtype=float)
    for i,m in enumerate(range(1,L+1)):
        for j,n in enumerate(range(1,L+1)):
            g = math.gcd(m,n)
            K[i,j] = (g/math.sqrt(m*n))*(C - math.log(m*n/(g*g)))
    return K, C, logq

def write_csv(path, rows, fieldnames=None):
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

# Squarefree obstruction table
ys = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 800, 1200, 1800, 2500]
sq_rows = [squarefree_minus_eigenvalue(y, kappa=0.5) for y in ys]
write_csv(OUT/'squarefree_cube_obstruction_step130.csv', sq_rows)

# Initial interval numerical lower-eigenvalue table
interval_rows = []
for kappa in [0.4, 0.5, 0.505, 0.6]:
    for L in [20, 40, 80, 120, 200, 300]:
        K,C,logq = K_norm_initial(L, kappa=kappa)
        eigs = np.linalg.eigvalsh(K)
        interval_rows.append({
            'kappa': kappa,
            'L': L,
            'log_q': logq,
            'C_q_model': C,
            'min_eigenvalue': float(eigs[0]),
            'min_over_logq': float(eigs[0]/logq),
            'min_times_logq': float(eigs[0]*logq),
            'max_eigenvalue': float(eigs[-1]),
            'condition_ratio': float(eigs[-1]/max(eigs[0], 1e-300)),
        })
write_csv(OUT/'initial_interval_lower_eigen_step130.csv', interval_rows)

# Hypercube exact eigenvalues for small y for all sign weights, to illustrate all-minus is small
cube_rows=[]
for y in [10,20,30,40]:
    ps = primes_upto(y)
    logq = y/0.5
    C = logq
    # enumerate up to 2^15 maybe y=50 -> 15 primes 32768 OK
    vals=[]
    for mask in range(1<<len(ps)):
        prod=1.0
        bracket=C
        minus_count=0
        for i,p in enumerate(ps):
            eps = -1 if (mask>>i)&1 else 1
            if eps < 0:
                minus_count += 1
            rho = p**-0.5
            prod *= (1 + eps*rho)
            bracket -= eps*rho*math.log(p)/(1 + eps*rho)
        vals.append(prod*bracket)
    vals=np.array(vals)
    cube_rows.append({
        'y':y,
        'num_primes':len(ps),
        'num_cube_vectors':len(vals),
        'min_eigenvalue':float(vals.min()),
        'median_eigenvalue':float(np.median(vals)),
        'max_eigenvalue':float(vals.max()),
        'all_minus_eigenvalue':squarefree_minus_eigenvalue(y,0.5)['lambda_minus'],
    })
write_csv(OUT/'squarefree_cube_exact_spectrum_step130.csv', cube_rows)

# Gate table
gate_rows = [
    {'gate':'BPRZ arbitrary-coefficient theorem', 'status':'imported platform', 'meaning':'Provides the right twisted second-moment object; not itself a membrane lower-frame certificate.'},
    {'gate':'shifted-limit main kernel', 'status':'audited', 'meaning':'Kernel has GCD-log form after the Step 129 normalization.'},
    {'gate':'full coefficient lower frame', 'status':'fails', 'meaning':'Squarefree Boolean cube gives eigenvalues tending to zero, so no full \u226b log q lower frame.'},
    {'gate':'residual-class restriction', 'status':'open', 'meaning':'Need to show the actual Burnol/Muentz residual coefficient image avoids the near-null GCD-log sector.'},
    {'gate':'additional source component', 'status':'fallback', 'meaning':'If the residual intersects the blind sector, add a non-smuggled source that charges it.'},
    {'gate':'completed tail promotion', 'status':'still required', 'meaning':'Finite lower-frame evidence must be promoted through fixed/exhaustive residual-tail control.'},
]
write_csv(OUT/'gcd_log_gate_table_step130.csv', gate_rows)

# Theorem map
thm_rows = [
    {'item':'Kernel derivative identity', 'statement':'K_tilde = C_q A_{1/2} + d/ds A_s|_{s=1/2}', 'use':'Turns the Step 129 main kernel into a GCD-kernel derivative.'},
    {'item':'Squarefree cube diagonalization', 'statement':'A_s diagonalizes on Boolean sign vectors with eigenvalues prod_p(1+sigma_p p^{-s}).', 'use':'Gives exact eigenvectors for the restricted kernel.'},
    {'item':'All-minus obstruction', 'statement':'lambda_minus = prod_p(1-p^{-1/2})(C_q + sum_p p^{-1/2} log p/(1-p^{-1/2})).', 'use':'Provides explicit Rayleigh quotients tending to zero.'},
    {'item':'Full lower-frame failure', 'statement':'K_tilde not >= c log q I on unrestricted coefficient space.', 'use':'Blocks wholesale import of BPRZ as a source-coercivity theorem.'},
    {'item':'Residual blind-sector definition', 'statement':'Xi_GCD,N = R_N^* Pi_sf R_N.', 'use':'Names the next adequacy residual to audit.'},
]
write_csv(OUT/'theorem_map_step130.csv', thm_rows)

# Route status
route_rows = [
    {'route':'BPRZ full coefficient lower frame', 'status':'blocked', 'reason':'GCD-log main kernel has squarefree near-null directions.'},
    {'route':'BPRZ restricted residual class', 'status':'open', 'reason':'May work if residual coefficients avoid squarefree alternating sector.'},
    {'route':'positive visibility floor + unweighted frame', 'status':'possible', 'reason':'Complete character orthogonality can charge coefficient space if source currency permits.'},
    {'route':'separate source for GCD blind sector', 'status':'fallback', 'reason':'Needed if Xi_GCD is nonzero.'},
]
write_csv(OUT/'route_status_step130.csv', route_rows)

# Nonclaim boundary
with open(OUT/'nonclaim_boundary_step130.md','w') as f:
    f.write('''# Step 130 nonclaim boundary\n\n- This step does not refute Bui--Pratt--Robles--Zaharescu.  Their theorem remains a valid twisted second-moment asymptotic platform.\n- This step does not prove RH or anti-localization.\n- This step does not claim the actual residual coefficient class contains the squarefree blind vectors.  It proves only that the unrestricted coefficient lower-frame import fails.\n- This step does not settle the source route.  It moves the route to a residual-class audit: determine whether `R_N Y_R` intersects the GCD-log near-null sector.\n- The constants in the Step 129 kernel must still be matched to the imported theorem normalization.  The obstruction is insensitive to bounded changes in `C_q`, because the all-minus eigenvalue still tends to zero.\n''')

# Schema
schema = {
    'step': 130,
    'title': 'GCD-log kernel lower-frame audit',
    'active_kernel': 'K_tilde_q(m,n)=gcd(m,n)/sqrt(mn)*(C_q-log(mn/gcd(m,n)^2))',
    'main_verdict': 'unrestricted lower-frame import fails',
    'obstruction': 'squarefree Boolean cube all-minus eigenvector',
    'new_residual': 'Xi_GCD,N = R_N^* Pi_sf R_N',
    'next_step': 'residual coefficient class vs GCD-log blind-sector audit',
    'artifacts': [p.name for p in OUT.iterdir() if p.is_file()]
}
with open(OUT/'step130_schema.json','w') as f:
    json.dump(schema, f, indent=2)

# Plots
plt.figure(figsize=(7,4.5))
plt.plot([r['y'] for r in sq_rows], [r['lambda_minus'] for r in sq_rows], marker='o')
plt.yscale('log')
plt.xlabel('prime cutoff y')
plt.ylabel('all-minus eigenvalue')
plt.title('Squarefree Boolean-cube obstruction')
plt.tight_layout()
plt.savefig(OUT/'squarefree_cube_obstruction_step130.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for kappa in sorted(set(r['kappa'] for r in interval_rows)):
    rows=[r for r in interval_rows if r['kappa']==kappa]
    plt.plot([r['L'] for r in rows], [r['min_eigenvalue'] for r in rows], marker='o', label=f'kappa={kappa}')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('initial interval length L')
plt.ylabel('minimum eigenvalue')
plt.title('Initial-interval GCD-log lower eigenvalue')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'initial_interval_lower_eigen_step130.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
for kappa in sorted(set(r['kappa'] for r in interval_rows)):
    rows=[r for r in interval_rows if r['kappa']==kappa]
    plt.plot([r['L'] for r in rows], [r['min_over_logq'] for r in rows], marker='o', label=f'kappa={kappa}')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('initial interval length L')
plt.ylabel('min eigenvalue / log q')
plt.title('Failure of log-q lower-frame scaling')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'lower_frame_ratio_step130.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot([r['y'] for r in sq_rows], [r['product_minus'] for r in sq_rows], marker='o', label='prod(1-p^-1/2)')
plt.plot([r['y'] for r in sq_rows], [r['lambda_minus']/max(r['C_q_model'],1e-9) for r in sq_rows], marker='s', label='lambda_minus / C_q')
plt.yscale('log')
plt.xlabel('prime cutoff y')
plt.ylabel('log-scale value')
plt.title('Product mechanism behind the blind sector')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'squarefree_product_mechanism_step130.png', dpi=180)
plt.close()

# Zip artifacts
zip_path = OUT/'step130_gcd_log_kernel_artifacts.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir():
        if p.is_file() and p.name != zip_path.name:
            z.write(p, p.name)

print('created', zip_path)
