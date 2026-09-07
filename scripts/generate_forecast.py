"""
======================================================================
ECDIP - ENTERPRISE FORECAST INTELLIGENCE GENERATOR
======================================================================

Forecast metrics:
    1. VIEWING_DEMAND
    2. REVENUE
    3. ENGAGEMENT

Sources:
    fact_viewing_events.csv
    fact_revenue.csv
    fact_engagement.csv

Output:
    data/synthetic/fact_forecast.csv

Model:
    - Daily aggregation
    - Log-linear trend
    - Day-of-week seasonality
    - Recent momentum
    - Residual uncertainty
    - Prediction intervals
    - Confidence score
    - Sparse-history fallback
======================================================================
"""

from pathlib import Path
from datetime import datetime
import sys

import numpy as np
import pandas as pd


# Support direct execution from Windows consoles that default to cp1252 while
# retaining the Unicode status messages used throughout this generator.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# =====================================================================
# CONFIGURATION
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "synthetic"

VIEWING_FILE = DATA_DIR / "fact_viewing_events.csv"
REVENUE_FILE = DATA_DIR / "fact_revenue.csv"
ENGAGEMENT_FILE = DATA_DIR / "fact_engagement.csv"

OUTPUT_FILE = DATA_DIR / "fact_forecast.csv"

LOOKBACK_DAYS = 180
FORECAST_HORIZON = 30
MIN_HISTORY_DAYS = 14

CHUNK_SIZE = 250_000


print("=" * 70)
print("ECDIP - ENTERPRISE FORECAST INTELLIGENCE GENERATOR")
print("=" * 70)


# =====================================================================
# HELPERS
# =====================================================================

def require_file(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Required source file does not exist:\n{path}"
        )


def require_columns(df, columns, source_name):
    missing = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"{source_name} is missing required columns: {missing}"
        )


def safe_numeric(series):
    return pd.to_numeric(
        series,
        errors="coerce"
    )


# =====================================================================
# SOURCE VALIDATION
# =====================================================================

print("\nValidating source files...")

require_file(VIEWING_FILE)
require_file(REVENUE_FILE)
require_file(ENGAGEMENT_FILE)

print("✓ Viewing events file found")
print("✓ Revenue file found")
print("✓ Engagement file found")


# =====================================================================
# LOAD VIEWING EVENTS
# =====================================================================

print("\nLoading viewing events...")

VIEWING_COLUMNS = [
    "content_id",
    "date_id",
    "watch_hours",
    "completion_rate",
    "rewatch_count",
]

viewing_chunks = []

for chunk in pd.read_csv(
    VIEWING_FILE,
    usecols=VIEWING_COLUMNS,
    chunksize=CHUNK_SIZE
):

    require_columns(
        chunk,
        VIEWING_COLUMNS,
        "fact_viewing_events"
    )

    chunk["date_id"] = pd.to_datetime(
        chunk["date_id"],
        errors="coerce"
    )

    chunk["watch_hours"] = safe_numeric(
        chunk["watch_hours"]
    ).fillna(0)

    chunk["completion_rate"] = safe_numeric(
        chunk["completion_rate"]
    )

    chunk["rewatch_count"] = safe_numeric(
        chunk["rewatch_count"]
    ).fillna(0)

    chunk = chunk.dropna(
        subset=[
            "content_id",
            "date_id"
        ]
    )

    viewing_chunks.append(chunk)


viewing = pd.concat(
    viewing_chunks,
    ignore_index=True
)

del viewing_chunks

print(
    f"✓ Viewing records loaded: "
    f"{len(viewing):,}"
)


# =====================================================================
# AGGREGATE VIEWING
# =====================================================================

print("\nAggregating viewing history...")

viewing_daily = (
    viewing
    .groupby(
        [
            "content_id",
            "date_id"
        ],
        as_index=False
    )
    .agg(
        watch_hours=(
            "watch_hours",
            "sum"
        ),

        viewing_completion_rate=(
            "completion_rate",
            "mean"
        ),

        rewatch_count=(
            "rewatch_count",
            "sum"
        )
    )
)

del viewing

print(
    f"✓ Viewing daily records: "
    f"{len(viewing_daily):,}"
)


# =====================================================================
# LOAD REVENUE
# =====================================================================

print("\nLoading revenue data...")

# Actual fact_revenue.csv uses revenue_amount.
REVENUE_COLUMNS = [
    "content_id",
    "date_id",
    "revenue_amount",
]

revenue_chunks = []

