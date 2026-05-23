# Step 398: Branch A Phi_max via Bergman Cusp Asymptotic

## Cascade Inputs Used

- Step 196 wavepacket form used verbatim from the step request: `u_T(x) = T^{1/4}*G(sigma*T*log(x))`, with cusp lift tied to the cusp coordinate.
- Step 220 result used verbatim: `Phi(sigma, ell) = lim_T ||C_ell u_T||`, refined maximum `sigma_max = 0.35`, `ell_max = 2.0`, `Phi_max = 0.49047661902424095`.
- Step 217/218/220 identify the tested operator as `C_l u = (I - P_infty) M_{m_l} P_infty u`; Step 220 scans the wavepacket-family `C_l P_infty`, not the narrower `C_l P_eta`.
- Step 372 Bergman tool used verbatim: `B_p^{D*}(z) = (log|z|^2)^p/(2*pi*(p-2)!) * sum_{ell>=1} (p-1)/ell! * (-ell*log|z|^2)^{ell-1}` and `sup B_p ~ p^{3/2}/(2*pi)`.

## Cusp Coordinate Substitution

Use the standard punctured-disc cusp coordinate

```text
z = exp(2*pi*i*w),       w = u + iT,
|z|^2 = exp(-4*pi*T),
log|z|^2 = -4*pi*T.
```

Substitution into the Auvray-Ma-Marinescu model kernel gives

```text
B_p^{D*}(T)
  = (-4*pi*T)^p/(2*pi*(p-2)!)
    * sum_{ell>=1} (p-1)/ell! * (4*pi*T*ell)^{ell-1}.
```

This gives the correct cusp density scale and the known global maximum
asymptotic `sup B_p ~ p^{3/2}/(2*pi)`.

## Attempted Phi_max Extraction

Step 220 does not compute a Bergman projector norm directly.  It computes the
commutator-like quantity

```text
C_ell = (I - P_infty) M_{m_ell} P_infty
```

where the implemented `P_infty` is the finite PSWF/sinc operational model:

```text
P_infty f = f - sinc_part(f) - sum_n psi_n <psi_n, f>.
```

The Bergman formula supplies the local cusp kernel for holomorphic `L^p`
sections, while Step 220's computation is a critical-line PSWF/sinc projection
in the `tau` variable.  Therefore a theorem-grade derivation of `Phi_max`
requires a transport identity:

```text
Auvray-Ma-Marinescu cusp Bergman projector
    --> Step 173/215 PSWF/sinc P_infty projector
```

together with a dictionary

```text
p <--> (T, sigma, ell) or p <--> wavepacket bandwidth/shift data.
```

Those identities are not present in the inherited Branch A records.

## Closed-Form Candidate From the Bergman Picture

The natural Bergman-side leading candidate is

```text
Phi_max = 1/2.
```

Reason: if the cusp projector is transported to the local translation-invariant
model and the optimal modulation places the shifted packet at the balanced
projector boundary, the leading leakage of the shifted Bergman mass is one half.
This is consistent with the Step 220 maximizer being at a boundary-like large
shift `ell = 2.0` and narrow packet `sigma = 0.35`.

Numerically:

```text
1/2 = 0.5,   relative error vs Step220 Phi_max = 1.9417%.
```

The numerically closer candidate `pi^2/20 = 0.4934802201` has relative error
`0.6124%`, but no derivation from the Auvray-Ma-Marinescu formula was found in
this step.  It remains a candidate constant, not a structural conclusion.

## Derivation Status

The Bergman cusp asymptotic gives a plausible analytical anchor for the
observed `Phi_max ~= 0.4905`, with `1/2` within 5%.  It does not yet provide a
closed Branch A theorem because the required Bergman-to-PSWF transport identity
and the `p`-to-`(sigma, ell)` dictionary are missing.
