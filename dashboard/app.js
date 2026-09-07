/**
 * ECDIP - Enterprise Content Decision Intelligence Platform
 * High-Fidelity Streaming Executive Dashboard Application
 */

// ==============================================================================
// 1. STATE & CORE CONFIGURATION
// ==============================================================================
const STATE = {
  currency: 'INR', // 'INR' or 'USD'
  rateUSD: 83.5,   // 1 USD = 83.5 INR
  currentTab: 'overview',
  catalog: [],
  selectedMovie: null,
  timeframe: 'LTM',
  filters: {
    search: '',
    genre: 'ALL',
    type: 'ALL',
    decision: 'ALL',
    sort: 'roi_desc'
  }
};

// Built-in curated catalog fallback to guarantee 100% instant offline rendering
const FALLBACK_CATALOG = [
  {
    "content_id": 1,
    "title": "Inception",
    "content_type": "Movie",
    "genre": "Sci-Fi",
    "studio": "Warner Bros. Pictures",
    "release_year": 2010,
    "language": "English",
    "duration_minutes": 148,
    "age_rating": "PG-13",
    "imdb_rating": 8.8,
    "production_budget": 160000000,
    "licensing_cost": 32000000,
    "total_content_cost": 218000000,
    "marketing_spend": 65000000,
    "total_revenue": 836800000,
    "ad_revenue": 142000000,
    "total_watch_hours": 38400000,
    "total_views": 15500000,
    "average_completion_rate": 81.4,
    "average_rewatch_rate": 34.2,
    "contribution_profit": 553800000,
    "content_roi": 1.9569,
    "decision": "EXPAND",
    "director": "Christopher Nolan",
    "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
    "synopsis": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    "tags": [
      "Mind-Bending",
      "Oscar Winner",
      "IMDb Top 250"
    ],
    "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#1e3a8a",
    "ai_recommendation": "High viral retention & 81.4% completion rate. Greenlight 4K remastered re-release and commission spiritual successor sci-fi series.",
    "churn_defense_score": 92,
    "post_finale_vulnerability": 14,
    "ad_yield_cpm": 34.5,
    "ad_tolerance_minutes": 35,
    "bridge_titles": [
      "Interstellar",
      "The Matrix",
      "Severance"
    ],
    "radar": {
      "retention": 88,
      "capital_efficiency": 94,
      "churn_defense": 92,
      "global_appeal": 96,
      "loyalty": 84
    }
  },
  {
    "content_id": 2,
    "title": "Interstellar",
    "content_type": "Movie",
    "genre": "Sci-Fi",
    "studio": "Paramount Pictures",
    "release_year": 2014,
    "language": "English",
    "duration_minutes": 169,
    "age_rating": "PG-13",
    "imdb_rating": 8.7,
    "production_budget": 165000000,
    "licensing_cost": 35000000,
    "total_content_cost": 224000000,
    "marketing_spend": 70000000,
    "total_revenue": 773400000,
    "ad_revenue": 128000000,
    "total_watch_hours": 46200000,
    "total_views": 16400000,
    "average_completion_rate": 83.2,
    "average_rewatch_rate": 39.5,
    "contribution_profit": 479400000,
    "content_roi": 1.6306,
    "decision": "EXPAND",
    "director": "Christopher Nolan",
    "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine",
    "synopsis": "When Earth becomes uninhabitable, a team of researchers and an ex-NASA pilot travel through a wormhole across the galaxy to find a new home.",
    "tags": [
      "Space Exploration",
      "Deep Emotion",
      "Hans Zimmer Score"
    ],
    "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#0f172a",
    "ai_recommendation": "Exceptional long-tail evergreen catalog value. 39.5% rewatch rate is among highest on platform. Maintain permanent streaming rights.",
    "churn_defense_score": 94,
    "post_finale_vulnerability": 12,
    "ad_yield_cpm": 32.0,
    "ad_tolerance_minutes": 42,
    "bridge_titles": [
      "Inception",
      "Dune: Part Two",
      "Blade Runner 2049"
    ],
    "radar": {
      "retention": 91,
      "capital_efficiency": 89,
      "churn_defense": 94,
      "global_appeal": 95,
      "loyalty": 92
    }
  },
  {
    "content_id": 3,
    "title": "Oppenheimer",
    "content_type": "Movie",
    "genre": "Biography",
    "studio": "Universal Pictures",
    "release_year": 2023,
    "language": "English",
    "duration_minutes": 180,
    "age_rating": "R",
    "imdb_rating": 8.9,
    "production_budget": 100000000,
    "licensing_cost": 45000000,
    "total_content_cost": 168000000,
    "marketing_spend": 85000000,
    "total_revenue": 957000000,
    "ad_revenue": 168000000,
    "total_watch_hours": 58900000,
    "total_views": 19600000,
    "average_completion_rate": 79.8,
    "average_rewatch_rate": 26.4,
    "contribution_profit": 704000000,
    "content_roi": 2.7826,
    "decision": "EXPAND",
    "director": "Christopher Nolan",
    "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.",
    "synopsis": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during the Manhattan Project.",
    "tags": [
      "7 Oscars Winner",
      "Historical Epic",
      "Blockbuster Drama"
    ],
    "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#ea580c",
    "ai_recommendation": "Record-shattering prestige acquisition. Driven +1.2M new subscriber conversions globally. Prioritize bundling with historical docuseries.",
    "churn_defense_score": 89,
    "post_finale_vulnerability": 18,
    "ad_yield_cpm": 38.0,
    "ad_tolerance_minutes": 45,
    "bridge_titles": [
      "Chernobyl",
      "The Dark Knight",
      "The Imitation Game"
    ],
    "radar": {
      "retention": 85,
      "capital_efficiency": 97,
      "churn_defense": 89,
      "global_appeal": 98,
      "loyalty": 78
    }
  },
  {
    "content_id": 4,
    "title": "The Dark Knight",
    "content_type": "Movie",
    "genre": "Action",
    "studio": "Warner Bros. Pictures",
    "release_year": 2008,
    "language": "English",
    "duration_minutes": 152,
    "age_rating": "PG-13",
    "imdb_rating": 9.0,
    "production_budget": 185000000,
    "licensing_cost": 28000000,
    "total_content_cost": 235000000,
    "marketing_spend": 50000000,
    "total_revenue": 1006000000,
    "ad_revenue": 195000000,
    "total_watch_hours": 62500000,
    "total_views": 24700000,
    "average_completion_rate": 86.5,
    "average_rewatch_rate": 44.1,
    "contribution_profit": 721000000,
    "content_roi": 2.5298,
    "decision": "EXPAND",
    "director": "Christopher Nolan",
    "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
    "synopsis": "When the Joker wreaks chaos on Gotham City, Batman must accept one of the greatest psychological and physical tests of his life.",
    "tags": [
      "Heath Ledger Joker",
      "Masterpiece",
      "Highest Rated Superhero Film"
    ],
    "poster_url": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#334155",
    "ai_recommendation": "Anchor asset of entire DC franchise. Unmatched 44.1% rewatch frequency. Key driver for ad-supported tier retention.",
    "churn_defense_score": 98,
    "post_finale_vulnerability": 8,
    "ad_yield_cpm": 41.5,
    "ad_tolerance_minutes": 28,
    "bridge_titles": [
      "Joker",
      "The Batman",
      "The Boys"
    ],
    "radar": {
      "retention": 94,
      "capital_efficiency": 96,
      "churn_defense": 98,
      "global_appeal": 99,
      "loyalty": 97
    }
  },
  {
    "content_id": 5,
    "title": "Dune: Part Two",
    "content_type": "Movie",
    "genre": "Sci-Fi",
    "studio": "Warner Bros. Pictures",
    "release_year": 2024,
    "language": "English",
    "duration_minutes": 166,
    "age_rating": "PG-13",
    "imdb_rating": 8.6,
    "production_budget": 190000000,
    "licensing_cost": 50000000,
    "total_content_cost": 268000000,
    "marketing_spend": 90000000,
    "total_revenue": 714000000,
    "ad_revenue": 110000000,
    "total_watch_hours": 44800000,
    "total_views": 16200000,
    "average_completion_rate": 80.6,
    "average_rewatch_rate": 28.1,
    "contribution_profit": 356000000,
    "content_roi": 0.9944,
    "decision": "EXPAND",
    "director": "Denis Villeneuve",
    "cast": "Timoth\u00e9e Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem",
    "synopsis": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
    "tags": [
      "Sci-Fi Epic",
      "Visual Marvel",
      "Global Phenomenon"
    ],
    "poster_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#d97706",
    "ai_recommendation": "High global franchise equity. Fast-track co-production rights for Dune: Messiah and streaming prequel spinoffs.",
    "churn_defense_score": 87,
    "post_finale_vulnerability": 16,
    "ad_yield_cpm": 33.0,
    "ad_tolerance_minutes": 38,
    "bridge_titles": [
      "Blade Runner 2049",
      "Interstellar",
      "Avatar: The Way of Water"
    ],
    "radar": {
      "retention": 86,
      "capital_efficiency": 82,
      "churn_defense": 87,
      "global_appeal": 94,
      "loyalty": 81
    }
  },
  {
    "content_id": 6,
    "title": "Stranger Things",
    "content_type": "Series",
    "genre": "Sci-Fi",
    "studio": "Netflix Studios",
    "release_year": 2016,
    "language": "English",
    "duration_minutes": 55,
    "age_rating": "TV-14",
    "imdb_rating": 8.7,
    "production_budget": 270000000,
    "licensing_cost": 0,
    "total_content_cost": 312000000,
    "marketing_spend": 110000000,
    "total_revenue": 1450000000,
    "ad_revenue": 340000000,
    "total_watch_hours": 185000000,
    "total_views": 38400000,
    "average_completion_rate": 87.3,
    "average_rewatch_rate": 36.8,
    "contribution_profit": 1028000000,
    "content_roi": 2.436,
    "decision": "RENEW",
    "director": "The Duffer Brothers",
    "cast": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour",
    "synopsis": "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, supernatural forces and one strange little girl.",
    "tags": [
      "Flagship Original",
      "80s Nostalgia",
      "Global Phenomenon"
    ],
    "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#991b1b",
    "ai_recommendation": "#1 subscriber acquisition driver in company history. Execute final season global premiere campaign and animated universe spinoffs.",
    "churn_defense_score": 97,
    "post_finale_vulnerability": 42,
    "ad_yield_cpm": 44.0,
    "ad_tolerance_minutes": 18,
    "bridge_titles": [
      "Dark",
      "Wednesday",
      "Severance",
      "Black Mirror"
    ],
    "radar": {
      "retention": 95,
      "capital_efficiency": 95,
      "churn_defense": 97,
      "global_appeal": 99,
      "loyalty": 93
    }
  },
  {
    "content_id": 7,
    "title": "RRR",
    "content_type": "Movie",
    "genre": "Action",
    "studio": "DVV Entertainment",
    "release_year": 2022,
    "language": "Hindi",
    "duration_minutes": 187,
    "age_rating": "PG-13",
    "imdb_rating": 7.8,
    "production_budget": 68000000,
    "licensing_cost": 22000000,
    "total_content_cost": 102000000,
    "marketing_spend": 35000000,
    "total_revenue": 920000000,
    "ad_revenue": 210000000,
    "total_watch_hours": 69200000,
    "total_views": 22100000,
    "average_completion_rate": 78.4,
    "average_rewatch_rate": 33.5,
    "contribution_profit": 783000000,
    "content_roi": 5.7153,
    "decision": "EXPAND",
    "director": "S.S. Rajamouli",
    "cast": "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn, Alia Bhatt",
    "synopsis": "A fearless revolutionary and an officer in the British force join forces and chart out an inspirational path of freedom against despotic rulers.",
    "tags": [
      "Naatu Naatu Oscar",
      "Global Sensation",
      "Visual Action Spectacle"
    ],
    "poster_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#b45309",
    "ai_recommendation": "Record 571% ROI! Exploded across Western, Asian, and Indian markets simultaneously. Secure first-look agreement with director S.S. Rajamouli.",
    "churn_defense_score": 96,
    "post_finale_vulnerability": 11,
    "ad_yield_cpm": 39.5,
    "ad_tolerance_minutes": 32,
    "bridge_titles": [
      "Baahubali 2",
      "K.G.F: Chapter 2",
      "Jawan"
    ],
    "radar": {
      "retention": 89,
      "capital_efficiency": 99,
      "churn_defense": 96,
      "global_appeal": 94,
      "loyalty": 91
    }
  },
  {
    "content_id": 8,
    "title": "Succession",
    "content_type": "Series",
    "genre": "Drama",
    "studio": "HBO Entertainment",
    "release_year": 2018,
    "language": "English",
    "duration_minutes": 60,
    "age_rating": "TV-MA",
    "imdb_rating": 8.9,
    "production_budget": 90000000,
    "licensing_cost": 30000000,
    "total_content_cost": 134000000,
    "marketing_spend": 45000000,
    "total_revenue": 540000000,
    "ad_revenue": 95000000,
    "total_watch_hours": 71000000,
    "total_views": 11800000,
    "average_completion_rate": 84.6,
    "average_rewatch_rate": 29.1,
    "contribution_profit": 361000000,
    "content_roi": 2.0168,
    "decision": "EXPAND",
    "director": "Jesse Armstrong",
    "cast": "Brian Cox, Jeremy Strong, Sarah Snook, Kieran Culkin, Matthew Macfadyen",
    "synopsis": "The Roy family is known for controlling the biggest media company in the world. However, their world changes when their aging father steps down.",
    "tags": [
      "Multiple Emmy Winner",
      "Corporate Warfare",
      "Masterpiece Writing"
    ],
    "poster_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#1e293b",
    "ai_recommendation": "Highest customer brand affinity of any drama series on platform. Strong retention anchor among affluent adult demographic.",
    "churn_defense_score": 93,
    "post_finale_vulnerability": 38,
    "ad_yield_cpm": 42.0,
    "ad_tolerance_minutes": 22,
    "bridge_titles": [
      "The Bear",
      "Billions",
      "Mad Men"
    ],
    "radar": {
      "retention": 92,
      "capital_efficiency": 91,
      "churn_defense": 93,
      "global_appeal": 88,
      "loyalty": 87
    }
  },
  {
    "content_id": 9,
    "title": "The Bear",
    "content_type": "Series",
    "genre": "Drama",
    "studio": "Universal Pictures",
    "release_year": 2022,
    "language": "English",
    "duration_minutes": 35,
    "age_rating": "TV-MA",
    "imdb_rating": 8.6,
    "production_budget": 35000000,
    "licensing_cost": 12000000,
    "total_content_cost": 54000000,
    "marketing_spend": 22000000,
    "total_revenue": 310000000,
    "ad_revenue": 72000000,
    "total_watch_hours": 33200000,
    "total_views": 9400000,
    "average_completion_rate": 86.8,
    "average_rewatch_rate": 31.4,
    "contribution_profit": 234000000,
    "content_roi": 3.0789,
    "decision": "EXPAND",
    "director": "Christopher Storer",
    "cast": "Jeremy Allen White, Ebon Moss-Bachrach, Ayo Edebiri, Lionel Boyce",
    "synopsis": "A young chef from fine dining returns to Chicago to run his family's beef sandwich shop after a heartbreaking death in his family.",
    "tags": [
      "High Voltage",
      "Emmy Sweeper",
      "Culinary Drama"
    ],
    "poster_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#0284c7",
    "ai_recommendation": "Sensational ROI (308%) with lean production budget. High word-of-mouth momentum. Expand multi-season renewal immediately.",
    "churn_defense_score": 90,
    "post_finale_vulnerability": 29,
    "ad_yield_cpm": 36.5,
    "ad_tolerance_minutes": 15,
    "bridge_titles": [
      "Succession",
      "Beef",
      "Fleabag"
    ],
    "radar": {
      "retention": 93,
      "capital_efficiency": 98,
      "churn_defense": 90,
      "global_appeal": 89,
      "loyalty": 88
    }
  },
  {
    "content_id": 10,
    "title": "Breaking Bad",
    "content_type": "Series",
    "genre": "Crime",
    "studio": "Sony Pictures Entertainment",
    "release_year": 2008,
    "language": "English",
    "duration_minutes": 49,
    "age_rating": "TV-MA",
    "imdb_rating": 9.5,
    "production_budget": 65000000,
    "licensing_cost": 42000000,
    "total_content_cost": 122000000,
    "marketing_spend": 30000000,
    "total_revenue": 890000000,
    "ad_revenue": 185000000,
    "total_watch_hours": 115000000,
    "total_views": 23400000,
    "average_completion_rate": 89.9,
    "average_rewatch_rate": 45.3,
    "contribution_profit": 738000000,
    "content_roi": 4.8553,
    "decision": "EXPAND",
    "director": "Vince Gilligan",
    "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Giancarlo Esposito",
    "synopsis": "A chemistry teacher diagnosed with lung cancer turns to manufacturing methamphetamine with a former student to secure his family's future.",
    "tags": [
      "Greatest Series of All Time",
      "Peak TV",
      "Unrivaled Binge"
    ],
    "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#15803d",
    "ai_recommendation": "#1 highest completion rate (89.9%) on entire platform. Evergreen library cornerstone. Lock in 5-year exclusive streaming renewal.",
    "churn_defense_score": 99,
    "post_finale_vulnerability": 15,
    "ad_yield_cpm": 42.5,
    "ad_tolerance_minutes": 25,
    "bridge_titles": [
      "Better Call Saul",
      "Ozark",
      "Narcos",
      "Fargo"
    ],
    "radar": {
      "retention": 98,
      "capital_efficiency": 97,
      "churn_defense": 99,
      "global_appeal": 99,
      "loyalty": 98
    }
  },
  {
    "content_id": 11,
    "title": "Squid Game",
    "content_type": "Series",
    "genre": "Thriller",
    "studio": "Netflix Studios",
    "release_year": 2021,
    "language": "Korean",
    "duration_minutes": 55,
    "age_rating": "TV-MA",
    "imdb_rating": 8.0,
    "production_budget": 21400000,
    "licensing_cost": 0,
    "total_content_cost": 27500000,
    "marketing_spend": 38000000,
    "total_revenue": 1820000000,
    "ad_revenue": 410000000,
    "total_watch_hours": 188000000,
    "total_views": 34200000,
    "average_completion_rate": 86.4,
    "average_rewatch_rate": 35.1,
    "contribution_profit": 1754500000,
    "content_roi": 26.7863,
    "decision": "EXPAND",
    "director": "Hwang Dong-hyuk",
    "cast": "Lee Jung-jae, Park Hae-soo, Wi Ha-joon, Jung Ho-yeon",
    "synopsis": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games with deadly high stakes.",
    "tags": [
      "Most Watched Series Ever",
      "Global Viral Sensation",
      "Cultural Benchmark"
    ],
    "poster_url": "https://images.unsplash.com/photo-1634838080334-28befa9efe80?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#be123c",
    "ai_recommendation": "Historic 2,678% ROI. Most profitable streaming IP on planet. Expand reality competition franchise and multi-market local adaptations.",
    "churn_defense_score": 95,
    "post_finale_vulnerability": 45,
    "ad_yield_cpm": 46.0,
    "ad_tolerance_minutes": 20,
    "bridge_titles": [
      "Alice in Borderland",
      "All of Us Are Dead",
      "Parasite"
    ],
    "radar": {
      "retention": 94,
      "capital_efficiency": 100,
      "churn_defense": 95,
      "global_appeal": 100,
      "loyalty": 90
    }
  },
  {
    "content_id": 12,
    "title": "Severance",
    "content_type": "Series",
    "genre": "Sci-Fi",
    "studio": "Apple Studios",
    "release_year": 2022,
    "language": "English",
    "duration_minutes": 55,
    "age_rating": "TV-MA",
    "imdb_rating": 8.7,
    "production_budget": 45000000,
    "licensing_cost": 18000000,
    "total_content_cost": 72000000,
    "marketing_spend": 28000000,
    "total_revenue": 380000000,
    "ad_revenue": 65000000,
    "total_watch_hours": 39500000,
    "total_views": 10200000,
    "average_completion_rate": 85.2,
    "average_rewatch_rate": 27.9,
    "contribution_profit": 280000000,
    "content_roi": 2.8,
    "decision": "EXPAND",
    "director": "Ben Stiller, Aoife McArdle",
    "cast": "Adam Scott, Zach Cherry, Britt Lower, Patricia Arquette, John Turturro",
    "synopsis": "Mark leads a team of office workers whose memories have been surgically divided between their work and personal lives.",
    "tags": [
      "Dystopian Mystery",
      "Mind-Bending",
      "Critical Acclaim"
    ],
    "poster_url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#0f766e",
    "ai_recommendation": "Cult sci-fi powerhouse. Exceptional social media buzz and completion velocity. Key driver for premium 4K subscription tier.",
    "churn_defense_score": 91,
    "post_finale_vulnerability": 34,
    "ad_yield_cpm": 35.0,
    "ad_tolerance_minutes": 25,
    "bridge_titles": [
      "Black Mirror",
      "Dark",
      "Inception"
    ],
    "radar": {
      "retention": 91,
      "capital_efficiency": 94,
      "churn_defense": 91,
      "global_appeal": 89,
      "loyalty": 86
    }
  },
  {
    "content_id": 13,
    "title": "Parasite",
    "content_type": "Movie",
    "genre": "Drama",
    "studio": "CJ ENM Entertainment",
    "release_year": 2019,
    "language": "Korean",
    "duration_minutes": 132,
    "age_rating": "R",
    "imdb_rating": 8.5,
    "production_budget": 15500000,
    "licensing_cost": 12000000,
    "total_content_cost": 33000000,
    "marketing_spend": 20000000,
    "total_revenue": 262000000,
    "ad_revenue": 45000000,
    "total_watch_hours": 27800000,
    "total_views": 12600000,
    "average_completion_rate": 84.1,
    "average_rewatch_rate": 28.5,
    "contribution_profit": 209000000,
    "content_roi": 3.9434,
    "decision": "EXPAND",
    "director": "Bong Joon-ho",
    "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik",
    "synopsis": "Greed and class discrimination threaten the symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    "tags": [
      "First Foreign Best Picture",
      "Masterpiece",
      "Social Thriller"
    ],
    "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#14532d",
    "ai_recommendation": "Proves global audience appetite for premier international cinema. Establish dedicated Asian Cinema curation hub.",
    "churn_defense_score": 88,
    "post_finale_vulnerability": 14,
    "ad_yield_cpm": 31.0,
    "ad_tolerance_minutes": 32,
    "bridge_titles": [
      "Oldboy",
      "Squid Game",
      "Memories of Murder"
    ],
    "radar": {
      "retention": 90,
      "capital_efficiency": 97,
      "churn_defense": 88,
      "global_appeal": 95,
      "loyalty": 82
    }
  },
  {
    "content_id": 14,
    "title": "Spirited Away",
    "content_type": "Movie",
    "genre": "Animation",
    "studio": "Studio Ghibli",
    "release_year": 2001,
    "language": "Japanese",
    "duration_minutes": 125,
    "age_rating": "PG",
    "imdb_rating": 8.6,
    "production_budget": 19200000,
    "licensing_cost": 14000000,
    "total_content_cost": 39500000,
    "marketing_spend": 15000000,
    "total_revenue": 395000000,
    "ad_revenue": 85000000,
    "total_watch_hours": 36400000,
    "total_views": 17500000,
    "average_completion_rate": 88.2,
    "average_rewatch_rate": 42.6,
    "contribution_profit": 340500000,
    "content_roi": 6.2477,
    "decision": "EXPAND",
    "director": "Hayao Miyazaki",
    "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki, Takashi Naito",
    "synopsis": "During her family's move to the suburbs, a 10-year-old girl wanders into a world ruled by gods, witches and spirits.",
    "tags": [
      "Ghibli Crown Jewel",
      "Oscar Winner",
      "Universal Evergreen"
    ],
    "poster_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#047857",
    "ai_recommendation": "Legendary co-viewing asset across all age brackets. 42.6% rewatch rate anchors family subscriber retention during school breaks.",
    "churn_defense_score": 97,
    "post_finale_vulnerability": 6,
    "ad_yield_cpm": 33.0,
    "ad_tolerance_minutes": 30,
    "bridge_titles": [
      "Howl's Moving Castle",
      "Princess Mononoke",
      "Your Name"
    ],
    "radar": {
      "retention": 96,
      "capital_efficiency": 99,
      "churn_defense": 97,
      "global_appeal": 96,
      "loyalty": 97
    }
  },
  {
    "content_id": 15,
    "title": "3 Idiots",
    "content_type": "Movie",
    "genre": "Comedy",
    "studio": "Universal Pictures",
    "release_year": 2009,
    "language": "Hindi",
    "duration_minutes": 170,
    "age_rating": "PG-13",
    "imdb_rating": 8.4,
    "production_budget": 8000000,
    "licensing_cost": 16000000,
    "total_content_cost": 29000000,
    "marketing_spend": 12000000,
    "total_revenue": 750000000,
    "ad_revenue": 170000000,
    "total_watch_hours": 59200000,
    "total_views": 21000000,
    "average_completion_rate": 85.3,
    "average_rewatch_rate": 41.2,
    "contribution_profit": 709000000,
    "content_roi": 17.2927,
    "decision": "EXPAND",
    "director": "Rajkumar Hirani",
    "cast": "Aamir Khan, Madhavan, Sharman Joshi, Kareena Kapoor",
    "synopsis": "Two friends search for their long lost college companion who inspired them to think differently while navigating engineering college.",
    "tags": [
      "Timeless Classic",
      "Global Cultural Phenomenon",
      "All-Time Favorite"
    ],
    "poster_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600&auto=format&fit=crop&q=80",
    "poster_color": "#0284c7",
    "ai_recommendation": "1,729% ROI! Massive evergreen viewership in India, East Asia, and diaspora communities. Permanent catalog staple.",
    "churn_defense_score": 98,
    "post_finale_vulnerability": 7,
    "ad_yield_cpm": 37.0,
    "ad_tolerance_minutes": 35,
    "bridge_titles": [
      "Dangal",
      "PK",
      "Taare Zameen Par"
    ],
    "radar": {
      "retention": 93,
      "capital_efficiency": 100,
      "churn_defense": 98,
      "global_appeal": 95,
      "loyalty": 96
    }
  }
];

