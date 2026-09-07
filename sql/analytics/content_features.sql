-- ==========================================================
-- ECDIP - CONTENT FEATURE ENGINEERING ENGINE
-- ==========================================================
--
-- Purpose:
-- Transform business KPIs into ML / scoring / decision
-- intelligence features.
--
-- Target:
-- ~40-50 engineered signals
--
-- Source:
-- vw_content_kpis
--
-- Downstream:
-- Content Health Score
-- Forecasting
-- Decision Engine
-- Recommendation Engine
-- Scenario Simulation
-- ==========================================================


DROP VIEW IF EXISTS vw_content_features CASCADE;


CREATE VIEW vw_content_features AS

WITH base AS (

    SELECT
        *
    FROM vw_content_kpis
),


-- ==========================================================
-- 1. NORMALIZED PORTFOLIO FEATURES
-- ==========================================================

ranked AS (

    SELECT

        b.*,

        -- --------------------------------------------------
        -- Financial percentile features
        -- --------------------------------------------------

        PERCENT_RANK() OVER (
            ORDER BY content_roi
        ) AS roi_percentile,

        PERCENT_RANK() OVER (
            ORDER BY contribution_profit
        ) AS profit_percentile,

        PERCENT_RANK() OVER (
            ORDER BY total_revenue
        ) AS revenue_percentile,

        PERCENT_RANK() OVER (
            ORDER BY profit_margin
        ) AS margin_percentile,

        -- --------------------------------------------------
        -- Engagement percentile features
        -- --------------------------------------------------

        PERCENT_RANK() OVER (
            ORDER BY average_completion_rate
        ) AS completion_percentile,

        PERCENT_RANK() OVER (
            ORDER BY average_rewatch_rate
        ) AS rewatch_percentile,

        PERCENT_RANK() OVER (
            ORDER BY engagement_quality_score
        ) AS engagement_percentile,

        -- --------------------------------------------------
        -- Marketing percentile
        -- --------------------------------------------------

        PERCENT_RANK() OVER (
            ORDER BY average_campaign_roi
        ) AS marketing_roi_percentile,

        PERCENT_RANK() OVER (
            ORDER BY conversion_rate
        ) AS conversion_percentile,

        -- --------------------------------------------------
        -- Reach percentile
        -- --------------------------------------------------

        PERCENT_RANK() OVER (
            ORDER BY available_regions
        ) AS regional_reach_percentile

    FROM base b
),


-- ==========================================================
-- 2. ENGINEERED BUSINESS FEATURES
-- ==========================================================

