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
    lines = [
        "# Claims List",
        "",
        "## Candidate claims",
        "",
        f"- Claim: {topic} can be positioned against relevant prior work and benchmark settings.",
        "  Claim type: positioning claim",
        "  Current status: exploratory",
        "  Evidence needed: verified prior papers, benchmark pages, and task-fit notes",
        "  Risk if overstated: benchmark mismatch or weak comparison framing",
        "  Scope limit: only for overlapping task settings and evaluation protocols",
        "",
        f"- Claim: {topic} requires explicit evidence on evaluation setup, baseline fairness, and result provenance before comparative language is used.",
        "  Claim type: evaluation framing",
        "  Current status: exploratory",
        "  Evidence needed: benchmark definitions, baseline set, and reviewed internal or external result evidence",
        "  Risk if overstated: unsupported comparative wording",
        "  Scope limit: applies only after evidence review",
        "",
        f"- Claim: {topic} may justify a comparative-result claim if reviewed project evidence or primary-source results support it.",
        "  Claim type: comparative result",
        "  Current status: blocked",
        "  Evidence needed: reviewed result artifact, direct baselines, and metric fit",
        "  Risk if overstated: unsupported benchmark win claim",
        "  Scope limit: blocked until direct evidence exists",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