for chunk in pd.read_csv(
    REVENUE_FILE,
    usecols=REVENUE_COLUMNS,
    chunksize=CHUNK_SIZE
):

    require_columns(
        chunk,
        REVENUE_COLUMNS,
        "fact_revenue"
    )

    chunk["date_id"] = pd.to_datetime(
        chunk["date_id"],
        errors="coerce"
    )

    chunk["revenue_amount"] = safe_numeric(
        chunk["revenue_amount"]
    ).fillna(0)

    chunk = chunk.dropna(
        subset=[
            "content_id",
            "date_id"
        ]
    )

    revenue_chunks.append(chunk)


revenue = pd.concat(
    revenue_chunks,
    ignore_index=True
)

del revenue_chunks

print(
    f"✓ Revenue records loaded: "
    f"{len(revenue):,}"
)


# =====================================================================
# AGGREGATE REVENUE
# =====================================================================

print("\nAggregating revenue history...")

revenue_daily = (
    revenue
    .groupby(
        [
            "content_id",
            "date_id"
        ],
        as_index=False
    )
    .agg(
        total_revenue=(
            "revenue_amount",
            "sum"
        )
    )
)

del revenue

print(
    f"✓ Revenue daily records: "
    f"{len(revenue_daily):,}"
)


# =====================================================================
# LOAD ENGAGEMENT
# =====================================================================

print("\nLoading engagement data...")

ENGAGEMENT_COLUMNS = [
    "content_id",
    "date_id",
    "likes",
    "dislikes",
    "average_watch_percentage",
    "completion_rate",
    "rewatch_rate",
]

engagement_chunks = []

for chunk in pd.read_csv(
    ENGAGEMENT_FILE,
    usecols=ENGAGEMENT_COLUMNS,
    chunksize=CHUNK_SIZE
):

    require_columns(
        chunk,
        ENGAGEMENT_COLUMNS,
        "fact_engagement"
    )

    chunk["date_id"] = pd.to_datetime(
        chunk["date_id"],
        errors="coerce"
    )

    for column in [
        "likes",
        "dislikes",
        "average_watch_percentage",
        "completion_rate",
        "rewatch_rate",
    ]:

        chunk[column] = safe_numeric(
            chunk[column]
        )

    chunk = chunk.dropna(
        subset=[
            "content_id",
            "date_id"
        ]
    )

    engagement_chunks.append(chunk)


engagement = pd.concat(
    engagement_chunks,
    ignore_index=True
)

del engagement_chunks

print(
    f"✓ Engagement records loaded: "
    f"{len(engagement):,}"
)


# =====================================================================
# AGGREGATE ENGAGEMENT
# =====================================================================

print("\nAggregating engagement history...")

engagement_daily = (
    engagement
    .groupby(
        [
            "content_id",
            "date_id"
        ],
        as_index=False
    )
    .agg(

        likes=(
            "likes",
            "sum"
        ),

        dislikes=(
            "dislikes",
            "sum"
        ),

        average_watch_percentage=(
            "average_watch_percentage",
            "mean"
        ),

        engagement_completion_rate=(
            "completion_rate",
            "mean"
        ),

        rewatch_rate=(
            "rewatch_rate",
            "mean"
        )
    )
)

del engagement

print(
    f"✓ Engagement daily records: "
    f"{len(engagement_daily):,}"
)


# =====================================================================
# COMBINE SOURCES
# =====================================================================

print("\nCombining historical signals...")

history = pd.merge(
    viewing_daily,
    revenue_daily,
    on=[
        "content_id",
        "date_id"
    ],
    how="outer"
)

history = pd.merge(
    history,
    engagement_daily,
    on=[
        "content_id",
        "date_id"
    ],
    how="outer"
)

del viewing_daily
del revenue_daily
del engagement_daily


history = history.sort_values(
    [
        "content_id",
        "date_id"
    ]
)


# =====================================================================
# CLEAN NUMERIC VALUES
# =====================================================================

numeric_columns = [
    "watch_hours",
    "viewing_completion_rate",
    "rewatch_count",
    "total_revenue",
    "likes",
    "dislikes",
    "average_watch_percentage",
    "engagement_completion_rate",
    "rewatch_rate",
]

for column in numeric_columns:

    if column in history.columns:

        history[column] = safe_numeric(
            history[column]
        )


history["watch_hours"] = (
    history["watch_hours"]
    .fillna(0)
)

history["total_revenue"] = (
    history["total_revenue"]
    .fillna(0)
)

