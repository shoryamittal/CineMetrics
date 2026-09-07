-- ==========================================================
-- Enterprise Content Decision Intelligence Platform (ECDIP)
-- Dimension Tables
-- ==========================================================

CREATE TABLE dim_content (
    content_id SERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    content_type VARCHAR(20) NOT NULL,

    genre_id INTEGER,

    studio_id INTEGER,

    release_year INTEGER,

    language VARCHAR(50),

    duration_minutes INTEGER,

    age_rating VARCHAR(20),

    imdb_rating NUMERIC(3,1),

    production_budget DECIMAL(15,2),

    licensing_cost DECIMAL(15,2),

    available_regions INTEGER,

    is_original BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ==========================================================
-- Dimension: Genre
-- ==========================================================

CREATE TABLE dim_genre (
    genre_id SERIAL PRIMARY KEY,

    genre_name VARCHAR(100) NOT NULL UNIQUE,

    genre_description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ==========================================================
-- Dimension: Studio
-- ==========================================================

CREATE TABLE dim_studio (
    studio_id SERIAL PRIMARY KEY,

    studio_name VARCHAR(200) NOT NULL UNIQUE,

    headquarters_country VARCHAR(100),

    founded_year INTEGER CHECK (founded_year >= 1900),

    website VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ==========================================================
-- Dimension: Region
-- ==========================================================

CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,

    country_name VARCHAR(100) NOT NULL,

    region_name VARCHAR(100),

    continent VARCHAR(50),

    currency VARCHAR(20),

    timezone VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Contract
-- ==========================================================

CREATE TABLE dim_contract (
    contract_id SERIAL PRIMARY KEY,

    contract_number VARCHAR(100) UNIQUE NOT NULL,

    contract_type VARCHAR(100) NOT NULL,

    contract_start DATE NOT NULL,

    contract_end DATE NOT NULL,

    licensing_model VARCHAR(100),

    licensing_cost DECIMAL(15,2) NOT NULL,

    renewal_cost DECIMAL(15,2),

    auto_renew BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Platform
-- ==========================================================

CREATE TABLE dim_platform (
    platform_id SERIAL PRIMARY KEY,

    platform_name VARCHAR(100) NOT NULL UNIQUE,

    headquarters VARCHAR(100),

    launch_year INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Subscription Plan
-- ==========================================================

CREATE TABLE dim_subscription_plan (
    plan_id SERIAL PRIMARY KEY,

    plan_name VARCHAR(100) NOT NULL UNIQUE,

    monthly_price DECIMAL(10,2) NOT NULL,

    max_devices INTEGER,

    video_quality VARCHAR(20),

    ads_supported BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Calendar
-- ==========================================================

CREATE TABLE dim_calendar (
    date_id DATE PRIMARY KEY,

    day INTEGER NOT NULL,

    month INTEGER NOT NULL,

    quarter INTEGER NOT NULL,

    year INTEGER NOT NULL,

    week_of_year INTEGER,

    day_name VARCHAR(20),

    month_name VARCHAR(20),

    is_weekend BOOLEAN
);

-- ==========================================================
-- Dimension: Campaign
-- ==========================================================

CREATE TABLE dim_campaign (
    campaign_id SERIAL PRIMARY KEY,

    campaign_name VARCHAR(255) NOT NULL,

    campaign_type VARCHAR(100),

    campaign_channel VARCHAR(100),

    start_date DATE,

    end_date DATE,

    budget DECIMAL(15,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Language
-- ==========================================================

CREATE TABLE dim_language (
    language_id SERIAL PRIMARY KEY,

    language_name VARCHAR(100) NOT NULL UNIQUE,

    language_code VARCHAR(10) UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- Dimension: Age Rating
-- ==========================================================

CREATE TABLE dim_age_rating (
    age_rating_id SERIAL PRIMARY KEY,

    rating_code VARCHAR(20) NOT NULL UNIQUE,

    description VARCHAR(255),

    minimum_age INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

