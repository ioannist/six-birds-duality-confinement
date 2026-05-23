# Step 403 Results Summary

## Formula Tested

The inherited Step403 formula was evaluated literally:

```text
B_p^{D*}(z)
 = x^p/(2*pi*(p-2)!) *
   sum_{ell>=1} (p-1)/ell! * (x*ell)^(ell-1),
```

where

```text
x = -log|z|^2 = 4*pi*T = 40*pi = 125.66370614359172
```

for `T=10`.

## Divergence Diagnostic

For the summand

```text
a_ell = (p-1)/ell! * (x*ell)^(ell-1),
```

the term ratio is

```text
a_{ell+1}/a_ell = x * (1 + 1/ell)^(ell-1) -> e*x.
```

At `x=40*pi`, this limit is

```text
e*40*pi = 341.521075369989...
```

so the series diverges rapidly for every tested `p`.

## Computed Evidence

Using mpmath precision above 50 dps:

- `p=3`: partial `ell<=5` already gives `log10(B_p) = 14.9158`; terms keep growing.
- `p=7`: partial `ell<=5` gives `log10(B_p) = 21.7106`; terms keep growing.
- `p=12`: partial `ell<=5` gives `log10(B_p) = 27.9893`; terms keep growing.

## Phi_max Prediction

The requested normalization

```text
Phi_B(p,T) ~= B_p^{D*}(z,T) * 2*pi / p^(3/2)
```

is undefined under the literal inherited series because `B_p^{D*}` is not
finite.

## Verdict

No finite-p sub-leading Bergman correction was obtained.  The literal inherited
formula cannot discriminate `p=3,7,12`, because the series diverges at
`T=10`.  A finite correction requires the fully normalized/off-diagonal
punctured-disc kernel expression, including the missing decay factor or
equivalent monomial coefficient normalization.  The Step399 off-diagonal
transport blocker remains load-bearing.

No RH claim is made.
