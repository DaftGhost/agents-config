MAX_RETRIES = 5


def run(fn):
    for attempt in range(MAX_RETRIES):
        try:
            return fn()
        except TimeoutError:
            continue
    raise TimeoutError("retries exhausted")
