# ==========================================================
# ECDIP - Engagement Intelligence Generator
# ==========================================================
#
# SOURCE:
#   fact_viewing_events.csv
#   dim_content.csv
#   dim_region.csv
#
# OUTPUT:
#   fact_engagement.csv
#
# GRAIN:
#   One record per Content + Region + Date
#
# PostgreSQL target:
#   fact_engagement
#
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# 1. CONFIGURATION
# ==========================================================

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_FILE = DATA_DIR / "fact_engagement.csv"


# ==========================================================
# 2. HELPER
# ==========================================================

def require_columns(df, required, name):
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(
            f"{name} is missing required columns: {missing}"
        )


# ==========================================================
# 3. LOAD SOURCE DATA
# ==========================================================

print("=" * 70)
print("ECDIP - ENGAGEMENT INTELLIGENCE GENERATOR")
print("=" * 70)

print("\nLoading viewing events...")

viewing = pd.read_csv(
    DATA_DIR / "fact_viewing_events.csv"
)

content = pd.read_csv(
    DATA_DIR / "dim_content.csv",
    usecols=[
        "content_id",
        "imdb_rating"
    ]
)

region = pd.read_csv(
    DATA_DIR / "dim_region.csv",
    usecols=[
        "region_id"
    ]
)


# ==========================================================
# 4. SOURCE SCHEMA VALIDATION
# ==========================================================

require_columns(
    viewing,
    [
        "viewing_id",
        "content_id",
        "region_id",
        "date_id",
        "watch_hours",
        "completion_rate",
        "rewatch_count"
    ],
    "fact_viewing_events"
)

require_columns(
    content,
    [
        "content_id",
        "imdb_rating"
    ],
    "dim_content"
)

require_columns(
    region,
    [
        "region_id"
    ],
    "dim_region"
)


# ==========================================================
# 5. BASIC SOURCE QUALITY
# ==========================================================

print("\nValidating source data...")

assert not viewing.empty, "Viewing dataset is empty."

assert viewing["viewing_id"].notna().all(), \
    "Missing viewing IDs."

assert viewing["viewing_id"].is_unique, \
    "Duplicate viewing IDs found."

assert viewing["content_id"].notna().all(), \
    "Missing content IDs."

assert viewing["region_id"].notna().all(), \
    "Missing region IDs."

assert viewing["date_id"].notna().all(), \
    "Missing date IDs."


# ==========================================================
# 6. REFERENTIAL INTEGRITY
# ==========================================================

invalid_content = (
    ~viewing["content_id"].isin(content["content_id"])
).sum()

invalid_region = (
    ~viewing["region_id"].isin(region["region_id"])
).sum()

if invalid_content > 0:
    raise ValueError(
        f"{invalid_content:,} invalid content_id values found."
    )

if invalid_region > 0:
    raise ValueError(
        f"{invalid_region:,} invalid region_id values found."
    )


# ==========================================================
# 7. NUMERIC CLEANING
# ==========================================================

viewing["watch_hours"] = pd.to_numeric(
    viewing["watch_hours"],
    errors="coerce"
)

viewing["completion_rate"] = pd.to_numeric(
    viewing["completion_rate"],
    errors="coerce"
)

viewing["rewatch_count"] = pd.to_numeric(
    viewing["rewatch_count"],
    errors="coerce"
)

content["imdb_rating"] = pd.to_numeric(
    content["imdb_rating"],
    errors="coerce"
)


# ==========================================================
# 8. RANGE VALIDATION
# ==========================================================

if viewing["watch_hours"].isna().any():
    raise ValueError("Invalid watch_hours values.")

if viewing["completion_rate"].isna().any():
    raise ValueError("Invalid completion_rate values.")

if viewing["rewatch_count"].isna().any():
    raise ValueError("Invalid rewatch_count values.")

if viewing["watch_hours"].lt(0).any():
    raise ValueError("Negative watch_hours detected.")

if viewing["completion_rate"].lt(0).any() or \
   viewing["completion_rate"].gt(100).any():

    raise ValueError(
        "completion_rate must be between 0 and 100."
    )

if viewing["rewatch_count"].lt(0).any():
    raise ValueError(
        "Negative rewatch_count detected."
    )


# ==========================================================
# 9. JOIN CONTENT QUALITY
# ==========================================================

print("Enriching viewing behavior with content quality...")

viewing = viewing.merge(
    content,
    on="content_id",
    how="left",
    validate="many_to_one"
)

assert viewing["imdb_rating"].notna().all(), \
    "Content quality enrichment failed."


# ==========================================================
# 10. DERIVE ENGAGEMENT SIGNALS
# ==========================================================

# Normalize content quality.
rating_factor = (
    (viewing["imdb_rating"] - 5.0) / 4.0
)

rating_factor = np.clip(
    rating_factor,
    0,
    1
)


# Completion signal.
completion_factor = (
    viewing["completion_rate"] / 100.0
)


# Watch intensity.
mean_watch = viewing["watch_hours"].mean()

if mean_watch <= 0:
    mean_watch = 1.0

watch_factor = (
    viewing["watch_hours"] / mean_watch
)

watch_factor = np.clip(
    watch_factor,
    0.25,
    3.0
)


# Rewatch signal.
rewatch_signal = np.clip(
    viewing["rewatch_count"] / 3.0,
    0,
    1
)


# ==========================================================
# 11. POSITIVE ENGAGEMENT PROPENSITY
# ==========================================================

