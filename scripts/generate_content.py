# ==============================================================================
# ECDIP - CONTENT DATA GENERATOR WITH REAL MOVIES & TV SERIES
# ==============================================================================

import pandas as pd
from pathlib import Path
import random
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import real catalog & title banks
sys.path.insert(0, str(Path(__file__).resolve().parent))
from real_movie_catalog import REAL_TITLES, REALISTIC_PREFIXES, REALISTIC_CORES, REALISTIC_SUFFIXES

# Load dimensions
genre_df = pd.read_csv(OUTPUT_DIR / "dim_genre.csv")
language_df = pd.read_csv(OUTPUT_DIR / "dim_language.csv")
rating_df = pd.read_csv(OUTPUT_DIR / "dim_age_rating.csv")
studio_df = pd.read_csv(OUTPUT_DIR / "dim_studio.csv")
region_df = pd.read_csv(OUTPUT_DIR / "dim_region.csv")

genre_name_to_id = dict(zip(genre_df["genre_name"], genre_df["genre_id"]))
studio_name_to_id = dict(zip(studio_df["studio_name"], studio_df["studio_id"]))
valid_languages = set(language_df["language_name"])
valid_ratings = set(rating_df["rating_code"])

# Additional 80+ iconic world titles for the real catalog
ADDITIONAL_REAL_TITLES = [
    # Hollywood Legends & Modern Classics
    {"title": "The Shawshank Redemption", "content_type": "Movie", "genre": "Drama", "studio": "Warner Bros. Pictures", "release_year": 1994, "language": "English", "duration_minutes": 142, "age_rating": "R", "imdb_rating": 9.3, "is_original": False},
    {"title": "The Godfather", "content_type": "Movie", "genre": "Crime", "studio": "Paramount Pictures", "release_year": 1972, "language": "English", "duration_minutes": 175, "age_rating": "R", "imdb_rating": 9.2, "is_original": False},
    {"title": "The Godfather Part II", "content_type": "Movie", "genre": "Crime", "studio": "Paramount Pictures", "release_year": 1974, "language": "English", "duration_minutes": 202, "age_rating": "R", "imdb_rating": 9.0, "is_original": False},
    {"title": "Fight Club", "content_type": "Movie", "genre": "Drama", "studio": "20th Century Studios", "release_year": 1999, "language": "English", "duration_minutes": 139, "age_rating": "R", "imdb_rating": 8.8, "is_original": False},
    {"title": "Forrest Gump", "content_type": "Movie", "genre": "Drama", "studio": "Paramount Pictures", "release_year": 1994, "language": "English", "duration_minutes": 142, "age_rating": "PG-13", "imdb_rating": 8.8, "is_original": False},
    {"title": "The Lord of the Rings: The Return of the King", "content_type": "Movie", "genre": "Fantasy", "studio": "Warner Bros. Pictures", "release_year": 2003, "language": "English", "duration_minutes": 201, "age_rating": "PG-13", "imdb_rating": 9.0, "is_original": False},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "content_type": "Movie", "genre": "Fantasy", "studio": "Warner Bros. Pictures", "release_year": 2001, "language": "English", "duration_minutes": 178, "age_rating": "PG-13", "imdb_rating": 8.9, "is_original": False},
    {"title": "Goodfellas", "content_type": "Movie", "genre": "Biography", "studio": "Warner Bros. Pictures", "release_year": 1990, "language": "English", "duration_minutes": 145, "age_rating": "R", "imdb_rating": 8.7, "is_original": False},
    {"title": "Gladiator", "content_type": "Movie", "genre": "Action", "studio": "Universal Pictures", "release_year": 2000, "language": "English", "duration_minutes": 155, "age_rating": "R", "imdb_rating": 8.5, "is_original": False},
    {"title": "Whiplash", "content_type": "Movie", "genre": "Drama", "studio": "Sony Pictures Entertainment", "release_year": 2014, "language": "English", "duration_minutes": 106, "age_rating": "R", "imdb_rating": 8.5, "is_original": False},
    {"title": "The Prestige", "content_type": "Movie", "genre": "Mystery", "studio": "Warner Bros. Pictures", "release_year": 2006, "language": "English", "duration_minutes": 130, "age_rating": "PG-13", "imdb_rating": 8.5, "is_original": False},
    {"title": "The Departed", "content_type": "Movie", "genre": "Crime", "studio": "Warner Bros. Pictures", "release_year": 2006, "language": "English", "duration_minutes": 151, "age_rating": "R", "imdb_rating": 8.5, "is_original": False},
    {"title": "Joker", "content_type": "Movie", "genre": "Crime", "studio": "Warner Bros. Pictures", "release_year": 2019, "language": "English", "duration_minutes": 122, "age_rating": "R", "imdb_rating": 8.4, "is_original": False},
    {"title": "Blade Runner 2049", "content_type": "Movie", "genre": "Sci-Fi", "studio": "Warner Bros. Pictures", "release_year": 2017, "language": "English", "duration_minutes": 164, "age_rating": "R", "imdb_rating": 8.0, "is_original": False},
    {"title": "Mad Max: Fury Road", "content_type": "Movie", "genre": "Action", "studio": "Warner Bros. Pictures", "release_year": 2015, "language": "English", "duration_minutes": 120, "age_rating": "R", "imdb_rating": 8.1, "is_original": False},
    {"title": "Django Unchained", "content_type": "Movie", "genre": "Drama", "studio": "Sony Pictures Entertainment", "release_year": 2012, "language": "English", "duration_minutes": 165, "age_rating": "R", "imdb_rating": 8.5, "is_original": False},
    {"title": "Inglourious Basterds", "content_type": "Movie", "genre": "Adventure", "studio": "Universal Pictures", "release_year": 2009, "language": "English", "duration_minutes": 153, "age_rating": "R", "imdb_rating": 8.4, "is_original": False},
    {"title": "Coco", "content_type": "Movie", "genre": "Animation", "studio": "Pixar Animation Studios", "release_year": 2017, "language": "English", "duration_minutes": 105, "age_rating": "PG", "imdb_rating": 8.4, "is_original": False},
    {"title": "WALL·E", "content_type": "Movie", "genre": "Animation", "studio": "Pixar Animation Studios", "release_year": 2008, "language": "English", "duration_minutes": 98, "age_rating": "G", "imdb_rating": 8.4, "is_original": False},
    {"title": "Inside Out", "content_type": "Movie", "genre": "Animation", "studio": "Pixar Animation Studios", "release_year": 2015, "language": "English", "duration_minutes": 95, "age_rating": "PG", "imdb_rating": 8.1, "is_original": False},
    {"title": "Inside Out 2", "content_type": "Movie", "genre": "Animation", "studio": "Pixar Animation Studios", "release_year": 2024, "language": "English", "duration_minutes": 96, "age_rating": "PG", "imdb_rating": 7.7, "is_original": False},
    {"title": "Titanic", "content_type": "Movie", "genre": "Romance", "studio": "Paramount Pictures", "release_year": 1997, "language": "English", "duration_minutes": 194, "age_rating": "PG-13", "imdb_rating": 7.9, "is_original": False},
    {"title": "Jurassic Park", "content_type": "Movie", "genre": "Sci-Fi", "studio": "Universal Pictures", "release_year": 1993, "language": "English", "duration_minutes": 127, "age_rating": "PG-13", "imdb_rating": 8.2, "is_original": False},
    {"title": "No Country for Old Men", "content_type": "Movie", "genre": "Crime", "studio": "Paramount Pictures", "release_year": 2007, "language": "English", "duration_minutes": 122, "age_rating": "R", "imdb_rating": 8.2, "is_original": False},
    {"title": "There Will Be Blood", "content_type": "Movie", "genre": "Drama", "studio": "Paramount Pictures", "release_year": 2007, "language": "English", "duration_minutes": 158, "age_rating": "R", "imdb_rating": 8.2, "is_original": False},
    {"title": "The Grand Budapest Hotel", "content_type": "Movie", "genre": "Comedy", "studio": "20th Century Studios", "release_year": 2014, "language": "English", "duration_minutes": 99, "age_rating": "R", "imdb_rating": 8.1, "is_original": False},
    {"title": "La La Land", "content_type": "Movie", "genre": "Comedy", "studio": "Lionsgate Films", "release_year": 2016, "language": "English", "duration_minutes": 128, "age_rating": "PG-13", "imdb_rating": 8.0, "is_original": False},
    {"title": "Gone Girl", "content_type": "Movie", "genre": "Mystery", "studio": "20th Century Studios", "release_year": 2014, "language": "English", "duration_minutes": 149, "age_rating": "R", "imdb_rating": 8.1, "is_original": False},
    {"title": "Zodiac", "content_type": "Movie", "genre": "Crime", "studio": "Paramount Pictures", "release_year": 2007, "language": "English", "duration_minutes": 157, "age_rating": "R", "imdb_rating": 7.7, "is_original": False},
    {"title": "Knives Out", "content_type": "Movie", "genre": "Comedy", "studio": "Lionsgate Films", "release_year": 2019, "language": "English", "duration_minutes": 130, "age_rating": "PG-13", "imdb_rating": 7.9, "is_original": False},
    {"title": "Glass Onion: A Knives Out Mystery", "content_type": "Movie", "genre": "Comedy", "studio": "Netflix Studios", "release_year": 2022, "language": "English", "duration_minutes": 139, "age_rating": "PG-13", "imdb_rating": 7.1, "is_original": True},
    {"title": "The Irishman", "content_type": "Movie", "genre": "Biography", "studio": "Netflix Studios", "release_year": 2019, "language": "English", "duration_minutes": 209, "age_rating": "R", "imdb_rating": 7.8, "is_original": True},
    {"title": "Roma", "content_type": "Movie", "genre": "Drama", "studio": "Netflix Studios", "release_year": 2018, "language": "Spanish", "duration_minutes": 135, "age_rating": "R", "imdb_rating": 7.7, "is_original": True},
    {"title": "Guillermo del Toro's Pinocchio", "content_type": "Movie", "genre": "Animation", "studio": "Netflix Studios", "release_year": 2022, "language": "English", "duration_minutes": 117, "age_rating": "PG", "imdb_rating": 7.6, "is_original": True},
    
    # Anime & International Classics
    {"title": "Princess Mononoke", "content_type": "Movie", "genre": "Animation", "studio": "Studio Ghibli", "release_year": 1997, "language": "Japanese", "duration_minutes": 134, "age_rating": "PG-13", "imdb_rating": 8.4, "is_original": False},
    {"title": "Howl's Moving Castle", "content_type": "Movie", "genre": "Animation", "studio": "Studio Ghibli", "release_year": 2004, "language": "Japanese", "duration_minutes": 119, "age_rating": "PG", "imdb_rating": 8.2, "is_original": False},
    {"title": "Demon Slayer: Mugen Train", "content_type": "Movie", "genre": "Animation", "studio": "Toho Company", "release_year": 2020, "language": "Japanese", "duration_minutes": 117, "age_rating": "R", "imdb_rating": 8.2, "is_original": False},
    {"title": "Jujutsu Kaisen 0", "content_type": "Movie", "genre": "Animation", "studio": "MAPPA Studio", "release_year": 2021, "language": "Japanese", "duration_minutes": 105, "age_rating": "PG-13", "imdb_rating": 7.8, "is_original": False},
    {"title": "Suzume", "content_type": "Movie", "genre": "Animation", "studio": "Toho Company", "release_year": 2022, "language": "Japanese", "duration_minutes": 122, "age_rating": "PG", "imdb_rating": 7.6, "is_original": False},
    {"title": "Pan's Labyrinth", "content_type": "Movie", "genre": "Fantasy", "studio": "Warner Bros. Pictures", "release_year": 2006, "language": "Spanish", "duration_minutes": 118, "age_rating": "R", "imdb_rating": 8.2, "is_original": False},
    {"title": "Amélie", "content_type": "Movie", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2001, "language": "French", "duration_minutes": 122, "age_rating": "R", "imdb_rating": 8.3, "is_original": False},
    {"title": "Oldboy", "content_type": "Movie", "genre": "Action", "studio": "CJ ENM Entertainment", "release_year": 2003, "language": "Korean", "duration_minutes": 120, "age_rating": "R", "imdb_rating": 8.4, "is_original": False},

    # Indian Cinema Superhits & Acclaimed Gems
    {"title": "Gangs of Wasseypur", "content_type": "Movie", "genre": "Crime", "studio": "Universal Pictures", "release_year": 2012, "language": "Hindi", "duration_minutes": 321, "age_rating": "TV-MA", "imdb_rating": 8.2, "is_original": False},
    {"title": "Sholay", "content_type": "Movie", "genre": "Action", "studio": "Universal Pictures", "release_year": 1975, "language": "Hindi", "duration_minutes": 204, "age_rating": "PG", "imdb_rating": 8.1, "is_original": False},
    {"title": "Lagaan: Once Upon a Time in India", "content_type": "Movie", "genre": "Drama", "studio": "Universal Pictures", "release_year": 2001, "language": "Hindi", "duration_minutes": 224, "age_rating": "PG", "imdb_rating": 8.1, "is_original": False},
    {"title": "Swades", "content_type": "Movie", "genre": "Drama", "studio": "Universal Pictures", "release_year": 2004, "language": "Hindi", "duration_minutes": 210, "age_rating": "PG", "imdb_rating": 8.2, "is_original": False},
    {"title": "Taare Zameen Par", "content_type": "Movie", "genre": "Drama", "studio": "Universal Pictures", "release_year": 2007, "language": "Hindi", "duration_minutes": 165, "age_rating": "PG", "imdb_rating": 8.3, "is_original": False},
    {"title": "Queen", "content_type": "Movie", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2013, "language": "Hindi", "duration_minutes": 144, "age_rating": "PG-13", "imdb_rating": 8.1, "is_original": False},
    {"title": "Barfi!", "content_type": "Movie", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2012, "language": "Hindi", "duration_minutes": 151, "age_rating": "PG", "imdb_rating": 8.1, "is_original": False},
    {"title": "PK", "content_type": "Movie", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2014, "language": "Hindi", "duration_minutes": 153, "age_rating": "PG-13", "imdb_rating": 8.1, "is_original": False},
    {"title": "Stree 2", "content_type": "Movie", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2024, "language": "Hindi", "duration_minutes": 147, "age_rating": "PG-13", "imdb_rating": 7.5, "is_original": False},
    {"title": "Kantara", "content_type": "Movie", "genre": "Action", "studio": "Hombale Films", "release_year": 2022, "language": "Hindi", "duration_minutes": 148, "age_rating": "PG-13", "imdb_rating": 8.2, "is_original": False},
    {"title": "Vikram", "content_type": "Movie", "genre": "Action", "studio": "Universal Pictures", "release_year": 2022, "language": "Hindi", "duration_minutes": 175, "age_rating": "PG-13", "imdb_rating": 8.3, "is_original": False},
    {"title": "Ponniyin Selvan: Part I", "content_type": "Movie", "genre": "Action", "studio": "Universal Pictures", "release_year": 2022, "language": "Hindi", "duration_minutes": 167, "age_rating": "PG-13", "imdb_rating": 7.6, "is_original": False},
    {"title": "Drishyam", "content_type": "Movie", "genre": "Crime", "studio": "Universal Pictures", "release_year": 2015, "language": "Hindi", "duration_minutes": 163, "age_rating": "PG-13", "imdb_rating": 8.2, "is_original": False},
    {"title": "Drishyam 2", "content_type": "Movie", "genre": "Crime", "studio": "Universal Pictures", "release_year": 2022, "language": "Hindi", "duration_minutes": 140, "age_rating": "PG-13", "imdb_rating": 8.2, "is_original": False},
    {"title": "Article 15", "content_type": "Movie", "genre": "Crime", "studio": "Universal Pictures", "release_year": 2019, "language": "Hindi", "duration_minutes": 130, "age_rating": "TV-MA", "imdb_rating": 8.1, "is_original": False},

    # Premium TV Series
    {"title": "Game of Thrones", "content_type": "Series", "genre": "Fantasy", "studio": "HBO Entertainment", "release_year": 2011, "language": "English", "duration_minutes": 57, "age_rating": "TV-MA", "imdb_rating": 9.2, "is_original": False},
    {"title": "Better Call Saul", "content_type": "Series", "genre": "Crime", "studio": "Sony Pictures Entertainment", "release_year": 2015, "language": "English", "duration_minutes": 46, "age_rating": "TV-MA", "imdb_rating": 9.0, "is_original": False},
    {"title": "Fargo", "content_type": "Series", "genre": "Crime", "studio": "MGM Studios", "release_year": 2014, "language": "English", "duration_minutes": 53, "age_rating": "TV-MA", "imdb_rating": 8.9, "is_original": False},
    {"title": "Narcos", "content_type": "Series", "genre": "Biography", "studio": "Netflix Studios", "release_year": 2015, "language": "Spanish", "duration_minutes": 49, "age_rating": "TV-MA", "imdb_rating": 8.8, "is_original": True},
    {"title": "Mindhunter", "content_type": "Series", "genre": "Crime", "studio": "Netflix Studios", "release_year": 2017, "language": "English", "duration_minutes": 50, "age_rating": "TV-MA", "imdb_rating": 8.6, "is_original": True},
    {"title": "Sherlock", "content_type": "Series", "genre": "Crime", "studio": "BBC Film", "release_year": 2010, "language": "English", "duration_minutes": 88, "age_rating": "TV-14", "imdb_rating": 9.1, "is_original": False},
    {"title": "Fleabag", "content_type": "Series", "genre": "Comedy", "studio": "BBC Film", "release_year": 2016, "language": "English", "duration_minutes": 27, "age_rating": "TV-MA", "imdb_rating": 8.7, "is_original": False},
    {"title": "Beef", "content_type": "Series", "genre": "Comedy", "studio": "A24", "release_year": 2023, "language": "English", "duration_minutes": 33, "age_rating": "TV-MA", "imdb_rating": 8.0, "is_original": True},
    {"title": "The White Lotus", "content_type": "Series", "genre": "Comedy", "studio": "HBO Entertainment", "release_year": 2021, "language": "English", "duration_minutes": 58, "age_rating": "TV-MA", "imdb_rating": 8.0, "is_original": True},
    {"title": "Euphoria", "content_type": "Series", "genre": "Drama", "studio": "HBO Entertainment", "release_year": 2019, "language": "English", "duration_minutes": 55, "age_rating": "TV-MA", "imdb_rating": 8.3, "is_original": True},
    {"title": "True Detective", "content_type": "Series", "genre": "Crime", "studio": "HBO Entertainment", "release_year": 2014, "language": "English", "duration_minutes": 55, "age_rating": "TV-MA", "imdb_rating": 8.9, "is_original": True},
    {"title": "Yellowstone", "content_type": "Series", "genre": "Drama", "studio": "Paramount Pictures", "release_year": 2018, "language": "English", "duration_minutes": 60, "age_rating": "TV-MA", "imdb_rating": 8.7, "is_original": False},
    {"title": "Ozark", "content_type": "Series", "genre": "Crime", "studio": "Netflix Studios", "release_year": 2017, "language": "English", "duration_minutes": 60, "age_rating": "TV-MA", "imdb_rating": 8.5, "is_original": True},
    {"title": "Alice in Borderland", "content_type": "Series", "genre": "Sci-Fi", "studio": "Netflix Studios", "release_year": 2020, "language": "Japanese", "duration_minutes": 50, "age_rating": "TV-MA", "imdb_rating": 7.7, "is_original": True},
    {"title": "Lupin", "content_type": "Series", "genre": "Action", "studio": "Netflix Studios", "release_year": 2021, "language": "French", "duration_minutes": 45, "age_rating": "TV-MA", "imdb_rating": 7.5, "is_original": True},
    {"title": "Heartstopper", "content_type": "Series", "genre": "Drama", "studio": "Netflix Studios", "release_year": 2022, "language": "English", "duration_minutes": 30, "age_rating": "TV-14", "imdb_rating": 8.6, "is_original": True},
    {"title": "Wednesday", "content_type": "Series", "genre": "Comedy", "studio": "Netflix Studios", "release_year": 2022, "language": "English", "duration_minutes": 45, "age_rating": "TV-14", "imdb_rating": 8.1, "is_original": True},
    {"title": "Bridgerton", "content_type": "Series", "genre": "Romance", "studio": "Netflix Studios", "release_year": 2020, "language": "English", "duration_minutes": 60, "age_rating": "TV-MA", "imdb_rating": 7.4, "is_original": True},
    {"title": "The Queen's Gambit", "content_type": "Series", "genre": "Drama", "studio": "Netflix Studios", "release_year": 2020, "language": "English", "duration_minutes": 55, "age_rating": "TV-MA", "imdb_rating": 8.5, "is_original": True},
    {"title": "Sacred Games", "content_type": "Series", "genre": "Crime", "studio": "Netflix Studios", "release_year": 2018, "language": "Hindi", "duration_minutes": 50, "age_rating": "TV-MA", "imdb_rating": 8.5, "is_original": True},
    {"title": "Mirzapur", "content_type": "Series", "genre": "Action", "studio": "Universal Pictures", "release_year": 2018, "language": "Hindi", "duration_minutes": 55, "age_rating": "TV-MA", "imdb_rating": 8.5, "is_original": False},
    {"title": "Panchayat", "content_type": "Series", "genre": "Comedy", "studio": "Universal Pictures", "release_year": 2020, "language": "Hindi", "duration_minutes": 35, "age_rating": "PG", "imdb_rating": 8.9, "is_original": False},
    {"title": "The Family Man", "content_type": "Series", "genre": "Action", "studio": "Universal Pictures", "release_year": 2019, "language": "Hindi", "duration_minutes": 45, "age_rating": "TV-MA", "imdb_rating": 8.7, "is_original": False}
]

