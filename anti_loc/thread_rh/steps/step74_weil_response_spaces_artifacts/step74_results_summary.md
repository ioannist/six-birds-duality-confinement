# Step 74: Weil Test Space and Anti-Invariant Response Space

## Purpose

This step identifies the space on which the RH Weil--Douglas bridge must live.

The RH membrane chain requires

\[
\mathsf A_Z \preceq \mathsf K_{\rm cmp},
\]

equivalently

\[
V_Z = T W_{\rm cmp},\qquad \|T\|\le 1.
\]

Step 74 clarifies that this is not a statement about a finite test family or a public trace shadow. It is a domination statement on the full completed anti-invariant response space, or on a dense form core with a closability/core-extension record.

## Four response levels

1. **Full completed response space** \(Y^-_{\rm full}\): the Hilbert completion of the anti-invariant response domain under the completed carrier form. Only here is a full Douglas bridge accepted.
2. **Dense Weil core** \(Y^-_{\rm core}\): a dense admissible test class. Positivity/domination here promotes only with a form-core and closability record.
3. **Finite/truncated family** \(Y^-_{N,T}\): finite windows or finite tests. This is support-only unless accompanied by an exhaustive tail bridge.
4. **Public shadow** \(Y^-_{\rm pub}\): traces, scalar moments, Li-type scalar values, or other public readouts. These do not promote to carrier domination without reconstruction and defect records.

## Main theorem

Let

\[
q_Z[y]=\|V_Zy\|^2,
\qquad
q_{\rm cmp}[y]=\|W_{\rm cmp}y\|^2.
\]

If, on a dense form core \(\mathcal C\),

\[
q_Z[y]\le q_{\rm cmp}[y],
\]

and \(q_{\rm cmp}\) is closable with \(\mathcal C\) as a form core, then the domination extends to the completed response space. Equivalently, there is a contraction

\[
V_Z=T W_{\rm cmp},\qquad \|T\|\le1.
\]

## Candidate core types

- Log-side core: compactly supported smooth functions in \(t=\log x\), suitable for shift-feature candidates.
- Spectral Paley--Wiener core: closer to classical explicit formula presentations.
- Carrier-native core: de Branges, adelic, Selberg/trace-formula, or another exact carrier-specific domain.

## Nonclaims

This step does not prove RH and does not prove the Weil bridge. It only states the precise spaces and gates needed before the bridge can be honestly attempted.

Finite test positivity, trace equality, and signed explicit formula identities are not enough.
