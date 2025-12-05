def clean_numeric(value: str):
    """Convert numeric strings to float. Return None for invalid or missing values."""
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (ValueError, TypeError):  #"abc"-ValueError;"[]"-TypeError
        return None
