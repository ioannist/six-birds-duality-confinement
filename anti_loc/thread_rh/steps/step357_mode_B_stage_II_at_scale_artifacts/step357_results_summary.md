# Step 357 Results Summary

Extended Mode B `U^flat` Stage II to a 520-cell reproduction.

Cell counts:

- Hecke atom reproductions: `70/70`
- Zeta atom reproductions: `30/30`
- Compare reproductions: `210/210`
- Operator-audit reproductions: `210/210`

Total: `520/520` cells passed.

All cells were emitted through the finite rewrite/lens paths from step 356:

- `R_H_load -> q(a)`
- `R_Z_load -> q(b)`
- `R_compare -> q(c)`
- `R_operator_audit -> q(d)`

No target transfer `tau` or kernel-preserving H6 closure was used.

## Ablations

Three substantive rewrite ablations were tested:

1. Remove `R_compare`: breaks `210/210` compare cells.
2. Remove `R_operator_audit`: breaks `210/210` operator-audit cells.
3. Remove `R_block`: breaks `210/210` non-descent gate decisions by
   preventing `u_NC = e` from being reached.

## Verdict

`V_mode_B_stage_II_passes_at_scale_substantive`.

Mode B earns its place at scale.  The carrier remains target-local and does
not claim H6 bridge closure.
