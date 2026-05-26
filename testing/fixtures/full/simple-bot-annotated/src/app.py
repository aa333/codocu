import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.connectors.telegram.bot import create_bot
from src.connectors.telegram.utils import is_group_chat
from src.core import di
from src.core.config import AppConfig, load_config
from src.core.di import ModuleList
from src.core.module import Module
from src.modules.captcha.module import CaptchaModule
from src.modules.chats.module import ChatsModule
from src.modules.help.module import HelpModule
from src.modules.system.module import SystemModule
from src.storage.database import db, init_db

MODULE_CLASSES: list[type[Module]] = [
    ChatsModule,
    CaptchaModule,
    HelpModule,
    SystemModule,
]


async def main() -> None:
    config = load_config()

    init_db(config.db.path)
    bot = create_bot(config.tg_token, config.proxy)

    di.register(AppConfig, config)
    di.register(AsyncTeleBot, bot)

    modules = [cls() for cls in MODULE_CLASSES]
    for m in modules:
        di.register(type(m), m)

    di.register(ModuleList, ModuleList(modules))

    all_models = [model for m in modules for model in m.models]
    db.create_tables(all_models)

    for m in modules:
        await m.init()

    captcha = di.get(CaptchaModule)
    chats_svc = di.get(ChatsModule).service

    async def handle_message(message: Message, bot: AsyncTeleBot) -> None:
        if not is_group_chat(message):
            return
        # Captcha intercept: if user has an active challenge, only process their answer
        if message.from_user and captcha.has_ongoing(message.chat.id, message.from_user.id):
            await captcha.verify_answer(bot, message)
            return
        if message.from_user is not None:
            chats_svc.touch(message)

    async def handle_new_member(message: Message, bot: AsyncTeleBot) -> None:
        if message.new_chat_members is None:
            return
        new_user = message.new_chat_members[0]
        await captcha.handle_join(bot, message, new_user)

    # pass_bot=True changes the callback signature at runtime but is not modelled in pytelegrambotapi stubs
    bot.register_message_handler(
        handle_message,  # pyright: ignore[reportArgumentType]
        content_types=[
            "text",
            "photo",
            "video",
            "document",
            "sticker",
            "voice",
            "audio",
        ],
        pass_bot=True,
    )
    bot.register_message_handler(
        handle_new_member,  # pyright: ignore[reportArgumentType]
        content_types=["new_chat_members"],
        pass_bot=True,
    )

    for chat_id in config.debug_chats:
        try:
            await bot.send_message(chat_id, "simplebot started")
        except Exception:
            pass

    await bot.infinity_polling(timeout=30, request_timeout=35)


if __name__ == "__main__":
    asyncio.run(main())
