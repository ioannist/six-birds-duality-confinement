# Step 448 Quotients and Comparison Map (Stage I.9)

Define equivalence relations on `H^!_L`:

- `h ~_Q h'` iff all observables in `E^!_Q^tr` agree with the same visibility and replay records.
- `h ~_M h'` iff all predictive zero-ledger events in `E^!_M^zero` agree with multiplicity, anti-invariant readout, and tail records.

Set

```text
Q^!_L = H^!_L / ~_Q
M^!_L = H^!_L / ~_M
pi^!_L : M^!_L -> Q^!_L
```

where `pi^!_L` forgets predictive zero-ledger data down to current trace observables and records the loss. Nontrivial fibers are expected; their existence is route-mismatch content, not failure.

Completed closure:

```text
Sel^!_{L,tr}=(H^!_L,I_tr,E^!_Q^tr,E^!_M^zero,Q^!_L,M^!_L,
              pi^!_L,J_L,Lambda_L,Z_L^nt,A_Z(L),Vis^!_L,Audit_L).
```
