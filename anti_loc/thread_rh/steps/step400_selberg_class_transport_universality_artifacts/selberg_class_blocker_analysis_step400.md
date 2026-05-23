# Step 400: Selberg-Class Transport Blocker Universality

## Inputs Used

- Step 372 used verbatim in substance: the punctured-disc cusp kernel is
  `B_p^{D*}(z) = (log|z|^2)^p/(2*pi*(p-2)!)*sum_{ell>=1}(p-1)/ell!*(-ell*log|z|^2)^{ell-1}`.
- Step 385 used verbatim in substance: Branch C theorem-grade closure stalls at the projected `P_infty` spectral asymptotic.
- Step 389 used verbatim in substance: the close-pair sign-flip mechanism is universal across zeta and `L(s,chi_3)`.
- Step 390 used verbatim: `delta_Dk^L=(L(s,chi_3) M(G_star)(s))^(k)(rho)` and `both_versions_fail_structural_law_not_supported_for_raw_linear_fit`.
- Step 391 used verbatim: best `L(s,chi_3)` structural form is `C4`, `a*T^c+b`, with `a=-0.003251402830227687`, `b=-1.1417869170337844`, `c=1.260178559814773`.
- Step 399 used verbatim in substance: blocker is the off-diagonal log-cusp Bergman large-`p` asymptotic plus `p <-> lambda,sigma,ell,T` scaling proving convergence to the PSWF/sinc kernel.

## T1: Branch-C Analog for L(s, chi_3)

For zeta the cascade uses

```text
L_{rho,k}(G) = < M_zeta G, P_infty y_{rho,k} >.
```

For the primitive character `chi_3 mod 3`, the analogous raw construction is

```text
L^chi_{rho,k}(G) = < M_{L(s,chi_3)} G_chi, P_infty^chi y^chi_{rho,k} >,
```

where `P_infty^chi` is the Sonine/Burnol projection adapted to the completed
Dirichlet L-function with conductor `q=3` and its gamma/parity data.

The raw proxy tested in Step390 was

```text
delta_Dk^L = (L(s,chi_3) M(G_star)(s))^(k)(rho).
```

This is not the fully projected `P_infty^chi` quantity, but it identifies the
correct Branch-C-analog input side.

## T2: Closure Path

The closure path for `L(s,chi_3)` needs the same type of missing statement as
zeta:

```text
off-diagonal cusp Bergman kernel
  -> log-cusp transport
  -> PSWF/sinc two-cutoff Sonine projection
  -> projected matrix-element asymptotic.
```

The difference is not the local punctured-disc model.  The difference is the
parameter dictionary:

```text
zeta:      level 1, trivial character, q=1, width at infinity 1.
chi_3:    level 3 / nebentypus, q=3, width at infinity still 1 for Gamma_0(3),
          but conductor/parity data modifies the completed L-function and
          the target spectral data.
```

## T3: Cusp Kernel at Gamma_0(3)

At the cusp at infinity, `Gamma_0(3)` contains the translation

```text
w -> w+1.
```

Thus the local punctured-disc coordinate can still be taken as

```text
z = exp(2*pi*i*w),
```

with the same local Poincare cusp metric and the same Auvray-Ma-Marinescu
punctured-disc model kernel.  Level and character affect global sections,
automorphy factors, and conductor-dependent normalization, but the local cusp
singularity type is unchanged.

## Transport Comparison

The core transport blocker is therefore shared:

```text
K_p^{D*}(z,z') in log-cusp coordinates
  ?--> delta(tau-tau') - sinc_lambda(tau-tau')
       - sum_n Psi_n^lambda(tau) conjugate(Psi_n^lambda(tau')).
```

For `chi_3`, the same identity would be used, but with a different dictionary
for `(p,lambda,sigma,ell,T)` because the completed `L(s,chi_3)` has conductor
`q=3` and parity data.  This explains why Step391 can find a different raw
power-law structural form without implying a different transport-identity
blocker.

## Verdict

The blocker is Selberg-class local/universal at the cusp-projector level:
resolving the off-diagonal Bergman-to-PSWF/sinc transport identity would remove
the same theorem-grade obstruction for zeta and for the `L(s,chi_3)` analog.

However, it would not automatically identify the `chi_3` structural law without
the conductor/parity scaling dictionary for `P_infty^chi`.  The shared blocker
is the transport identity; the `chi_3`-specific remaining layer is the parameter
normalization.
