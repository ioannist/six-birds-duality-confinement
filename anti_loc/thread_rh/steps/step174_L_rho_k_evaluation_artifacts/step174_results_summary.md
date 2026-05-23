# Step 174: L_{rho,k} Evaluation Attempt

Verdict:

`L_verdict = V_L_symbolic_form`.

Concrete choices:

- `rho_1 = 1/2 + 14.134725141734693 i`
- `k = 0`
- `lambda = 1`
- PSWF leading block displayed: `n = 0, 1, 2`
- `G_* = ghat_*` from a nonzero legal Burnol generator on `[1,4]`

The generator is built from three disjoint smooth compact bumps

```tex
b_j(t)=beta((t-c_j)/epsilon),
epsilon=1/5,
c_1=3/2, c_2=5/2, c_3=7/2,
```

where `beta(u)=exp(-1/(1-u^2))` for `|u|<1` and `0` otherwise.  Coefficients
are chosen so that

```tex
int g_*(t) dt = 0,
int g_*(t)t^{-1} dt = 0,
```

hence `G_*(0)=G_*(1)=0`, satisfying Step119 legality.

The result is:

```tex
L_{rho_1,0}(G_*)
= - int_R sinc(gamma_1-u) zeta(1/2+iu)G_*(1/2+iu) du
  - sum_{n>=0} Psi_n(rho_1)
      int_R zeta(1/2+iu)G_*(1/2+iu)conj(Psi_n(1/2+iu)) du.
```

Here `sinc(gamma_1-u)=sin(gamma_1-u)/(pi(gamma_1-u))`, and
`Psi_n = U_infty((I-P_1)phi_n^1/sqrt(1-mu_n^1))` from Step173.

The delta term vanishes because `zeta(rho_1)=0`.  The formula is not evaluated
to a zero/nonzero scalar in this step.  Branch C status is partial: the
terminal matrix element is now an explicit PSWF/sinc integral expression for a
nontrivial legal generator.
