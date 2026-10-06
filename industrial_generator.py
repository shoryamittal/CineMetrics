"""
Industrial Facility Operations Data Generator (Ecolab Simulator)
================================================================
Enterprise data simulator generating high-frequency industrial telemetry logs
for automated water volume treatment, energy usage, chemical dosing concentrations,
and sensor telemetry across global facilities.

Intentionally introduces realistic operational anomalies, sensor faults,
missing data (NaNs), and dirty categorical entries to validate data quality
profiling and schema cleansing pipelines.
"""

import os
import sys
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple
import numpy as np
import pandas as pd

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("IndustrialSimulator")


class IndustrialDataGenerator:
    """
    Simulates enterprise telemetry for global industrial facilities operating
    Ecolab water treatment, cooling towers, and boiler automation systems.
    """

    DEFAULT_FACILITIES = [
        {"id": "Facility_A", "name": "Naperville Global Technology Center", "location": "Illinois, USA", "industry": "Food & Beverage Processing", "target_kpi": 48.5},
        {"id": "Facility_B", "name": "Gary Chemical Operations", "location": "Indiana, USA", "industry": "Heavy Manufacturing", "target_kpi": 34.0},
        {"id": "Facility_C", "name": "Pune Water Technologies Campus", "location": "Maharashtra, India", "industry": "Refinery & Petrochemicals", "target_kpi": 52.0},
        {"id": "Facility_D", "name": "Antwerp European Operations Hub", "location": "Flanders, Belgium", "industry": "Pharmaceuticals & Healthcare", "target_kpi": 60.5},
        {"id": "Facility_E", "name": "Monterrey Advanced Plant", "location": "Nuevo Leon, Mexico", "industry": "Data Center Cooling", "target_kpi": 72.0},
    ]

    # Intentional dirty alias mappings for testing text standardization
    DIRTY_FACILITY_ALIASES = {
        "Facility_A": ["facility_a", "FACILITY_A", " Facility_A ", "Facility_A_Line1", "FAC_A"],
        "Facility_B": ["facility_b", "FACILITY_B", "Facility_B_Unit2", "FAC-B"],
        "Facility_C": ["facility_c", "Facility_C ", "pune_fac_c", "FACILITY_C"],
        "Facility_D": ["facility_d", "antwerp_hub_d", "FACILITY_D", "Fac_D"],
        "Facility_E": ["facility_e", "monterrey_e", "FACILITY_E", "Fac_E_Cooling"],
    }

    DIRTY_INDUSTRY_ALIASES = {
        "Food & Beverage Processing": ["food & beverage", "FOOD & BEV", "F&B Processing", "Food and Beverage"],
        "Heavy Manufacturing": ["heavy mfg", "HEAVY_MANUFACTURING", "Heavy Mfg.", "Mfg Heavy"],
        "Refinery & Petrochemicals": ["refinery", "REFINERY_PETRO", "Petrochem / Refining"],
        "Pharmaceuticals & Healthcare": ["pharma", "PHARMACEUTICALS", "Healthcare & Pharma"],
        "Data Center Cooling": ["data center", "DATA_CENTER_COOLING", "Hyperscale Cooling"],
    }

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.facilities = self.DEFAULT_FACILITIES

    def generate_raw_logs(
        self,
        output_path: str = "ecolab_raw_factory_logs.csv",
        num_records: int = 6000,
        start_date: str = "2026-01-01 00:00:00",
        interval_minutes: int = 15,
        anomaly_rate: float = 0.065,
        missing_rate: float = 0.04
    ) -> pd.DataFrame:
        """
        Generates sequential industrial telemetry records containing intentional
        anomalies, missing values, and messy string artifacts.

        Parameters
        ----------
        output_path : str
            Target destination path for raw CSV file.
        num_records : int
            Total number of timestamped observations to synthesize.
        start_date : str
            ISO formatted start timestamp.
        interval_minutes : int
            Sampling frequency in minutes between steps.
        anomaly_rate : float
            Fraction of rows subjected to extreme spikes or out-of-bounds metrics.
        missing_rate : float
            Fraction of values injected with NaNs or null representations.

        Returns
        -------
        pd.DataFrame
            The raw simulated telemetry dataframe.
        """
        logger.info(f"Initiating industrial telemetry generation: {num_records:,} target records...")
        
        base_time = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        records = []

        # Time series generation
        for i in range(num_records):
            current_time = base_time + timedelta(minutes=i * interval_minutes)
            fac_meta = random.choice(self.facilities)
            canonical_id = fac_meta["id"]
            canonical_industry = fac_meta["industry"]

            # Introduce dirty categorical representations (20% chance)
            if random.random() < 0.20:
                facility_label = random.choice(self.DIRTY_FACILITY_ALIASES.get(canonical_id, [canonical_id]))
            else:
                facility_label = canonical_id

            if random.random() < 0.15:
                industry_label = random.choice(self.DIRTY_INDUSTRY_ALIASES.get(canonical_industry, [canonical_industry]))
            else:
                industry_label = canonical_industry

            # Baseline Gaussian distributions per facility
            # 1. Water Volume (Liters / 15-min interval): 8,000 - 35,000 Liters
            base_water = 18000 + (hash(canonical_id) % 8000)
            water_volume = np.random.normal(base_water, base_water * 0.12)

            # 2. Energy Consumption (kWh / 15-min): 300 - 1,200 kWh
            base_energy = 550 + (hash(canonical_id) % 300)
            energy_kwh = np.random.normal(base_energy, base_energy * 0.10)

            # 3. Chemical Dosing (mg/L): Anti-corrosion / biocide / scale inhibitors (15 - 45 mg/L)
            base_chemical = 28.5 + (hash(canonical_id) % 10)
            chemical_dosing = np.random.normal(base_chemical, 4.2)

            # 4. Sensor Temperature (°C): Normal operating range 22.0 - 36.0 °C
            base_temp = 26.5 + 4.0 * np.sin(i / 96.0 * 2 * np.pi)  # Daily diurnal cycle
            sensor_temp = np.random.normal(base_temp, 1.8)

            # 5. Outflow Quality Score (0 - 100): Target > 90.0
            outflow_quality = min(100.0, max(40.0, np.random.normal(93.5, 3.2)))

            # 6. Valve Pressure (PSI): Normal 65 - 85 PSI
            valve_pressure = np.random.normal(74.0, 4.5)

            # 7. pH Level: Normal industrial wastewater treatment pH 6.8 - 8.2
            ph_level = np.random.normal(7.35, 0.28)

            # -------------------------------------------------------------
            # INJECT ANOMALIES (Extreme spikes, leaks, chemical overdosing)
            # -------------------------------------------------------------
            is_anomaly = False
            anomaly_type = "NONE"

            if random.random() < anomaly_rate:
                is_anomaly = True
                dice = random.random()
                if dice < 0.35:
                    # Extreme temperature spike (Cooling failure / sensor short circuit)
                    sensor_temp = random.choice([
                        np.random.uniform(92.0, 148.5),  # Overheating alarm
                        np.random.uniform(-45.0, -15.0)  # Cryogenic / probe detachment
                    ])
                    anomaly_type = "SENSOR_TEMP_SPIKE"
                elif dice < 0.65:
                    # Chemical overdose or pump failure
                    chemical_dosing = random.choice([
                        np.random.uniform(145.0, 310.0), # Critical over-dosing
                        np.random.uniform(-10.0, 0.5)     # Meter backflow error (negative mg/L)
                    ])
                    anomaly_type = "CHEMICAL_DOSING_BREACH"
                elif dice < 0.85:
                    # Pipe leak or valve blowout
                    water_volume = np.random.uniform(4.0 * base_water, 6.5 * base_water)
                    valve_pressure = np.random.uniform(115.0, 145.0)
                    outflow_quality = np.random.uniform(32.0, 58.0)
                    anomaly_type = "PRESSURE_BURST_SURGE"
                else:
                    # Power brownout with water stall
                    energy_kwh = np.random.uniform(1800.0, 3400.0)
                    water_volume = np.random.uniform(50.0, 400.0)
                    outflow_quality = np.random.uniform(45.0, 65.0)
                    anomaly_type = "BROWNOUT_WATER_STALL"

            # -------------------------------------------------------------
            # INJECT MISSING VALUES (NaNs & String Artifacts)
            # -------------------------------------------------------------
            water_val = water_volume
            chemical_val = chemical_dosing
            quality_val = outflow_quality

            if random.random() < missing_rate:
                water_val = np.nan
            if random.random() < missing_rate:
                chemical_val = np.nan
            if random.random() < missing_rate:
                # Store as dirty string representations
                quality_val = random.choice([np.nan, "null", "N/A", "--", "ERROR_SENSOR"])

            records.append({
                "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Facility_ID": facility_label,
                "Industry_Type": industry_label,
                "Location": fac_meta["location"],
                "Water_Volume_Liters": round(water_val, 2) if pd.notnull(water_val) else np.nan,
                "Energy_Consumption_kWh": round(energy_kwh, 2),
                "Chemical_Dosing_mg_L": round(chemical_val, 2) if pd.notnull(chemical_val) else np.nan,
                "Sensor_Temperature_C": round(sensor_temp, 2),
                "Outflow_Quality_Score": quality_val,
                "Valve_Pressure_PSI": round(valve_pressure, 2),
                "pH_Level": round(ph_level, 2),
                "Raw_Anomaly_Tag": anomaly_type
            })

        df = pd.DataFrame(records)
        
        # Save to disk
        target_path = Path(output_path).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(target_path, index=False)
        
        logger.info(
            f"Successfully generated {len(df):,} factory records at '{target_path}'.\n"
            f"  - Missing Water Volume count: {df['Water_Volume_Liters'].isna().sum():,}\n"
            f"  - Injected Sensor Anomalies: {(df['Raw_Anomaly_Tag'] != 'NONE').sum():,}\n"
            f"  - Distinct Dirty Facility tags: {df['Facility_ID'].nunique()}"
        )
        return df


def ensure_industrial_data(file_path: str = "ecolab_raw_factory_logs.csv", min_records: int = 5000) -> pd.DataFrame:
    """
    Guarantees existence of the industrial raw factory logs dataset.
    Generates new synthetic data if the file is absent or has fewer than min_records.
    """
    path = Path(file_path)
    if path.exists():
        try:
            df = pd.read_csv(path, low_memory=False)
            if len(df) >= min_records:
                logger.info(f"Found existing valid industrial logs: {len(df):,} records at '{path}'.")
                return df
            else:
                logger.warning(f"Existing file has only {len(df)} records (< {min_records}). Regenerating...")
        except Exception as e:
            logger.warning(f"Could not read existing file ({e}). Regenerating...")
    
    generator = IndustrialDataGenerator(seed=42)
    return generator.generate_raw_logs(output_path=file_path, num_records=max(6000, min_records))


if __name__ == "__main__":
    out_file = "ecolab_raw_factory_logs.csv"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    df = ensure_industrial_data(out_file, min_records=5000)
    print(f"\n[+] Industrial Generator Test Completed.")
    print(f"    Shape: {df.shape}")
    print(f"    Columns: {list(df.columns)}")
    print(f"    Sample Row:\n{df.iloc[0].to_dict()}")
