import pandas as pd
from pathlib import Path

# -------------------------------
# Output Folder
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Genre Data
# -------------------------------

genres = [
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sports",
    "Thriller",
    "War",
    "Western"
]

df = pd.DataFrame({
    "genre_id": range(1, len(genres)+1),
    "genre_name": genres
})

output_file = OUTPUT_DIR / "dim_genre.csv"

df.to_csv(output_file, index=False)

print("=" * 50)
print("Genre CSV Generated Successfully!")
print(f"Location: {output_file}")
print("=" * 50)
print(df)