import requests

RATES_URL = "https://rates.example.com/latest"


def get_exchange_rate(base, quote):
    resp = requests.get(RATES_URL, params={"base": base, "quote": quote}, timeout=5)
    resp.raise_for_status()
    return resp.json()["rate"]
