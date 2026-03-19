import requests
from config import Config


def initiate_masked_call(master_phone: str, client_phone: str):
    url = "https://api.exolve.ru/voice/v1/Callback"
    headers = {"Authorization": f"Bearer {Config.EXOLVE_API_KEY}"}

    payload = {
        "number": Config.SINGLE_SERVICE_NUMBER,
        "destination": master_phone,
        "peer": client_phone,
        "record": True,
    }

    try:
        requests.post(url, headers=headers, json=payload, timeout=5)
    except Exception as e:
        print(f"Callback error: {e}")
