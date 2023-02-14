import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String , ForeignKey , Integer , JSON , Boolean , DateTime
from sqlalchemy.dialects.postgresql import UUID

from typing import AsyncGenerator
from datetime import datetime
from .db_connection import Base, engine


class Rank(Base):

    __tablename__ = "ranks"

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    name = Column(String(100) , nullable=False)
    mmr_treshold = Column(Integer , nullable=False)





# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
