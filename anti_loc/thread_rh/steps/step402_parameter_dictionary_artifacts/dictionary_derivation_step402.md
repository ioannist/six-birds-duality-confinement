# Step 402: p <-> (lambda, sigma, ell, T) Parameter Dictionary Attempt

## Inputs Used

- Step 196 wavepacket scale used verbatim in substance:
  `u_T(x)=T^{1/4}*G(sigma*T*log(x))`.
- Step 220 value used verbatim:
  `Phi_max = 0.49047661902424095` at `(sigma, ell)=(0.35, 2.0)`.
- Step 372 Bergman input used verbatim:
  `B_p^{D*}` is the tensor-power `L^p` punctured-disc Bergman kernel, valid for
  `p>=2`, with `sup B_p ~ p^{3/2}/(2*pi)`.
- Step 398 used verbatim in substance:
  Branch A Bergman half-mass candidate `Phi_max=1/2`, relative error `1.94%`.
- Step 399/400 used verbatim in substance:
  the common blocker is the missing off-diagonal Bergman-to-PSWF/sinc transport
  identity and parameter dictionary.
- Step 401 used verbatim in substance:
  near-diagonal sufficiency holds for Branch A large `T` if `p <= (sigma*T)^2`.

## Candidate Dictionary Forms

At the requested test point

```text
sigma = 0.35, ell = 2.0, T = 10.
```

the packet width is

```text
1/(sigma*T) = 0.2857142857.
```

Candidates:

1. `p=k+2`, using `k=5`, gives `p=7`.
2. `p=floor(sigma*T)` gives `p=3`.
3. `p=floor((sigma*T)^2)` gives `p=12`.
4. `p=floor(ell+1)` gives `p=3`.
5. `p=ceil(2*pi*lambda)` with Step215/220 `lambda=1` gives `p=7`.

All candidates lie inside the Step401 near-diagonal scale at `T=10`.  The
boundary-matched candidate `p=floor((sigma*T)^2)=12` is closest to the
standard `1/sqrt(p)` threshold but still inside it.

## Bergman Phi Test

The leading near-diagonal Bergman half-mass model gives

```text
Phi_Bergman(p) = 1/2
```

for all listed `p`.  Therefore every candidate matches Step220's
`0.49047661902424095` with the same relative error:

```text
1.9416585%.
```

This is a marginal 1--5% match, but it does not identify a unique dictionary.
The leading half-mass model is too coarse to discriminate among `p=3`, `p=7`,
and `p=12`.

## Verdict

No clean parameter dictionary is identified by the Phi_max value alone.

The strongest structural direction is:

```text
p ~= (sigma*T)^2
```

because it is the only candidate derived directly from the Step401
near-diagonal boundary condition.  But the empirical `Phi_max` comparison does
not prefer it over `p=k+2` or `p=ceil(2*pi*lambda)`.

Further progress requires finite-`p` correction terms or an off-diagonal
transport calculation that changes the `1/2` half-mass into a p-sensitive
quantity.
