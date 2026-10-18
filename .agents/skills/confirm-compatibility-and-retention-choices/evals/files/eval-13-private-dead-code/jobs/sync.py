__all__ = ["run_sync"]


def _old_parse(raw):  # unused since the 2023 rewrite, no references anywhere
    return raw.split(",")


def _parse(raw):
    return [p.strip() for p in raw.split(",") if p.strip()]


def run_sync(raw):
    return _parse(raw)
