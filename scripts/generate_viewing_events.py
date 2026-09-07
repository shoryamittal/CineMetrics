# ===========================================
# CPIP - Viewing Events Generator
# ===========================================

import pandas as pd
import numpy as np
from pathlib import Path
import random

# -------------------------------------------
# Configuration
# -------------------------------------------

random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TOTAL_EVENTS = 1_000_000

# -------------------------------------------
# Load dimension data
# -------------------------------------------

content_df = pd.read_csv(
    OUTPUT_DIR / "dim_content.csv"
)

region_df = pd.read_csv(
    OUTPUT_DIR / "dim_region.csv"
)

platform_df = pd.read_csv(
    OUTPUT_DIR / "dim_platform.csv"
)

plan_df = pd.read_csv(
    OUTPUT_DIR / "dim_subscription_plan.csv"
)

calendar_df = pd.read_csv(
    OUTPUT_DIR / "dim_calendar.csv"
)

# -------------------------------------------
# Randomly select dimension IDs
# -------------------------------------------

content_ids = np.random.choice(
    content_df["content_id"].values,
    size=TOTAL_EVENTS
)

region_ids = np.random.choice(
    region_df["region_id"].values,
    size=TOTAL_EVENTS
)

platform_ids = np.random.choice(
    platform_df["platform_id"].values,
    size=TOTAL_EVENTS
)

plan_ids = np.random.choice(
    plan_df["plan_id"].values,
    size=TOTAL_EVENTS
)

date_ids = np.random.choice(
    calendar_df["date_id"].values,
    size=TOTAL_EVENTS
)

# -------------------------------------------
# Build lookup arrays
# -------------------------------------------

content_lookup = content_df.set_index(
    "content_id"
)

selected_content = content_lookup.loc[
    content_ids
]

# -------------------------------------------
# Base content quality
# -------------------------------------------

imdb_rating = selected_content[
    "imdb_rating"
].to_numpy()

content_type = selected_content[
    "content_type"
].to_numpy()

release_year = selected_content[
    "release_year"
].to_numpy()

# -------------------------------------------
# Rating effect
# -------------------------------------------

rating_effect = (
    imdb_rating - 5
) / 4

rating_effect = np.clip(
    rating_effect,
    0,
    1
)

# -------------------------------------------
# Recency effect
# -------------------------------------------

current_year = 2026

recency_effect = (
    release_year - 2015
) / 13

recency_effect = np.clip(
    recency_effect,
    0,
    1
)

# -------------------------------------------
# Base watch hours
# -------------------------------------------

base_watch_hours = np.random.gamma(
    shape=2.5,
    scale=1.2,
    size=TOTAL_EVENTS
)

# Higher-rated content gets more viewing
watch_hours = (
    base_watch_hours
    * (0.75 + rating_effect * 0.70)
)

# Newer content gets a modest boost
watch_hours *= (
    0.85 + recency_effect * 0.35
)

# Series generally create more total viewing
series_mask = content_type == "Series"

watch_hours[series_mask] *= 1.35

# Add realistic variation
watch_hours *= np.random.uniform(
    0.70,
    1.30,
    TOTAL_EVENTS
)

watch_hours = np.clip(
    watch_hours,
    0.05,
    20
)

# -------------------------------------------
# Completion rate
# -------------------------------------------

completion_rate = (
    45
    + rating_effect * 35
    + np.random.normal(
        0,
        8,
        TOTAL_EVENTS
    )
)

completion_rate = np.clip(
    completion_rate,
    10,
    100
)

# -------------------------------------------
# Rewatch count
# -------------------------------------------

rewatch_probability = (
    0.03
    + rating_effect * 0.15
)

rewatch_count = np.random.binomial(
    n=3,
    p=np.clip(
        rewatch_probability,
        0,
        0.5
    )
)

# -------------------------------------------
# Pause count
# -------------------------------------------

pause_lambda = np.maximum(
    0.5,
    3.5 - completion_rate / 30
)

pause_count = np.random.poisson(
    pause_lambda
)

pause_count = np.clip(
    pause_count,
    0,
    20
)

# -------------------------------------------
# Search before watching
# -------------------------------------------

search_probability = np.where(
    rating_effect < 0.4,
    0.35,
    0.22
)

search_before_watch = (
    np.random.random(TOTAL_EVENTS)
    < search_probability
)

# -------------------------------------------
# Marketing influence
# -------------------------------------------

marketing_probability = np.where(
    recency_effect > 0.6,
    0.35,
    0.18
)

marketing_influenced = (
    np.random.random(TOTAL_EVENTS)
    < marketing_probability
)

# -------------------------------------------
# Build final DataFrame
# -------------------------------------------

viewing_df = pd.DataFrame({

    "viewing_id":
        np.arange(
            1,
            TOTAL_EVENTS + 1
        ),

    "content_id":
        content_ids,

    "region_id":
        region_ids,

    "platform_id":
        platform_ids,

    "plan_id":
        plan_ids,

    "date_id":
        date_ids,

    "watch_hours":
        np.round(
            watch_hours,
            2
        ),

    "completion_rate":
        np.round(
            completion_rate,
            2
        ),

    "rewatch_count":
        rewatch_count,

    "pause_count":
        pause_count,

    "search_before_watch":
        search_before_watch,

    "marketing_influenced":
        marketing_influenced,

    "created_at":
        pd.Timestamp.now()
})

# -------------------------------------------
# Validation
# -------------------------------------------

assert len(viewing_df) == TOTAL_EVENTS

assert viewing_df[
    "viewing_id"
].is_unique

assert viewing_df[
    "content_id"
].isin(
    content_df["content_id"]
).all()

assert viewing_df[
    "region_id"
].isin(
    region_df["region_id"]
).all()

assert viewing_df[
    "platform_id"
].isin(
    platform_df["platform_id"]
).all()

assert viewing_df[
    "plan_id"
].isin(
    plan_df["plan_id"]
).all()

assert viewing_df[
    "watch_hours"
].gt(0).all()

assert viewing_df[
    "completion_rate"
].between(
    0,
    100
).all()

assert viewing_df[
    "rewatch_count"
].ge(0).all()

assert viewing_df[
    "pause_count"
].ge(0).all()

# -------------------------------------------
# Save
# -------------------------------------------

output_file = (
    OUTPUT_DIR /
    "fact_viewing_events.csv"
)

viewing_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Summary
# -------------------------------------------

print("=" * 65)
print("VIEWING EVENTS GENERATED SUCCESSFULLY")
print("=" * 65)

print(
    f"Records generated : {len(viewing_df):,}"
)

print(
    f"Output file       : {output_file}"
)

print("\nStatistics:")

print(
    f"Average watch hours : "
    f"{viewing_df['watch_hours'].mean():.2f}"
)

print(
    f"Average completion  : "
    f"{viewing_df['completion_rate'].mean():.2f}%"
)

print(
    f"Marketing influenced: "
    f"{viewing_df['marketing_influenced'].mean() * 100:.2f}%"
)

print(
    f"Search before watch : "
    f"{viewing_df['search_before_watch'].mean() * 100:.2f}%"
)

print("\nValidation:")

print("✓ Correct record count")
print("✓ Viewing IDs are unique")
print("✓ Content relationships are valid")
print("✓ Region relationships are valid")
print("✓ Platform relationships are valid")
print("✓ Subscription plan relationships are valid")
print("✓ Watch hours are positive")
print("✓ Completion rates are valid")
print("✓ Rewatch counts are valid")
print("✓ Pause counts are valid")

print("\nViewing event generation complete.")