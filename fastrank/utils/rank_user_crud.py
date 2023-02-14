from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db
from datetime import datetime


from fastrank.models import (
    Rank,
    RankUser,
)

from fastrank.schemas.models import (
    RankUpdate,
    RankCreate,
    RankDelete,
    RankRead,
    RankUserCreate,
    RankUserDelete,
    RankUserRead,
    RankUserUpdate,

)

def rank_user_get_all(db:Session):
    return db.query(RankUser).all()

def rank_user_get_by_user(db:Session, user_id : UUID):
    return db.query(RankUser).filter_by(user_id = user_id).one()

def rank_user_get_by_id(db:Session, record_id : UUID):
    return db.query(RankUser).filter_by(id = record_id).one()

def rank_user_update(db : Session , record : RankUserUpdate):
    
    update_query = {
        RankUser.stats_metadata : record.stats_metadata,
        RankUser.number_of_games : record.number_of_games,
        RankUser.xp : record.xp,
    }

    db.query(RankUser).filter_by(user_id = record.user_id).update(update_query)
    db.commit()

    return rank_user_get_by_user(db=db, user_id=record.user_id)