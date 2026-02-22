"""
README updater.

Reads ``README.md``, replaces content between the marker comments
``<!-- PAPERS_START -->`` / ``<!-- PAPERS_END -->``, and writes the
file back with updated paper tables, trending topics, and stats.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List

from config import (
    README_PATH,
    DISPLAY_CATEGORIES,
    MAX_PAPERS_PER_CATEGORY,
    STATUS_FILE,
    DATE_FORMAT,
)
from scanner import Paper


# ---------------------------------------------------------------------------
# Marker constants
# ---------------------------------------------------------------------------
PAPERS_START = "<!-- PAPERS_START -->"
PAPERS_END = "<!-- PAPERS_END -->"
TRENDS_START = "<!-- TRENDS_START -->"
TRENDS_END = "<!-- TRENDS_END -->"
STATS_START = "<!-- STATS_START -->"
STATS_END = "<!-- STATS_END -->"


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------

def _short_authors(authors: List[str], max_display: int = 3) -> str:
    """Return a compact author string, e.g. 'A. Smith, B. Jones et al.'"""
    if not authors:
        return "---"
    if len(authors) <= max_display:
        return ", ".join(authors)
    return ", ".join(authors[:max_display]) + " et al."


def _render_paper_row(idx: int, paper: Paper) -> str:
    """Render a single Markdown table row for a paper."""
    title_link = f"[{paper.title}]({paper.url})"
    authors = _short_authors(paper.authors)
    cat = paper.primary_category
    try:
        date = datetime.fromisoformat(
            paper.published.replace("Z", "+00:00")
        ).strftime(DATE_FORMAT)
    except (ValueError, TypeError):
        date = paper.published[:10] if paper.published else "---"
    return f"| {idx} | {title_link} | {authors} | {cat} | {date} |"


def _render_category_table(name: str, papers: List[Paper]) -> str:
    """Build a complete Markdown section for one display category."""
    info = DISPLAY_CATEGORIES.get(name, {})
    emoji = info.get("emoji", "")
    header = f"### {emoji} {name}\n"
    table_header = (
        "| # | Paper | Authors | Category | Date |\n"
        "|:-:|:------|:--------|:--------:|:----:|"
    )

    if not papers:
        rows = "| 1 | *No new papers in this category* | --- | --- | --- |"
    else:
        display = papers[:MAX_PAPERS_PER_CATEGORY]
        rows = "\n".join(_render_paper_row(i, p) for i, p in enumerate(display, 1))

    return f"{header}\n{table_header}\n{rows}\n"


def build_papers_section(categorized: Dict[str, List[Paper]]) -> str:
    """Build the full papers section to go between the marker comments."""
    sections: list[str] = []
    for name in DISPLAY_CATEGORIES:
        papers = categorized.get(name, [])
        sections.append(_render_category_table(name, papers))
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Trending topics
# ---------------------------------------------------------------------------

def _build_trending_section(categorized: Dict[str, List[Paper]]) -> str:
    """Build a simple trending-topics text block."""
    from collections import Counter
    keyword_counter: Counter = Counter()
    total = 0
    for papers in categorized.values():
        total += len(papers)
        for p in papers:
            for kw in p.keyword_matches:
                keyword_counter[kw] += 1

    if not keyword_counter:
        return (
            "```\n"
            "TRENDING TOPICS (Last 24 Hours)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "No keyword matches detected in this scan cycle.\n"
            "Check back after the next scan.\n"
            "```"
        )

    lines = [
        "```",
        "TRENDING TOPICS (Last 24 Hours)",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]
    for kw, count in keyword_counter.most_common(10):
        bar = "█" * min(count, 20)
        lines.append(f"  {bar} {kw} ({count})")
    lines.append(f"\n  Total papers scanned: {total}")
    lines.append("```")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def _build_stats_section(categorized: Dict[str, List[Paper]]) -> str:
    """Build the stats section."""
    total = sum(len(ps) for ps in categorized.values())
    unique_authors: set[str] = set()
    for ps in categorized.values():
        for p in ps:
            unique_authors.update(p.authors)
    topics: set[str] = set()
    for ps in categorized.values():
        for p in ps:
            topics.update(p.keyword_matches)

    # Read cumulative count from status file
    cumulative = total
    if STATUS_FILE.exists():
        try:
            status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
            cumulative = status.get("total_papers_tracked", 0) + total
        except (json.JSONDecodeError, OSError):
            pass

    return (
        "```\n"
        f"Papers Scanned:     {cumulative}\n"
        f"Categories:         {len(DISPLAY_CATEGORIES)}\n"
        f"Unique Authors:     {len(unique_authors)}\n"
        f"Trending Topics:    {len(topics)}\n"
        f"Weekly Digests:     (auto-generated Mondays)\n"
        "```"
    )


# ---------------------------------------------------------------------------
# Main update routine
# ---------------------------------------------------------------------------

def _replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    """Replace content between two marker comments in *text*."""
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        print(f"[readme_updater] WARNING: markers {start_marker} / {end_marker} not found")
        return text
    before = text[: start_idx + len(start_marker)]
    after = text[end_idx:]
    return f"{before}\n\n{replacement}\n\n{after}"


def update_readme(categorized: Dict[str, List[Paper]]) -> None:
    """
    Read README.md, replace the papers / trends / stats sections, and
    write the file back.
    """
    readme_text = README_PATH.read_text(encoding="utf-8")

    # Papers section
    papers_content = build_papers_section(categorized)
    readme_text = _replace_between(readme_text, PAPERS_START, PAPERS_END, papers_content)

    # Trending section
    trends_content = _build_trending_section(categorized)
    readme_text = _replace_between(readme_text, TRENDS_START, TRENDS_END, trends_content)

    # Stats section
    stats_content = _build_stats_section(categorized)
    readme_text = _replace_between(readme_text, STATS_START, STATS_END, stats_content)

    README_PATH.write_text(readme_text, encoding="utf-8")
    print(f"[readme_updater] README.md updated at {README_PATH}")


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from scanner import fetch_papers
    from categorizer import categorize_papers

    papers = fetch_papers()
    categorized = categorize_papers(papers)
    update_readme(categorized)
