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
    
    """
    This route retrive a all the rank-user records by the id of the rank.
    """
    return rank_user_get_by_id(db=db , id = rank_id)

@router.get(
    "/get-one/{user_id}",
)
async def get_one_by_user(
    user_id : UUID,
    db : Session = Depends(get_db),
):
    """
    This route retrive a specific rank-user record by the id of the **user**.
    """
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
    
    """
    This route lets you update a rank-user record.
    """
    return rank_user_update(record=record , db=db)

@router.post(
    "/update-mmr/{user_id}/{mmr_addition}"
)
async def update_user_mmr(
    user_id : UUID,
    mmr_addition : float,
    db : Session = Depends(get_db)
):
    
    """
    This route lets you update a user's mmr and rank by sending the `mmr_addition`.
    * `mmr_addition` - the reward send from the reward model. a float number between 0-1
    that represent the progression percentage of the user in his rank.

    When a user pass the value 1 with his mmr_percent, he will be promoted to the next available rank.
    Same as if a user is pass the 0 value (to negative values), he will be demoted a rank.
    """
    
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
    
    """
    This route allow adding xp level to a rank-user record. The XP value of a user is 
    a positive integer that can only increase with every game.
    """
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
    
    """
    This route allow adding a game to the number of games played by a user.

    * Calling this route with only `user_id` - increase the value of games played by 1.
    * Calling this route with only `user_id` and `game_number`- change the value of games played to `game_number`.

    """
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
    
    """
    This route allow apply multiple changes to a rank-user record at once.
    * Change mmr_percent of a user
    * Update XP level of a user
    * Update stats
    * Update number of games played
    """
    
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
    """
    This route will delete a rank-user record for a given id
    """
    return rank_user_delete(db=db , id=id)
