#!/usr/bin/env python3
"""Per-subsection codex prompt generator.

Reads queue state from formalization/traceability/queue_<axis>.csv,
LaTeX bodies from formalization/inventory/source_items.jsonl, cross-walk
hints from formalization/inventory/imported_foundations.yml, the
already-mechanized state from lean/manifests/<axis>_manifest.toml, and
the section-to-module mapping from lean/manifests/section_module_map.toml.

Emits a complete prompt that the operator pipes to a resumed codex
session. The prompt covers one paper subsection (= all pending
mechanize_now labels in one section); the kickoff document
(lean/codex_kickoff.md) is assumed to have been ingested as the
session's first turn.

CLI:
  python scripts/build_codex_prompt.py --axis {main,xi} --paper-label <label>
                                       [--out /tmp/prompt.txt]

If --out is omitted, the prompt is written to stdout.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_foundations_dependencies as audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_DIR = ROOT / "formalization" / "inventory"
TRACEABILITY_DIR = ROOT / "formalization" / "traceability"
LEAN_DIR = ROOT / "lean"
MANIFESTS_DIR = LEAN_DIR / "manifests"

SOURCE_ITEMS = INVENTORY_DIR / "source_items.jsonl"
IMPORTED_FOUNDATIONS = INVENTORY_DIR / "imported_foundations.yml"
SECTION_MODULE_MAP = MANIFESTS_DIR / "section_module_map.toml"
TRUST_BASE = MANIFESTS_DIR / "trust_base.txt"

# Per-axis math artifact paths. Used as the source body when
# source_items.jsonl is empty (markdown-driven workflow).
MATH_ARTIFACTS = {
    "duality_confinement": ROOT / "anti_loc" / "extracted_math" / "duality_confinement_csl.md",
    "rh": ROOT / "anti_loc" / "extracted_math" / "rh_construction.md",
}


def extract_section_body_from_artifact(axis: str, section_title: str) -> str | None:
    """Return the body of the named section from the per-axis math artifact.

    Section is identified by an `## §N. <title>` markdown header that
    contains the section_title substring. The body extends until the
    next `## ` heading.
    """
    artifact = MATH_ARTIFACTS.get(axis)
    if artifact is None or not artifact.exists():
        return None
    text = artifact.read_text(encoding="utf-8")
    lines = text.splitlines()
    matched_start: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            if section_title.lower() in line.lower():
                matched_start = i
                break
    if matched_start is None:
        return None
    body_lines: list[str] = []
    for line in lines[matched_start:]:
        if body_lines and line.startswith("## "):
            break
        body_lines.append(line)
    return "\n".join(body_lines)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_section_module_map(path: Path) -> dict[str, dict[str, str]]:
    """Parse a small TOML subset: `[axis]` table with `"section" = "module"` lines."""
    out: dict[str, dict[str, str]] = {}
    current: str | None = None
    table_re = re.compile(r"^\s*\[(?P<name>[A-Za-z0-9_]+)\]\s*$")
    kv_re = re.compile(r'^\s*"(?P<key>[^"]+)"\s*=\s*"(?P<value>[^"]+)"\s*$')
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        table_match = table_re.match(line)
        if table_match:
            current = table_match.group("name")
            out.setdefault(current, {})
            continue
        kv_match = kv_re.match(line)
        if kv_match and current is not None:
            out[current][kv_match.group("key")] = kv_match.group("value")
    return out


def read_queue(axis: str) -> list[dict]:
    path = TRACEABILITY_DIR / f"queue_{axis}.csv"
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def manifest_entries(axis: str) -> list[dict]:
    path = MANIFESTS_DIR / f"{axis}_manifest.toml"
    return [
        r for r in audit.parse_manifest(path) if r.get("manifest_table") in {"definition", "claim"}
    ]


def crosswalk_entries(axis: str) -> list[dict]:
    entries = audit.parse_imported_foundations()
    return [
        e
        for e in entries
        if e.get("paper_axis") in {axis, "both"}
    ]


def read_trust_base() -> list[str]:
    out: list[str] = []
    for line in TRUST_BASE.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if stripped:
            out.append(stripped)
    return out


def find_section_for_label(axis: str, paper_label: str) -> tuple[str, list[dict]]:
    """Return (section_title, all_queue_items_in_section_in_order)."""
    queue = read_queue(axis)
    target = next((row for row in queue if row["paper_label"] == paper_label), None)
    if target is None:
        raise SystemExit(f"paper_label {paper_label!r} not in queue_{axis}.csv")
    section = target["section"]
    section_items = sorted(
        [row for row in queue if row["section"] == section],
        key=lambda r: int(r["line_start"]),
    )
    return section, section_items


def relevant_notation_hints(axis: str) -> list[str]:
    """Return short notation hints from the governance doc.

    To keep the prompt focused, we list only headline reserved symbols
    from §4 of paper/notation_and_terminology.md. Codex was already
    primed on the full doc by the kickoff; this is a per-prompt
    reminder, not the source of truth.
    """
    common = [
        "`L`  = native probe family `E → Y`",
        "`D`  = layer-dissolving probe family `E → Z`",
        "`C`  = audit energy operator (positive self-adjoint)",
        "`\\Gamma`  = exact package",
        "`\\K_{C,Gamma}(L)`  = packaged native currency `L_Gamma C_Gamma^\\dagger L_Gamma^*`",
        "`\\Xi_C(D | L)`  = adequacy residual; reserved exclusively for this object",
        "`\\Fix(J)`  = fixed locus of an anti-linear involution",
        "`\\Theta`, `\\Theta^Y_j`, `\\Theta^-`  = budgets (positive operators)",
        "`A_*`  = optimal native explanation map `K_{DL} K_{LL}^\\dagger`",
        "`\\preceqq`  = Loewner order (alias for `\\preceq`)",
    ]
    duality = [
        "`J`  = anti-linear involution (duality-confinement)",
        "`\\psi`, `\\psi_-`  = readout and its anti-invariant component",
        "`\\mathsf A_X`  = anti-invariant object ledger",
        "`\\K^-`  = carrier-side anti-invariant currency",
        "`B_n`, `T_n`, `\\iota_n`  = domination record, tail, transport",
    ]
    xi_specific = [
        "`T_L`, `T_D`  = energy-scaled probe operators `L_0 C_0^{-1/2}`, `D_0 C_0^{-1/2}`",
        "`P_L`  = orthogonal projection onto `Ran T_L^*`",
        "`K_{MM | L}`, `K_{DM | L}`  = conditional currencies",
        "`\\Delta_\\Xi`  = adequacy defect `Xi - Omega`",
    ]
    if axis == "duality_confinement":
        return common + duality
    if axis == "rh":
        return common + xi_specific
    return common


def build_prompt(axis: str, paper_label: str) -> str:
    section, section_items = find_section_for_label(axis, paper_label)
    source_records = {r["latex_label"]: r for r in read_jsonl(SOURCE_ITEMS) if r.get("latex_label")}
    section_module = parse_section_module_map(SECTION_MODULE_MAP).get(axis, {}).get(section)
    if section_module is None:
        raise SystemExit(
            f"section {section!r} not in section_module_map.toml under [{axis}]"
        )
    module_file_rel = "lean/" + section_module.replace(".", "/") + ".lean"

    # A manifest entry only counts as "already mechanized" when its status
    # is `definition` or `theorem` (i.e. fully realized). Placeholder
    # statuses `partial` and `unformalized` mean the label still needs
    # work, so it stays in the pending queue and on the next prompt.
    COMPLETE_STATUSES = {"definition", "theorem"}
    already_done = {
        e["paper_label"]: e
        for e in manifest_entries(axis)
        if e.get("status") in COMPLETE_STATUSES
    }

    pending: list[dict] = []
    already: list[dict] = []
    for item in section_items:
        if item["paper_label"] in already_done:
            already.append(item)
        else:
            pending.append(item)

    if not pending:
        raise SystemExit(
            f"no pending labels in section {section!r}; nothing to mechanize"
        )

    lines: list[str] = []
    lines.append(f"# Subsection prompt — axis={axis}, section={section!r}")
    lines.append("")
    artifact_path = MATH_ARTIFACTS.get(axis)
    artifact_rel = (
        artifact_path.resolve().relative_to(ROOT).as_posix() if artifact_path else "(unknown)"
    )
    lines.append(
        f"Mechanize the pending labels in this subsection. Source math "
        f"artifact: `{artifact_rel}` (§ '{section}')."
    )
    lines.append("")
    lines.append(f"Target Lean module: `{section_module}`")
    lines.append(f"Target file: `{module_file_rel}`")
    lines.append(f"Target manifest: `lean/manifests/{axis}_manifest.toml`")
    lines.append("")
    lines.append("## Pending paper_labels in this subsection")
    lines.append("")
    for item in pending:
        lines.append(f"  - `{item['paper_label']}`   {item['kind']}   (line {item['line_start']})")
    lines.append("")
    if already:
        lines.append("## Already-mechanized labels in this section (reference; do NOT redefine)")
        lines.append("")
        for item in already:
            entry = already_done[item["paper_label"]]
            lines.append(f"  - `{item['paper_label']}`   →   `{entry.get('lean_decl', '?')}`")
        lines.append("")
    lines.append("## Source math (verbatim from artifact section)")
    lines.append("")
    section_body = extract_section_body_from_artifact(axis, section)
    if section_body:
        lines.append("```markdown")
        lines.append(section_body)
        lines.append("```")
        lines.append("")
    for item in pending:
        record = source_records.get(item["paper_label"])
        if not record:
            if not section_body:
                lines.append(f"  (no body available for {item['paper_label']})")
            continue
        lines.append(
            f"### `{item['paper_label']}` "
            f"(lines {record['line_start']}–{record['line_end']}, "
            f"env_kind={record['env_kind']})"
        )
        lines.append("")
        lines.append("```latex")
        lines.append(record["raw_body"])
        lines.append("```")
        lines.append("")

    lines.append("## Cross-walk hints (use foundations decls via Terminology aliases when applicable)")
    lines.append("")
    for entry in crosswalk_entries(axis):
        concept = entry.get("dependency_concept", "")
        decl = entry.get("lean_decl", "")
        if concept and decl:
            lines.append(f"  - {concept!r}   →   `{decl}`")
    lines.append("")
    lines.append("## Reserved notation cues")
    lines.append("")
    lines.append(
        "(Full governance doc: `paper/notation_and_terminology.md`. "
        "Headline reservations for this axis:)"
    )
    lines.append("")
    for hint in relevant_notation_hints(axis):
        lines.append(f"  - {hint}")
    lines.append("")
    lines.append("## Constraints")
    lines.append("")
    lines.append(
        "- Statement fidelity: every labeled environment in this subsection "
        "gets a Lean declaration whose statement faithfully matches the LaTeX. "
        "Hypotheses, conclusion, and quantifier order must agree."
    )
    lines.append(
        "- No `sorry`, `admit`, `axiom`, `opaque`, or `constant` anywhere."
    )
    lines.append(
        "- New axiom closures: only the five in `lean/manifests/trust_base.txt` "
        "(" + ", ".join(read_trust_base()) + ") are permitted. If your proof "
        "introduces another axiom, surface the issue instead of committing."
    )
    lines.append(
        "- Edit only `" + module_file_rel + "` and "
        "`lean/manifests/" + axis + "_manifest.toml`. Do not touch any other module, "
        "inventory toml, paper source, or vendor file."
    )
    lines.append(
        "- Reuse foundations decls via the `SixBirdsDualityConfinement` aliases in "
        "`Terminology.lean` and `FoundationsICompat.lean` whenever the cross-walk "
        "lists a canonical name; never coin a parallel name."
    )
    lines.append("")
    lines.append("## Manifest update")
    lines.append("")
    lines.append(
        f"Append one entry per new declaration to `lean/manifests/{axis}_manifest.toml`. "
        "Schema (all fields required; free-form strings may be empty):"
    )
    lines.append("")
    lines.append("```toml")
    lines.append("[[definition]]  # use [[claim]] for theorem/lemma/proposition/corollary")
    lines.append('paper_label = "<one of the pending labels above>"')
    lines.append(f'paper_section = "{section}"')
    lines.append('description = "<one-line summary>"')
    lines.append('status = "definition"  # or "theorem"; "partial" / "unformalized" only as placeholders')
    lines.append('lean_subproject = "."')
    lines.append(f'lean_module = "{section_module}"')
    lines.append(f'lean_decl = "{section_module}.<camelCaseName>"')
    lines.append('notes = ""')
    lines.append("```")
    lines.append("")
    lines.append(
        "When complete, the validator chain `python scripts/check_lean.py` "
        "must exit zero, including `lake build` and `check_manifests.py` "
        "(schema, cross-reference, lake probe, axiom audit)."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axis", required=True, choices=["duality_confinement", "rh"])
    parser.add_argument("--paper-label", required=True)
    parser.add_argument("--out", type=Path, help="write prompt to file (default: stdout)")
    args = parser.parse_args()

    prompt = build_prompt(args.axis, args.paper_label)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(prompt, encoding="utf-8")
        print(f"wrote prompt to {args.out} ({prompt.count(chr(10)) + 1} lines)", file=sys.stderr)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
