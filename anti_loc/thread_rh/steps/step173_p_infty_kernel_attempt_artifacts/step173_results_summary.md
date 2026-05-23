# Step 173: P_infty Kernel Attempt

Verdict:

`kernel_verdict = V_operational_identity`.

The step does not produce a closed elementary Mellin kernel.  It does produce
an exact operational identity for the inherited archimedean Sonin/prolate
projection by combining the Step104 two-cutoff definition with the classical
Slepian-Pollak PSWF diagonalization.

Let `P=P_lambda` be cutoff to `[-lambda,lambda]`, and
`Q=Phat_lambda=F^{-1}P_lambda F`.  Then

```tex
S_lambda = Proj(ker P cap ker Q)
         = I - P - (I-P)Q(I_{QH}-QPQ)^{-1}Q(I-P).
```

If `phi_n^lambda` are the bandlimited PSWFs diagonalizing
`QPQ phi_n = mu_n phi_n`, `0<mu_n<1`, then

```tex
S_lambda
= I-P
  - sum_n |(I-P)phi_n><(I-P)phi_n|/(1-mu_n).
```

Transporting by the standard log-Mellin realization gives the operational
Mellin kernel

```tex
K_infty^op(s,s')
= delta(tau-tau')
 - sin(lambda(tau-tau'))/(pi(tau-tau'))
 - sum_n Psi_n^lambda(s) conjugate(Psi_n^lambda(s')),
```

where `s=1/2+i tau` and

```tex
Psi_n^lambda
= U_infty((I-P_lambda)phi_n^lambda / sqrt(1-mu_n)).
```

This is an exact PSWF-series operational identity for `mathsf P_infty`.

Data point:

For the legal zero generator `g_0=0`, `G_0=0`, and
`rho_1=1/2+14.134725...i`, `k=0`,

```tex
L_{rho_1,0}(G_0)=0.
```

For nonzero legal generators, the result turns the formerly undefined
projection into a concrete PSWF-series pairing.  The remaining computational
work is evaluation of the Mellin transforms of the PSWF tails and of the
transported evaluator pairings.
