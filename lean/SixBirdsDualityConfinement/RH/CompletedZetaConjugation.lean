import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Analysis.Calculus.FDeriv.Star
open Complex Filter
open scoped Topology

noncomputable section

namespace SixBirdsDualityConfinement.RH.CompletedZetaConjugation

private theorem gammaR_conj (s : ℂ) : Gammaℝ (star s) = star (Gammaℝ s) := by
  have hpi : ((Real.pi : ℂ)).arg ≠ Real.pi := by
    rw [Complex.arg_ofReal_of_nonneg Real.pi_pos.le]
    exact Ne.symm (ne_of_gt Real.pi_pos)
  rw [Gammaℝ_def, Gammaℝ_def, star_mul]
  conv_rhs => rw [mul_comm]
  congr 1
  · simpa only [Complex.star_def, map_neg, map_div₀, map_ofNat, Complex.conj_ofReal] using Complex.cpow_conj (Real.pi : ℂ) (-s / 2) hpi
  · simpa only [map_div₀, map_ofNat] using Complex.Gamma_conj (s / 2)

private theorem zeta_conj_right (s : ℂ) (hs : 1 < s.re) :
    riemannZeta (star s) = star (riemannZeta s) := by
  have hs' : 1 < (star s).re := by simpa using hs
  rw [zeta_eq_tsum_one_div_nat_add_one_cpow hs',
      zeta_eq_tsum_one_div_nat_add_one_cpow hs, tsum_star]
  congr 1
  funext n
  have hn : ((n + 1 : ℂ)).arg ≠ Real.pi := by
    rw [show (n + 1 : ℂ) = (((n + 1 : ℕ) : ℝ) : ℂ) by norm_cast,
      Complex.arg_ofReal_of_nonneg (Nat.cast_nonneg _)]
    exact Ne.symm (ne_of_gt Real.pi_pos)
  have hpow : (n + 1 : ℂ) ^ star s = star ((n + 1 : ℂ) ^ s) := by
    simpa only [Complex.star_def, map_add, map_one, Complex.conj_natCast] using
      Complex.cpow_conj (n + 1 : ℂ) s hn
  simpa only [one_div, Complex.star_def, map_inv₀] using congrArg (fun z : ℂ => z⁻¹) hpow

private theorem completed_eq_gamma_mul_zeta (s : ℂ) (hs : 0 < s.re) :
    completedRiemannZeta s = Gammaℝ s * riemannZeta s := by
  have hs0 : s ≠ 0 := by
    intro h
    simp [h] at hs
  rw [riemannZeta_def_of_ne_zero hs0]
  field_simp [Gammaℝ_ne_zero_of_re_pos hs]

private theorem completed_conj_right (s : ℂ) (hs : 1 < s.re) :
    completedRiemannZeta (star s) = star (completedRiemannZeta s) := by
  have hs' : 1 < (star s).re := by simpa using hs
  rw [completed_eq_gamma_mul_zeta (star s) (by linarith),
      completed_eq_gamma_mul_zeta s (by linarith),
      gammaR_conj, zeta_conj_right s hs, star_mul]
  exact mul_comm _ _

private theorem completed0_eq (s : ℂ) :
    completedRiemannZeta₀ s = completedRiemannZeta s + 1 / s + 1 / (1 - s) := by
  rw [completedRiemannZeta_eq]
  ring

private theorem completed0_conj_right (s : ℂ) (hs : 1 < s.re) :
    completedRiemannZeta₀ (star s) = star (completedRiemannZeta₀ s) := by
  rw [completed0_eq, completed0_eq, completed_conj_right s hs]
  simp only [Complex.star_def, one_div, map_add, map_inv₀, map_sub, map_one]

private theorem completed0_conj (s : ℂ) :
    completedRiemannZeta₀ (star s) = star (completedRiemannZeta₀ s) := by
  let f : ℂ → ℂ := completedRiemannZeta₀
  let g : ℂ → ℂ := star ∘ f ∘ star
  have hf : Differentiable ℂ f := differentiable_completedZeta₀
  have hg : Differentiable ℂ g := by
    intro z
    simpa [g, f] using (hf (star z)).star_star
  have hfa : AnalyticOnNhd ℂ f Set.univ :=
    Complex.analyticOnNhd_univ_iff_differentiable.mpr hf
  have hga : AnalyticOnNhd ℂ g Set.univ :=
    Complex.analyticOnNhd_univ_iff_differentiable.mpr hg
  have hlocal : f =ᶠ[𝓝 (2 : ℂ)] g := by
    have hopen : IsOpen {z : ℂ | 1 < z.re} :=
      isOpen_Ioi.preimage Complex.continuous_re
    filter_upwards [hopen.mem_nhds (by norm_num)] with z hz
    dsimp [f, g]
    simpa using (congrArg star (completed0_conj_right z hz)).symm
  have hglobal := hfa.eq_of_eventuallyEq hga hlocal
  have h := congrFun hglobal (star s)
  simpa [f, g] using h

theorem completedRiemannZeta_conj (s : ℂ) :
    completedRiemannZeta (star s) = star (completedRiemannZeta s) := by
  rw [completedRiemannZeta_eq, completedRiemannZeta_eq, completed0_conj]
  simp only [Complex.star_def, one_div, map_sub, map_inv₀, map_one]

end SixBirdsDualityConfinement.RH.CompletedZetaConjugation
