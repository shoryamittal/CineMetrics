# ===========================================
# CPIP - Contract Data Generator
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

contract_types = [
    "Exclusive",
    "Non-Exclusive",
    "Original Production",
    "Distribution"
]

licensing_models = [
    "Fixed Fee",
    "Revenue Share",
    "Hybrid",
    "Minimum Guarantee"
]

# -------------------------------------------
# Generate contracts
# -------------------------------------------

rows = []

for contract_id in range(1, 5001):

    # Generate valid start date
    contract_start = fake.date_between(
        start_date=pd.Timestamp("2020-01-01").date(),
        end_date=pd.Timestamp("2028-01-01").date()
    )

    # Contract duration: approximately 6 months to 5 years
    duration_days = random.randint(
        180,
        1825
    )

    contract_end = (
        pd.Timestamp(contract_start)
        + pd.Timedelta(days=duration_days)
    ).date()

    # Licensing cost
    licensing_cost = random.uniform(
        50000,
        10000000
    )

    # Renewal cost is related to original cost
    renewal_cost = (
        licensing_cost
        * random.uniform(0.80, 1.50)
    )

    rows.append({

        "contract_id":
            contract_id,

        "contract_number":
            f"CTR-{contract_id:06d}",

        "contract_type":
            random.choice(contract_types),

        "contract_start":
            contract_start,

        "contract_end":
            contract_end,

        "licensing_model":
            random.choice(licensing_models),

        "licensing_cost":
            round(licensing_cost, 2),

        "renewal_cost":
            round(renewal_cost, 2),

        "auto_renew":
            random.choice([True, False]),

        "created_at":
            pd.Timestamp.now(),

        "updated_at":
            pd.Timestamp.now()
    })

# -------------------------------------------
# DataFrame
# -------------------------------------------

contract_df = pd.DataFrame(rows)

# -------------------------------------------
# Data validation
# -------------------------------------------

assert contract_df["contract_id"].is_unique

assert contract_df["contract_number"].is_unique

assert contract_df["contract_start"].notna().all()

assert contract_df["contract_end"].notna().all()

assert (
    pd.to_datetime(contract_df["contract_end"])
    >
    pd.to_datetime(contract_df["contract_start"])
).all()

assert contract_df["licensing_cost"].gt(0).all()

assert contract_df["renewal_cost"].gt(0).all()

# -------------------------------------------
# Save
# -------------------------------------------

output_file = OUTPUT_DIR / "dim_contract.csv"

contract_df.to_csv(
    output_file,
    index=False
)

# -------------------------------------------
# Results
# -------------------------------------------

print("=" * 60)
print("CONTRACT DATA GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Records generated : {len(contract_df)}")
print(f"Output file       : {output_file}")

print("\nPreview:")
print(contract_df.head())

print("\nValidation:")
print("✓ Contract IDs are unique")
print("✓ Contract numbers are unique")
print("✓ Contract dates are valid")
print("✓ Licensing costs are positive")
print("✓ Renewal costs are positive")
