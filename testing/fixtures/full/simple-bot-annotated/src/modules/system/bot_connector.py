import socket

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message
from telebot.util import quick_markup

from src.connectors.telegram.utils import (
    CommandAllowedIn,
    is_owner,
    register_bot_callback,
    register_bot_command,
)
from src.core import strings as shared
from src.modules.system import strings
from src.modules.system.service import SystemService

hostname = socket.gethostname()


class SystemBotConnector:
    def __init__(self, service: SystemService, owner_ids: list[int]) -> None:
        self._service = service
        self._owner_ids = owner_ids

    def register(self, bot: AsyncTeleBot) -> None:
        register_bot_command(bot, self._handle_ping, ["ping"], CommandAllowedIn.DM)
        register_bot_command(bot, self._handle_debug, ["debug"], CommandAllowedIn.DM)
        register_bot_command(bot, self._handle_sleep, ["sleep", "pause"], CommandAllowedIn.DM)
        register_bot_callback(
            bot,
            handler=self._handle_cleanup_message,
            func=lambda call: call.data == "cleanup_message",
        )

    async def _handle_ping(self, message: Message, bot: AsyncTeleBot) -> None:
        if not is_owner(message, self._owner_ids):
            return
        text = self._service.get_uptime_text()
        await bot.reply_to(message, strings.PONG.format(hostname=hostname, uptime=text))

    async def _handle_debug(self, message: Message, bot: AsyncTeleBot) -> None:
        if not is_owner(message, self._owner_ids):
            return

        text = await self._service.collect_debug_info()
        await bot.reply_to(
            message,
            text,
            reply_markup=quick_markup(
                {shared.BTN_DELETE: {"callback_data": "cleanup_message"}}, row_width=1
            ),
        )

    async def _handle_sleep(self, message: Message, bot: AsyncTeleBot) -> None:
        if not is_owner(message, self._owner_ids):
            return

        args = (message.text or "").split()[1:]
        ok, err = self._service.parse_sleep_args(args)
        if not ok:
            if err:
                await bot.reply_to(message, err)
            return

        seconds = int(args[0])
        await bot.reply_to(
            message,
            f"Инстанс {hostname}, засыпаю на {seconds} секунд.",
        )
        await self._service.sleep(seconds)
        await bot.reply_to(message, f"Инстанс {hostname}, просыпаюсь.")

    async def _handle_cleanup_message(self, call: CallbackQuery, bot: AsyncTeleBot) -> None:
        if not call.message or not call.message.reply_to_message:
            return

        command_message: Message = call.message.reply_to_message  # type: ignore
        command_author_id: int = (
            command_message.from_user.id if command_message is not None else 0  # type: ignore
        )

        if call.from_user.id != command_author_id:
            await bot.answer_callback_query(callback_query_id=call.id, text=shared.random_no())
            return

        await bot.answer_callback_query(callback_query_id=call.id, text=shared.MSG_DELETED)
        message_ids = [call.message.id]
        if command_message is not None:
            message_ids.append(command_message.id)
        await bot.delete_messages(
            chat_id=call.message.chat.id,
            message_ids=message_ids,  # type: ignore
        )
