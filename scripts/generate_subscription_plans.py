# ===========================================
# CPIP - Subscription Plan Data Generator
# ===========================================

import pandas as pd
from pathlib import Path

# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Output directory
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Subscription plan master data
plans = [
    ("Mobile", 149.00, 1, "SD", True),
    ("Basic", 199.00, 1, "HD", True),
    ("Standard", 299.00, 2, "Full HD", False),
    ("Premium", 499.00, 4, "4K", False),
    ("Family", 599.00, 6, "4K", False),
    ("Student", 129.00, 1, "HD", True),
    ("Annual Standard", 2999.00, 2, "Full HD", False),
    ("Annual Premium", 4999.00, 4, "4K", False)
]

# Convert to DataFrame
plan_df = pd.DataFrame(
    plans,
    columns=[
        "plan_name",
        "monthly_price",
        "max_devices",
        "video_quality",
        "ads_supported"
    ]
)

# Add primary key
plan_df.insert(
    0,
    "plan_id",
    range(1, len(plan_df) + 1)
)

# Save CSV
output_file = OUTPUT_DIR / "dim_subscription_plan.csv"

plan_df.to_csv(
    output_file,
    index=False
)

print("=" * 50)
print("Subscription Plan Data Generated Successfully")
print(f"Records generated: {len(plan_df)}")
print(f"File: {output_file}")
print("=" * 50)

print(plan_df)