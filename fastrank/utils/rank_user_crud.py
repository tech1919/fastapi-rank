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

from fastrank.utils.rank_crud import (
    rank_get_all,
)

def rank_user_get_all( db : Session ):
    return db.query(RankUser).all()

def rank_user_get_by_user(db:Session, user_id : UUID):
    return db.query(RankUser).filter_by(user_id = user_id).one()

def rank_user_get_by_id(db:Session, record_id : UUID):
    return db.query(RankUser).filter_by(id = record_id).one()

def rank_user_update(db : Session , record : RankUserUpdate):
    
    update_query = {
        RankUser.rank_id : record.rank_id,
        RankUser.stats_metadata : record.stats_metadata,
        RankUser.number_of_games : record.number_of_games,
        RankUser.xp : record.xp,
    }

    db.query(RankUser).filter_by(user_id = record.user_id).update(update_query)
    db.commit()

    return rank_user_get_by_user(db=db, user_id=record.user_id)

def rank_user_create(db : Session , record : RankUserCreate):
    new_record = RankUser(
        rank_id = record.rank_id,
        user_id = record.user_id,
        # number_of_games = record.number_of_games,
        # xp = record.xp,
        # stats_metadata = record.stats_metadata,
    )

    db.add(new_record)
    db.commit()

    return db.query(RankUser).filter_by(user_id = record.user_id).one()

def rank_user_delete(db: Session , id : UUID):

    db.query(RankUser).filter_by(id = id).delete()
    db.commit()

    return {"msg" : f"Record {id} deleted"}

def rank_user_update_rank_with_mmr_input( db : Session , record : RankUser , mmr_prec_addition : float) -> float:

    all_ranks = rank_get_all(db=db)
    all_ranks.reverse()
    cur_rank_index = [rank.id for rank in all_ranks].index(record.rank_id)
    
    is_min_rank = False
    is_max_rank = False
    prev_rank_index = cur_rank_index - 1
    next_rank_index = cur_rank_index + 1
    
    if cur_rank_index == 0:
        prev_rank_index = cur_rank_index
        is_min_rank = True
    if cur_rank_index == len(all_ranks)-1:
        next_rank_index = cur_rank_index
        is_max_rank = True


    record.mmr_percent += mmr_prec_addition

    # upgrade rank
    if record.mmr_percent >= 1.0:
        if is_max_rank:
            mmr_rest = record.mmr_percent
        else:
            mmr_rest = record.mmr_percent - 1.0
        rank_index = next_rank_index
    # downgrade rank
    elif record.mmr_percent <= 0.0:
        if is_min_rank:
            mmr_rest = record.mmr_percent
        else:
            mmr_rest = 1.0 + record.mmr_percent
        rank_index = prev_rank_index
    else:
        mmr_rest = record.mmr_percent
        rank_index = cur_rank_index
    
    record.rank_id = all_ranks[rank_index].id
    record.mmr_percent = mmr_rest

    return record