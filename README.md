# Exolve Number Masking Demo

Демо-проект из статьи про маскировку номеров, Flash Call и маршрутизацию звонков через MTS Exolve + Bitrix24.

## Структура

- `app.py` — Streamlit-интерфейс мастера
- `auth_service.py` — Flash Call авторизация
- `bitrix_integration.py` — интеграция с Bitrix24
- `exolve_voice.py` — исходящий Callback через Exolve
- `webhook_router.py` — входящий webhook и маршрутизация звонков
- `config.py` — загрузка конфигурации из переменных окружения
- `.env.example` — пример переменных окружения

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Заполни переменные окружения по примеру `.env.example`.

### Запуск интерфейса

```bash
streamlit run app.py
```

### Запуск webhook-сервера

```bash
python webhook_router.py
```

