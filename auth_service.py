import requests
from config import Config


def send_flash_call(target_phone: str):
    """
    Инициирует сброс-звонок.
    Возвращает 4 последние цифры номера, с которого пойдет вызов.
    """
    auth_number = Config.AUTH_POOL_NUMBER

    url = "https://api.exolve.ru/voice/v1/MakeCall"
    headers = {"Authorization": f"Bearer {Config.EXOLVE_API_KEY}"}

    payload = {
        "number": auth_number,
        "destination": target_phone,
        "record": False,
        "time_limit": 5,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=5)
        resp.raise_for_status()
        return auth_number[-4:]
    except Exception as e:
        print(f"Ошибка Flash Call: {e}")
        return None
