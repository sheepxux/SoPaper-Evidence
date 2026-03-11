# Sopaper Evidence v0.5.0

## Summary

Unified workflow release for Sopaper Evidence.

## Highlights

- added `run_evidence_pipeline.py` as a single entry point for ledger generation, claim-map bootstrap, and gap triage
- documented the end-to-end automation workflow in the README and supporting docs
- aligned the public repository state with the current automation-focused product direction

## Why this release matters

This release turns the helper scripts into a clearer workflow product. Users can now go from source list and claims file to a full draft evidence package with one command, while still preserving the project’s evidence-first review discipline.

## Notes

- pipeline outputs are still drafts and require manual review
- no new trust assumptions were introduced
- the individual helper scripts remain available for step-by-step use
