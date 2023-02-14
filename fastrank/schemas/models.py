from typing import Optional , List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session


class BaseDelete:
    id : UUID
    message : str

########################
# Ranks                #
########################


class RankCreate(BaseModel): 
    name : str
    mmr_treshold : int

class RankUpdate(BaseModel):
    id : UUID
    name : str 
    mmr_treshold : int

class RankDelete(BaseModel , BaseDelete):
    pass

class RankRead(BaseModel):
    id : UUID
