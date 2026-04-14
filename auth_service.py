import random
import requests
from config import Config


def send_auth_sms(target_phone: str):
    """
    Генерирует одноразовый код и отправляет его по SMS.
    Возвращает сам код для дальнейшей проверки в Streamlit.
    """
    code = str(random.randint(1000, 9999))

    url = "https://api.exolve.ru/messaging/v1/SendSMS"
    headers = {"Authorization": f"Bearer {Config.EXOLVE_API_KEY}"}

    payload = {
        "number": Config.SMS_SENDER,
        "destination": target_phone,
        "text": f"Код входа: {code}",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=5)
        resp.raise_for_status()
        return code
    except Exception as e:
        print(f"Ошибка отправки SMS: {e}")
        return None
