from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastrank.routes import ranks_users
from fastrank.db_connection import get_db
from fastrank.utils.reward_crud import (
    calculate_reward,
)
from fastrank.utils.rank_user_crud import (
    rank_user_update_rank_with_mmr_input,
    rank_user_get_by_user,

)
from fastrank.schemas.models import (
    RewardInfoRecive,
    RewardInfoResponse,
    LevelResults,
    RankUserUpdate,
)


router = APIRouter(tags = ["Reward"])

@router.post(
    "/pass-to-reward-model",
    # response_model=RewardInfoResponse,
)
async def pass_info_to_reward_model(
    data : RewardInfoRecive,
    db : Session = Depends(get_db)
):

    """
    This route let the client send data in a form of KVP object
    to a reward model for reward calculation. The data could be any
    type of data that match the reward it was sent to.

    This route await for a response from the model and then perform 
    the rank claculation according to the reward sent back
    """
    # get reward from model based on level results
    reward_from_model = await calculate_reward(data = data)

    # update user's rank based on that reward
    rank_record = rank_user_update_rank_with_mmr_input(
        db = db,
        record = rank_user_get_by_user(db = db , user_id=reward_from_model.data.user_id),
        mmr_prec_addition= reward_from_model.reward_mmr_percent
    )

    print(rank_record.mmr_percent)

    db.commit()

    return RewardInfoResponse(
            reward = reward_from_model,
            rank = RankUserUpdate(
                id = rank_record.id,
                rank_id = rank_record.rank_id,
                user_id = rank_record.user_id,
                number_of_games = rank_record.number_of_games,
                xp = rank_record.xp,
                mmr_percent = rank_record.mmr_percent,
                stats_metadata = rank_record.stats_metadata if not rank_record.stats_metadata == None else {},
            ),
        )
    

    

