-- ==========================================================
-- ECDIP - CONTENT HEALTH SCORE ENGINE
-- ==========================================================
--
-- Converts engineered business signals into an explainable
-- 0-100 Content Health Score.
--
-- Components:
-- Financial Health       30%
-- Audience Health        25%
-- Marketing Health       15%
-- Growth/Portfolio       15%
-- Risk                   15%
--
-- ==========================================================


DROP VIEW IF EXISTS vw_content_health_score CASCADE;


CREATE VIEW vw_content_health_score AS

WITH scoring AS (

    SELECT

        f.*,


        -- ==================================================
        -- 1. FINANCIAL HEALTH - 30%
        -- ==================================================

        (
            COALESCE(f.roi_percentile, 0) * 0.40
            +
            COALESCE(f.margin_percentile, 0) * 0.30
            +
            COALESCE(f.profit_percentile, 0) * 0.30
        ) AS financial_health,


        -- ==================================================
        -- 2. AUDIENCE HEALTH - 25%
        -- ==================================================

        (
            COALESCE(f.completion_percentile, 0) * 0.40
            +
            COALESCE(f.rewatch_percentile, 0) * 0.25
            +
            COALESCE(f.engagement_percentile, 0) * 0.35
        ) AS audience_health,


        -- ==================================================
        -- 3. MARKETING HEALTH - 15%
        -- ==================================================

        (
            COALESCE(f.marketing_roi_percentile, 0) * 0.50
            +
            COALESCE(f.conversion_percentile, 0) * 0.30
            +
            COALESCE(f.revenue_percentile, 0) * 0.20
        ) AS marketing_health,


        -- ==================================================
        -- 4. PORTFOLIO / STRATEGIC HEALTH - 15%
        -- ==================================================

        (
            COALESCE(f.portfolio_strength_score, 0) * 0.60
            +
            COALESCE(f.revenue_percentile, 0) * 0.20
            +
            COALESCE(f.regional_reach_percentile, 0) * 0.20
        ) AS strategic_health,


        -- ==================================================
        -- 5. RISK PENALTY
        -- ==================================================

        (
            CASE
                WHEN f.negative_roi_risk = 1
                THEN 0.30
                ELSE 0
            END

            +

            CASE
                WHEN f.negative_margin_risk = 1
                THEN 0.20
                ELSE 0
            END

            +

            CASE
                WHEN f.weak_completion_risk = 1
                THEN 0.15
                ELSE 0
            END

            +

            CASE
                WHEN f.weak_engagement_risk = 1
                THEN 0.15
                ELSE 0
            END

            +

            CASE
                WHEN f.negative_marketing_roi_risk = 1
                THEN 0.10
                ELSE 0
            END

            +

            CASE
                WHEN f.investment_recovery_risk_flag = 1
                THEN 0.10
                ELSE 0
            END

        ) AS risk_penalty

    FROM vw_content_features f
),


-- ==========================================================
-- FINAL SCORE
-- ==========================================================

