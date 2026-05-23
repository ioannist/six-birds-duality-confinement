# Step 221 Results Summary

## Target

Cross-track test of the RH-derived CTMT recursion pattern on the BSD track's Bloch-Kato determinant-line bridge decomposition.

## BSD Records Read

Read-only BSD records:

- `anti_loc/thread_bsd/cascade_map_bsd.md`
- `anti_loc/thread_bsd/steps/bsd_b52a_extracted/bsd_b52a_results_summary.md`
- `bsd_b52a_defect_equation.csv`
- `bsd_b52a_component_map.csv`
- `bsd_b52a_external_obligations.csv`
- `bsd_b52a_schema.json`

BSD state:

`diagnostic_complete`, not `proof_complete`.

Main decomposition:

`Delta_BSD^BK = E_an/period + E_ht/reg + E_finite + sum_p E_p + E_det`.

Central external theorem:

Construct `rho_an/period`, `rho_ht/reg`, `rho_finite`, `rho_p`, `rho_det` into the Bloch-Kato determinant line and prove all component defects vanish under the claimed hypotheses.

## Literature Audit

The literature supplies framework language and partial theorem rows, but not a general all-elliptic-curves determinant-line closure.

- Bloch-Kato 1990 formulates motivic Tamagawa-number special-value conjectures and removes the `Q*` ambiguity by defining Tamagawa numbers for motives.
- Fontaine-Perrin-Riou 1994 extends/refines the Bloch-Kato cohomological formulation.
- Burns-Flach 2001 supplies determinant functors and an equivariant Tamagawa formulation refining Bloch-Kato/FPR.
- Burns-Flach 2006 proves ETNC for Tate motives in specific abelian settings, not general elliptic curves.
- Kato 2004 supplies Euler-system / Selmer bounds for modular forms.
- Skinner-Urban 2014 proves the Iwasawa-Greenberg Main Conjecture in many GL2 cases under explicit hypotheses, combining with Kato for equality.
- Howard 2004 supplies one divisibility in a Heegner-point Iwasawa setting.
- Kim 2010 supplies Selmer-variety results for CM elliptic curves, not the BSD determinant-line component theorem.

## CTMT Recursion Layers

BSD layer chain:

1. `BK_component_maps` gate: construct component maps into the BK determinant line.
2. ETNC/Bloch-Kato determinant-line formulation: gives target object, not global proof.
3. Relative K-theory / determinant functor / orientation data: Burns-Flach refines the target into `K0`/determinant-line objects.
4. p-adic component: reduces to Iwasawa main conjecture rows under hypotheses.
5. Iwasawa/Euler-system layer: Kato gives one divisibility; Skinner-Urban gives complementary cases under hypotheses; Howard gives one divisibility in Heegner settings.
6. Residual BSD obligations persist: all support primes, higher rank cycles, component vanishing, determinant trivialization, global audit promotion.

## Verdict

`V_bsd_CTMT_recursion_verified`.

The BSD track replicates the CTMT recursion pattern on a second Clay track: the named external determinant-line gate is not a single terminal theorem. Literature resolution refines it into deeper determinant-line, ETNC, Iwasawa, Euler-system, control, and hypothesis gates.
