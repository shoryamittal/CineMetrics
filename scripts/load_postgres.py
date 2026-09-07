"""
======================================================================
ECDIP - POSTGRESQL WAREHOUSE LOADER
======================================================================

Purpose:
    Load generated CSV datasets into PostgreSQL using COPY.

Database:
    cpip

Schema:
    public

Design:
    CSV
      ↓
    PostgreSQL COPY
      ↓
    Row validation
      ↓
    Primary-key validation
      ↓
    Foreign-key validation
      ↓
    Warehouse validation

Important:
    This loader does NOT use pandas for the large fact files.

======================================================================
"""

from pathlib import Path
import csv
import getpass
import os
import sys
import time

import psycopg2
from psycopg2 import sql


# =====================================================================
# CONFIGURATION
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "synthetic"

DB_HOST = os.getenv("ECDIP_DB_HOST", "localhost")
DB_PORT = int(os.getenv("ECDIP_DB_PORT", "1076"))
DB_NAME = os.getenv("ECDIP_DB_NAME", "cpip")
DB_USER = os.getenv("ECDIP_DB_USER", "postgres")

DB_SCHEMA = "public"


# =====================================================================
# LOAD ORDER
# =====================================================================

# Dimensions first.
# Facts after dimensions.

LOAD_ORDER = [

    # ---------------------------------------------------------------
    # DIMENSIONS
    # ---------------------------------------------------------------

    "dim_age_rating.csv",
    "dim_genre.csv",
    "dim_language.csv",
    "dim_platform.csv",
    "dim_region.csv",
    "dim_studio.csv",
    "dim_calendar.csv",
    "dim_campaign.csv",
    "dim_subscription_plan.csv",
    "dim_subscriber.csv",
    "dim_content.csv",
    "dim_contract.csv",

    # ---------------------------------------------------------------
    # FACTS
    # ---------------------------------------------------------------

    "fact_content_cost.csv",
    "fact_marketing.csv",
    "fact_subscription_events.csv",
    "fact_search_events.csv",
    "fact_viewing_events.csv",
    "fact_engagement.csv",
    "fact_revenue.csv",
    "fact_forecast.csv",
]


# =====================================================================
# EXPECTED TABLES
# =====================================================================

EXPECTED_TABLES = [
    Path(filename).stem
    for filename in LOAD_ORDER
]


# =====================================================================
# UTILITY FUNCTIONS
# =====================================================================