like_probability = (
    0.04
    + 0.18 * rating_factor
    + 0.12 * completion_factor
    + 0.04 * np.minimum(watch_factor, 2.0)
    + 0.05 * rewatch_signal
)

like_probability = np.clip(
    like_probability,
    0.01,
    0.50
)


# ==========================================================
# 12. NEGATIVE ENGAGEMENT PROPENSITY
# ==========================================================

dislike_probability = (
    0.02
    + 0.07 * (1 - rating_factor)
    + 0.06 * (1 - completion_factor)
)

dislike_probability = np.clip(
    dislike_probability,
    0.005,
    0.20
)


# ==========================================================
# 13. GENERATE INTERACTION SIGNALS
# ==========================================================

random_like = np.random.random(
    len(viewing)
)

random_dislike = np.random.random(
    len(viewing)
)

viewing["like_event"] = (
    random_like < like_probability
)

viewing["dislike_event"] = (
    random_dislike < dislike_probability
)


# ==========================================================
# 14. AGGREGATE TO ANALYTICAL GRAIN
# ==========================================================

print("Aggregating engagement intelligence...")

engagement = (
    viewing
    .groupby(
        [
            "content_id",
            "region_id",
            "date_id"
        ],
        as_index=False
    )
    .agg(
        likes=(
            "like_event",
            "sum"
        ),

        dislikes=(
            "dislike_event",
            "sum"
        ),

        average_watch_percentage=(
            "completion_rate",
            "mean"
        ),

        completion_rate=(
            "completion_rate",
            "mean"
        ),

        rewatch_rate=(
            "rewatch_count",
            lambda x: (
                (x > 0).mean() * 100
            )
        )
    )
)


# ==========================================================
# 15. CLEAN OUTPUT VALUES
# ==========================================================

engagement["likes"] = (
    engagement["likes"]
    .astype("int64")
)

engagement["dislikes"] = (
    engagement["dislikes"]
    .astype("int64")
)

engagement["average_watch_percentage"] = (
    engagement["average_watch_percentage"]
    .clip(0, 100)
    .round(2)
)

engagement["completion_rate"] = (
    engagement["completion_rate"]
    .clip(0, 100)
    .round(2)
)

engagement["rewatch_rate"] = (
    engagement["rewatch_rate"]
    .clip(0, 100)
    .round(2)
)


# ==========================================================
# 16. CREATE PRIMARY KEY
# ==========================================================

engagement.insert(
    0,
    "engagement_id",
    np.arange(
        1,
        len(engagement) + 1,
        dtype="int64"
    )
)


# ==========================================================
# 17. CREATED TIMESTAMP
# ==========================================================

engagement["created_at"] = pd.Timestamp.now()


# ==========================================================
# 18. EXACT POSTGRES COLUMN ORDER
# ==========================================================

engagement = engagement[
    [
        "engagement_id",
        "content_id",
        "region_id",
        "date_id",
        "likes",
        "dislikes",
        "average_watch_percentage",
        "completion_rate",
        "rewatch_rate",
        "created_at"
    ]
]


# ==========================================================
# 19. ENTERPRISE DATA QUALITY VALIDATION
# ==========================================================

print("\nRunning enterprise validation...")

# Primary key
assert engagement[
    "engagement_id"
].is_unique


# Key fields
assert engagement[
    [
        "engagement_id",
        "content_id",
        "region_id",
        "date_id"
    ]
].notna().all().all()


# Foreign-key relationships
assert engagement[
    "content_id"
].isin(
    content["content_id"]
).all()


assert engagement[
    "region_id"
].isin(
    region["region_id"]
).all()


# Value ranges
assert engagement[
    "likes"
].ge(0).all()


assert engagement[
    "dislikes"
].ge(0).all()


assert engagement[
    "average_watch_percentage"
].between(0, 100).all()


assert engagement[
    "completion_rate"
].between(0, 100).all()


assert engagement[
    "rewatch_rate"
].between(0, 100).all()


# Analytical grain
assert not engagement[
    [
        "content_id",
        "region_id",
        "date_id"
    ]
].duplicated().any()


# ==========================================================
# 20. SAVE
# ==========================================================

engagement.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================================
# 21. FINAL REPORT
# ==========================================================

print("\n" + "=" * 70)
print("ENGAGEMENT DATA GENERATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Source viewing events : "
    f"{len(viewing):,}"
)

print(
    f"Engagement records    : "
    f"{len(engagement):,}"
)

print(
    f"Average likes         : "
    f"{engagement['likes'].mean():.2f}"
)

print(
    f"Average dislikes      : "
    f"{engagement['dislikes'].mean():.2f}"
)

print(
    f"Average watch %       : "
    f"{engagement['average_watch_percentage'].mean():.2f}%"
)

print(
    f"Average completion    : "
    f"{engagement['completion_rate'].mean():.2f}%"
)

print(
    f"Average rewatch rate  : "
    f"{engagement['rewatch_rate'].mean():.2f}%"
)

print("\nValidation:")
print("✓ Viewing IDs validated")
print("✓ Content relationships validated")
print("✓ Region relationships validated")
print("✓ Engagement IDs are unique")
print("✓ No invalid negative values")
print("✓ Percentage ranges are valid")
print("✓ Content + Region + Date grain is unique")
print("✓ PostgreSQL column structure matched")

print("\nOutput:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("ENGAGEMENT INTELLIGENCE COMPLETE")
print("=" * 70)