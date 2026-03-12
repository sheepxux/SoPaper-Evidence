#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>]+")


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta":
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            content = attr_map.get("content", "").strip()
            if name and content:
                self.meta[name] = content
            if prop and content:
                self.meta[prop] = content

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch external URLs from markdown/text files or direct URL arguments and generate "
            "structured source-note drafts."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Markdown/text files and/or direct URLs.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for generated source-note markdown files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout in seconds. Default: 15",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = collect_urls(args.inputs)
    if not urls:
        print("No external URLs found.", file=sys.stderr)
        return 1

    for index, url in enumerate(urls, start=1):
        try:
            note = fetch_note(url, timeout=args.timeout)
        except Exception as exc:  # pragma: no cover
            note = render_failure_note(url, str(exc))

        slug = slugify(note["title"] or guess_title_from_url(url))
        path = output_dir / f"{index:02d}-{slug}.md"
        path.write_text(render_note(note), encoding="utf-8")
        print(path)

    return 0


def collect_urls(values: list[str]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value.startswith(("http://", "https://")):
            add_url(found, seen, value)
            continue

        path = Path(value).expanduser().resolve()
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for _, locator in MARKDOWN_LINK_RE.findall(text):
            add_url(found, seen, locator)
        for locator in BARE_URL_RE.findall(text):
            add_url(found, seen, locator)
    return found


def add_url(found: list[str], seen: set[str], url: str) -> None:
    cleaned = url.strip().rstrip(").,")
    if cleaned not in seen:
        seen.add(cleaned)
        found.append(cleaned)


def fetch_note(url: str, *, timeout: int) -> dict[str, str]:
    request = Request(
        url,
        headers={
            "User-Agent": "SopaperEvidenceBot/0.6 (+https://github.com/sheepxux/SoPaper-Evidence)"
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in {301, 302, 303, 307, 308} and exc.headers.get("Location"):
            redirected = exc.headers["Location"]
            return fetch_note(redirected, timeout=timeout)
        raise

    parser = MetaParser()
    parser.feed(raw)

    title = clean_text(
        parser.meta.get("citation_title")
        or parser.meta.get("og:title")
        or parser.title
        or guess_title_from_url(url)
    )
    description = clean_text(
        parser.meta.get("description")
        or parser.meta.get("og:description")
        or parser.meta.get("twitter:description")
    )
    source_type = guess_external_source_type(url, content_type)
    access_date = datetime.now(timezone.utc).date().isoformat()
    facts = []
    if title:
        facts.append(f'Fetched page title: "{title}".')
    if description:
        facts.append(f"Meta description: {description}")
    if source_type == "paper" and "arxiv.org" in urlparse(url).netloc.lower():
        facts.append("Source host is arXiv, which is usually a primary paper distribution channel.")

    return {
        "title": title or guess_title_from_url(url),
        "url": url,
        "source_type": source_type,
        "access_date": access_date,
        "facts": " ".join(facts) if facts else "TODO: add reviewed facts from the fetched source.",
        "relevance": "TODO: explain why this fetched source matters for the current evidence pack.",
        "comparable": "TODO: state whether the source is directly comparable, partially comparable, or only contextual.",
        "limits": "TODO: state scope limits, benchmark mismatch risk, or unresolved verification gaps.",
        "verification": "fetched-primary-review-required",
    }


def render_failure_note(url: str, error: str) -> dict[str, str]:
    return {
        "title": guess_title_from_url(url),
        "url": url,
        "source_type": "other",
        "access_date": datetime.now(timezone.utc).date().isoformat(),
        "facts": f"TODO: fetch failed with error: {error}",
        "relevance": "TODO: retry fetch or review manually.",
        "comparable": "unknown",
        "limits": "fetch failed; source content not reviewed.",
        "verification": "fetch-failed",
    }


def render_note(note: dict[str, str]) -> str:
    return "\n".join(
        [
            "# Source Note",
            "",
            "## Title",
            "",
            f"- Title: {note['title']}",
            "",
            "## Source",
            "",
            f"- Source type: {note['source_type']}",
            f"- Locator: {note['url']}",
            f"- Access date: {note['access_date']}",
            "- Task: TODO",
            "- Metrics: TODO",
            f"- Verification status: {note['verification']}",
            "",
            "## Why it matters",
            "",
            f"- Relevance to our paper: {note['relevance']}",
            f"- Comparable to us: {note['comparable']}",
            "",
            "## Key facts",
            "",
            f"- Fact: {note['facts']}",
            "",
            "## Limits",
            "",
            f"- Limit: {note['limits']}",
            "",
            "## Reviewer risk",
            "",
            "- Risk: TODO",
            "- Risk: TODO",
            "",
        ]
    )


def guess_external_source_type(locator: str, content_type: str) -> str:
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
    if "html" in content_type.lower() or host:
        return "official_doc"
    return "other"


def guess_title_from_url(locator: str) -> str:
    parsed = urlparse(locator)
    if parsed.netloc:
        tail = parsed.path.rstrip("/").split("/")[-1]
        return (tail or parsed.netloc).replace("-", " ").replace("_", " ")
    return locator


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return cleaned[:50] or "source-note"


def clean_text(value: str) -> str:
    collapsed = re.sub(r"\s+", " ", html.unescape(value or "")).strip()
    return collapsed


if __name__ == "__main__":
    raise SystemExit(main())
