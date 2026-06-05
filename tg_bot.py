import telebot
from telebot.types import Message
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
print("Путь к ключу:", os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

SHEET_NAME = "ddata base"

# Подключение к Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def save_user(user):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    username = user.username if user.username else "—"
    first_name = user.first_name if user.first_name else "—"
    last_name = user.last_name if user.last_name else "—"
    language = user.language_code if user.language_code else "—"

    sheet.append_row([
        now,
        user.id,
        username,
        first_name,
        last_name,
        language
    ])

    print(f"Сохранён пользователь {user.id}")


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    try:
        save_user(message.from_user)
    except Exception as e:
        print("Ошибка записи:", e)

    bot.send_message(
        message.chat.id,
        "Введи юз для пробива @"
    )


@bot.message_handler(func=lambda message: True)
def ignore_all(message: Message):
    pass


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling(skip_pending=True)
