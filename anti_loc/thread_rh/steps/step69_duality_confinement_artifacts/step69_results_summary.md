# Step 69: General Duality-Confinement Membrane Theorem

This step lifts the RH-specific fixed-line work into the general formed-layer membrane framework.

## Main theorem

Let `(X,J)` be a visible object/root/defect ledger with an involution, and let

```math
\psi_- = P_-\psi
```

be a separating anti-invariant readout into a response space. Define the anti-invariant object ledger

```math
\mathsf A_X=\int_X \psi_-(x)\psi_-(x)^*\,d\mu(x).
```

If the completed carrier supplies shrinking domination records

```math
\mathsf A_X\preceq B_n,
\qquad \operatorname{tr}B_n\to0,
```

then

```math
\mathsf A_X=0.
```

If `psi_-` separates the fixed locus,

```math
\psi_-(x)=0 \iff x\in\operatorname{Fix}(J),
```

then all visible object mass is confined to `Fix(J)`.

## Exhaustive moving-ledger version

A moving finite ledger can prove exact confinement only with a tail/exhaustivity record:

```math
\mathsf A_X\preceq \iota_n\mathsf A_{X,n}\iota_n^*+T_n,
```

```math
\mathsf A_{X,n}\preceq B_n,
```

and

```math
\operatorname{tr}(\iota_nB_n\iota_n^*)+\operatorname{tr}T_n\to0.
```

Without this bridge, the status is `moving_ledger_support_only`.

## Contractive bridge

If

```math
\mathsf A_X=V^*V,
\qquad
\mathsf K^-=W^*W,
```

then

```math
\mathsf A_X\preceq\mathsf K^-
```

is equivalent, by Douglas factorization, to a contraction

```math
V=TW,
\qquad \|T\|\le1.
```

So the bridge is not trace equality; it is contractive domination.

## Defected obstruction budget

For budgets of the form

```math
B_n(t)=(1+t)(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n})+(1+t^{-1})E_{{\rm br},n},
```

with

```math
 a_n=\operatorname{tr}(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n}),
\qquad
 b_n=\operatorname{tr}E_{{\rm br},n},
```

we have

```math
\inf_{t>0}\operatorname{tr}B_n(t)=(\sqrt{a_n}+\sqrt{b_n})^2.
```

Thus exact confinement follows when `a_n -> 0`, `b_n -> 0`, and the ledger is fixed or exhaustive.

## RH specialization

For RH:

```math
J(s)=1-\overline{s},
\qquad
\operatorname{Fix}(J)=\{s:\operatorname{Re}(s)=1/2\}.
```

A separating readout is

```math
\psi_-(s)=\operatorname{Re}(s)-1/2.
```

RH becomes one specialization of the general theorem, requiring:

1. a fixed or exhaustive completed zero ledger;
2. completed explicit-formula domination;
3. anti-invariant budget collapse;
4. vanishing bridge/source/tail defects;
5. no trace-shadow or public-shadow overread.

## Nonclaim

This does not prove RH. It extracts the general duality-confinement membrane theorem that the RH path instantiated.
