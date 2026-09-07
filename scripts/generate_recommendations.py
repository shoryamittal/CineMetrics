# ==============================================================================
# ECDIP - AI EXECUTIVE DECISION ENGINE & RECOMMENDATIONS GENERATOR
# ==============================================================================
"""
Generates high-level executive strategic recommendations, greenlight approvals,
franchise renewal strategies, and cost-cutting alerts for streaming executives.
"""

from pathlib import Path
import json
import sys
import pandas as pd
import numpy as np

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"

print("=" * 70)
print("ECDIP - AI EXECUTIVE RECOMMENDATION ENGINE")
print("=" * 70)

scorecard_file = ANALYTICS_DIR / "content_performance_scorecard.csv"
kpis_file = ANALYTICS_DIR / "executive_kpis.csv"

if not scorecard_file.exists():
    raise FileNotFoundError("Run generate_ott_analytics.py first.")

scorecard = pd.read_csv(scorecard_file)
kpis = pd.read_csv(kpis_file).iloc[0].to_dict()

# 1. Top Franchise Expansion Opportunities (High ROI & High Completion)
expansions = scorecard[
    (scorecard["decision"] == "EXPAND") & (scorecard["imdb_rating"] >= 7.5)
].sort_values(by=["content_roi", "total_watch_hours"], ascending=[False, False]).head(10)

expansion_list = []
for _, row in expansions.iterrows():
    expansion_list.append({
        "content_id": int(row["content_id"]),
        "title": str(row["title"]),
        "genre": str(row.get("genre_name", "Unknown")),
        "studio": str(row.get("studio_name", "Unknown")),
        "imdb_rating": float(row["imdb_rating"]),
        "roi_percentage": f"{row['content_roi'] * 100:.1f}%",
        "watch_hours": f"{row['total_watch_hours']:,.0f} hrs",
        "completion_rate": f"{row['average_completion_rate']:.1f}%",
        "action": "Commission Sequel / Expand Global Rights",
        "rationale": f"Exceptional {row['average_completion_rate']:.1f}% viewer completion with {row['content_roi'] * 100:.1f}% ROI demonstrates massive audience loyalty and franchise viability."
    })

# 2. Critical Cost Review & Renegotiation Targets
cost_reviews = scorecard[
    (scorecard["decision"] == "COST_REVIEW") & (scorecard["total_content_cost"] > scorecard["total_content_cost"].median())
].sort_values(by="total_content_cost", ascending=False).head(10)

review_list = []
for _, row in cost_reviews.iterrows():
    review_list.append({
        "content_id": int(row["content_id"]),
        "title": str(row["title"]),
        "genre": str(row.get("genre_name", "Unknown")),
        "total_cost": f"₹{row['total_content_cost']:,.0f}",
        "roi_percentage": f"{row['content_roi'] * 100:.1f}%",
        "completion_rate": f"{row['average_completion_rate']:.1f}%",
        "action": "Renegotiate Licensing Tier / Shift to Ad-Tier",
        "rationale": f"High amortized expenditure (₹{row['total_content_cost']:,.0f}) with negative ROI ({row['content_roi'] * 100:.1f}%) warrants immediate 25% licensing renegotiation upon renewal."
    })

# 3. High-Efficiency Hidden Gems (High Completion, Low Marketing Spend)
hidden_gems = scorecard[
    (scorecard["average_completion_rate"] >= 65) & (scorecard["marketing_spend"] < 10000) & (scorecard["imdb_rating"] >= 7.8)
].sort_values(by="average_completion_rate", ascending=False).head(8)

gems_list = []
for _, row in hidden_gems.iterrows():
    gems_list.append({
        "content_id": int(row["content_id"]),
        "title": str(row["title"]),
        "genre": str(row.get("genre_name", "Unknown")),
        "imdb_rating": float(row["imdb_rating"]),
        "completion_rate": f"{row['average_completion_rate']:.1f}%",
        "action": "Boost Paid Acquisition / Editorial Placement",
        "rationale": "High organic stickiness and satisfaction rate with virtually zero marketing spend; ideal candidate for front-page hero carousel promotion."
    })

recommendations_payload = {
    "generated_at": pd.Timestamp.now().isoformat(),
    "portfolio_kpis": kpis,
    "strategic_initiatives": [
        {
            "pillar": "Franchise Monetization",
            "priority": "HIGH",
            "summary": "Fast-track sequel development and global spinoffs for top 10 breakout assets with >60% completion rates.",
            "candidates": expansion_list
        },
        {
            "pillar": "Cost Rationalization",
            "priority": "CRITICAL",
            "summary": "Initiate licensing audits on underperforming high-cost third-party acquisitions.",
            "candidates": review_list
        },
        {
            "pillar": "Viral Growth & Hidden Gems",
            "priority": "MEDIUM",
            "summary": "Amplify high-retention indie and international cinema using targeted programmatic push notifications.",
            "candidates": gems_list
        }
    ]
}

output_json = ANALYTICS_DIR / "executive_recommendations.json"
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(recommendations_payload, f, indent=2)

print(f"✓ Executive recommendations saved to: {output_json}")
print("\nTop 3 Recommended Franchise Expansions:")
for item in expansion_list[:3]:
    print(f"  ★ {item['title']} ({item['genre']}): {item['action']} [ROI: {item['roi_percentage']}, Completion: {item['completion_rate']}]")

print("\nTop 3 Cost Review Priorities:")
for item in review_list[:3]:
    print(f"  ⚠ {item['title']} ({item['genre']}): {item['action']} [Cost: {item['total_cost']}, ROI: {item['roi_percentage']}]")
