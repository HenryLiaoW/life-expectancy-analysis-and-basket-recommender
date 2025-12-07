def clean_numeric(value: str):
    """Convert numeric strings to float. Return None for invalid or missing values."""
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (ValueError, TypeError):  #"abc"-ValueError;"[]"-TypeError
        return None

def clean_row(row: dict):
    """
    Clean a single CSV row.
    - Non-dict input is rejected with TypeError (robustness).
    - 'year' is converted to int where possible.
    - Known numeric fields are converted using clean_numeric().
    - All other fields are returned unchanged.
    """
    # ============================
    # 1. Type validation (Very important for robustness)
    # ============================
    if not isinstance(row, dict):
        raise TypeError("Row must be a dictionary")

    cleaned = {}

# Numeric fields observed in the WHO-style life expectancy dataset
    numeric_fields = {
        "life_expect",
        "life_expectancy",
        "life_exp60",
        "adult_mortality",
        "infant_mort",
        "age1-4mort",
        "alcohol",
        "bmi",
        "age5-19thinness",
        "age5-19obesity",
        "hepatitis",
        "measles",
        "polio",
        "diphtheria",
        "basic_water",
        "doctors",
        "hospitals",
        "gni_capita",
        "gghe-d",
        "che_gdp",
        "une_pop",
        "une_infant",
        "une_life",
        "une_hiv",
        "une_gni",
        "une_poverty",
        "une_edu_spend",
        "une_literacy",
        "une_school",
    }

    # ============================
    # 2. Field-by-field cleaning
    # ============================

    for key, value in row.items(): 
            #processing each key-value pair outputed by csv.DictReader

        # ---------- YEAR ----------
        if key == "year":
            try:
                cleaned[key] = int(value)
            except (ValueError, TypeError):
                cleaned[key] = None
            continue

        # ---------- NUMERIC FIELDS ----------
        if key in numeric_fields:
            cleaned[key] = clean_numeric(value)
            continue

        # ---------- DEFAULT (unchanged) ----------
        cleaned[key] = value

    return cleaned


    # ============================
    # 3. dataset-level cleaning
    # ============================

def clean_dataset(rows):
    """
    Clean a whole dataset (list of dict rows).
    Returns a new list of cleaned rows.
    """
    return [clean_row(r) for r in rows]