history["engagement_completion_rate"] = (
    history["engagement_completion_rate"]
    .fillna(
        history["viewing_completion_rate"]
    )
)


# =====================================================================
# GLOBAL HISTORICAL CUTOFF
# =====================================================================

max_date = history["date_id"].max()

if pd.isna(max_date):

    raise ValueError(
        "No valid historical dates found."
    )


lookback_start = (
    max_date
    -
    pd.Timedelta(
        days=LOOKBACK_DAYS
    )
)

history = history[
    history["date_id"] >= lookback_start
].copy()


print(
    f"✓ Historical start: "
    f"{lookback_start.date()}"
)

print(
    f"✓ Historical end: "
    f"{max_date.date()}"
)


# =====================================================================
# FORECAST FUNCTION
# =====================================================================

def forecast_series(
    series_df,
    value_column,
    horizon=FORECAST_HORIZON
):

    if value_column not in series_df.columns:
        return None

    data = series_df[
        [
            "date_id",
            value_column
        ]
    ].dropna().copy()

    if data.empty:
        return None

    data = (
        data
        .groupby(
            "date_id",
            as_index=False
        )[value_column]
        .mean()
        .sort_values("date_id")
    )

    # ---------------------------------------------------------------
    # Complete daily calendar
    # ---------------------------------------------------------------

    full_dates = pd.date_range(
        data["date_id"].min(),
        data["date_id"].max(),
        freq="D"
    )

    data = (
        data
        .set_index("date_id")
        .reindex(full_dates)
        .rename_axis("date_id")
        .reset_index()
    )

    data[value_column] = (
        data[value_column]
        .interpolate(
            limit_direction="both"
        )
        .fillna(0)
    )

    history_days = len(data)

    # ---------------------------------------------------------------
    # Sparse-history fallback
    # ---------------------------------------------------------------

    if history_days < MIN_HISTORY_DAYS:

        baseline = float(
            data[value_column].mean()
        )

        future_dates = pd.date_range(
            max_date
            +
            pd.Timedelta(days=1),
            periods=horizon,
            freq="D"
        )

        predictions = np.repeat(
            max(0, baseline),
            horizon
        )

        lower = predictions * 0.70
        upper = predictions * 1.30

        return {
            "future_dates": future_dates,
            "predictions": predictions,
            "lower": lower,
            "upper": upper,
            "trend": "INSUFFICIENT_HISTORY",
            "confidence": 25.0,
            "history_days": history_days,
            "r_squared": 0.0,
            "momentum": 0.0,
            "method": "MEAN_FALLBACK",
        }

    # ---------------------------------------------------------------
    # Clean series
    # ---------------------------------------------------------------

    values = (
        safe_numeric(
            data[value_column]
        )
        .fillna(0)
        .clip(lower=0)
        .values
    )

    # ---------------------------------------------------------------
    # Log-linear trend
    # ---------------------------------------------------------------

    log_values = np.log1p(
        values
    )

    x = np.arange(
        len(log_values),
        dtype=float
    )

    slope, intercept = np.polyfit(
        x,
        log_values,
        1
    )

    fitted = (
        intercept
        +
        slope * x
    )

    residuals = (
        log_values
        -
        fitted
    )

    residual_std = float(
        np.std(residuals)
    )

    # ---------------------------------------------------------------
    # R-squared
    # ---------------------------------------------------------------

    ss_res = np.sum(
        residuals ** 2
    )

    ss_tot = np.sum(
        (
            log_values
            -
            np.mean(log_values)
        ) ** 2
    )

    if ss_tot <= 0:

        r_squared = 0.0

    else:

        r_squared = float(
            np.clip(
                1 - (
                    ss_res /
                    ss_tot
                ),
                0,
                1
            )
        )

    # ---------------------------------------------------------------
    # Day-of-week seasonality
    # ---------------------------------------------------------------

    data["day_of_week"] = (
        data["date_id"]
        .dt.dayofweek
    )

    overall_mean = float(
        data[value_column].mean()
    )

    if overall_mean > 0:

        seasonal = (
            data
            .groupby(
                "day_of_week"
            )[value_column]
            .mean()
            /
            overall_mean
        )

        seasonal = (
            seasonal
            .reindex(range(7))
            .fillna(1.0)
            .clip(
                0.70,
                1.30
            )
        )

    else:

        seasonal = pd.Series(
            1.0,
            index=range(7)
        )

    # ---------------------------------------------------------------
    # Momentum
    # ---------------------------------------------------------------

    recent_window = min(
        28,
        len(values)
    )

    recent_mean = float(
        np.mean(
            values[-recent_window:]
        )
    )

    if len(values) >= 56:

        older_mean = float(
            np.mean(
                values[-56:-28]
            )
        )

    else:

        older_mean = float(
            np.mean(values)
        )

    if older_mean > 0:

        momentum = (
            recent_mean
            /
            older_mean
            -
            1
        )

    else:

        momentum = 0.0

    momentum = float(
        np.clip(
            momentum,
            -0.50,
            0.50
        )
    )

    # ---------------------------------------------------------------
    # FUTURE DATES
    #
    # IMPORTANT:
    # The first forecast date is ALWAYS the day after the global
    # historical cutoff, preventing overlap with historical data.
    # ---------------------------------------------------------------

    future_dates = pd.date_range(
        start=max_date
        +
        pd.Timedelta(days=1),

        periods=horizon,

        freq="D"
    )

    future_x = np.arange(
        len(values),
        len(values) + horizon,
        dtype=float
    )

    future_log = (
        intercept
        +
        slope * future_x
    )

    predictions = np.expm1(
        future_log
    )

    predictions = np.maximum(
        predictions,
        0
    )

    # ---------------------------------------------------------------
    # MOMENTUM ADJUSTMENT
    # ---------------------------------------------------------------

    momentum_factor = (
        1
        +
        0.35 * momentum
    )

    predictions *= (
        momentum_factor
    )

    # ---------------------------------------------------------------
    # SEASONALITY ADJUSTMENT
    # ---------------------------------------------------------------

    seasonal_multiplier = np.array([
        seasonal.get(
            date.dayofweek,
            1.0
        )
        for date in future_dates
    ])

    predictions *= (
        seasonal_multiplier
    )

    predictions = np.maximum(
        predictions,
        0
    )

    # ---------------------------------------------------------------
    # UNCERTAINTY
    # ---------------------------------------------------------------

    relative_uncertainty = max(
        0.05,
        residual_std
    )

    uncertainty = (
        predictions
        *
        relative_uncertainty
    )

    lower = np.maximum(
        0,
        predictions
        -
        1.96 * uncertainty
    )

    upper = (
        predictions
        +
        1.96 * uncertainty
    )

    # ---------------------------------------------------------------
    # TREND CLASSIFICATION
    # ---------------------------------------------------------------

    if slope > 0.005:

        trend = "STRONG_GROWTH"

    elif slope > 0.001:

        trend = "GROWTH"

    elif slope < -0.005:

        trend = "STRONG_DECLINE"

    elif slope < -0.001:

        trend = "DECLINE"

    else:

        trend = "STABLE"

    # ---------------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------------

    history_score = min(
        1.0,
        history_days / 180
    )

    confidence = (
        35
        +
        history_score * 30
        +
        r_squared * 25
        -
        min(
            20,
            residual_std * 10
        )
    )

    confidence = float(
        np.clip(
            confidence,
            25,
            95
        )
    )

    return {
        "future_dates": future_dates,
        "predictions": predictions,
        "lower": lower,
        "upper": upper,
        "trend": trend,
        "confidence": confidence,
        "history_days": history_days,
        "r_squared": r_squared,
        "momentum": momentum,
        "method": (
            "LOG_LINEAR_TREND"
            "_DOW_SEASONALITY"
            "_MOMENTUM"
        ),
    }


