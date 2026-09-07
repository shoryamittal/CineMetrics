# ===========================================
# CPIP - Revenue Fact Generator
# ===========================================

import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------
# Configuration
# -------------------------------------------

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -------------------------------------------
# Load required data
# -------------------------------------------

viewing_df = pd.read_csv(
    OUTPUT_DIR / "fact_viewing_events.csv",
    usecols=[
        "viewing_id",
        "content_id",
        "region_id",
        "plan_id",
        "date_id",
        "watch_hours"
    ]
)

plan_df = pd.read_csv(
    OUTPUT_DIR / "dim_subscription_plan.csv"
)

region_df = pd.read_csv(
    OUTPUT_DIR / "dim_region.csv"
)

# -------------------------------------------
# Revenue is generated from viewing activity
# -------------------------------------------

revenue_df = viewing_df.copy()

# Join subscription plan information
revenue_df = revenue_df.merge(
    plan_df[
        [
            "plan_id",
            "monthly_price"
        ]
    ],
    on="plan_id",
    how="left",
    validate="many_to_one"
)

# -------------------------------------------
# Regional economic multiplier
# -------------------------------------------

region_multiplier = {
    1: 1.00,   # India
    2: 1.45,   # United States
    3: 1.25,   # Canada
    4: 1.35,   # United Kingdom
    5: 1.30,   # Germany
    6: 1.28,   # France
    7: 1.20,   # Spain
    8: 1.22,   # Italy
    9: 1.40,   # Japan
    10: 1.35,  # South Korea
    11: 1.30,  # Australia
    12: 0.90,  # Brazil
    13: 0.95,  # Mexico
    14: 1.30,  # Singapore
    15: 1.35   # UAE
}

revenue_df["region_multiplier"] = (
    revenue_df["region_id"]
    .map(region_multiplier)
    .fillna(1.0)
)

# -------------------------------------------
# Estimate revenue contribution
# -------------------------------------------

# A viewing event represents a fraction of
# the subscriber's subscription value.

base_event_value = (
    revenue_df["monthly_price"] / 30
)

# Allocate subscription value according to
# relative viewing intensity.

watch_factor = (
    revenue_df["watch_hours"]
    / revenue_df["watch_hours"].mean()
)

watch_factor = np.clip(
    watch_factor,
    0.25,
    3.0
)

revenue_df["gross_revenue"] = (
    base_event_value
    * watch_factor
    * revenue_df["region_multiplier"]
)

# Add realistic variation
revenue_df["gross_revenue"] *= np.random.uniform(
    0.85,
    1.15,
    len(revenue_df)
)

# -------------------------------------------
# Currency conversion
# -------------------------------------------

currency_rate = {
    1: 1.0,       # INR base
    2: 83.0,      # USD
    3: 61.0,      # CAD
    4: 105.0,     # GBP
    5: 90.0,      # EUR
    6: 90.0,
    7: 90.0,
    8: 90.0,
    9: 0.56,      # JPY
    10: 0.062,    # KRW
    11: 54.0,     # AUD
    12: 16.0,     # BRL
    13: 4.8,      # MXN
    14: 22.5,     # SGD
    15: 22.6      # AED
}

revenue_df["currency_rate_to_inr"] = (
    revenue_df["region_id"]
    .map(currency_rate)
    .fillna(1.0)
)

# -------------------------------------------
# Final revenue
# -------------------------------------------

revenue_df["revenue_amount"] = (
    revenue_df["gross_revenue"]
    * revenue_df["currency_rate_to_inr"]
)

revenue_df["revenue_amount"] = (
    revenue_df["revenue_amount"]
    .round(2)
)

# -------------------------------------------
# Revenue type
# -------------------------------------------

revenue_df["revenue_type"] = np.where(
    revenue_df["plan_id"].isin([4, 5, 7, 8]),
    "Premium Subscription",
    "Subscription"
)

# -------------------------------------------
# Select final columns
# -------------------------------------------

final_df = revenue_df[
    [
        "viewing_id",
        "content_id",
        "region_id",
        "plan_id",
        "date_id",
        "revenue_type",
        "revenue_amount"
    ]
].copy()

# -------------------------------------------
# Add revenue ID
# -------------------------------------------

final_df.insert(
    0,
    "revenue_id",
    range(1, len(final_df) + 1)
)

# -------------------------------------------
# Timestamp
# -------------------------------------------

final_df["created_at"] = pd.Timestamp.now()

# -------------------------------------------
# Validation
# -------------------------------------------

assert len(final_df) == len(viewing_df)

assert final_df["revenue_id"].is_unique

assert final_df["revenue_amount"].gt(0).all()

assert final_df["content_id"].isin(
    viewing_df["content_id"]
).all()

assert final_df["region_id"].isin(
    region_df["region_id"]
).all()

assert final_df["plan_id"].isin(
    plan_df["plan_id"]
).all()

# -------------------------------------------
# Save
# -------------------------------------------

output_file = (
    OUTPUT_DIR /
    "fact_revenue.csv"
)

final_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Results
# -------------------------------------------

print("=" * 65)
print("REVENUE DATA GENERATED SUCCESSFULLY")
print("=" * 65)

print(
    f"Records generated : {len(final_df):,}"
)

print(
    f"Total revenue     : ₹{final_df['revenue_amount'].sum():,.2f}"
)

print(
    f"Average event     : ₹{final_df['revenue_amount'].mean():,.2f}"
)

print("\nRevenue by type:")

print(
    final_df.groupby("revenue_type")[
        "revenue_amount"
    ].agg(
        ["count", "sum", "mean"]
    )
)

print("\nValidation:")

print("✓ Revenue IDs are unique")
print("✓ Revenue values are positive")
print("✓ Content relationships are valid")
print("✓ Region relationships are valid")
print("✓ Subscription relationships are valid")

print("\nRevenue generation complete.")