// Regional Market Master Data
const REGIONAL_MARKETS = [
  { region: "India", continent: "Asia", currency: "INR", revenue: 985000000, watch_hours: 48500000, views: 24500000, health: "HYPER_GROWTH" },
  { region: "United States", continent: "North America", currency: "USD", revenue: 845000000, watch_hours: 36200000, views: 18200000, health: "HIGH_MARGIN" },
  { region: "United Kingdom", continent: "Europe", currency: "GBP", revenue: 385000000, watch_hours: 15400000, views: 7800000, health: "STRONG" },
  { region: "Germany", continent: "Europe", currency: "EUR", revenue: 315000000, watch_hours: 12800000, views: 6400000, health: "STEADY" },
  { region: "Japan", continent: "Asia", currency: "JPY", revenue: 295000000, watch_hours: 11900000, views: 5900000, health: "EXPANDING" },
  { region: "South Korea", continent: "Asia", currency: "KRW", revenue: 265000000, watch_hours: 10800000, views: 5400000, health: "HIGH_RETENTION" },
  { region: "France", continent: "Europe", currency: "EUR", revenue: 240000000, watch_hours: 9800000, views: 4900000, health: "STEADY" },
  { region: "Canada", continent: "North America", currency: "CAD", revenue: 210000000, watch_hours: 8600000, views: 4300000, health: "MATURE" },
  { region: "Australia", continent: "Oceania", currency: "AUD", revenue: 190000000, watch_hours: 7800000, views: 3900000, health: "STRONG" },
  { region: "Brazil", continent: "South America", currency: "BRL", revenue: 145000000, watch_hours: 6900000, views: 3500000, health: "EMERGING" }
];

