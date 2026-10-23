_ZIPS = {"94107": "San Francisco", "10001": "New York"}


def lookup_city(zip_code: str) -> str | None:
    return _ZIPS.get(zip_code)
