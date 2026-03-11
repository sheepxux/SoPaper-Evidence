# Automation Workflow

Use this workflow when you want to turn rough source notes into a first-pass evidence package with the helper scripts.

## Inputs

- a markdown file with source links or notes
- a markdown file with candidate paper claims

## Pipeline

### 1. Build an evidence ledger draft

```bash
python3 scripts/build_evidence_ledger.py \
  sopaper-evidence/examples/openclaw-source-list.md \
  -o output/openclaw-ledger-draft.md
```

Output:

- a first-pass ledger with `E01`, `E02`, and other evidence ids

### 2. Bootstrap a claim map draft

```bash
python3 scripts/bootstrap_claim_map.py \
  sopaper-evidence/examples/openclaw-claims.md \
  output/openclaw-ledger-draft.md \
  -o output/openclaw-claim-map-draft.md
```

Output:

- a first-pass claim-to-evidence table

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

These outputs are drafts. Review and edit them before using them in any paper-writing workflow.

## Recommended follow-up

After the scripts run:

1. verify external sources
2. tighten claim wording
3. confirm baseline fairness
4. update the experiment gap report
5. only then draft outline or abstract support points
