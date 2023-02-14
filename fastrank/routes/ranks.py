from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.db_connection import get_db

from fastrank.models import Event
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
)

router = APIRouter(tags=["Ranks"])

@router.get("/get-all-ranks" , status_code=status.HTTP_200_OK)
def get_all(
    db : Session = Depends(get_db),
):
    return rank_get_all(db=db)

@router.put(
    "/update-rank",
    status_code=status.HTTP_200_OK,
)
async def update_one(
    record : RankUpdate,
    db : Session = Depends(get_db),
):
    return rank_update(record=record , db=db)