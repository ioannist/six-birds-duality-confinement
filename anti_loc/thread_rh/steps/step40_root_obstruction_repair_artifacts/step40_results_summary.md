# Step 40: Obstruction-to-Repair Theorem for the Root-Composite Route

## Purpose

Step 39 produced an obstruction ledger for the root-composite RH-facing anti-localization route. Step 40 turns that ledger into a repair calculus.

The central question is:

\[
\text{If zero confinement fails, which repair can lawfully reduce the obstruction budget?}
\]

The answer is strict: a repair is proof-strengthening only if it reduces the same-sector Loewner obstruction budget. Otherwise it is either support-only, truthfulness-improving, or scope-narrowing.

## Main budget

The visible anti-invariant displacement matrix satisfies the defective bound

\[
\mathsf A_Z
\preceq
(1+t)\bigl(\Lambda^{-1}\Theta_0^-+E_{\rm src}\bigr)
+
(1+t^{-1})E_{\rm EF}.
\]

Define

\[
\mathcal B_t(\Lambda,E_{\rm EF},E_{\rm src})
=
(1+t)\bigl(\Lambda^{-1}\Theta_0^-+E_{\rm src}\bigr)
+
(1+t^{-1})E_{\rm EF}.
\]

A repair is proof-strengthening when it decreases \(\mathcal B_t\) in Loewner order.

## Main theorem

If

\[
\Lambda'\ge\Lambda,
\qquad
E_{\rm EF}'\preceq E_{\rm EF},
\qquad
E_{\rm src}'\preceq E_{\rm src},
\]

then for every fixed \(t>0\),

\[
\boxed{
\mathcal B_t(\Lambda',E_{\rm EF}',E_{\rm src}')
\preceq
\mathcal B_t(\Lambda,E_{\rm EF},E_{\rm src}).
}
\]

So the true proof-strengthening repairs are:

1. reduce explicit-formula domination defect \(E_{\rm EF}\);
2. reduce source/promotion defect \(E_{\rm src}\);
3. increase full anti-invariant character-frame coercivity \(\Lambda\).

## Optimized bound

If

\[
a=\operatorname{tr}(\Lambda^{-1}\Theta_0^-+E_{\rm src}),
\qquad
b=\operatorname{tr}E_{\rm EF},
\]

then

\[
\inf_{t>0}\operatorname{tr}\mathcal B_t
=
(\sqrt a+\sqrt b)^2.
\]

This is the clean scalar obstruction budget when one wants a single number.

## Repair classification

| obstruction | proof-strengthening repair | weaker/non-proof repair |
|---|---|---|
| EF domination defect | lower \(E_{\rm EF}\) by completed contractive feature map | trace equality or formal term addition |
| character-frame hole | add sources increasing lower frame \(\Lambda\) | invariant-only or trace-only source |
| bounded coercivity | strict extension with \(\Lambda\uparrow\) | finite source only |
| null-mode failure | lawful quotient/annihilation record | hiding visible displacement |
| visibility failure | extend ledger truthfully | may increase obstruction |
| promotion/tail defect | reduce tail defect probe-wise | global norm closeness only |
| scope failure | explicit nonclaim/gating | pretending restricted proof is full proof |

## Important distinction

Null-mode, visibility, and scope repairs are not ordinary budget-decrease moves.

- Null repair can make a claim legal rather than undefined.
- Visibility repair may increase \(\mathsf A_Z\), because it reveals previously hidden displacement.
- Scope/gating repair can make a restricted claim true, but it does not prove full zero confinement.

## Finite checks

The finite checks were only PSD algebra sanity checks, not Six Birds simulations.

- 80 monotone repair trials all had positive Loewner budget decrease.
- The smallest observed minimum eigenvalue of old-minus-new budget was about \(3.65\times10^{-2}\).
- The optimized \(t\)-formula matched grid minimization to max relative error about \(1.1\times10^{-6}\).
- Character-frame repair showed the budget collapses only when the missing anti-invariant character direction is covered.

## Layman interpretation

A failed RH-facing anti-localization proof now has a repair checklist.

Not every repair is equal:

- adding a missing gamma/pole/tail feature helps only if it lowers the residual defect;
- adding character sources helps only if they cover the missing anti-invariant direction;
- quotienting or gating may narrow the claim rather than prove RH-style confinement;
- exposing hidden zeros may make the obstruction larger, but more honest.

The point is to prevent fake repairs. A repair must either reduce the same-sector budget or explicitly record a weaker claim.

## Bottom line

Step 40 adds the third part of the root-composite route:

\[
\text{forward theorem}
+
\text{obstruction ledger}
+
\boxed{\text{repair calculus}}.
\]

A proof can now say not just “this gate failed,” but “this is the lawful repair move, and here is whether it actually strengthens the confinement budget.”
