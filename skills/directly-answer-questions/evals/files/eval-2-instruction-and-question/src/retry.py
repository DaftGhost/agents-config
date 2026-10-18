MAX_RETRIES = 5  # changed from 3 in this session


def attempt_limit() -> int:
    return MAX_RETRIES
