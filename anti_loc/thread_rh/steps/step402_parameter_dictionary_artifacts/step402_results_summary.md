# Step 402 Results Summary

## Candidate p Formulas

- `p=k+2`, with `k=5`: `p=7`.
- `p=floor(sigma*T)`: `p=3`.
- `p=floor((sigma*T)^2)`: `p=12`.
- `p=floor(ell+1)`: `p=3`.
- `p=ceil(2*pi*lambda)`, with `lambda=1`: `p=7`.

At `(sigma, ell, T)=(0.35,2.0,10)`, all candidates are inside the
near-diagonal window.

## Bergman Phi_max

The leading Bergman half-mass model gives

```text
Phi_Bergman(p)=1/2=0.5
```

for every tested `p`.

Comparison to Step220:

```text
Phi_step220 = 0.49047661902424095
relative error = 1.9416585%
```

## Best Match

All candidates tie under the leading half-mass model.  The value `Phi_max`
alone does not identify the dictionary.

## Verdict

No unique clean dictionary.  The near-diagonal boundary condition points most
naturally to `p ~= (sigma*T)^2`, but the Bergman half-mass comparison is
p-insensitive.  Finite-`p` corrections or the off-diagonal transport identity
are needed to discriminate.

No RH claim is made.
