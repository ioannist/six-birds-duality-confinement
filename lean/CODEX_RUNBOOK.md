# Codex operator runbook

This document is for the operator (Claude) driving the mechanization
loop. Codex is the OpenAI `codex` CLI (see
`~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/reference_codex_cli.md`
for the underlying mechanics). Claude reviews codex's output after
each turn; this runbook tells the operator what commands to run when.

Two codex sessions exist, one per paper axis:

- Duality-confinement axis: `lean/.codex_thread_id_duality_confinement`
- RH axis:                  `lean/.codex_thread_id_rh`

Each is created once (per axis kickoff) and then resumed for every
subsequent subsection turn. **Never cross-resume between axes** — each
rollout learns its paper's vocabulary; mixing contaminates.

## Prerequisites

- `codex` CLI installed (verified at `/home/ioannis/.nvm/versions/node/v22.18.0/bin/codex`).
- `lake` in `PATH` (verified at `/home/ioannis/.elan/bin/lake`).
- `jq` for extracting `thread_id` from the kickoff JSONL output.
- Working tree clean enough that codex's writes land cleanly.

## One-shot kickoff (run once per axis)

The kickoff hands codex the contract (`lean/codex_kickoff.md`)
followed by the first per-subsection prompt. The kickoff turn
produces both the first batch of Lean code *and* the thread ID we
capture for all subsequent turns.

**Bootstrap prompts must use stdin redirection.** A multi-KB bootstrap
passed as a `"$(cat …)"` argv expansion has been observed to hang
indefinitely on fresh `codex exec` calls (see
`memory/feedback_codex_bootstrap_stdin.md`). For resumes, argv is
fine.

### Duality-confinement axis

```bash
cd /home/repos/six-birds-duality-confinement

# 1. Build the combined first-turn input: kickoff + first subsection prompt.
cat lean/codex_kickoff.md > /tmp/bootstrap_duality_confinement.txt
printf '\n---\n\n' >> /tmp/bootstrap_duality_confinement.txt
python scripts/build_codex_prompt.py \
    --axis duality_confinement \
    --paper-label <first-label-from-queue_duality_confinement.csv> \
    >> /tmp/bootstrap_duality_confinement.txt

# 2. Invoke codex via stdin (argv hangs on bootstraps).
codex exec --json --skip-git-repo-check --full-auto \
    -c model_reasoning_effort='"high"' \
    < /tmp/bootstrap_duality_confinement.txt \
    2>/tmp/bootstrap_duality_confinement.stderr \
    > /tmp/bootstrap_duality_confinement.jsonl

# 3. Capture the thread_id from the first JSONL event.
head -1 /tmp/bootstrap_duality_confinement.jsonl \
    | jq -r .thread_id \
    > lean/.codex_thread_id_duality_confinement

# 4. Sanity-check the captured ID is a UUID.
grep -E '^[0-9a-f-]{36}$' lean/.codex_thread_id_duality_confinement \
    || { echo "thread_id capture failed"; exit 1; }
```

### RH axis

Identical shape, swapping `duality_confinement` → `rh` and starting
paper label:

```bash
cat lean/codex_kickoff.md > /tmp/bootstrap_rh.txt
printf '\n---\n\n' >> /tmp/bootstrap_rh.txt
python scripts/build_codex_prompt.py \
    --axis rh \
    --paper-label <first-label-from-queue_rh.csv> \
    >> /tmp/bootstrap_rh.txt

codex exec --json --skip-git-repo-check --full-auto \
    -c model_reasoning_effort='"high"' \
    < /tmp/bootstrap_rh.txt \
    2>/tmp/bootstrap_rh.stderr \
    > /tmp/bootstrap_rh.jsonl

head -1 /tmp/bootstrap_rh.jsonl \
    | jq -r .thread_id \
    > lean/.codex_thread_id_rh
```

After kickoff, immediately review the codex output (the Lean files it
edited, the manifest entries it added) using the per-subsection
review procedure below.

## Per-subsection iteration

For every subsection after the first, the workflow is the same.
Pick the next `mechanize_now` label from the axis queue and run:

```bash
AXIS=duality_confinement                      # or rh
LABEL=<next-label-from-queue_${AXIS}.csv>

# 1. Build the prompt.
python scripts/build_codex_prompt.py \
    --axis "$AXIS" \
    --paper-label "$LABEL" \
    --out /tmp/dispatch.txt

# 2. Resume the per-axis session (argv on resume is fine).
codex exec resume --json --full-auto \
    -c model_reasoning_effort='"high"' \
    "$(cat lean/.codex_thread_id_${AXIS})" \
    "$(cat /tmp/dispatch.txt)" \
    2>/tmp/dispatch.stderr \
    > /tmp/dispatch.jsonl

# 3. Review (fast path: structural + lake build).
python scripts/check_lean.py --skip-probe
```

The `--skip-probe` flag is the fast feedback path (structural checks
+ schema + `lake build`, no `lake env lean` probes). Before declaring
the subsection accepted, run the full check with probes:

```bash
python scripts/check_lean.py
```

If the full check exits zero and Claude's review accepts the Lean
content (statement fidelity, terminology alignment, idiomatic
style, at least one non-`rfl` mathematical step per theorem), the
subsection is done. Advance the queue.

