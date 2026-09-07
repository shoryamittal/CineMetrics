# ==========================================================
# ECDIP - MASTER DATA GENERATION PIPELINE
# ==========================================================

from pathlib import Path
import os
import subprocess
import sys
from datetime import datetime


# ==========================================================
# PROJECT PATHS
# ==========================================================

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent

PYTHON = sys.executable

# The generators include human-readable status markers and currency symbols.
# Windows often defaults to a legacy console code page (for example cp1252),
# which cannot write those characters and previously stopped the pipeline
# after its first successful generator.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ==========================================================
# GENERATORS
# ==========================================================
#
# IMPORTANT:
# This list uses YOUR ACTUAL filenames.
#
# Order follows dependencies.
# ==========================================================

GENERATORS = [

    # ---------------- DIMENSIONS ----------------

    "generate_age_ratings.py",
    "generate_genres.py",
    "generate_languages.py",
    "generate_platforms.py",
    "generate_regions.py",
    "generate_subscription_plans.py",
    "generate_studios.py",
    "generate_calendar.py",

    # ---------------- CORE CONTENT ----------------

    "generate_content.py",
    "generate_contracts.py",
    "generate_campaigns.py",

    # ---------------- CORE FACTS ----------------

    "generate_viewing_events.py",
    "generate_engagement.py",
    "generate_marketing.py",

    # ---------------- CUSTOMER ----------------

    "generate_subscribers.py",
    "generate_subscription_events.py",

    # ---------------- SEARCH ----------------

    "generate_search_events.py",

    # ---------------- FINANCIAL ----------------

    "generate_revenue.py",
    "generate_content_cost.py",
    "generate_forecast.py",
]


# ==========================================================
# EXPECTED OUTPUTS
# ==========================================================

EXPECTED_OUTPUTS = {

    "generate_age_ratings.py":
        "dim_age_rating.csv",

    "generate_genres.py":
        "dim_genre.csv",

    "generate_languages.py":
        "dim_language.csv",

    "generate_platforms.py":
        "dim_platform.csv",

    "generate_regions.py":
        "dim_region.csv",

    "generate_subscription_plans.py":
        "dim_subscription_plan.csv",

    "generate_studios.py":
        "dim_studio.csv",

    "generate_calendar.py":
        "dim_calendar.csv",

    "generate_content.py":
        "dim_content.csv",

    "generate_contracts.py":
        "dim_contract.csv",

    "generate_campaigns.py":
        "dim_campaign.csv",

    "generate_viewing_events.py":
        "fact_viewing_events.csv",

    "generate_engagement.py":
        "fact_engagement.csv",

    "generate_marketing.py":
        "fact_marketing.csv",

    "generate_subscribers.py":
        "dim_subscriber.csv",

    "generate_subscription_events.py":
        "fact_subscription_events.csv",

    "generate_search_events.py":
        "fact_search_events.csv",

    "generate_revenue.py":
        "fact_revenue.csv",

    "generate_content_cost.py":
        "fact_content_cost.csv",

    "generate_forecast.py":
        "fact_forecast.csv",
}


# ==========================================================
# FUNCTIONS
# ==========================================================

def verify_generator_exists(script_name):

    path = SCRIPTS_DIR / script_name

    if not path.exists():

        raise FileNotFoundError(
            f"Generator not found:\n{path}"
        )

    return path


def verify_output(script_name):

    expected = EXPECTED_OUTPUTS.get(
        script_name
    )

    if expected is None:
        return

    output_path = (
        PROJECT_DIR
        / "data"
        / "synthetic"
        / expected
    )

    if not output_path.exists():

        raise FileNotFoundError(
            f"\nExpected output was not created:\n"
            f"{output_path}"
        )

    if output_path.stat().st_size == 0:

        raise ValueError(
            f"\nOutput file is empty:\n"
            f"{output_path}"
        )

    print(
        f"✓ Output verified: {expected}"
    )


def run_generator(script_name):

    script_path = verify_generator_exists(
        script_name
    )

    print("\n" + "=" * 70)
    print(f"RUNNING: {script_name}")
    print("=" * 70)

    start = datetime.now()

    child_environment = os.environ.copy()
    child_environment["PYTHONUTF8"] = "1"

    result = subprocess.run(
        [
            PYTHON,
            str(script_path)
        ],
        cwd=PROJECT_DIR,
        env=child_environment,
    )

    elapsed = (
        datetime.now() - start
    ).total_seconds()

    if result.returncode != 0:

        raise RuntimeError(
            f"{script_name} failed "
            f"with exit code "
            f"{result.returncode}"
        )

    verify_output(
        script_name
    )

    print(
        f"✓ Completed in {elapsed:.2f} seconds"
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n" + "#" * 70)
    print("# ECDIP MASTER DATA PIPELINE")
    print("#" * 70)

    print(
        f"\nPython:\n{PYTHON}"
    )

    print(
        f"\nGenerators scheduled: "
        f"{len(GENERATORS)}"
    )

    start = datetime.now()

    completed = []

    try:

        for script in GENERATORS:

            run_generator(
                script
            )

            completed.append(
                script
            )

    except Exception as error:

        print("\n" + "#" * 70)
        print("# PIPELINE STOPPED")
        print("#" * 70)

        print(
            f"\nCompleted: "
            f"{len(completed)}/{len(GENERATORS)}"
        )

        print("\nCompleted generators:")

        for script in completed:

            print(
                f"  ✓ {script}"
            )

        print(
            f"\nERROR:\n{error}"
        )

        print(
            "\nPipeline stopped safely."
        )

        sys.exit(1)

    elapsed = (
        datetime.now() - start
    ).total_seconds()

    print("\n" + "#" * 70)
    print("# MASTER PIPELINE COMPLETE")
    print("#" * 70)

    print(
        f"\nCompleted: "
        f"{len(completed)}/{len(GENERATORS)}"
    )

    print(
        f"Total time: "
        f"{elapsed:.2f} seconds"
    )

    print(
        "\n✓ All configured generators "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
