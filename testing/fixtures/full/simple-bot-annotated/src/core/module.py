from abc import ABC, abstractmethod


class Module(ABC):
    """Base unit of business functionality.

    Each module is a self-contained unit that provides help/debug info
    and wires its internals during init().

    Subclass in ``src/modules/<name>/module.py``.
    """

    name: str
    str_name: str
    is_system: bool = False
    depends_on: tuple[str, ...] = ()
    models: tuple[type, ...] = ()

    async def init(self) -> None:
        """Called after ALL modules are registered in DI.

        Override to resolve cross-module deps via ``di.get()``,
        load caches, create internal service/connectors, and register handlers.
        """

    @abstractmethod
    def help(self) -> str | None:
        """Return help text for this module, or None."""

    @abstractmethod
    async def debug(self) -> str:
        """Return debug/status info string."""
