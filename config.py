import os


class Config:
    EXOLVE_API_KEY = os.getenv("EXOLVE_API_KEY", "")
    SMS_SENDER = os.getenv("SMS_SENDER", "")
    SINGLE_SERVICE_NUMBER = os.getenv("SINGLE_SERVICE_NUMBER", "")
    SUPPORT_NUMBER = os.getenv("SUPPORT_NUMBER", "")
    BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK", "")
