from sqlalchemy import Column, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import relationship

from db.config import Base


class Message(Base):
    id = Column(Uuid, primary_key=True)
    content = Column(String, nullable=False)
    sender_id = Column(Uuid, ForeignKey("user.id"))
    receiver_id = Column(Uuid, ForeignKey("user.id"))
    forwarded_to_id = Column(Uuid, ForeignKey("user.id"))
    reply_id = Column(Uuid, ForeignKey("message.id"))

    __tablename__ = "message"
