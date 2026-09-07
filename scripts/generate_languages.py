# ===========================================
# CPIP - Language Data Generator
# ===========================================

import pandas as pd
from pathlib import Path

# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Output directory
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Language master data
languages = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de"),
    ("Japanese", "ja"),
    ("Korean", "ko"),
    ("Mandarin Chinese", "zh"),
    ("Portuguese", "pt"),
    ("Arabic", "ar"),
    ("Italian", "it"),
    ("Tamil", "ta"),
    ("Telugu", "te"),
    ("Bengali", "bn"),
    ("Marathi", "mr"),
    ("Turkish", "tr"),
    ("Russian", "ru"),
    ("Dutch", "nl"),
    ("Polish", "pl"),
    ("Indonesian", "id")
]

# Convert to DataFrame
language_df = pd.DataFrame(
    languages,
    columns=["language_name", "language_code"]
)

# Add IDs
language_df.insert(
    0,
    "language_id",
    range(1, len(language_df) + 1)
)

# Save CSV
output_file = OUTPUT_DIR / "dim_language.csv"

language_df.to_csv(output_file, index=False)

print("=" * 50)
print("Language Data Generated Successfully")
print(f"Records generated: {len(language_df)}")
print(f"File: {output_file}")
print("=" * 50)