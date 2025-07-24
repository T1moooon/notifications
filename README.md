# Telegram Notifier Bot

**Автоматический бот**, который отслеживает проверки на платформе Devman и отправляет уведомления в Telegram.


## Установка и запуск

1. **Создайте виртуальное окружение и установите зависимости**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install requirements.txt
    ```

2. **Создайте файл `.env`** рядом с `main.py`:
    ```env
    API_TOKEN=<ваш_API_TOKEN>
    TG_BOT_TOKEN=<ваш_Telegram_Bot_Token>
    TG_CHAT_ID=<ваш_chat_id>
    ```

3. **Запуск**:
    ```bash
    python main.py
    ```

##  Пример запуска

```bash
python main.py