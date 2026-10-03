import SixBirdsDualityConfinement.RH.ActualInvolution

/-!
AOR-style reserve calibration for actual exhaustive zero windows. A
nonnegative reserve paying each complete window charge can only exist
when the persistent displacement charge vanishes. The theorem is a
no-go control for using a bare reserve as the shared closure premise;
it does not exclude a different analytic operation with a different bill.
-/

noncomputable section
open scoped InnerProduct InnerProductSpace

namespace SixBirdsDualityConfinement.RH.ReservePaymentNoGo

open ClassicalZeroLedger FiniteZeroWindows
open SixBirdsNeedles.XiCore

/-- The full XI payment on the actual displacement state. Its native and
residual parts depend on the probe, while their complete sum does not. -/
def completeWindowCharge
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F]
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero)
    (L : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] F) : ℝ :=
  RCLike.re (inner ℝ (displacementVector m W)
    ((auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L ∘L
      auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L ∘L
      (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)† +
      auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)
      (displacementVector m W)))

theorem completeWindowCharge_eq_windowEnergy
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F]
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero)
    (L : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] F) :
    completeWindowCharge m W L = windowEnergy m W :=
  window_complete_currency_eq_windowEnergy m W L

/-- A separate nonnegative stock pays the full charge at every window. -/
def WindowReservePayment (m : NontrivialZero → ℕ)
    (W : ℕ → Finset NontrivialZero) : Prop :=
  ∃ reserve : ℕ → ℝ, (∀ n, 0 ≤ reserve n) ∧
    ∀ n, windowEnergy m (W n) ≤ reserve n - reserve (n + 1)

theorem summable_of_windowReservePayment
    (m : NontrivialZero → ℕ) (W : ℕ → Finset NontrivialZero)
    (hpay : WindowReservePayment m W) :
    Summable (fun n => windowEnergy m (W n)) := by
  obtain ⟨reserve, hnonneg, hprice⟩ := hpay
  have htel (N : ℕ) :
      ∑ n ∈ Finset.range N, (reserve n - reserve (n + 1)) =
        reserve 0 - reserve N := by
    induction N with
    | zero => simp
    | succ N ih =>
        rw [Finset.sum_range_succ, ih]
        ring
  have hbound (N : ℕ) :
      ∑ n ∈ Finset.range N, windowEnergy m (W n) ≤ reserve 0 := by
    calc
      _ ≤ ∑ n ∈ Finset.range N, (reserve n - reserve (n + 1)) :=
        Finset.sum_le_sum fun n _ => hprice n
      _ = reserve 0 - reserve N := htel N
      _ ≤ reserve 0 := sub_le_self _ (hnonneg N)
  apply summable_of_sum_range_le
  · intro n
    unfold windowEnergy
    exact Finset.sum_nonneg fun ρ _ => term_nonneg m ρ
  · exact hbound

/-- For any exhaustive actual-zero windows, a reserve paying their
complete repeated charges is precisely RH-strength. -/
theorem windowReservePayment_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : ℕ → Finset NontrivialZero) (hcover : EventuallyCovered W) :
    WindowReservePayment m W ↔ CriticalStripRH := by
  constructor
  · intro hpay
    exact (summable_windowEnergy_iff_criticalStripRH m hm W hcover).mp
      (summable_of_windowReservePayment m W hpay)
  · intro hRH
    refine ⟨fun _ => 0, fun _ => le_rfl, ?_⟩
    intro n
    have hz : windowEnergy m (W n) = 0 :=
      (windowEnergy_eq_zero_iff m hm (W n)).mpr (by
        intro ρ _
        exact sub_eq_zero.mpr (hRH ρ.val
          ((completed_zero_iff_zeta_zero_of_re_pos ρ.val
            ρ.property.2.1).mp ρ.property.1)
          ρ.property.2.1 ρ.property.2.2))
    simp [hz]

/-- A reserve paying the actual decoded-native-plus-residual XI charge
is RH-strength for *every* choice of native probes. -/
theorem completeCurrencyReservePayment_iff_criticalStripRH
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F]
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : ℕ → Finset NontrivialZero) (hcover : EventuallyCovered W)
    (L : ∀ n, EuclideanSpace ℝ {ρ // ρ ∈ W n} →L[ℝ] F) :
    (∃ reserve : ℕ → ℝ, (∀ n, 0 ≤ reserve n) ∧
      ∀ n, completeWindowCharge m (W n) (L n) ≤
        reserve n - reserve (n + 1)) ↔ CriticalStripRH := by
  simp_rw [completeWindowCharge_eq_windowEnergy]
  exact windowReservePayment_iff_criticalStripRH m hm W hcover

end SixBirdsDualityConfinement.RH.ReservePaymentNoGo
