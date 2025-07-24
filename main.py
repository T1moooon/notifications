import requests
import time
import os
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
            checks = response.json()

        except requests.exceptions.ReadTimeout:
            continue

        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue

        status = checks.get('status')
        if status == 'found':
            for attempt in checks.get('new_attempts', []):
                text = (
                    f"Урок: {attempt['lesson_title']}\n"
                    f"{attempt['lesson_url']}\n"
                    f"Статус: {'В работе нашлись ошибки.' if attempt['is_negative'] else 'Всё отлично!'}"
                )
                bot.send_message(chat_id=chat_id, text=text)
            timestamp = checks.get('last_attempt_timestamp')
        else:
            timestamp = None


def main():
    load_dotenv()
    api_token = os.environ['API_TOKEN']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    bot = Bot(token=tg_bot_token)

    notify_on_new_checks(api_token, bot, int(chat_id))


if __name__ == "__main__":
    main()
