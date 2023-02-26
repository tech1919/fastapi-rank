from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db

from fastrank.models import RankUser , Rank
from fastrank.schemas.models import (
    RankUserCreate,
    RankUserDelete,
    RankUserRead,
    RankUserUpdate,
)

from fastrank.utils.rank_user_crud import (
    rank_user_get_all,
    rank_user_get_by_id,
    rank_user_get_by_user,
    rank_user_update,
    rank_user_create,
    rank_user_delete,
    rank_user_update_rank_with_mmr_input,
)

router = APIRouter(tags=["Ranks"])

@router.get("/get-all" , status_code=status.HTTP_200_OK)
async def get_all(
    db : Session = Depends(get_db),
):
    return rank_user_get_all(db=db)

@router.get("/get-one/{id}")
async def get_one_by_id(
    rank_id : UUID,
    db : Session = Depends(get_db),
):
    return rank_user_get_by_id(db=db , id = rank_id)

@router.get(
    "/get-one/{user_id}",
)
async def get_one_by_user(
    user_id : UUID,
    db : Session = Depends(get_db),
):
    return rank_user_get_by_user(db=db , user_id = user_id)

@router.post(
        "/create",
        status_code = status.HTTP_200_OK,
)
async def create_one(
    record : RankUserCreate,
    db : Session = Depends(get_db),
):
    return rank_user_create(db = db , record = record)

@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
)
async def update_one(
    record : RankUserUpdate,
    db : Session = Depends(get_db),
):
    return rank_user_update(record=record , db=db)

@router.post(
    "/update-mmr/{user_id}/{mmr_addition}"
)
async def update_user_mmr(
    user_id : UUID,
    mmr_addition : float,
    db : Session = Depends(get_db)
):

    record = rank_user_get_by_user(db = db , user_id=user_id)

    rank_user_update_rank_with_mmr_input(db=db , record=record ,mmr_prec_addition=mmr_addition)

    db.commit()

    return rank_user_get_by_user(db = db , user_id=user_id)

@router.post(
        "/update-xp/{user_id}/{xp_addition}",
)
async def update_user_xp(
    user_id : UUID,
    xp_addition : int,
    db : Session = Depends(get_db),
):
    record = rank_user_get_by_user(db = db , user_id=user_id)
    record.xp += xp_addition
    db.commit()

    return rank_user_get_by_user(db = db , user_id=user_id)


@router.post(
        "/update-stats/{user_id}",
)
async def update_user_stats(
    user_id : UUID,
    stats : dict = None,
    db : Session = Depends(get_db),
):
    record = rank_user_get_by_user(db = db , user_id=user_id)
    if not stats == None:
        record.stats_metadata += stats
        db.commit()

    return rank_user_get_by_user(db = db , user_id=user_id)

@router.post(
        "/update-game-number/{user_id}"
)
async def update_user_game_number(
    user_id : UUID,
    game_number : int = None,
    db : Session = Depends(get_db),
):
    record = rank_user_get_by_user(db = db , user_id=user_id)

    if game_number == None:
        record.number_of_games += 1
    else:
        record.number_of_games = game_number

    db.commit()

    return rank_user_get_by_user(db = db , user_id=user_id)


@router.post(
        "/update-all-info/{user_id}/{mmr_addition}/{xp_addition}"
)
async def update_all_game_info(
    user_id : UUID,
    mmr_addition : float,
    xp_addition : int,
    game_number : int = None,
    stats : dict = None,
    db : Session = Depends(get_db),
):
    
    record = rank_user_get_by_user(db = db , user_id=user_id)

    # XP
    record.xp += xp_addition
    
    # NUMBER OF GAMES
    if game_number == None:
        record.number_of_games += 1
    else:
        record.number_of_games = game_number
    
    # METADATA STATS
    if not stats == None:
        record.stats_metadata += stats
    
    # MMR
    rank_user_update_rank_with_mmr_input(db=db , record=record ,mmr_prec_addition=mmr_addition)
    
    db.commit()

    return rank_user_get_by_user(db = db , user_id=user_id)



@router.delete(
    "/delete/{id}", 
)
async def delete_one(
    id : UUID,
    db : Session = Depends(get_db)
):
    return rank_user_delete(db=db , id=id)
