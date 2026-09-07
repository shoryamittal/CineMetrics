-- ==========================================================
-- ECDIP - DECISION INTELLIGENCE ENGINE
-- SCHEMA-SAFE VERSION
-- ==========================================================

DROP VIEW IF EXISTS vw_executive_decision_summary CASCADE;
DROP VIEW IF EXISTS vw_content_decision_intelligence CASCADE;


-- ==========================================================
-- 1. DECISION INTELLIGENCE
-- ==========================================================

CREATE VIEW vw_content_decision_intelligence AS

WITH combined AS (

    SELECT

        -- ==================================================
        -- CONTENT IDENTITY
        -- ==================================================

        h.content_id,
        h.title,
        h.content_type,
        h.genre_id,
        h.studio_id,
        h.release_year,
        h.is_original,


        -- ==================================================
        -- FINANCIAL METRICS
        -- FROM FEATURE LAYER
        -- ==================================================

        f.total_revenue,
        f.total_content_cost,
        f.total_marketing_spend,
        f.total_investment,
        f.contribution_profit,
        f.content_roi,
        f.profit_margin,


        -- ==================================================
        -- AUDIENCE / MARKETING
        -- FROM FEATURE LAYER
        -- ==================================================

        f.average_completion_rate,
        f.average_rewatch_rate,
        f.average_campaign_roi,
        f.conversion_rate,

        f.audience_quality_score,
        f.engagement_quality_score,


        -- ==================================================
        -- FEATURE SIGNALS
        -- ==================================================

        f.broad_regional_reach_flag,

        f.investment_recovery_risk_flag,

        f.negative_roi_risk,
        f.negative_margin_risk,
        f.weak_completion_risk,
        f.weak_rewatch_risk,
        f.weak_engagement_risk,
        f.negative_marketing_roi_risk,


        -- ==================================================
        -- HEALTH SCORE
        -- FROM HEALTH LAYER
        -- ==================================================

        h.content_health_score,
        h.health_class,

        h.financial_health_score,
        h.audience_health_score,
        h.marketing_health_score,
        h.strategic_health_score,
        h.risk_penalty_score,

        h.primary_strength,
        h.primary_weakness,

        h.decision_readiness_score,

        h.expansion_candidate_flag,
        h.renewal_candidate_flag,
        h.exit_candidate_flag,
        h.cost_optimization_candidate_flag,

        h.profitability_class,
        h.preliminary_decision

    FROM vw_content_health_score h

    INNER JOIN vw_content_features f
        ON h.content_id = f.content_id
),


-- ==========================================================
-- 2. SIGNAL ENGINE
-- ==========================================================

signals AS (

    SELECT

        c.*,


        -- --------------------------------------------------
        -- POSITIVE SIGNALS
        -- --------------------------------------------------

        (
            CASE
                WHEN c.content_health_score >= 75
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.content_roi >= 0.15
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_completion_rate >= 0.60
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_rewatch_rate >= 0.15
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_campaign_roi >= 1.00
                THEN 1 ELSE 0
            END

        ) AS positive_signal_count,


        -- --------------------------------------------------
        -- RISK SIGNALS
        -- --------------------------------------------------

        (
            CASE
                WHEN c.content_health_score < 60
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.content_roi < 0
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_completion_rate < 0.50
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_rewatch_rate < 0.10
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.average_campaign_roi < 0
                THEN 1 ELSE 0
            END

            +

            CASE
                WHEN c.risk_penalty_score >= 30
                THEN 1 ELSE 0
            END

        ) AS risk_signal_count

    FROM combined c
),


-- ==========================================================
-- 3. DECISION SCORES
-- ==========================================================

scored AS (

    SELECT

        s.*,


        -- ==================================================
        -- RENEWAL
        -- ==================================================

        (
            s.content_health_score * 0.35

            +

            LEAST(
                100,
                GREATEST(
                    0,
                    s.content_roi * 50
                )
            ) * 0.25

            +

            s.audience_health_score * 0.20

            +

            s.decision_readiness_score * 0.20

        ) AS renewal_score,


        -- ==================================================
        -- PROMOTION
        -- ==================================================

        (
            s.audience_health_score * 0.35

            +

            s.marketing_health_score * 0.25

            +

            s.content_health_score * 0.20

            +

            s.decision_readiness_score * 0.20

        ) AS promotion_score,


        -- ==================================================
        -- EXPANSION
        -- ==================================================

        (
            s.content_health_score * 0.30

            +

            s.financial_health_score * 0.25

            +

            s.audience_health_score * 0.20

            +

            s.marketing_health_score * 0.15

            +

            CASE
                WHEN s.broad_regional_reach_flag = 1
                THEN 100
                ELSE 50
            END * 0.10

        ) AS expansion_score,


        -- ==================================================
        -- MARKETING OPTIMIZATION
        -- ==================================================

        (
            (
                100 - s.marketing_health_score
            ) * 0.35

            +

            s.audience_health_score * 0.25

            +

            s.financial_health_score * 0.20

            +

            CASE
                WHEN s.average_campaign_roi < 1
                THEN 100
                ELSE 0
            END * 0.20

        ) AS marketing_optimization_score,


        -- ==================================================
        -- EXIT
        -- ==================================================

        (
            (
                100 - s.content_health_score
            ) * 0.30

            +

            CASE
                WHEN s.content_roi < 0
                THEN 100
                ELSE 0
            END * 0.25

            +

            CASE
                WHEN s.average_completion_rate < 0.50
                THEN 100
                ELSE 0
            END * 0.20

            +

            CASE
                WHEN s.average_rewatch_rate < 0.10
                THEN 100
                ELSE 0
            END * 0.15

            +

            s.risk_penalty_score * 0.10

        ) AS exit_score

    FROM signals s
),


