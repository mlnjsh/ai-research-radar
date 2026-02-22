"""
arXiv paper scanner.

Fetches recent papers from the arXiv Atom API using only the standard
library (urllib + xml.etree.ElementTree).  Falls back to the *requests*
library if available but does not require it.
"""

from __future__ import annotations

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from typing import List

from config import (
    ARXIV_API_URL,
    ARXIV_CATEGORIES,
    MAX_RESULTS_PER_QUERY,
    FETCH_WINDOW_HOURS,
    PRIORITY_KEYWORDS,
)

# Atom namespace used in the arXiv API responses
ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"


@dataclass
class Paper:
    """Lightweight representation of an arXiv paper."""
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]
    primary_category: str
    published: str          # ISO-8601 string
    updated: str            # ISO-8601 string
    url: str
    pdf_url: str
    relevance_score: float = 0.0
    display_category: str = ""
    summary: str = ""
    keyword_matches: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Paper":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


def _fetch_url(url: str) -> str:
    """Fetch a URL and return the response body as a string."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AIResearchRadar/1.0 (GitHub Actions)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _build_query(categories: List[str], max_results: int) -> str:
    """
    Build an arXiv API query URL.

    Uses the ``cat:`` prefix to search by category, combining multiple
    categories with ``OR``.
    """
    cat_query = " OR ".join(f"cat:{c}" for c in categories)
    params = {
        "search_query": cat_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"


def _parse_entry(entry: ET.Element) -> Paper:
    """Parse a single Atom <entry> element into a Paper."""
    def _text(tag: str, ns: str = ATOM_NS) -> str:
        el = entry.find(f"{{{ns}}}{tag}")
        return (el.text or "").strip() if el is not None else ""

    title = " ".join(_text("title").split())  # collapse whitespace
    abstract = " ".join(_text("summary").split())

    authors: list[str] = []
    for author_el in entry.findall(f"{{{ATOM_NS}}}author"):
        name_el = author_el.find(f"{{{ATOM_NS}}}name")
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())

    # Links
    url = ""
    pdf_url = ""
    for link_el in entry.findall(f"{{{ATOM_NS}}}link"):
        href = link_el.get("href", "")
        if link_el.get("title") == "pdf":
            pdf_url = href
        elif link_el.get("rel") == "alternate":
            url = href

    # Categories
    categories: list[str] = []
    for cat_el in entry.findall(f"{{{ATOM_NS}}}category"):
        term = cat_el.get("term", "")
        if term:
            categories.append(term)

    primary_cat_el = entry.find(f"{{{ARXIV_NS}}}primary_category")
    primary_category = primary_cat_el.get("term", "") if primary_cat_el is not None else (categories[0] if categories else "")

    # Extract arXiv ID from the <id> tag (e.g. http://arxiv.org/abs/2401.12345v1)
    raw_id = _text("id")
    arxiv_id = raw_id.split("/abs/")[-1] if "/abs/" in raw_id else raw_id

    return Paper(
        arxiv_id=arxiv_id,
        title=title,
        authors=authors,
        abstract=abstract,
        categories=categories,
        primary_category=primary_category,
        published=_text("published"),
        updated=_text("updated"),
        url=url or raw_id,
        pdf_url=pdf_url,
    )


def _compute_relevance(paper: Paper) -> Paper:
    """Compute a relevance score based on priority keyword matches."""
    text = f"{paper.title} {paper.abstract}".lower()
    matches: list[str] = []
    for kw in PRIORITY_KEYWORDS:
        if kw.lower() in text:
            matches.append(kw)
    paper.keyword_matches = matches
    paper.relevance_score = len(matches) * 10.0  # simple scoring
    return paper


def _is_recent(paper: Paper, hours: int) -> bool:
    """Return True if the paper was published within the look-back window."""
    try:
        pub = datetime.fromisoformat(paper.published.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        return pub >= cutoff
    except (ValueError, TypeError):
        return True  # keep paper if we cannot parse the date


def fetch_papers(
    categories: List[str] | None = None,
    max_results: int = MAX_RESULTS_PER_QUERY,
    window_hours: int = FETCH_WINDOW_HOURS,
) -> List[Paper]:
    """
    Fetch recent papers from arXiv.

    Parameters
    ----------
    categories : list[str], optional
        arXiv category codes. Defaults to ``ARXIV_CATEGORIES``.
    max_results : int
        Maximum number of results to request from the API.
    window_hours : int
        Only keep papers published within this many hours.

    Returns
    -------
    list[Paper]
        Papers sorted by relevance score (descending).
    """
    cats = categories or ARXIV_CATEGORIES
    url = _build_query(cats, max_results)
    print(f"[scanner] Fetching: {url}")

    xml_text = _fetch_url(url)
    root = ET.fromstring(xml_text)

    papers: list[Paper] = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        paper = _parse_entry(entry)
        if _is_recent(paper, window_hours):
            paper = _compute_relevance(paper)
            papers.append(paper)

    # Sort by relevance (descending), then by published date (descending)
    papers.sort(key=lambda p: (p.relevance_score, p.published), reverse=True)
    print(f"[scanner] Fetched {len(papers)} recent papers")
    return papers


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    papers = fetch_papers()
    for i, p in enumerate(papers[:10], 1):
        kw = ", ".join(p.keyword_matches) if p.keyword_matches else "none"
        print(f"{i:>3}. [{p.relevance_score:.0f}] {p.title[:80]}")
        print(f"     Keywords: {kw}")
        print(f"     {p.url}\n")
