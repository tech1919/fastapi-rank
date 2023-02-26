from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db

from fastrank.models import Rank
from fastrank.schemas.models import (
    RankCreate,
    RankDelete,
    RankRead,
    RankUpdate,
)

from fastrank.utils.rank_crud import (
    rank_get_all,
    rank_get_one,
    rank_update,
    rank_create,
)

router = APIRouter(tags=["Ranks"])

@router.get("/get-all" , status_code=status.HTTP_200_OK)
async def get_all(
    db : Session = Depends(get_db),
):
    return rank_get_all(db=db)

@router.get("/get-one/{rank_id}")
async def get_one(
    rank_id : UUID,
    db : Session = Depends(get_db),
):
    return rank_get_one(db=db , id = rank_id)

@router.post(
        "/create",
        status_code=status.HTTP_200_OK,
)
async def create_one(
    record : RankCreate,
    db : Session = Depends(get_db),
):
    
    return rank_create(db = db , record = record)

@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
)
async def update_one(
    record : RankUpdate,
    db : Session = Depends(get_db),
):
    return rank_update(record=record , db=db)



