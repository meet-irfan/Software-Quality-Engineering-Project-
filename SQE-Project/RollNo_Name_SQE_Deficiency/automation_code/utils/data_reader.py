"""Reads external test data so that data sets are not hard-coded inside tests."""
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_csv(file_name: str) -> list[dict]:
    """Return every row of data/<file_name> as a dict (header row = keys)."""
    path = DATA_DIR / file_name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