features AS (

    SELECT

        r.*,


        -- ==================================================
        -- FINANCIAL FEATURES
        -- ==================================================

        CASE
            WHEN total_investment = 0
            THEN 0
            ELSE contribution_profit
                 / total_investment
        END AS investment_profitability,

        CASE
            WHEN total_revenue = 0
            THEN 0
            ELSE total_content_cost
                 / total_revenue
        END AS content_cost_pressure,

        CASE
            WHEN total_revenue = 0
            THEN 0
            ELSE total_marketing_spend
                 / total_revenue
        END AS marketing_cost_pressure,

        CASE
            WHEN total_investment = 0
            THEN 0
            ELSE total_marketing_spend
                 / total_investment
        END AS marketing_dependency,

        CASE
            WHEN total_revenue = 0
            THEN 0
            ELSE contribution_profit
                 / total_revenue
        END AS profit_generation_efficiency,


        -- ==================================================
        -- REVENUE MIX FEATURES
        -- ==================================================

        GREATEST(
            subscription_revenue_share,
            advertising_revenue_share
        ) AS dominant_revenue_channel,

        LEAST(
            subscription_revenue_share,
            advertising_revenue_share
        ) AS secondary_revenue_channel,

        (
            1
            -
            ABS(
                subscription_revenue_share
                -
                advertising_revenue_share
            )
        ) AS revenue_diversification_score,


        -- ==================================================
        -- MARKETING FEATURES
        -- ==================================================

        CASE
            WHEN total_marketing_spend = 0
            THEN 0
            ELSE total_revenue
                 / total_marketing_spend
        END AS revenue_per_marketing_unit,

        CASE
            WHEN total_clicks = 0
            THEN 0
            ELSE total_conversions::NUMERIC
                 / total_clicks
        END AS conversion_efficiency,

        CASE
            WHEN total_impressions = 0
            THEN 0
            ELSE total_conversions::NUMERIC
                 / total_impressions
        END AS impression_to_conversion_rate,


        -- ==================================================
        -- AUDIENCE QUALITY FEATURES
        -- ==================================================

        (
            COALESCE(
                average_watch_percentage,
                0
            )
            * 0.40
            +
            COALESCE(
                average_completion_rate,
                0
            )
            * 0.35
            +
            COALESCE(
                average_rewatch_rate,
                0
            )
            * 0.25
        ) AS audience_quality_score,


        (
            COALESCE(
                average_completion_rate,
                0
            )
            +
            COALESCE(
                average_rewatch_rate,
                0
            )
        ) / 2.0 AS retention_engagement_signal,


        CASE
            WHEN average_completion_rate >= 0.70
             AND average_rewatch_rate >= 0.20
            THEN 1
            ELSE 0
        END AS strong_audience_signal,


        -- ==================================================
        -- CONTENT QUALITY FEATURES
        -- ==================================================

        CASE
            WHEN imdb_rating >= 8.0
            THEN 1
            ELSE 0
        END AS premium_quality_flag,

        CASE
            WHEN imdb_rating >= 7.0
            THEN 1
            ELSE 0
        END AS strong_quality_flag,

        CASE
            WHEN imdb_rating < 6.0
            THEN 1
            ELSE 0
        END AS weak_quality_flag,


        -- ==================================================
        -- COST RISK FEATURES
        -- ==================================================

        CASE
            WHEN total_content_cost > total_revenue
            THEN 1
            ELSE 0
        END AS content_cost_risk_flag,

        CASE
            WHEN total_marketing_spend > total_revenue
            THEN 1
            ELSE 0
        END AS marketing_cost_risk_flag,

        CASE
            WHEN total_investment > total_revenue
            THEN 1
            ELSE 0
        END AS investment_recovery_risk_flag,


        -- ==================================================
        -- PROFITABILITY RISK
        -- ==================================================

        CASE
            WHEN content_roi < 0
            THEN 1
            ELSE 0
        END AS negative_roi_risk,

        CASE
            WHEN profit_margin < 0
            THEN 1
            ELSE 0
        END AS negative_margin_risk,

        CASE
            WHEN content_roi < 0
             AND average_completion_rate < 0.50
            THEN 1
            ELSE 0
        END AS high_business_risk,


        -- ==================================================
        -- ENGAGEMENT RISK
        -- ==================================================

        CASE
            WHEN average_completion_rate < 0.50
            THEN 1
            ELSE 0
        END AS weak_completion_risk,

        CASE
            WHEN average_rewatch_rate < 0.10
            THEN 1
            ELSE 0
        END AS weak_rewatch_risk,

        CASE
            WHEN engagement_quality_score < 0.50
            THEN 1
            ELSE 0
        END AS weak_engagement_risk,


        -- ==================================================
        -- MARKETING RISK
        -- ==================================================

        CASE
            WHEN average_campaign_roi < 0
            THEN 1
            ELSE 0
        END AS negative_marketing_roi_risk,

        CASE
            WHEN conversion_rate < 0.05
            THEN 1
            ELSE 0
        END AS weak_conversion_risk,


        -- ==================================================
        -- REGIONAL FEATURES
        -- ==================================================

        CASE
            WHEN available_regions >= 10
            THEN 1
            ELSE 0
        END AS broad_regional_reach_flag,

        CASE
            WHEN available_regions <= 3
            THEN 1
            ELSE 0
        END AS concentrated_regional_reach_flag,


        -- ==================================================
        -- BUSINESS STRENGTH SIGNALS
        -- ==================================================

        CASE
            WHEN content_roi >= 0.50
             AND profit_margin >= 0.20
            THEN 1
            ELSE 0
        END AS strong_financial_signal,

        CASE
            WHEN average_completion_rate >= 0.70
             AND average_rewatch_rate >= 0.20
            THEN 1
            ELSE 0
        END AS strong_engagement_signal,

        CASE
            WHEN average_campaign_roi >= 1.00
             AND conversion_rate >= 0.10
            THEN 1
            ELSE 0
        END AS strong_marketing_signal,


        -- ==================================================
        -- STRATEGIC SIGNALS
        -- ==================================================

        CASE
            WHEN
                content_roi >= 0.50
                AND average_completion_rate >= 0.70
                AND average_campaign_roi >= 1.00
            THEN 1
            ELSE 0
        END AS expansion_candidate_flag,


        CASE
            WHEN
                content_roi >= 0.15
                AND average_completion_rate >= 0.60
            THEN 1
            ELSE 0
        END AS renewal_candidate_flag,


        CASE
            WHEN
                content_roi < 0
                AND average_completion_rate < 0.50
            THEN 1
            ELSE 0
        END AS exit_candidate_flag,


        CASE
            WHEN
                content_roi < 0
                AND average_campaign_roi < 0
            THEN 1
            ELSE 0
        END AS cost_optimization_candidate_flag,


        -- ==================================================
        -- PORTFOLIO POSITION FEATURES
        -- ==================================================

        (
            roi_percentile * 0.25
            +
            profit_percentile * 0.20
            +
            revenue_percentile * 0.15
            +
            margin_percentile * 0.15
            +
            engagement_percentile * 0.15
            +
            marketing_roi_percentile * 0.10
        ) AS portfolio_strength_score,


        (
            completion_percentile * 0.40
            +
            rewatch_percentile * 0.30
            +
            engagement_percentile * 0.30
        ) AS audience_strength_score,


        (
            marketing_roi_percentile * 0.60
            +
            conversion_percentile * 0.40
        ) AS marketing_strength_score,


        -- ==================================================
        -- DECISION READINESS
        -- ==================================================

        (
            roi_percentile * 0.25
            +
            profit_percentile * 0.20
            +
            engagement_percentile * 0.20
            +
            marketing_roi_percentile * 0.15
            +
            completion_percentile * 0.10
            +
            revenue_percentile * 0.10
        ) AS decision_readiness_score

    FROM ranked r
)


