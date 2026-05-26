from src.core import di
from src.core.di import ModuleList
from src.core.module import Module


class HelpService:
    def get_available_modules(self, is_owner: bool = False) -> list[Module]:
        modules = di.get(ModuleList)
        return [m for m in modules if m.help() is not None and (is_owner or not m.is_system)]

    def is_accessible(self, module_name: str, is_owner: bool) -> bool:
        m = di.get(ModuleList).get_or_none(module_name)
        return m is not None and m.help() is not None and (is_owner or not m.is_system)

    def get_module_help(self, module_name: str) -> str | None:
        m = di.get(ModuleList).get_or_none(module_name)
        return m.help() if m is not None else None
