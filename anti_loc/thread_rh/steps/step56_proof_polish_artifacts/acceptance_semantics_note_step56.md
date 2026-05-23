# Acceptance semantics clarification

The matrix predicate

```math
\widehat K_j \preceq \Theta \quad \forall j
```

is equivalent to the absence of native predictive recombination witnesses at the mathematical ledger level.

It is **not**, by itself, equivalent to Six Birds acceptance.

Six Birds acceptance additionally requires:

- formed closure;
- exact package;
- null-mode legality;
- declared native family;
- adequacy/exhaustivity for layer-dissolving probes;
- predictive transport;
- protocol honesty;
- all-six channel statuses;
- completed witness ledger;
- nonclaim boundary.

So the safe wording is:

```math
\text{accepted all-six membrane record} \Rightarrow \widehat K_j\preceq\Theta.
```

The reverse implication is allowed only relative to a fixed acceptance schema that already includes all gates.
