import uuid

from pydantic import BaseModel


class MessageSerializer(BaseModel):
    id: uuid.UUID
    content: str
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    forwarded_to_id: uuid.UUID | None
    reply_id: uuid.UUID | None

    class ConfigDict:
        from_attributes = True
