# ===========================================
# CPIP - Age Rating Data Generator
# ===========================================

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ratings = [
    ("G", "General audiences", 0),
    ("PG", "Parental guidance suggested", 7),
    ("PG-13", "Parents strongly cautioned", 13),
    ("R", "Restricted", 17),
    ("NC-17", "Adults only", 18),
    ("TV-Y", "Suitable for young children", 0),
    ("TV-PG", "Parental guidance suggested", 7),
    ("TV-MA", "Mature audiences", 17)
]

rating_df = pd.DataFrame(
    ratings,
    columns=[
        "rating_code",
        "description",
        "minimum_age"
    ]
)

rating_df.insert(
    0,
    "age_rating_id",
    range(1, len(rating_df) + 1)
)

output_file = OUTPUT_DIR / "dim_age_rating.csv"

rating_df.to_csv(output_file, index=False)

print("=" * 50)
print("Age Rating Data Generated Successfully")
print(f"Records generated: {len(rating_df)}")
print(f"File: {output_file}")
print("=" * 50)