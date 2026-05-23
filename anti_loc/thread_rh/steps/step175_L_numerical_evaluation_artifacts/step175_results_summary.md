# Step 175: Numerical Evaluation of `L_{rho_1,0}(G_*)`

Verdict:

`L_verdict = V_L_numerical_nonzero`.

Using the Step 174 formula

```tex
L_{rho_1,0}(G_*) = - I_sinc - sum_{n>=0} Psi_n(rho_1) J_n,
```

with `rho_1 = 1/2 + 14.134725141734693 i`, `lambda = 1`, `U = 200`,
grid spacing `h = 0.05`, and `mpmath` zeta precision `50` decimal digits,
the computed value using the required `n = 0,1,2` PSWF block is

```tex
L_{rho_1,0}^{[0,2]}(G_*)
  = 0.12146653476134234 - 0.08985731971133760 i
```

with total error radius

```tex
1.9648066412630187e-4.
```

Thus

```tex
|L_{rho_1,0}(G_*)| >= 0.1508944091096583
```

under the Step 173/174 normalization and numerical tail bound.  This is
well-separated from zero.

Key components:

- `I_sinc = -0.11261872344887212 + 0.08976645970797142 i`
- `sum_{n=0}^2 Psi_n(rho_1)J_n = -0.008847811312470217 + 0.00009086000336618477 i`
- PSWF tail bound for `n >= 3`: `1.0e-6`
- Diagnostic extended sum through `n = 11` gives
  `0.12146654891766735 - 0.08985771052931701 i`, consistent with the
  three-term value inside the error radius.

Branch C implication: this is numerical obstruction evidence for the full
ZI-COV(i) extension on the selected nontrivial legal generator.  It does not
prove a global theorem and does not remove retained no-gos.
