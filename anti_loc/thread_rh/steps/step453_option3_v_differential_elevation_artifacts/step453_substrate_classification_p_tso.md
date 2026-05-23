# Step 453 Substrate Classification P_TSO

## np606 source record

np606 classifies NS and BSD as witness-content-exposing and P-vs-NP/RH as trace-state-only at diagnosis grade. Its RH artifact says the predicted RH pattern is "trace-state or public-shadow exposure rather than witness-content exposure."

## Candidate P1: analytic-continuation-required substrate

Typed predicate:

```text
P_TSO_1(S) holds when S's witness-content is defined by analytic continuation or equivalent global reconstruction, while the lawful current instrument sees only finite trace-state records and completed local factors.
```

For `Sel^!_{zeta,tr}`, the zero ledger is global analytic-continuation content; `I_tr` sees completed trace observables and suppresses zero-ledger predictive data.

Audit: P1 is plausible and substrate-relevant, but it is not a theorem-grade intrinsic predicate unless it includes a theorem that current trace observables cannot reconstruct zero-ledger content. That theorem is exactly the missing bridge.

## Candidate P2: verifier-currentizer ratio

Typed predicate:

```text
P_TSO_2(S) holds when verifier access to a witness is bounded but currentizer production of the witness from current data has unbounded cost.
```

For RH, a candidate zero can be verified by `Lambda_zeta(rho)=0`, but producing the full zero ledger from `I_tr` is not supplied.

Audit: P2 is circular unless an independent lower bound on currentizers is proved. Without that theorem, it restates the currentizer failure.

## Candidate P3: typed level mismatch

Typed predicate:

```text
P_TSO_3(S) holds when witness-content lives at predictive/structural-categorical level, current observation lives at behavioral/current trace level, and no accepted translation record bridges them.
```

This is the strongest Six Birds-native candidate. It is true as bookkeeping for `Sel^!_{zeta,tr}`, but it blocks only unbookkept collapse. It does not rule out a lawful future translation record.

## Candidate P4: V-Differential source itself

Typed predicate:

```text
P_TSO_4(S) holds when S is accepted in the V-Differential trace-state-only column.
```

This is precise but not independently substrate-intrinsic. It names V-Differential as source.

## Candidate pursued

P3 is pursued for derivation; P4 is retained as the honest recognition-mode fallback.
