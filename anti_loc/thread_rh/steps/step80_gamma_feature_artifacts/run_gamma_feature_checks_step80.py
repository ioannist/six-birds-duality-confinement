import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import digamma
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step80_gamma_feature')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Verify digamma integral formula for zeta gamma symbol.
# Psi_inf(xi)=Re psi(1/4+i xi/2)-psi(1/4)= integral_0^inf e^{-t/4}/(1-e^{-t})(1-cos(xi t/2))dt

def psi_symbol(xi):
    return float(np.real(digamma(0.25 + 0.5j*xi) - digamma(0.25)))

def int_symbol(xi):
    f = lambda t: np.exp(-0.25*t)/(1-np.exp(-t))*(1-np.cos(0.5*xi*t)) if t != 0 else 0.0
    # split to handle zero and tail
    val1, err1 = quad(f, 0, 1, limit=200, epsabs=1e-10, epsrel=1e-10)
    val2, err2 = quad(f, 1, 80, limit=200, epsabs=1e-10, epsrel=1e-10)
    # tail is exponentially small by t=80
    return val1+val2, err1+err2

xis = np.concatenate([np.linspace(0,2,11), np.linspace(3,20,10)])
rows=[]
for xi in xis:
    ps=psi_symbol(xi)
    integ, err=int_symbol(xi)
    rows.append(dict(xi=xi, digamma_symbol=ps, integral_symbol=integ, abs_error=abs(ps-integ), quad_error_est=err))
pd.DataFrame(rows).to_csv(OUT/'gamma_digamma_integral_check_step80.csv', index=False)

# 2. Kernel behavior and truncated diagonal divergence
cutoffs = np.logspace(-5,-1,20)
# truncated diagonal integral: int_eps^infty kappa(t) dt with kappa=0.5 e^{-t/4}/(1-e^{-t})
def kappa(t):
    return 0.5*np.exp(-0.25*t)/(1-np.exp(-t))
def trunc_diag(eps):
    val, err = quad(lambda t: kappa(t), eps, 80, limit=200)
    return val
krows=[]
for eps in cutoffs:
    krows.append(dict(eps=eps, truncated_diagonal=trunc_diag(eps), log_inv_eps=np.log(1/eps)))
pd.DataFrame(krows).to_csv(OUT/'gamma_kernel_truncated_diagonal_step80.csv', index=False)

# 3. Symbol positivity and growth
xis2 = np.linspace(0,50,501)
sym = np.array([psi_symbol(x) for x in xis2])
pd.DataFrame({'xi':xis2,'gamma_symbol':sym}).to_csv(OUT/'gamma_symbol_profile_step80.csv', index=False)

# 4. Toy completion balance with gamma matched: illustrate residual accounting.
# We take d_pr increasing, c_inf values, residual negative budget and pole payment.
dpr = 9.0856035154  # from step 77 toy L=6
cvals = np.linspace(-15, 5, 101)
# If c_inf is negative, gamma contributes negative diagonal after matching; pole must pay max(0,-(dpr+c_inf)).
bal=[]
for c in cvals:
    needed_pole = max(0.0, -(dpr+c))
    bal.append(dict(c_infty=c, d_pr=dpr, residual_diagonal=dpr+c, minimum_pole_payment=needed_pole))
pd.DataFrame(bal).to_csv(OUT/'gamma_completion_constant_balance_step80.csv', index=False)

# plots
plt.figure(figsize=(6,4))
plt.plot([r['xi'] for r in rows], [r['digamma_symbol'] for r in rows], 'o-', label='digamma')
plt.plot([r['xi'] for r in rows], [r['integral_symbol'] for r in rows], 'x--', label='integral')
plt.xlabel(r'$\xi$')
plt.ylabel(r'$\Psi_\infty(\xi)$')
plt.title('Gamma symbol: digamma vs integral')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'gamma_digamma_integral_check_step80.png', dpi=160)
plt.close()

plt.figure(figsize=(6,4))
plt.plot([r['log_inv_eps'] for r in krows], [r['truncated_diagonal'] for r in krows], 'o-')
plt.xlabel(r'$\log(1/\epsilon)$')
plt.ylabel('truncated diagonal')
plt.title('Gamma kernel separated diagonal diverges logarithmically')
plt.tight_layout()
plt.savefig(OUT/'gamma_truncated_diagonal_step80.png', dpi=160)
plt.close()

plt.figure(figsize=(6,4))
plt.plot(xis2, sym)
plt.xlabel(r'$\xi$')
plt.ylabel(r'$\Psi_\infty(\xi)$')
plt.title('Positive gamma/archimedean symbol')
plt.tight_layout()
plt.savefig(OUT/'gamma_symbol_profile_step80.png', dpi=160)
plt.close()

plt.figure(figsize=(6,4))
plt.plot(cvals, [max(0.0, -(dpr+c)) for c in cvals])
plt.axvline(-dpr, linestyle='--')
plt.xlabel(r'$c_\infty$')
plt.ylabel('minimum pole/completion payment')
plt.title('Toy completion balance after gamma matching')
plt.tight_layout()
plt.savefig(OUT/'gamma_completion_constant_balance_step80.png', dpi=160)
plt.close()

print('wrote step80 checks')
