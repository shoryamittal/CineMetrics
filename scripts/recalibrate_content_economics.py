from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================================
# ECDIP - SAFE CONTENT ECONOMICS RECALIBRATION
# ==========================================================

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

INPUT_FILE = DATA_DIR / "dim_content.csv"
BACKUP_FILE = DATA_DIR / "dim_content_before_economics_fix.csv"
OUTPUT_FILE = DATA_DIR / "dim_content.csv"

print("=" * 70)
print("ECDIP - CONTENT ECONOMICS RECALIBRATION")
print("=" * 70)

# ----------------------------------------------------------
# Load
# ----------------------------------------------------------

content = pd.read_csv(INPUT_FILE)

print(f"Loaded content rows: {len(content):,}")

# ----------------------------------------------------------
# Backup
# ----------------------------------------------------------

content.to_csv(
    BACKUP_FILE,
    index=False
)

print(f"✓ Backup created: {BACKUP_FILE}")

# ----------------------------------------------------------
# Preserve original structure
# ----------------------------------------------------------

original_columns = content.columns.tolist()
original_ids = content["content_id"].copy()

# ----------------------------------------------------------
# New controlled production budget
# ----------------------------------------------------------

budget = np.zeros(len(content))

for i, row in content.iterrows():

    genre = row["genre_id"]
    is_original = bool(row["is_original"])
    content_type = row["content_type"]

    # Base budget by content type
    if content_type == "Movie":
        base_low = 2_000_000
        base_high = 20_000_000
    else:
        base_low = 1_000_000
        base_high = 15_000_000

    # Premium genre multiplier
    if genre in [1, 2, 3, 4]:
        multiplier = np.random.uniform(1.3, 2.2)
    elif genre in [5, 6, 7]:
        multiplier = np.random.uniform(0.8, 1.4)
    else:
        multiplier = np.random.uniform(0.6, 1.2)

    value = (
        np.random.uniform(
            base_low,
            base_high
        )
        * multiplier
    )

    # Originals receive premium production investment
    if is_original:
        value *= np.random.uniform(1.15, 1.40)

    budget[i] = value

# ----------------------------------------------------------
# Safety cap
# ----------------------------------------------------------

budget = np.clip(
    budget,
    500_000,
    50_000_000
)

content["production_budget"] = np.round(
    budget,
    2
)

# ----------------------------------------------------------
# Licensing cost
# ----------------------------------------------------------

licensed = ~content["is_original"].astype(bool)

content["licensing_cost"] = 0.0

content.loc[licensed, "licensing_cost"] = np.round(
    content.loc[licensed, "production_budget"]
    * np.random.uniform(
        0.05,
        0.25,
        licensed.sum()
    ),
    2
)

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

assert len(content) == 50_000

assert content["content_id"].equals(
    original_ids
)

assert content.columns.tolist() == original_columns

assert content["production_budget"].gt(0).all()

assert content["production_budget"].le(
    50_000_000
).all()

assert content["licensing_cost"].ge(0).all()

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

content.to_csv(
    OUTPUT_FILE,
    index=False
)

# ----------------------------------------------------------
# Results
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("RECALIBRATION COMPLETE")
print("=" * 70)

print(
    f"Content rows       : {len(content):,}"
)

print(
    f"Average budget     : ₹{content.production_budget.mean():,.2f}"
)

print(
    f"Minimum budget     : ₹{content.production_budget.min():,.2f}"
)

print(
    f"Maximum budget     : ₹{content.production_budget.max():,.2f}"
)

print(
    f"Total budget       : ₹{content.production_budget.sum():,.2f}"
)

print(
    f"Average licensing  : ₹{content.licensing_cost.mean():,.2f}"
)

print(
    f"Total licensing    : ₹{content.licensing_cost.sum():,.2f}"
)

print("\n✓ IDs preserved")
print("✓ Existing dimensions preserved")
print("✓ Only economic fields changed")
print("✓ Original CSV backed up")