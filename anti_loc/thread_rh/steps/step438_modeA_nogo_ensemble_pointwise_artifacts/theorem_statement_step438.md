# Step 438 Theorem Statement

## Universality statement

Let `E_N` be a generalized Wigner ensemble of Hermitian `N x N` matrices satisfying the standard normalization and moment hypotheses. Let `rho_k^(N)` be the normalized `k`-point correlation measure of bulk eigenvalues near a fixed bulk energy.

Erdős-Schlein-Yau / Tao-Vu universality has the form:

```text
int f(x_1,...,x_k) d rho_k^(N)(x_1,...,x_k)
  ->
int f(x_1,...,x_k) det[K(x_i,x_j)]_{i,j=1}^k dx_1...dx_k
```

for compactly supported continuous test functions `f`, where

```text
K(x,y) = sin(pi(x-y))/(pi(x-y)).
```

This is convergence of measures / correlation functions, in the vague or averaged-vague sense. It is not pointwise convergence of eigenvalue sequences.

## No-go theorem

**Theorem (Mode A no-go, Dispatch 2).** A random-matrix universality theorem that identifies the limiting local `k`-point correlation functions of eigenvalues with the sine-kernel/GUE limit cannot, by itself, imply a Hilbert-Polya pointwise identity

```text
Spec(H) = { gamma_n : zeta(1/2 + i gamma_n) = 0 }.
```

It can only constrain distributional local statistics. Therefore any construction that uses GUE universality alone to argue for `Spec(H)={gamma_n}` fails unless it supplies an independent deterministic pointwise mechanism. If that mechanism selects the zeta-zero realization by conditioning or by inserting zeta-zero data, it violates no-tautology / no-smuggling constraints.

## Consequence for Route 2

`C_ensemble_distributional_not_pointwise` is theorem-grade: ensemble universality is compatible with Montgomery-Odlyzko statistics but structurally insufficient for Hilbert-Polya pointwise spectral realization.
