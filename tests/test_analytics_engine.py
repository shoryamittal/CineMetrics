"""
Unit and Integration Tests for AnalyticsEngine and DataQualityProfiler.
Tests Data Quality Index (DQI) calculations, schema drift detection,
Bayesian weighted ratings, industrial efficiency ratios (WER), and
automated executive report generation.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from analytics_engine import DataQualityProfiler, ExecutiveAnalyticsEngine
from data_modeler import DataModeler


@pytest.fixture
def profiler():
    """Initializes DataQualityProfiler instance."""
    return DataQualityProfiler()


@pytest.fixture
def engine():
    """Initializes ExecutiveAnalyticsEngine instance."""
    return ExecutiveAnalyticsEngine()


@pytest.fixture
def sample_clean_telemetry():
    """Creates a pristine industrial fact dataframe."""
    return pd.DataFrame({
        "timestamp": pd.date_range("2026-03-01", periods=100, freq="15min"),
        "facility_id": ["Facility_A"] * 50 + ["Facility_B"] * 50,
        "water_volume_liters": np.random.uniform(15000, 22000, 100),
        "energy_consumption_kwh": np.random.uniform(400, 600, 100),
        "chemical_dosing_mg_l": np.random.uniform(20, 35, 100),
        "sensor_temperature_c": np.random.uniform(22, 28, 100),
        "outflow_quality_score": np.random.uniform(92, 98, 100),
        "valve_pressure_psi": np.random.uniform(65, 80, 100),
        "ph_level": np.random.uniform(7.1, 7.6, 100),
        "is_anomaly": [False] * 100,
        "anomaly_category": ["NOMINAL"] * 100
    })


@pytest.fixture
def sample_facilities_dim():
    """Creates a sample facilities dimension dataframe."""
    return pd.DataFrame([
        {
            "facility_id": "Facility_A",
            "facility_name": "Naperville Global Technology Center",
            "location": "Naperville, IL, USA",
            "region": "North America",
            "industry_type": "Food & Beverage Processing",
            "target_efficiency_kpi": 48.5,
            "active_sensors_count": 128
        },
        {
            "facility_id": "Facility_B",
            "facility_name": "Gary Chemical Operations",
            "location": "Gary, IN, USA",
            "region": "North America",
            "industry_type": "Heavy Manufacturing",
            "target_efficiency_kpi": 34.0,
            "active_sensors_count": 94
        }
    ])


class TestDataQualityProfiler:
    """Test suite for DataQualityProfiler."""

    def test_weights_configuration(self, profiler):
        """Verifies profiler weights sum exactly to 1.0."""
        total_weight = sum(profiler.weights.values())
        assert pytest.approx(total_weight, 0.001) == 1.0

    def test_clean_dataset_dqi_score(self, profiler, sample_clean_telemetry):
        """Verifies clean telemetry receives a pristine DQI score (>= 95.0%)."""
        profile = profiler.profile_dataset(sample_clean_telemetry, domain="ecometrics")
        assert profile["dqi_score"] >= 95.0
        assert "A+" in profile["letter_grade"]
        assert profile["overall_missing_rate_pct"] == 0.0
        assert profile["outlier_count"] == 0
        assert profile["schema_drift_status"] == "STABLE"

    def test_degraded_dataset_dqi(self, profiler):
        """Verifies dataset with missing values and outliers receives penalty."""
        degraded_df = pd.DataFrame({
            "timestamp": pd.date_range("2026-03-01", periods=50, freq="15min"),
            "facility_id": ["Facility_A"] * 50,
            "water_volume_liters": [np.nan] * 20 + [15000.0] * 30,  # 40% missing
            "energy_consumption_kwh": [500.0] * 50,
            "sensor_temperature_c": [85.0] * 25 + [22.0] * 25,     # 25 outliers (>42)
            "outflow_quality_score": [92.0] * 50,
            "ph_level": [-2.0] * 10 + [7.2] * 40                  # 10 invalid pH (<0)
        })

        profile = profiler.profile_dataset(degraded_df, domain="ecometrics")
        assert profile["dqi_score"] < 85.0
        assert profile["missing_cells_count"] > 0
        assert profile["outlier_count"] >= 25
        assert profile["sub_scores"]["completeness"] < 100.0

    def test_schema_drift_detection(self, profiler):
        """Verifies detection and scoring when expected schema columns are omitted."""
        # Missing "sensor_temperature_c" and "energy_consumption_kwh"
        drifted_df = pd.DataFrame({
            "timestamp": pd.date_range("2026-03-01", periods=10, freq="15min"),
            "facility_id": ["Facility_A"] * 10,
            "water_volume_liters": [15000.0] * 10,
        })

        profile = profiler.profile_dataset(drifted_df, domain="ecometrics")
        assert "DRIFT_DETECTED" in profile["schema_drift_status"]
        assert profile["sub_scores"]["schema_integrity"] == 60.0

    def test_empty_dataframe_profiling(self, profiler):
        """Verifies graceful handling of an empty dataframe without unhandled exceptions."""
        empty_df = pd.DataFrame(columns=["timestamp", "facility_id", "water_volume_liters"])
        profile = profiler.profile_dataset(empty_df, domain="ecometrics")
        assert profile["total_records"] == 0
        assert profile["missing_cells_count"] == 0
        assert profile["overall_missing_rate_pct"] == 0.0


class TestExecutiveAnalyticsEngine:
    """Test suite for ExecutiveAnalyticsEngine."""

    def test_industrial_operations_analysis(self, engine, sample_clean_telemetry, sample_facilities_dim):
        """Verifies industrial operational KPI analytics."""
        results = engine.analyze_industrial_operations(sample_clean_telemetry, sample_facilities_dim)

        assert results["domain"] == "ecometrics"
        assert results["total_water_liters"] > 0
        assert results["total_energy_kwh"] > 0
        assert results["overall_wer_ratio"] > 0
        assert results["water_saved_million_liters"] > 0
        assert results["financial_savings_usd"] > 0

        # Check facility KPIs
        assert len(results["facility_kpis"]) == 2
        fac_ids = [f["facility_id"] for f in results["facility_kpis"]]
        assert "Facility_A" in fac_ids
        assert "Facility_B" in fac_ids

        # Verify savings breakdown
        savings = results["savings_breakdown_usd"]
        assert "water_volumetric_savings" in savings
        assert "energy_efficiency_savings" in savings
        assert "chemical_waste_reduction" in savings

        # Verify natural language recommendations
        assert len(results["recommendations"]) >= 1

    def test_movie_performance_analytics(self, engine):
        """Verifies Bayesian ratings, genre ROI, and revenue velocity from real catalog."""
        modeler = DataModeler()
        movie_model = modeler.model_movie_domain()

        results = engine.analyze_movie_performance(
            movie_model["fact_table"],
            movie_model["dimension_tables"]["dim_movies"],
            movie_model["dimension_tables"]["dim_genres"]
        )

        assert results["domain"] == "cinemetrics"
        assert results["total_revenue_usd"] > 0
        assert results["total_budget_usd"] > 0
        assert results["total_profit_usd"] > 0

        # Bayesian rating checks
        top_titles = results["top_weighted_titles"]
        assert len(top_titles) == 5
        # Weighted ratings must be reasonable IMDb range (1.0 to 10.0)
        for t in top_titles:
            assert 1.0 <= t["weighted_rating"] <= 10.0

        # Genre performance checks
        genres = results["genre_performance"]
        assert len(genres) >= 5
        # Verify genres are sorted in descending order of avg_roi_pct
        for i in range(len(genres) - 1):
            assert genres[i]["avg_roi_pct"] >= genres[i + 1]["avg_roi_pct"]

        # Recommendations generated
        assert len(results["recommendations"]) >= 3

    def test_executive_report_generation(self, engine, tmp_path):
        """Verifies executive markdown summary report formatting and disk persistence."""
        modeler = DataModeler()
        eco_model = modeler.load_and_model("ecometrics")

        dqi = engine.profiler.profile_dataset(eco_model["fact_table"], "ecometrics")
        analytics = engine.analyze_industrial_operations(
            eco_model["fact_table"],
            eco_model["dimension_tables"]["dim_facilities"]
        )

        report_file = tmp_path / "test_executive_summary.md"
        content = engine.generate_executive_report(
            "ecometrics",
            dqi,
            analytics,
            str(report_file)
        )

        assert report_file.exists()
        assert "# 🌐 Enterprise Executive Analytical Summary" in content
        assert "Data Quality & Integrity Profiler (DQI)" in content
        assert "Executive Operational KPI Summary" in content
        assert "Global Facility Efficiency Breakdown" in content
        assert "Strategic Executive Recommendations" in content