# =====================================================================
# GENERATE FORECASTS
# =====================================================================

print("\nBuilding forecasts...")

content_ids = (
    history["content_id"]
    .dropna()
    .unique()
)

print(
    f"Content assets to forecast: "
    f"{len(content_ids):,}"
)


METRICS = [
    (
        "VIEWING_DEMAND",
        "watch_hours"
    ),
    (
        "REVENUE",
        "total_revenue"
    ),
    (
        "ENGAGEMENT",
        "engagement_completion_rate"
    ),
]


forecast_records = []


for counter, content_id in enumerate(
    content_ids,
    start=1
):

    content_history = history[
        history["content_id"] == content_id
    ].copy()

    for metric_name, value_column in METRICS:

        result = forecast_series(
            content_history,
            value_column,
            FORECAST_HORIZON
        )

        if result is None:
            continue

        future_dates = result[
            "future_dates"
        ]

        predictions = result[
            "predictions"
        ]

        lower = result[
            "lower"
        ]

        upper = result[
            "upper"
        ]

        for index, forecast_date in enumerate(
            future_dates
        ):

            forecast_records.append({

                "content_id":
                    int(content_id),

                "forecast_date":
                    forecast_date.date(),

                "forecast_horizon_day":
                    index + 1,

                "metric_name":
                    metric_name,

                "forecast_value":
                    float(
                        max(
                            0,
                            predictions[index]
                        )
                    ),

                "lower_bound":
                    float(
                        max(
                            0,
                            lower[index]
                        )
                    ),

                "upper_bound":
                    float(
                        max(
                            0,
                            upper[index]
                        )
                    ),

                "trend":
                    result["trend"],

                "confidence":
                    float(
                        result["confidence"]
                    ),

                "model_method":
                    result["method"],

                "history_days":
                    int(
                        result["history_days"]
                    ),

                "r_squared":
                    float(
                        result["r_squared"]
                    ),

                "momentum":
                    float(
                        result["momentum"]
                    ),

                "created_at":
                    datetime.now(),

            })

    if (
        counter % 100 == 0
        or counter == len(content_ids)
    ):

        print(
            f"Processed "
            f"{counter:,}/"
            f"{len(content_ids):,} "
            f"content assets"
        )


