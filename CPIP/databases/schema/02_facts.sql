-- ==========================================================
-- ECDIP - Fact tables
--
-- This contract intentionally mirrors the CSV headers produced by
-- scripts/generate_*.py. The loader copies only CSV columns, so generated
-- keys and timestamps are declared explicitly here.
-- ==========================================================

CREATE TABLE fact_viewing_events (
    viewing_id BIGINT PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    platform_id INTEGER NOT NULL REFERENCES dim_platform(platform_id),
    plan_id INTEGER NOT NULL REFERENCES dim_subscription_plan(plan_id),
    date_id DATE NOT NULL REFERENCES dim_calendar(date_id),
    watch_hours NUMERIC(10,2) NOT NULL,
    completion_rate NUMERIC(5,2),
    rewatch_count INTEGER NOT NULL DEFAULT 0,
    pause_count INTEGER NOT NULL DEFAULT 0,
    search_before_watch BOOLEAN,
    marketing_influenced BOOLEAN,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_content_cost (
    content_id INTEGER PRIMARY KEY REFERENCES dim_content(content_id),
    production_budget NUMERIC(15,2) NOT NULL,
    licensing_cost NUMERIC(15,2) NOT NULL,
    available_regions INTEGER NOT NULL,
    production_overhead NUMERIC(15,2) NOT NULL,
    distribution_cost NUMERIC(15,2) NOT NULL,
    technology_cost NUMERIC(15,2) NOT NULL,
    localization_cost NUMERIC(15,2) NOT NULL,
    contract_administration_cost NUMERIC(15,2) NOT NULL,
    contingency_cost NUMERIC(15,2) NOT NULL,
    total_content_cost NUMERIC(15,2) NOT NULL,
    licensing_cost_ratio NUMERIC(8,4) NOT NULL,
    production_cost_ratio NUMERIC(8,4) NOT NULL,
    localization_cost_per_region NUMERIC(15,2) NOT NULL
);

CREATE TABLE fact_marketing (
    marketing_id BIGINT PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES dim_campaign(campaign_id),
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    impressions BIGINT NOT NULL,
    clicks BIGINT NOT NULL,
    conversions BIGINT NOT NULL,
    marketing_views BIGINT NOT NULL,
    attributed_watch_hours NUMERIC(15,2) NOT NULL,
    attributed_completion_rate NUMERIC(5,2) NOT NULL,
    marketing_spend NUMERIC(15,2) NOT NULL,
    attributed_revenue NUMERIC(15,2) NOT NULL,
    acquisition_cost NUMERIC(15,2) NOT NULL,
    marketing_roi NUMERIC(15,4) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_subscription_events (
    subscription_event_id BIGINT PRIMARY KEY,
    subscriber_id INTEGER NOT NULL REFERENCES dim_subscriber(subscriber_id),
    plan_id INTEGER NOT NULL REFERENCES dim_subscription_plan(plan_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    date_id DATE NOT NULL REFERENCES dim_calendar(date_id),
    event_type VARCHAR(50) NOT NULL,
    event_value NUMERIC(15,2) NOT NULL,
    tenure_months INTEGER NOT NULL,
    churn_flag BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_search_events (
    search_event_id BIGINT PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    date_id DATE NOT NULL REFERENCES dim_calendar(date_id),
    query_type VARCHAR(50) NOT NULL,
    search_intensity INTEGER NOT NULL,
    result_clicked BOOLEAN NOT NULL,
    watch_after_search BOOLEAN NOT NULL,
    search_abandoned BOOLEAN NOT NULL,
    search_relevance_score NUMERIC(5,2) NOT NULL,
    search_to_watch BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_engagement (
    engagement_id BIGINT PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    date_id DATE NOT NULL REFERENCES dim_calendar(date_id),
    likes INTEGER NOT NULL,
    dislikes INTEGER NOT NULL,
    average_watch_percentage NUMERIC(5,2) NOT NULL,
    completion_rate NUMERIC(5,2) NOT NULL,
    rewatch_rate NUMERIC(5,2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_revenue (
    revenue_id BIGINT PRIMARY KEY,
    viewing_id BIGINT NOT NULL REFERENCES fact_viewing_events(viewing_id),
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    region_id INTEGER NOT NULL REFERENCES dim_region(region_id),
    plan_id INTEGER NOT NULL REFERENCES dim_subscription_plan(plan_id),
    date_id DATE NOT NULL REFERENCES dim_calendar(date_id),
    revenue_type VARCHAR(100) NOT NULL,
    revenue_amount NUMERIC(15,2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE fact_forecast (
    forecast_id BIGINT PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES dim_content(content_id),
    forecast_date DATE NOT NULL,
    forecast_horizon_day INTEGER NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    forecast_value NUMERIC(18,4) NOT NULL,
    lower_bound NUMERIC(18,4) NOT NULL,
    upper_bound NUMERIC(18,4) NOT NULL,
    trend VARCHAR(50) NOT NULL,
    confidence NUMERIC(8,4) NOT NULL,
    model_method VARCHAR(100) NOT NULL,
    history_days INTEGER NOT NULL,
    r_squared NUMERIC(8,4) NOT NULL,
    momentum NUMERIC(18,4) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
