# Step 372 Saddle Solution

## Literal inherited AMM formula

After `z=exp(2*pi*i*w)` and `T=Im(w)`, set

`R=4*pi*T`.

The literal summand in the inherited formula is

`a_ell = (p-1)/ell! * (R*ell)^(ell-1)`.

Ignoring constants independent of `ell`,

`f(ell)=log a_ell=(ell-1)log(R*ell)-log(ell!)`.

Stirling gives

`f(ell)=ell log R + ell - log R - (3/2)log ell - (1/2)log(2*pi)+O(1/ell)`.

Hence

`f'(ell)=log R + 1 - 3/(2ell)+O(ell^-2)`.

At all Riemann-zero heights in the Step 324 dataset, `R=4*pi*T>>1`, so the
stationary equation has no positive large-ell maximum.  The formal root

`ell approx 3/(2*(1+log R))`

lies below the large-ell regime and is not a dominant saddle.  The tail grows
because `exp(f(ell)) ~ (eR)^ell/ell^(3/2)`.

Conclusion: the literal formula has no usable dominant `ell_*` for this
substitution.

## Corrected local punctured-disc model

For the standard monomial-norm expression,

`B_p^{D*}(R) = R^p/[2*pi*(p-2)!] * sum_{ell>=1} ell^(p-1) exp(-R ell)`.

The exponent is

`g(ell)=(p-1)log ell - R ell`.

The saddle is exact at leading order:

`g'(ell)=(p-1)/ell - R = 0`,

so

`ell_*=(p-1)/R=(p-1)/(4*pi*T)`.

At the saddle,

`g(ell_*)=(p-1)[log(p-1)-log R-1]`.

Combining with `p log R - log((p-2)!)` cancels the exponential `p`-action.
The remaining local growth is polynomial in `p`, consistent with the AMM
`p^{3/2}` sup scale.

Thus the corrected Bergman saddle does not yield a Branch C decay coefficient
`gamma(T)`.  It yields a local cusp scale `ell_*/p=1/(4*pi*T)`.
