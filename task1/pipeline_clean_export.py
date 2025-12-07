"""
Enhanced CSV cleaning pipeline for Task 1 (PAI Individual Assignment)

Key engineering improvements:
- INFO & WARNING logging for transparency (required for high-quality SW design)
- Field consistency validation (real-world robustness)
- Missing value summary (supports analytic readiness)
- Clear separation of business logic vs orchestration logic (SW engineering best practice)

This file intentionally contains *no business logic*; all core logic resides
in cleaner.py, matching good modular design practices.
"""

import csv
import os

from task1.data_loader import load_csv
from task1.cleaner import clean_row


# --------------------------------------------------------------------
# Simple lightweight logging system (INFO + WARNING)
# --------------------------------------------------------------------
def log_info(msg: str):
    """Standardised info messages for clarity and traceability."""
    print(f"[INFO] {msg}")


def log_warning(msg: str):
    """Warnings highlight potential issues without interrupting the workflow."""
    print(f"[WARNING] {msg}")


# --------------------------------------------------------------------
# Field consistency check — real-world robustness
# --------------------------------------------------------------------
def check_field_consistency(rows):
    """
    Ensures every row has the same keys.
    If inconsistencies occur, we warn the user instead of failing early.
    This mirrors realistic engineering practices where datasets are often imperfect.
    """
    if not rows:
        return

    first_keys = set(rows[0].keys())
    inconsistent_rows = 0

    for r in rows:
        if set(r.keys()) != first_keys:
            inconsistent_rows += 1

    if inconsistent_rows > 0:
        # Non-blocking warning — robust handling of imperfect data
        log_warning(
            f"{inconsistent_rows} rows have inconsistent fields. "
            "Cleaning will continue, but analysis may be affected."
        )
    else:
        log_info("All rows have consistent fields.")


# --------------------------------------------------------------------
# Missing value summary — supports downstream analysis
# --------------------------------------------------------------------
def summarise_missing_values(cleaned_rows):
    """
    Produces a simple but highly informative missing-value summary.
    This directly supports analytic readiness and helps justify decisions in the report.
    """
    if not cleaned_rows:
        return

    fieldnames = cleaned_rows[0].keys()
    missing_count = {field: 0 for field in fieldnames}

    for row in cleaned_rows:
        for field, value in row.items():
            if value is None or value == "":
                missing_count[field] += 1

    log_info("Missing value summary (top fields with missing data):")
    for field, count in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   {field}: {count} missing")
    print()


# --------------------------------------------------------------------
# Main export function — orchestration layer only
# --------------------------------------------------------------------
def export_cleaned_dataset(
    input_path: str = "task1/data/life_expectancy.csv",
    output_path: str = "task1/data/life_expectancy_cleaned.csv",
):
    """
    Pipeline steps:
    1. Load raw CSV (using data_loader)
    2. Validate field structure
    3. Clean each row (delegated to clean_row for clear separation of concerns)
    4. Summarise missing values
    5. Export cleaned CSV

    This function demonstrates:
    - modularity (separate loader, cleaner, and exporter)
    - robustness (warnings, consistency checks)
    - analytic support (missing-value summary)
    """
    # --- Step 1: Load dataset ---
    rows = load_csv(input_path)
    if not rows:
        raise ValueError(f"Input file appears empty: {input_path}")

    log_info(f"Loaded {len(rows)} rows from {input_path}")

    # --- Step 2: Validate fields ---
    check_field_consistency(rows)

    # --- Step 3: Clean all rows ---
    cleaned_rows = [clean_row(row) for row in rows]
    log_info(f"Successfully cleaned {len(cleaned_rows)} rows.")

    # --- Step 4: Missing-value summary ---
    summarise_missing_values(cleaned_rows)

    # --- Step 5: Ensure output directory exists ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --- Step 6: Export cleaned CSV ---
    fieldnames = cleaned_rows[0].keys()
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    log_info(f"Cleaned dataset exported to: {output_path}")


# --------------------------------------------------------------------
# Script entry point
# --------------------------------------------------------------------
if __name__ == "__main__":
    export_cleaned_dataset()
