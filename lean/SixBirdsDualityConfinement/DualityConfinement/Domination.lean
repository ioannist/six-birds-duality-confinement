import SixBirdsDualityConfinement.Terminology

/-!
# Duality Confinement paper -- `Domination`

Completed-domination bridges and the typed-cone form of Douglas
factorization.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.Domination

universe u v

/--
Typed data for the Douglas factorization comparison
`A = V*V`, `K = W*W`.

The fields `order_to_factor` and `factor_to_order` are the local
mathlib-free package of the Douglas factorization content for the
chosen typed representation.
-/
structure DouglasData (Operator : Type u) where
  Factor : Type v
  A : Operator
  K : Operator
  V : Operator
  W : Operator
  preceq : Operator → Operator → Prop
  factorApply : Factor → Operator → Operator
  IsContraction : Factor → Prop
  A_eq_VstarV : Prop
  K_eq_WstarW : Prop
  order_to_factor :
    preceq A K →
      ∃ T : Factor, IsContraction T ∧ V = factorApply T W
  factor_to_order :
    (∃ T : Factor, IsContraction T ∧ V = factorApply T W) →
        preceq A K

/-- A typed witness of `A ⪯ K` for Douglas data. -/
structure Domination {Operator : Type u}
    (D : DouglasData.{u, v} Operator) where
  order : D.preceq D.A D.K

/-- A typed witness of a contractive factorization `V = T W`. -/
structure ContractiveFactor {Operator : Type u}
    (D : DouglasData.{u, v} Operator) where
  T : D.Factor
  contraction : D.IsContraction T
  factorization : D.V = D.factorApply T D.W

/--
A completed domination bridge `A_X ⪯ K_minus + E` with positive
carrier-side currency `K_minus` and positive defect `E`.

The exact case is recorded through Douglas data on the same cone:
when `E = 0`, domination and contractive factorization are equivalent.
-/
structure CompletedDominationBridge where
  Cone : Type u
  zero : Cone
  add : Cone → Cone → Cone
  preceq : Cone → Cone → Prop
  Positive : Cone → Prop
  A_X : Cone
  K_minus : Cone
  E : Cone
  K_minus_positive : Positive K_minus
  defect_positive : Positive E
  bridge : preceq A_X (add K_minus E)
  exact_data : DouglasData.{u, v} Cone
  exact_A_X : exact_data.A = A_X
  exact_K_minus : exact_data.K = K_minus
  exact_characterization :
    E = zero →
      (Nonempty (Domination exact_data) ↔
        Nonempty (ContractiveFactor exact_data))

/--
Douglas domination: for typed positive operators `A = V*V` and
`K = W*W`, domination is equivalent to the existence of a contractive
factor `T` with `V = T W`.
-/
theorem douglasDomination {Operator : Type u}
    (D : DouglasData.{u, v} Operator) :
    Nonempty (Domination D) ↔ Nonempty (ContractiveFactor D) := by
  refine Iff.intro ?_ ?_
  · intro h
    exact h.elim (fun hDom =>
      (D.order_to_factor hDom.order).elim (fun T hT =>
        Nonempty.intro
          { T := T
            contraction := hT.left
            factorization := hT.right }))
  · intro h
    exact h.elim (fun hFactor =>
      Nonempty.intro
        { order :=
            D.factor_to_order
              (Exists.intro hFactor.T
                (And.intro hFactor.contraction hFactor.factorization)) })

end SixBirdsDualityConfinement.DualityConfinement.Domination
