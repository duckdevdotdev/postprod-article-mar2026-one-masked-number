import requests
from config import Config


FINAL_STAGES = ["WON", "LOSE", "Apology"]


def get_user_id_by_phone(phone: str):
    """Ищет ID сотрудника по номеру телефона."""
    method = "user.search"
    params = {"FILTER": {"PERSONAL_MOBILE": phone}}

    resp = requests.post(f"{Config.BITRIX_WEBHOOK}/{method}", json=params, timeout=10)
    resp.raise_for_status()
    result = resp.json().get("result", [])
    return result[0]["ID"] if result else None


def get_active_deals(master_phone: str):
    """Ищет активные сделки, назначенные на мастера."""
    user_id = get_user_id_by_phone(master_phone)
    if not user_id:
        return []

    params = {
        "filter": {
            "ASSIGNED_BY_ID": user_id,
            "!STAGE_ID": FINAL_STAGES,
        },
        "select": ["ID", "TITLE", "UF_CRM_ADDRESS", "CONTACT_ID"],
    }

    resp = requests.post(f"{Config.BITRIX_WEBHOOK}/crm.deal.list", json=params, timeout=10)
    resp.raise_for_status()

    deals = []
    for item in resp.json().get("result", []):
        contact_id = item.get("CONTACT_ID")
        client_phone = _get_contact_phone(contact_id) if contact_id else None

        if client_phone:
            deals.append(
                {
                    "id": item["ID"],
                    "address": item.get("UF_CRM_ADDRESS", "Адрес не указан"),
                    "title": item["TITLE"],
                    "client_phone_hidden": client_phone,
                }
            )

    return deals


def _get_contact_phone(contact_id: str):
    """Получает телефон клиента из карточки контакта."""
    params = {"ID": contact_id}
    resp = requests.post(f"{Config.BITRIX_WEBHOOK}/crm.contact.get", json=params, timeout=10)
    resp.raise_for_status()

    phones = resp.json().get("result", {}).get("PHONE", [])
    if phones:
        return phones[0]["VALUE"]
    return None


def close_deal(deal_id: str):
    """Переводит сделку в стадию 'Успешно'."""
    params = {"id": deal_id, "fields": {"STAGE_ID": "WON"}}
    requests.post(f"{Config.BITRIX_WEBHOOK}/crm.deal.update", json=params, timeout=10)
