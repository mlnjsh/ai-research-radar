"""
Weekly digest generator.

Reads all paper JSON files from the past week, ranks them, and produces
a Markdown digest file in ``archive/week-<date>.md``.  Also updates the
digest section in README.md.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

from config import (
    PAPERS_DIR,
    ARCHIVE_DIR,
    README_PATH,
    DISPLAY_CATEGORIES,
    DIGEST_TOP_N,
    DIGEST_LOOKBACK_DAYS,
    DATE_FORMAT,
)
from scanner import Paper

# Markers in README
DIGEST_START = "<!-- DIGEST_START -->"
DIGEST_END = "<!-- DIGEST_END -->"


def _load_papers_since(days: int) -> List[Paper]:
    """Load papers from JSON files within the last *days* days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    papers: list[Paper] = []

    for json_file in sorted(PAPERS_DIR.glob("*.json")):
        try:
            date_str = json_file.stem  # e.g. "2026-02-22"
            file_date = datetime.strptime(date_str, DATE_FORMAT).replace(
                tzinfo=timezone.utc
            )
            if file_date < cutoff:
                continue
        except ValueError:
            continue  # skip non-date filenames

        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            for entry in data:
                papers.append(Paper.from_dict(entry))
        except (json.JSONDecodeError, OSError, TypeError) as exc:
            print(f"[digest] Skipping {json_file}: {exc}")

    return papers


def _trending_keywords(papers: List[Paper], top_n: int = 10) -> List[tuple]:
    """Return the most common keywords from the paper set."""
    counter: Counter = Counter()
    for p in papers:
        for kw in p.keyword_matches:
            counter[kw] += 1
    return counter.most_common(top_n)


def _category_breakdown(papers: List[Paper]) -> Dict[str, int]:
    """Return paper counts per display category."""
    counts: Dict[str, int] = {}
    for p in papers:
        cat = p.display_category or "Uncategorized"
        counts[cat] = counts.get(cat, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def generate_digest(lookback_days: int = DIGEST_LOOKBACK_DAYS) -> str | None:
    """
    Generate a weekly digest Markdown document.

    Returns the file path of the created digest, or ``None`` if no
    papers were found.
    """
    papers = _load_papers_since(lookback_days)
    if not papers:
        print("[digest] No papers found for digest period.")
        return None

    # Sort by relevance
    papers.sort(key=lambda p: p.relevance_score, reverse=True)
    top_papers = papers[:DIGEST_TOP_N]

    today = datetime.now(timezone.utc).strftime(DATE_FORMAT)
    week_start = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime(DATE_FORMAT)

    trending = _trending_keywords(papers)
    breakdown = _category_breakdown(papers)
    unique_authors = set()
    for p in papers:
        unique_authors.update(p.authors)

    # Build the digest Markdown
    lines: list[str] = [
        f"# Weekly Digest: {week_start} to {today}",
        "",
        f"**Total papers scanned:** {len(papers)}  ",
        f"**Unique authors:** {len(unique_authors)}  ",
        f"**Categories covered:** {len(breakdown)}",
        "",
        "---",
        "",
        f"## Top {len(top_papers)} Papers This Week",
        "",
    ]

    for i, p in enumerate(top_papers, 1):
        authors_str = ", ".join(p.authors[:3])
        if len(p.authors) > 3:
            authors_str += " et al."
        lines.append(f"### {i}. {p.title}")
        lines.append(f"**Authors:** {authors_str}  ")
        lines.append(f"**Category:** {p.display_category} | **arXiv:** [{p.arxiv_id}]({p.url})  ")
        if p.summary:
            lines.append(f"**Summary:** {p.summary}  ")
        if p.keyword_matches:
            lines.append(f"**Keywords matched:** {', '.join(p.keyword_matches)}")
        lines.append("")

    # Trending keywords section
    lines.extend([
        "---",
        "",
        "## Trending Keywords",
        "",
        "| Keyword | Count |",
        "|:--------|------:|",
    ])
    for kw, count in trending:
        lines.append(f"| {kw} | {count} |")

    # Category breakdown
    lines.extend([
        "",
        "---",
        "",
        "## Category Breakdown",
        "",
        "| Category | Papers |",
        "|:---------|-------:|",
    ])
    for cat, count in breakdown.items():
        emoji = DISPLAY_CATEGORIES.get(cat, {}).get("emoji", "")
        lines.append(f"| {emoji} {cat} | {count} |")

    lines.extend([
        "",
        "---",
        "",
        f"*Generated on {today} by [AI Research Radar](https://github.com/mlnjsh/ai-research-radar)*",
    ])

    digest_text = "\n".join(lines)

    # Save the digest file
    digest_filename = f"week-{today}.md"
    digest_path = ARCHIVE_DIR / digest_filename
    digest_path.write_text(digest_text, encoding="utf-8")
    print(f"[digest] Digest written to {digest_path}")

    # Update the digest section in README
    _update_readme_digest(top_papers, today, len(papers))

    return str(digest_path)


def _update_readme_digest(
    top_papers: List[Paper],
    date: str,
    total: int,
) -> None:
    """Replace the digest section in README.md with a summary."""
    readme_text = README_PATH.read_text(encoding="utf-8")

    start_idx = readme_text.find(DIGEST_START)
    end_idx = readme_text.find(DIGEST_END)
    if start_idx == -1 or end_idx == -1:
        print("[digest] WARNING: DIGEST markers not found in README.md")
        return

    lines = [
        f"**Week of {date}** | {total} papers scanned\n",
    ]
    for i, p in enumerate(top_papers[:5], 1):
        lines.append(f"{i}. [{p.title}]({p.url})")
    lines.append(f"\n**[View full digest and archives](archive/week-{date}.md)**")

    content = "\n".join(lines)
    before = readme_text[: start_idx + len(DIGEST_START)]
    after = readme_text[end_idx:]
    readme_text = f"{before}\n\n{content}\n\n{after}"

    README_PATH.write_text(readme_text, encoding="utf-8")
    print("[digest] README.md digest section updated")


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = generate_digest()
    if result:
        print(f"Digest saved to: {result}")
    else:
        print("No papers found for the digest period.")
