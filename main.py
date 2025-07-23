import requests
import time
import os
import argparse
from telegram import Bot
from dotenv import load_dotenv


def notify_on_new_checks(api_token, bot, chat_id: int):
    url = "https://dvmn.org/api/long_polling/"
    headers = {'Authorization': f'Token {api_token}'}
    timestamp = None
    while True:
        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            checks_data = response.json()

        except requests.exceptions.ReadTimeout:
            print('Сервер молчит... повторяем запрос')
            continue

        except requests.exceptions.ConnectionError:
            print('Нет интернета, ждем 5 секунд...')
            time.sleep(5)
            continue

        status = checks_data.get('status')
        if status == 'found':
            for attempt in checks_data.get('new_attempts', []):
                text = (
                    f"Урок: {attempt['lesson_title']}\n"
                    f"{attempt['lesson_url']}\n"
                    f"Статус: {'В работе нашлись ошибки.' if attempt['is_negative'] else 'Всё отлично!'}"
                )
                bot.send_message(chat_id=chat_id, text=text)
            timestamp = checks_data.get('last_attempt_timestamp')
        else:
            timestamp = None


def main():
    load_dotenv()
    api_token = os.environ['API_TOKEN']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    bot = Bot(token=tg_bot_token)
    parser = argparse.ArgumentParser(description="Telegram-бот для уведомлений о проверках")
    parser.add_argument(
        "--chat-id",
        type=int,
        help="ID Telegram-чата для отправки сообщений"
    )
    args = parser.parse_args()
    chat_id = args.chat_id or os.getenv('TG_CHAT_ID')
    if chat_id is None:
        parser.error("Не указан TG_CHAT_ID (через --chat-id или .env)")

    notify_on_new_checks(api_token, bot, int(chat_id))


if __name__ == "__main__":
    main()
