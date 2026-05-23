# six-birds-duality-confinement

Repo for two papers in the Six Birds series:

1. **Duality Confinement** — anchor proposal:
   `anti_loc/paper_proposal_self_dual_trace_confinement.md`
2. **Riemann Hypothesis (RH) via SDTC + Selberg** — anchor proposal:
   `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`

The two axes share the vendored Foundations I/II/III Lean tracks and
the writing-side terminology/macros surface; per-axis paper sources,
Lean modules, and per-axis manifests/queues live under their own
subdirectories.

## Status

Scaffolding only. No math has been extracted, mechanized, or drafted.
See `PLAN_mechanization.md` for the phased plan.

## Layout

```
anti_loc/
  paper_proposal_self_dual_trace_confinement.md   # Paper 1 anchor
  paper_proposal_rh_via_sdtc_selberg.md           # Paper 2 anchor
  thread_rh/                                      # RH cascade (steps + manager log)
  extracted_math/                                 # Phase A output target

paper/
  duality_confinement/    # Paper 1 LaTeX (from paper-template)
  rh/                     # Paper 2 LaTeX (from paper-template)
  notation_and_terminology.md  # Shared notation governance (stub)
  references.bib               # Shared Tsiokos-only bibliography
  writing-plan.md              # Drafting-arc runbook (stub)

lean/
  lakefile.toml                                # SixBirdsDualityConfinement
  lean-toolchain                               # leanprover/lean4:v4.28.0
  SixBirdsDualityConfinement/
    ImportedFoundations.lean                   # F1/F2/F3 drift canary
    FoundationsICompat.lean                    # F1 alias surface
    Terminology.lean                           # F2/F3 alias surface
    DualityConfinement.lean                    # axis-1 umbrella (empty)
    RH.lean                                    # axis-2 umbrella (empty)
    DualityConfinement/                        # per-section modules (empty)
    RH/                                        # per-section modules (empty)
  manifests/                                   # schema-only stubs

vendor/foundations/
  six-birds-theory/         # Foundations I (locally adapted, no mathlib)
  six-birds-foundations-ii/ # Foundations II (canonical)
  six-birds-foundations-iii/# Foundations III (prepublication snapshot)

formalization/
  inventory/                # paper inventories + boundary + foundations cross-walk
  traceability/             # per-axis mechanization queues

scripts/                    # python validators + paper_lint.sh
Makefile                    # paper-build / paper-preflight / paper-clean
```

## Build (when ready)

```bash
# Lean
cd lean && lake build

# Papers
make paper-build
make paper-preflight     # also runs validator chain
```

## Workflow

Phased per `PLAN_mechanization.md`:
extract math from `anti_loc/thread_rh/steps/` → consolidate per axis →
audit → mechanize one subsection per codex dispatch → draft papers.

Drafting is downstream of mechanization, not a prerequisite to it.
