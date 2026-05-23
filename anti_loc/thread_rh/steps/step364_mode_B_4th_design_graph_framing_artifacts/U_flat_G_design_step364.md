# U^flat_G: Graph-Based Mode B Operational Signature

## Graph

Nodes V = {v_H, v_Z, v_compare, v_audit, v_blocked}.

Edges E:

- e_load_H: v_H -> v_compare, loads H_{chi,k}.
- e_load_Z: v_Z -> v_compare, loads Z_{rho,k}.
- e_compare: v_compare -> v_audit, computes lambda_mag and lambda_phase.
- e_audit: v_audit -> v_audit, applies operator-compatibility path predicate.
- e_block: v_audit -> v_blocked, records defect.

Path predicates P:

- P_mag: path trace has lambda_mag below threshold.
- P_phase: path trace has lambda_phase below threshold.
- P_operator: path trace has certified operator compatibility.
- P_admit: P_mag and P_phase and P_operator all hold and no path reaches v_blocked.

Lens q emits host-layer values from node labels.  Equivalence is path-trace equivalence:
two paths are equivalent when they have identical emitted lens value and identical defect ledger.

This is not a state relabeling of U^flat/U^flat-prime/U^flat-double-prime: the primitive object is a finite labeled graph with admissibility over path traces.

## Stage III Graph Transfer

The transfer is not a primitive edge.  It is a path-composition rule using shared edge-label weights:

- log |T_G(H)| = a0 + a1 x + a2 k + a3 x k + a4 k^2, x = log|H|.
- arg T_G(H) = arg H + b0 + b1 x + b2 k + b3 x k + b4 k^2.

The coefficients are graph-level path weights shared across all characters.
