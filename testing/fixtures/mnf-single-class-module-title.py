"""
If you need to control a new capability specific to a module:
- Add it to caps for enumeration and constant safety
- Assign caps in one of the CapProvider implementations

System doc: docs/systems/access.md
"""


class AccessService:
    """Access capability resolution service. Holds the registered CapProvider
    list and answers 'does this user have cap X?' by querying every provider.

    Removing caps currently is not supported."""

    def __init__(self) -> None:
        self._providers: list = []
