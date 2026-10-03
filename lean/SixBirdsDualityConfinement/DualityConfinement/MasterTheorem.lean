import SixBirdsDualityConfinement.DualityConfinement.DirectConfinement
import SixBirdsDualityConfinement.DualityConfinement.Domination
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Topology.Order.OrderClosed

/-!
# Duality Confinement paper -- `MasterTheorem`

The duality-confinement membrane theorem: a typed positive-cone
squeeze converting a vanishing-trace domination sequence into
fixed-locus confinement.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.MasterTheorem

open Filter
open scoped Topology

universe u v w z q r

/-- The analytic cone step of the membrane argument. All trace and limit
inputs are explicit; no separating readout is used in this step. -/
theorem coneZeroOfDomination
    {ledger : Involution.InvolutiveObjectLedger.{u, v, w}}
    (A : AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q} ledger)
    (B_n : Nat → A.Cone)
    (domination_records : ∀ n : Nat, A.preceq A.A_X (B_n n))
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
    A.A_X = A.zero := by
  have hTraceNonnegative : TraceNonnegative (A.tr A.A_X) :=
    positive_trace_nonnegative A.A_X A.positive_A_X
  have hTraceUpper :
      ∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n)) := by
    intro n
    exact A.trace_mono A.A_X (B_n n) (domination_records n)
  have hTraceZero : A.tr A.A_X = TraceZero :=
    squeeze_trace_zero hTraceNonnegative hTraceUpper
      B_n_positive h_tr_B_n_tends_zero
  exact trace_zero_positive_zero hTraceZero

/--
Duality-confinement membrane theorem.

The sequence `B_n` represents completed domination records
`A_X ⪯ B_n` with `B_n ⪰ 0`. The abstract proposition
`tr_B_n_tends_zero` represents `tr B_n -> 0`. The non-definitional
analytic steps are explicit hypotheses. This legacy declaration returns
only the supplied measure-reading proposition `mu_nonfixed_zero` through
`mu_zero_of_ae`; its separating readout is not load-bearing for that
component. Use `masterTheoremFixedLocus` for the pointwise geometric
conclusion, where separation is an actual proof dependency.
-/
theorem masterTheorem
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A :
      AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q}
        ledger)
    (same_readout :
      ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (mu_nonfixed_zero : Prop)
    (mu_zero_of_ae : A.psi_minus_ae_zero → mu_nonfixed_zero)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
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
    mu_nonfixed_zero := by
  have hAZero : A.A_X = A.zero :=
    coneZeroOfDomination A B_n domination_records B_n_positive
      tr_B_n_tends_zero h_tr_B_n_tends_zero TraceNonnegative
      positive_trace_nonnegative TraceZero squeeze_trace_zero
      trace_zero_positive_zero
  exact
    (DirectConfinement.separationConfinement
      sep A same_readout mu_nonfixed_zero mu_zero_of_ae
      visible_zero_of_ae hAZero).left

/-- The geometric consequence that the legacy `masterTheorem` discarded:
every visible object lies in the fixed locus. Here separation and the
readout bridge are actual proof dependencies. -/
theorem masterTheoremFixedLocus
    {ledger : Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A : AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q} ledger)
    (same_readout : ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (B_n : Nat → A.Cone)
    (domination_records : ∀ n : Nat, A.preceq A.A_X (B_n n))
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
    ∀ x : ledger.X, x ∈ ledger.mu_support → ledger.J x = x := by
  have hAZero : A.A_X = A.zero :=
    coneZeroOfDomination A B_n domination_records B_n_positive
      tr_B_n_tends_zero h_tr_B_n_tends_zero TraceNonnegative
      positive_trace_nonnegative TraceZero squeeze_trace_zero
      trace_zero_positive_zero
  have hAe : A.psi_minus_ae_zero :=
    (AntiInvariantLedger.traceIdentity A).right.mp hAZero
  intro x hx
  have hzero : A.psi_minus x = sep.zero_Y :=
    visible_zero_of_ae hAe x hx
  have hsep : sep.psi_minus x = sep.zero_Y := by
    rw [← same_readout x]
    exact hzero
  exact (sep.separates_fixed_locus_on_visible x hx).mp hsep

/-- A numerical version of the cone squeeze. The positive-cone trace laws and
faithfulness remain explicit, but the limit-to-zero step is proved for a real
trace instead of being packaged as an arbitrary squeeze hypothesis. -/
theorem coneZeroOfRealTraceDomination
    {ledger : Involution.InvolutiveObjectLedger.{u, v, w}}
    (A : AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q} ledger)
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
    A.A_X = A.zero := by
  have hle : traceReal (A.tr A.A_X) ≤ 0 :=
    le_of_tendsto_of_tendsto tendsto_const_nhds trace_decay
      (Filter.Eventually.of_forall fun n =>
        traceReal_mono _ _ (A.trace_mono A.A_X (B_n n) (domination_records n)))
  have hnonneg : 0 ≤ traceReal (A.tr A.A_X) :=
    traceReal_nonneg A.A_X A.positive_A_X
  exact trace_zero_faithful
    (traceReal_zero_reflect _ (le_antisymm hle hnonneg))

/-- The corresponding visible fixed-locus result. No ambient measure is
constructed: a measure-zero reading needs its own measure bridge. -/
theorem masterTheoremFixedLocusRealTrace
    {ledger : Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A : AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q} ledger)
    (same_readout : ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
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
    ∀ x : ledger.X, x ∈ ledger.mu_support → ledger.J x = x := by
  have hAZero := coneZeroOfRealTraceDomination A B_n domination_records
    traceReal traceReal_mono traceReal_nonneg trace_decay
    traceReal_zero_reflect trace_zero_faithful
  have hAe : A.psi_minus_ae_zero :=
    (AntiInvariantLedger.traceIdentity A).right.mp hAZero
  intro x hx
  have hzero := visible_zero_of_ae hAe x hx
  have hsep : sep.psi_minus x = sep.zero_Y := by
    rw [← same_readout x]
    exact hzero
  exact (sep.separates_fixed_locus_on_visible x hx).mp hsep

end SixBirdsDualityConfinement.DualityConfinement.MasterTheorem
