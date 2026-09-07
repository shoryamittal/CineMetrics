# CineMetrics · CinePulse Decision Intelligence OS
### Executive Streaming Analytics, Churn Defense & Capital Efficiency Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Warehouse-PostgreSQL%20%7C%20CSV%20Mesh-green.svg)](https://www.postgresql.org/)
[![Theme](https://img.shields.io/badge/Theme-Dual%20Light%20%26%20Dark-azure.svg)](http://localhost:8080)
[![Copilot](https://img.shields.io/badge/AI%20Copilot-Offline%20Reasoning%20Engine-purple.svg)](http://localhost:8080)
[![Status](https://img.shields.io/badge/Status-Enterprise%20Ready-brightgreen.svg)]()

**CineMetrics (CinePulse OS)** is an executive-grade streaming decision intelligence operating system designed for C-suite streaming executives (Netflix, Disney+, Prime Video, JioCinema, Hotstar). It fuses multi-currency financial modeling (₹ INR / $ USD), post-finale churn defense, head-to-head title battle arena, hybrid AVOD ad-tier yield analytics, and an offline generative reasoning copilot.

---

## 🌟 Key Platform Capabilities

### 1. Dual-Theme Studio Design System (Light & Dark)
- **Executive Light Theme (Default)**: Apple / Linear / Bloomberg studio aesthetic with crisp pearl card surfaces (`#ffffff`), deep slate typography (`#0f172a`), and studio azure accents (`#0284c7`).
- **Obsidian Dark Mode**: Ultra-deep glassmorphism palette with subtle radiant neon accents.
- **Dual Synchronized Switchers**: Seamless 1-click theme toggling available in both the top header and sidebar footer.
- **Zero-Dependency Native HTML5 Canvas Charts**: All 6 visualizations (Radar, Revenue, Ad Pacing, Ad Fatigue, Scatter, and Traffic) dynamically adapt their grids, labels, and series strokes with high contrast.

### 2. 🛡️ Post-Finale Churn Defense & Bridge Sequences (`#view-churn`)
- Solves the #1 streaming crisis: subscriber cancellations within 72 hours of completing a marquee season finale.
- Tracks **Post-Finale Vulnerability Risk %** and automatically cues **Algorithmic Bridge Sequences** (e.g. *Stranger Things* $\rightarrow$ *Dark*, *Wednesday*, *Severance*).
- Projects **₹185M ($2.2M) in defended recurring MRR** with measurable bridge acceptance rates.

### 3. ⚔️ Head-to-Head Content Battle Arena (`#view-arena`)
- Interactive **5-Axis HTML5 Canvas Radar Chart** benchmarking titles across: **Retention Velocity**, **Capital Efficiency (ROI)**, **Churn Defense Index**, **Global Reach**, and **Evergreen Loyalty**.
- Side-by-side Contender A vs Contender B comparative dossier with an automated executive battle verdict.

### 4. 💰 Hybrid AVOD & Ad-Tier Monetization Intelligence (`#view-adtier`)
- **Dual-Stream Revenue Pacing**: Models SVOD subscription revenue vs programmatic AVOD yields.
- **High-CPM Leaderboard**: Ranks commercial command power (*Squid Game* at **$46.00/CPM**, *Stranger Things* at **$44.00/CPM**).
- **Viewer Commercial Fatigue Curve**: Identifies the optimal advertising break interval (**28–35 minutes**) that preserves >91% viewer retention.

### 5. ✨ "Ask CinePulse AI" Conversational Studio Copilot
- 100% offline client-side generative reasoning engine ([copilot_engine.js](dashboard/copilot_engine.js)).
- Answers natural language questions on churn risk, head-to-head title matchups, Indian cinema ROI leaders, and portfolio capital allocation.

### 6. Authentic Real-World Blockbusters & Series Catalog
Integrated with 120+ world-renowned masterpieces across Hollywood, Indian Cinema, Asian & European Cinema, and Prestige TV:
- **Blockbusters & Sci-Fi**: *Inception, Interstellar, Oppenheimer, The Dark Knight, Dune: Part Two, Avengers: Endgame, Spider-Man: Across the Spider-Verse, The Matrix, Blade Runner 2049, Everything Everywhere All at Once, Avatar: The Way of Water*
- **Prestige Series**: *Stranger Things, Succession, The Bear, Breaking Bad, Severance, The Last of Us, Chernobyl, Arcane, Shōgun, The Boys, Ted Lasso, Dark, Money Heist, Peaky Blinders, House of the Dragon*
- **Indian & Pan-India Hits**: *RRR, K.G.F: Chapter 2, Baahubali 2, Dangal, 3 Idiots, Tumbbad, Jawan, Andhadhun, Gangs of Wasseypur, Stree 2, Kantara, Vikram*
- **Anime & Global Cinema**: *Spirited Away, Your Name, Attack on Titan, Demon Slayer, Parasite, Oldboy, Pan's Labyrinth, Amélie*
- **Real Film & TV Studios**: Warner Bros., Universal Pictures, Walt Disney, Netflix Studios, Paramount, Sony Pictures, HBO Entertainment, A24, Marvel Studios, Studio Ghibli, Yash Raj Films, etc.

---

## 🚀 Quick Start Guide

### 1. Launch the Executive Dashboard
The dashboard is self-contained and pre-bundled with rich catalog data and analytics.

```powershell
# From the project root, start the local web server:
python -m http.server 8080 --directory dashboard
```

Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

---

### 2. Generate or Refresh Warehouse Data

To regenerate or recalibrate all synthetic warehouse data and analytics:

```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Generate studio and content dimensions with real movies
python scripts/generate_studios.py
python scripts/generate_content.py

# 3. Generate calibrated content costs
python scripts/generate_content_cost.py

# 4. Generate OTT analytics layers and dashboard feed
python scripts/generate_ott_analytics.py
python scripts/enrich_curated_catalog.py

# 5. Run AI recommendation engine
python scripts/generate_recommendations.py
```

All analytics outputs are written to `data/analytics/`:
- `content_performance_scorecard.csv` (50,000 asset performance scorecard)
- `executive_kpis.csv` (Portfolio-level financial & viewership summary)
- `regional_performance.csv` (15-territory performance metrics)
- `executive_recommendations.json` (AI decision engine directives)
- `curated_content_catalog.json` (Real titles metadata and streaming stats)

---

### 3. Load into PostgreSQL (Optional)

If using a dedicated PostgreSQL warehouse instance:

```powershell
psql -d cpip -f CPIP/databases/schema/01_dimensions.sql
psql -d cpip -f CPIP/databases/schema/02_facts.sql
python scripts/load_postgres.py
```

Run the reporting views in `sql/analytics/` to create SQL views (`vw_content_decision_intelligence`, `vw_executive_decision_summary`, etc.).

---

## 📊 Analytics Summary Snapshot

| Executive Metric | Warehouse Calibrated Value | Benchmark Status |
| :--- | :--- | :--- |
| **Catalog Assets** | 50,000 Indexed Titles | 100% Validated Foreign Keys |
| **Platform Revenue** | **₹2.56B+ / $30.6M+** | Strong Top-Line Attribution |
| **Total Content Cost** | **₹2.02B / $24.2M** | Production (79.7%) + Licensing (7.2%) |
| **Total Watch Hours** | **4,110,656.84 hrs** | High Streaming Engagement |
| **Total Viewing Events** | **1,000,000 Events** | Validated Event Counting |
| **Expand Candidates** | **16,472 Titles** | High ROI & Completion |
| **Renew Candidates** | **7,370 Titles** | Steady Series Retention |
| **Cost Review / Audit** | **19,762 Titles** | Capital Rationalization Targets |

---

## 📁 Repository Structure

```
ENTERPRISE/
├── dashboard/                     # Executive Streaming Decision Dashboard
│   ├── index.html                 # Modern glassmorphism UI application shell
│   ├── styles.css                 # Dark obsidian theme & radiant accent styles
│   ├── app.js                     # Interactive charting, filtering, and simulator
│   └── catalog.json               # Preloaded blockbuster real titles feed
├── data/
│   ├── analytics/                 # Processed executive analytics & scorecards
│   └── synthetic/                 # Core dimension & fact warehouse CSVs
├── scripts/
│   ├── real_movie_catalog.py      # Master curated real titles dataset
│   ├── generate_studios.py        # Real film & television studio generator
│   ├── generate_content.py        # Real movies & content warehouse generator
│   ├── generate_content_cost.py   # Calibrated content cost generator
│   ├── generate_ott_analytics.py  # Scorecard and KPI aggregation engine
│   ├── enrich_curated_catalog.py  # Blockbuster streaming metrics builder
│   ├── generate_recommendations.py# AI executive recommendation engine
│   └── load_postgres.py           # PostgreSQL warehouse loader
├── sql/
│   └── analytics/                 # Advanced SQL decision intelligence views
├── powerbi/                       # Power BI DAX blueprints and measures
└── requirements.txt               # Python package dependencies
```
