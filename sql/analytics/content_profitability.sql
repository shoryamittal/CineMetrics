-- ==========================================================
-- ECDIP - Content profitability and ROI intelligence
-- Aligned to the CSV-backed fact-table contract.
-- ==========================================================

DROP VIEW IF EXISTS vw_content_profitability CASCADE;
DROP VIEW IF EXISTS vw_content_economic_profile CASCADE;
DROP VIEW IF EXISTS vw_content_engagement_intelligence CASCADE;
DROP VIEW IF EXISTS vw_content_revenue_intelligence CASCADE;
DROP VIEW IF EXISTS vw_content_marketing_intelligence CASCADE;
DROP VIEW IF EXISTS vw_content_cost_intelligence CASCADE;

CREATE VIEW vw_content_cost_intelligence AS
SELECT
    content_id,
    total_content_cost,
    licensing_cost AS total_licensing_cost,
    production_budget,
    production_overhead,
    distribution_cost,
    technology_cost,
    localization_cost,
    contract_administration_cost,
    contingency_cost
FROM fact_content_cost;

CREATE VIEW vw_content_marketing_intelligence AS
SELECT
    content_id,
    COUNT(*) AS marketing_records,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    SUM(marketing_spend) AS total_marketing_spend,
    SUM(attributed_revenue) AS total_attributed_revenue,
    AVG(marketing_roi) AS average_campaign_roi,
    CASE WHEN SUM(impressions) = 0 THEN 0
         ELSE SUM(clicks)::NUMERIC / SUM(impressions) END AS click_through_rate,
    CASE WHEN SUM(clicks) = 0 THEN 0
         ELSE SUM(conversions)::NUMERIC / SUM(clicks) END AS conversion_rate,
    CASE WHEN SUM(conversions) = 0 THEN 0
         ELSE SUM(marketing_spend) / SUM(conversions) END AS cost_per_conversion
FROM fact_marketing
GROUP BY content_id;

CREATE VIEW vw_content_revenue_intelligence AS
SELECT
    content_id,
    COUNT(*) AS revenue_records,
    SUM(revenue_amount) AS total_revenue,
    AVG(revenue_amount) AS average_revenue_per_record,
    COALESCE(SUM(revenue_amount) FILTER (WHERE revenue_type = 'Subscription'), 0)
        AS total_subscription_revenue,
    COALESCE(SUM(revenue_amount) FILTER (WHERE revenue_type <> 'Subscription'), 0)
        AS total_advertising_revenue,
    CASE WHEN SUM(revenue_amount) = 0 THEN 0
         ELSE COALESCE(SUM(revenue_amount) FILTER (WHERE revenue_type = 'Subscription'), 0)
              / SUM(revenue_amount) END AS subscription_revenue_share,
    CASE WHEN SUM(revenue_amount) = 0 THEN 0
         ELSE COALESCE(SUM(revenue_amount) FILTER (WHERE revenue_type <> 'Subscription'), 0)
              / SUM(revenue_amount) END AS advertising_revenue_share
FROM fact_revenue
GROUP BY content_id;

CREATE VIEW vw_content_engagement_intelligence AS
SELECT
    content_id,
    COUNT(*) AS engagement_records,
    SUM(likes) AS total_likes,
    SUM(dislikes) AS total_dislikes,
    AVG(average_watch_percentage) AS average_watch_percentage,
    AVG(completion_rate) AS average_completion_rate,
    AVG(rewatch_rate) AS average_rewatch_rate,
    CASE WHEN SUM(likes) + SUM(dislikes) = 0 THEN 0
         ELSE SUM(likes)::NUMERIC / (SUM(likes) + SUM(dislikes)) END
        AS positive_engagement_rate
FROM fact_engagement
GROUP BY content_id;

