# Field Test Log

## 2026-03-12

| Topic | Observed behavior | Expected behavior | Root cause | Fix direction | Priority |
| --- | --- | --- | --- | --- | --- |
| OpenClaw long-horizon manipulation benchmark evaluation | Topic-first search returned no results, so the whole pipeline stayed unsupported. | The search stage should at least surface related manipulation benchmarks, repos, or embodiment papers for follow-up review. | The current topic-query expansion is specialized for browser-agent and retrieval/citation themes, but not robotics or manipulation topics. | Add robotics/manipulation query expansion and primary-source seeds for benchmark-style robotics searches. | P1 |
| citation-grounded retrieval for code assistants | The pipeline found only one survey-style source and produced sparse evidence coverage. | The search stage should surface code-retrieval benchmarks, citation-grounded QA work, code-assistant evaluation repos, and benchmark papers. | Current source search relies on generic topic token overlap and lacks domain-specific retrieval/citation seeds for code tasks. | Add domain-specific query expansion and stronger source ranking for code retrieval, citation metrics, and grounded generation benchmarks. | P1 |
| browser agent benchmark evaluation | The search stage now returns relevant benchmark pages, but claim support remains capped at page-level partial support. | Positioning should rise beyond partial only after reviewed benchmark notes or stronger extracted statements exist. | Verification currently upgrades fetched page metadata into page-level verified facts, but statement extraction is still too shallow to support stronger claim grounding. | Add stronger statement extraction from fetched notes and require reviewed benchmark-definition style statements before promoting support. | P1 |
| browser agent benchmark evaluation | A small number of relevant sources are found, but benchmark coverage is still narrow. | The source list should consistently include broader primary benchmark anchors such as WebArena-style evaluation sources when they exist. | Topic search now has stricter relevance filters, but primary-source coverage is still dependent on coarse query expansion. | Improve benchmark-specific query planning and add host-aware ranking for benchmark pages and repos. | P2 |
| All topic-first runs | Gap triage is useful, but many runs stop at `source verification` because fetched notes are only page-level verified. | The pipeline should produce more reviewed-ready source notes with clearer candidate facts and benchmark/task definitions. | `verify_source_notes.py` is intentionally conservative and only validates page-level facts. | Add a second pass that extracts benchmark definitions, task framing, and metric snippets for human review. | P2 |

## 2026-03-12 follow-up

- OpenClaw rerun after robotics/manipulation query expansion now returns benchmark-style sources instead of an empty source list.
- The improved OpenClaw source list includes CALVIN, FurnitureBench, LoHoRavens, VLABench, and IKEA Furniture Assembly environment pages.
- The OpenClaw claim map now reaches `partial` for positioning and evaluation framing claims, which is the intended intermediate state before reviewed benchmark notes exist.
- After stronger source-note statement extraction, the OpenClaw ledger now captures benchmark/task facts instead of only page titles.
- The OpenClaw positioning claim now reaches `supported`, while evaluation framing and comparative-result claims remain conservatively capped at `partial`.
- The next remaining bottleneck is no longer source recall for OpenClaw; it is richer benchmark-definition and metric extraction for stronger non-comparative support.
- Retrieval/citation rerun after query-aware filtering no longer mixes in obviously irrelevant retrieval papers from non-AI domains.
- Retrieval/citation source recall is cleaner but still narrow; the current pipeline mainly surfaces xCodeEval-style benchmark results and still needs broader citation-grounded benchmark recall.
- After stronger source-note statement extraction, retrieval/citation notes now promote benchmark/task facts such as \"This source appears to define a code retrieval benchmark\" instead of relying on page titles alone.
- Retrieval/citation positioning claims now reach `supported` on clean benchmark evidence, while comparative-result claims remain capped at `partial`.
- After combining benchmark/task facts with evaluation facts in the ledger, verified statements now carry both task-definition and evaluation-setup signals.
- The pipeline now reaches a stable pattern on both OpenClaw and retrieval/citation topics: positioning support can become `supported`, while evaluation/comparative claims remain conservatively constrained without direct result evidence.
- Gap reports now distinguish between `direct result evidence`, `metric definition`, and `source verification` instead of collapsing everything into a generic blocker.
- The next meaningful upgrade for comparative claims is no longer generic search improvement; it is adding structured result artifacts or stronger metric extraction from primary sources.
- After ingesting a structured OpenClaw result artifact, the ledger now includes a `project_evidence` entry with direct result, metric, and baseline context instead of leaving comparative support entirely to fetched external notes.
- On the OpenClaw rerun with the result artifact, the `direct result evidence` and `metric definition` gaps disappear, leaving `source verification` and `evaluation scope` as the remaining major issues.
- Result-artifact ingestion now gives the comparative-result claim a real project-evidence anchor rather than only benchmark-alignment signals from external benchmark pages.
- After adding reviewed primary-source summaries, verified fetched notes now carry synthesized benchmark/evaluation/baseline statements instead of only page-level facts.
- The OpenClaw topic-first rerun now produces `reviewed-primary` notes and the ledger uses those reviewed summaries directly, which is a cleaner research-level evidence surface than page metadata alone.
- Direct CSV and JSON result artifacts now validate and ingest without requiring a handwritten markdown wrapper.
- The OpenClaw topic-first rerun with `openclaw-results.csv` and `openclaw-results.json` now generates `project_evidence` entries that preserve metric, baseline, and scope signals directly from the raw result files.
- Multi-artifact ingestion now creates an additional aggregated result-evidence entry, which gives downstream claim mapping a stronger project-level view when several result files are supplied together.
- Metric strings such as `success_rate` are now normalized into cleaner evidence text like `success rate` during ingestion.

## Current conclusion

- The topic-driven pipeline is now operational and produces stable outputs.
- Search quality is acceptable for browser-agent themes, improved for OpenClaw/robotics, and cleaner but still narrow for code-retrieval citation themes.
- The current bottleneck is no longer pipeline stability; it is broader source recall, deeper primary-source reading, and stronger handling of explicit metric and benchmark definitions from primary sources.
