from telebot.async_telebot import AsyncTeleBot
from telebot.formatting import escape_markdown
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from src.connectors.telegram.utils import (
    CommandAllowedIn,
    is_owner,
    register_bot_callback,
    register_bot_command,
)
from src.core import strings as shared
from src.modules.help import strings
from src.modules.help.service import HelpService

# `cleanup_message` callback is registered by SystemBotConnector — help only emits the data.


class HelpBotConnector:
    def __init__(self, service: HelpService, owner_ids: list[int]) -> None:
        self._service = service
        self._owner_ids = owner_ids

    def register(self, bot: AsyncTeleBot) -> None:
        register_bot_command(bot, self._handle_help, ["help"], CommandAllowedIn.DM)
        register_bot_callback(
            bot,
            handler=self._handle_show_module,
            func=lambda call: call.data and call.data.startswith("helpshow:"),
        )
        register_bot_callback(
            bot,
            handler=self._handle_noop,
            func=lambda call: call.data == "noop",
        )

    def _build_keyboard(self, current_module: str | None, owner: bool) -> InlineKeyboardMarkup:
        modules = self._service.get_available_modules(is_owner=owner)
        kb = InlineKeyboardMarkup(row_width=3)
        buttons = [
            InlineKeyboardButton(
                m.str_name,
                callback_data=("noop" if m.name == current_module else f"helpshow:{m.name}"),
            )
            for m in modules
        ]
        for i in range(0, len(buttons), 3):
            kb.row(*buttons[i : i + 3])
        kb.row(InlineKeyboardButton(shared.BTN_DELETE, callback_data="cleanup_message"))
        return kb

    async def _handle_help(self, message: Message, bot: AsyncTeleBot) -> None:
        caller_is_owner = is_owner(message, self._owner_ids)
        markup = self._build_keyboard(current_module=None, owner=caller_is_owner)
        await bot.reply_to(
            message,
            strings.DEFAULT_HELP_TEXT,
            parse_mode="MarkdownV2",
            reply_markup=markup,
        )

    async def _handle_show_module(self, call: CallbackQuery, bot: AsyncTeleBot) -> None:
        if not call.data or not call.message or not call.message.reply_to_message:
            return
        command_message: Message = call.message.reply_to_message  # type: ignore
        command_author_id = (
            command_message.from_user.id if command_message is not None else 0  # type: ignore
        )
        if call.from_user.id != command_author_id:
            await bot.answer_callback_query(callback_query_id=call.id, text=shared.random_no())
            return

        try:
            _, module_name = call.data.split(":")
        except Exception:
            return

        caller_is_owner = call.from_user.id in self._owner_ids
        if not self._service.is_accessible(module_name, is_owner=caller_is_owner):
            text = strings.ACCESS_DENIED
        else:
            raw_help = self._service.get_module_help(module_name)
            text = escape_markdown(raw_help) if raw_help else strings.NO_HELP

        markup = self._build_keyboard(current_module=module_name, owner=caller_is_owner)
        await bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.id,
            parse_mode="MarkdownV2",
            reply_markup=markup,
        )
        await bot.answer_callback_query(call.id)

    async def _handle_noop(self, call: CallbackQuery, bot: AsyncTeleBot) -> None:
        await bot.answer_callback_query(call.id)
