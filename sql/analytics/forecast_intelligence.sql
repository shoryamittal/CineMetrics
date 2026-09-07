-- ==========================================================
-- ECDIP - FORECAST INTELLIGENCE LAYER
-- ==========================================================
--
-- Converts raw forecast rows into business-ready signals.
--
-- Outputs:
--   Forecast summaries
--   Growth / decline
--   Confidence
--   Upside potential
--   Downside risk
--   30-day business outlook
--
-- ==========================================================


-- ==========================================================
-- 1. CONTENT FORECAST SUMMARY
-- ==========================================================

DROP VIEW IF EXISTS vw_content_forecast_summary CASCADE;

CREATE VIEW vw_content_forecast_summary AS

SELECT

    content_id,

    metric_name,

    COUNT(*) AS forecast_days,

    MIN(forecast_date) AS forecast_start_date,

    MAX(forecast_date) AS forecast_end_date,

    SUM(forecast_value) AS total_forecast_value,

    AVG(forecast_value) AS average_daily_forecast,

    MIN(forecast_value) AS minimum_forecast,

    MAX(forecast_value) AS maximum_forecast,

    SUM(lower_bound) AS total_lower_bound,

    SUM(upper_bound) AS total_upper_bound,

    AVG(confidence) AS average_confidence,

    MAX(forecast_horizon_day) AS forecast_horizon,

    MODE() WITHIN GROUP (
        ORDER BY trend
    ) AS dominant_trend,

    AVG(momentum) AS average_momentum,

    AVG(r_squared) AS average_model_fit

FROM fact_forecast

GROUP BY
    content_id,
    metric_name;


-- ==========================================================
-- 2. VIEWING DEMAND FORECAST
-- ==========================================================

DROP VIEW IF EXISTS vw_content_demand_forecast CASCADE;

CREATE VIEW vw_content_demand_forecast AS

SELECT

    content_id,

    total_forecast_value
        AS forecast_30d_watch_hours,

    average_daily_forecast
        AS forecast_daily_watch_hours,

    total_lower_bound
        AS forecast_30d_watch_hours_lower,

    total_upper_bound
        AS forecast_30d_watch_hours_upper,

    average_confidence
        AS demand_forecast_confidence,

    dominant_trend
        AS demand_trend,

    average_momentum
        AS demand_momentum,

    average_model_fit
        AS demand_model_fit

FROM vw_content_forecast_summary

WHERE metric_name = 'VIEWING_DEMAND';


-- ==========================================================
-- 3. REVENUE FORECAST
-- ==========================================================

DROP VIEW IF EXISTS vw_content_revenue_forecast CASCADE;

CREATE VIEW vw_content_revenue_forecast AS

SELECT

    content_id,

    total_forecast_value
        AS forecast_30d_revenue,

    average_daily_forecast
        AS forecast_daily_revenue,

    total_lower_bound
        AS forecast_30d_revenue_lower,

    total_upper_bound
        AS forecast_30d_revenue_upper,

    average_confidence
        AS revenue_forecast_confidence,

    dominant_trend
        AS revenue_trend,

    average_momentum
        AS revenue_momentum,

    average_model_fit
        AS revenue_model_fit

FROM vw_content_forecast_summary

WHERE metric_name = 'REVENUE';


-- ==========================================================
-- 4. ENGAGEMENT FORECAST
-- ==========================================================

DROP VIEW IF EXISTS vw_content_engagement_forecast CASCADE;

CREATE VIEW vw_content_engagement_forecast AS

SELECT

    content_id,

    average_daily_forecast
        AS forecast_engagement_rate,

    total_lower_bound
        AS forecast_engagement_lower,

    total_upper_bound
        AS forecast_engagement_upper,

    average_confidence
        AS engagement_forecast_confidence,

    dominant_trend
        AS engagement_trend,

    average_momentum
        AS engagement_momentum,

    average_model_fit
        AS engagement_model_fit

FROM vw_content_forecast_summary

WHERE metric_name = 'ENGAGEMENT';


-- ==========================================================
-- 5. PREDICTIVE CONTENT INTELLIGENCE
-- ==========================================================

DROP VIEW IF EXISTS vw_content_predictive_intelligence CASCADE;

CREATE VIEW vw_content_predictive_intelligence AS

