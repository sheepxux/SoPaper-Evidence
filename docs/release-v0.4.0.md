# Sopaper Evidence v0.4.0

## Summary

First lightweight automation release for Sopaper Evidence.

## Highlights

- added `build_evidence_ledger.py` for first-pass evidence ledger generation from markdown notes and source lists
- added `bootstrap_claim_map.py` for first-pass claim-to-evidence map generation from claims and ledger drafts
- added `triage_evidence_gaps.py` for blocker/major/minor experiment gap triage
- added OpenClaw examples for source lists, ledger drafts, claim map drafts, and gap report drafts
- extended the skill documentation to connect the new automation steps to the evidence-first workflow

## Why this release matters

This release moves Sopaper Evidence beyond static templates and into lightweight automation. The project now helps users structure sources, bootstrap claim maps, and triage evidence gaps without weakening the evidence-first discipline.

## Notes

- these helpers generate drafts, not final paper-safe outputs
- all generated ledgers, claim maps, and gap reports still require manual review
- the project remains conservative: no fabricated evidence, no unsupported quantitative claims