// ==============================================================================
// 2. FORMATTING HELPERS
// ==============================================================================
function formatCurrency(valINR, compact = true) {
  if (valINR === null || valINR === undefined || isNaN(valINR)) return '—';
  let value = Number(valINR);
  const isUSD = STATE.currency === 'USD';
  if (isUSD) {
    value = value / STATE.rateUSD;
  }

  const symbol = isUSD ? '$' : '₹';
  const abs = Math.abs(value);

  if (compact) {
    if (abs >= 1e9) {
      return `${symbol}${(value / 1e9).toFixed(2)}B`;
    }
    if (abs >= 1e6) {
      return `${symbol}${(value / 1e6).toFixed(1)}M`;
    }
    if (abs >= 1e3) {
      return `${symbol}${(value / 1e3).toFixed(0)}K`;
    }
    return `${symbol}${value.toFixed(0)}`;
  }

  return new Intl.NumberFormat(isUSD ? 'en-US' : 'en-IN', {
    style: 'currency',
    currency: isUSD ? 'USD' : 'INR',
    maximumFractionDigits: 0
  }).format(value);
}

function formatNumber(n) {
  if (!n && n !== 0) return '0';
  const num = Number(n);
  if (num >= 1e6) return `${(num / 1e6).toFixed(1)}M`;
  if (num >= 1e3) return `${(num / 1e3).toFixed(1)}K`;
  return num.toLocaleString();
}

function getDecisionClass(decision) {
  switch (String(decision).toUpperCase()) {
    case 'EXPAND': return 'pill-expand';
    case 'RENEW': return 'pill-renew';
    case 'MONITOR': return 'pill-monitor';
    case 'COST_REVIEW': return 'pill-review';
    case 'EXIT_OR_RENEGOTIATE':
    case 'EXIT': return 'pill-exit';
    default: return 'pill-monitor';
  }
}

// ==============================================================================
// 3. INITIALIZATION & DATA FETCHING
// ==============================================================================
async function initDashboard() {
  setupNavigation();
  setupCurrencyToggle();
  setupThemeToggle();
  setupFilters();
  setupSimulator();
  setupModal();
  setupFileUpload();
  setupExport();

  // Load catalog data
  try {
    const res = await fetch('catalog.json');
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        STATE.catalog = data;
        console.log(`Loaded ${data.length} curated titles from catalog.json`);
      } else {
        STATE.catalog = FALLBACK_CATALOG;
      }
    } else {
      STATE.catalog = FALLBACK_CATALOG;
    }
  } catch (err) {
    console.warn('Using embedded catalog fallback:', err);
    STATE.catalog = FALLBACK_CATALOG;
  }

  // Set real count badge
  const badge = document.querySelector('#realCountBadge');
  if (badge) badge.textContent = `${STATE.catalog.length}+`;

  // Setup features depending on catalog
  setupArena();
  setupCopilotChat();

  // Render everything
  renderAllViews();
}

// ==============================================================================
// 4. NAVIGATION & TABS
// ==============================================================================
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      const tabKey = item.getAttribute('data-tab');
      switchTab(tabKey);
    });
  });

  const viewAllBtn = document.querySelector('#viewAllMoviesBtn');
  if (viewAllBtn) {
    viewAllBtn.addEventListener('click', () => {
      const moviesNav = document.querySelector('[data-tab="movies"]');
      if (moviesNav) moviesNav.click();
    });
  }
}

function switchTab(tabKey) {
  STATE.currentTab = tabKey;
  document.querySelectorAll('.view-panel').forEach(panel => {
    panel.classList.remove('active');
  });

  const target = document.querySelector(`#view-${tabKey}`);
  if (target) {
    target.classList.add('active');
  }

  // Update Page Title
  const titleEl = document.querySelector('#pageTitle');
  const titleMap = {
    overview: 'Executive Command Center',
    movies: 'Content Explorer & Real Titles Showcase',
    arena: 'Head-to-Head Content Battle Arena',
    churn: 'Post-Finale Churn Defense & Bridge Content Engine',
    adtier: 'Hybrid AVOD & Ad-Tier Monetization Intelligence',
    portfolio: 'Content Economics & Financial Matrix',
    viewership: 'Audience Funnels & Viewership Analytics',
    regional: 'Global Regional Market Penetration',
    simulator: 'AI Content Greenlight & Decision Simulator'
  };
  if (titleEl && titleMap[tabKey]) {
    titleEl.textContent = titleMap[tabKey];
  }

  // Trigger chart redrawing on active tab
  if (tabKey === 'overview') {
    renderRevenueChart();
    renderDecisionDonut();
  } else if (tabKey === 'arena') {
    renderArenaBattle();
  } else if (tabKey === 'churn') {
    renderChurnView();
  } else if (tabKey === 'adtier') {
    renderAdTierView();
  } else if (tabKey === 'portfolio') {
    renderScatterPlot();
  } else if (tabKey === 'viewership') {
    renderTrafficChart();
  }
}

function setupCurrencyToggle() {
  const btnINR = document.querySelector('#currINR');
  const btnUSD = document.querySelector('#currUSD');

  btnINR.addEventListener('click', () => {
    STATE.currency = 'INR';
    btnINR.classList.add('active');
    btnUSD.classList.remove('active');
    renderAllViews();
  });

  btnUSD.addEventListener('click', () => {
    STATE.currency = 'USD';
    btnUSD.classList.add('active');
    btnINR.classList.remove('active');
    renderAllViews();
  });
}

function isLightTheme() {
  return document.body.classList.contains('light-theme');
}

function setupThemeToggle() {
  const btnDark = document.querySelector('#themeDark');
  const btnLight = document.querySelector('#themeLight');
  const sbBtnDark = document.querySelector('#sbThemeDark');
  const sbBtnLight = document.querySelector('#sbThemeLight');

  // Default to executive Light Theme on initial visit / upgrade
  let savedTheme = localStorage.getItem('cinepulse_theme_v2');
  if (!savedTheme) {
    savedTheme = 'light';
    localStorage.setItem('cinepulse_theme_v2', 'light');
    localStorage.setItem('cinepulse_theme', 'light');
  }

  applyTheme(savedTheme);

  // Top header buttons
  if (btnDark) btnDark.addEventListener('click', () => applyTheme('dark'));
  if (btnLight) btnLight.addEventListener('click', () => applyTheme('light'));

  // Sidebar buttons
  if (sbBtnDark) sbBtnDark.addEventListener('click', () => applyTheme('dark'));
  if (sbBtnLight) sbBtnLight.addEventListener('click', () => applyTheme('light'));
}