CREATE VIEW vw_content_economic_profile AS
SELECT
    c.content_id,
    c.title,
    c.content_type,
    c.genre_id,
    c.studio_id,
    c.release_year,
    c.imdb_rating,
    c.available_regions,
    c.is_original,
    COALESCE(cost.total_content_cost, 0) AS total_content_cost,
    COALESCE(cost.total_licensing_cost, 0) AS total_licensing_cost,
    COALESCE(marketing.total_marketing_spend, 0) AS total_marketing_spend,
    COALESCE(marketing.total_impressions, 0) AS total_impressions,
    COALESCE(marketing.total_clicks, 0) AS total_clicks,
    COALESCE(marketing.total_conversions, 0) AS total_conversions,
    COALESCE(marketing.click_through_rate, 0) AS click_through_rate,
    COALESCE(marketing.conversion_rate, 0) AS conversion_rate,
    COALESCE(marketing.cost_per_conversion, 0) AS cost_per_conversion,
    COALESCE(revenue.total_revenue, 0) AS total_revenue,
    COALESCE(revenue.total_subscription_revenue, 0) AS total_subscription_revenue,
    COALESCE(revenue.total_advertising_revenue, 0) AS total_advertising_revenue,
    COALESCE(revenue.subscription_revenue_share, 0) AS subscription_revenue_share,
    COALESCE(revenue.advertising_revenue_share, 0) AS advertising_revenue_share,
    COALESCE(engagement.total_likes, 0) AS total_likes,
    COALESCE(engagement.total_dislikes, 0) AS total_dislikes,
    COALESCE(engagement.average_watch_percentage, 0) AS average_watch_percentage,
    COALESCE(engagement.average_completion_rate, 0) AS average_completion_rate,
    COALESCE(engagement.average_rewatch_rate, 0) AS average_rewatch_rate,
    COALESCE(marketing.average_campaign_roi, 0) AS average_campaign_roi,
    COALESCE(cost.total_content_cost, 0) + COALESCE(marketing.total_marketing_spend, 0)
        AS total_investment,
    COALESCE(revenue.total_revenue, 0) - COALESCE(cost.total_content_cost, 0)
        - COALESCE(marketing.total_marketing_spend, 0) AS contribution_profit,
    CASE WHEN COALESCE(cost.total_content_cost, 0) + COALESCE(marketing.total_marketing_spend, 0) = 0
         THEN 0
         ELSE (COALESCE(revenue.total_revenue, 0) - COALESCE(cost.total_content_cost, 0)
               - COALESCE(marketing.total_marketing_spend, 0))
              / (COALESCE(cost.total_content_cost, 0) + COALESCE(marketing.total_marketing_spend, 0))
    END AS content_roi,
    CASE WHEN COALESCE(revenue.total_revenue, 0) = 0 THEN 0
         ELSE (COALESCE(revenue.total_revenue, 0) - COALESCE(cost.total_content_cost, 0)
               - COALESCE(marketing.total_marketing_spend, 0)) / COALESCE(revenue.total_revenue, 0)
    END AS profit_margin,
    CASE WHEN COALESCE(cost.total_content_cost, 0) = 0 THEN 0
         ELSE COALESCE(revenue.total_revenue, 0) / COALESCE(cost.total_content_cost, 0)
    END AS revenue_to_content_cost_ratio
FROM dim_content c
LEFT JOIN vw_content_cost_intelligence cost USING (content_id)
LEFT JOIN vw_content_marketing_intelligence marketing USING (content_id)
LEFT JOIN vw_content_revenue_intelligence revenue USING (content_id)
LEFT JOIN vw_content_engagement_intelligence engagement USING (content_id);

CREATE VIEW vw_content_profitability AS
SELECT *,
    CASE WHEN content_roi >= 1 THEN 'EXCEPTIONAL'
         WHEN content_roi >= .5 THEN 'HIGH'
         WHEN content_roi >= .15 THEN 'POSITIVE'
         WHEN content_roi >= 0 THEN 'LOW_POSITIVE'
         ELSE 'NEGATIVE' END AS profitability_class,
    CASE WHEN content_roi >= .5 AND average_completion_rate >= .7 THEN 'STRONG_RENEWAL_CANDIDATE'
         WHEN content_roi >= .15 AND average_completion_rate >= .6 THEN 'REVIEW_FOR_RENEWAL'
         WHEN content_roi < 0 AND average_completion_rate < .5 THEN 'HIGH_RISK'
         WHEN content_roi < 0 THEN 'COST_REVIEW_REQUIRED'
         ELSE 'MONITOR' END AS preliminary_decision
FROM vw_content_economic_profile;

SELECT content_id, title, total_revenue, total_content_cost, total_marketing_spend,
       total_investment, contribution_profit, content_roi, profitability_class,
       preliminary_decision
FROM vw_content_profitability
ORDER BY contribution_profit DESC
LIMIT 25;
