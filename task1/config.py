"""Shared paths and defaults for Task 1."""

from pathlib import Path

TASK1_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TASK1_DIR.parent
DATA_DIR = TASK1_DIR / "data"
OUTPUT_DIR = TASK1_DIR / "output"

RAW_LIFE_EXPECTANCY_CSV = DATA_DIR / "life_expectancy.csv"
CLEANED_LIFE_EXPECTANCY_CSV = DATA_DIR / "life_expectancy_cleaned.csv"
FULL_DATABASE = DATA_DIR / "life_expectancy.db"
DEMO_DATABASE = DATA_DIR / "CLI_demo.db"
TEST_DATABASE = DATA_DIR / "test_life_expectancy.db"

DEFAULT_VACCINATION_THRESHOLD = 90.0
DEFAULT_POLICY_TARGET_LIFE_EXPECTANCY = 75.0
