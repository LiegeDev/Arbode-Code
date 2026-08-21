from datetime import datetime, date
from fastapi import APIRouter, HTTPException

from models import UserProfile, LessonProgress, ChallengeProgress

router = APIRouter(
    prefix="/api/progress",
    tags=["Progress"]
)


def calculate_level(xp: int) -> int:
    return (xp // 100) + 1


def add_xp(user: UserProfile, amount: int) -> UserProfile:
    if amount < 0:
        raise ValueError("XP amount cannot be negative")

    user.xp += amount
    user.level = calculate_level(user.xp)

    return user


def complete_lesson(
    user: UserProfile,
    lesson: LessonProgress,
    xp_reward: int = 50
) -> UserProfile:

    if not lesson.completed:
        lesson.completed = True
        lesson.completed_at = datetime.utcnow().isoformat()

        if lesson.lesson_id not in user.completed_lessons:
            user.completed_lessons.append(lesson.lesson_id)

        add_xp(user, xp_reward)

    return user


def complete_challenge(
    user: UserProfile,
    challenge: ChallengeProgress,
    xp_reward: int = 100
) -> UserProfile:

    if not challenge.completed:
        challenge.completed = True
        challenge.completed_at = datetime.utcnow().isoformat()

        if challenge.challenge_id not in user.completed_challenges:
            user.completed_challenges.append(challenge.challenge_id)

        add_xp(user, xp_reward)

    return user


def update_streak(user: UserProfile) -> UserProfile:
    today = date.today().isoformat()

    if user.last_active_date == today:
        return user

    if user.last_active_date is None:
        user.streak_days = 1

    else:
        previous = date.fromisoformat(user.last_active_date)
        difference = (date.today() - previous).days

        if difference == 1:
            user.streak_days += 1
        else:
            user.streak_days = 1

    user.last_active_date = today

    return user
