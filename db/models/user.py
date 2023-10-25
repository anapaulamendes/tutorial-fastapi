from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship

from db.config import Base


class User(Base):
    id = Column(Uuid, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)

    __tablename__ = "user"
