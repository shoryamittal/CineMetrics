# ===========================================
# CPIP - Calendar Data Generator
# ===========================================

import pandas as pd
from pathlib import Path

# -------------------------------------------
# Project paths
# -------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -------------------------------------------
# Generate daily dates
# -------------------------------------------

dates = pd.date_range(
    start="2020-01-01",
    end="2029-12-31",
    freq="D"
)

calendar_df = pd.DataFrame({
    "date_id": dates.date
})

# -------------------------------------------
# Calendar attributes
# -------------------------------------------

calendar_df["day"] = dates.day

calendar_df["month"] = dates.month

calendar_df["quarter"] = dates.quarter

calendar_df["year"] = dates.year

calendar_df["week_of_year"] = dates.isocalendar().week.to_numpy()

calendar_df["day_name"] = dates.day_name()

calendar_df["month_name"] = dates.month_name()

calendar_df["is_weekend"] = dates.dayofweek >= 5

# -------------------------------------------
# Validation
# -------------------------------------------

assert calendar_df["date_id"].is_unique

assert calendar_df["date_id"].notna().all()

assert calendar_df["year"].between(2020, 2029).all()

# -------------------------------------------
# Save CSV
# -------------------------------------------

output_file = OUTPUT_DIR / "dim_calendar.csv"

calendar_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Result
# -------------------------------------------

print("=" * 55)
print("CALENDAR DATA GENERATED SUCCESSFULLY")
print("=" * 55)

print(f"Records generated : {len(calendar_df)}")
print(f"Start date        : {calendar_df['date_id'].min()}")
print(f"End date          : {calendar_df['date_id'].max()}")
print(f"Output file       : {output_file}")

print("\nPreview:")
print(calendar_df.head())

print("\nValidation:")
print("✓ Dates are unique")
print("✓ Dates are not missing")
print("✓ Year range is valid")