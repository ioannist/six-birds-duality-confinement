# Step 401: Near-Diagonal Bergman Sufficiency Test

## Inputs Used

- Step 196 wavepacket scale used verbatim in substance:
  `u_T(x)=T^{1/4}*G(sigma*T*log(x))`.
- Step 220 Branch A result used verbatim:
  `Phi_max = 0.49047661902424095` at `(sigma, ell)=(0.35, 2.0)`.
- Step 372 cusp coordinate used verbatim:
  `z=exp(2*pi*i*w)`, `|z|^2=exp(-4*pi*T)`.
- Step 399 blocker used verbatim in substance:
  need off-diagonal `K_p^{D*}(z,z')` in log-cusp coordinates converging to
  the Step173 PSWF/sinc kernel.
- Step 400 classification used verbatim in substance:
  the transport blocker is local/Selberg-class shared.

## Scale Test

The wavepacket relative displacement in cusp coordinates is

```text
delta z / z ~= 2*pi*delta w,
```

and after dropping the harmless fixed `2*pi` convention factor the controlling
dimensionless packet width is

```text
width ~= 1/(sigma*T).
```

Published near-diagonal Bergman asymptotics apply in windows of the form

```text
d(z,z') <= 1/sqrt(p)
```

or in logarithmic refinements

```text
d(z,z') <= sqrt(log(p)/p).
```

For the Step220 maximizer `sigma=0.35`, the standard near-diagonal condition is

```text
1/(sigma*T) <= 1/sqrt(p)
```

equivalently

```text
p <= (sigma*T)^2.
```

## Results

At low height `T=14.1347`, `(sigma*T)^2 = 24.47`.
So the packet is inside the standard `1/sqrt(p)` regime for `p<=20`, just
outside for `p=30`, and still inside the weaker `sqrt(log(p)/p)` regime through
`p=100`.

At `T=100`, `(sigma*T)^2=1225`, so `p<=1000` is inside the standard regime.

At the Step220 essential-norm scale `T=10000`, `(sigma*T)^2=12,250,000`, so
`p=30`, `p=1000`, and even `p=1,000,000` are inside the standard regime.

## Partial Closure Attempt

For Branch A specifically, Step220's `Phi_max` is a large-`T` wavepacket
quantity.  If the Bergman tensor power `p` corresponding to the cascade model
is bounded or grows more slowly than `(sigma*T)^2`, the known near-diagonal
Bergman asymptotic is sufficient for the wavepacket action.  In that regime the
full off-diagonal Step399 blocker is not needed for Branch A's large-`T`
wavepacket family.

However, the inherited records still do not provide the dictionary

```text
p <-> (lambda, sigma, ell, T)
```

needed to certify that the Step220 `P_infty` computation lies in that
near-diagonal Bergman regime.

## Verdict

Marginal-to-conditionally-sufficient.

For the actual Step220 large-`T` regime, the packet width is far inside the
near-diagonal window for all plausible finite `p` comparable to the cascade's
`k<=30` scales.  At low `T=14`, the test is marginal: `p=30` is outside
`1/sqrt(p)` but inside `sqrt(log(p)/p)`.

Therefore Branch A may be theorem-grade closable using published near-diagonal
Bergman asymptotics, but only after the missing `p`-to-PSWF parameter dictionary
is supplied.  Branch C still needs the broader off-diagonal/transition regime.
