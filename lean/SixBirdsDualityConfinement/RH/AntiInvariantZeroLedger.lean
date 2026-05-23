import SixBirdsDualityConfinement.RH.ZeroLedger

/-!
# RH paper — `AntiInvariantZeroLedger`

Multiplicity-weighted anti-invariant zero ledger `A_Z(zeta)` over the typed
zero ledger, with the abstract scalar and positivity interfaces used by the
translation theorem.
-/

namespace SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger

universe u v w q

/--
The anti-invariant zero ledger
`A_Z(zeta) = Sigma_{rho in Z_zeta^nt} m_rho * |Re(rho) - 1/2|^2`.

The scalar arithmetic is kept typed and abstract.  The finite sum is
over the support list carried by the nontrivial-zero ledger, and the
term formula records the multiplicity-weighted squared centered real
part.  The nonnegativity and zero-term interfaces are construction
data for the later translation theorem.
-/
structure AntiInvariantZeroLedger
    {R : Involution.RealCoordinate.{u}}
    (Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R) where
  Scalar : Type q
  zero : Scalar
  add : Scalar → Scalar → Scalar
  le : Scalar → Scalar → Prop
  abs_sq : R.Real → Scalar
  nat_mul : Nat → Scalar → Scalar
  term : Z.Z_zeta_nt → Scalar
  term_formula :
    ∀ ρ : Z.Z_zeta_nt,
      term ρ = nat_mul (Z.m_rho ρ) (abs_sq (R.sub (Z.rho ρ).re R.half))
  finite_sum : List Z.Z_zeta_nt → Scalar
  finite_sum_empty : finite_sum [] = zero
  finite_sum_cons :
    ∀ (ρ : Z.Z_zeta_nt) (tail : List Z.Z_zeta_nt),
      finite_sum (ρ :: tail) = add (term ρ) (finite_sum tail)
  A_Z : Scalar
  A_Z_formula : A_Z = finite_sum Z.support
  term_nonnegative : ∀ ρ : Z.Z_zeta_nt, le zero (term ρ)
  A_Z_nonnegative : le zero A_Z
  sum_zero_imp_term_zero :
    A_Z = zero → ∀ ρ : Z.Z_zeta_nt, term ρ = zero
  term_zero_imp_on_line :
    ∀ ρ : Z.Z_zeta_nt, term ρ = zero → (Z.rho ρ).re = R.half
  term_zero_of_on_line :
    ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half → term ρ = zero
  A_Z_eq_zero_of_terms_zero :
    (∀ ρ : Z.Z_zeta_nt, term ρ = zero) → A_Z = zero

end SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger
