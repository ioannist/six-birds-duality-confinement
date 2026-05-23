# Step 178: Kappa Derivation Attempt

Verdict:

`kappa_verdict = V_kappa_classical_theorem_needed`.

Target:

```tex
kappa_{a,w}(tau) = (T_a^*K_a^Gamma(.,w))(1/2+i tau).
```

The inherited records give:

```tex
T_a = M_Gamma J_a U_infty^{-1}
```

and

```tex
K_a^Gamma(.,w)=P_{L_a^Gamma}K_a^{Gamma,amb}(.,w),
```

with the ambient Hardy kernel

```tex
K_a^{Gamma,amb}(s,w)
= A_infty(s)conj(A_infty(w))
  s/(s-1) conj(w/(w-1))
  a^{s+conj(w)-1}/(s+conj(w)-1).
```

Attack A reaches

```tex
kappa_{a,w}=T_a^*P_{L_a^Gamma}K_a^{Gamma,amb}(.,w),
```

but needs the explicit projected Sonine kernel.  Attack B reaches the integral
operator identity

```tex
kappa_{a,w}(tau)=int overline{T_a(z,tau)} K_a^Gamma(z,w) dz,
```

but needs the kernel of `T_a^*` and the projected kernel.  Attack C reaches a
formal spectral expansion, but needs the Bessel/Hankel spectral data for
`P_{L_a^Gamma}`.

Specific named missing theorem:

Burnol's explicit Bessel/Hankel resolvent formula for the orthogonal projection
`P_{L_a^Gamma}`, equivalently the reproducing kernel
`K_a^Gamma=P_{L_a^Gamma}K_a^{Gamma,amb}`, for the extended Sonine space `L_a`
at `a=1/2`.

No sample kappa values were lawfully computed; `kappa_sample_values_step178.csv`
records the requested tau grid with status
`not_computed_classical_projection_theorem_needed`.  Consequently
`c_{11}(log 2)` was not attempted numerically.

Branch B implication: the blockage is now externalized as a specific classical
Burnol/Bessel projection theorem, not a generic transport ambiguity.