SELECT

    c.content_id,

    c.title,

    c.content_type,

    c.genre_id,

    c.studio_id,

    c.release_year,


    -- ------------------------------------------------------
    -- DEMAND OUTLOOK
    -- ------------------------------------------------------

    COALESCE(
        d.forecast_30d_watch_hours,
        0
    ) AS forecast_30d_watch_hours,

    COALESCE(
        d.forecast_daily_watch_hours,
        0
    ) AS forecast_daily_watch_hours,

    COALESCE(
        d.forecast_30d_watch_hours_lower,
        0
    ) AS forecast_30d_watch_hours_lower,

    COALESCE(
        d.forecast_30d_watch_hours_upper,
        0
    ) AS forecast_30d_watch_hours_upper,

    COALESCE(
        d.demand_forecast_confidence,
        0
    ) AS demand_forecast_confidence,

    COALESCE(
        d.demand_trend,
        'UNKNOWN'
    ) AS demand_trend,

    COALESCE(
        d.demand_momentum,
        0
    ) AS demand_momentum,


    -- ------------------------------------------------------
    -- REVENUE OUTLOOK
    -- ------------------------------------------------------

    COALESCE(
        r.forecast_30d_revenue,
        0
    ) AS forecast_30d_revenue,

    COALESCE(
        r.forecast_daily_revenue,
        0
    ) AS forecast_daily_revenue,

    COALESCE(
        r.forecast_30d_revenue_lower,
        0
    ) AS forecast_30d_revenue_lower,

    COALESCE(
        r.forecast_30d_revenue_upper,
        0
    ) AS forecast_30d_revenue_upper,

    COALESCE(
        r.revenue_forecast_confidence,
        0
    ) AS revenue_forecast_confidence,

    COALESCE(
        r.revenue_trend,
        'UNKNOWN'
    ) AS revenue_trend,

    COALESCE(
        r.revenue_momentum,
        0
    ) AS revenue_momentum,


    -- ------------------------------------------------------
    -- ENGAGEMENT OUTLOOK
    -- ------------------------------------------------------

    COALESCE(
        e.forecast_engagement_rate,
        0
    ) AS forecast_engagement_rate,

    COALESCE(
        e.forecast_engagement_lower,
        0
    ) AS forecast_engagement_lower,

    COALESCE(
        e.forecast_engagement_upper,
        0
    ) AS forecast_engagement_upper,

    COALESCE(
        e.engagement_forecast_confidence,
        0
    ) AS engagement_forecast_confidence,

    COALESCE(
        e.engagement_trend,
        'UNKNOWN'
    ) AS engagement_trend,

    COALESCE(
        e.engagement_momentum,
        0
    ) AS engagement_momentum,


    -- ------------------------------------------------------
    -- COMBINED CONFIDENCE
    -- ------------------------------------------------------

    (
        COALESCE(
            d.demand_forecast_confidence,
            0
        ) * 0.35

        +

        COALESCE(
            r.revenue_forecast_confidence,
            0
        ) * 0.40

        +

        COALESCE(
            e.engagement_forecast_confidence,
            0
        ) * 0.25

    ) AS overall_forecast_confidence,


    -- ------------------------------------------------------
    -- FORECAST RISK
    -- ------------------------------------------------------

    CASE

        WHEN
            COALESCE(
                r.revenue_trend,
                'UNKNOWN'
            ) IN (
                'DECLINE',
                'STRONG_DECLINE'
            )

        THEN 'HIGH'


        WHEN
            COALESCE(
                d.demand_trend,
                'UNKNOWN'
            ) IN (
                'DECLINE',
                'STRONG_DECLINE'
            )

        THEN 'MEDIUM'


        WHEN
            (
                COALESCE(
                    r.revenue_forecast_confidence,
                    0
                ) < 60
            )

        THEN 'MEDIUM'


        ELSE 'LOW'

    END AS forecast_risk,


    -- ------------------------------------------------------
    -- UPSIDE OPPORTUNITY
    -- ------------------------------------------------------

    CASE

        WHEN
            COALESCE(
                r.revenue_trend,
                'UNKNOWN'
            ) IN (
                'GROWTH',
                'STRONG_GROWTH'
            )
            AND
            COALESCE(
                d.demand_trend,
                'UNKNOWN'
            ) IN (
                'GROWTH',
                'STRONG_GROWTH'
            )

        THEN 'HIGH'


        WHEN
            COALESCE(
                r.revenue_trend,
                'UNKNOWN'
            ) = 'GROWTH'

        THEN 'MEDIUM'


        ELSE 'LOW'

    END AS forecast_opportunity


FROM dim_content c

LEFT JOIN vw_content_demand_forecast d
    ON c.content_id = d.content_id

LEFT JOIN vw_content_revenue_forecast r
    ON c.content_id = r.content_id

LEFT JOIN vw_content_engagement_forecast e
    ON c.content_id = e.content_id;


-- ==========================================================
-- 6. FORECAST EXECUTIVE SUMMARY
-- ==========================================================

DROP VIEW IF EXISTS vw_executive_forecast_summary CASCADE;

CREATE VIEW vw_executive_forecast_summary AS

SELECT

    COUNT(*) AS total_content,

    COUNT(*) FILTER (
        WHERE forecast_risk = 'HIGH'
    ) AS high_forecast_risk_content,

    COUNT(*) FILTER (
        WHERE forecast_risk = 'MEDIUM'
    ) AS medium_forecast_risk_content,

    COUNT(*) FILTER (
        WHERE forecast_opportunity = 'HIGH'
    ) AS high_forecast_opportunity_content,

    ROUND(
        AVG(overall_forecast_confidence)::numeric,
        2
    ) AS average_forecast_confidence,

    COUNT(*) FILTER (
        WHERE revenue_trend IN (
            'GROWTH',
            'STRONG_GROWTH'
        )
    ) AS revenue_growth_content,

    COUNT(*) FILTER (
        WHERE revenue_trend IN (
            'DECLINE',
            'STRONG_DECLINE'
        )
    ) AS revenue_decline_content,

    COUNT(*) FILTER (
        WHERE demand_trend IN (
            'GROWTH',
            'STRONG_GROWTH'
        )
    ) AS demand_growth_content,

    COUNT(*) FILTER (
        WHERE demand_trend IN (
            'DECLINE',
            'STRONG_DECLINE'
        )
    ) AS demand_decline_content

FROM vw_content_predictive_intelligence;


-- ==========================================================
-- 7. TOP FORECAST OPPORTUNITIES
-- ==========================================================

SELECT

    content_id,

    title,

    content_type,

    forecast_30d_revenue,

    forecast_30d_watch_hours,

    revenue_trend,

    demand_trend,

    engagement_trend,

    overall_forecast_confidence,

    forecast_risk,

    forecast_opportunity

FROM vw_content_predictive_intelligence

ORDER BY
    forecast_opportunity DESC,
    forecast_30d_revenue DESC

LIMIT 25;
