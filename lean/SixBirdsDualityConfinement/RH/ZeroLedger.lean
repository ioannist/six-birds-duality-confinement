import SixBirdsDualityConfinement.RH.Involution

/-!
RH paper — module ZeroLedger.

Stub. Populated by codex during Phase G per the queue at
`formalization/traceability/queue_rh.csv`.
-/

namespace SixBirdsDualityConfinement.RH.ZeroLedger

universe u v w

/--
The nontrivial zero ledger `Z_zeta^nt` for the completed zeta input.

The completed zeta function `Lambda_zeta` and its zero predicate are
external typed data.  The ledger carrier `Z_zeta_nt` is finite through
the exhaustive `support` list, each ledger entry maps to a typed
complex point in the critical strip `0 < Re(rho) < 1`, and each entry
has a positive integer multiplicity `m_rho`.  The measure `mu_L` is
recorded at singleton entries by `mu_L({rho}) = m_rho`.
-/
structure NontrivialZeroLedger
    (R : Involution.RealCoordinate.{u}) where
  LambdaValue : Type w
  Lambda_zeta : Involution.Complex R → LambdaValue
  IsZero : LambdaValue → Prop
  Z_zeta_nt : Type v
  rho : Z_zeta_nt → Involution.Complex R
  support : List Z_zeta_nt
  support_complete : ∀ ρ : Z_zeta_nt, ρ ∈ support
  lt : R.Real → R.Real → Prop
  one : R.Real
  in_critical_strip :
    ∀ ρ : Z_zeta_nt, lt R.zero (rho ρ).re ∧ lt (rho ρ).re one
  lambda_vanishes :
    ∀ ρ : Z_zeta_nt, IsZero (Lambda_zeta (rho ρ))
  m_rho : Z_zeta_nt → Nat
  m_rho_positive : ∀ ρ : Z_zeta_nt, m_rho ρ > 0
  mu_L : Z_zeta_nt → Nat
  mu_L_singleton : ∀ ρ : Z_zeta_nt, mu_L ρ = m_rho ρ

end SixBirdsDualityConfinement.RH.ZeroLedger
