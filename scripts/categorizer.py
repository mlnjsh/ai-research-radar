"""
Paper categorizer.

Assigns each paper to one of the display categories defined in
``config.DISPLAY_CATEGORIES`` by matching arXiv categories and keywords
against the paper's primary category, title, and abstract.
"""

from __future__ import annotations

from typing import Dict, List

from config import DISPLAY_CATEGORIES
from scanner import Paper


def categorize_paper(paper: Paper) -> str:
    """
    Return the best display-category name for *paper*.

    Scoring:
    - +3 points if the paper's primary arXiv category appears in the
      display category's ``arxiv_cats`` list.
    - +1 point for each display-category keyword found in the paper's
      title or abstract (case-insensitive).

    Falls back to ``"Machine Learning & Deep Learning"`` when no
    category scores any points.
    """
    text = f"{paper.title} {paper.abstract}".lower()
    best_name = "Machine Learning & Deep Learning"
    best_score = 0

    for name, info in DISPLAY_CATEGORIES.items():
        score = 0

        # arXiv category match
        if paper.primary_category in info["arxiv_cats"]:
            score += 3
        # Also check non-primary categories
        for cat in paper.categories:
            if cat in info["arxiv_cats"]:
                score += 1

        # Keyword match
        for kw in info["keywords"]:
            if kw.lower() in text:
                score += 1

        if score > best_score:
            best_score = score
            best_name = name

    return best_name


def categorize_papers(papers: List[Paper]) -> Dict[str, List[Paper]]:
    """
    Assign each paper to a display category.

    Returns a dict mapping category names to lists of papers.  Every
    category key from ``DISPLAY_CATEGORIES`` is present (possibly with
    an empty list).
    """
    result: Dict[str, List[Paper]] = {name: [] for name in DISPLAY_CATEGORIES}

    for paper in papers:
        cat = categorize_paper(paper)
        paper.display_category = cat
        result[cat].append(paper)

    # Sort each category by relevance score descending
    for cat_papers in result.values():
        cat_papers.sort(key=lambda p: p.relevance_score, reverse=True)

    return result


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from scanner import fetch_papers

    papers = fetch_papers()
    categorized = categorize_papers(papers)

    for cat_name, cat_papers in categorized.items():
        info = DISPLAY_CATEGORIES[cat_name]
        print(f"\n{info['emoji']} {cat_name} ({len(cat_papers)} papers)")
        for p in cat_papers[:5]:
            print(f"   - {p.title[:70]}")
