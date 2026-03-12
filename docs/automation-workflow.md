# Automation Workflow

Use this workflow when you want to turn rough source notes into a first-pass evidence package with the helper scripts.

If the inputs still contain raw URLs, fetch structured source-note drafts before building the ledger.

## Inputs

- a markdown file with source links or notes
- a markdown file with candidate research claims

## Pipeline

### 0. Fetch external source notes from URLs

```bash
python3 scripts/fetch_external_sources.py \
  sopaper-evidence/examples/openclaw-source-list.md \
  --output-dir output/openclaw-fetched-sources
```

Output:

- one structured source-note draft per fetched URL
- titles, access dates, and directly observed page metadata
- verification status left in a review-required state until a human upgrades it

### 1. Build an evidence ledger draft

```bash
python3 scripts/build_evidence_ledger.py \
  sopaper-evidence/examples/openclaw-source-list.md \
  -o output/openclaw-ledger-draft.md
```

Output:

- a first-pass ledger with `E01`, `E02`, and other evidence ids
- structured source notes and result artifacts can seed non-placeholder statements

### 2. Bootstrap a claim map draft

```bash
python3 scripts/bootstrap_claim_map.py \
  sopaper-evidence/examples/openclaw-claims.md \
  output/openclaw-ledger-draft.md \
  -o output/openclaw-claim-map-draft.md
```

Output:

- a first-pass claim-to-evidence table
- reviewed local result artifacts can raise comparative claims from `unsupported` to `partial`

### 3. Triage evidence gaps

```bash
python3 scripts/triage_evidence_gaps.py \
  sopaper-evidence/examples/openclaw-claims.md \
  output/openclaw-ledger-draft.md \
  -o output/openclaw-gap-report-draft.md
```

Output:

- a first-pass blocker / major / minor gap report

### 4. Review the generated summary

The unified pipeline also generates a summary file that points to the three drafts and lists the next review actions.

## Review rule

These outputs are drafts. Review and edit them before using them in any downstream research workflow.

## Recommended follow-up

After the scripts run:

1. verify external sources
2. tighten claim wording
3. confirm baseline fairness
4. update the experiment gap report
5. only then draft outline or abstract support points
