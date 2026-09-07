import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

platforms = [
    ("Netflix", "United States", 2007),
    ("Prime Video", "United States", 2006),
    ("Disney+", "United States", 2019),
    ("JioHotstar", "India", 2019),
    ("Apple TV+", "United States", 2019),
    ("Hulu", "United States", 2007),
    ("Max", "United States", 2023),
    ("Paramount+", "United States", 2021),
    ("Peacock", "United States", 2020),
    ("SonyLIV", "India", 2013)
]

df = pd.DataFrame(
    platforms,
    columns=[
        "platform_name",
        "headquarters",
        "launch_year"
    ]
)

df.insert(0, "platform_id", range(1, len(df) + 1))

df["created_at"] = pd.Timestamp.now()
df["updated_at"] = pd.Timestamp.now()

df.to_csv(OUTPUT_DIR / "dim_platform.csv", index=False)

print(f"Created {len(df)} platform records.")