-- ==========================================================
-- FINAL FEATURE OUTPUT
-- ==========================================================

SELECT

    content_id,

    title,

    content_type,

    genre_id,

    studio_id,

    release_year,

    imdb_rating,

    is_original,

    available_regions,


    -- ------------------------------------------------------
    -- ORIGINAL KPIs
    -- ------------------------------------------------------

    total_revenue,
    total_content_cost,
    total_marketing_spend,
    total_investment,
    contribution_profit,
    content_roi,
    profit_margin,

    average_completion_rate,
    average_rewatch_rate,
    engagement_quality_score,

    average_campaign_roi,
    conversion_rate,


    -- ------------------------------------------------------
    -- FINANCIAL FEATURES
    -- ------------------------------------------------------

    investment_profitability,
    content_cost_pressure,
    marketing_cost_pressure,
    marketing_dependency,
    profit_generation_efficiency,


    -- ------------------------------------------------------
    -- REVENUE FEATURES
    -- ------------------------------------------------------

    dominant_revenue_channel,
    secondary_revenue_channel,
    revenue_diversification_score,


    -- ------------------------------------------------------
    -- MARKETING FEATURES
    -- ------------------------------------------------------

    revenue_per_marketing_unit,
    conversion_efficiency,
    impression_to_conversion_rate,


    -- ------------------------------------------------------
    -- AUDIENCE FEATURES
    -- ------------------------------------------------------

    audience_quality_score,
    retention_engagement_signal,
    strong_audience_signal,


    -- ------------------------------------------------------
    -- QUALITY FEATURES
    -- ------------------------------------------------------

    premium_quality_flag,
    strong_quality_flag,
    weak_quality_flag,


    -- ------------------------------------------------------
    -- RISK FEATURES
    -- ------------------------------------------------------

    content_cost_risk_flag,
    marketing_cost_risk_flag,
    investment_recovery_risk_flag,

    negative_roi_risk,
    negative_margin_risk,
    high_business_risk,

    weak_completion_risk,
    weak_rewatch_risk,
    weak_engagement_risk,

    negative_marketing_roi_risk,
    weak_conversion_risk,


    -- ------------------------------------------------------
    -- REGIONAL FEATURES
    -- ------------------------------------------------------

    broad_regional_reach_flag,
    concentrated_regional_reach_flag,


    -- ------------------------------------------------------
    -- BUSINESS STRENGTH
    -- ------------------------------------------------------

    strong_financial_signal,
    strong_engagement_signal,
    strong_marketing_signal,


    -- ------------------------------------------------------
    -- STRATEGIC FEATURES
    -- ------------------------------------------------------

    expansion_candidate_flag,
    renewal_candidate_flag,
    exit_candidate_flag,
    cost_optimization_candidate_flag,


    -- ------------------------------------------------------
    -- PORTFOLIO FEATURES
    -- ------------------------------------------------------

    roi_percentile,
    profit_percentile,
    revenue_percentile,
    margin_percentile,

    completion_percentile,
    rewatch_percentile,
    engagement_percentile,

    marketing_roi_percentile,
    conversion_percentile,
    regional_reach_percentile,


    portfolio_strength_score,
    audience_strength_score,
    marketing_strength_score,

    decision_readiness_score,


    -- ------------------------------------------------------
    -- EXISTING DECISION
    -- ------------------------------------------------------

    profitability_class,
    preliminary_decision

FROM features;