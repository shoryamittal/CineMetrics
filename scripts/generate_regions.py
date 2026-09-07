# ===========================================
# CPIP - Region Data Generator
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
# Region master data
# -------------------------------------------

regions = [
    ("India", "South Asia", "Asia", "INR", "Asia/Kolkata"),
    ("United States", "North America", "North America", "USD", "America/New_York"),
    ("Canada", "North America", "North America", "CAD", "America/Toronto"),
    ("United Kingdom", "Western Europe", "Europe", "GBP", "Europe/London"),
    ("Germany", "Western Europe", "Europe", "EUR", "Europe/Berlin"),
    ("France", "Western Europe", "Europe", "EUR", "Europe/Paris"),
    ("Spain", "Southern Europe", "Europe", "EUR", "Europe/Madrid"),
    ("Italy", "Southern Europe", "Europe", "EUR", "Europe/Rome"),
    ("Japan", "East Asia", "Asia", "JPY", "Asia/Tokyo"),
    ("South Korea", "East Asia", "Asia", "KRW", "Asia/Seoul"),
    ("Australia", "Oceania", "Oceania", "AUD", "Australia/Sydney"),
    ("Brazil", "South America", "South America", "BRL", "America/Sao_Paulo"),
    ("Mexico", "Latin America", "North America", "MXN", "America/Mexico_City"),
    ("Singapore", "Southeast Asia", "Asia", "SGD", "Asia/Singapore"),
    ("United Arab Emirates", "Middle East", "Asia", "AED", "Asia/Dubai")
]

# -------------------------------------------
# Create DataFrame
# -------------------------------------------

region_df = pd.DataFrame(
    regions,
    columns=[
        "country_name",
        "region_name",
        "continent",
        "currency",
        "timezone"
    ]
)

# -------------------------------------------
# Add primary key
# -------------------------------------------

region_df.insert(
    0,
    "region_id",
    range(1, len(region_df) + 1)
)

# -------------------------------------------
# Audit timestamps
# -------------------------------------------

region_df["created_at"] = pd.Timestamp.now()

region_df["updated_at"] = pd.Timestamp.now()

# -------------------------------------------
# Save CSV
# -------------------------------------------

output_file = OUTPUT_DIR / "dim_region.csv"

region_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Validation
# -------------------------------------------

assert region_df["region_id"].is_unique

assert region_df["country_name"].notna().all()

assert not region_df["country_name"].duplicated().any()

# -------------------------------------------
# Result
# -------------------------------------------

print("=" * 55)
print("REGION DATA GENERATED SUCCESSFULLY")
print("=" * 55)

print(f"Records generated : {len(region_df)}")
print(f"Output file       : {output_file}")

print("\nPreview:")
print(region_df.head())

print("\nValidation:")
print("✓ IDs are unique")
print("✓ Country names are not missing")
print("✓ No duplicate countries")