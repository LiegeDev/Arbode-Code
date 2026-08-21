from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/progress",
    tags=["Progress"]
)


class ProgressUpdate(BaseModel):
    user_id: int
    xp: int = 0
    lesson_id: int | None = None
    challenge_id: int | None = None


class ProgressResponse(BaseModel):
    user_id: int
    xp: int
    level: int
    lessons_completed: int
    challenges_completed: int
    streak_days: int


progress_store: dict[int, ProgressResponse] = {}


@router.get("/{user_id}", response_model=ProgressResponse)
def get_progress(user_id: int):
    if user_id not in progress_store:
        progress_store[user_id] = ProgressResponse(
            user_id=user_id,
            xp=0,
            level=1,
            lessons_completed=0,
            challenges_completed=0,
            streak_days=0
        )

    return progress_store[user_id]


@router.post("/{user_id}/xp", response_model=ProgressResponse)
def add_xp(user_id: int, amount: int):
    if amount < 0:
        raise HTTPException(
            status_code=400,
            detail="XP amount cannot be negative"
        )

    progress = get_progress(user_id)

    progress.xp += amount
    progress.level = (progress.xp // 100) + 1

    progress_store[user_id] = progress

    return progress


@router.post("/{user_id}/lesson", response_model=ProgressResponse)
def complete_lesson(user_id: int):
    progress = get_progress(user_id)

    progress.lessons_completed += 1
    progress.xp += 50
    progress.level = (progress.xp // 100) + 1

    progress_store[user_id] = progress

    return progress


@router.post("/{user_id}/challenge", response_model=ProgressResponse)
def complete_challenge(user_id: int, xp_reward: int = 100):
    if xp_reward < 0:
        raise HTTPException(
            status_code=400,
            detail="XP reward cannot be negative"
        )

    progress = get_progress(user_id)

    progress.challenges_completed += 1
    progress.xp += xp_reward
    progress.level = (progress.xp // 100) + 1

    progress_store[user_id] = progress

    return progressvvv
