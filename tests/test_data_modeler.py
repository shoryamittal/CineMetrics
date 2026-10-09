"""
Unit and Integration Tests for DataModeler (The Data Engine).
Tests Star Schema Dimensional Modeling, Data Hygiene Checkpoints,
Canonical Mapping, Null Imputation, and Anomaly Tagging.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from data_modeler import DataModeler, DomainMode


@pytest.fixture
def modeler():
    """Initializes a fresh DataModeler instance."""
    return DataModeler()


@pytest.fixture
def synthetic_raw_telemetry_csv(tmp_path):
    """Creates a controlled raw telemetry CSV with intentional edge-case corruptions."""
    data = {
        "Timestamp": [
            "2026-03-01 06:15:00",
            "2026-03-01 14:30:00",
            "2026-03-01 23:45:00",
            "2026-03-02 02:00:00",
            "2026-03-02 10:00:00",
        ],
        "Facility_ID": [
            "FAC_A",            # Dirty alias -> Facility_A
            "FAC-B",            # Dirty alias -> Facility_B
            "PUNE_CAMPUS",      # Dirty alias -> Facility_C
            "ANTWERP_HUB",      # Dirty alias -> Facility_D
            "UNKNOWN_SITE",     # Unknown alias -> Facility_A (fallback)
        ],
        "Industry_Type": [
            "Food & Beverage",
            "Heavy Mfg",
            "Refinery",
            "Pharma",
            "Hyperscale",
        ],
        "Location": ["IL, USA", "IN, USA", "MH, India", "Belgium", "Mexico"],
        "Water_Volume_Liters": [12000.0, np.nan, 25000.0, 30000.0, np.nan],
        "Energy_Consumption_kWh": [400.0, 600.0, 800.0, 950.0, 500.0],
        "Chemical_Dosing_mg_L": [25.0, 35.0, np.nan, 45.0, np.nan],
        "Sensor_Temperature_C": [22.0, 48.0, 10.0, 30.0, 25.0],  # 48 is >42, 10 is <15
        "Outflow_Quality_Score": ["95.2", "ERROR_SENSOR", "80.0", "92.0", np.nan],
        "Valve_Pressure_PSI": [70.0, 115.0, 40.0, 80.0, 75.0],   # 115 is >100, 40 is <50
        "pH_Level": [7.2, 7.4, 7.1, 7.8, 7.3],
        "Raw_Anomaly_Tag": ["NONE", "SPIKE", "PRESSURE_DROP", "NONE", "NONE"]
    }
    df = pd.DataFrame(data)
    csv_file = tmp_path / "test_raw_telemetry.csv"
    df.to_csv(csv_file, index=False)
    return str(csv_file)


class TestDataModeler:
    """Test suite for DataModeler core logic."""

    def test_instantiation(self, modeler):
        """Verifies modeler initializes with canonical masters and empty audit trail."""
        assert len(modeler.CANONICAL_FACILITIES) == 5
        assert len(modeler.ALERT_THRESHOLDS) == 5
        assert modeler.audit_trail == []

    def test_checkpoint1_text_normalization(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies checkpoint 1 normalizes facility aliases to canonical keys."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        fact_df = result["fact_table"]

        assert fact_df.iloc[0]["facility_id"] == "Facility_A"
        assert fact_df.iloc[1]["facility_id"] == "Facility_B"
        assert fact_df.iloc[2]["facility_id"] == "Facility_C"
        assert fact_df.iloc[3]["facility_id"] == "Facility_D"
        assert fact_df.iloc[4]["facility_id"] == "Facility_A"  # Fallback

        # Check audit trail recorded TEXT_NORMALIZATION
        stages = [step["stage"] for step in result["audit_trail"]]
        assert "TEXT_NORMALIZATION" in stages

    def test_checkpoint1_type_coercion(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies checkpoint 1 coerces dirty string representations into numeric values."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        fact_df = result["fact_table"]

        # Row 0 was "95.2" -> float 95.2
        assert fact_df.iloc[0]["outflow_quality_score"] == 95.2
        # Row 1 was "ERROR_SENSOR" -> coerced to NaN, then imputed to 93.5 in Checkpoint 2
        assert fact_df.iloc[1]["outflow_quality_score"] == 93.5

    def test_checkpoint2_null_imputation(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies checkpoint 2 imputes missing water volume, chemical dosing, and quality."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        fact_df = result["fact_table"]

        # Ensure no NaNs remain in any operational column
        assert fact_df["water_volume_liters"].isna().sum() == 0
        assert fact_df["chemical_dosing_mg_l"].isna().sum() == 0
        assert fact_df["outflow_quality_score"].isna().sum() == 0

        # Row 4 quality was NaN -> benchmark 93.5
        assert fact_df.iloc[4]["outflow_quality_score"] == 93.5

    def test_checkpoint3_anomaly_tagging(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies checkpoint 3 tags physical safety boundary excursions."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        fact_df = result["fact_table"]

        # Row 0: Nominal operating conditions
        assert bool(fact_df.iloc[0]["is_anomaly"]) is False
        assert fact_df.iloc[0]["anomaly_category"] == "NOMINAL"

        # Row 1: Temp 48 (>42) and Pressure 115 (>100)
        assert bool(fact_df.iloc[1]["is_anomaly"]) is True
        assert "TEMPERATURE_BREACH" in fact_df.iloc[1]["anomaly_category"]
        assert "PRESSURE_FAULT" in fact_df.iloc[1]["anomaly_category"]

        # Row 2: Temp 10 (<15), Pressure 40 (<50), Quality 80 (<85)
        assert bool(fact_df.iloc[2]["is_anomaly"]) is True
        assert "TEMPERATURE_BREACH" in fact_df.iloc[2]["anomaly_category"]
        assert "PRESSURE_FAULT" in fact_df.iloc[2]["anomaly_category"]
        assert "QUALITY_DEGRADATION" in fact_df.iloc[2]["anomaly_category"]

    def test_star_schema_dimensions(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies dimensional tables adhere to Star Schema specifications."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        dims = result["dimension_tables"]

        # 1. dim_facilities
        assert "dim_facilities" in dims
        df_fac = dims["dim_facilities"]
        assert len(df_fac) == 5
        assert set(["facility_id", "facility_name", "location", "region", "industry_type", "target_efficiency_kpi"]).issubset(df_fac.columns)

        # 2. dim_time
        assert "dim_time" in dims
        df_time = dims["dim_time"]
        assert len(df_time) == 5
        assert set(["timestamp", "date_key", "date", "year", "quarter", "month", "hour", "shift_id", "shift_name", "is_weekend"]).issubset(df_time.columns)
        # Shift classifications: 06:15 is Morning (1), 14:30 is Afternoon (2), 23:45 is Night (3)
        assert df_time.iloc[0]["shift_id"] == 1
        assert df_time.iloc[1]["shift_id"] == 2
        assert df_time.iloc[2]["shift_id"] == 3

        # 3. dim_alerts
        assert "dim_alerts" in dims
        df_alerts = dims["dim_alerts"]
        assert len(df_alerts) == 5
        assert set(["alert_id", "metric_name", "safe_min", "safe_max", "priority"]).issubset(df_alerts.columns)

    def test_ecometrics_derived_kpis(self, modeler, synthetic_raw_telemetry_csv):
        """Verifies derived KPIs such as water-to-energy ratio (WER)."""
        result = modeler.model_ecometrics_domain(synthetic_raw_telemetry_csv)
        fact_df = result["fact_table"]

        assert "water_energy_ratio" in fact_df.columns
        # Row 0: 12000 L / 400 kWh = 30.0 L/kWh
        expected_wer = round(12000.0 / 400.0, 2)
        assert fact_df.iloc[0]["water_energy_ratio"] == expected_wer

    def test_movie_domain_catalog_modeling(self, modeler):
        """Verifies CineMetrics media domain Star Schema generation using real catalog.json."""
        catalog_path = modeler.base_dir / "dashboard" / "catalog.json"
        assert catalog_path.exists(), "catalog.json must exist in dashboard directory"

        result = modeler.model_movie_domain(str(catalog_path))
        assert result["domain"] == DomainMode.CINEMETRICS.value
        assert result["clean_record_count"] == 50

        fact_df = result["fact_table"]
        assert len(fact_df) == 50
        assert set(["content_id", "title", "production_budget", "licensing_cost", "total_revenue", "contribution_profit", "content_roi", "imdb_rating"]).issubset(fact_df.columns)

        # Verify profit and ROI mathematics: profit = revenue - costs
        first_row = fact_df.iloc[0]
        costs = first_row["production_budget"] + first_row["licensing_cost"] + first_row["marketing_spend"]
        expected_profit = first_row["total_revenue"] - costs
        assert first_row["contribution_profit"] == expected_profit

        # Verify Dimensions
        dims = result["dimension_tables"]
        assert "dim_movies" in dims
        assert "dim_genres" in dims
        assert "dim_creatives" in dims

        assert len(dims["dim_movies"]) == 50
        assert len(dims["dim_creatives"]) == 50
        assert len(dims["dim_genres"]) >= 5

    def test_load_and_model_dispatcher(self, modeler):
        """Verifies unified load_and_model dispatcher routes domains correctly."""
        eco_res = modeler.load_and_model("ecometrics")
        assert eco_res["domain"] == DomainMode.ECOMETRICS.value

        eco_alias_res = modeler.load_and_model("industrial_telemetry")
        assert eco_alias_res["domain"] == DomainMode.ECOMETRICS.value

        media_res = modeler.load_and_model("cinemetrics")
        assert media_res["domain"] == DomainMode.CINEMETRICS.value

        media_alias_res = modeler.load_and_model("entertainment")
        assert media_alias_res["domain"] == DomainMode.CINEMETRICS.value