# Combine all curated real titles
all_curated_titles = list(REAL_TITLES) + ADDITIONAL_REAL_TITLES

TOTAL_CONTENT = 50000
rows = []
used_titles = set()

# Economics calibration:
# In streaming warehouse accounting, content cost amortizes across the catalog.
# To achieve healthy realistic platform economics (~₹2.5B revenue vs ~₹1.8B total cost):
# Average production budget per title ~₹20,000 - ₹35,000 for standard catalog,
# with blockbusters and marquee originals having premium investments (₹150K - ₹500K),
# and licensing costs proportional (5% - 25% of budget for licensed content, 0 for originals).

def generate_cinematic_title(index):
    pref = random.choice(REALISTIC_PREFIXES)
    core = random.choice(REALISTIC_CORES)
    style = random.randint(1, 4)
    if style == 1:
        t = f"{pref} {core}"
    elif style == 2:
        suff = random.choice(REALISTIC_SUFFIXES)
        t = f"{core}: {suff}"
    elif style == 3:
        suff = random.choice(REALISTIC_SUFFIXES)
        t = f"{pref} {core} - {suff}"
    else:
        part = random.randint(2, 5)
        t = f"{core} {part}"
    
    if t in used_titles:
        t = f"{t} ({index})"
    used_titles.add(t)
    return t

