# ==========================================================
# ECDIP - Subscription Event Intelligence Generator
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

OUTPUT_FILE = DATA_DIR / "fact_subscription_events.csv"

# ----------------------------------------------------------
# Load enterprise dimensions
# ----------------------------------------------------------

print("=" * 70)
print("ECDIP - SUBSCRIPTION EVENT GENERATOR")
print("=" * 70)

subscriber = pd.read_csv(
    DATA_DIR / "dim_subscriber.csv"
)

plan = pd.read_csv(
    DATA_DIR / "dim_subscription_plan.csv"
)

calendar = pd.read_csv(
    DATA_DIR / "dim_calendar.csv"
)

region = pd.read_csv(
    DATA_DIR / "dim_region.csv"
)

# ----------------------------------------------------------
# Determine event volume
# ----------------------------------------------------------

TOTAL_EVENTS = 500_000

# ----------------------------------------------------------
# Create event IDs
# ----------------------------------------------------------

event_ids = np.arange(
    1,
    TOTAL_EVENTS + 1
)

# ----------------------------------------------------------
# Select subscribers
# ----------------------------------------------------------

subscriber_ids = np.random.choice(
    subscriber["subscriber_id"].values,
    size=TOTAL_EVENTS
)

# ----------------------------------------------------------
# Select plans
# ----------------------------------------------------------

plan_ids = np.random.choice(
    plan["plan_id"].values,
    size=TOTAL_EVENTS
)

# ----------------------------------------------------------
# Select regions
# ----------------------------------------------------------

region_ids = np.random.choice(
    region["region_id"].values,
    size=TOTAL_EVENTS
)

# ----------------------------------------------------------
# Select dates
# ----------------------------------------------------------

date_ids = np.random.choice(
    calendar["date_id"].values,
    size=TOTAL_EVENTS
)

# ----------------------------------------------------------
# Event types
# ----------------------------------------------------------

event_types = np.random.choice(
    [
        "subscription",
        "upgrade",
        "downgrade",
        "renewal",
        "cancellation",
        "reactivation"
    ],
    size=TOTAL_EVENTS,
    p=[
        0.30,
        0.10,
        0.08,
        0.28,
        0.16,
        0.08
    ]
)

# ----------------------------------------------------------
# Event value
# ----------------------------------------------------------

plan_price_lookup = plan.set_index(
    "plan_id"
)["monthly_price"]

monthly_price = pd.Series(
    plan_ids
).map(
    plan_price_lookup
).fillna(
    plan["monthly_price"].median()
).to_numpy()

# ----------------------------------------------------------
# Event value logic
# ----------------------------------------------------------

event_multiplier = np.select(
    [
        event_types == "subscription",
        event_types == "upgrade",
        event_types == "downgrade",
        event_types == "renewal",
        event_types == "cancellation",
        event_types == "reactivation"
    ],
    [
        1.0,
        1.25,
        0.75,
        1.0,
        0.0,
        1.10
    ],
    default=1.0
)

event_value = (
    monthly_price
    * event_multiplier
    * np.random.uniform(
        0.90,
        1.10,
        TOTAL_EVENTS
    )
)

event_value = np.round(
    np.maximum(
        event_value,
        0
    ),
    2
)

# ----------------------------------------------------------
# Tenure / lifecycle signal
# ----------------------------------------------------------

tenure_months = np.random.gamma(
    shape=2.5,
    scale=5.0,
    size=TOTAL_EVENTS
)

tenure_months = np.clip(
    tenure_months,
    1,
    60
).round(1)

# ----------------------------------------------------------
# Churn probability
# ----------------------------------------------------------

base_churn_probability = np.where(
    event_types == "cancellation",
    0.80,
    0.08
)

churn_probability = np.clip(
    base_churn_probability
    + np.maximum(
        0,
        0.15 - tenure_months / 200
    ),
    0,
    0.90
)

churn_flag = (
    np.random.random(TOTAL_EVENTS)
    < churn_probability
)

# Cancellation events must be churn events.
churn_flag[event_types == "cancellation"] = True

# ----------------------------------------------------------
# Build DataFrame
# ----------------------------------------------------------

subscription = pd.DataFrame({

    "subscription_event_id":
        event_ids,

    "subscriber_id":
        subscriber_ids,

    "plan_id":
        plan_ids,

    "region_id":
        region_ids,

    "date_id":
        date_ids,

    "event_type":
        event_types,

    "event_value":
        event_value,

    "tenure_months":
        tenure_months,

    "churn_flag":
        churn_flag,

    "created_at":
        pd.Timestamp.now()
})

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

print("\nRunning subscription-event validation...")

assert len(subscription) == TOTAL_EVENTS

assert subscription[
    "subscription_event_id"
].is_unique

assert subscription[
    "subscriber_id"
].isin(
    subscriber["subscriber_id"]
).all()

assert subscription[
    "plan_id"
].isin(
    plan["plan_id"]
).all()

assert subscription[
    "region_id"
].isin(
    region["region_id"]
).all()

assert subscription[
    "date_id"
].isin(
    calendar["date_id"]
).all()

assert subscription[
    "event_value"
].ge(0).all()

assert subscription[
    "tenure_months"
].between(
    1,
    60
).all()

assert subscription[
    "churn_flag"
].isin(
    [True, False]
).all()

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

subscription.to_csv(
    OUTPUT_FILE,
    index=False
)

# ----------------------------------------------------------
# Report
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("SUBSCRIPTION EVENT DATA GENERATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Records generated : "
    f"{len(subscription):,}"
)

print(
    f"Churn events      : "
    f"{subscription['churn_flag'].sum():,}"
)

print(
    f"Churn rate        : "
    f"{subscription['churn_flag'].mean() * 100:.2f}%"
)

print(
    f"Average tenure    : "
    f"{subscription['tenure_months'].mean():.2f} months"
)

print(
    f"Total event value : "
    f"₹{subscription['event_value'].sum():,.2f}"
)

print("\nEvent distribution:")

print(
    subscription["event_type"]
    .value_counts()
)

print("\nValidation:")
print("✓ Subscriber relationships valid")
print("✓ Plan relationships valid")
print("✓ Region relationships valid")
print("✓ Calendar relationships valid")
print("✓ Event IDs unique")
print("✓ Event values valid")
print("✓ Tenure values valid")
print("✓ Churn flags valid")

print("\nOutput:")
print(OUTPUT_FILE)

print("\nSUBSCRIPTION INTELLIGENCE COMPLETE")