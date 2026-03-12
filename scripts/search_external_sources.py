#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urlparse
from urllib.request import Request, urlopen


QUERY_LINE_RE = re.compile(r"^- Query:\s*(.+)\s*$")
RESULT_LINK_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search external sources from a topic or query plan and emit a markdown source list."
    )
    parser.add_argument("--topic", help="Research topic used to build default queries.")
    parser.add_argument("--plan", help="Markdown search-plan file containing '- Query:' lines.")
    parser.add_argument("--output", required=True, help="Markdown output file.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum number of results. Default: 8")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queries = collect_queries(args.topic, args.plan)
    if not queries:
        print("No queries available. Provide --topic or --plan.", file=sys.stderr)
        return 1

    results = search_queries(queries, args.limit)
    output = render_source_list(args.topic or "Topic search", queries, results)
    path = Path(args.output).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")
    print(path)
    return 0


def collect_queries(topic: str | None, plan_path: str | None) -> list[str]:
    queries: list[str] = []
    if topic:
        queries.extend(
            [
                f"{topic} paper arxiv benchmark",
                f"{topic} benchmark dataset",
                f"{topic} github repo",
                f"{topic} official documentation",
            ]
        )
    if plan_path:
        text = Path(plan_path).expanduser().resolve().read_text(encoding="utf-8")
        queries.extend(match.group(1).strip() for match in QUERY_LINE_RE.finditer(text))
    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        if query not in seen:
            seen.add(query)
            deduped.append(query)
    return deduped


def search_queries(queries: list[str], limit: int) -> list[dict[str, str]]:
    seen: set[str] = set()
    results: list[dict[str, str]] = []

    for query in queries:
        for result in search_duckduckgo(query):
            if should_skip_result(result["url"]):
                continue
            canonical = canonicalize_url(result["url"])
            if canonical in seen:
                continue
            seen.add(canonical)
            results.append(result | {"query": query})
            if len(results) >= limit:
                return results
    return results


def search_duckduckgo(query: str) -> list[dict[str, str]]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="replace")
    results: list[dict[str, str]] = []
    for match in RESULT_LINK_RE.finditer(raw):
        href = extract_result_url(match.group("href"))
        title = clean_text(re.sub(r"<[^>]+>", " ", match.group("title")))
        if title and href and href.startswith("http"):
            results.append({"title": title, "url": href})
    return results


def render_source_list(topic: str, queries: list[str], results: list[dict[str, str]]) -> str:
    lines = [
        "# Topic Search Source List",
        "",
        f"- Topic: {topic}",
        "",
        "## Queries",
        "",
    ]
    for query in queries:
        lines.append(f"- Query: {query}")

    lines.extend(["", "## Results", ""])
    if not results:
        lines.append("- No results found.")
    for result in results:
        host = urlparse(result["url"]).netloc
        lines.append(f"- [{escape_brackets(result['title'])}]({result['url']})")
        lines.append(f"  - Source host: {host}")
        lines.append(f"  - Found via query: {result['query']}")
    lines.append("")
    return "\n".join(lines)


def extract_result_url(href: str) -> str:
    if href.startswith("//"):
        href = "https:" + href
    href = html.unescape(href)
    parsed = urlparse(href)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        uddg = parse_qs(parsed.query).get("uddg")
        if uddg:
            return unquote(uddg[0])
    return href


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.netloc.lower()}{parsed.path.rstrip('/')}"


def should_skip_result(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    return (
        "duckduckgo.com" in host
        or parsed.path.endswith(".pdf")
        or "researchgate.net" in host
        or "semanticscholar.org" in host
    )


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def escape_brackets(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


if __name__ == "__main__":
    raise SystemExit(main())
