# Step 445 Falsification Conditions

## 1. Does Theta^D's specification require smuggling arithmetic?

Partly yes. As a finite matrix bound, `Theta^D` is non-arithmetic. As a claim that the bound holds iff all scoped zeros lie on `Re(s)=1/2`, it becomes an implicit RH/zero-localization predicate. This triggers the semantic-audit failure.

## 2. Does Xi require invoking RH or arithmetic data beyond K^L?

No. `Xi` is Schur-computed from `K_LL,K_DL,K_DD` with eigenvalues `['0.0007', '0.0018', '0.0036']` and error `1.3177747e-82`.

## 3. Does the Capacity-bound conclusion require an external audit step the three components do not supply?

Yes. This is the primary failure. The package proves `S K^D S^* <= Theta^D` as a formal capacity bound, but an external semantic audit is needed to read `D` and `Theta^D` as zero-localization-on-critical-line.

## 4. Does the failure pattern match prior no-gos?

It matches the Step 444 meta-pattern in shifted form. Removing the audit component does not remove audit content; it relocates it into the semantics of `D` and `Theta^D`.

## Verdict

Stage I retracts under new constraint `C_capacity_bound_semantic_audit_smuggling`. This is evidence for local Mode B saturation pressure on the constitutive-closure design space at the zeta substrate, but this single attempt does not exhaust `G_closure_only_no_audit`.
