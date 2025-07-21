import requests
import time
import os
import argparse
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

bot = Bot(token=TG_BOT_TOKEN)
HEADERS = {'Authorization': f'Token {API_TOKEN}'}


def send_message(chat_id: int, text: str):
    bot.send_message(chat_id=chat_id, text=text)


def long_polling(chat_id: int):
    url = "https://dvmn.org/api/long_polling/"
    timestamp = None
    while True:
        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=HEADERS, params=params, timeout=60)
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
                send_message(chat_id, text)
            timestamp = checks_data.get('last_attempt_timestamp')
        else:
            timestamp = None


def main():
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

    long_polling(int(chat_id))


if __name__ == "__main__":
    main()
