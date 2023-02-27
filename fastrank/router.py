from fastapi import APIRouter , Depends

from fastrank.routes import (
    ranks,
    ranks_users,
    rewards,
)

rank_router = APIRouter()

rank_router.include_router( router = ranks.router , prefix="/ranks")
rank_router.include_router( router = ranks_users.router , prefix="/ranks-users")
rank_router.include_router( router = rewards.router , prefix = "/reward")