# =====================================================================
# BUILD DATAFRAME
# =====================================================================

forecast_df = pd.DataFrame(
    forecast_records
)

if forecast_df.empty:

    raise ValueError(
        "Forecast generation produced zero records."
    )


# =====================================================================
# FORECAST ID
# =====================================================================

forecast_df.insert(
    0,
    "forecast_id",
    np.arange(
        1,
        len(forecast_df) + 1
    )
)


# =====================================================================
# ROUND NUMERIC FIELDS
# =====================================================================

for column in [
    "forecast_value",
    "lower_bound",
    "upper_bound",
    "confidence",
    "r_squared",
    "momentum",
]:

    forecast_df[column] = (
        forecast_df[column]
        .round(4)
    )


# =====================================================================
# VALIDATION
# =====================================================================

print("\nRunning forecast validation...")


# ---------------------------------------------------------------------
# Forecast IDs
# ---------------------------------------------------------------------

if not forecast_df[
    "forecast_id"
].is_unique:

    raise ValueError(
        "Forecast IDs are not unique."
    )

print(
    "✓ Forecast IDs unique"
)


# ---------------------------------------------------------------------
# Content IDs
# ---------------------------------------------------------------------

if forecast_df[
    "content_id"
].isna().any():

    raise ValueError(
        "NULL content IDs detected."
    )

print(
    "✓ Content relationships valid"
)


# ---------------------------------------------------------------------
# Forecast dates
# ---------------------------------------------------------------------

forecast_dates = pd.to_datetime(
    forecast_df[
        "forecast_date"
    ],
    errors="coerce"
)

if forecast_dates.isna().any():

    raise ValueError(
        "Invalid forecast dates detected."
    )

print(
    "✓ Forecast dates valid"
)


# ---------------------------------------------------------------------
# Critical future-date validation
# ---------------------------------------------------------------------

invalid_dates = (
    forecast_dates
    <= max_date
)

if invalid_dates.any():

    invalid_count = int(
        invalid_dates.sum()
    )

    raise ValueError(
        f"Forecast contains "
        f"{invalid_count:,} dates that are "
        f"not after the historical cutoff "
        f"{max_date.date()}."
    )

print(
    "✓ Forecast dates are after historical cutoff"
)


# ---------------------------------------------------------------------
# Forecast values
# ---------------------------------------------------------------------

if (
    forecast_df[
        "forecast_value"
    ] < 0
).any():

    raise ValueError(
        "Negative forecast values detected."
    )

print(
    "✓ Forecast values non-negative"
)


# ---------------------------------------------------------------------
# Prediction intervals
# ---------------------------------------------------------------------

if (
    forecast_df["lower_bound"]
    >
    forecast_df["forecast_value"]
).any():

    raise ValueError(
        "Lower bound exceeds forecast."
    )

if (
    forecast_df["upper_bound"]
    <
    forecast_df["forecast_value"]
).any():

    raise ValueError(
        "Upper bound below forecast."
    )

print(
    "✓ Prediction intervals valid"
)


# ---------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------

if (
    (
        forecast_df[
            "confidence"
        ] < 0
    )
    |
    (
        forecast_df[
            "confidence"
        ] > 100
    )
).any():

    raise ValueError(
        "Confidence values outside 0-100."
    )

print(
    "✓ Confidence scores valid"
)


# ---------------------------------------------------------------------
# Forecast horizon
# ---------------------------------------------------------------------

