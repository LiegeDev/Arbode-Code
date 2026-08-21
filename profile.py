from fastapi import APIRouter

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)


def get_profile(connection, user_id: int):
    user = connection.execute(
        """
        SELECT
            id,
            username,
            level,
            xp,
            streak_days,
            orbs,
            gems,
            ads_watched,
            max_ads_per_day,
            last_active_date,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if user is None:
        return None

    completed_lessons = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM lesson_progress
        WHERE user_id = ?
        AND completed = 1
        """,
        (user_id,)
    ).fetchone()["count"]

    completed_challenges = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM challenge_progress
        WHERE user_id = ?
        AND completed = 1
        """,
        (user_id,)
    ).fetchone()["count"]

    return {
        "id": user["id"],
        "username": user["username"],
        "level": user["level"],
        "xp": user["xp"],
        "streak_days": user["streak_days"],
        "orbs": user["orbs"],
        "gems": user["gems"],
        "ads_watched": user["ads_watched"],
        "max_ads_per_day": user["max_ads_per_day"],
        "last_active_date": user["last_active_date"],
        "created_at": user["created_at"],
        "completed_lessons": completed_lessons,
        "completed_challenges": completed_challenges
    }
