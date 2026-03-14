# Sopaper Evidence v0.7.0

## Summary

Reviewed-source grounding release for stronger research-level evidence extraction.

## Highlights

- upgraded fetched source-note verification from page-level metadata only to optional `reviewed-primary` summaries
- synthesized reviewed benchmark, evaluation, metric, and baseline statements directly into verified notes
- updated ledger construction to prefer reviewed summaries over weaker page-level facts
- kept the topic-first and result-artifact workflows conservative while improving source quality
- synchronized English and Chinese README content with the new reviewed-source capability

## Why this release matters

This release pushes Sopaper Evidence beyond basic page verification. External sources that contain enough structured semantic signals can now become reviewed research summaries, which gives the downstream ledger and claim map a cleaner, stronger evidence surface without pretending that full manual paper reading has happened.

## Notes

- reviewed-source extraction is still conservative and does not replace manual reading of primary papers
- no output or local test artifacts were included in the release bundle
- result-artifact ingestion and comparative-claim gating remain unchanged in trust level
