from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.core import di
from src.core.module import Module
from src.modules.chats.models import ChatMembership
from src.modules.chats.service import ChatsService


class ChatsModule(Module):
    name = "chats"
    str_name = "Chats"
    models = (ChatMembership,)

    def __init__(self) -> None:
        self.service = ChatsService()

    async def init(self) -> None:
        bot = di.get(AsyncTeleBot)
        self.service.load_cache()

        async def on_left(message: Message, bot: AsyncTeleBot) -> None:
            if message.left_chat_member is None:
                return
            self.service.mark_left(message.chat.id, message.left_chat_member.id)

        bot.register_message_handler(
            on_left,  # pyright: ignore[reportArgumentType]
            content_types=["left_chat_member"],
            pass_bot=True,
        )

    def help(self) -> str | None:
        return None

    async def debug(self) -> str:
        return f"[Chats]\nTracked memberships: {len(self.service._cache)}"
