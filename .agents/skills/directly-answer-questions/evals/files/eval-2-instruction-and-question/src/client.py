from .retry import attempt_limit


def fetch(url: str) -> bytes:
    attempts = 0
    while attempts < attempt_limit():
        attempts += 1
        try:
            return _request(url)
        except TimeoutError:
            continue
    raise TimeoutError(url)


def _request(url: str) -> bytes:
    raise NotImplementedError
