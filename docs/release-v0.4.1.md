# Sopaper Evidence v0.4.1

## Summary

Quality hardening release for the first automation helpers.

## Highlights

- tightened `build_evidence_ledger.py` so source-list notes no longer default to `project_evidence`
- tightened `bootstrap_claim_map.py` so placeholder `TODO:` statements no longer generate misleading partial matches
- updated example drafts to match the corrected automation behavior

## Why this release matters

This release reduces false confidence in the automation workflow. Freshly generated drafts now stay conservative until real reviewed evidence is added, which keeps the project aligned with its evidence-first trust model.

## Notes

- no new automation stages were added
- this release focuses on trust and output correctness
- existing workflow commands remain the same
