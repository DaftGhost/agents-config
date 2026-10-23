from datetime import date


def parse_date(s):
    """Parse YYYY-MM-DD into a date."""
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))
