from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from src.core.module import Module

T = TypeVar("T")

_registry: dict[type, Any] = {}


class ModuleList:
    """Typed wrapper for the list of all bot modules, registered in DI."""

    def __init__(self, modules: list[Module]) -> None:
        self._modules = modules
        self._by_name: dict[str, Module] = {m.name: m for m in modules}

    def __iter__(self):  # noqa: ANN204
        return iter(self._modules)

    def __len__(self) -> int:
        return len(self._modules)

    def __getitem__(self, idx: int) -> Module:
        return self._modules[idx]

    def get(self, name: str) -> Module:
        return self._by_name[name]

    def get_or_none(self, name: str) -> Module | None:
        return self._by_name.get(name)


def register(interface: type[T], instance: T) -> None:
    """Register an instance by its type in the global DI container."""
    _registry[interface] = instance


def get(interface: type[T]) -> T:
    """Resolve an instance from the global DI container."""
    try:
        return _registry[interface]
    except KeyError:
        raise KeyError(f"Not registered: {interface.__name__}") from None
