# ==============================================================================
# ECDIP - ADVANCED OTT ANALYTICS & DECISION INTELLIGENCE GENERATOR
# ==============================================================================
"""
Build Power BI & Executive Dashboard analytics from data warehouse CSVs.
Features:
- Fixed event counting (precise row counts for total_views)
- Realistic streaming economics with positive portfolio ROI
- Multi-dimensional decision intelligence (EXPAND, RENEW, MONITOR, COST_REVIEW, EXIT)
- Enriched metadata (Studio name, Genre name)
- Export of curated titles JSON for high-performance dashboard rendering
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
SOURCE_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR = BASE_DIR / "data" / "analytics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHUNK_SIZE = 250_000

print("=" * 70)
print("ECDIP - OTT ANALYTICS & DECISION INTELLIGENCE GENERATOR")
print("=" * 70)

# Load dimensions
print("Loading dimensions...")
content = pd.read_csv(SOURCE_DIR / "dim_content.csv")
cost = pd.read_csv(SOURCE_DIR / "fact_content_cost.csv")
regions = pd.read_csv(SOURCE_DIR / "dim_region.csv")
genres = pd.read_csv(SOURCE_DIR / "dim_genre.csv")
studios = pd.read_csv(SOURCE_DIR / "dim_studio.csv")

# 1. Aggregate Viewing Events (Correct Count & Sum)
print("Aggregating viewing events...")
def aggregate_viewing(group_col):
    chunks = []
    for chunk in pd.read_csv(SOURCE_DIR / "fact_viewing_events.csv", usecols=[group_col, "watch_hours"], chunksize=CHUNK_SIZE):
        agg = chunk.groupby(group_col, as_index=False).agg(
            total_watch_hours=("watch_hours", "sum"),
            total_views=("watch_hours", "count")
        )
        chunks.append(agg)
    return pd.concat(chunks, ignore_index=True).groupby(group_col, as_index=False).agg(
        total_watch_hours=("total_watch_hours", "sum"),
        total_views=("total_views", "sum")
    )

viewing_by_content = aggregate_viewing("content_id")
viewing_by_region = aggregate_viewing("region_id")

# 2. Aggregate Revenue Events
print("Aggregating revenue...")
def aggregate_revenue(group_col):
    chunks = []
    for chunk in pd.read_csv(SOURCE_DIR / "fact_revenue.csv", usecols=[group_col, "revenue_amount"], chunksize=CHUNK_SIZE):
        agg = chunk.groupby(group_col, as_index=False)["revenue_amount"].sum().rename(columns={"revenue_amount": "total_revenue"})
        chunks.append(agg)
    return pd.concat(chunks, ignore_index=True).groupby(group_col, as_index=False)["total_revenue"].sum()

revenue_by_content = aggregate_revenue("content_id")
revenue_by_region = aggregate_revenue("region_id")

# 3. Aggregate Engagement
print("Aggregating audience engagement...")
def aggregate_engagement():
    chunks = []
    cols = ["content_id", "likes", "dislikes", "completion_rate", "rewatch_rate"]
    for chunk in pd.read_csv(SOURCE_DIR / "fact_engagement.csv", usecols=cols, chunksize=CHUNK_SIZE):
        agg = chunk.groupby("content_id", as_index=False).agg(
            likes=("likes", "sum"),
            dislikes=("dislikes", "sum"),
            sum_comp=("completion_rate", "sum"),
            sum_rewatch=("rewatch_rate", "sum"),
            count=("completion_rate", "count")
        )
        chunks.append(agg)
    combined = pd.concat(chunks, ignore_index=True).groupby("content_id", as_index=False).agg(
        likes=("likes", "sum"),
        dislikes=("dislikes", "sum"),
        sum_comp=("sum_comp", "sum"),
        sum_rewatch=("sum_rewatch", "sum"),
        count=("count", "sum")
    )
    combined["average_completion_rate"] = np.where(combined["count"] > 0, (combined["sum_comp"] / combined["count"]).round(2), 0)
    combined["average_rewatch_rate"] = np.where(combined["count"] > 0, (combined["sum_rewatch"] / combined["count"]).round(2), 0)
    return combined.drop(columns=["sum_comp", "sum_rewatch", "count"])

engagement = aggregate_engagement()

# 4. Aggregate Marketing
print("Aggregating marketing spend and conversions...")
marketing = pd.read_csv(
    SOURCE_DIR / "fact_marketing.csv",
    usecols=["content_id", "marketing_spend", "attributed_revenue", "conversions"]
).groupby("content_id", as_index=False).sum()

# 5. Build Content Scorecard
print("Building content performance scorecard...")
cost_cols_to_merge = [c for c in cost.columns if c == "content_id" or c not in ["production_budget", "licensing_cost", "available_regions"]]
scorecard = content.merge(cost[cost_cols_to_merge], on="content_id", how="left")
scorecard = scorecard.merge(revenue_by_content, on="content_id", how="left")
scorecard = scorecard.merge(viewing_by_content, on="content_id", how="left")
scorecard = scorecard.merge(engagement, on="content_id", how="left")
scorecard = scorecard.merge(marketing, on="content_id", how="left")

# Merge genre name and studio name
scorecard = scorecard.merge(genres[["genre_id", "genre_name"]], on="genre_id", how="left")
scorecard = scorecard.merge(studios[["studio_id", "studio_name"]], on="studio_id", how="left")

numeric_columns = [
    "total_content_cost", "total_revenue", "total_watch_hours", "total_views",
    "likes", "dislikes", "average_completion_rate", "average_rewatch_rate",
    "marketing_spend", "attributed_revenue", "conversions"
]
scorecard[numeric_columns] = scorecard[numeric_columns].fillna(0)

# Financial Metrics
scorecard["total_investment"] = (scorecard["total_content_cost"] + scorecard["marketing_spend"]).round(2)
scorecard["contribution_profit"] = (scorecard["total_revenue"] - scorecard["total_investment"]).round(2)
scorecard["content_roi"] = np.where(
    scorecard["total_investment"] > 0,
    (scorecard["contribution_profit"] / scorecard["total_investment"]).round(4),
    0
)
scorecard["revenue_per_watch_hour"] = np.where(
    scorecard["total_watch_hours"] > 0,
    (scorecard["total_revenue"] / scorecard["total_watch_hours"]).round(2),
    0
)
scorecard["positive_engagement_rate"] = np.where(
    (scorecard["likes"] + scorecard["dislikes"]) > 0,
    (scorecard["likes"] / (scorecard["likes"] + scorecard["dislikes"])).round(4),
    0
)
scorecard["portfolio_revenue_percentile"] = scorecard["total_revenue"].rank(pct=True).round(4)
scorecard["portfolio_roi_percentile"] = scorecard["content_roi"].rank(pct=True).round(4)

# Executive Decision Intelligence Classification
scorecard["decision"] = np.select(
    [
        (scorecard.content_roi >= 0.25) & (scorecard.average_completion_rate >= 60),
        (scorecard.content_roi >= 0.10) & (scorecard.average_completion_rate >= 50),
        (scorecard.content_roi < -0.30) & (scorecard.average_completion_rate < 45),
        scorecard.content_roi < -0.05,
    ],
    ["EXPAND", "RENEW", "EXIT_OR_RENEGOTIATE", "COST_REVIEW"],
    default="MONITOR"
)

# Save Scorecard
scorecard_path = OUTPUT_DIR / "content_performance_scorecard.csv"
scorecard.to_csv(scorecard_path, index=False)
print(f"✓ Saved content scorecard: {scorecard_path} ({len(scorecard):,} rows)")

# 6. Regional Performance
print("Building regional performance layer...")
regional = regions.merge(revenue_by_region, on="region_id", how="left").merge(viewing_by_region, on="region_id", how="left")
regional[["total_revenue", "total_watch_hours", "total_views"]] = regional[["total_revenue", "total_watch_hours", "total_views"]].fillna(0)
regional["revenue_per_watch_hour"] = np.where(
    regional.total_watch_hours > 0,
    (regional.total_revenue / regional.total_watch_hours).round(2),
    0
)
regional_path = OUTPUT_DIR / "regional_performance.csv"
regional.to_csv(regional_path, index=False)
print(f"✓ Saved regional performance: {regional_path}")

# 7. Executive KPIs
print("Building executive KPIs...")
portfolio_investment = scorecard.total_investment.sum()
portfolio_profit = scorecard.contribution_profit.sum()
portfolio_roi = round(portfolio_profit / portfolio_investment, 4) if portfolio_investment > 0 else 0

summary = pd.DataFrame([{
    "content_assets": len(scorecard),
    "total_revenue": round(scorecard.total_revenue.sum(), 2),
    "total_content_cost": round(scorecard.total_content_cost.sum(), 2),
    "total_marketing_spend": round(scorecard.marketing_spend.sum(), 2),
    "total_watch_hours": round(scorecard.total_watch_hours.sum(), 2),
    "total_views": int(scorecard.total_views.sum()),
    "portfolio_roi": portfolio_roi,
    "expand_candidates": int((scorecard.decision == "EXPAND").sum()),
    "renew_candidates": int((scorecard.decision == "RENEW").sum()),
    "monitor_candidates": int((scorecard.decision == "MONITOR").sum()),
    "cost_review_candidates": int((scorecard.decision == "COST_REVIEW").sum()),
    "exit_candidates": int((scorecard.decision == "EXIT_OR_RENEGOTIATE").sum())
}])
summary_path = OUTPUT_DIR / "executive_kpis.csv"
summary.to_csv(summary_path, index=False)
print(f"✓ Saved executive KPIs: {summary_path}")

# 8. Curate Rich Titles JSON for Instant Dashboard Loading
print("Exporting curated titles catalog for dashboard...")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from real_movie_catalog import REAL_TITLES

curated_list = []
for idx, real_info in enumerate(REAL_TITLES, start=1):
    matching_row = scorecard[scorecard["content_id"] == idx]
    if not matching_row.empty:
        r = matching_row.iloc[0]
        curated_list.append({
            "content_id": int(r["content_id"]),
            "title": str(r["title"]),
            "content_type": str(r["content_type"]),
            "genre": str(r.get("genre_name", real_info.get("genre", "Drama"))),
            "studio": str(r.get("studio_name", real_info.get("studio", "Warner Bros. Pictures"))),
            "release_year": int(r["release_year"]),
            "language": str(r["language"]),
            "duration_minutes": int(r["duration_minutes"]),
            "age_rating": str(r["age_rating"]),
            "imdb_rating": float(r["imdb_rating"]),
            "production_budget": float(r["production_budget"]),
            "licensing_cost": float(r["licensing_cost"]),
            "total_content_cost": float(r["total_content_cost"]),
            "total_revenue": float(r["total_revenue"]),
            "total_watch_hours": float(r["total_watch_hours"]),
            "total_views": int(r["total_views"]),
            "average_completion_rate": float(r["average_completion_rate"]),
            "average_rewatch_rate": float(r["average_rewatch_rate"]),
            "contribution_profit": float(r["contribution_profit"]),
            "content_roi": float(r["content_roi"]),
            "decision": str(r["decision"]),
            "director": real_info.get("director", "Acclaimed Director"),
            "cast": real_info.get("cast", "Star Cast"),
            "synopsis": real_info.get("synopsis", "Award-winning streaming production."),
            "tags": real_info.get("tags", ["Featured"]),
            "poster_url": real_info.get("poster_url", ""),
            "poster_color": real_info.get("poster_color", "#1e3a8a")
        })

# Also copy curated JSON to dashboard directory for immediate direct browser fetch
dashboard_json = BASE_DIR / "dashboard" / "catalog.json"
with open(dashboard_json, "w", encoding="utf-8") as f:
    json.dump(curated_list, f, indent=2)

with open(OUTPUT_DIR / "curated_content_catalog.json", "w", encoding="utf-8") as f:
    json.dump(curated_list, f, indent=2)

print(f"✓ Saved curated catalog JSON: {dashboard_json} ({len(curated_list)} titles)")

print("\n" + "=" * 70)
print("EXECUTIVE INTELLIGENCE SUMMARY:")
print("=" * 70)
print(f"Content Assets        : {summary['content_assets'].iloc[0]:,}")
print(f"Total Revenue         : ₹{summary['total_revenue'].iloc[0]:,.2f}")
print(f"Total Content Cost    : ₹{summary['total_content_cost'].iloc[0]:,.2f}")
print(f"Total Marketing Spend : ₹{summary['total_marketing_spend'].iloc[0]:,.2f}")
print(f"Total Watch Hours     : {summary['total_watch_hours'].iloc[0]:,.2f}")
print(f"Total Views           : {summary['total_views'].iloc[0]:,}")
print(f"Portfolio ROI         : {summary['portfolio_roi'].iloc[0] * 100:.2f}%")
print(f"Expand Candidates     : {summary['expand_candidates'].iloc[0]:,}")
print(f"Renew Candidates      : {summary['renew_candidates'].iloc[0]:,}")
print(f"Monitor Candidates    : {summary['monitor_candidates'].iloc[0]:,}")
print(f"Cost Review           : {summary['cost_review_candidates'].iloc[0]:,}")
print(f"Exit / Renegotiate    : {summary['exit_candidates'].iloc[0]:,}")
print("=" * 70)
