from fastapi import APIRouter

router = APIRouter(
    prefix="/api/leaderboard",
    tags=["Leaderboard"]
)


def get_leaderboard(connection, limit: int = 100):
    rows = connection.execute(
        """
        SELECT
            id,
            username,
            level,
            xp,
            streak_days
        FROM users
        ORDER BY xp DESC, level DESC, username ASC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    leaderboard = []

    for position, row in enumerate(rows, start=1):
        leaderboard.append({
            "rank": position,
            "user_id": row["id"],
            "username": row["username"],
            "level": row["level"],
            "xp": row["xp"],
            "streak_days": row["streak_days"]
        })

    return leaderboard


def get_user_rank(connection, user_id: int):
    user = connection.execute(
        """
        SELECT id, username, level, xp, streak_days
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if user is None:
        return None

    rank = connection.execute(
        """
        SELECT COUNT(*) + 1 AS rank
        FROM users
        WHERE xp > ?
           OR (xp = ? AND level > ?)
        """,
        (
            user["xp"],
            user["xp"],
            user["level"]
        )
    ).fetchone()["rank"]

    return {
        "rank": rank,
        "user_id": user["id"],
        "username": user["username"],
        "level": user["level"],
        "xp": user["xp"],
        "streak_days": user["streak_days"]
    }
