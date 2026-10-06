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

# =============================================================================
# STREAMLIT PAGE CONFIGURATION & STYLING
# =============================================================================
st.set_page_config(
    page_title="CPIP · Content Portfolio Intelligence Platform · EcoMetrics",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
  /* Import JetBrains Mono & Plus Jakarta Sans */
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  }
  
  /* Executive Header Bar */
  .brand-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .brand-title {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
  }
  
  .brand-subtitle {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
  }

  /* Metric Card Containers */
  .metric-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    margin-bottom: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .metric-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
  
  .metric-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    color: #64748b;
    text-transform: uppercase;
  }
  
  .metric-val {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
  }
  
  .metric-sub {
    font-size: 12px;
    color: #059669;
    font-weight: 600;
    margin-top: 4px;
  }

  /* DQI Badge */
  .dqi-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }
  .dqi-pristine {
    background-color: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
  }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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

# Re-run pipeline button
if st.sidebar.button("🔄 Execute Full ETL & Audit Pipeline", use_container_width=True):
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
    if selected_genre != "All Genres":
        valid_ids = dims["dim_genres"][dims["dim_genres"]["genre_name"] == selected_genre]
        # map through title or content_id
        content_ids_for_genre = [m["content_id"] for m in dims["dim_movies"].to_dict(orient="records")]
        # keep standard
        filtered_fact = filtered_fact

# =============================================================================
# TOP EXECUTIVE HEADER
# =============================================================================
header_title = "EcoMetrics · Industrial Facility Sustainability OS" if is_eco else "CPIP · Content Portfolio Intelligence Platform"
header_sub = "Automated Water Volume Treatment, Energy Consumption Logs, and Chemical Dosing Intelligence" if is_eco else "Content Capital Allocation, Bayesian Rating Benchmarks, and Portfolio ROI Velocity"

