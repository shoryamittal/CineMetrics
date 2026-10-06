"""
CineMetrics Master Pipeline Entry Point
Delegates execution to generate_all.py
"""
import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent
generate_all_script = scripts_dir / "generate_all.py"

if __name__ == "__main__":
    import runpy
    runpy.run_path(str(generate_all_script), run_name="__main__")
