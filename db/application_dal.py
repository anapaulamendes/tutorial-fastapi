import uuid

from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.message import Message
from db.models.user import User


class ApplicationDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, name: str, username: str):
        new_user = User(id=uuid.uuid4(), name=name, username=username)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_all_users(self) -> list[User]:
        query = await self.db_session.execute(select(User).order_by(User.name))
        return query.scalars().all()

    async def get_user(self, user_id: uuid.UUID) -> User:
        query = select(User).where(User.id == user_id)
        results = await self.db_session.execute(query)
        user = results.one_or_none()
        return user[0]

    async def get_many_users(self, user_ids: list[uuid.UUID]):
        query = select(User).where(User.id.in_(user_ids))
        results = await self.db_session.execute(query)
        users = results.all()

        return users

    async def create_message(
        self, content: str, sender_id: uuid.UUID, receiver_id: uuid.UUID
    ):
        new_message = Message(
            id=uuid.uuid4(),
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id,
        )

        self.db_session.add(new_message)
        await self.db_session.flush()

        return new_message

    async def get_all_messages(self) -> list[Message]:
        query = await self.db_session.execute(
            select(Message).order_by(Message.sender_id)
        )
        return query.scalars().all()

    async def get_message(self, message_id: uuid.UUID) -> Message:
        query = select(Message).where(Message.id == message_id)
        results = await self.db_session.execute(query)
        message = results.one_or_none()
        return message[0]

    async def update_message(
        self,
        message_id: uuid.UUID,
        forwarded_to_id: uuid.UUID | None = None,
        reply_id: uuid.UUID | None = None,
    ):
        query = update(Message).where(Message.id == message_id)
        if forwarded_to_id:
            query = query.values(forwarded_to_id=forwarded_to_id)
        if reply_id:
            query = query.values(reply_id=reply_id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)

    async def delete_message(self, message_id: uuid.UUID):
        query = delete(Message).where(Message.id == message_id)
        await self.db_session.execute(query)
