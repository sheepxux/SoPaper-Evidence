#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CLAIM_LINE_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")
FIELD_RE = re.compile(r"^\s{2}([a-zA-Z0-9_]+):\s*(.*)\s*$")
ID_RE = re.compile(r"^\s*-\s+id:\s*(\S+)\s*$")


@dataclass
class EvidenceEntry:
    evidence_id: str
    statement: str
    classification: str
    source_title: str


@dataclass
class MatchCandidate:
    entry: EvidenceEntry
    score: int
    basis: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a first-pass claim-to-evidence map from a claims list and an evidence ledger draft. "
            "This script uses simple token overlap to suggest candidate evidence items."
        )
    )
    parser.add_argument("claims", help="Markdown file containing bullet-list claims.")
    parser.add_argument("ledger", help="Evidence ledger markdown file.")
    parser.add_argument("-o", "--output", help="Write output to file instead of stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    claims_path = Path(args.claims).expanduser().resolve()
    ledger_path = Path(args.ledger).expanduser().resolve()

    if not claims_path.exists():
        print(f"Missing claims file: {claims_path}", file=sys.stderr)
        return 1
    if not ledger_path.exists():
        print(f"Missing ledger file: {ledger_path}", file=sys.stderr)
        return 1

    claims = parse_claims(claims_path.read_text(encoding="utf-8"))
    evidence = parse_ledger(ledger_path.read_text(encoding="utf-8"))
    output = render_claim_map(claims, evidence)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


def parse_claims(text: str) -> list[str]:
    claims: list[str] = []
    for line in text.splitlines():
        match = CLAIM_LINE_RE.match(line)
        if match:
            claims.append(match.group(1).strip())
    return claims


def parse_ledger(text: str) -> list[EvidenceEntry]:
    entries: list[EvidenceEntry] = []
    current_id = ""
    current_statement = ""
    current_classification = "unverified"
    current_source_title = ""

    for line in text.splitlines():
        id_match = ID_RE.match(line)
        if id_match:
            if current_id:
                entries.append(
                    EvidenceEntry(
                        evidence_id=current_id,
                        statement=current_statement,
                        classification=current_classification,
                        source_title=current_source_title,
                    )
                )
            current_id = id_match.group(1)
            current_statement = ""
            current_classification = "unverified"
            current_source_title = ""
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            field, value = field_match.groups()
            value = strip_quotes(value.strip())
            if field == "statement":
                current_statement = value
            elif field == "classification":
                current_classification = value
            elif field == "source_title":
                current_source_title = value

    if current_id:
        entries.append(
            EvidenceEntry(
                evidence_id=current_id,
                statement=current_statement,
                classification=current_classification,
                source_title=current_source_title,
            )
        )

    return entries


def render_claim_map(claims: list[str], evidence: list[EvidenceEntry]) -> str:
    lines = [
        "# Claim-to-Evidence Map Draft",
        "",
        "This draft was generated automatically. Review every suggested match before using it in paper writing.",
        "",
        "## Major claims",
        "",
        "| Claim ID | Claim | Status | Evidence IDs | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for index, claim in enumerate(claims, start=1):
        matches = match_evidence_for_claim(claim, evidence)
        evidence_ids = ", ".join(item.entry.evidence_id for item in matches[:3])
        status = suggest_status(matches)
        notes = suggest_note(matches)
        lines.append(f"| C{index} | {escape_pipes(claim)} | {status} | {evidence_ids} | {escape_pipes(notes)} |")

    lines.extend(
        [
            "",
            "## Evidence notes",
            "",
            "| Evidence ID | Classification | Statement |",
            "| --- | --- | --- |",
        ]
    )

    for entry in evidence:
        statement = entry.statement or "TODO: fill exact statement."
        lines.append(
            f"| {entry.evidence_id} | {entry.classification} | {escape_pipes(statement)} |"
        )

    return "\n".join(lines) + "\n"


def match_evidence_for_claim(claim: str, evidence: list[EvidenceEntry]) -> list[MatchCandidate]:
    claim_tokens = tokenize(claim)
    scored: list[MatchCandidate] = []

    for entry in evidence:
        if not is_placeholder_statement(entry.statement):
            statement_tokens = tokenize(entry.statement)
            overlap = len(claim_tokens & statement_tokens)
            if overlap > 0:
                scored.append(MatchCandidate(entry=entry, score=overlap * 10, basis="statement"))
                continue

        title_tokens = tokenize(entry.source_title)
        title_overlap = len(claim_tokens & title_tokens)
        if title_overlap > 0:
            scored.append(MatchCandidate(entry=entry, score=title_overlap, basis="title"))

    scored.sort(key=lambda item: (-item.score, item.entry.evidence_id))
    return scored


def suggest_status(matches: list[MatchCandidate]) -> str:
    if not matches:
        return "unsupported"
    if any(match.basis == "statement" and match.entry.classification == "verified_fact" for match in matches):
        return "supported"
    if any(match.basis == "statement" and match.entry.classification == "project_evidence" for match in matches):
        return "partial"
    return "unsupported"


def suggest_note(matches: list[MatchCandidate]) -> str:
    if not matches:
        return "No matching evidence found. Review the claim wording or add supporting sources."
    if all(match.basis == "title" for match in matches[:3]):
        return "Potential title-level leads exist, but no reviewed evidence statement supports this claim yet."
    if all(match.entry.classification == "unverified" for match in matches[:3]):
        return "Potential matches exist, but all suggested evidence is still unverified."
    return "Review suggested evidence ids and tighten the claim wording if support is weak."


def tokenize(value: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "that",
        "this",
        "from",
        "with",
        "into",
        "claim",
        "observation",
        "summarize",
        "exact",
        "todo",
        "source",
        "example",
        "repository",
        "listing",
    }
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", value.lower())
        if len(token) > 2 and token not in stopwords
    }


def is_placeholder_statement(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith("todo:")


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def escape_pipes(value: str) -> str:
    return value.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
