# ==========================================================
# ECDIP - Subscriber Dimension Generator
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_FILE = DATA_DIR / "dim_subscriber.csv"

TOTAL_SUBSCRIBERS = 100_000

# ----------------------------------------------------------
# Reference data
# ----------------------------------------------------------

region = pd.read_csv(
    DATA_DIR / "dim_region.csv"
)

plan = pd.read_csv(
    DATA_DIR / "dim_subscription_plan.csv"
)

# ----------------------------------------------------------
# Subscriber generation
# ----------------------------------------------------------

print("=" * 70)
print("ECDIP - SUBSCRIBER DIMENSION GENERATOR")
print("=" * 70)

subscriber_ids = np.arange(
    1,
    TOTAL_SUBSCRIBERS + 1
)

# ----------------------------------------------------------
# Demographic / behavioral segmentation
# ----------------------------------------------------------

age_groups = np.random.choice(
    [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55+"
    ],
    TOTAL_SUBSCRIBERS,
    p=[
        0.22,
        0.34,
        0.22,
        0.14,
        0.08
    ]
)

customer_segments = np.random.choice(
    [
        "Value Seeker",
        "Casual Viewer",
        "Power Viewer",
        "Family",
        "Premium Enthusiast"
    ],
    TOTAL_SUBSCRIBERS,
    p=[
        0.22,
        0.28,
        0.18,
        0.20,
        0.12
    ]
)

acquisition_channels = np.random.choice(
    [
        "Organic",
        "Search",
        "Social",
        "Referral",
        "Partner",
        "Campaign"
    ],
    TOTAL_SUBSCRIBERS,
    p=[
        0.25,
        0.18,
        0.20,
        0.12,
        0.10,
        0.15
    ]
)

# ----------------------------------------------------------
# Region assignment
# ----------------------------------------------------------

region_ids = np.random.choice(
    region["region_id"].values,
    TOTAL_SUBSCRIBERS
)

# ----------------------------------------------------------
# Subscription plan assignment
# ----------------------------------------------------------

plan_ids = np.random.choice(
    plan["plan_id"].values,
    TOTAL_SUBSCRIBERS
)

# ----------------------------------------------------------
# Tenure
# ----------------------------------------------------------

tenure_months = np.random.gamma(
    shape=2.5,
    scale=6.0,
    size=TOTAL_SUBSCRIBERS
)

tenure_months = np.clip(
    tenure_months,
    1,
    72
).round(1)

# ----------------------------------------------------------
# Customer value
# ----------------------------------------------------------

customer_value = np.select(
    [
        customer_segments == "Value Seeker",
        customer_segments == "Casual Viewer",
        customer_segments == "Power Viewer",
        customer_segments == "Family",
        customer_segments == "Premium Enthusiast"
    ],
    [
        "Low",
        "Medium",
        "High",
        "Medium",
        "Very High"
    ],
    default="Medium"
)

# ----------------------------------------------------------
# Activity level
# ----------------------------------------------------------

activity_score = np.random.normal(
    60,
    18,
    TOTAL_SUBSCRIBERS
)

activity_score = np.clip(
    activity_score,
    0,
    100
).round(2)

# ----------------------------------------------------------
# Churn propensity
# ----------------------------------------------------------

churn_propensity = (
    100
    - activity_score
)

churn_propensity += np.random.normal(
    0,
    10,
    TOTAL_SUBSCRIBERS
)

churn_propensity = np.clip(
    churn_propensity,
    0,
    100
).round(2)

# ----------------------------------------------------------
# Build dimension
# ----------------------------------------------------------

subscriber = pd.DataFrame({

    "subscriber_id":
        subscriber_ids,

    "region_id":
        region_ids,

    "plan_id":
        plan_ids,

    "age_group":
        age_groups,

    "customer_segment":
        customer_segments,

    "acquisition_channel":
        acquisition_channels,

    "tenure_months":
        tenure_months,

    "customer_value_segment":
        customer_value,

    "activity_score":
        activity_score,

    "churn_propensity":
        churn_propensity,

    "created_at":
        pd.Timestamp.now(),

    "updated_at":
        pd.Timestamp.now()
})

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

print("\nRunning subscriber validation...")

assert len(subscriber) == TOTAL_SUBSCRIBERS

assert subscriber[
    "subscriber_id"
].is_unique

assert subscriber[
    "region_id"
].isin(
    region["region_id"]
).all()

assert subscriber[
    "plan_id"
].isin(
    plan["plan_id"]
).all()

assert subscriber[
    "tenure_months"
].between(
    1,
    72
).all()

assert subscriber[
    "activity_score"
].between(
    0,
    100
).all()

assert subscriber[
    "churn_propensity"
].between(
    0,
    100
).all()

assert subscriber[
    "subscriber_id"
].notna().all()

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

subscriber.to_csv(
    OUTPUT_FILE,
    index=False
)

# ----------------------------------------------------------
# Report
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("SUBSCRIBER DATA GENERATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Subscribers generated : "
    f"{len(subscriber):,}"
)

print(
    f"Average tenure        : "
    f"{subscriber['tenure_months'].mean():.2f} months"
)

print(
    f"Average activity      : "
    f"{subscriber['activity_score'].mean():.2f}"
)

print(
    f"Average churn propensity: "
    f"{subscriber['churn_propensity'].mean():.2f}"
)

print("\nCustomer segments:")

print(
    subscriber[
        "customer_segment"
    ].value_counts()
)

print("\nValidation:")
print("✓ Subscriber IDs are unique")
print("✓ Region relationships are valid")
print("✓ Subscription plan relationships are valid")
print("✓ Tenure values are valid")
print("✓ Activity scores are valid")
print("✓ Churn propensity is valid")
print("✓ Required fields are populated")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nSUBSCRIBER DIMENSION COMPLETE")