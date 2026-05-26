from telebot import asyncio_helper
from telebot.async_telebot import AsyncTeleBot


def create_bot(token: str, proxy: str | None = None) -> AsyncTeleBot:
    if proxy:
        asyncio_helper.proxy = proxy
    return AsyncTeleBot(token)
