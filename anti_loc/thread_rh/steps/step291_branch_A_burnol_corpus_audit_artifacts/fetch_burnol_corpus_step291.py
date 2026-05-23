#!/usr/bin/env python3
"""Step 291 Burnol corpus fetch/audit helper.

This script intentionally keeps the audit reproducible: it queries arXiv for
Burnol's bibliography, downloads the zeta/Sonine/Fourier/Hankel/operator subset,
extracts PDF text with pdftotext, and writes machine-readable CSV evidence.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import re
import subprocess
import tarfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step291_branch_A_burnol_corpus_audit_artifacts")
RAW = ART / "raw_corpus"
RAW.mkdir(parents=True, exist_ok=True)

ARXIV_API = "https://export.arxiv.org/api/query?search_query={query}&start=0&max_results=100"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

RELEVANCE_TERMS = [
    "zeta",
    "riemann",
    "sonine",
    "fourier",
    "hankel",
    "mellin",
    "hardy",
    "paley",
    "hamburger",
    "conductor",
    "commutator",
    "copoisson",
    "co-poisson",
    "explicit formula",
    "l-functions",
    "abelian l",
    "gamma",
    "cosine kernel",
]

BRANCH_A_TERMS = [
    "calkin",
    "essential norm",
    "norme essentielle",
    "commutator",
    "commutateur",
    "projection",
    "sonine",
    "kernel",
    "noyau",
    "zeta",
    "m_zeta",
    "multiplication",
    "multiplier",
    "compact",
    "compacte",
    "norm",
    "norme",
]


def fetch_url(url: str, out: Path | None = None, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "six-birds-step291-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if out is not None:
        out.write_bytes(data)
    return data


def arxiv_entries() -> list[dict[str, str]]:
    query = urllib.parse.quote('au:"Burnol"')
    data = fetch_url(ARXIV_API.format(query=query))
    (RAW / "arxiv_author_burnol.xml").write_bytes(data)
    root = ET.fromstring(data)
    entries = []
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[1]
        aid_base = aid.split("v")[0] if aid.startswith("math/") else re.sub(r"v\d+$", "", aid)
        title = " ".join(e.find("a:title", NS).text.split())
        summary = " ".join(e.find("a:summary", NS).text.split())
        published = e.find("a:published", NS).text[:10]
        journal_el = e.find("arxiv:journal_ref", NS)
        doi_el = e.find("arxiv:doi", NS)
        entries.append(
            {
                "arxiv_id": aid_base,
                "arxiv_version": aid,
                "year": published[:4],
                "published": published,
                "title": title,
                "summary": summary,
                "journal_ref": journal_el.text.strip().replace("\n", " ") if journal_el is not None and journal_el.text else "",
                "doi": doi_el.text.strip() if doi_el is not None and doi_el.text else "",
            }
        )
    return entries


def relevant(entry: dict[str, str]) -> bool:
    text = (entry["title"] + " " + entry["summary"] + " " + entry["journal_ref"]).lower()
    if any(term in text for term in RELEVANCE_TERMS):
        # Exclude recent Kempner/missing-digit work unless zeta is the central title.
        if any(x in text for x in ["kempner", "irwin", "missing digits", "ellipsephic", "exactly one 42"]):
            return "zeta function" in text and int(entry["year"]) < 2015
        return True
    return False


def safe_name(arxiv_id: str) -> str:
    return arxiv_id.replace("/", "_")


def download_paper(entry: dict[str, str]) -> dict[str, str]:
    aid = entry["arxiv_id"]
    base = safe_name(aid)
    pdf = RAW / f"{base}.pdf"
    txt = RAW / f"{base}.txt"
    src = RAW / f"{base}.source"
    src_txt = RAW / f"{base}.source.txt"
    status = "not_fetched"
    errors = []
    try:
        fetch_url(f"https://arxiv.org/pdf/{aid}", pdf)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True, timeout=60)
        status = "pdf_text_ok"
    except Exception as exc:  # noqa: BLE001
        errors.append(f"pdf:{type(exc).__name__}:{exc}")
    time.sleep(0.35)
    try:
        data = fetch_url(f"https://arxiv.org/e-print/{aid}", src)
        try:
            # Single gzipped TeX.
            src_txt.write_text(gzip.decompress(data).decode("utf-8", "replace"), encoding="utf-8")
        except Exception:
            try:
                with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tar:
                    chunks = []
                    for member in tar.getmembers():
                        if member.isfile() and re.search(r"\.(tex|bbl|ltx)$", member.name):
                            f = tar.extractfile(member)
                            if f:
                                chunks.append(f"\n\n%% FILE: {member.name}\n" + f.read().decode("utf-8", "replace"))
                    src_txt.write_text("\n".join(chunks), encoding="utf-8")
            except Exception:
                src_txt.write_bytes(data)
        status += "+source_ok"
    except Exception as exc:  # noqa: BLE001
        errors.append(f"source:{type(exc).__name__}:{exc}")
    entry["fetch_status"] = status
    entry["fetch_errors"] = " | ".join(errors)
    entry["pdf_path"] = str(pdf if pdf.exists() else "")
    entry["text_path"] = str(txt if txt.exists() else "")
    entry["source_text_path"] = str(src_txt if src_txt.exists() else "")
    return entry


def read_text(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def section_rows(entry: dict[str, str]) -> list[dict[str, str]]:
    text = read_text(entry.get("source_text_path", "")) or read_text(entry.get("text_path", ""))
    rows = []
    if not text:
        return rows
    # Prefer TeX section markers; fall back to visible numbered headings.
    found = []
    for m in re.finditer(r"\\(?:section|subsection)\*?\{([^{}]{1,160})\}", text):
        found.append((m.start(), m.group(1).strip()))
    if not found:
        for m in re.finditer(r"(?m)^\s*(\d+(?:\.\d+)*)[.)]?\s+([A-ZÀ-ÿ][^\n]{3,120})$", text):
            title = f"{m.group(1)} {m.group(2).strip()}"
            if len(title.split()) <= 18:
                found.append((m.start(), title))
    if not found:
        rows.append(
            {
                "paper": entry["title"],
                "arxiv_id": entry["arxiv_id"],
                "section": "unsectioned_or_not_detected",
                "key_claims_keywords": keyword_summary(text),
            }
        )
        return rows
    for idx, (pos, title) in enumerate(found):
        end = found[idx + 1][0] if idx + 1 < len(found) else min(len(text), pos + 6000)
        chunk = text[pos:end]
        rows.append(
            {
                "paper": entry["title"],
                "arxiv_id": entry["arxiv_id"],
                "section": title,
                "key_claims_keywords": keyword_summary(chunk),
            }
        )
    return rows


def keyword_summary(text: str) -> str:
    lo = text.lower()
    hits = []
    for term in BRANCH_A_TERMS:
        n = lo.count(term)
        if n:
            hits.append(f"{term}:{n}")
    return "; ".join(hits[:14])


def candidate_rows(entry: dict[str, str]) -> list[dict[str, str]]:
    text = read_text(entry.get("source_text_path", "")) or read_text(entry.get("text_path", ""))
    lo = text.lower()
    rows = []
    needs = [
        ("faithful Calkin symbol for M_zeta commutator", ["calkin", "commutator", "commutateur", "m_zeta"]),
        ("closed form for Phi_max essential norm", ["essential norm", "norme essentielle", "0.490476", "calkin"]),
        ("structural identity for Sonine projection commutator", ["projection", "sonine", "commutator", "commutateur", "compact"]),
    ]
    for need, terms in needs:
        hits = [t for t in terms if t in lo]
        strength = "none"
        reason = "no matched keywords"
        if hits:
            strength = "background_or_adjacent"
            reason = f"keyword hits: {', '.join(hits)}"
        if ("calkin" in hits) or ("essential norm" in hits) or ("norme essentielle" in hits):
            strength = "potential_match_needs_manual_check"
        rows.append(
            {
                "paper": entry["title"],
                "arxiv_id": entry["arxiv_id"],
                "candidate_lemma": reason,
                "branch_A_need": need,
                "match_strength": strength,
            }
        )
    return rows


def quote_rows(entry: dict[str, str]) -> list[dict[str, str]]:
    text = read_text(entry.get("source_text_path", "")) or read_text(entry.get("text_path", ""))
    if not text:
        return []
    patterns = [
        (r"K_\\lambda\(z,w\)\s*=.{0,220}", "Sonine kernel formula"),
        (r"K_\\lambda\([^)]+\).{0,180}", "Sonine kernel mention"),
        (r"\\begin\{theoreme\}.{0,600}?\\end\{theoreme\}", "theorem"),
        (r"\\begin\{thm\}.{0,600}?\\end\{thm\}", "theorem"),
        (r"Z\^\{\\lambda\}_\{w,k\}.{0,250}", "zeta-zero evaluator"),
        (r"\[f,Z\^\{\\lambda\}_\{w,k\}\].{0,250}", "Burnol evaluator identity"),
        (r"complete.{0,80}minimal.{0,160}", "complete/minimal systems"),
        (r"Sonine.{0,220}", "Sonine context"),
    ]
    rows = []
    for pat, label in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            quote = re.sub(r"\s+", " ", m.group(0)).strip()
            rows.append(
                {
                    "paper": entry["title"],
                    "arxiv_id": entry["arxiv_id"],
                    "section_or_page": "auto-extracted; see section table",
                    "quote": quote[:500],
                    "relevance": label,
                }
            )
    return rows[:4]


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> None:
    entries = arxiv_entries()
    selected = [e for e in entries if relevant(e)]
    # Force include key corpus entries even if keyword filtering changes.
    force = {
        "math/0001013",
        "math/0103058",
        "math/0105120",
        "math/0208121",
        "math/0203120",
        "math/0112254",
        "math/0407443",
        "1106.4751",
        "1008.0518",
        "math/9812012",
        "math/9811040",
        "math/9902080",
        "math/0602425",
        "math/0509619",
        "1008.0617",
    }
    for e in entries:
        if e["arxiv_id"] in force and e not in selected:
            selected.append(e)
    selected.sort(key=lambda x: (x["year"], x["arxiv_id"]))
    fetched = []
    for e in selected:
        print(f"FETCH {e['arxiv_id']} {e['title']}")
        fetched.append(download_paper(e.copy()))
        time.sleep(0.5)

    biblio_rows = []
    section_all = []
    cand_all = []
    quote_all = []
    for e in fetched:
        sections = section_rows(e)
        cands = candidate_rows(e)
        quotes = quote_rows(e)
        section_all.extend(sections)
        cand_all.extend(cands)
        quote_all.extend(quotes)
        biblio_rows.append(
            {
                "paper": e["title"],
                "year": e["year"],
                "arxiv_id": e["arxiv_id"],
                "doi": e["doi"],
                "journal_ref": e["journal_ref"],
                "audited_yes_no": "yes" if e["text_path"] or e["source_text_path"] else "fetch_failed",
                "section_count": str(len(sections)),
                "fetch_status": e["fetch_status"],
            }
        )

    write_csv(
        ART / "burnol_bibliography_step291.csv",
        biblio_rows,
        ["paper", "year", "arxiv_id", "doi", "journal_ref", "audited_yes_no", "section_count", "fetch_status"],
    )
    write_csv(
        ART / "candidate_lemma_matches_step291.csv",
        cand_all,
        ["paper", "arxiv_id", "candidate_lemma", "branch_A_need", "match_strength"],
    )
    write_csv(
        ART / "verbatim_quotes_step291.csv",
        quote_all,
        ["paper", "arxiv_id", "section_or_page", "quote", "relevance"],
    )
    write_csv(
        ART / "auto_section_rows_step291.csv",
        section_all,
        ["paper", "arxiv_id", "section", "key_claims_keywords"],
    )
    (ART / "burnol_arxiv_selection_step291.json").write_text(json.dumps(fetched, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"selected={len(selected)}")
    print(f"sections={len(section_all)} candidates={len(cand_all)} quotes={len(quote_all)}")


if __name__ == "__main__":
    main()