print("Generating content with real movies and calibrated economics...")

for content_id in range(1, TOTAL_CONTENT + 1):
    if content_id <= len(all_curated_titles):
        # Real curated movie or series
        curated = all_curated_titles[content_id - 1]
        title = curated["title"]
        used_titles.add(title)
        content_type = curated["content_type"]
        genre_name = curated["genre"]
        genre_id = genre_name_to_id.get(genre_name, 1)
        
        studio_name = curated.get("studio", "Warner Bros. Pictures")
        studio_id = studio_name_to_id.get(studio_name, 1)
        
        release_year = curated.get("release_year", random.randint(2012, 2024))
        language = curated.get("language", "English")
        if language not in valid_languages:
            language = "English"
        duration_minutes = curated.get("duration_minutes", 120 if content_type == "Movie" else 50)
        age_rating = curated.get("age_rating", "PG-13")
        if age_rating not in valid_ratings:
            age_rating = "PG-13"
        imdb_rating = curated.get("imdb_rating", 8.2)
        is_original = curated.get("is_original", False)
        
        # Calibrated platform production budget
        # Tier 1 Blockbusters / Flagships: ₹120K - ₹450K
        production_budget = round(random.uniform(120000, 450000), 2)
        if is_original:
            licensing_cost = 0.0
            production_budget *= 1.25
        else:
            licensing_cost = round(production_budget * random.uniform(0.08, 0.22), 2)

        available_regions = random.randint(12, len(region_df)) # Global availability for hits

    else:
        # Realistic catalog title
        title = generate_cinematic_title(content_id)
        content_type = "Movie" if random.random() < 0.65 else "Series"
        genre = genre_df.sample(1).iloc[0]
        genre_id = int(genre["genre_id"])
        genre_name = genre["genre_name"]
        
        studio = studio_df.sample(1).iloc[0]
        studio_id = int(studio["studio_id"])
        
        # Weighted languages towards English and Hindi, with Asian & European variety
        lang_choice = random.choices(
            ["English", "Hindi", "Spanish", "Japanese", "Korean", "French", "German"],
            weights=[45, 25, 10, 8, 5, 4, 3],
            k=1
        )[0]
        language = lang_choice if lang_choice in valid_languages else "English"
        
        release_year = random.randint(2010, 2025)
        duration_minutes = random.randint(75, 175) if content_type == "Movie" else random.randint(25, 65)
        
        rating = rating_df.sample(1).iloc[0]
        age_rating = rating["rating_code"]
        
        # Natural IMDb rating bell-curve centered around 6.7
        imdb_rating = round(min(9.4, max(4.2, random.gauss(6.7, 0.95))), 1)
        
        is_original = random.random() < 0.30
        
        # Base budget calibrated to streaming warehouse scale (mean ~₹25,000)
        base_budget = random.uniform(12000, 38000)
        if genre_name in ["Action", "Sci-Fi", "Fantasy"]:
            base_budget *= random.uniform(1.2, 1.8)
        elif genre_name in ["Documentary", "Comedy"]:
            base_budget *= random.uniform(0.7, 1.1)

        production_budget = round(base_budget, 2)
        
        if is_original:
            licensing_cost = 0.0
            production_budget = round(production_budget * random.uniform(1.15, 1.35), 2)
        else:
            licensing_cost = round(production_budget * random.uniform(0.05, 0.25), 2)
            
        available_regions = random.randint(3, len(region_df))

    rows.append({
        "content_id": content_id,
        "title": title,
        "content_type": content_type,
        "genre_id": genre_id,
        "studio_id": studio_id,
        "release_year": release_year,
        "language": language,
        "duration_minutes": duration_minutes,
        "age_rating": age_rating,
        "imdb_rating": imdb_rating,
        "production_budget": production_budget,
        "licensing_cost": licensing_cost,
        "available_regions": available_regions,
        "is_original": is_original,
        "created_at": pd.Timestamp.now(),
        "updated_at": pd.Timestamp.now()
    })

