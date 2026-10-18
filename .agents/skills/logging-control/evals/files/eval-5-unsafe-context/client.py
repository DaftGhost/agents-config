import logging

logger = logging.getLogger(__name__)


class PartnerClient:
    def __init__(self, session, base_url):
        self._session = session
        self._base_url = base_url

    def create_payment(self, payload, headers):
        try:
            response = self._session.post(
                f"{self._base_url}/payments", json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.error(
                "partner request failed headers=%s payload=%s", headers, payload
            )
            raise
