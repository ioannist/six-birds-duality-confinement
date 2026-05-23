# Step 398 Results Summary

## Cusp Substitution

Using `z = exp(2*pi*i*w)` with `Im(w)=T`,

```text
|z|^2 = exp(-4*pi*T),     log|z|^2 = -4*pi*T.
```

The Auvray-Ma-Marinescu punctured-disc kernel becomes

```text
B_p^{D*}(T)
  = (-4*pi*T)^p/(2*pi*(p-2)!)
    * sum_{ell>=1} (p-1)/ell! * (4*pi*T*ell)^{ell-1}.
```

## Comparison Target

Step 220: `Phi_max = 0.49047661902424095` at `(sigma, ell)=(0.35, 2.0)`.

## Candidate Outcome

Best defensible Bergman-side leading candidate:

```text
Phi_max = 1/2 = 0.5
```

Relative error vs Step220:

```text
1.9416585%
```

Closest simple candidate tested:

```text
pi^2/20 = 0.4934802200544679
```

Relative error:

```text
0.6123841%
```

but no structural derivation of `pi^2/20` from the Bergman formula was found.

## Verdict

Partial analytical anchor.  The Bergman cusp picture supports a natural
half-mass candidate `Phi_max = 1/2`, within 5% of Step220's `0.4904766190`.
The derivation is not theorem-grade because the inherited records do not supply
the transport identity from the Auvray-Ma-Marinescu `L^p` cusp Bergman projector
to the Step173/215 finite PSWF/sinc `P_infty` model, nor the dictionary mapping
`p` to Step220's `(T, sigma, ell)` wavepacket parameters.

No RH claim is made.
