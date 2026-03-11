#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>]+")
HEADING_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$")


@dataclass(frozen=True)
class SourceItem:
    title: str
    locator: str
    source_type: str
    classification: str
    origin: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a markdown evidence ledger draft from local markdown/text files. "
            "The script extracts markdown links, bare URLs, and the input files themselves "
            "as candidate evidence items."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Markdown or text files to scan for evidence sources.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write the ledger to this file instead of stdout.",
    )
    parser.add_argument(
        "--id-prefix",
        default="E",
        help="Prefix for evidence ids. Default: E",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_paths = [Path(value).expanduser().resolve() for value in args.inputs]
    missing = [str(path) for path in input_paths if not path.exists()]
    if missing:
        for item in missing:
            print(f"Missing input: {item}", file=sys.stderr)
        return 1

    sources = collect_sources(input_paths)
    output = render_ledger(sources, args.id_prefix)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


def collect_sources(paths: Iterable[Path]) -> list[SourceItem]:
    seen: set[tuple[str, str]] = set()
    items: list[SourceItem] = []

    for path in paths:
        if path.is_file():
            local_source = SourceItem(
                title=extract_local_title(path),
                locator=str(path),
                source_type=guess_local_source_type(path),
                classification=guess_local_classification(path),
                origin=path.name,
            )
            add_source(items, seen, local_source)

            if path.suffix.lower() not in {".md", ".txt"}:
                continue

            text = path.read_text(encoding="utf-8")
            for title, locator in extract_markdown_links(text):
                add_source(
                    items,
                    seen,
                    SourceItem(
                        title=title,
                        locator=locator,
                        source_type=guess_external_source_type(locator),
                        classification="unverified",
                        origin=path.name,
                    ),
                )
            for locator in extract_bare_urls(text):
                add_source(
                    items,
                    seen,
                    SourceItem(
                        title=guess_title_from_url(locator),
                        locator=locator,
                        source_type=guess_external_source_type(locator),
                        classification="unverified",
                        origin=path.name,
                    ),
                )

    return items


def add_source(items: list[SourceItem], seen: set[tuple[str, str]], source: SourceItem) -> None:
    key = (source.locator, source.origin)
    if key in seen:
        return
    seen.add(key)
    items.append(source)


def extract_local_title(path: Path) -> str:
    if path.suffix.lower() in {".md", ".txt"}:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = HEADING_RE.match(line)
            if match:
                return match.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").strip() or path.name


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for title, locator in MARKDOWN_LINK_RE.findall(text):
        if locator.startswith("#"):
            continue
        results.append((title.strip() or guess_title_from_url(locator), locator.strip()))
    return results


def extract_bare_urls(text: str) -> list[str]:
    linked_urls = {locator for _, locator in extract_markdown_links(text)}
    urls = []
    for match in BARE_URL_RE.findall(text):
        if match not in linked_urls:
            urls.append(match)
    return urls


def guess_external_source_type(locator: str) -> str:
    parsed = urlparse(locator)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "arxiv.org" in host or "doi.org" in host:
        return "paper"
    if "github.com" in host or "gitlab.com" in host:
        return "repo"
    if any(token in host for token in ["paperswithcode.com", "huggingface.co"]):
        return "benchmark"
    if any(token in path for token in ["/dataset", "/datasets"]):
        return "dataset"
    return "official_doc" if host else "other"


def guess_local_source_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return "note"
    if suffix in {".json", ".yaml", ".yml", ".toml"}:
        return "local_code"
    if suffix in {".csv", ".tsv"}:
        return "local_result"
    return "local_code"


def guess_local_classification(path: Path) -> str:
    source_type = guess_local_source_type(path)
    if source_type == "local_result":
        return "project_evidence"
    return "unverified"


def guess_title_from_url(locator: str) -> str:
    parsed = urlparse(locator)
    if parsed.netloc:
        tail = parsed.path.rstrip("/").split("/")[-1]
        if tail:
            return tail.replace("-", " ").replace("_", " ")
        return parsed.netloc
    return locator


def render_ledger(sources: list[SourceItem], id_prefix: str) -> str:
    lines = [
        "# Evidence Ledger Draft",
        "",
        "This draft was generated automatically. Review every item before using it in paper writing.",
        "",
    ]

    for index, source in enumerate(sources, start=1):
        lines.extend(
            [
                f"- id: {id_prefix}{index:02d}",
                f"  statement: \"TODO: summarize the exact claim or observation from {source.title}.\"",
                f"  classification: {source.classification}",
                f"  source_type: {source.source_type}",
                f"  source_title: \"{escape_quotes(source.title)}\"",
                f"  source_locator: \"{escape_quotes(source.locator)}\"",
                "  date: \"unknown\"",
                f"  relevance: \"TODO: explain why this source matters for the paper. Found in {source.origin}.\"",
                "  limitations: \"TODO: state scope limits, comparability risks, or verification gaps.\"",
                "",
            ]
        )

    if not sources:
        lines.extend(
            [
                "No sources were extracted.",
                "",
                "Check that the input files contain markdown links, URLs, or useful local artifacts.",
                "",
            ]
        )

    return "\n".join(lines)


def escape_quotes(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    raise SystemExit(main())
