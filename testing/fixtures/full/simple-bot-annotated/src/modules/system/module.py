import socket

from src.core import di
from src.core.config import AppConfig
from src.core.module import Module
from src.modules.system import strings
from src.modules.system.bot_connector import SystemBotConnector
from src.modules.system.service import SystemService

hostname = socket.gethostname()


class SystemModule(Module):
    name = "system"
    str_name = "System"
    is_system = True

    def __init__(self) -> None:
        self._service: SystemService | None = None

    async def init(self) -> None:
        from telebot.async_telebot import AsyncTeleBot

        config = di.get(AppConfig)
        bot = di.get(AsyncTeleBot)
        self._service = SystemService(config.log_file)
        SystemBotConnector(self._service, config.owner_ids).register(bot)

    def help(self) -> str:
        return strings.HELP

    async def debug(self) -> str:
        count = self._service.module_count if self._service else 0
        uptime = self._service.get_uptime_seconds() if self._service else 0
        return f"[System]\n• Host: {hostname}\n• Modules: {count}\n• Uptime: {uptime}s"
