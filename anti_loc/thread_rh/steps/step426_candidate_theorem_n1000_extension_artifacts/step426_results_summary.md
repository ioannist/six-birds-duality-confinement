# Step 426 Results Summary

## Computation

- Zeros computed: `rho_1..rho_1001`.
- Tested zeros: `j=1..1000`.
- mpmath dps: `50`.
- Truncated diagnostic Hadamard rest window: `|gamma'-gamma| < 50`.

## Exceptional Count

- Exceptional zeros `Re zeta''(rho_j) >= 0`: `181/1000` = `0.181000`.

## Dominance Verification

- Audited rows: `211` = `181` exceptional + `30` non-exceptional baseline.
- Dominance matches: `208/211`.
- Exceptional matches: `178/181`.
- Baseline matches: `30/30`.

## Mismatches

- j=705: Re zeta''=22.1741515257, |A|=11.4821098255, |B|=10.6920417002, rel_gap=0.068808619, s_min=0.57113996
- j=871: Re zeta''=19.8091824243, |A|=10.3695676959, |B|=9.4396147284, rel_gap=0.089680978, s_min=0.37022617
- j=965: Re zeta''=23.1908247343, |A|=13.2893147998, |B|=9.90150993444, rel_gap=0.25492698, s_min=0.46529541

These are exceptional zeros with `B>0` but `|B| < |A|`; the actual `Re zeta''` remains positive because `A` is also positive enough. This refines the Step 422 candidate: close-pair dominance is sufficient in most cases but not necessary at n=1000.

## Aggregates on Audited Rows

- mean |A|: `6.49481276767558668439051`.
- median |A|: `4.424237721319254745822036`.
- max |A|: `44.41329065259875363835818`.
- mean |B|: `8.29490308405778975497924`.
- median |B|: `8.034035782939504599653446`.
- max |B|: `16.269447197043675146233`.
- tightest relative dominance gap: `0.001427809892817569594261617`.

## Verdict

The candidate theorem is not maintained exactly at n=1000. The large-sample audit finds `3` positive exceptional cells where close-pair dominance fails, so the Step 422 iff statement must be weakened or refined to include positive regular-remainder assistance.

## Verbatim Step Anchors

- Step 377: `93/100 zeros have Re zeta''(rho_j) < 0`.
- Step 378: exceptions are characterized by compressed local spacing.
- Step 381: `zeta''(rho_j) = 2*zeta'(rho_j)*g_j'(rho_j)`.
- Step 422: `Re L''(rho) >= 0 iff B(rho) > 0 and |B(rho)| > |A(rho)|`.