content_df = pd.DataFrame(rows)

# Validations
assert len(content_df) == TOTAL_CONTENT
assert content_df["content_id"].is_unique
assert content_df["title"].notna().all()
assert not content_df["title"].duplicated().any()
assert content_df["genre_id"].isin(genre_df["genre_id"]).all()
assert content_df["studio_id"].isin(studio_df["studio_id"]).all()
assert content_df["language"].isin(language_df["language_name"]).all()
assert content_df["age_rating"].isin(rating_df["rating_code"]).all()
assert content_df["imdb_rating"].between(0, 10).all()
assert content_df["production_budget"].gt(0).all()
assert content_df["licensing_cost"].ge(0).all()
assert content_df["available_regions"].between(1, len(region_df)).all()

output_file = OUTPUT_DIR / "dim_content.csv"
content_df.to_csv(output_file, index=False)

print("=" * 65)
print("CONTENT DATA GENERATED SUCCESSFULLY WITH REAL MOVIES")
print("=" * 65)
print(f"Records generated    : {len(content_df):,}")
print(f"Real curated titles  : {len(all_curated_titles)}")
print(f"Total budget         : ₹{content_df.production_budget.sum():,.2f}")
print(f"Average budget/asset : ₹{content_df.production_budget.mean():,.2f}")
print(f"Output file          : {output_file}")
print("\nPreview Top 15 Real Titles:")
print(content_df[["content_id", "title", "content_type", "release_year", "language", "imdb_rating"]].head(15))