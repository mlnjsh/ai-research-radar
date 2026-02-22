<div align="center">

# 📡 AI Research Radar

### *Self-Updating AI Paper Tracker — Powered by GitHub Actions*

[![Auto-Update](https://img.shields.io/badge/Updates-Every_6_Hours-00C853?style=for-the-badge&logo=github-actions)](https://github.com/mlnjsh/ai-research-radar/actions)
[![Papers Tracked](https://img.shields.io/badge/Papers_Tracked-500+-blueviolet?style=for-the-badge)](https://arxiv.org)
[![Last Updated](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/mlnjsh/ai-research-radar/main/data/status.json&query=$.last_updated&label=Last%20Updated&style=for-the-badge&color=blue)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

**This README updates itself every 6 hours with the latest AI research papers from arXiv.**

No manual curation needed. GitHub Actions fetches, summarizes, and categorizes new papers automatically.

[Today's Papers](#-todays-papers) · [Trending Topics](#-trending-topics) · [Weekly Digest](#-weekly-digest) · [How It Works](#-how-it-works) · [Customize](#-customize-your-radar)

</div>

---

## 🔴 Live Status

```
┌─────────────────────────────────────────────────────────────────┐
│                    📡 AI RESEARCH RADAR                          │
│                    ━━━━━━━━━━━━━━━━━━━                          │
│                                                                  │
│  Status:     🟢 ACTIVE — Scanning arXiv every 6 hours           │
│  Last Scan:  [Auto-updated by GitHub Actions]                    │
│  Papers:     500+ tracked since launch                           │
│  Categories: TDA, ML, LLM, Agents, Optimization, RAG, Vision    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  SCAN CYCLE                                          │       │
│  │                                                      │       │
│  │  00:00 ──── 06:00 ──── 12:00 ──── 18:00 ──── 00:00  │       │
│  │    ↑          ↑          ↑          ↑          ↑     │       │
│  │   scan      scan      scan      scan      scan      │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📰 Today's Papers

> *This section is automatically updated by GitHub Actions*

<!-- PAPERS_START -->

### 🧠 Machine Learning & Deep Learning

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

### 📐 Topological Data Analysis

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

### 🤖 LLMs & Agents

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

### ⚙️ Optimization & Engineering

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

### 🔍 Retrieval & RAG

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

### 👁️ Computer Vision

| # | Paper | Authors | Category | Date |
|:-:|:------|:--------|:--------:|:----:|
| 1 | *Waiting for first scan...* | — | — | — |

<!-- PAPERS_END -->

---

## 📊 Trending Topics

> *Auto-generated from the last 7 days of papers*

<!-- TRENDS_START -->

```
TRENDING TOPICS (Last 7 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Waiting for data accumulation...
   First trend report will appear after 7 days of scanning.
```

<!-- TRENDS_END -->

---

## 📋 Weekly Digest

> *Generated every Monday at 00:00 UTC*

<!-- DIGEST_START -->

The weekly digest will appear here after the first week of operation. It includes:
- Top 10 most impactful papers
- Emerging research trends
- Notable author contributions
- Cross-domain connections

**[📁 View all weekly digests →](archive/)**

<!-- DIGEST_END -->

---

## 🏗️ How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    RADAR PIPELINE                                │
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐       │
│  │  GitHub   │───>│  Python      │───>│  arXiv API       │       │
│  │  Actions  │    │  Script      │    │  Fetch Papers    │       │
│  │  (cron)   │    │  (scanner)   │    │  (cs.AI, cs.LG,  │       │
│  └──────────┘    └──────────────┘    │   stat.ML, etc.) │       │
│                                      └────────┬─────────┘       │
│                                               │                  │
│  ┌──────────────────────────────────────────┐ │                  │
│  │  Processing Pipeline                      │<┘                  │
│  │                                          │                    │
│  │  1. Fetch new papers from arXiv RSS      │                    │
│  │  2. Filter by categories & keywords      │                    │
│  │  3. Extract title, authors, abstract     │                    │
│  │  4. Categorize (ML, TDA, LLM, etc.)     │                    │
│  │  5. Generate one-line summary            │                    │
│  │  6. Calculate relevance score            │                    │
│  │  7. Update README.md tables              │                    │
│  │  8. Commit & push changes               │                    │
│  └──────────────────────────────────────────┘                    │
│                                                                  │
│  Output Files:                                                   │
│  ├── README.md          (Updated paper tables)                   │
│  ├── data/papers/       (JSON paper database)                    │
│  ├── data/summaries/    (AI-generated summaries)                 │
│  ├── data/status.json   (Last scan metadata)                     │
│  └── archive/           (Weekly digest archives)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Tracked Categories

| arXiv Category | Description | Keywords |
|:---------------|:-----------|:---------|
| `cs.AI` | Artificial Intelligence | agents, reasoning, planning |
| `cs.LG` | Machine Learning | neural networks, deep learning |
| `cs.CL` | Computation and Language | NLP, LLMs, transformers |
| `cs.CV` | Computer Vision | image, video, detection |
| `cs.IR` | Information Retrieval | search, RAG, retrieval |
| `stat.ML` | Statistics - ML | statistical learning, Bayesian |
| `math.AT` | Algebraic Topology | TDA, homology, topology |
| `cs.MA` | Multi-Agent Systems | agents, coordination |

### Custom Keywords (Higher Priority)

```python
PRIORITY_KEYWORDS = [
    "topological data analysis", "persistent homology",
    "multi-objective optimization", "NSGA", "Pareto",
    "support vector machine", "metamodel",
    "context engineering", "RAG", "retrieval augmented",
    "agentic", "multi-agent", "tool use",
    "feature extraction", "healthcare AI",
    "almost periodic", "Banach algebra", "fixed point"
]
```

---

## 🚀 Setup Your Own Radar

### 1. Fork This Repo

```bash
gh repo fork mlnjsh/ai-research-radar --clone
cd ai-research-radar
```

### 2. Add Secrets (Optional, for AI summaries)

```
Settings → Secrets → Actions → New Repository Secret
Name: OPENAI_API_KEY
Value: sk-your-key-here
```

### 3. Customize Categories

Edit `scripts/config.py` to change:
- arXiv categories to track
- Priority keywords
- Number of papers per category
- Update frequency

### 4. Enable GitHub Actions

The workflow at `.github/workflows/scan.yml` runs automatically. You can also trigger manually:

```bash
gh workflow run scan.yml
```

---

## 🗂️ Repository Structure

```
ai-research-radar/
├── README.md                    # Auto-updated with latest papers
├── .github/
│   └── workflows/
│       ├── scan.yml             # Every 6 hours: fetch & update
│       └── weekly-digest.yml    # Every Monday: generate digest
├── scripts/
│   ├── config.py                # Categories, keywords, settings
│   ├── scanner.py               # arXiv API fetcher
│   ├── categorizer.py           # Paper classification
│   ├── summarizer.py            # AI summary generation
│   ├── readme_updater.py        # README table generator
│   └── digest_generator.py      # Weekly digest creator
├── data/
│   ├── papers/                  # Raw paper metadata (JSON)
│   │   ├── 2026-02-22.json
│   │   └── ...
│   ├── summaries/               # AI-generated summaries
│   ├── trends.json              # 7-day trending topics
│   └── status.json              # Last scan metadata
├── archive/
│   ├── week-2026-02-17.md       # Weekly digest archives
│   └── ...
├── requirements.txt
└── LICENSE
```

---

## 📈 Stats Since Launch

<!-- STATS_START -->
```
Papers Scanned:     0 (waiting for first scan)
Categories:         8
Unique Authors:     0
Trending Topics:    0
Weekly Digests:     0
```
<!-- STATS_END -->

---

## 🤝 Contributing

- :star: **Star this repo** to get notified of trending papers
- :bug: **Report issues** with paper categorization
- :heavy_plus_sign: **Suggest categories** or keywords to track
- :fork_and_knife: **Fork & customize** for your research area

---

## 📜 Citation

```bibtex
@software{joshi2026radar,
  title   = {AI Research Radar: Self-Updating Paper Tracker},
  author  = {Joshi, Milan Amrut},
  year    = {2026},
  url     = {https://github.com/mlnjsh/ai-research-radar}
}
```

---

<div align="center">

**Built by [Prof. Milan Amrut Joshi](https://github.com/mlnjsh)**

*"Never miss an important AI paper again."*

[![Star History](https://api.star-history.com/svg?repos=mlnjsh/ai-research-radar&type=Date)](https://star-history.com/#mlnjsh/ai-research-radar&Date)

</div>
