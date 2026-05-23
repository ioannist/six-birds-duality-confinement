# Step 429 Functional Equation Phase

For a primitive Dirichlet character chi, write the completed function as

```text
Lambda(s,chi) = F_chi(s) L(s,chi),
F_chi(s) = (q/pi)^((s+a)/2) Gamma((s+a)/2).
```

For a self-dual real primitive character, the functional equation has scalar form

```text
Lambda(s,chi) = epsilon_chi Lambda(1-s,chi),  epsilon_chi in {+1,-1}.
```

On the critical line `s = 1/2 + it`, this gives a Hardy-type real function after multiplication by a unit phase. At a simple critical-line zero `rho = 1/2+iT`, differentiating along the line gives

```text
d/dt Lambda(1/2+it,chi)|_T = i Lambda'(rho,chi).
```

Since the Hardy-normalized completed function is real on the line, `i Lambda'(rho,chi)` lies on a fixed real line. At a zero,

```text
Lambda'(rho,chi) = F_chi(rho) L'(rho,chi),
```

so the functional equation imposes the phase-line constraint

```text
Arg L'(rho,chi) = -Arg(i F_chi(rho))  (mod pi)
```

for self-dual real characters. For zeta, with

```text
F_zeta(s) = (1/2) s(s-1) pi^(-s/2) Gamma(s/2),
```

the same formula becomes

```text
Arg zeta'(rho) = -Arg(i F_zeta(rho)) (mod pi).
```

This is a genuine phase constraint, but only modulo `pi`: it fixes a line, not the orientation on that line. The missing orientation is the sign of the derivative of the real Hardy function at the zero.

For non-real characters, the scalar real-line reduction is replaced by the coupled functional equation between `chi` and `conj(chi)`. A one-function phase line is not obtained without passing to a two-component self-dual combination.

## Verbatim Step Anchors

- Step 381: `zeta''(rho_j) = 2*zeta'(rho_j)*g_j'(rho_j)`.
- Step 411: `For L(s, chi_3): same identity should hold with L replacing zeta.`
- Step 422: `Re L''(rho) >= 0 iff B(rho) > 0 AND |B(rho)| > |A(rho)|`.
- Step 427: `B>0, A>0, |A|>|B|` identifies the regular-residual-driven mechanism.
- Step 428: `empirical verification 410/410 = 100% across 9 L-functions through n=2000 zeta`.
