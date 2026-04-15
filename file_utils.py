import csv
from pathlib import Path


def safe_load_csv(filepath, skip_header=True):
    """
    Safely loads CSV files.
    Returns empty list if file doesn't exist or is broken.
    """

    path = Path(filepath)

    if not path.exists():
        return []

    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            if skip_header:
                next(reader, None)

            return [row for row in reader]

    except Exception:
        # SAFE MODE: never crash
        return []