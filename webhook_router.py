from flask import Flask, request, jsonify
import requests
from config import Config


app = Flask(__name__)
FINAL_STAGES = ["WON", "LOSE", "Apology"]


@app.route("/exolve/incoming", methods=["POST"])
def handle_call():
    data = request.json or {}
    caller_phone = data.get("numbers", {}).get("a")

    master_phone = find_master_phone_by_client(caller_phone)

    if master_phone:
        print(f"🔀 Маршрутизация: Клиент {caller_phone} -> Мастер {master_phone}")
        return jsonify(
            {
                "action": "forward",
                "destination": master_phone,
                "record": True,
            }
        )

    print(f"⛔ Нет активных заказов для {caller_phone}. В поддержку.")
    return jsonify(
        {
            "action": "forward",
            "destination": Config.SUPPORT_NUMBER,
        }
    )


def find_master_phone_by_client(client_phone: str):
    """
    Ищет телефон мастера, который ведет активную сделку клиента.
    Цепочка: Телефон -> Контакт -> Сделка -> Ответственный -> Телефон ответственного
    """
    params = {
        "type": "PHONE",
        "values": [client_phone],
        "entity_type": "CONTACT",
    }
    resp = requests.post(
        f"{Config.BITRIX_WEBHOOK}/crm.duplicate.findbycomm",
        json=params,
        timeout=10,
    )
    resp.raise_for_status()
    contacts = resp.json().get("result", {})

    if not contacts:
        return None

    contact_id = contacts[0]

    deal_params = {
        "filter": {
            "CONTACT_ID": contact_id,
            "!STAGE_ID": FINAL_STAGES,
        },
        "select": ["ASSIGNED_BY_ID"],
    }
    deal_resp = requests.post(
        f"{Config.BITRIX_WEBHOOK}/crm.deal.list",
        json=deal_params,
        timeout=10,
    )
    deal_resp.raise_for_status()
    deals = deal_resp.json().get("result", [])

    if not deals:
        return None

    assigned_id = deals[0]["ASSIGNED_BY_ID"]
    user_resp = requests.post(
        f"{Config.BITRIX_WEBHOOK}/user.get",
        json={"ID": assigned_id},
        timeout=10,
    )
    user_resp.raise_for_status()

    users = user_resp.json().get("result", [])
    if users:
        return users[0].get("PERSONAL_MOBILE")

    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
