from __future__ import annotations

from typing import TYPE_CHECKING

from src.core import di
from src.core.config import AppConfig
from src.core.module import Module
from src.modules.captcha import strings
from src.modules.captcha.bot_connector import CaptchaBotConnector
from src.modules.captcha.service import CaptchaService
from src.modules.captcha.types import JoinOutcome
from src.modules.chats.module import ChatsModule

if TYPE_CHECKING:
    from telebot.async_telebot import AsyncTeleBot
    from telebot.types import Message, User


class CaptchaModule(Module):
    name = "captcha"
    str_name = "Captcha"
    depends_on = ("chats",)

    def __init__(self) -> None:
        self.service = CaptchaService()
        self._bot_conn: CaptchaBotConnector | None = None

    async def init(self) -> None:
        from telebot.async_telebot import AsyncTeleBot

        config = di.get(AppConfig)
        bot = di.get(AsyncTeleBot)
        chats_mod = di.get(ChatsModule)

        self._bot_conn = CaptchaBotConnector(
            self.service, chats_mod.service, config.captcha.challenge_time
        )
        self._bot_conn.register(bot)

    def has_ongoing(self, chat_id: int, user_id: int) -> bool:
        return self.service.has_ongoing(chat_id, user_id)

    async def verify_answer(self, bot: AsyncTeleBot, message: Message) -> None:
        assert self._bot_conn is not None
        await self._bot_conn.verify_answer(bot, message)

    async def handle_join(self, bot: AsyncTeleBot, message: Message, new_user: User) -> JoinOutcome:
        assert self._bot_conn is not None
        return await self._bot_conn.handle_join(bot, message, new_user)

    def help(self) -> str | None:
        return strings.HELP

    async def debug(self) -> str:
        lines = "\n".join(f"  {c}" for c in self.service.challenges)
        return f"[Captcha]\nActive challenges: {len(self.service.challenges)}\n{lines}"
