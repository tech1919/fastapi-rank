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
)

router = APIRouter(tags=["Ranks Users"])


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


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
)
async def update_one(
    record : RankUserUpdate,
    db : Session = Depends(get_db),
):
    return rank_user_update(record=record , db=db)


