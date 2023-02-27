from typing import Optional , List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from fastrank.models import (
    RankUser
)

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
    rank_id : UUID
    user_id : UUID
    number_of_games : int
    xp : int
    mmr_percent : float
    stats_metadata : dict

class RankUserDelete(BaseModel , BaseDelete):
    pass

class RankUserRead(BaseModel):
    id : UUID



########################
# Reward               #
########################

class LevelResults(BaseModel):

    level_name : str
    battary: float = 0.13 # ["battary% / time*x"]
    distance: float = 0 # ["integral of x(t)"]
    vel: float = 0
    acc: float = 0
    power: float = 0 # [kg*m^2 / s^3]
    level_xp : int = 15 
    cur_user_mmr : float
    communication_loss : int = 0 
    yaw_diff : float
    pitch_diff : float
    roll_diff : float
    collisions : int = 0
    close_calls : int = 0
    mission_achievement_percent : float = 0.5

class RewardInfoRecive(BaseModel):

    user_id : UUID
    level_info : LevelResults

class RewardInfoFromModel(BaseModel):
    reward_mmr_percent : float
    comment : str
    data : RewardInfoRecive

class RewardInfoResponse(BaseModel):

    reward : RewardInfoFromModel
    rank : RankUserUpdate