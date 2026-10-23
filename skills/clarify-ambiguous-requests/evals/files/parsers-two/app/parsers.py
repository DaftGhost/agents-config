import json
from datetime import date


def parse_data(raw):
    """Parse a JSON payload into a dict."""
    return json.loads(raw)


def parse_date(s):
    """Parse YYYY-MM-DD into a date."""
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))
