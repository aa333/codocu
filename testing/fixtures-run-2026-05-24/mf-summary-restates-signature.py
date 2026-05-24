"""
Bot module base class. Modules inherit from this and register with the DI container.

System doc: docs/systems/modules.md
"""

from abc import ABC, abstractmethod


class BotModule(ABC):
    """Base class for bot modules. Holds lifecycle hooks and module identity."""

    @abstractmethod
    def help(self) -> str | None:
        """Return help text for this module, or None."""

    async def init(self) -> None:
        """Called after ALL modules are registered in DI.
        Override to resolve cross-module dependencies via di.get(), load caches,
        create internal service/connectors, and register handlers."""
