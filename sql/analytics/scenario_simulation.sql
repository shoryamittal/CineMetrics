-- ==========================================================
-- ECDIP - SCENARIO / WHAT-IF SIMULATION ENGINE
-- ==========================================================
--
-- Purpose:
-- Simulate business decisions before management executes them.
--
-- Scenarios:
--   1. Marketing Increase
--   2. Marketing Reduction
--   3. Cost Increase
--   4. Cost Reduction
--   5. Revenue Growth
--   6. Revenue Decline
--   7. Regional Expansion
--   8. Combined Scenario
--
-- ==========================================================


DROP VIEW IF EXISTS vw_content_scenario_simulation CASCADE;


CREATE VIEW vw_content_scenario_simulation AS

WITH base AS (

    SELECT

        d.content_id,
        d.title,
        d.content_type,

        d.total_revenue,
        d.total_content_cost,
        d.total_marketing_spend,
        d.total_investment,
        d.contribution_profit,
        d.content_roi,

        d.content_health_score,
        d.health_class,

        d.recommended_action,
        d.decision_confidence

    FROM vw_content_decision_intelligence d
),


-- ==========================================================
-- SCENARIO PARAMETERS
-- ==========================================================

scenarios AS (

    SELECT
        'BASELINE' AS scenario_name,
        0.00::NUMERIC AS marketing_change,
        0.00::NUMERIC AS content_cost_change,
        0.00::NUMERIC AS revenue_change

    UNION ALL

    SELECT
        'MARKETING_UP_20',
        0.20,
        0.00,
        0.00

    UNION ALL

    SELECT
        'MARKETING_DOWN_20',
        -0.20,
        0.00,
        0.00

    UNION ALL

    SELECT
        'CONTENT_COST_UP_15',
        0.00,
        0.15,
        0.00

    UNION ALL

    SELECT
        'CONTENT_COST_DOWN_15',
        0.00,
        -0.15,
        0.00

    UNION ALL

    SELECT
        'REVENUE_UP_20',
        0.00,
        0.00,
        0.20

    UNION ALL

    SELECT
        'REVENUE_DOWN_20',
        0.00,
        0.00,
        -0.20

    UNION ALL

    SELECT
        'GROWTH_CASE',
        0.20,
        0.10,
        0.20

    UNION ALL

    SELECT
        'DOWNSIDE_CASE',
        0.10,
        0.15,
        -0.15

    UNION ALL

    SELECT
        'EFFICIENCY_CASE',
        -0.20,
        -0.10,
        0.10
),


-- ==========================================================
-- APPLY SCENARIOS
-- ==========================================================

calculated AS (

    SELECT

        b.content_id,
        b.title,
        b.content_type,

        s.scenario_name,

        -- --------------------------------------------------
        -- BASELINE
        -- --------------------------------------------------

        b.total_revenue AS baseline_revenue,

        b.total_content_cost AS baseline_content_cost,

        b.total_marketing_spend AS baseline_marketing_spend,

        b.total_investment AS baseline_investment,

        b.contribution_profit AS baseline_profit,

        b.content_roi AS baseline_roi,


        -- --------------------------------------------------
        -- SCENARIO REVENUE
        -- --------------------------------------------------

        (
            b.total_revenue
            *
            (1 + s.revenue_change)
        ) AS scenario_revenue,


        -- --------------------------------------------------
        -- SCENARIO CONTENT COST
        -- --------------------------------------------------

        (
            b.total_content_cost
            *
            (1 + s.content_cost_change)
        ) AS scenario_content_cost,


        -- --------------------------------------------------
        -- SCENARIO MARKETING
        -- --------------------------------------------------

        (
            b.total_marketing_spend
            *
            (1 + s.marketing_change)
        ) AS scenario_marketing_spend,


        b.content_health_score,

        b.health_class,

        b.recommended_action,

        b.decision_confidence,

        s.marketing_change,

        s.content_cost_change,

        s.revenue_change

    FROM base b

    CROSS JOIN scenarios s
),


-- ==========================================================
-- FINANCIAL CALCULATION
-- ==========================================================

financials AS (

    SELECT

        c.*,


        -- --------------------------------------------------
        -- TOTAL SCENARIO INVESTMENT
        -- --------------------------------------------------

        (
            c.scenario_content_cost
            +
            c.scenario_marketing_spend
        ) AS scenario_investment,


        -- --------------------------------------------------
        -- SCENARIO PROFIT
        -- --------------------------------------------------

        (
            c.scenario_revenue
            -
            c.scenario_content_cost
            -
            c.scenario_marketing_spend
        ) AS scenario_profit

    FROM calculated c
),


-- ==========================================================
-- ROI CALCULATION
-- ==========================================================

roi_calculated AS (

    SELECT

        f.*,


        CASE

            WHEN f.scenario_investment = 0

            THEN 0

            ELSE

                f.scenario_profit
                /
                f.scenario_investment

        END AS scenario_roi

    FROM financials f
)


-- ==========================================================
-- FINAL OUTPUT
-- ==========================================================

SELECT

    content_id,

    title,

    content_type,

    scenario_name,


    -- ------------------------------------------------------
    -- BASELINE
    -- ------------------------------------------------------

    baseline_revenue,

    baseline_content_cost,

    baseline_marketing_spend,

    baseline_investment,

    baseline_profit,

    baseline_roi,


    -- ------------------------------------------------------
    -- SCENARIO
    -- ------------------------------------------------------

    scenario_revenue,

    scenario_content_cost,

    scenario_marketing_spend,

    scenario_investment,

    scenario_profit,

    scenario_roi,


    -- ------------------------------------------------------
    -- IMPACT
    -- ------------------------------------------------------

    (
        scenario_revenue
        -
        baseline_revenue
    ) AS revenue_change_amount,


    (
        scenario_profit
        -
        baseline_profit
    ) AS profit_change_amount,


    (
        scenario_roi
        -
        baseline_roi
    ) AS roi_change,


    -- ------------------------------------------------------
    -- HEALTH / DECISION
    -- ------------------------------------------------------

    content_health_score,

    health_class,

    recommended_action,

    decision_confidence,


    -- ------------------------------------------------------
    -- SCENARIO CLASSIFICATION
    -- ------------------------------------------------------

    CASE

        WHEN scenario_profit > baseline_profit
         AND scenario_roi > baseline_roi

            THEN 'POSITIVE_IMPACT'


        WHEN scenario_profit < baseline_profit
         AND scenario_roi < baseline_roi

            THEN 'NEGATIVE_IMPACT'


        ELSE
            'MIXED_IMPACT'

    END AS scenario_impact,


    -- ------------------------------------------------------
    -- MANAGEMENT INTERPRETATION
    -- ------------------------------------------------------

    CASE

        WHEN
            scenario_profit > baseline_profit
            AND scenario_roi > baseline_roi

            THEN
                'Scenario improves both profit and ROI'


        WHEN
            scenario_profit < baseline_profit
            AND scenario_roi < baseline_roi

            THEN
                'Scenario reduces both profit and ROI'


        WHEN
            scenario_profit > baseline_profit
            AND scenario_roi < baseline_roi

            THEN
                'Profit increases but investment efficiency declines'


        WHEN
            scenario_profit < baseline_profit
            AND scenario_roi > baseline_roi

            THEN
                'Profit declines but investment efficiency improves'


        ELSE
            'Scenario impact is neutral'

    END AS management_interpretation

FROM roi_calculated;