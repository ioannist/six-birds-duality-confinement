import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step83_paired_weil')

# Toy prime weights as in earlier steps: von Mangoldt for n up to exp(L) with smooth cutoff.
def von_mangoldt(n: int) -> float:
    # Return log p if n is a prime power p^k, else 0.
    x = n
    for p in range(2, int(np.sqrt(n)) + 1):
        if x % p == 0:
            k = 0
            while x % p == 0:
                x //= p
                k += 1
            if x == 1:
                return np.log(p)
            return 0.0
    # n itself prime
    return np.log(n)

L = 8.0
N = int(np.floor(np.exp(L)))
# keep only moderate n for speed but cutoff already exp(8)=2980, OK.
records = []
for n in range(2, N + 1):
    lam = von_mangoldt(n)
    if lam == 0:
        continue
    a = np.log(n)
    alpha = max(0.0, 1 - a / L)**2
    w = lam / np.sqrt(n) * alpha
    if w > 0:
        records.append((n, a, w))

arr = np.array(records, dtype=float)
if arr.size == 0:
    raise RuntimeError('no weights')
a_vals = arr[:,1]
w_vals = arr[:,2]

d_pr = 2 * w_vals.sum()

xi = np.linspace(0, 40, 2000)
prime_signed = -2 * np.sum(w_vals[:,None] * np.cos(a_vals[:,None] * xi[None,:]), axis=0)
prime_paired = 2 * np.sum(w_vals[:,None] * (1 - np.cos(a_vals[:,None] * xi[None,:])), axis=0)

# Gamma paired symbol via numerical quadrature with a small t grid; no SciPy.
t = np.concatenate([
    np.geomspace(1e-5, 1, 1200),
    np.linspace(1.001, 50, 2500)
])
kappa = 0.5 * np.exp(-t/4) / (1 - np.exp(-t))
# integrate for selected xi values only to keep memory low
gamma_symbol = []
for x in xi[::10]:
    vals = kappa * (1 - np.cos(x * t / 2))
    gamma_symbol.append(np.trapz(vals, t))
gamma_symbol = np.array(gamma_symbol)
xi_gamma = xi[::10]

# Paired test: Gaussian Fourier profile, compare gamma paired integral as cutoff epsilon shrinks
# q = ∫ Psi_gamma(xi)|fhat|² dxi. Separated diagonal integral diverges.
fh2 = np.exp(-xi_gamma**2 / 8)
paired_gamma_q = np.trapz(gamma_symbol * fh2, xi_gamma)

eps_vals = np.geomspace(1e-5, 1e-1, 80)
diag_trunc = []
paired_trunc = []
for eps in eps_vals:
    tt = t[t >= eps]
    kk = 0.5 * np.exp(-tt/4) / (1 - np.exp(-tt))
    diag_trunc.append(np.trapz(kk, tt))
    # compute paired q for Gaussian f via symbol with truncated kernel on coarse xi
    gs = []
    for x in xi_gamma:
        gs.append(np.trapz(kk * (1 - np.cos(x * tt / 2)), tt))
    gs = np.array(gs)
    paired_trunc.append(np.trapz(gs * fh2, xi_gamma))

diag_trunc = np.array(diag_trunc)
paired_trunc = np.array(paired_trunc)

# Save CSVs
pd.DataFrame({
    'xi': xi,
    'prime_signed_symbol': prime_signed,
    'prime_paired_symbol': prime_paired,
    'diagonal_repair_d_pr': d_pr
}).to_csv(OUT / 'paired_prime_symbol_step83.csv', index=False)

pd.DataFrame({
    'xi': xi_gamma,
    'gamma_paired_symbol': gamma_symbol,
    'gaussian_weight': fh2
}).to_csv(OUT / 'gamma_paired_symbol_step83.csv', index=False)

pd.DataFrame({
    'epsilon_cutoff': eps_vals,
    'separated_gamma_diagonal_truncated': diag_trunc,
    'paired_gamma_q_gaussian': paired_trunc
}).to_csv(OUT / 'paired_vs_separated_gamma_step83.csv', index=False)

pd.DataFrame({
    'L': [L],
    'num_prime_power_weights': [len(w_vals)],
    'sum_weights': [w_vals.sum()],
    'd_pr': [d_pr],
    'min_prime_signed': [prime_signed.min()],
    'min_prime_paired': [prime_paired.min()],
    'paired_gamma_q_gaussian_reference': [paired_gamma_q],
    'diag_trunc_min_epsilon': [diag_trunc[0]],
    'paired_trunc_min_epsilon': [paired_trunc[0]]
}).to_csv(OUT / 'paired_weil_summary_step83.csv', index=False)

# plots
plt.figure(figsize=(7,4))
plt.plot(xi, prime_signed, label='signed prime symbol')
plt.plot(xi, prime_paired, label='paired positive prime symbol')
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Prime signed symbol vs paired positive feature')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'paired_prime_symbol_step83.png', dpi=160)
plt.close()

plt.figure(figsize=(7,4))
plt.plot(xi_gamma, gamma_symbol, label='gamma paired symbol')
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Positive paired gamma/archimedean symbol')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'gamma_paired_symbol_step83.png', dpi=160)
plt.close()

plt.figure(figsize=(7,4))
plt.loglog(eps_vals, diag_trunc, label='separated diagonal (truncated)')
plt.loglog(eps_vals, paired_trunc, label='paired q on Gaussian')
plt.gca().invert_xaxis()
plt.xlabel('near-zero cutoff epsilon')
plt.ylabel('value')
plt.title('Gamma: separated diagonal diverges, paired form stabilizes')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'paired_vs_separated_gamma_step83.png', dpi=160)
plt.close()

print('done')