If any gate fails, send a targeted fix prompt to codex *in the same
session*:

```bash
echo "Fix the following issue: <description>" > /tmp/fix.txt
codex exec resume --json --full-auto \
    -c model_reasoning_effort='"high"' \
    "$(cat lean/.codex_thread_id_${AXIS})" \
    "$(cat /tmp/fix.txt)" \
    2>/tmp/fix.stderr \
    > /tmp/fix.jsonl
python scripts/check_lean.py --skip-probe
```

Repeat until all gates pass. Do not move to the next subsection while
the current one is unresolved.

## Foundations-audit flag interaction (operator footgun)

`scripts/check_lean.py` invokes
`audit_foundations_dependencies.py --check --skip-validation`. The
committed artifacts at
`formalization/inventory/foundations_declarations.jsonl` and
`formalization/inventory/foundations_dependency_audit.md` are
generated in that same mode (`--skip-validation`, no `--skip-probe`).
If you run the audit script without `--skip-validation`, the
artifacts gain `validation_status: passed` and check_lean.py then
flags them as stale.

Use the Makefile wrappers:

- `make audit-check` — the safe verification command (matches
  check_lean.py's invocation).
- `make audit-regenerate` — regenerate in the safe mode.
- `make audit-regenerate-full` — only if you intend to also update
  check_lean.py's flag combination.

## Codex CLI footguns (from `memory/reference_codex_cli.md`)

- **Resume by UUID only.** `codex exec resume <typo> "..."` silently
  spawns a new thread (losing context). Always pass the captured
  UUID from `lean/.codex_thread_id_<axis>`.
- **Stderr "thread not found" line is benign.** `ERROR codex_core::session:
  failed to record rollout items: thread <id> not found` appears after
  every `exec` run; the rollout file is still written correctly.
  Ignore it. Redirecting stderr to a file (`2>/tmp/*.stderr`) keeps
  it out of the way.
- **`--ephemeral`** discards the rollout file. Only use it if the
  current kickoff turn must be thrown away and rerun (e.g. the
  conventions in `codex_kickoff.md` were wrong and you want to start
  fresh). The thread_id is also discarded with `--ephemeral`.
- **`--full-auto`** = workspace-write sandbox + approval=never.
  Writable roots: cwd (the repo), `/tmp`, `~/.codex/memories`. Codex
  can edit the files listed under §3 "you will write" in
  `codex_kickoff.md` without confirmation.
- **`--skip-git-repo-check`** is recommended for the kickoff. Once
  the thread is running, resume calls don't need it.

## When Claude updates the cross-walk or governance doc

These are Claude's edits, not codex's. Trigger conditions:

1. Codex surfaces a concept that should be in the cross-walk but
   isn't (e.g. a new foundations decl it wants to consume). Claude
   edits `formalization/inventory/imported_foundations.yml`,
   regenerates the canary
   (`python scripts/generate_imported_foundations.py`), and re-runs
   the validator chain.
2. Codex surfaces a notation gap (a symbol used in the LaTeX that
   isn't governed). Claude edits
   `paper/notation_and_terminology.md`, re-extracts the inventory
   (`python scripts/extract_latex_inventory.py`) so the
   `terminology_snapshot.json` hash updates, and re-runs validators.
   Then optionally re-issue the affected subsection to codex with
   the updated vocabulary.
3. Codex requests a new axiom for the trust base. Claude reviews
   whether the axiom is justified; if yes, edits
   `lean/manifests/trust_base.txt`; if no, sends codex a fix prompt
   asking for a reworked proof.

## Section-level flow review (the only legal batching)

After all `mechanize_now` labels in a section are accepted, send
codex a section-level flow-review prompt:

```bash
cat > /tmp/flow_review.txt <<'EOF'
Review the SixBirdsDualityConfinement.DualityConfinement.<Section> module as a whole:
- Is there redundant scaffolding?
- Can imports be tightened?
- Are naming and tactic conventions consistent across decls?
- Does the module hang together as a unit?
Propose changes; do not commit them — Claude reviews first.
EOF

codex exec resume --json --full-auto \
    -c model_reasoning_effort='"high"' \
    "$(cat lean/.codex_thread_id_duality_confinement)" \
    "$(cat /tmp/flow_review.txt)" \
    2>/tmp/flow_review.stderr \
    > /tmp/flow_review.jsonl
```

This is the only legal batching operation per
`memory/feedback_no_batching.md`.

## Pointers

- Kickoff contract: `lean/codex_kickoff.md`
- Prompt generator: `scripts/build_codex_prompt.py`
- Review orchestrator: `scripts/check_lean.py`
- Per-axis queue: `formalization/traceability/queue_{duality_confinement,rh}.csv`
- Per-axis manifest: `lean/manifests/{duality_confinement,rh}_manifest.toml`
- Trust base: `lean/manifests/trust_base.txt`
- Cross-walk: `formalization/inventory/imported_foundations.yml`
- Notation governance: `paper/notation_and_terminology.md`
- Strict protocol memory: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/feedback_no_batching.md`
- Review authority memory: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/feedback_review_authority.md`
- Codex CLI reference: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/reference_codex_cli.md`
- Bootstrap stdin discipline: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/feedback_codex_bootstrap_stdin.md`
