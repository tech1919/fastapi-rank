import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String , ForeignKey , Integer , JSON , Boolean , DateTime , Float
from sqlalchemy.dialects.postgresql import UUID

from typing import AsyncGenerator
from datetime import datetime
from .db_connection import Base, engine


class Rank(Base):

    __tablename__ = "ranks"

    id =  Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    name = Column(String(100) , nullable=False)
    number = Column(Integer , nullable = False)
    sub_number = Column(Integer , nullable = True)
    mmr_treshold = Column(Integer , nullable=False)


class RankUser(Base):

    __tablename__ = "ranks_users"

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    rank_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    number_of_games = Column(Integer , nullable = False , default = 0)
    xp = Column(Integer , nullable = False , default = 0)
    mmr_percent = Column(Float , nullable = False , default = 0.0)
    stats_metadata = Column(JSON , nullable = True)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