-- ==========================================================
-- 4. FINAL DECISION
-- ==========================================================

decisioned AS (

    SELECT

        s.*,


        CASE

            WHEN
                s.content_health_score >= 75
                AND s.content_roi >= 0.30
                AND s.audience_health_score >= 70

                THEN 'RENEW'


            WHEN
                s.audience_health_score >= 75
                AND s.marketing_health_score < 60
                AND s.content_roi >= 0

                THEN 'PROMOTE'


            WHEN
                s.expansion_score >= 75
                AND s.content_roi >= 0.30

                THEN 'EXPAND'


            WHEN
                s.marketing_optimization_score >= 70
                AND s.content_health_score >= 60

                THEN 'OPTIMIZE_MARKETING'


            WHEN
                s.content_roi < 0
                AND s.audience_health_score >= 65

                THEN 'RENEGOTIATE'


            WHEN
                s.exit_score >= 75
                AND s.risk_signal_count >= 3

                THEN 'EXIT'


            WHEN
                s.content_health_score < 60

                THEN 'MONITOR'


            ELSE
                'MONITOR'

        END AS recommended_action

    FROM scored s
)


-- ==========================================================
-- 5. FINAL OUTPUT
-- ==========================================================

SELECT

    content_id,
    title,
    content_type,
    genre_id,
    studio_id,
    release_year,
    is_original,

    total_revenue,
    total_content_cost,
    total_marketing_spend,
    total_investment,
    contribution_profit,

    content_roi,
    profit_margin,

    content_health_score,
    health_class,

    financial_health_score,
    audience_health_score,
    marketing_health_score,
    strategic_health_score,
    risk_penalty_score,

    average_completion_rate,
    average_rewatch_rate,
    average_campaign_roi,
    conversion_rate,

    audience_quality_score,
    engagement_quality_score,

    ROUND(
        renewal_score::numeric,
        2
    ) AS renewal_score,

    ROUND(
        promotion_score::numeric,
        2
    ) AS promotion_score,

    ROUND(
        expansion_score::numeric,
        2
    ) AS expansion_score,

    ROUND(
        marketing_optimization_score::numeric,
        2
    ) AS marketing_optimization_score,

    ROUND(
        exit_score::numeric,
        2
    ) AS exit_score,

    positive_signal_count,
    risk_signal_count,

    recommended_action,


    -- ======================================================
    -- CONFIDENCE
    -- ======================================================

    ROUND(

        LEAST(
            100,

            GREATEST(
                0,

                (
                    content_health_score * 0.40

                    +

                    decision_readiness_score * 0.30

                    +

                    (
                        positive_signal_count::numeric
                        / 5.0
                    ) * 100 * 0.15

                    +

                    (
                        100
                        -
                        (
                            risk_signal_count::numeric
                            / 6.0
                        ) * 100
                    ) * 0.15
                )
            )
        )::numeric,

        2

    ) AS decision_confidence,


    -- ======================================================
    -- PRIMARY EXPLANATION
    -- ======================================================

    CASE

        WHEN
            content_roi >= 0.30
            AND content_health_score >= 75

            THEN
                'Strong economic performance and healthy content signals'


        WHEN
            audience_health_score >= 75

            THEN
                'Strong audience engagement and retention signals'


        WHEN
            marketing_health_score < 60
            AND content_roi >= 0

            THEN
                'Content is viable but marketing efficiency requires improvement'


        WHEN
            content_roi < 0
            AND audience_health_score >= 65

            THEN
                'Audience value exists despite negative economics'


        WHEN
            risk_signal_count >= 3

            THEN
                'Multiple financial, engagement or marketing risk signals'


        ELSE
            'Performance requires continued monitoring'

    END AS primary_reason,


    -- ======================================================
    -- SECONDARY EXPLANATION
    -- ======================================================

    CASE

        WHEN average_completion_rate >= 0.70
            THEN 'High completion rate'

        WHEN average_rewatch_rate >= 0.20
            THEN 'Strong rewatch behavior'

        WHEN average_campaign_roi >= 1.00
            THEN 'Efficient marketing performance'

        WHEN profit_margin >= 0.20
            THEN 'Healthy profit margin'

        WHEN content_roi < 0
            THEN 'Negative content ROI'

        ELSE
            'No dominant secondary signal'

    END AS secondary_reason,


    preliminary_decision

FROM decisioned;


-- ==========================================================
-- 6. EXECUTIVE SUMMARY
-- ==========================================================

CREATE VIEW vw_executive_decision_summary AS

SELECT

    COUNT(*) AS total_content,

    COUNT(*) FILTER (
        WHERE recommended_action = 'RENEW'
    ) AS renew_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'PROMOTE'
    ) AS promote_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'EXPAND'
    ) AS expand_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'RENEGOTIATE'
    ) AS renegotiate_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'OPTIMIZE_MARKETING'
    ) AS optimize_marketing_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'MONITOR'
    ) AS monitor_count,

    COUNT(*) FILTER (
        WHERE recommended_action = 'EXIT'
    ) AS exit_count,

    ROUND(
        AVG(decision_confidence)::numeric,
        2
    ) AS average_decision_confidence,

    ROUND(
        AVG(content_health_score)::numeric,
        2
    ) AS average_content_health,

    ROUND(
        AVG(content_roi)::numeric,
        3
    ) AS average_content_roi

FROM vw_content_decision_intelligence;