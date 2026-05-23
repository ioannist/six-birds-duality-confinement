# Step 280 Results Summary

## Target

Audit Skinner-Urban 2014, *The Iwasawa Main Conjectures for GL2*, as the BSD track's top score-2 bridge candidate for the b-52a CTMT chain.

## Paper-Grounded Extract

Skinner-Urban's scope statement is:

> We prove the one-, two-, and three-variable Iwasawa-Greenberg Main Conjectures for a large class of modular forms that are ordinary with respect to an odd prime p.

The ordinary hypothesis is explicit:

> Suppose f is ordinary; that is, a(p, f) is a p-adic unit

Theorem 1 hypotheses include residual irreducibility, an auxiliary ramified prime, and a level restriction:

> the reduction rho_bar_f of rho_f modulo the maximal ideal of O_L is irreducible

> there exists a prime q != p such that q||N and rho_bar_f is ramified at q

> p does not divide N

The conclusion supplies the Iwasawa characteristic-ideal equality:

> Then Ch_Q_infty,L(f) = (L_f) in Lambda_Q,O_L tensor_Zp Q_p.

The integral equality add-on requires a big-image condition:

> there exists an O_L-basis of T_f with respect to which the image of rho_f contains SL_2(Z_p)

For elliptic curves, the application hypotheses include:

> E has good ordinary reduction at p; rho_bar_E,p is irreducible; there exists a prime q != p such that q||N_E and rho_bar_E,p is ramified at q.

## Cascade Need vs Supplied Theorem

The BSD b-52a chain needs all-primes and all-cases closure for the p-adic/determinant component of the residual
`E_an/period + E_ht/reg + E_finite + sum_p E_p + E_det = 0`.

Skinner-Urban supplies a deep ordinary GL2 Iwasawa main-conjecture theorem under explicit technical hypotheses. It does not by itself supply:

- non-ordinary prime control,
- residually reducible case control,
- missing auxiliary ramification cases,
- all local support primes,
- the global ETNC/Bloch-Kato determinant identity needed by the b-52a residual.

## Verdict

`V_skinner_urban_BSD_bridge_blocked`

The cascade-needed full BSD bridge is not derivable from Skinner-Urban 2014 alone. The candidate score-2 BSD interface downgrades to score-1: a new all-primes/all-cases bridge theorem would be required.

## Pattern Assessment

This extends the empirical downgrade pattern to four audited score-2 candidates:

1. Step 267: Burnol transport-sampling -> score-1.
2. Step 268: Connes-Consani recoverability -> score-1.
3. Step 279: Burnol `a<1` form -> score-1.
4. Step 280: Skinner-Urban GL2 Iwasawa bridge -> score-1 for full BSD b-52a closure.

This is cross-track evidence for the Attack Foreclosure Conjecture, not a theorem that BSD or RH is impossible or solved.
