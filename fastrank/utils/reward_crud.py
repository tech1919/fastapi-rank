import time
from fastrank.schemas.models import (
    RewardInfoRecive,
    RewardInfoResponse,
    LevelResults,
    RewardInfoFromModel,
    RankUserUpdate
)




async def calculate_reward( data : RewardInfoRecive , **kwargs) -> RewardInfoFromModel:


    # later will be inserted a call to the NN model here
    reward_from_model = RewardInfoFromModel(
        reward_mmr_percent = 0.5,
        comment = "NN reward model",
        data = data
    )

    # time.sleep(5)

    return reward_from_model