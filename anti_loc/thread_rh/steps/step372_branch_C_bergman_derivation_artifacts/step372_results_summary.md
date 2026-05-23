# Step 372 Results Summary

Cusp substitution:

`z=exp(2*pi*i*w)`, `T=Im(w)`, `|z|^2=exp(-4*pi*T)`, and
`-log|z|^2=4*pi*T`.

Using the inherited Auvray-Ma-Marinescu formula exactly gives

`B_p^{D*}(T)=(4*pi*T)^p/[2*pi*(p-2)!] * sum_{ell>=1} (p-1)/ell! * (4*pi*T*ell)^(ell-1)`.

The literal summand has exponent

`f(ell)=(ell-1)log(4*pi*T*ell)-log(ell!)`,

with derivative

`f'(ell)=log(4*pi*T)+1-3/(2ell)+...`.

Since `4*pi*T` is large for all Riemann-zero heights tested, the literal series
has no finite dominant saddle and diverges termwise.  This blocks a theorem
derivation from the formula as stated.

For comparison, the standard corrected punctured-disc kernel with the expected
decay factor has saddle

`ell_*=(p-1)/(4*pi*T)`.

After Stirling, the exponential `p`-action cancels against `(p-2)!`; the local
kernel gives a `1/(4*pi*T)` cusp scale and polynomial Bergman growth, not the
Riemann-von-Mangoldt factor `pi/(T log(T/(2*pi)))`.

Numerical comparison artifact records all 15 Step 324 zeros.  The AMM local
kernel does not supply a `gamma_derived(T)` matching the empirical law.

Verdict: `shape_mismatch_and_projector_identification_stall`.

The stall is twofold:

1. the inherited literal formula has no finite saddle under the cusp
   substitution at zeta-zero heights;
2. even the corrected local punctured-disc Bergman saddle is not identified
   with Branch C's `P_infty T_a^* partial^k K_a^Gamma` projector and lacks the
   zero-density `log(T/(2*pi))` factor.

No RH or Branch C closure is claimed.
