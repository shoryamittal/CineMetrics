-- ==========================================================
-- ECDIP - ADVANCED CONTENT KPI INTELLIGENCE
-- ==========================================================

DROP VIEW IF EXISTS vw_content_kpis CASCADE;

CREATE VIEW vw_content_kpis AS

WITH base AS (

    SELECT
        p.*,

        -- Revenue efficiency
        CASE
            WHEN p.total_investment = 0
            THEN 0
            ELSE p.total_revenue
                 / p.total_investment
        END AS revenue_per_investment,

        -- Profit efficiency
        CASE
            WHEN p.total_content_cost = 0
            THEN 0
            ELSE p.contribution_profit
                 / p.total_content_cost
        END AS profit_per_content_cost,

        -- Marketing efficiency
        CASE
            WHEN p.total_marketing_spend = 0
            THEN 0
            ELSE p.total_revenue
                 / p.total_marketing_spend
        END AS revenue_per_marketing_spend,

        -- Engagement quality
        (
            COALESCE(
                p.average_completion_rate,
                0
            )
            *
            0.50
            +
            COALESCE(
                p.average_rewatch_rate,
                0
            )
            *
            0.30
            +
            COALESCE(
                p.positive_engagement_rate,
                0
            )
            *
            0.20
        ) AS engagement_quality_score

    FROM vw_content_profitability p
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
    -- FINANCIAL KPIs
    -- ======================================================

    total_revenue,

    total_content_cost,

    total_marketing_spend,

    total_investment,

    contribution_profit,

    content_roi,

    profit_margin,

    revenue_to_content_cost_ratio,

    revenue_per_investment,

    profit_per_content_cost,

    revenue_per_marketing_spend,

    -- ======================================================
    -- REVENUE MIX
    -- ======================================================

    total_subscription_revenue,

    total_advertising_revenue,

    subscription_revenue_share,

    advertising_revenue_share,

    -- ======================================================
    -- MARKETING KPIs
    -- ======================================================

    total_impressions,

    total_clicks,

    total_conversions,

    average_campaign_roi,

    click_through_rate,

    conversion_rate,

    cost_per_conversion,

    -- ======================================================
    -- ENGAGEMENT KPIs
    -- ======================================================

    total_likes,

    total_dislikes,

    average_watch_percentage,

    average_completion_rate,

    average_rewatch_rate,

    positive_engagement_rate,

    engagement_quality_score,

    -- ======================================================
    -- BUSINESS CLASSIFICATION
    -- ======================================================

    profitability_class,

    preliminary_decision,

    -- ======================================================
    -- KPI FLAGS
    -- ======================================================

    CASE
        WHEN content_roi >= 0.50
        THEN 1
        ELSE 0
    END AS high_roi_flag,

    CASE
        WHEN profit_margin >= 0.20
        THEN 1
        ELSE 0
    END AS healthy_margin_flag,

    CASE
        WHEN average_completion_rate >= 0.70
        THEN 1
        ELSE 0
    END AS strong_completion_flag,

    CASE
        WHEN average_rewatch_rate >= 0.20
        THEN 1
        ELSE 0
    END AS strong_rewatch_flag,

    CASE
        WHEN conversion_rate >= 0.10
        THEN 1
        ELSE 0
    END AS strong_conversion_flag,

    CASE
        WHEN average_campaign_roi >= 1.00
        THEN 1
        ELSE 0
    END AS efficient_marketing_flag,

    CASE
        WHEN contribution_profit < 0
        THEN 1
        ELSE 0
    END AS loss_making_flag,

    CASE
        WHEN content_roi < 0
        THEN 1
        ELSE 0
    END AS negative_roi_flag,

    CASE
        WHEN average_completion_rate < 0.50
        THEN 1
        ELSE 0
    END AS weak_completion_flag

FROM base;


-- ==========================================================
-- EXECUTIVE KPI SUMMARY
-- ==========================================================

DROP VIEW IF EXISTS vw_executive_content_kpis CASCADE;

CREATE VIEW vw_executive_content_kpis AS

SELECT

    COUNT(*) AS total_content,

    COUNT(*) FILTER (
        WHERE content_roi > 0
    ) AS profitable_content,

    COUNT(*) FILTER (
        WHERE content_roi < 0
    ) AS loss_making_content,

    COUNT(*) FILTER (
        WHERE high_roi_flag = 1
    ) AS high_roi_content,

    COUNT(*) FILTER (
        WHERE healthy_margin_flag = 1
    ) AS healthy_margin_content,

    COUNT(*) FILTER (
        WHERE strong_completion_flag = 1
    ) AS high_completion_content,

    COUNT(*) FILTER (
        WHERE strong_rewatch_flag = 1
    ) AS high_rewatch_content,

    COUNT(*) FILTER (
        WHERE efficient_marketing_flag = 1
    ) AS efficient_marketing_content,

    ROUND(
        SUM(total_revenue)::numeric,
        2
    ) AS portfolio_revenue,

    ROUND(
        SUM(total_investment)::numeric,
        2
    ) AS portfolio_investment,

    ROUND(
        SUM(contribution_profit)::numeric,
        2
    ) AS portfolio_profit,

    ROUND(
        AVG(content_roi)::numeric,
        3
    ) AS average_content_roi,

    ROUND(
        AVG(profit_margin)::numeric,
        3
    ) AS average_profit_margin,

    ROUND(
        AVG(average_completion_rate)::numeric,
        3
    ) AS average_completion_rate,

    ROUND(
        AVG(average_rewatch_rate)::numeric,
        3
    ) AS average_rewatch_rate,

    ROUND(
        AVG(conversion_rate)::numeric,
        3
    ) AS average_conversion_rate,

    ROUND(
        AVG(engagement_quality_score)::numeric,
        3
    ) AS average_engagement_quality

FROM vw_content_kpis;


-- ==========================================================
-- TOP CONTENT BY BUSINESS VALUE
-- ==========================================================

SELECT

    content_id,

    title,

    content_type,

    total_revenue,

    contribution_profit,

    content_roi,

    profit_margin,

    average_completion_rate,

    average_rewatch_rate,

    average_campaign_roi,

    engagement_quality_score,

    profitability_class,

    preliminary_decision

FROM vw_content_kpis

ORDER BY contribution_profit DESC

LIMIT 25;