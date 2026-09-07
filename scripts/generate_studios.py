# ===========================================
# CPIP / ECDIP - Studio Data Generator
# ===========================================

import pandas as pd
from pathlib import Path
from faker import Faker
import random
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Initialize Faker
fake = Faker()
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import curated real studios
sys.path.insert(0, str(Path(__file__).resolve().parent))
from real_movie_catalog import REAL_STUDIOS

countries = [
    "United States", "United Kingdom", "Japan", "India",
    "South Korea", "France", "Germany", "Canada", "Australia", "Spain"
]

rows = []

# First populate real curated studios
for studio in REAL_STUDIOS:
    rows.append({
        "studio_id": studio["studio_id"],
        "studio_name": studio["studio_name"],
        "headquarters_country": studio["headquarters_country"],
        "founded_year": studio["founded_year"],
        "website": studio["website"],
        "created_at": pd.Timestamp.now(),
        "updated_at": pd.Timestamp.now()
    })

# Fill remaining up to 300 with realistic studio houses
used_names = {s["studio_name"] for s in rows}
current_id = len(rows) + 1

studio_adjectives = ["Apex", "Summit", "Horizon", "Pinnacle", "Vanguard", "Starlight", "Beacon", "Atlas", "Crest", "Solar", "Silver", "Crown", "Orion", "Pacific", "Atlantic", "Omni", "Nexus", "Zenith", "Mirage", "Prism"]
studio_types = ["Pictures", "Entertainment", "Studios", "Media", "Films", "Productions", "Cinema", "Motion Pictures", "Group", "Interactive"]

for studio_id in range(current_id, 301):
    name = f"{random.choice(studio_adjectives)} {random.choice(studio_types)}"
    if name in used_names:
        name = f"{name} {studio_id}"
    used_names.add(name)

    rows.append({
        "studio_id": studio_id,
        "studio_name": name,
        "headquarters_country": random.choice(countries),
        "founded_year": random.randint(1960, 2023),
        "website": f"https://www.{name.lower().replace(' ', '')}.com",
        "created_at": pd.Timestamp.now(),
        "updated_at": pd.Timestamp.now()
    })

studio_df = pd.DataFrame(rows)

assert studio_df["studio_id"].is_unique
assert studio_df["studio_name"].notna().all()
assert not studio_df["studio_name"].duplicated().any()
assert studio_df["founded_year"].between(1900, 2025).all()

output_file = OUTPUT_DIR / "dim_studio.csv"
studio_df.to_csv(output_file, index=False)

print("=" * 60)
print("STUDIO DATA GENERATED SUCCESSFULLY WITH REAL PRESTIGE STUDIOS")
print("=" * 60)
print(f"Records generated : {len(studio_df)}")
print(f"Output file       : {output_file}")
print("\nPreview Top 10 Studios:")
print(studio_df[["studio_id", "studio_name", "headquarters_country"]].head(10))