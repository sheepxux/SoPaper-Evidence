# Marketplace Publish Checklist

Use this checklist when publishing Sopaper Evidence to ClawHub or similar skill marketplaces.

## Listing basics

- Name: `Sopaper Evidence`
- Short description:
  `Evidence-first research workflow for paper writing. Search, verify, and organize real papers, datasets, benchmarks, case studies, and project artifacts without unsupported claims.`
- Category suggestion: `Research` or `Productivity`
- Tags:
  - research
  - paper-writing
  - evidence
  - literature-review
  - robotics
  - embodiedai
  - openclaw

## Trust statement

Sopaper Evidence does not invent papers, results, datasets, benchmark wins, or citations. If evidence is incomplete, it reports the gap instead of overstating the claim.

## What to link

- Primary source: GitHub repository
- Cover image: `docs/assets/cover.png`
- Example references:
  - `sopaper-evidence/examples/openclaw-input.md`
  - `sopaper-evidence/examples/openclaw-search-plan.md`
  - `sopaper-evidence/examples/openclaw-evidence-brief.md`
  - `sopaper-evidence/examples/openclaw-claim-map.md`
  - `sopaper-evidence/examples/openclaw-paper-outline.md`

## Listing body

Sopaper Evidence is a high-trust research skill for teams that want paper support without unsupported claims. It searches and organizes real sources first, maps claims to evidence, identifies unsupported conclusions, and only then supports related work, experiment planning, abstracts, and outlines.

This skill is designed for workflows where every important sentence should be defensible under reviewer scrutiny.

## Pre-publish checks

- README is visible and complete
- cover image renders correctly on GitHub
- examples are linked from the README
- no broken links in markdown
- release notes exist
- license is present
- repository description and topics are set

## Post-publish checks

- marketplace listing links back to GitHub
- GitHub README links back to marketplace listing
- the example chain is easy to find from the repository home page
- release tag exists for the published version

## Recommended launch order

1. Confirm the GitHub repository page is complete
2. Create the `v0.2.0` Git tag and GitHub release
3. Publish the marketplace listing with the GitHub repository as the source of truth
4. Add the marketplace URL back into the GitHub repository website field
5. Re-check the README, cover image, and example links from a logged-out browser
