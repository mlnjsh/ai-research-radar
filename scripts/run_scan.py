#!/usr/bin/env python3
"""
Main entry point for the AI Research Radar pipeline.

Orchestrates the full scan cycle:
  1. Fetch papers from arXiv
  2. Categorize papers
  3. Generate summaries (optional, needs OPENAI_API_KEY)
  4. Update README.md
  5. Persist paper data and status
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure the scripts directory is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    PAPERS_DIR,
    STATUS_FILE,
    DATE_FORMAT,
    DATETIME_FORMAT,
    ENABLE_AI_SUMMARIES,
)
from scanner import fetch_papers
from categorizer import categorize_papers
from summarizer import summarize_papers
from readme_updater import update_readme


def _save_papers(papers, today: str) -> Path:
    """Persist today's papers to a JSON file."""
    papers_file = PAPERS_DIR / f"{today}.json"

    # Load existing papers for today (if any) to avoid duplicates
    existing_ids: set[str] = set()
    existing_data: list[dict] = []
    if papers_file.exists():
        try:
            existing_data = json.loads(papers_file.read_text(encoding="utf-8"))
            existing_ids = {p["arxiv_id"] for p in existing_data}
        except (json.JSONDecodeError, OSError):
            pass

    # Merge new papers
    new_count = 0
    for paper in papers:
        if paper.arxiv_id not in existing_ids:
            existing_data.append(paper.to_dict())
            existing_ids.add(paper.arxiv_id)
            new_count += 1

    papers_file.write_text(
        json.dumps(existing_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[run_scan] Saved {new_count} new papers ({len(existing_data)} total today) to {papers_file}")
    return papers_file


def _update_status(total_new: int, total_today: int, today: str) -> None:
    """Update the status.json file."""
    existing: dict = {}
    if STATUS_FILE.exists():
        try:
            existing = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    existing["last_updated"] = datetime.now(timezone.utc).strftime(DATETIME_FORMAT)
    existing["last_scan_date"] = today
    existing["papers_found_last_scan"] = total_new
    existing["papers_today"] = total_today
    existing["total_papers_tracked"] = existing.get("total_papers_tracked", 0) + total_new
    existing["total_scans"] = existing.get("total_scans", 0) + 1
    existing["ai_summaries_enabled"] = ENABLE_AI_SUMMARIES

    STATUS_FILE.write_text(
        json.dumps(existing, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[run_scan] Status updated: {STATUS_FILE}")


def main() -> None:
    """Run the full scan pipeline."""
    print("=" * 60)
    print("  AI Research Radar - Scan Pipeline")
    print("=" * 60)

    today = datetime.now(timezone.utc).strftime(DATE_FORMAT)

    # Step 1: Fetch papers
    print("\n[Step 1/5] Fetching papers from arXiv...")
    papers = fetch_papers()
    if not papers:
        print("[run_scan] No papers found. Exiting.")
        _update_status(0, 0, today)
        return

    # Step 2: Categorize
    print("\n[Step 2/5] Categorizing papers...")
    categorized = categorize_papers(papers)
    for cat_name, cat_papers in categorized.items():
        print(f"  {cat_name}: {len(cat_papers)} papers")

    # Step 3: Summarize
    print("\n[Step 3/5] Generating summaries...")
    if ENABLE_AI_SUMMARIES:
        print("  AI summaries enabled (OpenAI)")
    else:
        print("  AI summaries disabled (no OPENAI_API_KEY), using extractive fallback")
    papers = summarize_papers(papers)

    # Step 4: Update README
    print("\n[Step 4/5] Updating README.md...")
    update_readme(categorized)

    # Step 5: Persist data
    print("\n[Step 5/5] Saving paper data and status...")
    _save_papers(papers, today)
    _update_status(len(papers), len(papers), today)

    print("\n" + "=" * 60)
    print(f"  Scan complete! {len(papers)} papers processed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