health AS (

    SELECT

        s.*,


        (
            (
                s.financial_health * 0.30
                +
                s.audience_health * 0.25
                +
                s.marketing_health * 0.15
                +
                s.strategic_health * 0.15
                +
                (1 - s.risk_penalty) * 0.15
            )
            * 100
        ) AS raw_health_score

    FROM scoring s
)


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


    -- ======================================================
    -- SCORE COMPONENTS
    -- ======================================================

    ROUND(
        (financial_health * 100)::numeric,
        2
    ) AS financial_health_score,

    ROUND(
        (audience_health * 100)::numeric,
        2
    ) AS audience_health_score,

    ROUND(
        (marketing_health * 100)::numeric,
        2
    ) AS marketing_health_score,

    ROUND(
        (strategic_health * 100)::numeric,
        2
    ) AS strategic_health_score,

    ROUND(
        (risk_penalty * 100)::numeric,
        2
    ) AS risk_penalty_score,


    -- ======================================================
    -- FINAL HEALTH SCORE
    -- ======================================================

    ROUND(
        GREATEST(
            0,
            LEAST(
                100,
                raw_health_score
            )
        )::numeric,
        2
    ) AS content_health_score,


    -- ======================================================
    -- HEALTH CLASSIFICATION
    -- ======================================================

    CASE

        WHEN raw_health_score >= 90
            THEN 'EXCEPTIONAL'

        WHEN raw_health_score >= 75
            THEN 'HEALTHY'

        WHEN raw_health_score >= 60
            THEN 'MONITOR'

        WHEN raw_health_score >= 40
            THEN 'AT_RISK'

        ELSE
            'CRITICAL'

    END AS health_class,


    -- ======================================================
    -- PRIMARY STRENGTH
    -- ======================================================

    CASE

        WHEN financial_health >= audience_health
         AND financial_health >= marketing_health
         AND financial_health >= strategic_health

            THEN 'FINANCIAL'

        WHEN audience_health >= marketing_health
         AND audience_health >= strategic_health

            THEN 'AUDIENCE'

        WHEN marketing_health >= strategic_health

            THEN 'MARKETING'

        ELSE
            'STRATEGIC'

    END AS primary_strength,


    -- ======================================================
    -- PRIMARY WEAKNESS
    -- ======================================================

    CASE

        WHEN financial_health <= audience_health
         AND financial_health <= marketing_health
         AND financial_health <= strategic_health

            THEN 'FINANCIAL'

        WHEN audience_health <= marketing_health
         AND audience_health <= strategic_health

            THEN 'AUDIENCE'

        WHEN marketing_health <= strategic_health

            THEN 'MARKETING'

        ELSE
            'STRATEGIC'

    END AS primary_weakness,


    -- ======================================================
    -- DECISION READINESS
    -- ======================================================

    ROUND(
        (
            COALESCE(
                decision_readiness_score,
                0
            ) * 100
        )::numeric,
        2
    ) AS decision_readiness_score,


    -- ======================================================
    -- EXISTING BUSINESS FLAGS
    -- ======================================================

    expansion_candidate_flag,

    renewal_candidate_flag,

    exit_candidate_flag,

    cost_optimization_candidate_flag,

    profitability_class,

    preliminary_decision

FROM health;


-- ==========================================================
-- EXECUTIVE HEALTH SUMMARY
-- ==========================================================

DROP VIEW IF EXISTS vw_executive_health_summary CASCADE;


CREATE VIEW vw_executive_health_summary AS

SELECT

    COUNT(*) AS total_content,

    ROUND(
        AVG(content_health_score)::numeric,
        2
    ) AS average_health_score,


    COUNT(*) FILTER (
        WHERE health_class = 'EXCEPTIONAL'
    ) AS exceptional_content,


    COUNT(*) FILTER (
        WHERE health_class = 'HEALTHY'
    ) AS healthy_content,


    COUNT(*) FILTER (
        WHERE health_class = 'MONITOR'
    ) AS monitor_content,


    COUNT(*) FILTER (
        WHERE health_class = 'AT_RISK'
    ) AS at_risk_content,


    COUNT(*) FILTER (
        WHERE health_class = 'CRITICAL'
    ) AS critical_content,


    ROUND(
        AVG(financial_health_score)::numeric,
        2
    ) AS average_financial_health,


    ROUND(
        AVG(audience_health_score)::numeric,
        2
    ) AS average_audience_health,


    ROUND(
        AVG(marketing_health_score)::numeric,
        2
    ) AS average_marketing_health,


    ROUND(
        AVG(strategic_health_score)::numeric,
        2
    ) AS average_strategic_health,


    ROUND(
        AVG(risk_penalty_score)::numeric,
        2
    ) AS average_risk_penalty

FROM vw_content_health_score;


-- ==========================================================
-- TOP / BOTTOM CONTENT
-- ==========================================================

SELECT

    content_id,

    title,

    content_type,

    content_health_score,

    health_class,

    financial_health_score,

    audience_health_score,

    marketing_health_score,

    strategic_health_score,

    risk_penalty_score,

    primary_strength,

    primary_weakness,

    decision_readiness_score,

    preliminary_decision

FROM vw_content_health_score

ORDER BY content_health_score DESC

LIMIT 25;