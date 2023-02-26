from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db
from datetime import datetime
from sqlalchemy import desc



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
    
    return db.query(Rank).order_by(desc(Rank.mmr_treshold)).all()

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


def redevide_treshold_ranks(db : Session , min_th_value : int = 10):

    all_ranks = rank_get_all(db=db)
    all_ranks.reverse()

    # all_ranks.sort(key=lambda x: x.mmr_treshold)
        
    # create a list of all the mmr_treshold in the same order of the records
    mmr_th_list = [rank.mmr_treshold for rank in all_ranks]
    
    # the difference between the maximum value and the min_th_value
    value_to_split = max(mmr_th_list) - min_th_value

    # split the diff according to the number of ranks
    value_for_each_rank = round(value_to_split / len(all_ranks))
    
    th_value = min_th_value + value_for_each_rank


    for rank in all_ranks:
        rank.mmr_treshold = th_value
        th_value += value_for_each_rank
    
    db.bulk_save_objects(all_ranks)
    db.commit()

    return

def rank_delete( db : Session , id : UUID):

    db.query(Rank).filter_by(id = id).delete()
    db.commit()

    return {"msg" : f"Record {id} deleted"}