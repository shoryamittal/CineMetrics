from pathlib import Path
import csv
import psycopg2

# ==========================================================
# ECDIP - LOAD ONLY FACT_REVENUE
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "synthetic" / "fact_revenue.csv"

DB_NAME = "cpip"
HOST = "localhost"
PORT = 1076
USER = "postgres"

print("=" * 70)
print("ECDIP - FACT REVENUE ONLY LOADER")
print("=" * 70)

print(f"Database : {DB_NAME}")
print(f"Host     : {HOST}")
print(f"Port     : {PORT}")
print(f"User     : {USER}")
print(f"CSV      : {CSV_FILE}")

password = input("\nPostgreSQL password: ")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        host=HOST,
        port=PORT,
        user=USER,
        password=password
    )

    print("\n✓ PostgreSQL connection successful")

    cur = conn.cursor()

    # ------------------------------------------------------
    # Verify CSV
    # ------------------------------------------------------

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Revenue CSV not found: {CSV_FILE}"
        )

    print("\nChecking revenue CSV...")

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        reader = csv.reader(f)

        header = next(reader)

        print(
            f"✓ Columns detected: {len(header)}"
        )

        print(
            "✓ Header:",
            ", ".join(header)
        )

    # ------------------------------------------------------
    # Clear ONLY fact_revenue
    # ------------------------------------------------------

    print("\nClearing existing fact_revenue...")

    cur.execute(
        "TRUNCATE TABLE public.fact_revenue;"
    )

    conn.commit()

    print("✓ fact_revenue cleared")

    # ------------------------------------------------------
    # PostgreSQL COPY
    # ------------------------------------------------------

    print("\nLoading fact_revenue using PostgreSQL COPY...")

    copy_sql = """
        COPY public.fact_revenue (
            revenue_id,
            viewing_id,
            content_id,
            region_id,
            plan_id,
            date_id,
            revenue_type,
            revenue_amount,
            created_at
        )
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            QUOTE '"'
        )
    """

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        cur.copy_expert(
            copy_sql,
            f
        )

    conn.commit()

    print("✓ COPY completed")

    # ------------------------------------------------------
    # Row count
    # ------------------------------------------------------

    cur.execute(
        """
        SELECT COUNT(*)
        FROM public.fact_revenue;
        """
    )

    row_count = cur.fetchone()[0]

    print(
        f"\nRows loaded: {row_count:,}"
    )

    # ------------------------------------------------------
    # Revenue summary
    # ------------------------------------------------------

    cur.execute(
        """
        SELECT
            ROUND(SUM(revenue_amount)::numeric, 2),
            ROUND(AVG(revenue_amount)::numeric, 2),
            MIN(revenue_amount),
            MAX(revenue_amount)
        FROM public.fact_revenue;
        """
    )

    total, average, minimum, maximum = cur.fetchone()

    print("\nRevenue summary:")
    print(f"Total   : ₹{total:,.2f}")
    print(f"Average : ₹{average:,.2f}")
    print(f"Minimum : ₹{minimum:,.2f}")
    print(f"Maximum : ₹{maximum:,.2f}")

    # ------------------------------------------------------
    # Relationship validation
    # ------------------------------------------------------

    print("\nValidating relationships...")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM public.fact_revenue r
        LEFT JOIN public.dim_content c
            ON r.content_id = c.content_id
        WHERE c.content_id IS NULL;
        """
    )

    invalid_content = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COUNT(*)
        FROM public.fact_revenue r
        LEFT JOIN public.dim_subscription_plan p
            ON r.plan_id = p.plan_id
        WHERE p.plan_id IS NULL;
        """
    )

    invalid_plan = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COUNT(*)
        FROM public.fact_revenue r
        LEFT JOIN public.dim_region rg
            ON r.region_id = rg.region_id
        WHERE rg.region_id IS NULL;
        """
    )

    invalid_region = cur.fetchone()[0]

    print(
        f"Invalid content IDs : {invalid_content}"
    )

    print(
        f"Invalid plan IDs    : {invalid_plan}"
    )

    print(
        f"Invalid region IDs  : {invalid_region}"
    )

    if (
        invalid_content != 0
        or invalid_plan != 0
        or invalid_region != 0
    ):
        raise ValueError(
            "Relationship validation failed."
        )

    # ------------------------------------------------------
    # Revenue type summary
    # ------------------------------------------------------

    print("\nRevenue by type:")

    cur.execute(
        """
        SELECT
            revenue_type,
            COUNT(*) AS transactions,
            ROUND(
                SUM(revenue_amount)::numeric,
                2
            ) AS total_revenue,
            ROUND(
                AVG(revenue_amount)::numeric,
                2
            ) AS average_revenue
        FROM public.fact_revenue
        GROUP BY revenue_type
        ORDER BY total_revenue DESC;
        """
    )

    for row in cur.fetchall():
        print(
            f"{row[0]:25} "
            f"{row[1]:>10,} "
            f"₹{row[2]:>18,.2f} "
            f"₹{row[3]:>12,.2f}"
        )

    cur.close()
    conn.close()

    print("\n" + "=" * 70)
    print("FACT_REVENUE LOAD SUCCESSFUL")
    print("=" * 70)

except Exception as e:

    print("\n" + "=" * 70)
    print("FACT_REVENUE LOAD FAILED")
    print("=" * 70)

    print("\nError:")
    print(e)

    try:
        conn.rollback()
        conn.close()
    except:
        pass