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



########################
# Ranks Users          #
########################


class RankUserCreate(BaseModel): 
    rank_id : int
    user_id : UUID
    number_of_games : int
    xp : int
    stats_metadata : dict

class RankUserUpdate(BaseModel):
    id : UUID
    rank_id : int
    user_id : UUID
    number_of_games : int
    xp : int
    stats_metadata : dict

class RankUserDelete(BaseModel , BaseDelete):
    pass

class RankUserRead(BaseModel):
    id : UUID
