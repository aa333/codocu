from peewee import BooleanField, CompositeKey, DateTimeField, IntegerField

from src.storage.database import BaseModel


class ChatMembership(BaseModel):
    chat_id = IntegerField()
    user_id = IntegerField()
    in_chat = BooleanField(default=True)
    registered_at = DateTimeField(null=True)
    last_message_at = DateTimeField(null=True)

    class Meta:
        primary_key = CompositeKey("chat_id", "user_id")
        table_name = "chat_memberships"
