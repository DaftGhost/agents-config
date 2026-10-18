"""Token validation and refresh helpers.

Refactored in this session: expiry comparison and refresh issuance were moved
out of the request handlers into these helpers.
"""

from datetime import datetime, timedelta


def is_expired(payload: dict, at: datetime | None = None) -> bool:
    at = at or datetime.utcnow()
    return payload["exp"] < at.timestamp()


def issue_refresh(original: dict, at: datetime | None = None) -> dict:
    at = at or datetime.utcnow()
    return {
        **original,
        "exp": (at + timedelta(hours=1)).timestamp(),
        "iat": at.timestamp(),
    }
