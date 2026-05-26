from src.core import di
from src.core.config import AppConfig
from src.core.di import ModuleList
from src.core.module import Module
from src.modules.help import strings
from src.modules.help.bot_connector import HelpBotConnector
from src.modules.help.service import HelpService


class HelpModule(Module):
    name = "help"
    str_name = "Help"

    async def init(self) -> None:
        from telebot.async_telebot import AsyncTeleBot

        config = di.get(AppConfig)
        bot = di.get(AsyncTeleBot)

        service = HelpService()
        HelpBotConnector(service, config.owner_ids).register(bot)

    def help(self) -> str:
        return strings.HELP

    async def debug(self) -> str:
        count = len(di.get(ModuleList))
        return f"[Help]\n• Modules: {count}"
