# Step 450 Non-Conjunctive Verification (Stage II.3)

`Pop_SDTC_DominationCandidateAudit` is not equivalent to `P1 and P2 and P3 and P4` over independently existing predicates.

Non-conjunctive structural content: **mutual coupling**.

- The Loewner check uses `A_Z(W_N)`, which is computed from `psi_-` on the zero ledger.
- The Douglas factorization check uses the same `A_Z(W_N)` as the object-side operator in a domination bridge.
- The trace-limit check couples `B_n` to the same window/tail schedule.
- The source/readout check governs whether a candidate record is admissible as source or merely repeats the RH-equivalent readout.
- Visibility/audit records must remain consistent across all checks.

If any component is moved to an independent carrier, the procedure cannot run because the next step consumes its typed output. That data dependency is operational, not conjunctive.

Verdict: Pop passes the non-conjunctive audit.
