"""Small algebraic/symbolic sanity checks for Step 79.
These are not RH evidence; they only verify balance identities and toy PSD inequalities.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step79_arch_pole_tail')
OUT.mkdir(parents=True, exist_ok=True)

# Prime-weight toy from previous setup: Λ(n)/sqrt(n)*(1-log n/L)_+^2.
def von_mangoldt(n: int) -> float:
    # Return log p if n is a prime power p^k, else 0.
    m = n
    for p in range(2, int(np.sqrt(n)) + 1):
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p
                k += 1
            if m == 1:
                return float(np.log(p))
            return 0.0
    return float(np.log(n))  # prime

def prime_weights(L: float):
    Nmax = int(np.floor(np.exp(L)))
    vals=[]
    for n in range(2, Nmax+1):
        lam=von_mangoldt(n)
        if lam == 0.0:
            continue
        a=np.log(n)
        alpha=max(0.0,1.0-a/L)**2
        if alpha>0:
            vals.append((n,a,lam/np.sqrt(n)*alpha))
    return vals

# Build toy slots to illustrate required diagonal payment.
Ls = [3,4,5,6,7,8]
summary=[]
for L in Ls:
    w=prime_weights(float(L))
    sw=sum(x[2] for x in w)
    d=2*sw
    # A toy archimedean diagonal contribution: integral kernel over cutoffs, not exact zeta.
    # We just use a declared positive diagonal capacity proxy from the renormalized kernel.
    Amax=8.0
    a=np.linspace(1e-4,Amax,20000)
    kappa=1.0/(2*np.sinh(a/2))
    # Difference kernel positive symbol near zero; integral of min(a^2,1)*kappa is finite.
    arch_diag_proxy=np.trapz(np.minimum(a*a,1.0)*kappa, a)
    # Tail budget proxy decreases with L in this toy.
    tail_proxy=1.0/max(L,1.0)
    required_pole=max(0.0,d - arch_diag_proxy - tail_proxy)
    summary.append({
        'L':L,'num_prime_powers':len(w),'sum_w':sw,'d_prime':d,
        'arch_diag_proxy':arch_diag_proxy,'tail_proxy':tail_proxy,
        'required_pole_diag_proxy':required_pole,
        'status':'toy_balance_only_not_zeta_evidence'
    })
summary_df=pd.DataFrame(summary)
summary_df.to_csv(OUT/'arch_pole_tail_balance_summary_step79.csv', index=False)

# Symbol sanity for positive archimedean difference kernel cutoff.
xi=np.linspace(0,20,800)
Amaxs=[2,4,8,16]
rows=[]
for Amax in Amaxs:
    a=np.linspace(1e-4,Amax,20000)
    kappa=1.0/(2*np.sinh(a/2))
    # symbol Ψ(ξ)=2∫(1-cos(aξ))κ(a)da. Compute for sampled ξ.
    for x in xi:
        psi=2*np.trapz((1-np.cos(a*x))*kappa,a)
        rows.append({'Amax':Amax,'xi':x,'psi':psi})
arch_df=pd.DataFrame(rows)
arch_df.to_csv(OUT/'archimedean_difference_symbol_step79.csv', index=False)

plt.figure(figsize=(7,4.5))
for Amax in Amaxs:
    sub=arch_df[arch_df['Amax']==Amax]
    plt.plot(sub['xi'], sub['psi'], label=f'A={Amax}')
plt.xlabel(r'$\xi$')
plt.ylabel(r'$\Psi_{\infty,A}(\xi)$')
plt.title('Toy archimedean positive difference symbols')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'archimedean_difference_symbol_step79.png', dpi=180)
plt.close()

# Diagonal repair sweep plot.
plt.figure(figsize=(7,4.5))
plt.plot(summary_df['L'], summary_df['d_prime'], marker='o', label='prime diagonal repair')
plt.plot(summary_df['L'], summary_df['arch_diag_proxy']+summary_df['tail_proxy'], marker='s', label='arch+tail toy payment')
plt.plot(summary_df['L'], summary_df['required_pole_diag_proxy'], marker='^', label='remaining pole/completion toy need')
plt.xlabel('L')
plt.ylabel('diagonal budget proxy')
plt.title('Toy completion-balance bookkeeping')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'arch_pole_tail_balance_step79.png', dpi=180)
plt.close()

# Trace not balance countermodel: same trace but not PSD domination.
K=np.diag([2.0,0.25])
Theta=np.eye(2)*1.125
# tr equal? tr(K)=2.25, tr(Theta)=2.25; K not <= Theta.
eig=np.linalg.eigvalsh(Theta-K)
pd.DataFrame([{
    'tr_K':np.trace(K),'tr_Theta':np.trace(Theta),'min_eig_Theta_minus_K':eig[0],
    'loewner_domination': bool(eig[0] >= -1e-12),
    'status':'trace_balance_fails_loewner_balance'
}]).to_csv(OUT/'trace_balance_not_loewner_step79.csv', index=False)

# Structural compile check omitted; no TeX engine assumed.
print('wrote step79 artifacts to', OUT)
