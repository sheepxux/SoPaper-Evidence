# Sopaper Evidence v0.9.0

## Summary

Multi-artifact fusion release for stronger experiment-evidence packaging.

## Highlights

- fused multiple result artifacts into an aggregated `project_evidence` entry
- normalized common metric names such as `success_rate` into cleaner evidence text
- kept direct `.csv`, `.tsv`, and `.json` ingestion while improving downstream evidence quality
- improved comparative-result evidence surfacing so direct result artifacts appear more clearly in claim mapping
- synchronized English and Chinese README content with the new multi-artifact workflow

## Why this release matters

Real projects rarely have a single result file. This release makes Sopaper Evidence much more usable on real experiment directories by letting several result artifacts reinforce each other instead of staying isolated. The pipeline now builds a stronger project-level evidence surface before claim mapping and gap triage begin.

## Notes

- aggregate result evidence is still conservative and does not replace fairness review
- local `output/` test artifacts were not included in the release
- raw result ingestion remains compatible with the markdown result-artifact template
