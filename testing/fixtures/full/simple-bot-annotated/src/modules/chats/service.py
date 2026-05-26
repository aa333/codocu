from datetime import datetime, timezone
from typing import cast

from telebot.types import Message

from src.modules.chats.models import ChatMembership

MESSAGES_TO_BE_KNOWN = 3


class ChatsService:
    """Per-real-chat presence tracking. Rows stay keyed by raw chat_id."""

    def __init__(self) -> None:
        self._cache: dict[tuple[int, int], ChatMembership] = {}
        self._watch: dict[tuple[int, int], int] = {}

    def load_cache(self) -> None:
        self._cache.clear()
        for row in ChatMembership.select():
            self._cache[(cast(int, row.chat_id), cast(int, row.user_id))] = row

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def is_known(self, chat_id: int, user_id: int) -> bool:
        return (chat_id, user_id) in self._cache

    def is_in_chat(self, chat_id: int, user_id: int) -> bool:
        m = self._cache.get((chat_id, user_id))
        return m is not None and bool(m.in_chat)

    def get_all(self, chat_id: int) -> list[ChatMembership]:
        return [m for k, m in self._cache.items() if k[0] == chat_id and bool(m.in_chat)]

    def get_user_chats(self, user_id: int) -> list[int]:
        return [k[0] for k in self._cache if k[1] == user_id]

    def touch(self, message: Message) -> None:
        if message.from_user is None:
            return
        chat_id = message.chat.id
        user_id = message.from_user.id
        key = (chat_id, user_id)
        now = self._now()

        existing = self._cache.get(key)
        if existing is None:
            self._watch[key] = self._watch.get(key, 0) + 1
            if self._watch[key] >= MESSAGES_TO_BE_KNOWN:
                del self._watch[key]
                row = ChatMembership.create(
                    chat_id=chat_id,
                    user_id=user_id,
                    in_chat=True,
                    registered_at=now,
                    last_message_at=now,
                )
                self._cache[key] = row
            return

        existing.last_message_at = now  # pyright: ignore[reportAttributeAccessIssue]
        was_out = not bool(existing.in_chat)
        if was_out:
            existing.in_chat = True  # pyright: ignore[reportAttributeAccessIssue]
        ChatMembership.update(last_message_at=now, in_chat=True).where(
            ChatMembership.chat_id == chat_id,
            ChatMembership.user_id == user_id,
        ).execute()

    def mark_left(self, chat_id: int, user_id: int) -> None:
        key = (chat_id, user_id)
        row = self._cache.get(key)
        if row is None:
            return
        row.in_chat = False  # pyright: ignore[reportAttributeAccessIssue]
        ChatMembership.update(in_chat=False).where(
            ChatMembership.chat_id == chat_id,
            ChatMembership.user_id == user_id,
        ).execute()
