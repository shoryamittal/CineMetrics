from pathlib import Path
import csv
import os
import re
import psycopg2


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"

DB_HOST = os.getenv("ECDIP_DB_HOST", "localhost")
DB_PORT = int(os.getenv("ECDIP_DB_PORT", "1076"))
DB_NAME = os.getenv("ECDIP_DB_NAME", "cpip")
DB_USER = os.getenv("ECDIP_DB_USER", "postgres")

TABLES = [
    "dim_age_rating",
    "dim_genre",
    "dim_language",
    "dim_platform",
    "dim_region",
    "dim_studio",
    "dim_calendar",
    "dim_campaign",
    "dim_subscription_plan",
    "dim_subscriber",
    "dim_content",
    "dim_contract",
    "fact_content_cost",
    "fact_marketing",
    "fact_subscription_events",
    "fact_search_events",
    "fact_viewing_events",
    "fact_engagement",
    "fact_revenue",
    "fact_forecast",
]


def get_csv_columns(path):
    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.reader(f)
        return [x.strip() for x in next(reader)]


def sample_values(path, column, limit=1000):
    values = []

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            value = row.get(column, "")

            if value is not None:
                value = value.strip()

            if value != "":
                values.append(value)

            if len(values) >= limit:
                break

    return values


def detect_csv_type(path, column):

    values = sample_values(path, column)

    if not values:
        return "EMPTY"

    lower = {v.lower() for v in values}

    # BOOLEAN
    if lower <= {"true", "false"}:
        return "BOOLEAN"

    # DATE: YYYY-MM-DD
    if all(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}", v)
        for v in values
    ):
        return "DATE"

    # TIMESTAMP
    timestamp_pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2}"
        r"[ T]\d{2}:\d{2}:\d{2}"
    )

    if all(
        timestamp_pattern.match(v)
        for v in values
    ):
        return "TIMESTAMP"

    # INTEGER
    if all(
        re.fullmatch(r"-?\d+", v)
        for v in values
    ):
        return "INTEGER"

    # NUMERIC
    try:
        for v in values:
            float(v)

        return "NUMERIC"

    except ValueError:
        pass

    return "TEXT"


def compatible(csv_type, pg_type):

    pg_type = pg_type.lower()

    if csv_type == "BOOLEAN":
        return pg_type == "boolean"

    if csv_type == "DATE":
        return pg_type in {
            "date",
            "timestamp without time zone",
            "timestamp with time zone"
        }

    if csv_type == "TIMESTAMP":
        return pg_type in {
            "timestamp without time zone",
            "timestamp with time zone"
        }

    if csv_type == "INTEGER":
        return pg_type in {
            "smallint",
            "integer",
            "bigint",
            "numeric",
            "decimal"
        }

    if csv_type == "NUMERIC":
        return pg_type in {
            "smallint",
            "integer",
            "bigint",
            "numeric",
            "decimal",
            "real",
            "double precision"
        }

    if csv_type == "TEXT":
        return pg_type in {
            "character varying",
            "varchar",
            "text",
            "character",
            "char"
        }

    if csv_type == "EMPTY":
        return True

    return False


password = os.getenv("ECDIP_DB_PASSWORD")

if not password:
    import getpass
    password = getpass.getpass("PostgreSQL password: ")


connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=password
)

cursor = connection.cursor()

print("=" * 90)
print("ECDIP - FINAL CSV / POSTGRESQL SCHEMA + TYPE AUDIT")
print("=" * 90)

problems = []


for table in TABLES:

    csv_file = DATA_DIR / f"{table}.csv"

    print("\n" + "-" * 90)
    print(f"TABLE: {table}")
    print("-" * 90)

    if not csv_file.exists():
        print(f"❌ CSV NOT FOUND: {csv_file}")
        problems.append(
            f"{table}: CSV file missing"
        )
        continue

    csv_columns = get_csv_columns(csv_file)

    cursor.execute(
        """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (table,)
    )

    pg_columns = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    # ---------------------------------------------------------
    # CSV columns must exist in PostgreSQL
    # ---------------------------------------------------------

    for column in csv_columns:

        if column not in pg_columns:

            print(
                f"❌ MISSING COLUMN: {column}"
            )

            problems.append(
                f"{table}.{column}: missing"
            )

            continue

        csv_type = detect_csv_type(
            csv_file,
            column
        )

        pg_type = pg_columns[column]

        if compatible(csv_type, pg_type):

            print(
                f"✓ {column:<40}"
                f"CSV={csv_type:<10}"
                f"PG={pg_type}"
            )

        else:

            print(
                f"❌ TYPE MISMATCH: {column:<25}"
                f"CSV={csv_type:<10}"
                f"PG={pg_type}"
            )

            problems.append(
                f"{table}.{column}: "
                f"CSV={csv_type}, PG={pg_type}"
            )

    # ---------------------------------------------------------
    # DB-only columns
    # ---------------------------------------------------------

    db_only = [
        column
        for column in pg_columns
        if column not in csv_columns
    ]

    for column in db_only:

        print(
            f"⚠ DB ONLY: {column}"
        )


print("\n" + "=" * 90)

if problems:

    print("❌ REAL SCHEMA / TYPE PROBLEMS FOUND")

    for problem in problems:
        print(f"  - {problem}")

else:

    print(
        "✅ ALL CSV COLUMNS AND DATA TYPES ARE COMPATIBLE"
    )

print("=" * 90)

cursor.close()
connection.close()