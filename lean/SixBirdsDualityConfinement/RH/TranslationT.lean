import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger

/-!
# RH paper — `TranslationT`

Theorem T for the typed zero ledger: vanishing of the anti-invariant zero ledger
is equivalent to every typed nontrivial zero lying on the critical line.
-/

namespace SixBirdsDualityConfinement.RH.TranslationT

universe u v w q

/--
Forward direction of Theorem T: if the anti-invariant zero ledger
vanishes, then every typed nontrivial zero lies on the critical line.
-/
theorem translationTForward
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w, q} Z) :
    A.A_Z = A.zero → ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half := by
  intro hA ρ
  exact A.term_zero_imp_on_line ρ (A.sum_zero_imp_term_zero hA ρ)

/--
Reverse direction of Theorem T: if every typed nontrivial zero lies on
the critical line, then the anti-invariant zero ledger vanishes.
-/
theorem translationTReverse
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w, q} Z) :
    (∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half) → A.A_Z = A.zero := by
  intro hRH
  exact A.A_Z_eq_zero_of_terms_zero
    (fun ρ => A.term_zero_of_on_line ρ (hRH ρ))

/--
Theorem T: vanishing of the anti-invariant zero ledger is equivalent
to the RH ledger statement that every typed nontrivial zero has
`Re(rho) = 1 / 2`.
-/
theorem translationT
    {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w, q} Z) :
    A.A_Z = A.zero ↔
      ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half :=
  Iff.intro (translationTForward A) (translationTReverse A)

end SixBirdsDualityConfinement.RH.TranslationT
