"""IO helpers for the DSSA assessment."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "local" / "data.json"
OUTPUT_PATH = PROJECT_ROOT / "local" / "output.csv"


def load_data() -> dict:
    """Load the raw company response data."""
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_output(output: list[dict], fieldnames: list[str]) -> None:
    """Write the scoring output to a CSV file in the local folder."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        if not fieldnames:
            return
        import csv

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in output:
            writer.writerow(row)
