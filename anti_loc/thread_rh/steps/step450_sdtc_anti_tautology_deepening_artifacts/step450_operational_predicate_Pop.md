# Step 450 Operational Predicate Pop (Stage II.1)

Chosen operational predicate:

```text
Pop_SDTC_DominationCandidateAudit
```

## Operational signature

Inputs:

1. `Sel^!_{zeta,tr}` closure record;
2. a candidate domination sequence `(B_n, cert_n)`;
3. finite-window exhaustion schedule `(W_N, T_N)` for the zero ledger;
4. source record label (`framework-derived`, `recognition-supplied`, or `external/invalid`).

Outputs:

- `PASS_n` or `FAIL_n` for each candidate record;
- failure code in `{ledger, positivity, Loewner, trace-limit, Douglas-factorization, source-readout, tail-exhaustivity, visibility}`;
- global status `candidate_domination_sequence_admissible` only if all local checks pass and trace/tail bounds tend to zero.

Procedure:

1. build windowed `A_Z(W_N)` from zero-ledger readout;
2. check positivity of `B_n`;
3. check Loewner domination `A_Z(W_N)+T_N <= B_n`;
4. attempt Douglas factorization certificate `V_N=T_n W_N` where applicable;
5. check `tr B_n + tr T_N -> 0`;
6. verify source/readout nonclaim: a readout-equivalent `A_Z=0` is not accepted as source.

This is operational because it is an audit procedure with inputs, outputs, failure modes, and replay records. It is not a predicate conjunction.
