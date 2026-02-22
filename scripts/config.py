"""
Configuration for AI Research Radar.

Defines arXiv categories to track, priority keywords for scoring,
display categories for README grouping, and general settings.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (all relative to the repository root)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
DATA_DIR = REPO_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"
SUMMARIES_DIR = DATA_DIR / "summaries"
STATUS_FILE = DATA_DIR / "status.json"
TRENDS_FILE = DATA_DIR / "trends.json"
ARCHIVE_DIR = REPO_ROOT / "archive"

# Ensure directories exist
for _dir in (PAPERS_DIR, SUMMARIES_DIR, ARCHIVE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# arXiv categories to monitor
# ---------------------------------------------------------------------------
ARXIV_CATEGORIES = [
    "cs.AI",   # Artificial Intelligence
    "cs.LG",   # Machine Learning
    "cs.CL",   # Computation and Language
    "cs.CV",   # Computer Vision
    "cs.IR",   # Information Retrieval
    "stat.ML", # Statistics - Machine Learning
    "math.AT", # Algebraic Topology
    "cs.MA",   # Multi-Agent Systems
]

# ---------------------------------------------------------------------------
# Priority keywords  (case-insensitive matching against title + abstract)
# Papers matching these get a relevance boost.
# ---------------------------------------------------------------------------
PRIORITY_KEYWORDS = [
    "topological data analysis", "persistent homology",
    "multi-objective optimization", "NSGA", "Pareto",
    "support vector machine", "metamodel",
    "context engineering", "RAG", "retrieval augmented",
    "agentic", "multi-agent", "tool use",
    "feature extraction", "healthcare AI",
    "almost periodic", "Banach algebra", "fixed point",
]

# ---------------------------------------------------------------------------
# Display categories used in the README tables
# Each entry maps a display name -> (emoji, list of matching keywords/arxiv cats)
# ---------------------------------------------------------------------------
DISPLAY_CATEGORIES = {
    "Machine Learning & Deep Learning": {
        "emoji": "\U0001f9e0",  # brain
        "arxiv_cats": ["cs.LG", "stat.ML"],
        "keywords": [
            "neural network", "deep learning", "machine learning",
            "support vector machine", "feature extraction",
            "classification", "regression", "supervised", "unsupervised",
        ],
    },
    "Topological Data Analysis": {
        "emoji": "\U0001f4d0",  # triangular ruler
        "arxiv_cats": ["math.AT"],
        "keywords": [
            "topological data analysis", "persistent homology",
            "simplicial complex", "Betti number", "mapper",
            "almost periodic", "Banach algebra", "fixed point",
        ],
    },
    "LLMs & Agents": {
        "emoji": "\U0001f916",  # robot
        "arxiv_cats": ["cs.CL", "cs.MA"],
        "keywords": [
            "large language model", "LLM", "transformer",
            "agentic", "multi-agent", "tool use", "agent",
            "context engineering", "prompt",
        ],
    },
    "Optimization & Engineering": {
        "emoji": "\u2699\ufe0f",  # gear
        "arxiv_cats": [],
        "keywords": [
            "multi-objective optimization", "NSGA", "Pareto",
            "metamodel", "surrogate", "optimization",
            "evolutionary", "genetic algorithm",
        ],
    },
    "Retrieval & RAG": {
        "emoji": "\U0001f50d",  # magnifying glass
        "arxiv_cats": ["cs.IR"],
        "keywords": [
            "RAG", "retrieval augmented", "information retrieval",
            "dense retrieval", "search", "embedding",
        ],
    },
    "Computer Vision": {
        "emoji": "\U0001f441\ufe0f",  # eye
        "arxiv_cats": ["cs.CV"],
        "keywords": [
            "computer vision", "image", "object detection",
            "segmentation", "video", "visual",
            "healthcare AI",
        ],
    },
}

# ---------------------------------------------------------------------------
# arXiv API settings
# ---------------------------------------------------------------------------
ARXIV_API_URL = "http://export.arxiv.org/api/query"
MAX_RESULTS_PER_QUERY = 50          # papers per API call
FETCH_WINDOW_HOURS = 24             # look-back window in hours

# ---------------------------------------------------------------------------
# Summarizer settings (optional, requires OPENAI_API_KEY secret)
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"
ENABLE_AI_SUMMARIES = bool(OPENAI_API_KEY)
SUMMARY_MAX_TOKENS = 120

# ---------------------------------------------------------------------------
# README / Display settings
# ---------------------------------------------------------------------------
MAX_PAPERS_PER_CATEGORY = 15        # max rows shown per table
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# ---------------------------------------------------------------------------
# Digest settings
# ---------------------------------------------------------------------------
DIGEST_TOP_N = 10                   # top papers per weekly digest
DIGEST_LOOKBACK_DAYS = 7