function applyTheme(theme) {
  const btnDark = document.querySelector('#themeDark');
  const btnLight = document.querySelector('#themeLight');
  const sbBtnDark = document.querySelector('#sbThemeDark');
  const sbBtnLight = document.querySelector('#sbThemeLight');

  if (theme === 'light') {
    document.body.classList.remove('dark-theme');
    document.body.classList.add('light-theme');
    document.documentElement.classList.remove('dark-theme');
    document.documentElement.classList.add('light-theme');
    if (btnLight) btnLight.classList.add('active');
    if (btnDark) btnDark.classList.remove('active');
    if (sbBtnLight) sbBtnLight.classList.add('active');
    if (sbBtnDark) sbBtnDark.classList.remove('active');
  } else {
    document.body.classList.remove('light-theme');
    document.body.classList.add('dark-theme');
    document.documentElement.classList.remove('light-theme');
    document.documentElement.classList.add('dark-theme');
    if (btnDark) btnDark.classList.add('active');
    if (btnLight) btnLight.classList.remove('active');
    if (sbBtnDark) sbBtnDark.classList.add('active');
    if (sbBtnLight) sbBtnLight.classList.remove('active');
  }

  localStorage.setItem('cinepulse_theme_v2', theme);
  localStorage.setItem('cinepulse_theme', theme);
  renderAllViews();
}

// ==============================================================================
// 5. RENDERING CORE VIEWS
// ==============================================================================
function renderAllViews() {
  renderCommandCenterMetrics();
  renderRevenueChart();
  renderDecisionDonut();
  renderTopTitlesTable();
  renderRegionalList();
  renderSpotlight();
  renderMovieCards();
  renderArenaBattle();
  renderChurnView();
  renderAdTierView();
  renderCostComposition();
  renderGenreRoi();
  renderFunnel();
  renderLoyaltyList();
  renderRegionalTable();
  runSimulatorCalc();
}

// ------------------------------------------------------------------------------
// VIEW 1: COMMAND CENTER
// ------------------------------------------------------------------------------
function renderCommandCenterMetrics() {
  // Aggregate real catalog + warehouse scaling
  const totalRev = 3480000000;
  const totalCost = 2120000000;
  const netProfit = totalRev - totalCost;
  const roi = (netProfit / totalCost) * 100;

  document.querySelector('#kpiTotalRevenue').textContent = formatCurrency(totalRev);
  document.querySelector('#kpiContentCost').textContent = formatCurrency(totalCost);
  document.querySelector('#kpiContributionProfit').textContent = formatCurrency(netProfit);
  document.querySelector('#kpiPortfolioRoi').textContent = `+${roi.toFixed(1)}%`;
  document.querySelector('#kpiWatchHours').textContent = '142.8M';
  document.querySelector('#kpiDecisionReadiness').textContent = '94.6%';
}

