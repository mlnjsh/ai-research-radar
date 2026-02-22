"""
Optional AI-powered paper summarizer.

Generates one-line summaries for papers using the OpenAI API when an
``OPENAI_API_KEY`` environment variable is set.  If the key is absent
the module silently falls back to a simple extractive summary built
from the first sentence of the abstract.
"""

from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from config import (
    ENABLE_AI_SUMMARIES,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    SUMMARY_MAX_TOKENS,
    SUMMARIES_DIR,
    DATE_FORMAT,
)
from scanner import Paper


# ---------------------------------------------------------------------------
# Fallback extractive summary
# ---------------------------------------------------------------------------

def _extractive_summary(abstract: str, max_chars: int = 200) -> str:
    """Return the first sentence of *abstract*, truncated to *max_chars*."""
    # Try splitting on ". " first
    parts = abstract.split(". ")
    first = parts[0].strip()
    if not first.endswith("."):
        first += "."
    if len(first) > max_chars:
        first = first[: max_chars - 3].rsplit(" ", 1)[0] + "..."
    return first


# ---------------------------------------------------------------------------
# OpenAI-based summary
# ---------------------------------------------------------------------------

def _openai_summary(title: str, abstract: str) -> str:
    """Call the OpenAI chat completions API and return a one-line summary."""
    url = "https://api.openai.com/v1/chat/completions"
    prompt = (
        "You are a research paper summarizer. Given the title and abstract "
        "of an academic paper, produce a single concise sentence (max 30 words) "
        "that captures the key contribution.\n\n"
        f"Title: {title}\n\n"
        f"Abstract: {abstract}\n\n"
        "One-line summary:"
    )
    payload = json.dumps({
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": SUMMARY_MAX_TOKENS,
        "temperature": 0.3,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def summarize_paper(paper: Paper) -> str:
    """
    Return a short summary for *paper*.

    Uses OpenAI when available; otherwise falls back to the first
    sentence of the abstract.
    """
    if ENABLE_AI_SUMMARIES:
        try:
            return _openai_summary(paper.title, paper.abstract)
        except Exception as exc:
            print(f"[summarizer] OpenAI error for {paper.arxiv_id}: {exc}")
    return _extractive_summary(paper.abstract)


def summarize_papers(papers: List[Paper]) -> List[Paper]:
    """
    Populate the ``summary`` field on each paper in *papers*.

    Also persists summaries to ``data/summaries/<date>.json``.
    """
    summaries_today: Dict[str, str] = {}

    for paper in papers:
        if not paper.summary:
            paper.summary = summarize_paper(paper)
        summaries_today[paper.arxiv_id] = paper.summary

    # Persist summaries
    today = datetime.utcnow().strftime(DATE_FORMAT)
    summary_file = SUMMARIES_DIR / f"{today}.json"

    existing: Dict[str, str] = {}
    if summary_file.exists():
        try:
            existing = json.loads(summary_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    existing.update(summaries_today)
    summary_file.write_text(
        json.dumps(existing, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[summarizer] Saved {len(summaries_today)} summaries to {summary_file}")
    return papers


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from scanner import fetch_papers

    papers = fetch_papers()
    papers = summarize_papers(papers[:5])
    for p in papers:
        print(f"  {p.title[:60]}")
        print(f"    => {p.summary}\n")
