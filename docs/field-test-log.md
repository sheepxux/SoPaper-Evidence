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
- The next remaining bottleneck is no longer source recall for OpenClaw; it is stronger statement extraction from fetched robotics benchmark notes.

## Current conclusion

- The topic-driven pipeline is now operational and produces stable outputs.
- Search quality is acceptable for browser-agent themes, improved for OpenClaw/robotics, and still weak for code-retrieval citation themes.
- The current bottleneck is no longer pipeline stability; it is source recall and statement quality.
