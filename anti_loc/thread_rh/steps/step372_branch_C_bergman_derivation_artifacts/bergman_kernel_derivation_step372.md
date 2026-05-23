# Step 372 Bergman Kernel Derivation Attempt

## Inherited Auvray-Ma-Marinescu input

The inherited punctured-disc model uses the cusp Poincare metric

`omega_{D*}=i dz wedge dbar(z) / (|z|^2 log^2(|z|^2))`

and the model Bergman kernel formula

`B_p^{D*}(z) = [log|z|^2]^p/[2*pi*(p-2)!] * sum_{ell>=1} (p-1)/ell! * (-ell*log|z|^2)^{ell-1}`.

With the cusp coordinate

`z=exp(2*pi*i*w)`, `T=Im(w)`,

we have

`|z|^2=exp(-4*pi*T)` and `log|z|^2=-4*pi*T`.

Therefore the literal inherited formula gives the magnitude-level expression

`B_p^{D*}(T) = (4*pi*T)^p/[2*pi*(p-2)!] * sum_{ell>=1} (p-1)/ell! * (4*pi*T*ell)^{ell-1}`,

up to the sign convention from `[log|z|^2]^p`.

## Literal saddle analysis

Let `R=4*pi*T`.  The summand exponent is

`f(ell)=(ell-1) log(R*ell) - log(ell!)`.

Using Stirling,

`log(ell!)=ell log ell - ell + (1/2)log(2*pi*ell)+...`

so

`f(ell)=ell log R + ell - log R - log ell - (1/2)log(2*pi*ell)+...`.

Thus

`f'(ell)=log R + 1 - 3/(2*ell)+...`.

At zeta-zero cusp heights, `R=4*pi*T` is large, so `log R + 1 > 0`.
There is no finite maximum.  The literal series grows like

`(e*R)^ell / ell^(3/2)`

and diverges.  Hence the inherited formula, used exactly as written, cannot
produce a theorem-grade Branch C saddle at Riemann-zero heights.

## Corrected standard punctured-disc check

The standard local punctured-disc Bergman expression derived from monomial
norms has the decaying factor

`sum_{ell>=1} ell^{p-1} exp(-R*ell)`.

For this corrected local model, the saddle is

`ell_*=(p-1)/R=(p-1)/(4*pi*T)`.

Substituting this saddle into

`R^p/(p-2)! * ell^{p-1} exp(-R ell)`

shows that the exponential `p`-terms cancel after Stirling.  The result is the
usual local Bergman growth scale rather than an exponential decay coefficient:
there is no `gamma(T)=pi/(T log(T/(2*pi)))` term.

The local cusp scale present in this model is `1/(4*pi*T)`, which has a `1/T`
shape but lacks the Riemann-von-Mangoldt density factor `log(T/(2*pi))`.

## Branch C projector mismatch

Auvray-Ma-Marinescu gives an `L^p` Bergman kernel for sections on a punctured
Riemann surface.  Branch C needs the large-`k` asymptotic of the projected
Burnol/Sonine pulled evaluator

`P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho)`.

The inherited records do not identify this `P_infty` projector with the AMM
`L^p` Bergman projection, nor do they justify setting `p=k` in the Branch C
zero-evaluator derivative problem.  This mismatch blocks theorem-grade
transfer of the AMM saddle into the Branch C gamma law.
