import uuid

from pydantic import BaseModel


class UserSerializer(BaseModel):
    id: uuid.UUID
    name: str
    username: str

    class ConfigDict:
        from_attributes = True
