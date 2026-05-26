from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


class CommandAllowedIn(Enum):
    DM = "dm"
    Group = "group"
    Both = "both"


def is_group_chat(message: Message) -> bool:
    return message.chat.type in ("group", "supergroup")


def register_bot_command(
    bot: AsyncTeleBot,
    handler,
    commands: list[str],
    allowed_in: CommandAllowedIn = CommandAllowedIn.Group,
) -> None:
    group_allowed = allowed_in is CommandAllowedIn.Group

    def chat_filter(message: Message) -> bool:
        return allowed_in == CommandAllowedIn.Both or is_group_chat(message) == group_allowed

    bot.register_message_handler(handler, commands=commands, func=chat_filter, pass_bot=True)


def register_bot_callback(bot: AsyncTeleBot, handler, func) -> None:
    bot.register_callback_query_handler(handler, func=func, pass_bot=True)


def is_owner(message: Message, owner_ids: list[int]) -> bool:
    return message.from_user is not None and message.from_user.id in owner_ids
