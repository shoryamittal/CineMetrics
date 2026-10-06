import json
import random
from datetime import datetime, timedelta

def get_poster_url():
    ids = [
        "1536440136628-849c177e76a1", "1440404347458-f88c1b50c8b5", "1509198397868-475647b2a1e5",
        "1538986145453-03c85b5d28b1", "1464639351491-d1852ad9d4a5", "1574375927584-1b9b9a8b65e3",
        "1635805737950-d958c3e24e72", "1507003211169-0a1dd7228f2d", "1555396273-367ea4eb4db5",
        "1523413651479-597eb2da6458", "1526374965328-7f61d4dc18c5", "1551854838-212c3e7e4573",
        "1497366216548-37526070297c", "1496104136589-da13a90eb45f", "1612345382609-5b7b8b23e1e5",
        "1494790108377-be9c29b29330", "1486406146926-c627a92ad1ab", "1634838080334-28befa9efe80",
        "1560472354-b33ff0ad5a3", "1612036782180-6f0b6cd846fe"
    ]
    return f"https://images.unsplash.com/photo-{random.choice(ids)}?w=600&auto=format&fit=crop&q=80"

titles = [
    # Required 15
    ("Inception", "Movie", "Sci-Fi", "Warner Bros.", 2010, "English", "Christopher Nolan"),
    ("Interstellar", "Movie", "Sci-Fi", "Paramount Pictures", 2014, "English", "Christopher Nolan"),
    ("Oppenheimer", "Movie", "Biography", "Universal Pictures", 2023, "English", "Christopher Nolan"),
    ("The Dark Knight", "Movie", "Action", "Warner Bros.", 2008, "English", "Christopher Nolan"),
    ("Dune: Part Two", "Movie", "Sci-Fi", "Warner Bros.", 2024, "English", "Denis Villeneuve"),
    ("Stranger Things", "Series", "Sci-Fi", "Netflix", 2016, "English", "The Duffer Brothers"),
    ("RRR", "Movie", "Action", "DVV Entertainment", 2022, "Telugu", "S. S. Rajamouli"),
    ("Succession", "Series", "Drama", "HBO", 2018, "English", "Jesse Armstrong"),
    ("The Bear", "Series", "Comedy", "FX", 2022, "English", "Christopher Storer"),
    ("Breaking Bad", "Series", "Crime", "AMC", 2008, "English", "Vince Gilligan"),
    ("Squid Game", "Series", "Thriller", "Netflix", 2021, "Korean", "Hwang Dong-hyuk"),
    ("Severance", "Series", "Sci-Fi", "Apple TV+", 2022, "English", "Dan Erickson"),
    ("Parasite", "Movie", "Thriller", "CJ Entertainment", 2019, "Korean", "Bong Joon-ho"),
    ("Spirited Away", "Movie", "Animation", "Studio Ghibli", 2001, "Japanese", "Hayao Miyazaki"),
    ("3 Idiots", "Movie", "Comedy", "Vinod Chopra Films", 2009, "Hindi", "Rajkumar Hirani"),
    # Additional 35
    ("Baahubali 2", "Movie", "Action", "Arka Media Works", 2017, "Telugu", "S. S. Rajamouli"),
    ("KGF Chapter 2", "Movie", "Action", "Hombale Films", 2022, "Telugu", "Prashanth Neel"), # Made Kannada, but requested Telugu mapping for simplicity
    ("Dangal", "Movie", "Biography", "Aamir Khan Productions", 2016, "Hindi", "Nitesh Tiwari"),
    ("Tumbbad", "Movie", "Horror", "Sohum Shah Films", 2018, "Hindi", "Rahi Anil Barve"),
    ("Delhi Crime", "Series", "Crime", "Netflix", 2019, "Hindi", "Richie Mehta"),
    ("Mirzapur", "Series", "Crime", "Amazon Prime", 2018, "Hindi", "Karan Anshuman"),
    ("Sacred Games", "Series", "Crime", "Netflix", 2018, "Hindi", "Anurag Kashyap"),
    ("Panchayat", "Series", "Comedy", "TVF", 2020, "Hindi", "Deepak Kumar Mishra"),
    ("Dark", "Series", "Sci-Fi", "Netflix", 2017, "German", "Baran bo Odar"),
    ("Money Heist", "Series", "Crime", "Netflix", 2017, "Spanish", "Álex Pina"),
    ("Lupin", "Series", "Crime", "Netflix", 2021, "French", "George Kay"),
    ("My Name", "Series", "Action", "Netflix", 2021, "Korean", "Kim Jin-min"),
    ("Encanto", "Movie", "Animation", "Walt Disney", 2021, "English", "Jared Bush"),
    ("Spider-Man: Into the Spider-Verse", "Movie", "Animation", "Sony Pictures", 2018, "English", "Bob Persichetti"),
    ("The Lion King", "Movie", "Animation", "Walt Disney", 1994, "English", "Roger Allers"),
    ("The Shawshank Redemption", "Movie", "Drama", "Castle Rock Entertainment", 1994, "English", "Frank Darabont"),
    ("Pulp Fiction", "Movie", "Crime", "Miramax Films", 1994, "English", "Quentin Tarantino"),
    ("The Godfather", "Movie", "Crime", "Paramount Pictures", 1972, "English", "Francis Ford Coppola"),
    ("Wednesday", "Series", "Comedy", "Netflix", 2022, "English", "Tim Burton"),
    ("The Last of Us", "Series", "Drama", "HBO", 2023, "English", "Craig Mazin"),
    ("House of the Dragon", "Series", "Fantasy", "HBO", 2022, "English", "Ryan Condal"),
    ("Andor", "Series", "Sci-Fi", "Lucasfilm", 2022, "English", "Tony Gilroy"),
    ("Only Murders in the Building", "Series", "Comedy", "Hulu", 2021, "English", "Steve Martin"),
    ("Making a Murderer", "Series", "Documentary", "Netflix", 2015, "English", "Laura Ricciardi"),
    ("Our Planet", "Series", "Documentary", "Netflix", 2019, "English", "Alastair Fothergill"),
    ("Seaspiracy", "Movie", "Documentary", "Netflix", 2021, "English", "Ali Tabrizi"),
    ("Avatar: The Way of Water", "Movie", "Sci-Fi", "20th Century Studios", 2022, "English", "James Cameron"),
    ("Top Gun: Maverick", "Movie", "Action", "Paramount Pictures", 2022, "English", "Joseph Kosinski"),
    ("Black Panther", "Movie", "Action", "Marvel Studios", 2018, "English", "Ryan Coogler"),
    ("The Avengers", "Movie", "Action", "Marvel Studios", 2012, "English", "Joss Whedon"),
    ("The Witcher", "Series", "Fantasy", "Netflix", 2019, "English", "Lauren Schmidt Hissrich"),
    ("The Mandalorian", "Series", "Sci-Fi", "Lucasfilm", 2019, "English", "Jon Favreau"),
    ("Chernobyl", "Series", "Drama", "HBO", 2019, "English", "Craig Mazin"),
    ("Fleabag", "Series", "Comedy", "BBC", 2016, "English", "Phoebe Waller-Bridge"),
    ("Black Mirror", "Series", "Sci-Fi", "Netflix", 2011, "English", "Charlie Brooker")
]

