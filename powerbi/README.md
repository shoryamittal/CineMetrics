# OTT Power BI analytics blueprint

Import `data/analytics/content_performance_scorecard.csv`,
`data/analytics/regional_performance.csv`, and `data/analytics/executive_kpis.csv`
alongside the original synthetic model. Create the measures in
`OTT_Gold_Standard_Measures.dax`.

Build four report pages:

1. **Executive command center** — revenue, investment, contribution profit,
portfolio ROI, 30-day forecast, and decision-candidate counts.
2. **Content portfolio** — scatter plot of revenue versus ROI sized by cost;
title drill-through with cost mix, completion, rewatch, and profitability.
3. **Audience & growth** — watch hours, views, completion, search-to-watch,
and subscriber-event trends by date, region, plan, and platform.
4. **Market & marketing** — regional revenue map, revenue per watch hour,
campaign conversion funnel, CAC, and marketing ROI.

Use slicers for date, region, genre, content type, studio, plan, and platform.
Use the `decision` field from the scorecard as an executive action filter.
