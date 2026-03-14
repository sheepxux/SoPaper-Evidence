# Sopaper Evidence v0.8.0

## Summary

Zero-wrapper result ingestion release for direct tabular and JSON experiment evidence.

## Highlights

- added direct `.csv`, `.tsv`, and `.json` result-artifact validation and ingestion
- inferred metric, baseline, scope, benchmark, and run-id signals from raw result files
- converted raw result files into `project_evidence` without requiring a handwritten markdown wrapper
- added example CSV and JSON result artifacts for OpenClaw
- synchronized English and Chinese README content with the new low-friction result onboarding workflow

## Why this release matters

This release lowers one of the biggest practical barriers to real adoption: users no longer need to manually rewrite experiment outputs into markdown templates before Sopaper Evidence can use them. The pipeline can now ingest common raw result formats directly and preserve enough structure to influence comparative claim gating.

## Notes

- raw result ingestion is still conservative and does not infer benchmark wins on its own
- local `output/` test artifacts were not included in the release
- the markdown result-artifact template remains available for teams that want tighter manual control
