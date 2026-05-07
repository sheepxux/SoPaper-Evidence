# Sopaper Evidence v1.1.0

## Summary

Adds experiment-directory ingestion so real project result folders can enter the evidence pipeline without listing every result file manually.

## Highlights

- `run_evidence_pipeline.py` now supports `--result-dir`
- `run_topic_evidence_pipeline.py` now passes result directories into the downstream evidence pipeline
- result directories are scanned recursively for `.csv`, `.tsv`, and `.json` artifacts
- discovered result artifacts reuse the existing result parsing, metric normalization, multi-artifact fusion, claim mapping, gap triage, and fairness review layers
- added an OpenClaw result-directory example under `sopaper-evidence/examples/openclaw-results-dir`
- updated English and Chinese documentation, skill instructions, and marketplace copy

## Why this release matters

Most research projects store experiment outputs in directories, not single curated files. This release lets Sopaper Evidence ingest that shape directly, making the skill easier to use on real project workspaces.

## Notes

- markdown result artifacts are still supported through `--result-artifacts`
- result-directory discovery is intentionally limited to `.csv`, `.tsv`, and `.json` files to avoid treating arbitrary notes as project evidence
- local `output/` test artifacts were not included in the release
