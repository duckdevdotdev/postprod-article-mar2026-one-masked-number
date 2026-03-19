import os


class Config:
    EXOLVE_API_KEY = os.getenv("EXOLVE_API_KEY", "")
    AUTH_POOL_NUMBER = os.getenv("AUTH_POOL_NUMBER", "")
    SINGLE_SERVICE_NUMBER = os.getenv("SINGLE_SERVICE_NUMBER", "")
    SUPPORT_NUMBER = os.getenv("SUPPORT_NUMBER", "")
    BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK", "")
