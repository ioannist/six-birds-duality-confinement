import SixBirdsDualityConfinement.DualityConfinement.MasterTheorem
import SixBirdsDualityConfinement.RH.SatSelShell
import SixBirdsDualityConfinement.RH.TranslationT

/-!
# RH paper — `DCMasterApplied`

Conditional bridge from the Duality-Confinement fixed-locus theorem to the
typed `SatSelShell` interface. The DC apparatus is supplied as parameters
together with explicit bridge propositions (`same_readout`,
`visible_zero_of_ae`, and the zero-object map) that connect the abstract DC conclusion to the shell's
`A_Z` ledger. The zero-ledger equality is derived from those bridges:
this theorem combines them with `MasterTheorem.masterTheoremFixedLocus` to conclude
`S.A_Z.A_Z = S.A_Z.zero`.
-/

namespace SixBirdsDualityConfinement.RH.DCMasterApplied

open Filter
open scoped Topology

universe u v w q x y z cone trace scale

/-- The supplied faithful readout carries fixedness of a represented DC
object to fixedness under the shell's functional-equation involution.
This is a one-way fixed-locus bridge, not an identification of the two
involutions or their entire carriers. -/
theorem dcFixed_implies_shellFixed
    {R : Involution.RealCoordinate.{u}}
    (S : SatSelShell.SatSelShell R)
    {ledger :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger.{x, y, z}}
    (sep :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout.{x, y, z, scale}
        ledger)
    (A :
      _root_.SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger.{x, y, z, cone, trace}
        ledger)
    (same_readout : ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (zero_object : S.Z_nt.Z_zeta_nt → ledger.X)
    (zero_object_visible :
      ∀ ρ : S.Z_nt.Z_zeta_nt, zero_object ρ ∈ ledger.mu_support)
    (encode : R.Real → ledger.Y)
    (encode_faithful :
      ∀ r : R.Real, encode r = sep.zero_Y → r = R.zero)
    (readout_formula :
      ∀ ρ : S.Z_nt.Z_zeta_nt,
        A.psi_minus (zero_object ρ) =
          encode (R.sub (S.Z_nt.rho ρ).re R.half))
    (ρ : S.Z_nt.Z_zeta_nt)
    (hfixed : ledger.J (zero_object ρ) = zero_object ρ) :
    S.J_L.J_L (S.Z_nt.rho ρ) = S.Z_nt.rho ρ := by
  have hx : zero_object ρ ∈ ledger.mu_support := zero_object_visible ρ
  have hsep : sep.psi_minus (zero_object ρ) = sep.zero_Y :=
    (sep.separates_fixed_locus_on_visible (zero_object ρ) hx).mpr hfixed
  have hreadout : A.psi_minus (zero_object ρ) = sep.zero_Y := by
    rw [same_readout]
    exact hsep
  rw [readout_formula ρ] at hreadout
  have hre : (S.Z_nt.rho ρ).re = R.half :=
    (R.sub_half_eq_zero_iff _).mp (encode_faithful _ hreadout)
  exact (S.J_L.fixed_locus _).mpr hre

/--
Typed bridge: the fixed-locus consequence of the Duality-Confinement
master theorem, fed through user-supplied bridge hypotheses,
yields `S.A_Z.A_Z = S.A_Z.zero` on the saturated Selberg shell `S`. The DC
apparatus parameters are supplied as bridge data, not derived from the shell.
-/
theorem dcMasterApplied
    {R : Involution.RealCoordinate.{u}}
    (S : SatSelShell.SatSelShell R)
    {ledger :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger.{x, y, z}}
    (sep :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout.{x, y, z, scale}
        ledger)
    (A :
      _root_.SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger.{x, y, z, cone, trace}
        ledger)
    (same_readout :
      ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (zero_object : S.Z_nt.Z_zeta_nt → ledger.X)
    (zero_object_visible :
      ∀ ρ : S.Z_nt.Z_zeta_nt, zero_object ρ ∈ ledger.mu_support)
    (encode : R.Real → ledger.Y)
    (encode_faithful :
      ∀ r : R.Real, encode r = sep.zero_Y → r = R.zero)
    (readout_formula :
      ∀ ρ : S.Z_nt.Z_zeta_nt,
        A.psi_minus (zero_object ρ) =
          encode (R.sub (S.Z_nt.rho ρ).re R.half))
    (B_n : Nat → A.Cone)
    (domination_records :
      ∀ n : Nat, A.preceq A.A_X (B_n n))
    (B_n_positive : ∀ n : Nat, A.Positive (B_n n))
    (tr_B_n_tends_zero : Prop)
    (h_tr_B_n_tends_zero : tr_B_n_tends_zero)
    (TraceNonnegative : A.TraceValue → Prop)
    (positive_trace_nonnegative :
      ∀ C : A.Cone, A.Positive C → TraceNonnegative (A.tr C))
    (TraceZero : A.TraceValue)
    (squeeze_trace_zero :
      TraceNonnegative (A.tr A.A_X) →
        (∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n))) →
          (∀ n : Nat, A.Positive (B_n n)) →
            tr_B_n_tends_zero →
              A.tr A.A_X = TraceZero)
    (trace_zero_positive_zero :
      A.tr A.A_X = TraceZero → A.A_X = A.zero) :
    S.A_Z.A_Z = S.A_Z.zero := by
  have hfixed : ∀ x : ledger.X, x ∈ ledger.mu_support → ledger.J x = x :=
    _root_.SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheoremFixedLocus
      sep A same_readout visible_zero_of_ae B_n domination_records
      B_n_positive tr_B_n_tends_zero h_tr_B_n_tends_zero
      TraceNonnegative positive_trace_nonnegative TraceZero
      squeeze_trace_zero trace_zero_positive_zero
  apply TranslationT.translationTReverse S.A_Z
  intro ρ
  have hx : zero_object ρ ∈ ledger.mu_support := zero_object_visible ρ
  have hShellFixed :
      S.J_L.J_L (S.Z_nt.rho ρ) = S.Z_nt.rho ρ :=
    dcFixed_implies_shellFixed S sep A same_readout zero_object
      zero_object_visible encode encode_faithful readout_formula ρ
      (hfixed (zero_object ρ) hx)
  exact (S.J_L.fixed_locus _).mp hShellFixed

