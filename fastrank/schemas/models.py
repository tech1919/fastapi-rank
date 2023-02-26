from typing import Optional , List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session


class BaseDelete:
    id : UUID
    message : dict = {"msg" : "Record deleted"} 

########################
# Ranks                #
########################


class RankCreate(BaseModel): 

    name : str
    number : int
    sub_number : int
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
    rank_id : UUID
    user_id : UUID
    number_of_games : int = 0
    xp : int = 0
    stats_metadata : dict

class RankUserUpdate(BaseModel):
    id : UUID
    rank_id : int
    user_id : UUID
    number_of_games : int
    xp : int
    mmr : int
    stats_metadata : dict

class RankUserDelete(BaseModel , BaseDelete):
    pass

class RankUserRead(BaseModel):
    id : UUID
