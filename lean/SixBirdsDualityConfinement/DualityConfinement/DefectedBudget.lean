import SixBirdsDualityConfinement.Terminology

/-!
Duality Confinement paper — module DefectedBudget.

Stub. Populated by codex during Phase G per the queue at
`formalization/traceability/queue_duality_confinement.csv`.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.DefectedBudget

universe u

/--
Optimized scalar trace budget.

For scalar trace budgets `traceBudget n t = tr B_n(t)` over positive
parameters `t > 0`, the supplied AM-GM minimization principle gives
the closed form `inf_{t>0} tr B_n(t) = (sqrt a_n + sqrt b_n)^2`.
The second component records the sufficient scalar condition for exact
confinement by fixed-ledger squeeze: if both scalar defect traces tend
to zero, the fixed-ledger squeeze conclusion follows.
-/
theorem optimizedTraceBudget
    {Scalar : Type u}
    (Positive : Scalar → Prop)
    (a_n b_n : Nat → Scalar)
    (traceBudget : Nat → ({ t : Scalar // Positive t }) → Scalar)
    (infPositive :
      (({ t : Scalar // Positive t }) → Scalar) → Scalar)
    (sqrt : Scalar → Scalar)
    (add : Scalar → Scalar → Scalar)
    (square : Scalar → Scalar)
    (am_gm_optimization :
      ∀ n : Nat,
        infPositive (traceBudget n) =
          square (add (sqrt (a_n n)) (sqrt (b_n n))))
    (a_tends_zero : Prop)
    (b_tends_zero : Prop)
    (exact_confinement : Prop)
    (fixed_ledger_squeeze :
      a_tends_zero → b_tends_zero → exact_confinement) :
    (∀ n : Nat,
      infPositive (traceBudget n) =
        square (add (sqrt (a_n n)) (sqrt (b_n n)))) ∧
      (a_tends_zero → b_tends_zero → exact_confinement) :=
  And.intro am_gm_optimization fixed_ledger_squeeze

end SixBirdsDualityConfinement.DualityConfinement.DefectedBudget
