# Step 399: Bergman-to-PSWF/Sinc Transport Identity Attempt

## Inputs Used

- Step 173 identity used verbatim:
  `K_infty^op(s,s') = delta(tau-tau') - sin(lambda(tau-tau'))/(pi(tau-tau')) - sum_n Psi_n^lambda(s) conjugate(Psi_n^lambda(s'))`.
- Step 196/220 wavepacket form used verbatim from the request:
  `u_{T,sigma,ell}(x) = T^{1/4}*G(sigma*T*log(x))*g_ell(x)`.
- Step 220 operator used verbatim from the Branch A records:
  `C_l u_n = (I - P_infty) M_{m_l} P_infty u_n`.
- Step 372 Auvray-Ma-Marinescu formula used verbatim:
  `B_p^{D*}(z) = (log|z|^2)^p/(2*pi*(p-2)!)*sum_{ell>=1}(p-1)/ell!*(-ell*log|z|^2)^{ell-1}`.
- Step 385/387 blocker used verbatim in substance: Branch C stalls at the PSWF transition asymptotic / missing PSWF evaluator.
- Step 398 blocker used verbatim in substance: Branch A stalls at the missing Bergman-to-PSWF transport identity.

## T1: Wavepacket in Cusp Coordinate

With

```text
z = exp(2*pi*i*w),       w = u+iT,
|z|^2 = exp(-4*pi*T),
T(z) = -log|z|^2/(4*pi).
```

a critical-line wavepacket centered at height `T0` becomes a punctured-disc
annular packet

```text
u_tilde_{T0,sigma,ell}(z)
  = J(z)^{1/2} * Z^{-1/2}
    * G(sigma*T0*(T(z)-T0)) * g_ell(z),
```

where `J(z)` is the Jacobian needed to move from the cascade's `d tau/(2*pi)`
normalization to the punctured-disc Poincare volume normalization.  The packet
is concentrated near the annulus

```text
|z| = exp(-2*pi*T0)
```

with logarithmic radial width determined by the chosen Step196/220 wavepacket
normalization.

## T2: Bergman Action on the Packet

The desired Bergman action is

```text
(B_p^{D*} u_tilde)(z)
  = integral_{D*} K_p^{D*}(z,z') u_tilde(z') dmu_{D*}(z').
```

The inherited Auvray-Ma-Marinescu input supplies the diagonal kernel function
`B_p^{D*}(z)=K_p^{D*}(z,z)`.  It does not by itself supply the off-diagonal
kernel `K_p^{D*}(z,z')` needed to act on a wavepacket.

Using the orthonormal monomial basis mentioned in Step372, the off-diagonal
kernel should have the schematic form

```text
K_p^{D*}(z,z') = sum_{m>=1} a_{p,m} z^m conjugate(z')^m,
```

but the cascade has not recorded the transported coefficients `a_{p,m}` in
the same normalization as the PSWF/sinc `P_infty` model.

## T3: Comparison with PSWF/Sinc P_infty

The Step173/215 operator is additive in the critical-line variable:

```text
(P_infty u)(tau)
  = u(tau)
    - integral sinc_lambda(tau-tau') u(tau') d tau'
    - sum_n Psi_n^lambda(tau) <Psi_n^lambda,u>.
```

This is a Sonine/prolate two-cutoff projection:

```text
S_lambda = Proj(ker P_lambda cap ker Phat_lambda).
```

The Bergman projector is a holomorphic cusp-form `L^p` projector.  Its large
`p` asymptotic is controlled by cusp monomial modes and the Poincare metric.
The PSWF/sinc projector is controlled by a fixed bandwidth `lambda`, the sinc
kernel, and PSWF transition modes.

To prove the requested transport identity one needs, at minimum, a scaling
dictionary

```text
p  <-->  lambda, sigma, ell, T0
```

and an off-diagonal asymptotic showing that the Bergman monomial sum converges
after log-cusp transport to

```text
delta - sinc_lambda - sum_n Psi_n^lambda Psi_n^{lambda,*}.
```

No such identity is present in the inherited records.

## Attempted Large-p Limit

After the substitution `T=-log|z|^2/(4*pi)`, the diagonal Bergman expression is

```text
B_p^{D*}(T)
  = (-4*pi*T)^p/(2*pi*(p-2)!)
    * sum_{m>=1} (p-1)/m! * (4*pi*T*m)^{m-1}.
```

The saddle of this diagonal sum describes the pointwise cusp density of an
`L^p` Bergman projector.  It does not generate the translation-invariant sinc
kernel in `tau-tau'`, because sinc arises from a sharp additive frequency
cutoff, while the diagonal Bergman sum has only radial pointwise information.

The missing subproblem is therefore not merely a constant: it is the
off-diagonal, log-cusp, transition asymptotic

```text
K_p^{D*}(T,T') under z=exp(2*pi*i*w)
  --> delta(tau-tau') - sinc_lambda(tau-tau')
      - sum_n Psi_n^lambda(tau) conjugate(Psi_n^lambda(tau')).
```

## Verdict

No closed-form transport identity was derived.

Partial progress: both projectors share a cusp concentration mechanism, and
the Bergman diagonal asymptotic plausibly explains the Step398 half-mass scale.

Precise stall:

```text
Need an off-diagonal Auvray-Ma-Marinescu large-p asymptotic in log-cusp
coordinates, with a scaling p <--> lambda, proving convergence to the
Slepian-Pollak PSWF/sinc two-cutoff kernel.
```

This is the common blocker for theorem-grade Branch A Phi_max and Branch C
gamma_zeta closure.
