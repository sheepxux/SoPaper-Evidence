#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a cautious structured claims draft from a research topic."
    )
    parser.add_argument("topic", help="Research topic or paper theme.")
    parser.add_argument("-o", "--output", help="Write markdown output to file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    topic = args.topic.strip()
    output = render_claims(topic)
    if args.output:
        path = Path(args.output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


def render_claims(topic: str) -> str:
    profile = topic_profile(topic)
    lines = [
        "# Claims List",
        "",
        "## Candidate claims",
        "",
        f"- Claim: {topic} can be positioned against {profile['positioning_target']}.",
        "  Claim type: positioning claim",
        "  Current status: exploratory",
        f"  Evidence needed: {profile['positioning_evidence']}",
        f"  Risk if overstated: {profile['positioning_risk']}",
        f"  Scope limit: {profile['positioning_scope']}",
        "",
        f"- Claim: {topic} requires explicit evidence on {profile['evaluation_focus']} before comparative language is used.",
        "  Claim type: evaluation framing",
        "  Current status: exploratory",
        f"  Evidence needed: {profile['evaluation_evidence']}",
        f"  Risk if overstated: {profile['evaluation_risk']}",
        f"  Scope limit: {profile['evaluation_scope']}",
        "",
        f"- Claim: {topic} may justify a comparative-result claim if {profile['comparative_condition']}.",
        "  Claim type: comparative result",
        "  Current status: blocked",
        f"  Evidence needed: {profile['comparative_evidence']}",
        f"  Risk if overstated: {profile['comparative_risk']}",
        f"  Scope limit: {profile['comparative_scope']}",
        "",
    ]
    return "\n".join(lines)


def topic_profile(topic: str) -> dict[str, str]:
    lowered = topic.lower()
    if any(token in lowered for token in ["browser", "browsing", "web"]):
        return {
            "positioning_target": "relevant browsing-agent benchmarks and prior systems",
            "positioning_evidence": "verified benchmark pages, prior papers, and task-overlap notes",
            "positioning_risk": "benchmark mismatch, open-web vs closed-web mismatch, or weak prior-work framing",
            "positioning_scope": "only for overlapping task families and verified benchmark settings",
            "evaluation_focus": "task setup, benchmark fit, baseline fairness, and result provenance",
            "evaluation_evidence": "benchmark definitions, task-scope notes, baseline set, and reviewed result evidence",
            "evaluation_risk": "unsupported benchmark comparison wording",
            "evaluation_scope": "applies only after benchmark and baseline review",
            "comparative_condition": "reviewed project evidence and direct benchmark-aligned baselines exist",
            "comparative_evidence": "reviewed result artifact, benchmark-aligned metrics, and direct baselines",
            "comparative_risk": "unsupported benchmark win claim",
            "comparative_scope": "blocked until direct benchmark-fit evidence exists",
        }
    if any(token in lowered for token in ["retrieval", "citation", "rag", "code assistant"]):
        return {
            "positioning_target": "relevant retrieval, grounded-generation, and citation-evaluation work",
            "positioning_evidence": "verified papers, benchmark pages, and evaluation-method notes",
            "positioning_risk": "overclaiming transfer from generic QA or retrieval settings",
            "positioning_scope": "only for matching retrieval and evaluation settings",
            "evaluation_focus": "citation quality, retrieval setup, baseline fairness, and result provenance",
            "evaluation_evidence": "metric definitions, benchmark notes, baseline set, and reviewed internal or external result evidence",
            "evaluation_risk": "unsupported citation-quality or benchmark wording",
            "evaluation_scope": "applies only after metric and retrieval-setting review",
            "comparative_condition": "reviewed citation metrics and direct baseline comparisons support it",
            "comparative_evidence": "reviewed result artifact, retrieval baseline set, and citation-aligned metrics",
            "comparative_risk": "unsupported comparative retrieval claim",
            "comparative_scope": "blocked until direct comparative evidence exists",
        }
    return {
        "positioning_target": "relevant prior work and benchmark settings",
        "positioning_evidence": "verified prior papers, benchmark pages, and task-fit notes",
        "positioning_risk": "benchmark mismatch or weak comparison framing",
        "positioning_scope": "only for overlapping task settings and evaluation protocols",
        "evaluation_focus": "evaluation setup, baseline fairness, and result provenance",
        "evaluation_evidence": "benchmark definitions, baseline set, and reviewed internal or external result evidence",
        "evaluation_risk": "unsupported comparative wording",
        "evaluation_scope": "applies only after evidence review",
        "comparative_condition": "reviewed project evidence or primary-source results support it",
        "comparative_evidence": "reviewed result artifact, direct baselines, and metric fit",
        "comparative_risk": "unsupported benchmark win claim",
        "comparative_scope": "blocked until direct evidence exists",
    }


if __name__ == "__main__":
    raise SystemExit(main())
