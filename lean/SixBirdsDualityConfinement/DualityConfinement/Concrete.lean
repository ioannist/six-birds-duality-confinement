import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
import SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
import SixBirdsDualityConfinement.DualityConfinement.ConcreteBudget
import SixBirdsDualityConfinement.DualityConfinement.ConcreteDouglas
import SixBirdsDualityConfinement.DualityConfinement.ConcreteMeasured
import SixBirdsDualityConfinement.DualityConfinement.ConcreteConverse
import SixBirdsDualityConfinement.DualityConfinement.ConcreteHilbert
import SixBirdsDualityConfinement.DualityConfinement.AbstractSqueeze

/-!
# Concrete self-dual trace confinement (DC-1)

For an isometric involution `S` and equivariant `psi`, the actual anti-invariant
readout is `r := ConcreteCore.psiMinus S psi`. The two ledger constructors are
`ConcreteFinite.finiteLedger mu r` and `ConcreteMeasured.measuredLedger mu r`. All ledger
results are stated for general readouts, hence also for this specialization.

Separation, domination and decay are explicit hypotheses. Projection laws,
positivity, trace identity and faithfulness, Markov estimates, scalar
optimization (including zero components), Douglas factorization, and ambient
exhaustive squeeze are proved from the pinned Mathlib mathematics.

The measured results allow arbitrary measures; quantitative bounds take values
in `ENNReal`. Null fixed-locus complements need no measurability hypothesis.

The audit in `review/paper-readability-pass-2026-09-30/lean-audit/ConcreteAxiomAudit.lean`
prints exact types and transitive axioms of every concrete definition and theorem;
run it with `lake env lean <path>` from `lean/` after `lake build`.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.Concrete
end SixBirdsDualityConfinement.DualityConfinement.Concrete
