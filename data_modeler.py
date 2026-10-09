"""
Enterprise Star Schema Dimensional Modeling Engine (The Data Engine)
=====================================================================
A unified, modular dimensional modeler capable of processing dual operational domains:
  1. Entertainment Domain ("CineMetrics Mode"):
     - Fact: fact_movie_performance
     - Dimensions: dim_movies, dim_genres, dim_creatives
  2. Enterprise Industrial Sustainability Domain ("EcoMetrics Mode"):
     - Fact: fact_facility_operations
     - Dimensions: dim_facilities, dim_time, dim_alerts

Enforces strict data cleansing checkpoints:
  - Checkpoint 1: Mismatched text normalization & canonical mapping
  - Checkpoint 2: Business-rule null imputation (grouped median / mean)
  - Checkpoint 3: Out-of-bounds anomaly tagging and sensor validation
"""

import json
import logging
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DataModeler")


class DomainMode(str, Enum):
    """Supported business analytical domain modes."""
    CINEMETRICS = "cinemetrics"
    ECOMETRICS = "ecometrics"


class DataModeler:
    """
    Transforms raw datasets into enterprise-grade Star Schema relational models
    with full data hygiene checkpoints and audit trail tracking.
    """

    # Canonical Facility Master
    CANONICAL_FACILITIES = {
        "FACILITY_A": {"id": "Facility_A", "name": "Naperville Global Technology Center", "location": "Naperville, IL, USA", "region": "North America", "industry": "Food & Beverage Processing", "target_kpi": 48.5, "sensors": 128},
        "FACILITY_B": {"id": "Facility_B", "name": "Gary Chemical Operations", "location": "Gary, IN, USA", "region": "North America", "industry": "Heavy Manufacturing", "target_kpi": 34.0, "sensors": 94},
        "FACILITY_C": {"id": "Facility_C", "name": "Pune Water Technologies Campus", "location": "Pune, MH, India", "region": "Asia-Pacific", "industry": "Refinery & Petrochemicals", "target_kpi": 52.0, "sensors": 156},
        "FACILITY_D": {"id": "Facility_D", "name": "Antwerp European Operations Hub", "location": "Antwerp, Flanders, Belgium", "region": "Europe", "industry": "Pharmaceuticals & Healthcare", "target_kpi": 60.5, "sensors": 112},
        "FACILITY_E": {"id": "Facility_E", "name": "Monterrey Advanced Plant", "location": "Monterrey, NL, Mexico", "region": "Latin America", "industry": "Data Center Cooling", "target_kpi": 72.0, "sensors": 140},
    }

    # Canonical Threshold Boundaries for Alerts
    ALERT_THRESHOLDS = [
        {"alert_id": 101, "metric_name": "Sensor_Temperature_C", "safe_min": 15.0, "safe_max": 42.0, "unit": "°C", "priority": "CRITICAL", "protocol": "Trigger automated emergency valve bypass & cooling loop coolant boost."},
        {"alert_id": 102, "metric_name": "Chemical_Dosing_mg_L", "safe_min": 10.0, "safe_max": 65.0, "unit": "mg/L", "priority": "HIGH", "protocol": "Isolate dosing pump manifold; recalibrate peristaltic feeder."},
        {"alert_id": 103, "metric_name": "Valve_Pressure_PSI", "safe_min": 50.0, "safe_max": 100.0, "unit": "PSI", "priority": "HIGH", "protocol": "Engage pressure relief regulator valve; dispatch maintenance team."},
        {"alert_id": 104, "metric_name": "Outflow_Quality_Score", "safe_min": 85.0, "safe_max": 100.0, "unit": "Score (0-100)", "priority": "CRITICAL", "protocol": "Reroute effluent flow to secondary holding retention tank immediately."},
        {"alert_id": 105, "metric_name": "pH_Level", "safe_min": 6.5, "safe_max": 8.5, "unit": "pH", "priority": "MEDIUM", "protocol": "Adjust buffer neutralizer injection rate."},
    ]

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parent
        self.audit_trail: List[Dict[str, Any]] = []

    def _log_audit_step(self, stage: str, details: str, affected_count: int = 0):
        """Records a timestamped data quality transition event."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stage": stage,
            "details": details,
            "affected_records": int(affected_count)
        }
        self.audit_trail.append(entry)
        logger.info(f"[{stage}] {details} (Records affected: {affected_count:,})")

    # =========================================================================
    # ENTERPRISE INDUSTRIAL SUSTAINABILITY DOMAIN MODELER
    # =========================================================================

    def model_ecometrics_domain(self, raw_csv_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes complete ingestion, cleansing checkpoints, and dimensional star
        schema construction for enterprise industrial factory telemetry.
        """
        self.audit_trail.clear()
        self._log_audit_step("INGESTION_START", "Initiating industrial telemetry dimensional modeling.")

        csv_file = Path(raw_csv_path) if raw_csv_path else self.base_dir / "industrial_raw_factory_logs.csv"
        
        # Verify source file existence
        if not csv_file.exists():
            from industrial_generator import ensure_industrial_data
            df_raw = ensure_industrial_data(str(csv_file), min_records=5000)
        else:
            df_raw = pd.read_csv(csv_file, low_memory=False)

        total_ingested = len(df_raw)
        self._log_audit_step("RAW_EXTRACTION", f"Loaded raw factory logs from '{csv_file.name}'.", total_ingested)

        df = df_raw.copy()

        # ---------------------------------------------------------------------
        # CHECKPOINT 1: TEXT STANDARDIZATION & CANONICAL MAPPING
        # ---------------------------------------------------------------------
        # Facility ID Cleaning
        raw_fac_series = df["Facility_ID"].astype(str).str.strip().str.upper()
        
        def resolve_facility(val: str) -> str:
            if "FACILITY_A" in val or "FAC_A" in val:
                return "Facility_A"
            if "FACILITY_B" in val or "FAC_B" in val or "FAC-B" in val:
                return "Facility_B"
            if "FACILITY_C" in val or "PUNE" in val:
                return "Facility_C"
            if "FACILITY_D" in val or "ANTWERP" in val or "FAC_D" in val:
                return "Facility_D"
            if "FACILITY_E" in val or "MONTERREY" in val or "FAC_E" in val:
                return "Facility_E"
            return "Facility_A"  # Default fallback

        cleaned_facilities = raw_fac_series.apply(resolve_facility)
        fac_mismatches = (df["Facility_ID"] != cleaned_facilities).sum()
        df["Facility_ID"] = cleaned_facilities
        self._log_audit_step("TEXT_NORMALIZATION", "Harmonized dirty Facility_ID aliases to canonical identifiers.", fac_mismatches)

        # Telemetry Dirty String Parsing & Type Coercion
        df["Water_Volume_Liters"] = pd.to_numeric(df.get("Water_Volume_Liters", np.nan), errors="coerce")
        df["Energy_Consumption_kWh"] = pd.to_numeric(df.get("Energy_Consumption_kWh", 550.0), errors="coerce").fillna(550.0)
        df["Chemical_Dosing_mg_L"] = pd.to_numeric(df.get("Chemical_Dosing_mg_L", np.nan), errors="coerce")
        df["Sensor_Temperature_C"] = pd.to_numeric(df.get("Sensor_Temperature_C", 26.0), errors="coerce").fillna(26.0)
        df["Valve_Pressure_PSI"] = pd.to_numeric(df.get("Valve_Pressure_PSI", 74.0), errors="coerce").fillna(74.0)
        df["pH_Level"] = pd.to_numeric(df.get("pH_Level", 7.35), errors="coerce").fillna(7.35)
        df["Outflow_Quality_Score"] = pd.to_numeric(df.get("Outflow_Quality_Score", np.nan), errors="coerce")
        coerced_quality_nulls = df["Outflow_Quality_Score"].isna().sum()
        self._log_audit_step("TYPE_COERCION", "Sanitized telemetry numeric strings and parsed floats.", coerced_quality_nulls)

        # ---------------------------------------------------------------------
        # CHECKPOINT 2: BUSINESS-RULE NULL IMPUTATION
        # ---------------------------------------------------------------------
        # 1. Water Volume: Impute using median by Facility
        null_water_before = df["Water_Volume_Liters"].isna().sum()
        fac_water_medians = df.groupby("Facility_ID")["Water_Volume_Liters"].transform("median")
        df["Water_Volume_Liters"] = df["Water_Volume_Liters"].fillna(fac_water_medians).fillna(18500.0)
        self._log_audit_step("NULL_IMPUTATION_WATER", "Imputed missing Water Volume via Facility-level historical median.", null_water_before)

        # 2. Chemical Dosing: Impute using mean by Facility
        null_chem_before = df["Chemical_Dosing_mg_L"].isna().sum()
        fac_chem_means = df.groupby("Facility_ID")["Chemical_Dosing_mg_L"].transform("mean")
        df["Chemical_Dosing_mg_L"] = df["Chemical_Dosing_mg_L"].fillna(fac_chem_means).fillna(28.0)
        self._log_audit_step("NULL_IMPUTATION_CHEMICAL", "Imputed missing Chemical Dosing via Facility-level mean.", null_chem_before)

        # 3. Outflow Quality: Impute using Target Benchmark (93.5)
        null_quality_before = df["Outflow_Quality_Score"].isna().sum()
        df["Outflow_Quality_Score"] = df["Outflow_Quality_Score"].fillna(93.5)
        self._log_audit_step("NULL_IMPUTATION_QUALITY", "Imputed missing Outflow Quality via target baseline score.", null_quality_before)

        # ---------------------------------------------------------------------
        # CHECKPOINT 3: OUT-OF-BOUNDS METRIC DETECTION & ANOMALY FLAGGING
        # ---------------------------------------------------------------------
        # Ensure timestamp is parsed
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        
        # Rule-based threshold alerts
        temp_breach = (df["Sensor_Temperature_C"] < 15.0) | (df["Sensor_Temperature_C"] > 42.0)
        chem_breach = (df["Chemical_Dosing_mg_L"] < 10.0) | (df["Chemical_Dosing_mg_L"] > 65.0)
        pressure_breach = (df["Valve_Pressure_PSI"] < 50.0) | (df["Valve_Pressure_PSI"] > 100.0)
        quality_breach = df["Outflow_Quality_Score"] < 85.0
        
        # Combined anomaly definition
        df["is_anomaly"] = temp_breach | chem_breach | pressure_breach | quality_breach
        
        def assign_anomaly_category(row) -> str:
            tags = []
            if row["Sensor_Temperature_C"] < 15.0 or row["Sensor_Temperature_C"] > 42.0:
                tags.append("TEMPERATURE_BREACH")
            if row["Chemical_Dosing_mg_L"] < 10.0 or row["Chemical_Dosing_mg_L"] > 65.0:
                tags.append("CHEMICAL_OVERDOSE")
            if row["Valve_Pressure_PSI"] < 50.0 or row["Valve_Pressure_PSI"] > 100.0:
                tags.append("PRESSURE_FAULT")
            if row["Outflow_Quality_Score"] < 85.0:
                tags.append("QUALITY_DEGRADATION")
            return "|".join(tags) if tags else "NOMINAL"

        df["anomaly_category"] = df.apply(assign_anomaly_category, axis=1)
        total_anomalies = df["is_anomaly"].sum()
        self._log_audit_step("OUTLIER_CLASSIFICATION", "Tagged telemetry outliers against operational safety boundaries.", total_anomalies)

        # Derived KPI: Water-to-Energy Ratio (Liters per kWh)
        df["water_energy_ratio"] = (df["Water_Volume_Liters"] / (df["Energy_Consumption_kWh"] + 1e-4)).round(2)

        # ---------------------------------------------------------------------
        # STAR SCHEMA GENERATION
        # ---------------------------------------------------------------------
        # 1. Dimension: dim_time
        dim_time = pd.DataFrame()
        dim_time["timestamp"] = df["Timestamp"]
        dim_time["date_key"] = df["Timestamp"].dt.strftime("%Y%m%d%H%M").astype(int)
        dim_time["date"] = df["Timestamp"].dt.date
        dim_time["year"] = df["Timestamp"].dt.year
        dim_time["quarter"] = df["Timestamp"].dt.quarter
        dim_time["month"] = df["Timestamp"].dt.month
        dim_time["month_name"] = df["Timestamp"].dt.strftime("%B")
        dim_time["day"] = df["Timestamp"].dt.day
        dim_time["day_of_week"] = df["Timestamp"].dt.day_name()
        dim_time["hour"] = df["Timestamp"].dt.hour
        
        def compute_shift(hour: int) -> Tuple[int, str]:
            if 6 <= hour < 14:
                return (1, "Morning Shift (06:00-14:00)")
            elif 14 <= hour < 22:
                return (2, "Afternoon Shift (14:00-22:00)")
            else:
                return (3, "Night Shift (22:00-06:00)")

        shifts = dim_time["hour"].apply(compute_shift)
        dim_time["shift_id"] = [s[0] for s in shifts]
        dim_time["shift_name"] = [s[1] for s in shifts]
        dim_time["is_weekend"] = df["Timestamp"].dt.dayofweek.isin([5, 6])
        dim_time = dim_time.drop_duplicates(subset=["date_key"]).reset_index(drop=True)

        # 2. Dimension: dim_facilities
        fac_records = []
        for fac_id, meta in self.CANONICAL_FACILITIES.items():
            fac_records.append({
                "facility_id": meta["id"],
                "facility_name": meta["name"],
                "location": meta["location"],
                "region": meta["region"],
                "industry_type": meta["industry"],
                "target_efficiency_kpi": meta["target_kpi"],
                "active_sensors_count": meta["sensors"]
            })
        dim_facilities = pd.DataFrame(fac_records)

        # 3. Dimension: dim_alerts
        dim_alerts = pd.DataFrame(self.ALERT_THRESHOLDS)

        # 4. Fact Table: fact_facility_operations
        fact_operations = pd.DataFrame()
        fact_operations["operation_id"] = np.arange(1, len(df) + 1)
        fact_operations["facility_id"] = df["Facility_ID"]
        fact_operations["date_key"] = df["Timestamp"].dt.strftime("%Y%m%d%H%M").astype(int)
        fact_operations["timestamp"] = df["Timestamp"]
        fact_operations["shift_id"] = [s[0] for s in shifts]
        fact_operations["water_volume_liters"] = df["Water_Volume_Liters"].round(2)
        fact_operations["energy_consumption_kwh"] = df["Energy_Consumption_kWh"].round(2)
        fact_operations["chemical_dosing_mg_l"] = df["Chemical_Dosing_mg_L"].round(2)
        fact_operations["sensor_temperature_c"] = df["Sensor_Temperature_C"].round(2)
        fact_operations["outflow_quality_score"] = df["Outflow_Quality_Score"].round(2)
        fact_operations["valve_pressure_psi"] = df["Valve_Pressure_PSI"].round(2)
        fact_operations["ph_level"] = df["pH_Level"].round(2)
        fact_operations["water_energy_ratio"] = df["water_energy_ratio"]
        fact_operations["is_anomaly"] = df["is_anomaly"].astype(bool)
        fact_operations["anomaly_category"] = df["anomaly_category"]

        self._log_audit_step("STAR_SCHEMA_COMPLETE", "Successfully materialized Star Schema relational tables.", len(fact_operations))

        return {
            "domain": DomainMode.ECOMETRICS.value,
            "fact_table": fact_operations,
            "dimension_tables": {
                "dim_facilities": dim_facilities,
                "dim_time": dim_time,
                "dim_alerts": dim_alerts
            },
            "audit_trail": self.audit_trail,
            "raw_record_count": total_ingested,
            "clean_record_count": len(fact_operations)
        }

    # =========================================================================
    # ENTERTAINMENT DOMAIN MODELER (CINEMETRICS)
    # =========================================================================

    def model_movie_domain(self, catalog_json_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Ingests the curated movie and series catalog into a Star Schema relational model:
          - Fact: fact_movie_performance
          - Dimensions: dim_movies, dim_genres, dim_creatives
        """
        self.audit_trail.clear()
        self._log_audit_step("INGESTION_START", "Initiating CineMetrics media domain dimensional modeling.")

        cat_path = Path(catalog_json_path) if catalog_json_path else self.base_dir / "dashboard" / "catalog.json"
        
        if not cat_path.exists():
            # Fallback to data/synthetic
            cat_path = self.base_dir / "data" / "analytics" / "curated_content_catalog.json"

        with open(cat_path, "r", encoding="utf-8") as f:
            raw_catalog = json.load(f)

        df = pd.DataFrame(raw_catalog)
        self._log_audit_step("RAW_EXTRACTION", f"Ingested {len(df)} titles from '{cat_path.name}'.", len(df))

        # ---------------------------------------------------------------------
        # CHECKPOINT: TYPE NORMALIZATION & VALUE VERIFICATION
        # ---------------------------------------------------------------------
        df["production_budget"] = pd.to_numeric(df.get("production_budget", 0), errors="coerce").fillna(50000000)
        df["licensing_cost"] = pd.to_numeric(df.get("licensing_cost", 0), errors="coerce").fillna(10000000)
        df["marketing_spend"] = pd.to_numeric(df.get("marketing_spend", 0), errors="coerce").fillna(20000000)
        df["total_revenue"] = pd.to_numeric(df.get("total_revenue", 0), errors="coerce").fillna(100000000)
        df["imdb_rating"] = pd.to_numeric(df.get("imdb_rating", 7.0), errors="coerce").fillna(7.0)
        df["duration_minutes"] = pd.to_numeric(df.get("duration_minutes", 120), errors="coerce").fillna(120)
        df["total_views"] = pd.to_numeric(df.get("total_views", 1000000), errors="coerce").fillna(1000000)

        # Derived profit & ROI
        total_costs = df["production_budget"] + df["licensing_cost"] + df["marketing_spend"]
        df["calculated_profit"] = df["total_revenue"] - total_costs
        df["calculated_roi"] = (df["calculated_profit"] / (total_costs + 1.0)).round(4)

        # ---------------------------------------------------------------------
        # STAR SCHEMA GENERATION
        # ---------------------------------------------------------------------
        # 1. Fact Table: fact_movie_performance
        fact_movies = pd.DataFrame({
            "content_id": df["content_id"],
            "title": df["title"],
            "production_budget": df["production_budget"],
            "licensing_cost": df["licensing_cost"],
            "marketing_spend": df["marketing_spend"],
            "total_revenue": df["total_revenue"],
            "ad_revenue": df.get("ad_revenue", df["total_revenue"] * 0.35),
            "contribution_profit": df["calculated_profit"],
            "content_roi": df["calculated_roi"],
            "votes": (df["total_views"] * 0.05).astype(int),
            "runtime_minutes": df["duration_minutes"],
            "imdb_rating": df["imdb_rating"],
            "total_watch_hours": df.get("total_watch_hours", df["total_views"] * 2.2),
            "completion_rate": df.get("average_completion_rate", 82.5),
            "decision": df.get("decision", "MONITOR")
        })

        # 2. Dimension: dim_movies
        dim_movies = pd.DataFrame({
            "content_id": df["content_id"],
            "title": df["title"],
            "content_type": df.get("content_type", "Movie"),
            "release_year": df.get("release_year", 2022),
            "age_rating": df.get("age_rating", "PG-13"),
            "studio": df.get("studio", "Global Pictures"),
            "language": df.get("language", "English"),
            "rights_expiry": df.get("rights_expiry", "2028-12-31"),
            "territory_count": df.get("territory_count", 45),
            "poster_url": df.get("poster_url", "")
        })

        # 3. Dimension: dim_genres
        unique_genres = df["genre"].unique()
        genre_records = []
        for gid, gname in enumerate(unique_genres, start=1):
            sub_df = df[df["genre"] == gname]
            genre_records.append({
                "genre_id": gid,
                "genre_name": gname,
                "title_count": len(sub_df),
                "avg_production_budget": round(sub_df["production_budget"].mean(), 2),
                "avg_imdb_rating": round(sub_df["imdb_rating"].mean(), 2),
                "avg_roi": round(sub_df["calculated_roi"].mean(), 4)
            })
        dim_genres = pd.DataFrame(genre_records)

        # 4. Dimension: dim_creatives
        dim_creatives = pd.DataFrame({
            "creative_id": np.arange(1, len(df) + 1),
            "content_id": df["content_id"],
            "director": df.get("director", "Acclaimed Director"),
            "starring_cast": df.get("cast", "Ensemble Cast"),
            "talent_value_index": df.get("talent_value_index", 85)
        })

        self._log_audit_step("STAR_SCHEMA_COMPLETE", "Successfully constructed media performance Star Schema relational model.", len(fact_movies))

        return {
            "domain": DomainMode.CINEMETRICS.value,
            "fact_table": fact_movies,
            "dimension_tables": {
                "dim_movies": dim_movies,
                "dim_genres": dim_genres,
                "dim_creatives": dim_creatives
            },
            "audit_trail": self.audit_trail,
            "raw_record_count": len(df),
            "clean_record_count": len(fact_movies)
        }

    # =========================================================================
    # UNIFIED DISPATCHER
    # =========================================================================

    def load_and_model(self, domain: str = "ecometrics", source_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Unified router that parses and models data into a Star Schema based on
        active domain mode.
        """
        domain_normalized = str(domain).lower().strip()
        if "eco" in domain_normalized or "industrial" in domain_normalized:
            return self.model_ecometrics_domain(source_path)
        else:
            return self.model_movie_domain(source_path)


if __name__ == "__main__":
    modeler = DataModeler()
    
    print("\n--- TEST 1: ECOMETRICS INDUSTRIAL DOMAIN ---")
    eco_model = modeler.load_and_model("ecometrics")
    print("Fact Table Shape:", eco_model["fact_table"].shape)
    print("Dimensions:", list(eco_model["dimension_tables"].keys()))
    print("Sample Anomaly Count:", eco_model["fact_table"]["is_anomaly"].sum())

    print("\n--- TEST 2: CINEMETRICS ENTERTAINMENT DOMAIN ---")
    movie_model = modeler.load_and_model("cinemetrics")
    print("Fact Table Shape:", movie_model["fact_table"].shape)
    print("Dimensions:", list(movie_model["dimension_tables"].keys()))
    print("Average Content ROI:", f"+{movie_model['fact_table']['content_roi'].mean() * 100:.1f}%")

    