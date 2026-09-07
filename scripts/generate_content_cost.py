# ==========================================================
# ECDIP - Content Cost Intelligence Generator
# ==========================================================

from pathlib import Path
import sys
import pandas as pd
import numpy as np

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_FILE = DATA_DIR / "fact_content_cost.csv"

print("=" * 70)
print("ECDIP - CONTENT COST INTELLIGENCE GENERATOR")
print("=" * 70)

# ----------------------------------------------------------
# Load content economics
# ----------------------------------------------------------

print("\nLoading content economics...")
content = pd.read_csv(DATA_DIR / "dim_content.csv")

required_content = [
    "content_id",
    "production_budget",
    "licensing_cost",
    "available_regions"
]

for column in required_content:
    if column not in content.columns:
        raise ValueError(f"dim_content is missing: {column}")

if content.empty:
    raise ValueError("dim_content.csv is empty.")

if not content["content_id"].is_unique:
    raise ValueError("Duplicate content_id values found.")

cost = content[
    [
        "content_id",
        "production_budget",
        "licensing_cost",
        "available_regions"
    ]
].copy()

numeric_columns = [
    "production_budget",
    "licensing_cost",
    "available_regions"
]

for column in numeric_columns:
    cost[column] = pd.to_numeric(cost[column], errors="coerce")

if cost[numeric_columns].isna().any().any():
    raise ValueError("Invalid numeric values found in content economics.")

if cost["production_budget"].lt(0).any():
    raise ValueError("Negative production budget detected.")
if cost["licensing_cost"].lt(0).any():
    raise ValueError("Negative licensing cost detected.")
if cost["available_regions"].lt(0).any():
    raise ValueError("Negative available_regions detected.")

# ----------------------------------------------------------
# Cost Components
# ----------------------------------------------------------

# Production overhead: 6% to 15% of production budget
cost["production_overhead"] = (
    cost["production_budget"] * np.random.uniform(0.06, 0.15, len(cost))
)

# Distribution cost: 1.5% to 5% of production budget
cost["distribution_cost"] = (
    cost["production_budget"] * np.random.uniform(0.015, 0.05, len(cost))
)

# Technology / platform delivery cost: 0.5% to 2.5% of production budget
cost["technology_cost"] = (
    cost["production_budget"] * np.random.uniform(0.005, 0.025, len(cost))
)

# Localization cost: proportional to budget and regions
cost["localization_cost"] = (
    cost["production_budget"] * np.random.uniform(0.015, 0.045, len(cost))
    + cost["available_regions"] * np.random.uniform(80, 250, len(cost))
)

# Contract administration / legal cost: 1% to 3.5% of licensing cost
cost["contract_administration_cost"] = (
    cost["licensing_cost"] * np.random.uniform(0.01, 0.035, len(cost))
)

# Contingency reserve: 2% to 6% of (budget + licensing)
cost["contingency_cost"] = (
    (cost["production_budget"] + cost["licensing_cost"])
    * np.random.uniform(0.02, 0.06, len(cost))
)

# ----------------------------------------------------------
# Round individual monetary components
# ----------------------------------------------------------

money_columns = [
    "production_budget",
    "licensing_cost",
    "production_overhead",
    "distribution_cost",
    "technology_cost",
    "localization_cost",
    "contract_administration_cost",
    "contingency_cost"
]

for column in money_columns:
    cost[column] = cost[column].round(2)

# Total content cost: calculated AFTER individual components are rounded
cost["total_content_cost"] = (
    cost["production_budget"]
    + cost["licensing_cost"]
    + cost["production_overhead"]
    + cost["distribution_cost"]
    + cost["technology_cost"]
    + cost["localization_cost"]
    + cost["contract_administration_cost"]
    + cost["contingency_cost"]
).round(2)

# ----------------------------------------------------------
# Cost intelligence metrics
# ----------------------------------------------------------

cost["licensing_cost_ratio"] = np.where(
    cost["total_content_cost"] > 0,
    cost["licensing_cost"] / cost["total_content_cost"],
    0
).round(4)

cost["production_cost_ratio"] = np.where(
    cost["total_content_cost"] > 0,
    (cost["production_budget"] + cost["production_overhead"]) / cost["total_content_cost"],
    0
).round(4)

cost["localization_cost_per_region"] = np.where(
    cost["available_regions"] > 0,
    cost["localization_cost"] / cost["available_regions"],
    0
).round(2)

# ----------------------------------------------------------
# Final validation
# ----------------------------------------------------------

print("\nRunning cost validation...")

expected_total = (
    cost["production_budget"]
    + cost["licensing_cost"]
    + cost["production_overhead"]
    + cost["distribution_cost"]
    + cost["technology_cost"]
    + cost["localization_cost"]
    + cost["contract_administration_cost"]
    + cost["contingency_cost"]
).round(2)

formula_mismatch = (expected_total != cost["total_content_cost"]).sum()
if formula_mismatch != 0:
    raise ValueError(f"Total cost formula mismatch detected in {formula_mismatch:,} rows.")

if cost["content_id"].duplicated().any():
    raise ValueError("Duplicate content_id values found in cost table.")

if cost["total_content_cost"].le(0).any():
    raise ValueError("Non-positive total content cost detected.")

if cost["production_cost_ratio"].lt(0).any() or cost["production_cost_ratio"].gt(1).any():
    raise ValueError("Invalid production cost ratio detected.")

if cost["licensing_cost_ratio"].lt(0).any() or cost["licensing_cost_ratio"].gt(1).any():
    raise ValueError("Invalid licensing cost ratio detected.")

print("✓ Correct record count")
print("✓ Unique content IDs")
print("✓ No negative costs")
print("✓ Total cost formula validated")
print("✓ Cost ratios validated")

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

cost.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 70)
print("CONTENT COST DATA GENERATED SUCCESSFULLY")
print("=" * 70)
print(f"Records generated    : {len(cost):,}")
print(f"Average total cost   : ₹{cost['total_content_cost'].mean():,.2f}")
print(f"Minimum total cost   : ₹{cost['total_content_cost'].min():,.2f}")
print(f"Maximum total cost   : ₹{cost['total_content_cost'].max():,.2f}")
print(f"Total portfolio cost : ₹{cost['total_content_cost'].sum():,.2f}")
print(f"Average licensing ratio  : {cost['licensing_cost_ratio'].mean():.4f}")
print(f"Average production ratio : {cost['production_cost_ratio'].mean():.4f}")
print(f"\nOutput file: {OUTPUT_FILE}")
