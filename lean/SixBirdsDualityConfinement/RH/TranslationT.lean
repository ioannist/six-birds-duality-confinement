import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger

/-!
# RH paper — `TranslationT`

Theorem T for the typed zero ledger: vanishing of the anti-invariant zero ledger
is equivalent to every typed nontrivial zero lying on the critical line.
-/

namespace SixBirdsDualityConfinement.RH.TranslationT

universe u v w

/--
Forward direction of Theorem T: if the anti-invariant zero ledger
vanishes, then every typed nontrivial zero lies on the critical line.
-/
theorem translationTForward
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w} Z) :
    A.A_Z = A.zero → ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half := by
  exact A.sum_zero_iff_on_line.mp

/--
Reverse direction of Theorem T: if every typed nontrivial zero lies on
the critical line, then the anti-invariant zero ledger vanishes.
-/
theorem translationTReverse
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w} Z) :
    (∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half) → A.A_Z = A.zero := by
  exact A.sum_zero_iff_on_line.mpr

/--
Theorem T: vanishing of the anti-invariant zero ledger is equivalent
to the RH ledger statement that every typed nontrivial zero has
`Re(rho) = 1 / 2`.
-/
theorem translationT
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w} Z) :
    A.A_Z = A.zero ↔
      ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half :=
  Iff.intro (translationTForward A) (translationTReverse A)

end SixBirdsDualityConfinement.RH.TranslationT