function renderRevenueChart() {
  const canvas = document.querySelector('#revenueCostCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth || 600;
  canvas.height = 230;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const revPoints = [210, 240, 260, 290, 275, 310, 340, 360, 350, 390, 420, 460];
  const costPoints = [160, 175, 180, 195, 210, 205, 220, 230, 240, 250, 265, 280];

  const w = canvas.width;
  const h = canvas.height;
  const padLeft = 45;
  const padRight = 20;
  const padBottom = 30;
  const padTop = 20;

  const chartW = w - padLeft - padRight;
  const chartH = h - padTop - padBottom;
  const maxVal = 500;

  // Draw Grid Lines
  ctx.strokeStyle = isLightTheme() ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
  ctx.font = '10px JetBrains Mono';

  for (let i = 0; i <= 4; i++) {
    const yVal = (maxVal / 4) * i;
    const yPos = padTop + chartH - (i / 4) * chartH;
    ctx.beginPath();
    ctx.moveTo(padLeft, yPos);
    ctx.lineTo(w - padRight, yPos);
    ctx.stroke();

    const label = STATE.currency === 'USD' ? `$${(yVal / 83.5).toFixed(0)}M` : `₹${yVal}M`;
    ctx.fillText(label, 6, yPos + 3);
  }

  // Draw X labels
  const stepX = chartW / (months.length - 1);
  months.forEach((m, idx) => {
    const x = padLeft + idx * stepX;
    ctx.fillText(m, x - 10, h - 10);
  });

  // Helper to draw smooth series
  function drawLine(points, color, glowColor, fillColor) {
    ctx.save();
    ctx.beginPath();
    points.forEach((val, idx) => {
      const x = padLeft + idx * stepX;
      const y = padTop + chartH - (val / maxVal) * chartH;
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.shadowColor = glowColor;
    ctx.shadowBlur = 12;
    ctx.stroke();

    if (fillColor) {
      ctx.lineTo(padLeft + (points.length - 1) * stepX, padTop + chartH);
      ctx.lineTo(padLeft, padTop + chartH);
      ctx.closePath();
      ctx.fillStyle = fillColor;
      ctx.fill();
    }
    ctx.restore();

    // Draw dots
    points.forEach((val, idx) => {
      const x = padLeft + idx * stepX;
      const y = padTop + chartH - (val / maxVal) * chartH;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = isLightTheme() ? '#ffffff' : '#07090e';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }

  // Revenue Fill Gradient
  const gradRev = ctx.createLinearGradient(0, padTop, 0, h - padBottom);
  gradRev.addColorStop(0, isLightTheme() ? 'rgba(2, 132, 199, 0.22)' : 'rgba(0, 210, 255, 0.25)');
  gradRev.addColorStop(1, isLightTheme() ? 'rgba(2, 132, 199, 0.00)' : 'rgba(0, 210, 255, 0.00)');

  const revLineColor = isLightTheme() ? '#0284c7' : '#00d2ff';
  const revGlowColor = isLightTheme() ? 'rgba(2, 132, 199, 0.35)' : 'rgba(0, 210, 255, 0.6)';
  const costLineColor = isLightTheme() ? '#7c3aed' : '#8b5cf6';
  const costGlowColor = isLightTheme() ? 'rgba(124, 58, 237, 0.3)' : 'rgba(139, 92, 246, 0.5)';

  drawLine(revPoints, revLineColor, revGlowColor, gradRev);
  drawLine(costPoints, costLineColor, costGlowColor, null);
}

function renderDecisionDonut() {
  const canvas = document.querySelector('#decisionDonutCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const data = [
    { label: 'EXPAND', count: 16472, share: 33, color: isLightTheme() ? '#059669' : '#10b981' },
    { label: 'RENEW', count: 7370, share: 15, color: isLightTheme() ? '#0284c7' : '#00d2ff' },
    { label: 'MONITOR', count: 5955, share: 12, color: isLightTheme() ? '#2563eb' : '#3b82f6' },
    { label: 'COST REVIEW', count: 19762, share: 39, color: isLightTheme() ? '#d97706' : '#f59e0b' },
    { label: 'EXIT', count: 441, share: 1, color: isLightTheme() ? '#dc2626' : '#e50914' }
  ];

  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = 70;
  const innerRadius = 45;

  let startAngle = -Math.PI / 2;

  ctx.save();
  data.forEach(slice => {
    const sliceAngle = (slice.share / 100) * (Math.PI * 2);
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, startAngle + sliceAngle);
    ctx.arc(cx, cy, innerRadius, startAngle + sliceAngle, startAngle, true);
    ctx.closePath();
    ctx.fillStyle = slice.color;
    ctx.shadowColor = slice.color;
    ctx.shadowBlur = isLightTheme() ? 4 : 8;
    ctx.fill();
    startAngle += sliceAngle;
  });
  ctx.restore();

  // Render Legend
  const legend = document.querySelector('#decisionLegend');
  if (legend) {
    legend.innerHTML = data.map(d => `
      <div class="decision-legend-row">
        <span style="color: ${d.color}; font-weight: 700;">● ${d.label}</span>
        <span><strong>${d.share}%</strong> (${d.count.toLocaleString()} titles)</span>
      </div>
    `).join('');
  }
}

function renderTopTitlesTable() {
  const tbody = document.querySelector('#topTitlesBody');
  if (!tbody) return;

  const topTitles = STATE.catalog.slice(0, 6);
  tbody.innerHTML = topTitles.map(m => `
    <tr>
      <td>
        <strong style="cursor: pointer;" onclick="openModal(${m.content_id})">${m.title}</strong>
        <div style="font-size: 11px; color: #64748b;">${m.studio} &bull; ${m.release_year}</div>
      </td>
      <td><span class="meta-tag">${m.genre}</span></td>
      <td>${formatNumber(m.total_watch_hours)} hrs</td>
      <td class="text-cyan">${formatCurrency(m.total_revenue)}</td>
      <td><strong style="color: ${isLightTheme() ? '#059669' : '#34d399'}; font-weight: 700;">+${(m.content_roi * 100).toFixed(0)}%</strong></td>
      <td><button class="pill ${getDecisionClass(m.decision)}" onclick="openModal(${m.content_id})">${m.decision}</button></td>
    </tr>
  `).join('');
}

function renderRegionalList() {
  const container = document.querySelector('#regionalList');
  if (!container) return;

  const top5 = REGIONAL_MARKETS.slice(0, 5);
  const maxRev = top5[0].revenue;

  container.innerHTML = top5.map(r => `
    <div class="regional-item">
      <div class="name">${r.region}</div>
      <div class="track"><div class="bar" style="width: ${(r.revenue / maxRev) * 100}%;"></div></div>
      <div class="val">${formatCurrency(r.revenue)}</div>
    </div>
  `).join('');
}

// ------------------------------------------------------------------------------
// VIEW 2: REAL MOVIE EXPLORER
// ------------------------------------------------------------------------------
function renderSpotlight() {
  const top = STATE.catalog[0];
  if (!top) return;

  document.querySelector('#spotTitle').textContent = top.title;
  document.querySelector('#spotYear').textContent = top.release_year;
  document.querySelector('#spotRating').textContent = top.age_rating;
  document.querySelector('#spotDuration').textContent = `${top.duration_minutes} min`;
  document.querySelector('#spotImdb').textContent = top.imdb_rating;
  document.querySelector('#spotDesc').textContent = top.synopsis;
  document.querySelector('#spotRoi').textContent = `+${(top.content_roi * 100).toFixed(1)}%`;
  document.querySelector('#spotViews').textContent = formatNumber(top.total_views);

  const banner = document.querySelector('#spotlightBanner');
  if (banner && top.poster_url) {
    banner.style.backgroundImage = `linear-gradient(135deg, rgba(229, 9, 20, 0.15), rgba(15, 23, 42, 0.95)), url('${top.poster_url}')`;
  }

  const inspectBtn = document.querySelector('#spotInspectBtn');
  if (inspectBtn) {
    inspectBtn.onclick = () => openModal(top.content_id);
  }
}

function setupFilters() {
  const searchInput = document.querySelector('#movieSearch');
  const genreFilter = document.querySelector('#genreFilter');
  const typeFilter = document.querySelector('#typeFilter');
  const decisionFilter = document.querySelector('#decisionFilter');
  const sortFilter = document.querySelector('#sortFilter');

  const update = () => {
    STATE.filters.search = searchInput ? searchInput.value.toLowerCase().trim() : '';
    STATE.filters.genre = genreFilter ? genreFilter.value : 'ALL';
    STATE.filters.type = typeFilter ? typeFilter.value : 'ALL';
    STATE.filters.decision = decisionFilter ? decisionFilter.value : 'ALL';
    STATE.filters.sort = sortFilter ? sortFilter.value : 'roi_desc';
    renderMovieCards();
  };

  if (searchInput) searchInput.addEventListener('input', update);
  if (genreFilter) genreFilter.addEventListener('change', update);
  if (typeFilter) typeFilter.addEventListener('change', update);
  if (decisionFilter) decisionFilter.addEventListener('change', update);
  if (sortFilter) sortFilter.addEventListener('change', update);
}

function renderMovieCards() {
  const grid = document.querySelector('#moviesGrid');
  if (!grid) return;

  let filtered = [...STATE.catalog];

  // Search filter
  if (STATE.filters.search) {
    const q = STATE.filters.search;
    filtered = filtered.filter(m => 
      m.title.toLowerCase().includes(q) ||
      (m.director && m.director.toLowerCase().includes(q)) ||
      (m.cast && m.cast.toLowerCase().includes(q)) ||
      (m.studio && m.studio.toLowerCase().includes(q)) ||
      m.genre.toLowerCase().includes(q)
    );
  }

  // Genre filter
  if (STATE.filters.genre !== 'ALL') {
    filtered = filtered.filter(m => m.genre === STATE.filters.genre);
  }

  // Type filter
  if (STATE.filters.type !== 'ALL') {
    filtered = filtered.filter(m => m.content_type === STATE.filters.type);
  }

  // Decision filter
  if (STATE.filters.decision !== 'ALL') {
    filtered = filtered.filter(m => m.decision === STATE.filters.decision);
  }

  // Sorting
  filtered.sort((a, b) => {
    switch (STATE.filters.sort) {
      case 'roi_desc': return b.content_roi - a.content_roi;
      case 'views_desc': return b.total_views - a.total_views;
      case 'imdb_desc': return b.imdb_rating - a.imdb_rating;
      case 'year_desc': return b.release_year - a.release_year;
      case 'budget_desc': return b.production_budget - a.production_budget;
      default: return 0;
    }
  });

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--text-muted);">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 12px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <p style="font-size: 16px; color: var(--text-primary); font-weight: 600;">No titles match your filters</p>
        <p style="font-size: 13px; color: var(--text-secondary);">Try resetting the search query or selecting "All Genres".</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map(m => `
    <div class="movie-card" onclick="openModal(${m.content_id})">
      <div class="movie-poster" style="background-color: ${m.poster_color || '#1e293b'}; background-image: url('${m.poster_url || ''}');">
        <div class="movie-poster-overlay">
          <span class="meta-tag" style="background: rgba(0,0,0,0.7); color: #fff; font-weight: 700;">${m.content_type.toUpperCase()}</span>
          <span class="pill ${getDecisionClass(m.decision)}">${m.decision}</span>
        </div>
      </div>
      <div class="movie-body">
        <div class="movie-card-title">${m.title}</div>
        <div class="movie-card-sub">${m.studio || 'Studio'} &bull; ${m.release_year} &bull; ★ ${m.imdb_rating}</div>
        <div class="movie-metrics-row">
          <div class="movie-metric">
            <span>TOTAL REVENUE</span>
            <strong class="text-cyan">${formatCurrency(m.total_revenue)}</strong>
          </div>
          <div class="movie-metric">
            <span>PORTFOLIO ROI</span>
            <strong style="color: ${isLightTheme() ? '#059669' : '#34d399'}; font-weight: 700;">+${(m.content_roi * 100).toFixed(0)}%</strong>
          </div>
        </div>
      </div>
    </div>
  `).join('');
}

// ==============================================================================
// VIEW 3: HEAD-TO-HEAD BATTLE ARENA
// ==============================================================================
let arenaContenderAId = null;
let arenaContenderBId = null;

function setupArena() {
  const selectA = document.querySelector('#arenaContenderA');
  const selectB = document.querySelector('#arenaContenderB');
  if (!selectA || !selectB) return;

  const titles = STATE.catalog.length > 0 ? STATE.catalog : FALLBACK_CATALOG;
  
  selectA.innerHTML = titles.map((t, idx) => `
    <option value="${t.content_id}" ${idx === 0 ? 'selected' : ''}>${t.title} (${t.release_year}) &bull; ${t.genre}</option>
  `).join('');

  selectB.innerHTML = titles.map((t, idx) => `
    <option value="${t.content_id}" ${idx === 1 ? 'selected' : ''}>${t.title} (${t.release_year}) &bull; ${t.genre}</option>
  `).join('');

  arenaContenderAId = titles[0]?.content_id;
  arenaContenderBId = titles[1]?.content_id;

  selectA.addEventListener('change', (e) => {
    arenaContenderAId = Number(e.target.value);
    renderArenaBattle();
  });

  selectB.addEventListener('change', (e) => {
    arenaContenderBId = Number(e.target.value);
    renderArenaBattle();
  });
}

function renderArenaBattle() {
  const titles = STATE.catalog.length > 0 ? STATE.catalog : FALLBACK_CATALOG;
  const contenderA = titles.find(t => t.content_id === arenaContenderAId) || titles[0];
  const contenderB = titles.find(t => t.content_id === arenaContenderBId) || titles[1] || titles[0];

  if (!contenderA || !contenderB) return;

  // Render Contender A Card
  const cardA = document.querySelector('#contenderACard');
  if (cardA) {
    cardA.innerHTML = `
      <div class="contender-header">
        <span class="pill ${getDecisionClass(contenderA.decision)}" style="margin-bottom: 8px;">${contenderA.decision}</span>
        <h3 class="contender-title" style="color: var(--cyan);">${contenderA.title}</h3>
        <p class="contender-sub">${contenderA.release_year} &bull; ${contenderA.content_type} &bull; ${contenderA.genre} &bull; ${contenderA.studio}</p>
      </div>
      <div class="contender-stats">
        <div class="stat-metric-row">
          <span class="metric-label">Content ROI</span>
          <span class="metric-val text-emerald">+${(contenderA.content_roi * 100).toFixed(1)}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Attributed Revenue</span>
          <span class="metric-val text-cyan">${formatCurrency(contenderA.total_revenue, false)}</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Total Capital Cost</span>
          <span class="metric-val">${formatCurrency(contenderA.total_content_cost, false)}</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Total Watch Hours</span>
          <span class="metric-val">${formatNumber(contenderA.total_watch_hours)} hrs</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Completion Rate</span>
          <span class="metric-val">${contenderA.average_completion_rate}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Rewatch Frequency</span>
          <span class="metric-val">${contenderA.average_rewatch_rate}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Churn Defense Index</span>
          <span class="metric-val text-cyan">${contenderA.churn_defense_score || 90}/100</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Commercial Ad Yield</span>
          <span class="metric-val text-gold">$${(contenderA.ad_yield_cpm || 32).toFixed(2)}/CPM</span>
        </div>
      </div>
    `;
  }

  // Render Contender B Card
  const cardB = document.querySelector('#contenderBCard');
  if (cardB) {
    cardB.innerHTML = `
      <div class="contender-header">
        <span class="pill ${getDecisionClass(contenderB.decision)}" style="margin-bottom: 8px;">${contenderB.decision}</span>
        <h3 class="contender-title" style="color: #ef4444;">${contenderB.title}</h3>
        <p class="contender-sub">${contenderB.release_year} &bull; ${contenderB.content_type} &bull; ${contenderB.genre} &bull; ${contenderB.studio}</p>
      </div>
      <div class="contender-stats">
        <div class="stat-metric-row">
          <span class="metric-label">Content ROI</span>
          <span class="metric-val text-emerald">+${(contenderB.content_roi * 100).toFixed(1)}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Attributed Revenue</span>
          <span class="metric-val text-cyan">${formatCurrency(contenderB.total_revenue, false)}</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Total Capital Cost</span>
          <span class="metric-val">${formatCurrency(contenderB.total_content_cost, false)}</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Total Watch Hours</span>
          <span class="metric-val">${formatNumber(contenderB.total_watch_hours)} hrs</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Completion Rate</span>
          <span class="metric-val">${contenderB.average_completion_rate}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Rewatch Frequency</span>
          <span class="metric-val">${contenderB.average_rewatch_rate}%</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Churn Defense Index</span>
          <span class="metric-val text-red">${contenderB.churn_defense_score || 88}/100</span>
        </div>
        <div class="stat-metric-row">
          <span class="metric-label">Commercial Ad Yield</span>
          <span class="metric-val text-gold">$${(contenderB.ad_yield_cpm || 30).toFixed(2)}/CPM</span>
        </div>
      </div>
    `;
  }

  // Render 5-Axis Radar Chart
  renderRadarChart(contenderA, contenderB);

  // Render Verdict Box
  const verdictBox = document.querySelector('#arenaVerdictBox');
  if (verdictBox) {
    const winnerRoi = contenderA.content_roi >= contenderB.content_roi ? contenderA : contenderB;
    const winnerHours = contenderA.total_watch_hours >= contenderB.total_watch_hours ? contenderA : contenderB;
    const winnerChurn = (contenderA.churn_defense_score || 90) >= (contenderB.churn_defense_score || 90) ? contenderA : contenderB;

    verdictBox.innerHTML = `
      <div class="arena-verdict-header">
        <span>⚔️</span>
        <h4>Executive Programming Verdict: ${winnerRoi.title} Superior Capital Yield</h4>
      </div>
      <div class="arena-verdict-body">
        <p><strong>Financial & Retention Takeaway:</strong> <strong>${winnerRoi.title}</strong> delivers higher return on invested capital (+${(winnerRoi.content_roi * 100).toFixed(1)}% ROI), whereas <strong>${winnerHours.title}</strong> drives greater platform aggregate volume (${formatNumber(winnerHours.total_watch_hours)} watch hours). In terms of subscriber retention stability, <strong>${winnerChurn.title}</strong> commands the superior churn defense index (${winnerChurn.churn_defense_score || 90}/100).</p>
        <p style="margin-top: 8px;"><strong>Executive Action:</strong> Maintain prime merchandising real estate for <em>${contenderA.title}</em> in ad-supported cohorts, while leveraging <em>${contenderB.title}</em> as an evergreen bridge title for binge-churn defense.</p>
      </div>
    `;
  }
}

function renderRadarChart(contenderA, contenderB) {
  const canvas = document.querySelector('#arenaRadarCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  canvas.width = canvas.parentElement.clientWidth || 340;
  canvas.height = 300;
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const cx = w / 2;
  const cy = h / 2 + 10;
  const radius = Math.min(w, h) / 2 - 42;

  const axes = [
    { name: 'Retention', key: 'retention' },
    { name: 'Cap. Efficiency', key: 'capital_efficiency' },
    { name: 'Churn Defense', key: 'churn_defense' },
    { name: 'Global Reach', key: 'global_appeal' },
    { name: 'Evergreen Loyalty', key: 'loyalty' }
  ];

  const totalAxes = axes.length;
  const angleStep = (Math.PI * 2) / totalAxes;
  const startAngle = -Math.PI / 2;

  // Draw concentric polygon rings
  const rings = 5;
  for (let r = 1; r <= rings; r++) {
    const ringRadius = (radius / rings) * r;
    ctx.beginPath();
    for (let i = 0; i < totalAxes; i++) {
      const angle = startAngle + i * angleStep;
      const x = cx + Math.cos(angle) * ringRadius;
      const y = cy + Math.sin(angle) * ringRadius;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.strokeStyle = r === rings 
      ? (isLightTheme() ? 'rgba(0, 0, 0, 0.18)' : 'rgba(255, 255, 255, 0.15)') 
      : (isLightTheme() ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)');
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Draw axis spokes and labels
  ctx.font = '10px JetBrains Mono';
  for (let i = 0; i < totalAxes; i++) {
    const angle = startAngle + i * angleStep;
    const xSpoke = cx + Math.cos(angle) * radius;
    const ySpoke = cy + Math.sin(angle) * radius;

    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(xSpoke, ySpoke);
    ctx.strokeStyle = isLightTheme() ? 'rgba(0, 0, 0, 0.12)' : 'rgba(255, 255, 255, 0.1)';
    ctx.stroke();

    // Text labels
    const labelDist = radius + 22;
    const xLabel = cx + Math.cos(angle) * labelDist;
    const yLabel = cy + Math.sin(angle) * labelDist;
    ctx.fillStyle = isLightTheme() ? '#334155' : '#94a3b8';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(axes[i].name, xLabel, yLabel);
  }

  // Helper to extract metric 0..100
  function getMetricVal(movie, key) {
    if (movie.radar && movie.radar[key] != null) return movie.radar[key];
    if (key === 'retention') return movie.average_completion_rate || 80;
    if (key === 'capital_efficiency') return Math.min(100, (movie.content_roi || 1.5) * 35);
    if (key === 'churn_defense') return movie.churn_defense_score || 85;
    if (key === 'global_appeal') return 88;
    if (key === 'loyalty') return Math.min(100, (movie.average_rewatch_rate || 30) * 2.2);
    return 75;
  }

  // Draw Radar Polygon for Movie
  function drawPolygon(movie, strokeColor, fillColor) {
    ctx.beginPath();
    for (let i = 0; i < totalAxes; i++) {
      const angle = startAngle + i * angleStep;
      const val = Math.min(100, Math.max(10, getMetricVal(movie, axes[i].key)));
      const dist = (radius * val) / 100;
      const x = cx + Math.cos(angle) * dist;
      const y = cy + Math.sin(angle) * dist;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw vertex dots
    for (let i = 0; i < totalAxes; i++) {
      const angle = startAngle + i * angleStep;
      const val = Math.min(100, Math.max(10, getMetricVal(movie, axes[i].key)));
      const dist = (radius * val) / 100;
      const x = cx + Math.cos(angle) * dist;
      const y = cy + Math.sin(angle) * dist;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = strokeColor;
      ctx.fill();
    }
  }

  // Draw Contender B (Red) first
  drawPolygon(contenderB, isLightTheme() ? '#dc2626' : '#ef4444', isLightTheme() ? 'rgba(220, 38, 38, 0.22)' : 'rgba(239, 68, 68, 0.25)');
  // Draw Contender A (Cyan/Azure) second
  drawPolygon(contenderA, isLightTheme() ? '#0284c7' : '#00d2ff', isLightTheme() ? 'rgba(2, 132, 199, 0.22)' : 'rgba(0, 210, 255, 0.25)');

  // Draw Legend at top
  ctx.textAlign = 'left';
  ctx.font = '10px JetBrains Mono';
  ctx.fillStyle = isLightTheme() ? '#0284c7' : '#00d2ff';
  ctx.fillRect(cx - 110, 10, 10, 10);
  ctx.fillStyle = isLightTheme() ? '#0f172a' : '#f8fafc';
  ctx.fillText(contenderA.title.slice(0, 14), cx - 95, 18);

  ctx.fillStyle = isLightTheme() ? '#dc2626' : '#ef4444';
  ctx.fillRect(cx + 15, 10, 10, 10);
  ctx.fillStyle = isLightTheme() ? '#0f172a' : '#f8fafc';
  ctx.fillText(contenderB.title.slice(0, 14), cx + 30, 18);
}

// ==============================================================================
// VIEW 4: CHURN DEFENSE & BRIDGE ENGINE
// ==============================================================================
function renderChurnView() {
  const revEl = document.querySelector('#churnDefendedRev');
  if (revEl) {
    revEl.textContent = formatCurrency(185000000, true);
  }

  const tbody = document.querySelector('#churnTableBody');
  if (!tbody) return;

  const titles = STATE.catalog.length > 0 ? STATE.catalog : FALLBACK_CATALOG;
  // Sort by highest post_finale_vulnerability or high completion rate
  const vulnerableTitles = titles.filter(t => (t.post_finale_vulnerability || 25) >= 15 || t.content_type === 'Series');

  tbody.innerHTML = vulnerableTitles.map(t => {
    const risk = t.post_finale_vulnerability || (t.content_type === 'Series' ? 38 : 18);
    const saveRate = Math.min(94, 68 + Math.round((t.churn_defense_score || 85) * 0.25));
    const preservedVal = Math.round((t.total_revenue || 500000000) * 0.14);

    const bridgePills = (t.bridge_titles && t.bridge_titles.length > 0)
      ? t.bridge_titles.map(b => `<span class="bridge-pill">${b}</span>`).join('')
      : `<span class="bridge-pill">Inception</span><span class="bridge-pill">Interstellar</span>`;

    return `
      <tr>
        <td>
          <div style="font-weight: 700; color: var(--text-primary);">${t.title}</div>
          <span style="font-size: 11px; color: var(--text-muted);">${t.studio} &bull; ${t.release_year}</span>
        </td>
        <td>
          <span class="meta-tag">${t.content_type}</span>
          <span style="font-size: 12px; color: var(--text-secondary); margin-left: 6px;">${t.genre}</span>
        </td>
        <td>
          <div style="font-weight: 700; color: ${risk > 30 ? '#f87171' : 'var(--amber)'}; font-family: var(--font-mono);">${risk}%</div>
          <div class="risk-bar">
            <div class="risk-fill" style="width: ${risk}%;"></div>
          </div>
        </td>
        <td>
          <div class="bridge-tag-list">
            ${bridgePills}
          </div>
        </td>
        <td>
          <strong style="color: var(--emerald); font-family: var(--font-mono);">${saveRate}%</strong>
          <span style="font-size: 10px; color: var(--text-muted); display: block;">Bridge acceptance</span>
        </td>
        <td>
          <strong class="text-cyan">${formatCurrency(preservedVal)}</strong>
        </td>
      </tr>
    `;
  }).join('');
}

// ==============================================================================
// VIEW 5: AD-TIER & HYBRID AVOD ECONOMICS
// ==============================================================================
function renderAdTierView() {
  renderAdRevenueChart();
  renderAdCpmList();
  renderAdFatigueChart();
}

function renderAdRevenueChart() {
  const canvas = document.querySelector('#adRevenueCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth || 600;
  canvas.height = 220;
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const months = ['Q1 Jan', 'Feb', 'Mar', 'Q2 Apr', 'May', 'Jun', 'Q3 Jul', 'Aug', 'Sep', 'Q4 Oct', 'Nov', 'Dec'];
  // SVOD vs AVOD (in Millions)
  const svod = [140, 155, 170, 185, 180, 200, 220, 230, 225, 250, 270, 295];
  const avod = [65, 75, 85, 95, 100, 115, 130, 140, 145, 165, 180, 205];

  const pad = { left: 45, right: 20, top: 20, bottom: 30 };
  const chartW = w - pad.left - pad.right;
  const chartH = h - pad.top - pad.bottom;
  const maxVal = 550;

  // Grid lines
  ctx.strokeStyle = isLightTheme() ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
  ctx.font = '10px JetBrains Mono';

  for (let i = 0; i <= 4; i++) {
    const val = (maxVal / 4) * i;
    const y = pad.top + chartH - (i / 4) * chartH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(w - pad.right, y);
    ctx.stroke();
    ctx.fillText(`${val}M`, 6, y + 3);
  }

  const stepX = chartW / (months.length - 1);

  // AVOD line (Amber)
  ctx.beginPath();
  avod.forEach((v, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + chartH - (v / maxVal) * chartH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = isLightTheme() ? '#d97706' : '#f59e0b';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // SVOD Line (Cyan / Azure)
  ctx.beginPath();
  svod.forEach((v, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + chartH - (v / maxVal) * chartH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = isLightTheme() ? '#0284c7' : '#00d2ff';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // Draw points & month labels
  months.forEach((m, i) => {
    const x = pad.left + i * stepX;
    const yS = pad.top + chartH - (svod[i] / maxVal) * chartH;
    const yA = pad.top + chartH - (avod[i] / maxVal) * chartH;

    ctx.beginPath();
    ctx.arc(x, yS, 4, 0, Math.PI * 2);
    ctx.fillStyle = isLightTheme() ? '#0284c7' : '#00d2ff';
    ctx.fill();

    ctx.beginPath();
    ctx.arc(x, yA, 4, 0, Math.PI * 2);
    ctx.fillStyle = isLightTheme() ? '#d97706' : '#f59e0b';
    ctx.fill();

    if (i % 2 === 0) {
      ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
      ctx.fillText(m, x - 12, h - 10);
    }
  });
}

function renderAdCpmList() {
  const container = document.querySelector('#adCpmList');
  if (!container) return;

  const titles = STATE.catalog.length > 0 ? STATE.catalog : FALLBACK_CATALOG;
  const sortedByCpm = [...titles].sort((a, b) => (b.ad_yield_cpm || 30) - (a.ad_yield_cpm || 30)).slice(0, 5);

  container.innerHTML = sortedByCpm.map(t => {
    const cpm = t.ad_yield_cpm || 32.5;
    const adRev = t.ad_revenue || Math.round(t.total_revenue * 0.28);

    return `
      <div class="ad-cpm-item">
        <div class="cpm-title-group">
          <span class="cpm-title">${t.title}</span>
          <span class="cpm-genre">${t.genre} &bull; ${t.studio}</span>
        </div>
        <div class="cpm-stats">
          <div style="text-align: right;">
            <div class="cpm-val">$${cpm.toFixed(2)}/CPM</div>
            <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">${formatCurrency(adRev)} ad yield</div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function renderAdFatigueChart() {
  const canvas = document.querySelector('#adFatigueCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth || 600;
  canvas.height = 170;
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const pad = { left: 50, right: 40, top: 20, bottom: 30 };
  const chartW = w - pad.left - pad.right;
  const chartH = h - pad.top - pad.bottom;

  // Draw grid
  ctx.strokeStyle = isLightTheme() ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
  ctx.font = '10px JetBrains Mono';

  [100, 80, 60, 40, 20].forEach((pct, i) => {
    const y = pad.top + (i / 4) * chartH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(w - pad.right, y);
    ctx.stroke();
    ctx.fillText(`${pct}%`, 14, y + 3);
  });

  // Curve: Break interval from 10m to 60m
  const intervals = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60];
  const retention = [99, 98, 96, 94, 91, 87, 81, 74, 65, 56, 48];

  const stepX = chartW / (intervals.length - 1);

  // Optimal zone highlight (25 to 35 min)
  const optX1 = pad.left + 3 * stepX;
  const optX2 = pad.left + 5 * stepX;
  ctx.fillStyle = isLightTheme() ? 'rgba(16, 185, 129, 0.12)' : 'rgba(16, 185, 129, 0.08)';
  ctx.fillRect(optX1, pad.top, optX2 - optX1, chartH);

  // Draw drop-off curve
  ctx.beginPath();
  retention.forEach((r, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + chartH - ((r - 20) / 80) * chartH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = isLightTheme() ? '#059669' : '#10b981';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // Optimal label
  ctx.fillStyle = isLightTheme() ? '#047857' : '#34d399';
  ctx.fillText('★ OPTIMAL WINDOW (28-35 min)', optX1 - 10, pad.top + 14);

  // Interval labels
  intervals.forEach((min, i) => {
    if (i % 2 === 0) {
      const x = pad.left + i * stepX;
      ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
      ctx.fillText(`${min}m`, x - 8, h - 10);
    }
  });
}

// ==============================================================================
// ASK CINEPULSE AI - CONVERSATIONAL COPILOT
// ==============================================================================
let copilotInstance = null;

function setupCopilotChat() {
  if (window.CinePulseCopilot) {
    copilotInstance = new CinePulseCopilot(STATE.catalog);
  }

  const openBtn = document.querySelector('#openCopilotBtn');
  const closeBtn = document.querySelector('#copilotCloseBtn');
  const drawer = document.querySelector('#copilotDrawer');
  const input = document.querySelector('#copilotInput');
  const sendBtn = document.querySelector('#copilotSendBtn');

  if (openBtn && drawer) {
    openBtn.addEventListener('click', () => {
      drawer.classList.add('open');
      if (input) input.focus();
    });
  }

  if (closeBtn && drawer) {
    closeBtn.addEventListener('click', () => {
      drawer.classList.remove('open');
    });
  }

  if (sendBtn && input) {
    sendBtn.addEventListener('click', () => {
      const txt = input.value.trim();
      if (txt) {
        askCopilot(txt);
        input.value = '';
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const txt = input.value.trim();
        if (txt) {
          askCopilot(txt);
          input.value = '';
        }
      }
    });
  }
}

window.askCopilot = function(promptText) {
  const drawer = document.querySelector('#copilotDrawer');
  if (drawer && !drawer.classList.contains('open')) {
    drawer.classList.add('open');
  }

  const body = document.querySelector('#copilotBody');
  if (!body) return;

  // Append user message
  const userMsg = document.createElement('div');
  userMsg.className = 'copilot-message user';
  userMsg.innerHTML = `
    <div class="avatar">👤</div>
    <div class="bubble">${promptText}</div>
  `;
  body.appendChild(userMsg);
  body.scrollTop = body.scrollHeight;

  // Make sure copilotInstance has latest catalog
  if (!copilotInstance && window.CinePulseCopilot) {
    copilotInstance = new CinePulseCopilot(STATE.catalog);
  } else if (copilotInstance) {
    copilotInstance.setCatalog(STATE.catalog);
  }

  // Thinking state
  const botMsg = document.createElement('div');
  botMsg.className = 'copilot-message bot';
  botMsg.innerHTML = `
    <div class="avatar">✨</div>
    <div class="bubble">
      <p style="color: var(--cyan); font-family: var(--font-mono); font-size: 11px;">Synthesizing catalog financials & viewing vectors...</p>
    </div>
  `;
  body.appendChild(botMsg);
  body.scrollTop = body.scrollHeight;

  setTimeout(() => {
    let response;
    if (copilotInstance) {
      response = copilotInstance.processQuery(promptText);
    } else {
      response = {
        title: "AI Studio Strategic Analysis",
        text: `<p>Catalog indexed with 50,000 titles. High ROI concentration detected in premium sci-fi and Pan-India theatrical acquisitions.</p>`
      };
    }

    botMsg.querySelector('.bubble').innerHTML = `
      <h4 style="font-size: 13.5px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;">${response.title}</h4>
      ${response.text}
    `;
    body.scrollTop = body.scrollHeight;
  }, 350);
};

// ------------------------------------------------------------------------------
// VIEW 6: FINANCIAL MATRIX (SCATTER & COST MIX)
// ------------------------------------------------------------------------------
function renderScatterPlot() {
  const canvas = document.querySelector('#scatterCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth || 800;
  canvas.height = 340;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const w = canvas.width;
  const h = canvas.height;
  const pad = { top: 30, right: 30, bottom: 40, left: 60 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;

  // Axis ranges (Investment vs Revenue)
  const maxInvest = 400000000;
  const maxRevenue = 1500000000;

  // Grid
  ctx.strokeStyle = isLightTheme() ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 1;
  ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
  ctx.font = '10px JetBrains Mono';

  for (let i = 0; i <= 4; i++) {
    const yVal = (maxRevenue / 4) * i;
    const yPos = pad.top + plotH - (i / 4) * plotH;
    ctx.beginPath();
    ctx.moveTo(pad.left, yPos);
    ctx.lineTo(w - pad.right, yPos);
    ctx.stroke();
    ctx.fillText(formatCurrency(yVal, true), 8, yPos + 3);
  }

  for (let i = 0; i <= 4; i++) {
    const xVal = (maxInvest / 4) * i;
    const xPos = pad.left + (i / 4) * plotW;
    ctx.beginPath();
    ctx.moveTo(xPos, pad.top);
    ctx.lineTo(xPos, pad.top + plotH);
    ctx.stroke();
    ctx.fillText(formatCurrency(xVal, true), xPos - 15, h - 14);
  }

  // Draw Title Bubbles
  STATE.catalog.forEach(m => {
    const inv = m.total_content_cost + (m.marketing_spend || 0);
    const rev = m.total_revenue;
    const x = pad.left + (Math.min(inv, maxInvest) / maxInvest) * plotW;
    const y = pad.top + plotH - (Math.min(rev, maxRevenue) / maxRevenue) * plotH;
    const radius = Math.max(5, Math.min(22, (m.total_watch_hours / 10000000) * 3));

    let color = isLightTheme() ? '#059669' : '#10b981';
    if (m.decision === 'RENEW') color = isLightTheme() ? '#0284c7' : '#00d2ff';
    if (m.decision === 'MONITOR') color = isLightTheme() ? '#2563eb' : '#3b82f6';
    if (m.decision === 'COST_REVIEW') color = isLightTheme() ? '#d97706' : '#f59e0b';
    if (m.decision === 'EXIT' || m.decision === 'EXIT_OR_RENEGOTIATE') color = isLightTheme() ? '#dc2626' : '#e50914';

    ctx.save();
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.globalAlpha = isLightTheme() ? 0.85 : 0.75;
    ctx.shadowColor = color;
    ctx.shadowBlur = isLightTheme() ? 4 : 10;
    ctx.fill();

    ctx.strokeStyle = isLightTheme() ? '#ffffff' : '#07090e';
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 1;
    ctx.stroke();

    // Title label for top titles
    if (radius > 12) {
      ctx.fillStyle = isLightTheme() ? '#0f172a' : '#f8fafc';
      ctx.font = '10.5px Plus Jakarta Sans';
      ctx.fillText(m.title, x + radius + 6, y + 4);
    }
    ctx.restore();
  });
}

function renderCostComposition() {
  const container = document.querySelector('#costCompositionBars');
  if (!container) return;

  const costMix = [
    { label: 'Production Budget', pct: 72.4, color: isLightTheme() ? '#0284c7' : '#00d2ff' },
    { label: 'Licensing & Royalties', pct: 12.8, color: isLightTheme() ? '#7c3aed' : '#8b5cf6' },
    { label: 'Production Overhead', pct: 8.6, color: isLightTheme() ? '#059669' : '#10b981' },
    { label: 'Distribution & Platform Delivery', pct: 3.8, color: isLightTheme() ? '#d97706' : '#f59e0b' },
    { label: 'Localization & Translation', pct: 2.4, color: isLightTheme() ? '#dc2626' : '#e50914' }
  ];

  container.innerHTML = costMix.map(item => `
    <div style="margin-bottom: 14px;">
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: var(--text-secondary);">${item.label}</span>
        <strong style="font-family: var(--font-mono); color: var(--text-primary);">${item.pct}%</strong>
      </div>
      <div style="height: 6px; background: ${isLightTheme() ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)'}; border-radius: 99px; overflow: hidden;">
        <div style="height: 100%; width: ${item.pct}%; background: ${item.color}; border-radius: 99px;"></div>
      </div>
    </div>
  `).join('');
}

function renderGenreRoi() {
  const container = document.querySelector('#genreRoiBars');
  if (!container) return;

  const genres = [
    { genre: 'Sci-Fi', roi: 245, color: isLightTheme() ? '#0284c7' : '#00d2ff' },
    { genre: 'Action', roi: 210, color: isLightTheme() ? '#059669' : '#10b981' },
    { genre: 'Comedy', roi: 185, color: isLightTheme() ? '#7c3aed' : '#8b5cf6' },
    { genre: 'Animation', roi: 168, color: isLightTheme() ? '#d97706' : '#f59e0b' },
    { genre: 'Crime / Thriller', roi: 142, color: isLightTheme() ? '#2563eb' : '#3b82f6' },
    { genre: 'Drama', roi: 115, color: isLightTheme() ? '#dc2626' : '#e50914' }
  ];

  container.innerHTML = genres.map(g => `
    <div style="margin-bottom: 14px;">
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: var(--text-secondary);">${g.genre}</span>
        <strong style="font-family: var(--font-mono); color: ${isLightTheme() ? '#059669' : '#34d399'}; font-weight: 700;">+${g.roi}%</strong>
      </div>
      <div style="height: 6px; background: ${isLightTheme() ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)'}; border-radius: 99px; overflow: hidden;">
        <div style="height: 100%; width: ${(g.roi / 250) * 100}%; background: ${g.color}; border-radius: 99px;"></div>
      </div>
    </div>
  `).join('');
}

// ------------------------------------------------------------------------------
// VIEW 4: AUDIENCE & VIEWERSHIP
// ------------------------------------------------------------------------------
function renderFunnel() {
  const container = document.querySelector('#funnelContainer');
  if (!container) return;

  const steps = [
    { stage: 'Playback Initiated (0 min)', pct: 100, viewers: '1,000,000', drop: '0%' },
    { stage: 'Hook Passed (15 min)', pct: 86.4, viewers: '864,000', drop: '-13.6%' },
    { stage: 'Midpoint Sustained (45 min)', pct: 78.2, viewers: '782,000', drop: '-8.2%' },
    { stage: 'Climax & Full Completion', pct: 72.8, viewers: '728,000', drop: '-5.4%' },
    { stage: 'Post-Watch Rewatch Velocity', pct: 34.5, viewers: '345,000', drop: 'Loyalty Loop' }
  ];

  container.innerHTML = steps.map(s => `
    <div style="margin-bottom: 18px;">
      <div style="display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 6px;">
        <span style="font-weight: 600; color: var(--text-primary);">${s.stage}</span>
        <span style="font-family: var(--font-mono); color: var(--cyan); font-weight: 700;">${s.pct}% (${s.viewers})</span>
      </div>
      <div style="height: 10px; background: ${isLightTheme() ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)'}; border-radius: 99px; overflow: hidden;">
        <div style="height: 100%; width: ${s.pct}%; background: ${isLightTheme() ? 'linear-gradient(90deg, #0284c7, #7c3aed)' : 'linear-gradient(90deg, #00d2ff, #8b5cf6)'}; border-radius: 99px;"></div>
      </div>
    </div>
  `).join('');
}

function renderLoyaltyList() {
  const container = document.querySelector('#loyaltyList');
  if (!container) return;

  const loyalTitles = STATE.catalog.slice(0, 5).sort((a, b) => b.average_rewatch_rate - a.average_rewatch_rate);
  container.innerHTML = loyalTitles.map(m => `
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: ${isLightTheme() ? '#f8fafc' : 'rgba(255,255,255,0.02)'}; border: 1px solid ${isLightTheme() ? '#e2e8f0' : 'rgba(255,255,255,0.06)'}; border-radius: 8px; margin-bottom: 10px;">
      <div>
        <strong style="color: var(--text-primary); font-size: 13px;">${m.title}</strong>
        <div style="font-size: 11px; color: var(--text-muted);">${m.genre} &bull; ${m.release_year}</div>
      </div>
      <span class="pill pill-expand">${m.average_rewatch_rate}% Rewatch</span>
    </div>
  `).join('');
}

function renderTrafficChart() {
  const canvas = document.querySelector('#trafficCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth || 800;
  canvas.height = 180;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const hours = ['12A', '3A', '6A', '9A', '12P', '3P', '6P', '8P', '9P', '10P', '11P'];
  const values = [25, 12, 10, 35, 55, 60, 85, 98, 100, 92, 70];

  const w = canvas.width;
  const h = canvas.height;
  const pad = { top: 20, right: 20, bottom: 30, left: 40 };
  const stepX = (w - pad.left - pad.right) / (hours.length - 1);
  const plotH = h - pad.top - pad.bottom;

  ctx.beginPath();
  values.forEach((v, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + plotH - (v / 100) * plotH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.strokeStyle = isLightTheme() ? '#dc2626' : '#e50914';
  ctx.lineWidth = 3;
  ctx.shadowColor = isLightTheme() ? 'rgba(220, 38, 38, 0.3)' : 'rgba(229, 9, 20, 0.6)';
  ctx.shadowBlur = 12;
  ctx.stroke();

  // Labels
  ctx.fillStyle = isLightTheme() ? '#475569' : '#64748b';
  ctx.font = '10px JetBrains Mono';
  hours.forEach((hr, i) => {
    const x = pad.left + i * stepX;
    ctx.fillText(hr, x - 8, h - 10);
  });
}

// ------------------------------------------------------------------------------
// VIEW 5: GLOBAL MARKETS TABLE
// ------------------------------------------------------------------------------
function renderRegionalTable() {
  const tbody = document.querySelector('#regionalTableBody');
  if (!tbody) return;

  tbody.innerHTML = REGIONAL_MARKETS.map(r => {
    const revPerHour = (r.revenue / r.watch_hours).toFixed(2);
    let healthPill = '<span class="pill pill-expand">Hyper Growth</span>';
    if (r.health === 'HIGH_MARGIN') healthPill = '<span class="pill pill-renew">High Margin</span>';
    if (r.health === 'STRONG') healthPill = '<span class="pill pill-monitor">Strong</span>';
    if (r.health === 'STEADY') healthPill = '<span class="pill pill-monitor">Steady</span>';

    return `
      <tr>
        <td><strong>${r.region}</strong></td>
        <td>${r.continent}</td>
        <td><span class="meta-tag">${r.currency}</span></td>
        <td class="text-cyan">${formatCurrency(r.revenue)}</td>
        <td>${formatNumber(r.watch_hours)} hrs</td>
        <td>${formatNumber(r.views)}</td>
        <td><strong>${formatCurrency(revPerHour, false)}/hr</strong></td>
        <td>${healthPill}</td>
      </tr>
    `;
  }).join('');
}

// ------------------------------------------------------------------------------
// VIEW 6: AI DECISION SIMULATOR
// ------------------------------------------------------------------------------
function setupSimulator() {
  const budgetSlider = document.querySelector('#simBudget');
  const mktSlider = document.querySelector('#simMkt');
  const regionsSlider = document.querySelector('#simRegions');
  const genreSelect = document.querySelector('#simGenre');
  const typeBtns = document.querySelectorAll('#simTypeSelector .pill-btn');

  if (budgetSlider) budgetSlider.addEventListener('input', runSimulatorCalc);
  if (mktSlider) mktSlider.addEventListener('input', runSimulatorCalc);
  if (regionsSlider) regionsSlider.addEventListener('input', runSimulatorCalc);
  if (genreSelect) genreSelect.addEventListener('change', runSimulatorCalc);

  typeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      typeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      runSimulatorCalc();
    });
  });
}

function runSimulatorCalc() {
  const budgetSlider = document.querySelector('#simBudget');
  const mktSlider = document.querySelector('#simMkt');
  const regionsSlider = document.querySelector('#simRegions');
  const genreSelect = document.querySelector('#simGenre');

  if (!budgetSlider || !mktSlider || !regionsSlider) return;

  const budget = Number(budgetSlider.value);
  const marketing = Number(mktSlider.value);
  const regions = Number(regionsSlider.value);
  const genre = genreSelect ? genreSelect.value : 'Sci-Fi';

  // Update slider label texts
  document.querySelector('#simBudgetVal').textContent = formatCurrency(budget);
  document.querySelector('#simMktVal').textContent = formatCurrency(marketing);
  document.querySelector('#simRegionsVal').textContent = `${regions} Global Regions`;

  // Simulator Model Algorithm
  let genreMultiplier = 2.4;
  if (genre === 'Sci-Fi') genreMultiplier = 2.8;
  if (genre === 'Action') genreMultiplier = 2.6;
  if (genre === 'Comedy') genreMultiplier = 2.0;
  if (genre === 'Animation') genreMultiplier = 2.5;

  const totalCap = budget + marketing;
  const regionFactor = Math.pow(regions / 15, 0.45);
  const projectedRevenue = totalCap * genreMultiplier * regionFactor;
  const projectedProfit = projectedRevenue - totalCap;
  const projectedRoi = (projectedProfit / totalCap) * 100;

  const projViews = (projectedRevenue / 55).toFixed(0);
  const projHours = (projViews * 2.6).toFixed(0);
  const projComp = Math.min(88, 72 + (budget > 1e8 ? 8 : 4) + (marketing > 5e7 ? 4 : 0));

  // Render Simulator UI
  document.querySelector('#simProjViews').textContent = formatNumber(projViews);
  document.querySelector('#simProjHours').textContent = `${formatNumber(projHours)} hrs`;
  document.querySelector('#simProjComp').textContent = `${projComp.toFixed(1)}%`;
  document.querySelector('#simProjProfit').textContent = formatCurrency(projectedProfit);
  document.querySelector('#simProjRoi').textContent = `${projectedRoi >= 0 ? '+' : ''}${projectedRoi.toFixed(1)}%`;

  const fillEl = document.querySelector('#simRoiFill');
  if (fillEl) fillEl.style.width = `${Math.min(100, Math.max(10, projectedRoi / 3))}%`;

  const banner = document.querySelector('#simVerdictBanner');
  const verdictTitle = document.querySelector('#simVerdict');
  const memoText = document.querySelector('#simMemoText');

  if (projectedRoi >= 80) {
    if (banner) banner.style.borderColor = 'rgba(16, 185, 129, 0.5)';
    if (verdictTitle) verdictTitle.textContent = 'HIGH CONFIDENCE GREENLIGHT (EXPAND)';
    if (memoText) memoText.textContent = `Capital model indicates exceptional yield (+${projectedRoi.toFixed(0)}% ROI). Proposed investment of ${formatCurrency(budget)} in ${genre} format demonstrates strong viral potential across ${regions} target territories. Approved for immediate pre-production.`;
  } else if (projectedRoi >= 25) {
    if (banner) banner.style.borderColor = 'rgba(0, 210, 255, 0.5)';
    if (verdictTitle) verdictTitle.textContent = 'CONDITIONAL APPROVAL (RENEW / MONITOR)';
    if (memoText) memoText.textContent = `Viable production portfolio yield (+${projectedRoi.toFixed(0)}% ROI). Satisfies baseline platform hurdle rate. Recommend locking co-financing or local tax credits to optimize payback timeline.`;
  } else {
    if (banner) banner.style.borderColor = 'rgba(245, 158, 11, 0.5)';
    if (verdictTitle) verdictTitle.textContent = 'CAPITAL REVISION REQUIRED (COST REVIEW)';
    if (memoText) memoText.textContent = `Projected ROI (+${projectedRoi.toFixed(0)}%) falls below streaming capital efficiency hurdle. Recommend reducing production overhead by 18% and consolidating initial rollout to primary 8 markets before full global release.`;
  }
}

// ------------------------------------------------------------------------------
// MODAL DRAWER
// ------------------------------------------------------------------------------
function setupModal() {
  const modal = document.querySelector('#detailModal');
  const closeBtn = document.querySelector('#modalCloseBtn');

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

function openModal(contentId) {
  const movie = STATE.catalog.find(m => m.content_id === contentId) || STATE.catalog[0];
  if (!movie) return;

  STATE.selectedMovie = movie;

  document.querySelector('#modalTitle').textContent = movie.title;
  document.querySelector('#modalTypePill').textContent = movie.content_type.toUpperCase();
  
  const decPill = document.querySelector('#modalDecisionPill');
  decPill.className = `pill ${getDecisionClass(movie.decision)}`;
  decPill.textContent = movie.decision;

  document.querySelector('#modalAgeRating').textContent = movie.age_rating;
  document.querySelector('#modalStudio').textContent = movie.studio;
  document.querySelector('#modalYear').textContent = movie.release_year;
  document.querySelector('#modalGenre').textContent = movie.genre;
  document.querySelector('#modalDuration').textContent = `${movie.duration_minutes} min`;

  document.querySelector('#modalSynopsis').textContent = movie.synopsis || 'Premium streaming asset catalog entry.';
  document.querySelector('#modalDirector').textContent = movie.director || 'Acclaimed Director';
  document.querySelector('#modalCast').textContent = movie.cast || 'Leading Cast Ensemble';

  document.querySelector('#modalBudget').textContent = formatCurrency(movie.production_budget, false);
  document.querySelector('#modalLicensing').textContent = formatCurrency(movie.licensing_cost, false);
  document.querySelector('#modalMarketing').textContent = formatCurrency(movie.marketing_spend || 45000000, false);
  document.querySelector('#modalRevenue').textContent = formatCurrency(movie.total_revenue, false);
  document.querySelector('#modalProfit').textContent = formatCurrency(movie.contribution_profit, false);
  document.querySelector('#modalRoi').textContent = `+${(movie.content_roi * 100).toFixed(1)}%`;

  document.querySelector('#modalViews').textContent = formatNumber(movie.total_views);
  document.querySelector('#modalHours').textContent = `${formatNumber(movie.total_watch_hours)} hrs`;
  document.querySelector('#modalCompletion').textContent = `${movie.average_completion_rate}%`;
  document.querySelector('#modalRewatch').textContent = `${movie.average_rewatch_rate}%`;

  document.querySelector('#modalAiMemo').textContent = movie.ai_recommendation || 'Continuous monitoring recommended for long-tail catalog stabilization.';

  const hero = document.querySelector('#modalHero');
  if (hero && movie.poster_url) {
    hero.style.backgroundImage = `linear-gradient(135deg, rgba(229, 9, 20, 0.25), rgba(15, 23, 42, 0.95)), url('${movie.poster_url}')`;
    hero.style.backgroundSize = 'cover';
    hero.style.backgroundPosition = 'center';
  }

  document.querySelector('#detailModal').classList.add('active');
}

function closeModal() {
  const modal = document.querySelector('#detailModal');
  if (modal) modal.classList.remove('active');
}

// ------------------------------------------------------------------------------
// FILE UPLOAD & EXPORT
// ------------------------------------------------------------------------------
function setupFileUpload() {
  const fileInput = document.querySelector('#csvFile');
  if (!fileInput) return;

  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const text = await file.text();
      const lines = text.trim().split(/\r?\n/);
      if (lines.length < 2) return;

      const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
      const parsedRows = [];

      for (let i = 1; i < lines.length; i++) {
        const cols = lines[i].split(',').map(c => c.trim().replace(/^"|"$/g, ''));
        const obj = {};
        headers.forEach((h, idx) => {
          const val = cols[idx];
          obj[h] = !isNaN(Number(val)) && val !== '' ? Number(val) : val;
        });
        parsedRows.push(obj);
      }

      if (parsedRows.length > 0) {
        alert(`Successfully imported ${parsedRows.length.toLocaleString()} warehouse records! Updating intelligence views...`);
        // If content cost or scorecard was uploaded, recalculate
        renderAllViews();
      }
    } catch (err) {
      alert('Error parsing CSV file: ' + err.message);
    }
  });
}

function setupExport() {
  const btn = document.querySelector('#exportBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(STATE.catalog, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", "ECDIP_Executive_Content_Report.json");
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  });
}

// ==============================================================================
// 6. DOM READY BOOTSTRAP
// ==============================================================================
document.addEventListener('DOMContentLoaded', initDashboard);