colors = ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#222831", "#393e46", "#00adb5", "#eeeeee"]
ratings = ["PG", "PG-13", "R", "TV-14", "TV-MA"]

catalog = []
for i, item in enumerate(titles, 1):
    t_title, t_type, t_genre, t_studio, t_year, t_lang, t_dir = item
    
    prod_budget = random.randint(10, 300) * 1000000
    lic_cost = 0 if random.random() > 0.5 else random.randint(5, 50) * 1000000
    total_cost = prod_budget + lic_cost + (random.randint(5, 20) * 1000000)
    marketing = random.randint(10, 150) * 1000000
    
    # Revenue logic
    if t_title in ["Avatar: The Way of Water", "The Avengers", "Top Gun: Maverick"]:
        total_rev = random.randint(1000, 2500) * 1000000
    elif t_title in ["Breaking Bad", "Stranger Things", "Squid Game", "Succession"]:
        total_rev = random.randint(500, 1500) * 1000000
    else:
        # Some negative
        if random.random() < 0.1:
            total_rev = total_cost * random.uniform(0.5, 0.9)
        else:
            total_rev = total_cost * random.uniform(1.2, 5.0)
            
    ad_rev = total_rev * random.uniform(0.3, 0.4)
    contrib = total_rev - total_cost - marketing
    roi = contrib / total_cost if total_cost > 0 else 0
    
    decisions = ["EXPAND", "RENEW", "MONITOR", "COST_REVIEW", "EXIT_OR_RENEGOTIATE"]
    if roi < 0:
        dec = "EXIT_OR_RENEGOTIATE"
    elif roi > 1.5:
        dec = random.choice(["EXPAND", "RENEW"])
    else:
        dec = random.choice(["MONITOR", "COST_REVIEW"])

    expiry = (datetime.now() + timedelta(days=random.randint(180, 540))).strftime("%Y-%m-%d")
    
    entry = {
        "content_id": i,
        "title": t_title,
        "content_type": t_type,
        "genre": t_genre,
        "studio": t_studio,
        "release_year": t_year,
        "language": t_lang,
        "duration_minutes": random.randint(90, 180) if t_type == "Movie" else random.randint(20, 60),
        "age_rating": random.choice(ratings),
        "imdb_rating": round(random.uniform(7.0, 9.5), 1),
        "production_budget": prod_budget,
        "licensing_cost": lic_cost,
        "total_content_cost": total_cost,
        "marketing_spend": marketing,
        "total_revenue": total_rev,
        "ad_revenue": ad_rev,
        "total_watch_hours": random.randint(10, 500) * 1000000,
        "total_views": random.randint(5, 250) * 1000000,
        "average_completion_rate": round(random.uniform(60, 95), 1),
        "average_rewatch_rate": round(random.uniform(10, 50), 1),
        "contribution_profit": contrib,
        "content_roi": round(roi, 2),
        "decision": dec,
        "director": t_dir,
        "cast": f"Famous Actor {i}A, Famous Actor {i}B, Famous Actor {i}C",
        "synopsis": f"A captivating {t_genre.lower()} story full of twists and turns. Don't miss this acclaimed masterpiece.",
        "tags": [t_genre.lower(), "must-watch", "trending"],
        "poster_url": get_poster_url(),
        "poster_color": random.choice(colors),
        "ai_recommendation": f"Title shows strong performance in {t_lang} markets. Consider targeted campaigns.",
        "churn_defense_score": random.randint(60, 99),
        "post_finale_vulnerability": random.randint(10, 60) if t_type == "Series" else random.randint(5, 20),
        "ad_yield_cpm": random.randint(15, 50),
        "ad_tolerance_minutes": random.randint(10, 45),
        "bridge_titles": [titles[(i+1)%50][0], titles[(i+2)%50][0]],
        "radar": {
            "retention": random.randint(60, 100),
            "capital_efficiency": random.randint(60, 100),
            "churn_defense": random.randint(60, 100),
            "global_appeal": random.randint(60, 100),
            "loyalty": random.randint(60, 100)
        },
        "rights_expiry": expiry,
        "territory_count": random.randint(5, 195),
        "subscriber_uplift": random.randint(10000, 500000),
        "search_rank": random.randint(1, 50),
        "talent_value_index": random.randint(60, 100),
        "piracy_risk_score": random.randint(20, 80),
        "ab_test_ctr_lift": round(random.uniform(0.1, 0.4), 2)
    }
    catalog.append(entry)

import os
path = r"c:\Users\SHORYA MITTAL\OneDrive\Attachments\Project\ENTERPRISE\dashboard\catalog.json"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
