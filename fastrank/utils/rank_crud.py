from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db
from datetime import datetime

from fastrank.models import (
    Rank
)

from fastrank.schemas.models import (
    RankUpdate,
    RankCreate,
    RankDelete,
    RankRead,
)

def rank_get_all(db: Session):
    return db.query(Rank).all()

def rank_get_one(db: Session , id : UUID):
    return db.query(Rank).filter_by(id=id).one()

def rank_update(db: Session , record : RankUpdate):
    update_query = {
        Rank.id : record.id ,
        Rank.name : record.name,
        Rank.mmr_treshold : record.mmr_treshold,
        }
    db.query(Rank).filter_by(id=record.id).update(update_query)
    db.commit()
    return db.query(Rank).filter_by(id=record.id).one()

def rank_create( db : Session , record : RankCreate):

    new_rank = Rank(
        name = record.name,
        number = record.number,
        sub_number = record.sub_number,
        mmr_treshold = record.mmr_treshold,
    )
    db.add(new_rank)
    db.commit()

    return db.query(Rank).filter_by(name = record.name , mmr_treshold = record.mmr_treshold).first()