/-- The same bridge with an actual real trace limit. This theorem proves the
scalar squeeze through the generic DC real-trace result rather than taking a
squeeze rule as an additional hypothesis. -/
theorem dcMasterAppliedRealTrace
    {R : Involution.RealCoordinate.{u}}
    (S : SatSelShell.SatSelShell R)
    {ledger :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger.{x, y, z}}
    (sep :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout.{x, y, z, scale}
        ledger)
    (A :
      _root_.SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger.{x, y, z, cone, trace}
        ledger)
    (same_readout : ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (zero_object : S.Z_nt.Z_zeta_nt → ledger.X)
    (zero_object_visible :
      ∀ ρ : S.Z_nt.Z_zeta_nt, zero_object ρ ∈ ledger.mu_support)
    (encode : R.Real → ledger.Y)
    (encode_faithful :
      ∀ r : R.Real, encode r = sep.zero_Y → r = R.zero)
    (readout_formula :
      ∀ ρ : S.Z_nt.Z_zeta_nt,
        A.psi_minus (zero_object ρ) =
          encode (R.sub (S.Z_nt.rho ρ).re R.half))
    (B_n : Nat → A.Cone)
    (domination_records : ∀ n : Nat, A.preceq A.A_X (B_n n))
    (traceReal : A.TraceValue → ℝ)
    (traceReal_mono :
      ∀ a b : A.TraceValue, A.TraceLE a b → traceReal a ≤ traceReal b)
    (traceReal_nonneg :
      ∀ C : A.Cone, A.Positive C → 0 ≤ traceReal (A.tr C))
    (trace_decay : Tendsto (fun n => traceReal (A.tr (B_n n))) atTop (𝓝 0))
    (traceReal_zero_reflect :
      ∀ t : A.TraceValue, traceReal t = 0 → t = A.tr A.zero)
    (trace_zero_faithful :
      A.tr A.A_X = A.tr A.zero → A.A_X = A.zero) :
    S.A_Z.A_Z = S.A_Z.zero := by
  have hfixed :=
    _root_.SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheoremFixedLocusRealTrace
      sep A same_readout visible_zero_of_ae B_n domination_records
      traceReal traceReal_mono traceReal_nonneg trace_decay
      traceReal_zero_reflect trace_zero_faithful
  apply TranslationT.translationTReverse S.A_Z
  intro ρ
  have hShellFixed :=
    dcFixed_implies_shellFixed S sep A same_readout zero_object
      zero_object_visible encode encode_faithful readout_formula ρ
      (hfixed (zero_object ρ) (zero_object_visible ρ))
  exact (S.J_L.fixed_locus _).mp hShellFixed

end SixBirdsDualityConfinement.RH.DCMasterApplied
