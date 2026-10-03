import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore

/-! Optimized real scalar budgets, including the non-attained boundary cases. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteBudget
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore

/-- The two-component defect budget. -/
noncomputable def scalarBudget (a b t : ℝ) : ℝ := (1 + t) * a + (1 + t⁻¹) * b

noncomputable def optimalBudget (a b : ℝ) : ℝ := (Real.sqrt a + Real.sqrt b) ^ 2

theorem scalarBudget_lower {a b t : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (ht : 0 < t) :
    optimalBudget a b ≤ scalarBudget a b t := by
  have h := sq_nonneg (Real.sqrt a * t - Real.sqrt b)
  have ha' := Real.sq_sqrt ha
  have hb' := Real.sq_sqrt hb
  apply (mul_le_mul_iff_right₀ ht).mp
  dsimp [optimalBudget, scalarBudget]
  have hi : t⁻¹ * t = 1 := inv_mul_cancel₀ ht.ne'
  generalize Real.sqrt a = u at *
  generalize Real.sqrt b = v at *
  rw [← ha', ← hb'] at *
  nlinarith

theorem scalarBudget_attained {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    scalarBudget a b (Real.sqrt (b / a)) = optimalBudget a b := by
  have hsa : 0 < Real.sqrt a := Real.sqrt_pos.2 ha
  have hsb : 0 < Real.sqrt b := Real.sqrt_pos.2 hb
  have ha' := Real.sq_sqrt ha.le
  have hb' := Real.sq_sqrt hb.le
  rw [Real.sqrt_div hb.le]
  dsimp [scalarBudget, optimalBudget]
  field_simp
  nlinarith

/-- The infimum need not be attained when either component vanishes. -/
theorem scalarBudget_isGLB {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    IsGLB (Set.range (fun t : {t : ℝ // 0 < t} => scalarBudget a b t))
      (optimalBudget a b) := by
  constructor
  · rintro _ ⟨t, rfl⟩
    exact scalarBudget_lower ha hb t.property
  · intro c hc
    by_cases haz : a = 0
    · subst a
      have ho : optimalBudget 0 b = b := by simp [optimalBudget, Real.sq_sqrt hb]
      rw [ho]
      by_contra hn
      have hcb : 0 < c - b := sub_pos.mpr (lt_of_not_ge hn)
      let t : ℝ := (b + 1) / (c - b)
      have ht : 0 < t := div_pos (by linarith) hcb
      have hh := hc (Set.mem_range_self (⟨t, ht⟩ : {t : ℝ // 0 < t}))
      change c ≤ scalarBudget 0 b t at hh
      have hi : t⁻¹ = (c - b) / (b + 1) := by simp [t]
      simp only [scalarBudget, mul_zero, zero_add, hi] at hh
      have he : (c - b) / (b + 1) * (b + 1) = c - b :=
        div_mul_cancel₀ _ (by linarith)
      nlinarith
    · have hap : 0 < a := lt_of_le_of_ne ha (Ne.symm haz)
      by_cases hbz : b = 0
      · subst b
        have ho : optimalBudget a 0 = a := by simp [optimalBudget, Real.sq_sqrt ha]
        rw [ho]
        by_contra hn
        have hca : 0 < c - a := sub_pos.mpr (lt_of_not_ge hn)
        let t : ℝ := (c - a) / (2 * a)
        have ht : 0 < t := div_pos hca (by positivity)
        have hh := hc (Set.mem_range_self (⟨t, ht⟩ : {t : ℝ // 0 < t}))
        change c ≤ scalarBudget a 0 t at hh
        simp only [scalarBudget, mul_zero, add_zero] at hh
        have he : t * (2 * a) = c - a := div_mul_cancel₀ _ (by positivity)
        nlinarith
      · have hbp : 0 < b := lt_of_le_of_ne hb (Ne.symm hbz)
        have ht : 0 < Real.sqrt (b / a) := Real.sqrt_pos.mpr (div_pos hbp hap)
        have hh := hc (Set.mem_range_self
          (⟨Real.sqrt (b / a), ht⟩ : {t : ℝ // 0 < t}))
        simpa only [scalarBudget_attained hap hbp] using hh

/-- Trace optimization of a family of genuine positive operator bounds. -/
theorem optimized_operator_budget {Y : Type*} [NormedAddCommGroup Y]
    [InnerProductSpace ℝ Y] [FiniteDimensional ℝ Y]
    (A K E : Y →L[ℝ] Y) (hK : K.IsPositive) (hE : E.IsPositive)
    (hdom : ∀ t : ℝ, 0 < t → ((1 + t) • K + (1 + t⁻¹) • E - A).IsPositive) :
    opTrace A ≤ (Real.sqrt (opTrace K) + Real.sqrt (opTrace E)) ^ 2 := by
  apply (scalarBudget_isGLB (positive_trace_nonneg hK) (positive_trace_nonneg hE)).2
  rintro _ ⟨t, rfl⟩
  have hh := trace_mono (hdom t t.property)
  simpa [scalarBudget] using hh

/-- Vanishing component traces force a positive operator under all scalar budgets to vanish. -/
theorem budget_sequence_zero {Y : Type*} [NormedAddCommGroup Y]
    [InnerProductSpace ℝ Y] [FiniteDimensional ℝ Y]
    (A : Y →L[ℝ] Y) (hA : A.IsPositive) (K E : ℕ → Y →L[ℝ] Y)
    (hK : ∀ n, (K n).IsPositive) (hE : ∀ n, (E n).IsPositive)
    (hdom : ∀ n (t : ℝ), 0 < t → ((1 + t) • K n + (1 + t⁻¹) • E n - A).IsPositive)
    (hKlim : Filter.Tendsto (fun n => opTrace (K n)) Filter.atTop (nhds 0))
    (hElim : Filter.Tendsto (fun n => opTrace (E n)) Filter.atTop (nhds 0)) : A = 0 := by
  have hk := (Real.continuous_sqrt.tendsto (0 : ℝ)).comp hKlim
  have he := (Real.continuous_sqrt.tendsto (0 : ℝ)).comp hElim
  have hlim : Filter.Tendsto
      (fun n => (Real.sqrt (opTrace (K n)) + Real.sqrt (opTrace (E n))) ^ 2)
      Filter.atTop (nhds 0) := by
    simpa using (hk.add he).pow 2
  apply positive_trace_zero hA
  exact le_antisymm
    (le_of_tendsto_of_tendsto tendsto_const_nhds hlim
      (Filter.Eventually.of_forall fun n =>
        optimized_operator_budget A (K n) (E n) (hK n) (hE n) (hdom n)))
    (positive_trace_nonneg hA)

end SixBirdsDualityConfinement.DualityConfinement.ConcreteBudget
