# ===========================================
# CPIP - Campaign Data Generator
# ===========================================

import pandas as pd
from pathlib import Path
from faker import Faker
import random

# -------------------------------------------
# Configuration
# -------------------------------------------

fake = Faker()

random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -------------------------------------------
# Business reference values
# -------------------------------------------

campaign_types = [
    "Content Launch",
    "Seasonal",
    "Retention",
    "Acquisition",
    "Brand Awareness",
    "Regional Expansion"
]

channels = [
    "YouTube",
    "Instagram",
    "Google",
    "Television",
    "Email",
    "Influencer",
    "In-App",
    "Search"
]

# -------------------------------------------
# Generate campaigns
# -------------------------------------------

rows = []

for campaign_id in range(1, 501):

    start_date = fake.date_between(
        start_date=pd.Timestamp("2020-01-01").date(),
        end_date=pd.Timestamp("2029-10-01").date()
    )

    duration_days = random.randint(7, 90)

    end_date = (
        pd.Timestamp(start_date)
        + pd.Timedelta(days=duration_days)
    ).date()

    budget = random.uniform(
        10000,
        5000000
    )

    rows.append({
        "campaign_id": campaign_id,

        "campaign_name":
            f"{fake.word().title()} Campaign {campaign_id}",

        "campaign_type":
            random.choice(campaign_types),

        "campaign_channel":
            random.choice(channels),

        "start_date":
            start_date,

        "end_date":
            end_date,

        "budget":
            round(budget, 2),

        "created_at":
            pd.Timestamp.now(),

        "updated_at":
            pd.Timestamp.now()
    })

# -------------------------------------------
# DataFrame
# -------------------------------------------

campaign_df = pd.DataFrame(rows)

# -------------------------------------------
# Validation
# -------------------------------------------

assert campaign_df["campaign_id"].is_unique

assert campaign_df["campaign_name"].notna().all()

assert not campaign_df["campaign_name"].duplicated().any()

assert campaign_df["budget"].gt(0).all()

assert (
    pd.to_datetime(campaign_df["end_date"])
    >= pd.to_datetime(campaign_df["start_date"])
).all()

# -------------------------------------------
# Save
# -------------------------------------------

output_file = OUTPUT_DIR / "dim_campaign.csv"

campaign_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Results
# -------------------------------------------

print("=" * 60)
print("CAMPAIGN DATA GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Records generated : {len(campaign_df)}")
print(f"Output file       : {output_file}")

print("\nPreview:")
print(campaign_df.head())

print("\nValidation:")
print("✓ Campaign IDs are unique")
print("✓ Campaign names are not missing")
print("✓ Campaign names are unique")
print("✓ Budgets are positive")
print("✓ End dates are after start dates")