def print_header(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def fail(message):

    print("\n" + "=" * 70)
    print("PIPELINE STOPPED")
    print("=" * 70)
    print()
    print(message)
    print()

    sys.exit(1)


def get_csv_header(csv_file):

    with open(
        csv_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(file)

        header = next(reader)

    return [
        column.strip()
        for column in header
    ]


def get_table_columns(cursor, table_name):

    cursor.execute(
        """
        SELECT
            column_name,
            is_nullable,
            column_default,
            ordinal_position
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (
            DB_SCHEMA,
            table_name
        )
    )

    rows = cursor.fetchall()

    return rows


def table_exists(cursor, table_name):

    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
        );
        """,
        (
            DB_SCHEMA,
            table_name
        )
    )

    return cursor.fetchone()[0]


def get_primary_key_columns(cursor, table_name):

    cursor.execute(
        """
        SELECT
            kcu.column_name
        FROM information_schema.table_constraints tc

        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name =
             kcu.constraint_name
         AND tc.table_schema =
             kcu.table_schema
         AND tc.table_name =
             kcu.table_name

        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = %s
          AND tc.table_name = %s

        ORDER BY kcu.ordinal_position;
        """,
        (
            DB_SCHEMA,
            table_name
        )
    )

    return [
        row[0]
        for row in cursor.fetchall()
    ]


def get_foreign_keys(cursor):

    cursor.execute(
        """
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS referenced_table,
            ccu.column_name AS referenced_column

        FROM information_schema.table_constraints tc

        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name =
             kcu.constraint_name
         AND tc.table_schema =
             kcu.table_schema

        JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name =
             ccu.constraint_name
         AND tc.table_schema =
             ccu.table_schema

        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = %s

        ORDER BY tc.table_name;
        """,
        (DB_SCHEMA,)
    )

    return cursor.fetchall()


def get_row_count(cursor, table_name):

    cursor.execute(
        sql.SQL(
            "SELECT COUNT(*) FROM {}.{}"
        ).format(
            sql.Identifier(DB_SCHEMA),
            sql.Identifier(table_name)
        )
    )

    return cursor.fetchone()[0]


# =====================================================================
# DATABASE CONNECTION
# =====================================================================

print_header(
    "ECDIP - POSTGRESQL WAREHOUSE LOADER"
)

print(
    f"Database : {DB_NAME}"
)

print(
    f"Host     : {DB_HOST}"
)

print(
    f"Port     : {DB_PORT}"
)

print(
    f"User     : {DB_USER}"
)

print(
    f"Schema   : {DB_SCHEMA}"
)


password = os.getenv("ECDIP_DB_PASSWORD")

if not password:

    password = getpass.getpass(
        "\nPostgreSQL password: "
    )


try:

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=password
    )

except Exception as error:

    fail(
        "Could not connect to PostgreSQL.\n\n"
        f"Error: {error}"
    )


connection.autocommit = False

cursor = connection.cursor()

print(
    "\n✓ PostgreSQL connection successful"
)


# =====================================================================
# VERIFY TABLES
# =====================================================================

print_header(
    "VERIFYING WAREHOUSE TABLES"
)

missing_tables = []

for table_name in EXPECTED_TABLES:

    if not table_exists(
        cursor,
        table_name
    ):

        missing_tables.append(
            table_name
        )

        print(
            f"✗ Missing table: {table_name}"
        )

    else:

        print(
            f"✓ Table found: {table_name}"
        )


if missing_tables:

    connection.close()

    fail(
        "The following PostgreSQL tables "
        "are missing:\n"
        +
        "\n".join(
            missing_tables
        )
    )


# =====================================================================
# VERIFY CSV FILES
# =====================================================================

print_header(
    "VERIFYING CSV FILES"
)

missing_files = []

for filename in LOAD_ORDER:

    csv_file = DATA_DIR / filename

    if not csv_file.exists():

        missing_files.append(
            filename
        )

        print(
            f"✗ Missing CSV: {filename}"
        )

    else:

        size_mb = (
            csv_file.stat().st_size
            /
            (1024 * 1024)
        )

        print(
            f"✓ {filename:<35} "
            f"{size_mb:,.2f} MB"
        )


if missing_files:

    connection.close()

    fail(
        "The following CSV files are missing:\n"
        +
        "\n".join(
            missing_files
        )
    )


# =====================================================================
# CURRENT ROW COUNTS
# =====================================================================

print_header(
    "CURRENT DATABASE ROW COUNTS"
)

current_counts = {}

for table_name in EXPECTED_TABLES:

    count = get_row_count(
        cursor,
        table_name
    )

    current_counts[
        table_name
    ] = count

    print(
        f"{table_name:<35} "
        f"{count:>12,}"
    )


# =====================================================================
# LOAD FUNCTION
# =====================================================================

def load_csv(
    connection,
    cursor,
    csv_file,
    table_name
):

    print(
        f"\nLoading {table_name}..."
    )

    start_time = time.time()

    # ---------------------------------------------------------------
    # Read CSV header only
    # ---------------------------------------------------------------

    csv_columns = get_csv_header(
        csv_file
    )

    if not csv_columns:

        raise ValueError(
            f"{csv_file.name} has no columns."
        )

    # ---------------------------------------------------------------
    # Get database columns
    # ---------------------------------------------------------------

    db_columns_info = get_table_columns(
        cursor,
        table_name
    )

    if not db_columns_info:

        raise ValueError(
            f"No columns found for "
            f"table {table_name}."
        )

    db_columns = [
        row[0]
        for row in db_columns_info
    ]

    # ---------------------------------------------------------------
    # Check CSV columns exist in DB
    # ---------------------------------------------------------------

    missing_in_db = [
        column
        for column in csv_columns
        if column not in db_columns
    ]

    if missing_in_db:

        raise ValueError(
            f"{table_name}: CSV contains "
            f"columns not present in PostgreSQL: "
            f"{missing_in_db}"
        )

    # ---------------------------------------------------------------
    # Check required DB columns
    #
    # Required means:
    #   NOT NULL
    #   no default
    #
    # ---------------------------------------------------------------

    required_columns = []

    for (
        column_name,
        is_nullable,
        column_default,
        ordinal_position
    ) in db_columns_info:

        if (
            is_nullable == "NO"
            and column_default is None
            and column_name not in csv_columns
        ):

            required_columns.append(
                column_name
            )

    if required_columns:

        raise ValueError(
            f"{table_name}: required PostgreSQL "
            f"columns missing from CSV: "
            f"{required_columns}"
        )

    # ---------------------------------------------------------------
    # COPY
    # ---------------------------------------------------------------

    column_sql = sql.SQL(", ").join(
        sql.Identifier(column)
        for column in csv_columns
    )

    copy_command = sql.SQL(
        """
        COPY {}.{} ({})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            QUOTE '"',
            ESCAPE '"'
        )
        """
    ).format(
        sql.Identifier(DB_SCHEMA),
        sql.Identifier(table_name),
        column_sql
    )

    with open(
        csv_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        cursor.copy_expert(
            copy_command.as_string(
                connection
            ),
            file
        )

    connection.commit()

    elapsed = (
        time.time()
        -
        start_time
    )

    row_count = get_row_count(
        cursor,
        table_name
    )

    print(
        f"✓ Loaded {table_name}"
    )

    print(
        f"  Rows now : {row_count:,}"
    )

    print(
        f"  Time     : {elapsed:.2f} seconds"
    )

    return row_count


# =====================================================================
# LOAD ALL TABLES
# =====================================================================

print_header(
    "STARTING CSV → POSTGRESQL COPY"
)

loaded_counts = {}

try:

    for index, filename in enumerate(
        LOAD_ORDER,
        start=1
    ):

        table_name = Path(
            filename
        ).stem

        csv_file = (
            DATA_DIR /
            filename
        )

        print(
            f"\n[{index}/{len(LOAD_ORDER)}]"
        )

        count = load_csv(
            connection,
            cursor,
            csv_file,
            table_name
        )

        loaded_counts[
            table_name
        ] = count


except Exception as error:

    connection.rollback()

    connection.close()

    fail(
        "Generator/loader failed.\n\n"
        f"Error:\n{error}"
    )


# =====================================================================
# PRIMARY KEY VALIDATION
# =====================================================================

print_header(
    "PRIMARY KEY VALIDATION"
)

primary_key_errors = []

for table_name in EXPECTED_TABLES:

    primary_columns = (
        get_primary_key_columns(
            cursor,
            table_name
        )
    )

    if not primary_columns:

        print(
            f"⚠ {table_name}: "
            f"No primary key detected"
        )

        continue

    columns_sql = sql.SQL(", ").join(
        sql.Identifier(column)
        for column in primary_columns
    )

    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM (
            SELECT {}
            FROM {}.{}
            GROUP BY {}
            HAVING COUNT(*) > 1
        ) duplicates
        """
    ).format(
        columns_sql,
        sql.Identifier(DB_SCHEMA),
        sql.Identifier(table_name),
        columns_sql
    )

    cursor.execute(query)

    duplicate_groups = (
        cursor.fetchone()[0]
    )

    if duplicate_groups > 0:

        primary_key_errors.append(
            (
                table_name,
                duplicate_groups
            )
        )

        print(
            f"✗ {table_name}: "
            f"{duplicate_groups:,} duplicate "
            f"primary-key groups"
        )

    else:

        print(
            f"✓ {table_name}: "
            f"primary key unique"
        )


if primary_key_errors:

    connection.close()

    fail(
        "Primary-key validation failed."
    )


# =====================================================================
# FOREIGN KEY VALIDATION
# =====================================================================

print_header(
    "FOREIGN KEY RELATIONSHIP VALIDATION"
)

foreign_keys = get_foreign_keys(
    cursor
)

foreign_key_errors = []

for (
    table_name,
    column_name,
    referenced_table,
    referenced_column
) in foreign_keys:

    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM {}.{} child
        LEFT JOIN {}.{} parent
          ON child.{} = parent.{}
        WHERE child.{} IS NOT NULL
          AND parent.{} IS NULL
        """
    ).format(
        sql.Identifier(DB_SCHEMA),
        sql.Identifier(table_name),

        sql.Identifier(DB_SCHEMA),
        sql.Identifier(referenced_table),

        sql.Identifier(column_name),
        sql.Identifier(referenced_column),

        sql.Identifier(column_name),
        sql.Identifier(referenced_column)
    )

    cursor.execute(query)

    orphan_count = (
        cursor.fetchone()[0]
    )

    if orphan_count > 0:

        foreign_key_errors.append(
            (
                table_name,
                column_name,
                referenced_table,
                referenced_column,
                orphan_count
            )
        )

        print(
            f"✗ {table_name}.{column_name}"
            f" → "
            f"{referenced_table}."
            f"{referenced_column}"
            f": "
            f"{orphan_count:,} orphan rows"
        )

    else:

        print(
            f"✓ {table_name}.{column_name}"
            f" → "
            f"{referenced_table}."
            f"{referenced_column}"
        )


if foreign_key_errors:

    connection.close()

    fail(
        "Foreign-key validation failed."
    )


# =====================================================================
# FORECAST-SPECIFIC VALIDATION
# =====================================================================

print_header(
    "FORECAST VALIDATION"
)

cursor.execute(
    """
    SELECT COUNT(*)
    FROM public.fact_forecast;
    """
)

forecast_rows = (
    cursor.fetchone()[0]
)

if forecast_rows == 0:

    connection.close()

    fail(
        "fact_forecast is still empty."
    )

print(
    f"✓ Forecast rows: "
    f"{forecast_rows:,}"
)


cursor.execute(
    """
    SELECT
        COUNT(DISTINCT content_id)
    FROM public.fact_forecast;
    """
)

forecast_content_count = (
    cursor.fetchone()[0]
)

print(
    f"✓ Forecast content assets: "
    f"{forecast_content_count:,}"
)


cursor.execute(
    """
    SELECT
        MIN(forecast_date),
        MAX(forecast_date)
    FROM public.fact_forecast;
    """
)

forecast_dates = cursor.fetchone()

print(
    f"✓ Forecast start: "
    f"{forecast_dates[0]}"
)

print(
    f"✓ Forecast end: "
    f"{forecast_dates[1]}"
)


cursor.execute(
    """
    SELECT
        metric_name,
        COUNT(*)
    FROM public.fact_forecast
    GROUP BY metric_name
    ORDER BY metric_name;
    """
)

print(
    "\nForecast metric distribution:"
)

for metric_name, count in cursor.fetchall():

    print(
        f"  {metric_name:<25}"
        f"{count:>12,}"
    )


# =====================================================================
# FINAL TABLE SUMMARY
# =====================================================================

print_header(
    "FINAL WAREHOUSE ROW COUNTS"
)

final_counts = {}

for table_name in EXPECTED_TABLES:

    count = get_row_count(
        cursor,
        table_name
    )

    final_counts[
        table_name
    ] = count

    status = (
        "✓"
        if count > 0
        else "✗"
    )

    print(
        f"{status} "
        f"{table_name:<35}"
        f"{count:>15,}"
    )


# =====================================================================
# EMPTY TABLE DETECTION
# =====================================================================

empty_tables = [
    table_name
    for table_name, count
    in final_counts.items()
    if count == 0
]

if empty_tables:

    connection.close()

    fail(
        "The following expected tables "
        "are still empty:\n"
        +
        "\n".join(
            empty_tables
        )
    )


# =====================================================================
# COMMIT
# =====================================================================

connection.commit()


# =====================================================================
# CLOSE
# =====================================================================

cursor.close()

connection.close()


# =====================================================================
# FINAL REPORT
# =====================================================================

print_header(
    "ECDIP POSTGRESQL LOAD COMPLETE"
)

print(
    f"Database : {DB_NAME}"
)

print(
    f"Schema   : {DB_SCHEMA}"
)

print(
    f"Tables   : {len(EXPECTED_TABLES)}"
)

print()

for table_name in EXPECTED_TABLES:

    print(
        f"✓ {table_name:<35}"
        f"{final_counts[table_name]:>15,}"
    )


print("\nValidation:")

print(
    "✓ All expected tables exist"
)

print(
    "✓ All CSV files found"
)

print(
    "✓ CSV columns validated"
)

print(
    "✓ PostgreSQL COPY completed"
)

print(
    "✓ Primary keys validated"
)

print(
    "✓ Foreign-key relationships validated"
)

print(
    "✓ Forecast table populated"
)

print(
    "✓ No expected tables are empty"
)

print("\n" + "=" * 70)
print("WAREHOUSE READY FOR SQL ANALYTICS")
print("=" * 70)
