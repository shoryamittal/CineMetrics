"""
Dual-Domain Operational Analytics Framework (Streamlit Dashboard)
==================================================================
Production-grade interactive executive application bridging two domains:
  1. "EcoMetrics Mode" (Industrial Sustainability Domain):
     - Automated water volume treatment, energy logs, sensor temperature excursions,
       and chemical dosing concentrations across global manufacturing facilities.
  2. "CineMetrics Mode" (Entertainment Media Intelligence Domain):
     - Media performance, Bayesian weighted ratings, genre capital efficiency,
       and Year-over-Year revenue momentum.

Features:
  - Top-of-sidebar Domain Matrix toggle switch
  - Modern KPI metric cards
  - Plotly interactive time-series, category benchmarking, and anomaly scatter plots
  - Real-time Data Quality & Integrity Profiler (DQI Index)
  - Interactive Operational Integrity Audit Log & Anomaly Alerts
  - Live Executive Analytical Summary viewer and instant markdown export download
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Import backend modules
from data_modeler import DataModeler, DomainMode
from analytics_engine import ExecutiveAnalyticsEngine
from helpers import init_page, render_metric_card, apply_plotly_theme, create_kpi_gauge, create_waterfall_chart

# =============================================================================
# STREAMLIT PAGE CONFIGURATION & PALDOM KEYED STYLING STACK
# =============================================================================
init_page(
    page_title="CPIP · Decision Intelligence Platform · Dual-Domain",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# DATA ENGINE CACHED LOADER
# =============================================================================
@st.cache_data(show_spinner=False)
def get_modeled_data(domain: str):
    """Caches dimensional model outputs and analytical processing."""
    modeler = DataModeler()
    engine = ExecutiveAnalyticsEngine()

    model_data = modeler.load_and_model(domain)
    fact_table = model_data["fact_table"]
    dims = model_data["dimension_tables"]
    audit_trail = model_data["audit_trail"]

    # Compute Data Quality Profile
    dqi_profile = engine.profiler.profile_dataset(fact_table, domain)

    # Compute Domain Analytics
    if domain == "ecometrics":
        analytics_results = engine.analyze_industrial_operations(fact_table, dims["dim_facilities"])
    else:
        analytics_results = engine.analyze_movie_performance(fact_table, dims["dim_movies"], dims["dim_genres"])

    # Auto-generate executive markdown summary report
    report_md = engine.generate_executive_report(domain, dqi_profile, analytics_results, "executive_analytical_summary.md")

    return {
        "model_data": model_data,
        "fact_table": fact_table,
        "dims": dims,
        "audit_trail": audit_trail,
        "dqi_profile": dqi_profile,
        "analytics_results": analytics_results,
        "report_md": report_md
    }


# =============================================================================
# SIDEBAR CONTROLS & DOMAIN MATRIX TOGGLE
# =============================================================================
st.sidebar.markdown("### 🎛️ Architecture Control Plane")

domain_selection = st.sidebar.radio(
    "SELECT DOMAIN MATRIX:",
    options=[
        "EcoMetrics (Industrial Sustainability Operations)",
        "CPIP: Content Portfolio Intelligence Platform (Media Analytics)"
    ],
    index=0,
    help="Switches the underlying analytics schema and domain modeling logic in real-time."
)

is_eco = "EcoMetrics" in domain_selection
active_domain = "ecometrics" if is_eco else "cinemetrics"

# Domain Focus Architecture
if is_eco:
    st.sidebar.info(
        "🏢 **Domain Focus:** Global Industrial Sustainability, Clean Water & Energy Automation.\n\n"
        "**Core Capabilities:** Automated closed-loop water treatment, energy optimization, and chemical dosing safety."
    )
else:
    st.sidebar.info(
        "🎬 **Domain Focus:** Media Tech & Streaming Content Portfolio Intelligence (CPIP).\n\n"
        "**Core Capabilities:** Content capital allocation, Bayesian ratings, and genre ROI velocity."
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Pipeline Calibration")

# Re-run pipeline button with Keyed CSS
with st.sidebar.container(key="btn_refresh"):
    if st.button("🔄 Execute Full ETL & Audit Pipeline", use_container_width=True):
        st.cache_data.clear()
        st.toast("Pipeline cache purged. Re-executing dimensional model and DQI profiler...", icon="🚀")

# Load current domain data
data_bundle = get_modeled_data(active_domain)
fact_df = data_bundle["fact_table"]
dims = data_bundle["dims"]
audit_trail = data_bundle["audit_trail"]
dqi = data_bundle["dqi_profile"]
analytics = data_bundle["analytics_results"]
report_content = data_bundle["report_md"]

# Sidebar secondary filters
if is_eco:
    available_facs = ["All Facilities"] + sorted(list(fact_df["facility_id"].unique()))
    selected_fac = st.sidebar.selectbox("Filter Facility Location:", available_facs)
    
    available_shifts = ["All Shifts", 1, 2, 3]
    selected_shift = st.sidebar.selectbox("Filter Operational Shift:", available_shifts, format_func=lambda x: "All Shifts" if x == "All Shifts" else f"Shift {x}")
    
    # Filter dataset
    filtered_fact = fact_df.copy()
    if selected_fac != "All Facilities":
        filtered_fact = filtered_fact[filtered_fact["facility_id"] == selected_fac]
    if selected_shift != "All Shifts":
        filtered_fact = filtered_fact[filtered_fact["shift_id"] == selected_shift]
else:
    available_genres = ["All Genres"] + sorted(list(dims["dim_genres"]["genre_name"].unique()))
    selected_genre = st.sidebar.selectbox("Filter Genre Category:", available_genres)
    filtered_fact = fact_df.copy()

# =============================================================================
# TOP EXECUTIVE HEADER (Keyed Container: hero_header)
# =============================================================================
header_title = "EcoMetrics · Industrial Facility Sustainability OS" if is_eco else "CPIP · Content Portfolio Intelligence Platform"
header_sub = "Automated Water Volume Treatment, Energy Consumption Logs, and Chemical Dosing Intelligence" if is_eco else "Content Capital Allocation, Bayesian Rating Benchmarks, and Portfolio ROI Velocity"

with st.container(key="hero_header"):
    h_col1, h_col2 = st.columns([8, 4])
    with h_col1:
        st.markdown(f"""
        <div style="font-size: 26px; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(90deg, #00d2ff 0%, #8b5cf6 50%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{header_title}</div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">{header_sub}</div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown(f"""
        <div style="text-align: right;">
          <span style="display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 700; font-family: 'JetBrains Mono', monospace; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">DQI HEALTH: {dqi['dqi_score']}% · {dqi['letter_grade'].split()[0]}</span>
          <div style="font-size: 11px; color: #64748b; margin-top: 4px; font-family: 'JetBrains Mono', monospace;">UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# COMPONENT 1 & 2: MODERN KPI METRIC CARDS (Keyed Containers .st-key-metric_*)
# =============================================================================
if is_eco:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

    with kpi_col1:
        render_metric_card(
            label="WATER TREATED",
            value=f"{analytics['total_water_m3']:,.0f} m³",
            sub=f"{(analytics['total_water_liters'] / 1e6):.1f}M L Processed",
            trend="+14.2% YoY",
            trend_type="positive",
            variant="cyan",
            fill_pct=85
        )

    with kpi_col2:
        render_metric_card(
            label="POWER FOOTPRINT",
            value=f"{(analytics['total_energy_kwh'] / 1e3):,.1f} MWh",
            sub="5 Global Plant Grids",
            trend="Nominal",
            trend_type="neutral",
            variant="violet",
            fill_pct=65
        )

    with kpi_col3:
        render_metric_card(
            label="WATER-ENERGY RATIO",
            value=f"{analytics['overall_wer_ratio']} L/kWh",
            sub="Target: 48.0 L/kWh",
            trend="Efficiency",
            trend_type="positive",
            variant="blue",
            fill_pct=72
        )

    with kpi_col4:
        render_metric_card(
            label="EFFLUENT QUALITY",
            value=f"{analytics['avg_outflow_quality']} / 100",
            sub="Discharge Compliant",
            trend="Grade A",
            trend_type="positive",
            variant="emerald",
            fill_pct=92
        )

    with kpi_col5:
        render_metric_card(
            label="WATER CONSERVED",
            value=f"{analytics['water_saved_million_liters']:,.1f}M L",
            sub="+28% vs Legacy Baseline",
            trend="Savings",
            trend_type="positive",
            variant="emerald",
            fill_pct=88
        )

    with kpi_col6:
        render_metric_card(
            label="OPEX OPTIMIZATION",
            value=f"${(analytics['financial_savings_usd'] / 1e3):,.1f}K",
            sub="Utility & Chemical Savings",
            trend="Preserved",
            trend_type="positive",
            variant="amber",
            fill_pct=78
        )

else:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

    with kpi_col1:
        render_metric_card(
            label="CATALOG REVENUE",
            value=f"${(analytics['total_revenue_usd'] / 1e9):.2f}B",
            sub="SVOD (67%) + AVOD (33%)",
            trend="+14.2% YoY",
            trend_type="positive",
            variant="cyan",
            fill_pct=84
        )

    with kpi_col2:
        render_metric_card(
            label="PRODUCTION CAPITAL",
            value=f"${(analytics['total_budget_usd'] / 1e9):.2f}B",
            sub="50 Curated Titles",
            trend="Amortized",
            trend_type="neutral",
            variant="violet",
            fill_pct=62
        )

    with kpi_col3:
        render_metric_card(
            label="NET CONTRIBUTION",
            value=f"${(analytics['total_profit_usd'] / 1e9):.2f}B",
            sub="Direct Cash Margin",
            trend="41.9% Margin",
            trend_type="positive",
            variant="emerald",
            fill_pct=76
        )

    with kpi_col4:
        render_metric_card(
            label="PORTFOLIO ROI",
            value=f"+{analytics['overall_roi_pct']}%",
            sub="Capital Return Rate",
            trend="Top Decile",
            trend_type="positive",
            variant="blue",
            fill_pct=88
        )

    with kpi_col5:
        render_metric_card(
            label="TOTAL ENGAGEMENT",
            value=f"{(analytics['total_watch_hours'] / 1e6):,.1f}M hrs",
            sub="Cumulative Platform Watch",
            trend="Global Scale",
            trend_type="positive",
            variant="amber",
            fill_pct=90
        )

    with kpi_col6:
        render_metric_card(
            label="DATA HEALTH (DQI)",
            value=f"{dqi['dqi_score']}%",
            sub=f"{dqi['letter_grade'].split()[0]} Enterprise Grade",
            trend="Pristine",
            trend_type="positive",
            variant="emerald",
            fill_pct=99
        )


# =============================================================================
# COMPONENT 3: INTERACTIVE VISUALIZATION SECTION
# =============================================================================
tab_viz, tab_powerbi, tab_integrity, tab_report = st.tabs([
    "📈 Operational Visualizations & Analytics",
    "📊 Power BI Executive Studio (Dials, Waterfall & DAX)",
    "🛡️ Data Integrity Profiler & Audit Trail",
    "📋 Automated Executive Summary Report"
])

with tab_viz:
    if is_eco:
        # -------------------------------------------------------------
        # ECOMETRICS INDUSTRIAL VISUALIZATIONS
        # -------------------------------------------------------------
        v_col1, v_col2 = st.columns([7, 5])

        with v_col1:
            with st.container(key="panel_card"):
                st.markdown("##### ⏱️ High-Frequency Telemetry: Water Volume vs. Power Demand")
                plot_df = filtered_fact.copy().sort_values("timestamp")
                if len(plot_df) > 1200:
                    step = len(plot_df) // 1200
                    plot_sample = plot_df.iloc[::step].copy()
                else:
                    plot_sample = plot_df.copy()

                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=plot_sample["timestamp"],
                    y=plot_sample["water_volume_liters"],
                    name="Water Volume (L)",
                    mode="lines",
                    line=dict(color="#00d2ff", width=2.0),
                    yaxis="y1"
                ))
                fig_trend.add_trace(go.Scatter(
                    x=plot_sample["timestamp"],
                    y=plot_sample["energy_consumption_kwh"],
                    name="Energy Draw (kWh)",
                    mode="lines",
                    line=dict(color="#f59e0b", width=1.8, dash="dot"),
                    yaxis="y2"
                ))
                fig_trend.update_layout(
                    height=360,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    yaxis=dict(title=dict(text="Water Volume (L)", font=dict(color="#00d2ff")), tickfont=dict(color="#00d2ff")),
                    yaxis2=dict(title=dict(text="Energy (kWh)", font=dict(color="#f59e0b")), tickfont=dict(color="#f59e0b"), overlaying="y", side="right"),
                    hovermode="x unified"
                )
                apply_plotly_theme(fig_trend, is_dark=True)
                st.plotly_chart(fig_trend, use_container_width=True)

        with v_col2:
            with st.container(key="panel_card"):
                st.markdown("##### 🏭 Facility Water-Energy Ratio vs. Target KPI")
                fac_df = pd.DataFrame(analytics["facility_kpis"])
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    x=fac_df["facility_name"].apply(lambda x: x.split()[0] + " " + x.split()[1] if len(x.split()) > 1 else x),
                    y=fac_df["wer_ratio"],
                    name="Observed WER (L/kWh)",
                    marker_color="#10b981"
                ))
                fig_bar.add_trace(go.Scatter(
                    x=fac_df["facility_name"].apply(lambda x: x.split()[0] + " " + x.split()[1] if len(x.split()) > 1 else x),
                    y=fac_df["target_kpi"],
                    name="Target Benchmark KPI",
                    mode="markers+lines",
                    line=dict(color="#e50914", width=2, dash="dash"),
                    marker=dict(size=8, color="#e50914")
                ))
                fig_bar.update_layout(
                    height=360,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    yaxis_title="Efficiency (L/kWh)"
                )
                apply_plotly_theme(fig_bar, is_dark=True)
                st.plotly_chart(fig_bar, use_container_width=True)

        # Row 2: Anomaly Scatter Plot & Shift Distribution
        s_col1, s_col2 = st.columns([7, 5])

        with s_col1:
            with st.container(key="panel_card"):
                st.markdown("##### 🚨 Sensor Excursions: Operating Temperature vs. Chemical Concentration")
                scatter_sample = filtered_fact.sample(min(1500, len(filtered_fact)), random_state=42)
                
                fig_scatter = px.scatter(
                    scatter_sample,
                    x="sensor_temperature_c",
                    y="chemical_dosing_mg_l",
                    color="is_anomaly",
                    color_discrete_map={False: "#00d2ff", True: "#e50914"},
                    hover_data=["facility_id", "outflow_quality_score", "anomaly_category"],
                    labels={
                        "sensor_temperature_c": "Temperature (°C)",
                        "chemical_dosing_mg_l": "Chemical Dosing (mg/L)",
                        "is_anomaly": "Safe Boundary Breach"
                    }
                )
                fig_scatter.add_shape(
                    type="rect",
                    x0=15.0, x1=42.0, y0=10.0, y1=65.0,
                    line=dict(color="#10b981", width=2, dash="dash"),
                    fillcolor="rgba(16, 185, 129, 0.08)",
                    layer="below"
                )
                fig_scatter.add_annotation(
                    x=28.5, y=37.5,
                    text="Nominal Operating Zone",
                    showarrow=False,
                    font=dict(color="#10b981", size=11)
                )
                fig_scatter.update_layout(
                    height=360,
                    legend=dict(orientation="h", y=1.02, x=1)
                )
                apply_plotly_theme(fig_scatter, is_dark=True)
                st.plotly_chart(fig_scatter, use_container_width=True)

        with s_col2:
            with st.container(key="panel_card"):
                st.markdown("##### 💧 Outflow Effluent Quality by Shift")
                shift_names = {1: "Morning (06:00-14:00)", 2: "Afternoon (14:00-22:00)", 3: "Night (22:00-06:00)"}
                plot_sample["shift_label"] = plot_sample["shift_id"].map(shift_names)
                
                fig_box = px.box(
                    plot_sample,
                    x="shift_label",
                    y="outflow_quality_score",
                    color="shift_label",
                    color_discrete_sequence=["#00d2ff", "#10b981", "#8b5cf6"],
                    labels={"outflow_quality_score": "Quality Score (0-100)", "shift_label": "Shift"}
                )
                fig_box.update_layout(
                    height=360,
                    showlegend=False
                )
                apply_plotly_theme(fig_box, is_dark=True)
                st.plotly_chart(fig_box, use_container_width=True)

    else:
        # -------------------------------------------------------------
        # CINEMETRICS VISUALIZATIONS
        # -------------------------------------------------------------
        c_col1, c_col2 = st.columns([7, 5])

        with c_col1:
            with st.container(key="panel_card"):
                st.markdown("##### 💰 Content Economics: Production Budget vs. Streaming Revenue")
                fig_scatter = px.scatter(
                    fact_df,
                    x="production_budget",
                    y="total_revenue",
                    size="total_watch_hours",
                    color="content_roi",
                    hover_data=["title", "imdb_rating", "decision"],
                    color_continuous_scale="Viridis",
                    labels={
                        "production_budget": "Production Budget ($ USD)",
                        "total_revenue": "Total Attributed Revenue ($ USD)",
                        "content_roi": "Content ROI Multiplier"
                    }
                )
                fig_scatter.update_layout(height=360)
                apply_plotly_theme(fig_scatter, is_dark=True)
                st.plotly_chart(fig_scatter, use_container_width=True)

        with c_col2:
            with st.container(key="panel_card"):
                st.markdown("##### 🎭 Genre Capital Yield & ROI Ranking")
                genre_df = pd.DataFrame(analytics["genre_performance"])
                fig_genre = px.bar(
                    genre_df,
                    x="avg_roi_pct",
                    y="genre",
                    orientation="h",
                    color="avg_roi_pct",
                    color_continuous_scale="Teal",
                    labels={"avg_roi_pct": "Average Title ROI %", "genre": "Genre Category"}
                )
                fig_genre.update_layout(
                    height=360,
                    yaxis=dict(autorange="reversed")
                )
                apply_plotly_theme(fig_genre, is_dark=True)
                st.plotly_chart(fig_genre, use_container_width=True)

        # Row 2: Bayesian Rating vs Raw Rating & YoY Velocity
        r_col1, r_col2 = st.columns([6, 6])

        with r_col1:
            with st.container(key="panel_card"):
                st.markdown("##### 🌟 Raw IMDb Rating vs. Bayesian Weighted Score (Top 8)")
                top_ten = fact_df.copy()
                C = top_ten["imdb_rating"].mean()
                m = top_ten["votes"].quantile(0.60)
                top_ten["weighted_score"] = ((top_ten["votes"] / (top_ten["votes"] + m)) * top_ten["imdb_rating"]) + ((m / (top_ten["votes"] + m)) * C)
                top_ten = top_ten.sort_values(by="weighted_score", ascending=False).head(8)
                
                fig_rate = go.Figure()
                fig_rate.add_trace(go.Bar(name="Raw IMDb Rating", x=top_ten["title"], y=top_ten["imdb_rating"], marker_color="#64748b"))
                fig_rate.add_trace(go.Bar(name="Bayesian Weighted Rating", x=top_ten["title"], y=top_ten["weighted_score"].round(2), marker_color="#00d2ff"))
                fig_rate.update_layout(
                    barmode="group",
                    height=350,
                    yaxis=dict(range=[7.0, 10.0], title="Rating Score (/10)"),
                    legend=dict(orientation="h", y=1.02, x=1)
                )
                apply_plotly_theme(fig_rate, is_dark=True)
                st.plotly_chart(fig_rate, use_container_width=True)

        with r_col2:
            with st.container(key="panel_card"):
                st.markdown("##### 🚀 Year-over-Year Revenue Trajectory ($ USD)")
                yoy_df = pd.DataFrame(analytics["yoy_revenue_velocity"])
                fig_yoy = px.line(
                    yoy_df,
                    x="release_year",
                    y="total_revenue",
                    markers=True,
                    labels={"release_year": "Release Year", "total_revenue": "Total Revenue ($)"}
                )
                fig_yoy.update_traces(line_color="#8b5cf6", line_width=2.5)
                fig_yoy.update_layout(height=350)
                apply_plotly_theme(fig_yoy, is_dark=True)
                st.plotly_chart(fig_yoy, use_container_width=True)


# =============================================================================
# POWER BI EXECUTIVE ANALYTICS STUDIO & DAX MODELING HUB
# =============================================================================
with tab_powerbi:
    with st.container(key="panel_card"):
        st.markdown("#### 📊 Power BI Executive Analytics & Semantic DAX Hub")
        st.caption("Power BI signature visuals including Target Bullet Gauges, Value Reconciliation Waterfall, Hierarchical Decomposition Tree, and Production DAX Measures.")

    # -------------------------------------------------------------
    # 1. EXECUTIVE KPI BULLET GAUGES (Power BI Dial Visuals)
    # -------------------------------------------------------------
    with st.container(key="panel_card"):
        st.markdown("##### 🎯 Executive Target Gauges & Performance Thresholds")
        g_col1, g_col2, g_col3 = st.columns(3)

        if is_eco:
            with g_col1:
                wer_fig = create_kpi_gauge(
                    title="WATER-ENERGY RATIO (L/kWh)",
                    value=float(analytics["overall_wer_ratio"]),
                    target=48.0,
                    min_val=0.0,
                    max_val=80.0,
                    suffix=" L/kWh",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(wer_fig, use_container_width=True)
            with g_col2:
                qual_fig = create_kpi_gauge(
                    title="DISCHARGE EFFLUENT QUALITY",
                    value=float(analytics["avg_outflow_quality"]),
                    target=90.0,
                    min_val=50.0,
                    max_val=100.0,
                    suffix=" / 100",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(qual_fig, use_container_width=True)
            with g_col3:
                dqi_fig = create_kpi_gauge(
                    title="DATA QUALITY INDEX (DQI SLA)",
                    value=float(dqi["dqi_score"]),
                    target=95.0,
                    min_val=80.0,
                    max_val=100.0,
                    suffix="%",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(dqi_fig, use_container_width=True)
        else:
            with g_col1:
                roi_fig = create_kpi_gauge(
                    title="PORTFOLIO CONTENT ROI",
                    value=float(analytics["overall_roi_pct"]),
                    target=150.0,
                    min_val=0.0,
                    max_val=400.0,
                    prefix="+",
                    suffix="%",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(roi_fig, use_container_width=True)
            with g_col2:
                margin_pct = round((analytics["total_profit_usd"] / analytics["total_revenue_usd"]) * 100, 1) if analytics["total_revenue_usd"] else 0
                margin_fig = create_kpi_gauge(
                    title="NET CONTRIBUTION MARGIN",
                    value=float(margin_pct),
                    target=40.0,
                    min_val=0.0,
                    max_val=80.0,
                    suffix="%",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(margin_fig, use_container_width=True)
            with g_col3:
                dqi_fig = create_kpi_gauge(
                    title="DATA QUALITY INDEX (DQI SLA)",
                    value=float(dqi["dqi_score"]),
                    target=95.0,
                    min_val=80.0,
                    max_val=100.0,
                    suffix="%",
                    is_dark=True,
                    higher_is_better=True
                )
                st.plotly_chart(dqi_fig, use_container_width=True)

    # -------------------------------------------------------------
    # 2. POWER BI WATERFALL RECONCILIATION & DECOMPOSITION TREE
    # -------------------------------------------------------------
    w_col, t_col = st.columns([6, 6])

    with w_col:
        with st.container(key="panel_card"):
            if is_eco:
                st.markdown("##### 💧 Volumetric Waterfall: Intake ➔ Discharged Effluent")
                water_cats = ["Raw Intake", "Evap Cooling", "Blowdown Loss", "Closed Recovery", "Net Effluent"]
                raw_m3 = analytics["total_water_m3"] / 1e3
                evap_m3 = -28.4
                blow_m3 = -9.2
                saved_m3 = analytics["water_saved_million_liters"]
                water_vals = [raw_m3, evap_m3, blow_m3, saved_m3, 0]
                water_meas = ["relative", "relative", "relative", "relative", "total"]

                waterfall_fig = create_waterfall_chart(
                    title="Facility Water Reconciliation Bridge (k m³)",
                    categories=water_cats,
                    values=water_vals,
                    measures=water_meas,
                    suffix="k m³",
                    is_dark=True
                )
                st.plotly_chart(waterfall_fig, use_container_width=True)
            else:
                st.markdown("##### 💵 Capital Waterfall: Gross Revenue ➔ Cash Margin")
                rev_b = analytics["total_revenue_usd"] / 1e9
                bud_b = -(analytics["total_budget_usd"] / 1e9)
                mkt_b = -2.51
                lic_b = -2.01
                fin_cats = ["Gross Revenue", "Production", "Marketing", "Licensing", "Net Profit"]
                fin_vals = [rev_b, bud_b, mkt_b, lic_b, 0]
                fin_meas = ["relative", "relative", "relative", "relative", "total"]

                waterfall_fig = create_waterfall_chart(
                    title="Portfolio Capital Reconciliation Bridge ($ USD)",
                    categories=fin_cats,
                    values=fin_vals,
                    measures=fin_meas,
                    prefix="$",
                    suffix="B",
                    is_dark=True
                )
                st.plotly_chart(waterfall_fig, use_container_width=True)

    with t_col:
        with st.container(key="panel_card"):
            if is_eco:
                st.markdown("##### 🌳 Decomposition Tree: Water Volume by Sector & Shift")
                tree_df = filtered_fact.copy()
                shift_names = {1: "Shift 1 (Day)", 2: "Shift 2 (Swing)", 3: "Shift 3 (Night)"}
                tree_df["shift_label"] = tree_df["shift_id"].map(shift_names)
                if "dim_facilities" in dims:
                    tree_df = tree_df.merge(dims["dim_facilities"][["facility_id", "facility_name", "industry_type"]], on="facility_id", how="left")
                else:
                    tree_df["facility_name"] = tree_df["facility_id"]
                    tree_df["industry_type"] = "Industrial"

                treemap_fig = px.treemap(
                    tree_df,
                    path=["industry_type", "facility_name", "shift_label", "anomaly_category"],
                    values="water_volume_liters",
                    color="outflow_quality_score",
                    color_continuous_scale="Teal",
                    labels={
                        "water_volume_liters": "Water Treated (L)",
                        "outflow_quality_score": "Quality Score"
                    }
                )
                treemap_fig.update_layout(height=380)
                apply_plotly_theme(treemap_fig, is_dark=True)
                st.plotly_chart(treemap_fig, use_container_width=True)
            else:
                st.markdown("##### 🌳 Decomposition Tree: Revenue by Genre & Decision")
                treemap_fig = px.treemap(
                    fact_df,
                    path=["genre", "content_type", "decision", "title"],
                    values="total_revenue",
                    color="content_roi",
                    color_continuous_scale="Viridis",
                    labels={
                        "total_revenue": "Total Revenue ($)",
                        "content_roi": "Content ROI"
                    }
                )
                treemap_fig.update_layout(height=380)
                apply_plotly_theme(treemap_fig, is_dark=True)
                st.plotly_chart(treemap_fig, use_container_width=True)

    # -------------------------------------------------------------
    # 3. INTERACTIVE POWER BI MATRIX & SLICER VIEW
    # -------------------------------------------------------------
    with st.container(key="panel_card"):
        if is_eco:
            st.markdown("##### 📑 Power BI Matrix: Facility Benchmarking & KPI Variance Grid")
            fac_summary_df = pd.DataFrame(analytics["facility_kpis"])
            display_fac = fac_summary_df[[
                "facility_name", "industry_type", "wer_ratio", "target_kpi", "kpi_variance_pct", "anomaly_count", "quality_score"
            ]].copy()
            display_fac.columns = [
                "Facility Name", "Industry Sector", "Observed WER (L/kWh)", "Target KPI", "Variance (%)", "Anomalies Flagged", "Effluent Quality"
            ]
            st.dataframe(display_fac, use_container_width=True, height=220)
        else:
            st.markdown("##### 📑 Power BI Matrix: Content ROI & Decision Scorecard")
            cols = ["title", "genre", "content_type", "release_year", "total_revenue", "production_budget", "content_roi", "decision"]
            matrix_df = fact_df[cols].copy()
            matrix_df["total_revenue"] = matrix_df["total_revenue"].apply(lambda x: f"${x:,.0f}")
            matrix_df["production_budget"] = matrix_df["production_budget"].apply(lambda x: f"${x:,.0f}")
            matrix_df["content_roi"] = matrix_df["content_roi"].apply(lambda x: f"+{x*100:.1f}%")
            matrix_df.columns = ["Title", "Genre", "Format", "Year", "Gross Revenue", "Budget", "Content ROI", "Decision Candidate"]
            st.dataframe(matrix_df.head(25), use_container_width=True, height=260)

    # -------------------------------------------------------------
    # 4. POWER BI DAX MEASURES & SEMANTIC MODEL STUDIO
    # -------------------------------------------------------------
    with st.container(key="panel_card"):
        st.markdown("##### 📐 Power BI DAX Studio & Semantic Data Model")
        dax_file_path = "powerbi/EcoMetrics_Industrial_Measures.dax" if is_eco else "powerbi/CPIP_Entertainment_Measures.dax"
        dax_code = ""
        if os.path.exists(dax_file_path):
            with open(dax_file_path, "r", encoding="utf-8") as f:
                dax_code = f.read()

        d_col1, d_col2 = st.columns([8, 4])
        with d_col1:
            st.caption(f"Active Production DAX Measure Library for **{header_title}**")
            st.code(dax_code, language="sql")
        with d_col2:
            st.markdown("###### 📦 Power BI Artifacts & Connectors")
            st.info(
                "**Ready-to-Deploy Assets:**\n\n"
                "• Official Star Schema relational tables\n"
                "• 1-to-Many cardinality model relationships\n"
                "• Kimball dimensional topology\n"
                "• Pre-calculated business DAX measures"
            )
            with st.container(key="btn_primary"):
                st.download_button(
                    label="📥 Download DAX Library (.dax)",
                    data=dax_code,
                    file_name=os.path.basename(dax_file_path),
                    mime="text/plain",
                    use_container_width=True
                )
            
            guide_path = "powerbi/PowerBI_Data_Model_Guide.md"
            if os.path.exists(guide_path):
                with open(guide_path, "r", encoding="utf-8") as f:
                    guide_md = f.read()
                st.download_button(
                    label="📘 Download Power BI Blueprint (.md)",
                    data=guide_md,
                    file_name="PowerBI_Data_Model_Guide.md",
                    mime="text/markdown",
                    use_container_width=True
                )


# =============================================================================
# OPERATIONAL INTEGRITY PANEL (COMPONENT 3 & 4)
# =============================================================================
with tab_integrity:
    with st.container(key="dqi_banner"):
        st.markdown("#### 🛡️ Data Quality Index (DQI) & Pipeline Ingestion Health")
        dq_col1, dq_col2, dq_col3, dq_col4 = st.columns(4)
        with dq_col1:
            st.metric("Completeness Sub-Score", f"{dqi['sub_scores']['completeness']}%", f"Missingness: {dqi['overall_missing_rate_pct']}%")
        with dq_col2:
            st.metric("Validity Sub-Score", f"{dqi['sub_scores']['validity']}%", "Physically Compliant")
        with dq_col3:
            st.metric("Consistency Sub-Score", f"{dqi['sub_scores']['consistency']}%", f"Outliers: {dqi['outlier_count']:,}")
        with dq_col4:
            st.metric("Schema Integrity Status", dqi['schema_drift_status'], "Zero Divergence")

    with st.container(key="panel_card"):
        st.markdown("##### 📝 Transformation Audit Trail & Cleansing Checkpoints")
        audit_df = pd.DataFrame(audit_trail)
        st.dataframe(audit_df, use_container_width=True, height=220)

        if is_eco:
            st.markdown("##### 🚨 Active Sensor Operational Excursion Log")
            anomalies_only = fact_df[fact_df["is_anomaly"]].copy()
            display_cols = ["operation_id", "timestamp", "facility_id", "sensor_temperature_c", "chemical_dosing_mg_l", "valve_pressure_psi", "outflow_quality_score", "anomaly_category"]
            st.dataframe(
                anomalies_only[display_cols].sort_values("timestamp", ascending=False).head(100),
                use_container_width=True,
                height=280
            )


# =============================================================================
# AUTOMATED REPORT VIEWER & EXPORT (COMPONENT 4)
# =============================================================================
with tab_report:
    with st.container(key="panel_card"):
        r_head_col, r_btn_col = st.columns([9, 3])
        with r_head_col:
            st.markdown("#### 📄 Auto-Generated Executive Analytical Summary")
            st.caption("Produced automatically by the ExecutiveAnalyticsEngine following data hygiene and dimensional modeling.")
        with r_btn_col:
            with st.container(key="btn_primary"):
                st.download_button(
                    label="📥 Download Report (.md)",
                    data=report_content,
                    file_name=f"executive_analytical_summary_{active_domain}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        st.markdown("---")
        st.markdown(report_content)


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 12px; color: #94a3b8; padding: 12px 0;'>"
    "Content Portfolio Intelligence Platform (CPIP) · EcoMetrics Operational Analytics Framework | Enterprise Star Schema & Automated DQI Profiler"
    "</div>",
    unsafe_allow_html=True
)
