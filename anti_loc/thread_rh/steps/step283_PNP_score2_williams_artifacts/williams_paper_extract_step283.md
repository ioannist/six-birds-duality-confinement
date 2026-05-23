# Williams ACC Lower Bound Extract -- Step 283

Primary source: Ryan Williams, *Non-Uniform ACC Circuit Lower Bounds*, J. ACM 61(1), Article 2, 2014; earlier CCC 2011 version.

Main lower-bound statement:

> NEXP ... does not have non-uniform ACC circuits of polynomial size.

Theorem 1.1 statement:

> NTIME[2^n] does not have non-uniform ACC circuits of polynomial size.

Stronger related bound:

> ENP ... doesn't have non-uniform ACC circuits of 2^{n^{o(1)}} size.

Williams explicitly distinguishes this from the NP lower-bound target:

> P != NP follows if one could provide an NP problem

Barrier context from Aaronson-Wigderson:

> Any proof of P != NP will have to overcome two barriers: relativization and natural proofs.

and:

> we present such a barrier, which we call algebraic relativization or algebrization

Audit reading: Williams supplies a major unconditional lower bound, but it separates `NEXP`/`NTIME[2^n]` from non-uniform `ACC^0`.  The P-vs-NP cascade needs a bridge to the NP/P scale or to the universal P-machine atlas.  Williams does not supply that bridge.
