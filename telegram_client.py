# telegram_client.py
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, PARSE_MODE
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(
    token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
)


async def send_message(text: str):
    """Отправка сообщения в Telegram через aiogram."""
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode=ParseMode.MARKDOWN_V2
    )
