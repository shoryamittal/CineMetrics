from pathlib import Path
import pandas as pd
import numpy as np

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_FILE = DATA_DIR / "fact_search_events.csv"

TOTAL_EVENTS = 750_000

print("=" * 70)
print("ECDIP - SEARCH INTELLIGENCE GENERATOR")
print("=" * 70)

# ----------------------------------------------------------
# Load dimensions
# ----------------------------------------------------------

content = pd.read_csv(
    DATA_DIR / "dim_content.csv",
    usecols=[
        "content_id",
        "genre_id",
        "language",
        "imdb_rating"
    ]
)

region = pd.read_csv(
    DATA_DIR / "dim_region.csv",
    usecols=["region_id"]
)

calendar = pd.read_csv(
    DATA_DIR / "dim_calendar.csv",
    usecols=["date_id"]
)

# ----------------------------------------------------------
# Create search events
# ----------------------------------------------------------

content_ids = np.random.choice(
    content["content_id"].values,
    TOTAL_EVENTS
)

region_ids = np.random.choice(
    region["region_id"].values,
    TOTAL_EVENTS
)

date_ids = np.random.choice(
    calendar["date_id"].values,
    TOTAL_EVENTS
)

selected_content = content.set_index(
    "content_id"
).loc[content_ids].reset_index()

# ----------------------------------------------------------
# Search intent
# ----------------------------------------------------------

rating_factor = (
    selected_content["imdb_rating"] - 5
) / 4

rating_factor = np.clip(
    rating_factor,
    0,
    1
)

# High-quality content has stronger discovery intent
search_intensity = np.random.gamma(
    shape=2.0,
    scale=1.5,
    size=TOTAL_EVENTS
)

# ----------------------------------------------------------
# Search result behavior
# ----------------------------------------------------------

result_click_probability = (
    0.25
    + rating_factor * 0.30
)

result_click_probability = np.clip(
    result_click_probability,
    0.05,
    0.85
)

result_clicked = (
    np.random.random(TOTAL_EVENTS)
    < result_click_probability
)

# ----------------------------------------------------------
# Search → Watch conversion
# ----------------------------------------------------------

watch_probability = (
    0.25
    + rating_factor * 0.30
    + result_clicked.astype(float) * 0.25
)

watch_probability = np.clip(
    watch_probability,
    0.05,
    0.95
)

watch_after_search = (
    np.random.random(TOTAL_EVENTS)
    < watch_probability
)

# ----------------------------------------------------------
# Search abandonment
# ----------------------------------------------------------

search_abandoned = (
    ~result_clicked
)

# ----------------------------------------------------------
# Search query categories
# ----------------------------------------------------------

query_type = np.random.choice(
    [
        "Exact Title",
        "Genre",
        "Actor / Creator",
        "Language",
        "Trending",
        "Recommendation",
        "General Discovery"
    ],
    TOTAL_EVENTS,
    p=[
        0.22,
        0.18,
        0.12,
        0.10,
        0.14,
        0.12,
        0.12
    ]
)

# ----------------------------------------------------------
# Search relevance
# ----------------------------------------------------------

search_relevance_score = np.where(
    result_clicked,
    np.random.uniform(0.65, 1.0, TOTAL_EVENTS),
    np.random.uniform(0.10, 0.70, TOTAL_EVENTS)
)

search_relevance_score = np.round(
    search_relevance_score,
    3
)

# ----------------------------------------------------------
# Search-to-watch conversion
# ----------------------------------------------------------

search_to_watch = (
    watch_after_search.astype(int)
)

# ----------------------------------------------------------
# Build DataFrame
# ----------------------------------------------------------

search = pd.DataFrame({

    "search_event_id":
        np.arange(
            1,
            TOTAL_EVENTS + 1
        ),

    "content_id":
        content_ids,

    "region_id":
        region_ids,

    "date_id":
        date_ids,

    "query_type":
        query_type,

    "search_intensity":
        np.round(
            search_intensity,
            2
        ),

    "result_clicked":
        result_clicked,

    "watch_after_search":
        watch_after_search,

    "search_abandoned":
        search_abandoned,

    "search_relevance_score":
        search_relevance_score,

    "search_to_watch":
        search_to_watch,

    "created_at":
        pd.Timestamp.now()
})

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

print("\nRunning search-event validation...")

assert len(search) == TOTAL_EVENTS

assert search[
    "search_event_id"
].is_unique

assert search[
    "content_id"
].isin(
    content["content_id"]
).all()

assert search[
    "region_id"
].isin(
    region["region_id"]
).all()

assert search[
    "date_id"
].isin(
    calendar["date_id"]
).all()

assert search[
    "search_intensity"
].ge(0).all()

assert search[
    "search_relevance_score"
].between(
    0,
    1
).all()

assert search[
    "result_clicked"
].isin(
    [True, False]
).all()

assert search[
    "watch_after_search"
].isin(
    [True, False]
).all()

assert search[
    "search_abandoned"
].isin(
    [True, False]
).all()

# Logical consistency
assert (
    search.loc[
        search["result_clicked"] == False,
        "search_abandoned"
    ]
    .all()
)

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

search.to_csv(
    OUTPUT_FILE,
    index=False
)

# ----------------------------------------------------------
# Report
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("SEARCH DATA GENERATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Records generated : "
    f"{len(search):,}"
)

print(
    f"Click-through rate : "
    f"{search['result_clicked'].mean() * 100:.2f}%"
)

print(
    f"Search → watch rate: "
    f"{search['watch_after_search'].mean() * 100:.2f}%"
)

print(
    f"Search abandonment : "
    f"{search['search_abandoned'].mean() * 100:.2f}%"
)

print(
    f"Average relevance  : "
    f"{search['search_relevance_score'].mean():.3f}"
)

print("\nQuery distribution:")

print(
    search["query_type"]
    .value_counts()
)

print("\nValidation:")
print("✓ Search IDs unique")
print("✓ Content relationships valid")
print("✓ Region relationships valid")
print("✓ Calendar relationships valid")
print("✓ Search intensity valid")
print("✓ Relevance scores valid")
print("✓ Boolean signals valid")
print("✓ Search logic consistent")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nSEARCH INTELLIGENCE COMPLETE")