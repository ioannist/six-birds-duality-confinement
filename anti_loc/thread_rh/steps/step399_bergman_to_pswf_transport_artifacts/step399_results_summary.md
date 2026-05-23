# Step 399 Results Summary

## Cusp-Coordinate Wavepacket

With `z=exp(2*pi*i*w)`, `Im(w)=T`,

```text
T(z) = -log|z|^2/(4*pi).
```

The cascade wavepacket becomes an annular punctured-disc packet

```text
u_tilde(z) = J(z)^(1/2) * Z^(-1/2)
             * G(sigma*T0*(T(z)-T0)) * g_ell(z),
```

concentrated near `|z|=exp(-2*pi*T0)`.

## Bergman Action

The desired action is

```text
(B_p^{D*}u_tilde)(z)=integral K_p^{D*}(z,z')u_tilde(z')dmu_Dstar(z').
```

The inherited Auvray-Ma-Marinescu formula supplies the diagonal kernel
`B_p^{D*}(z)=K_p^{D*}(z,z)`, not the off-diagonal kernel needed for the
operator action on `u_tilde`.

## Comparison to P_infty

Step173 gives

```text
P_infty = delta - sinc_lambda - sum_n Psi_n^lambda Psi_n^{lambda,*}.
```

This is a Slepian-Pollak PSWF two-cutoff projection in additive `tau`.  The
Bergman kernel is a holomorphic `L^p` cusp projector in multiplicative `z`.

## Verdict

Transport identity not found.  Partial match only: the Bergman diagonal cusp
asymptotic explains the half-mass scale behind Step398, but the dual-branch
closure needs an off-diagonal log-cusp large-`p` asymptotic plus a scaling
dictionary `p <-> lambda,sigma,ell,T` proving convergence to the Step173
PSWF/sinc kernel.

Named missing subproblem:

```text
Off-diagonal Auvray-Ma-Marinescu Bergman kernel asymptotic in log-cusp
coordinates converging to the Slepian-Pollak PSWF/sinc two-cutoff kernel.
```

No RH claim is made.