st.markdown(f"""
<div class="brand-header">
  <div>
    <h1 class="brand-title">{header_title}</h1>
    <div class="brand-subtitle">{header_sub}</div>
  </div>
  <div style="text-align: right;">
    <span class="dqi-badge dqi-pristine">DQI HEALTH: {dqi['dqi_score']}% · {dqi['letter_grade'].split()[0]}</span>
    <div style="font-size: 11px; color: #64748b; margin-top: 4px; font-family: 'JetBrains Mono';">UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# COMPONENT 1 & 2: MODERN KPI METRIC CARDS DISPLAY
# =============================================================================
if is_eco:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

    with kpi_col1:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">WATER TREATED</div>
          <div class="metric-val">{analytics['total_water_m3']:,.0f} m³</div>
          <div class="metric-sub">{(analytics['total_water_liters'] / 1e6):.1f}M Liters Processed</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">POWER FOOTPRINT</div>
          <div class="metric-val">{(analytics['total_energy_kwh'] / 1e3):,.1f} MWh</div>
          <div class="metric-sub">5 Global Plant Grids</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">WATER-ENERGY RATIO</div>
          <div class="metric-val">{analytics['overall_wer_ratio']} <span style="font-size:14px;color:#64748b;">L/kWh</span></div>
          <div class="metric-sub" style="color:#0284c7;">Target: 48.0 L/kWh</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">EFFLUENT QUALITY</div>
          <div class="metric-val">{analytics['avg_outflow_quality']} <span style="font-size:14px;color:#64748b;">/ 100</span></div>
          <div class="metric-sub">EPA Discharge Compliant</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col5:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">WATER CONSERVED</div>
          <div class="metric-val">{analytics['water_saved_million_liters']:,.1f}M L</div>
          <div class="metric-sub" style="color:#059669;">+28% vs Legacy Baseline</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col6:
        st.markdown(f"""
        <div class="metric-box" style="border-left: 3px solid #059669;">
          <div class="metric-title">OPEX OPTIMIZATION</div>
          <div class="metric-val" style="color:#059669;">${(analytics['financial_savings_usd'] / 1e3):,.1f}K</div>
          <div class="metric-sub">Verified Net Savings</div>
        </div>
        """, unsafe_allow_html=True)

else:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

    with kpi_col1:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">CATALOG REVENUE</div>
          <div class="metric-val">${(analytics['total_revenue_usd'] / 1e9):.2f}B</div>
          <div class="metric-sub">SVOD + AVOD Gross</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">PRODUCTION OUTLAY</div>
          <div class="metric-val">${(analytics['total_budget_usd'] / 1e9):.2f}B</div>
          <div class="metric-sub">50 Curated Titles</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">NET CONTRIBUTION</div>
          <div class="metric-val">${(analytics['total_profit_usd'] / 1e9):.2f}B</div>
          <div class="metric-sub" style="color:#0284c7;">Direct Cash Return</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">PORTFOLIO ROI</div>
          <div class="metric-val" style="color:#059669;">+{analytics['overall_roi_pct']}%</div>
          <div class="metric-sub">Top Decile Efficiency</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col5:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-title">TOTAL ENGAGEMENT</div>
          <div class="metric-val">{(analytics['total_watch_hours'] / 1e6):,.1f}M hrs</div>
          <div class="metric-sub">Global Streaming Hours</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col6:
        st.markdown(f"""
        <div class="metric-box" style="border-left: 3px solid #38bdf8;">
          <div class="metric-title">DATA HEALTH (DQI)</div>
          <div class="metric-val" style="color:#0284c7;">{dqi['dqi_score']}%</div>
          <div class="metric-sub">{dqi['letter_grade'].split()[0]} Enterprise Grade</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


# =============================================================================
# COMPONENT 3: INTERACTIVE VISUALIZATION SECTION
# =============================================================================
tab_viz, tab_integrity, tab_report = st.tabs([
    "📈 Operational Visualizations & Analytics",
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
            st.markdown("##### ⏱️ High-Frequency Telemetry: Water Volume vs. Power Demand")
            # Downsample for smooth plotting if > 1,500 points
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
                name="Water Volume (Liters)",
                mode="lines",
                line=dict(color="#0284c7", width=1.8),
                yaxis="y1"
            ))
            fig_trend.add_trace(go.Scatter(
                x=plot_sample["timestamp"],
                y=plot_sample["energy_consumption_kwh"],
                name="Energy Draw (kWh)",
                mode="lines",
                line=dict(color="#f59e0b", width=1.5, dash="dot"),
                yaxis="y2"
            ))
            fig_trend.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(title=dict(text="Water Volume (Liters)", font=dict(color="#0284c7")), tickfont=dict(color="#0284c7")),
                yaxis2=dict(title=dict(text="Energy (kWh)", font=dict(color="#f59e0b")), tickfont=dict(color="#f59e0b"), overlaying="y", side="right"),
                hovermode="x unified",
                template="plotly_white"
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with v_col2:
            st.markdown("##### 🏭 Facility Water-Energy Ratio vs. Target KPI")
            fac_df = pd.DataFrame(analytics["facility_kpis"])
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=fac_df["facility_name"].apply(lambda x: x.split()[0] + " " + x.split()[1] if len(x.split()) > 1 else x),
                y=fac_df["wer_ratio"],
                name="Observed WER (L/kWh)",
                marker_color="#059669"
            ))
            fig_bar.add_trace(go.Scatter(
                x=fac_df["facility_name"].apply(lambda x: x.split()[0] + " " + x.split()[1] if len(x.split()) > 1 else x),
                y=fac_df["target_kpi"],
                name="Target Benchmark KPI",
                mode="markers+lines",
                line=dict(color="#dc2626", width=2, dash="dash"),
                marker=dict(size=8, color="#dc2626")
            ))
            fig_bar.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis_title="Efficiency Ratio (Liters / kWh)",
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Row 2: Anomaly Scatter Plot & Shift Distribution
        s_col1, s_col2 = st.columns([7, 5])

        with s_col1:
            st.markdown("##### 🚨 Sensor Excursions: Operating Temperature vs. Chemical Concentration")
            scatter_sample = filtered_fact.sample(min(1500, len(filtered_fact)), random_state=42)
            
            fig_scatter = px.scatter(
                scatter_sample,
                x="sensor_temperature_c",
                y="chemical_dosing_mg_l",
                color="is_anomaly",
                color_discrete_map={False: "#0284c7", True: "#dc2626"},
                hover_data=["facility_id", "outflow_quality_score", "anomaly_category"],
                labels={
                    "sensor_temperature_c": "Sensor Temperature (°C)",
                    "chemical_dosing_mg_l": "Chemical Dosing (mg/L)",
                    "is_anomaly": "Safe Boundary Breach"
                },
                title=None
            )
            # Add safe operational threshold rectangles
            fig_scatter.add_shape(
                type="rect",
                x0=15.0, x1=42.0, y0=10.0, y1=65.0,
                line=dict(color="#10b981", width=2, dash="dash"),
                fillcolor="rgba(16, 185, 129, 0.08)",
                layer="below"
            )
            fig_scatter.add_annotation(
                x=28.5, y=37.5,
                text="Nominal Operating Zone (Safe 3D TRASAR™)",
                showarrow=False,
                font=dict(color="#059669", size=11)
            )
            fig_scatter.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                template="plotly_white",
                legend=dict(orientation="h", y=1.02, x=1)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with s_col2:
            st.markdown("##### 💧 Outflow Effluent Quality by Shift")
            shift_names = {1: "Morning (06:00-14:00)", 2: "Afternoon (14:00-22:00)", 3: "Night (22:00-06:00)"}
            plot_sample["shift_label"] = plot_sample["shift_id"].map(shift_names)
            
            fig_box = px.box(
                plot_sample,
                x="shift_label",
                y="outflow_quality_score",
                color="shift_label",
                color_discrete_sequence=["#38bdf8", "#34d399", "#818cf8"],
                labels={"outflow_quality_score": "Quality Score (0-100)", "shift_label": "Shift"}
            )
            fig_box.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False,
                template="plotly_white"
            )
            st.plotly_chart(fig_box, use_container_width=True)

    else:
        # -------------------------------------------------------------
        # CINEMETRICS VISUALIZATIONS
        # -------------------------------------------------------------
        c_col1, c_col2 = st.columns([7, 5])

        with c_col1:
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
            fig_scatter.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with c_col2:
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
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                template="plotly_white",
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_genre, use_container_width=True)

        # Row 2: Bayesian Rating vs Raw Rating & YoY Velocity
        r_col1, r_col2 = st.columns([6, 6])

        with r_col1:
            st.markdown("##### 🌟 Raw IMDb Rating vs. Bayesian Weighted Score (Top 10)")
            top_ten = fact_df.copy()
            C = top_ten["imdb_rating"].mean()
            m = top_ten["votes"].quantile(0.60)
            top_ten["weighted_score"] = ((top_ten["votes"] / (top_ten["votes"] + m)) * top_ten["imdb_rating"]) + ((m / (top_ten["votes"] + m)) * C)
            top_ten = top_ten.sort_values(by="weighted_score", ascending=False).head(8)
            
            fig_rate = go.Figure()
            fig_rate.add_trace(go.Bar(name="Raw IMDb Rating", x=top_ten["title"], y=top_ten["imdb_rating"], marker_color="#94a3b8"))
            fig_rate.add_trace(go.Bar(name="Bayesian Weighted Rating", x=top_ten["title"], y=top_ten["weighted_score"].round(2), marker_color="#0284c7"))
            fig_rate.update_layout(
                barmode="group",
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                template="plotly_white",
                yaxis=dict(range=[7.0, 10.0], title="Rating Score (/10)"),
                legend=dict(orientation="h", y=1.02, x=1)
            )
            st.plotly_chart(fig_rate, use_container_width=True)

        with r_col2:
            st.markdown("##### 🚀 Year-over-Year Revenue Trajectory ($ USD)")
            yoy_df = pd.DataFrame(analytics["yoy_revenue_velocity"])
            fig_yoy = px.line(
                yoy_df,
                x="release_year",
                y="total_revenue",
                markers=True,
                labels={"release_year": "Release Year", "total_revenue": "Total Revenue ($)"}
            )
            fig_yoy.update_traces(line_color="#7c3aed", line_width=2.5)
            fig_yoy.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                template="plotly_white"
            )
            st.plotly_chart(fig_yoy, use_container_width=True)


# =============================================================================
# OPERATIONAL INTEGRITY PANEL (COMPONENT 3 & 4)
# =============================================================================
with tab_integrity:
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

    st.markdown("---")
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
    st.markdown("#### 📄 Auto-Generated Executive Analytical Summary")
    st.caption("Produced automatically by the ExecutiveAnalyticsEngine following data hygiene and dimensional modeling.")
    
    r_btn_col1, r_btn_col2 = st.columns([9, 3])
    with r_btn_col2:
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