if (
    forecast_df[
        "forecast_horizon_day"
    ] < 1
).any():

    raise ValueError(
        "Invalid forecast horizon."
    )

if (
    forecast_df[
        "forecast_horizon_day"
    ]
    > FORECAST_HORIZON
).any():

    raise ValueError(
        "Forecast horizon exceeds configuration."
    )

print(
    "✓ Forecast horizon valid"
)


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------

VALID_METRICS = {
    "VIEWING_DEMAND",
    "REVENUE",
    "ENGAGEMENT",
}

actual_metrics = set(
    forecast_df[
        "metric_name"
    ].unique()
)

invalid_metrics = (
    actual_metrics
    -
    VALID_METRICS
)

if invalid_metrics:

    raise ValueError(
        f"Invalid forecast metrics: "
        f"{invalid_metrics}"
    )

print(
    "✓ Forecast metrics valid"
)


# ---------------------------------------------------------------------
# Duplicate business keys
# ---------------------------------------------------------------------

duplicate_mask = (
    forecast_df
    .duplicated(
        subset=[
            "content_id",
            "forecast_date",
            "metric_name",
        ]
    )
)

if duplicate_mask.any():

    duplicate_count = int(
        duplicate_mask.sum()
    )

    raise ValueError(
        f"Duplicate forecast records detected: "
        f"{duplicate_count:,}"
    )

print(
    "✓ No duplicate forecast records"
)


# ---------------------------------------------------------------------
# Forecast horizon consistency
# ---------------------------------------------------------------------

horizon_by_content_metric = (
    forecast_df
    .groupby(
        [
            "content_id",
            "metric_name"
        ]
    )[
        "forecast_horizon_day"
    ]
    .agg(
        ["min", "max", "count"]
    )
)

invalid_horizon_groups = (
    (horizon_by_content_metric["min"] != 1)
    |
    (
        horizon_by_content_metric["max"]
        != FORECAST_HORIZON
    )
    |
    (
        horizon_by_content_metric["count"]
        != FORECAST_HORIZON
    )
)

if invalid_horizon_groups.any():

    raise ValueError(
        "One or more content/metric groups "
        "do not contain exactly the configured "
        f"{FORECAST_HORIZON}-day horizon."
    )

print(
    "✓ Complete forecast horizon for every content/metric"
)


# =====================================================================
# SAVE ONLY AFTER ALL VALIDATION PASSES
# =====================================================================

if forecast_df.empty:

    raise ValueError(
        "Forecast dataframe is empty."
    )

print(
    f"\nSaving forecast output:\n"
    f"{OUTPUT_FILE}"
)

forecast_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =====================================================================
# FINAL REPORT
# =====================================================================

print("\n" + "=" * 70)
print("FORECAST GENERATION COMPLETE")
print("=" * 70)

print(
    f"Forecast records       : "
    f"{len(forecast_df):,}"
)

print(
    f"Content assets         : "
    f"{forecast_df['content_id'].nunique():,}"
)

print(
    f"Forecast metrics       : "
    f"{forecast_df['metric_name'].nunique():,}"
)

print(
    f"Forecast horizon       : "
    f"{FORECAST_HORIZON} days"
)

print(
    f"Forecast start date    : "
    f"{forecast_df['forecast_date'].min()}"
)

print(
    f"Forecast end date      : "
    f"{forecast_df['forecast_date'].max()}"
)

print(
    f"Average confidence     : "
    f"{forecast_df['confidence'].mean():.2f}%"
)

print(
    f"High-confidence rows   : "
    f"{(
        forecast_df['confidence'] >= 75
    ).sum():,}"
)

print("\nMetric distribution:")

print(
    forecast_df[
        "metric_name"
    ]
    .value_counts()
    .to_string()
)

print("\nTrend distribution:")

print(
    forecast_df[
        "trend"
    ]
    .value_counts()
    .to_string()
)

print("\nValidation:")
print("✓ Forecast IDs unique")
print("✓ Content relationships valid")
print("✓ Forecast dates valid")
print("✓ Forecast dates after historical cutoff")
print("✓ Forecast values non-negative")
print("✓ Prediction intervals valid")
print("✓ Confidence scores valid")
print("✓ Forecast horizons valid")
print("✓ Forecast metrics valid")
print("✓ No duplicate records")
print("✓ Complete 30-day horizon")
print("✓ Output saved only after validation")

print("\nOutput:")
print(OUTPUT_FILE)

print("=" * 70)
