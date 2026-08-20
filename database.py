import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "arbode.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            level INTEGER NOT NULL DEFAULT 1,
            xp INTEGER NOT NULL DEFAULT 0,
            streak_days INTEGER NOT NULL DEFAULT 0,
            orbs INTEGER NOT NULL DEFAULT 0,
            gems INTEGER NOT NULL DEFAULT 0,
            ads_watched INTEGER NOT NULL DEFAULT 0,
            max_ads_per_day INTEGER NOT NULL DEFAULT 5,
            last_active_date TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            lesson_id TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            score INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            UNIQUE(user_id, lesson_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS challenge_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            score INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            UNIQUE(user_id, challenge_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def create_user(username: str):
    from datetime import datetime, timezone

    connection = get_connection()

    created_at = datetime.now(timezone.utc).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO users (
            username,
            created_at
        )
        VALUES (?, ?)
        """,
        (username, created_at)
    )

    connection.commit()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()

    return user


def get_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    connection = get_connection()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    connection = get_connection()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    return user


def update_user(
    user_id: int,
    xp: Optional[int] = None,
    level: Optional[int] = None,
    streak_days: Optional[int] = None,
    orbs: Optional[int] = None,
    gems: Optional[int] = None
):
    connection = get_connection()

    current = connection.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if current is None:
        connection.close()
        return None

    new_xp = current["xp"] if xp is None else max(0, xp)
    new_level = current["level"] if level is None else max(1, level)
    new_streak = (
        current["streak_days"]
        if streak_days is None
        else max(0, streak_days)
    )
    new_orbs = current["orbs"] if orbs is None else max(0, orbs)
    new_gems = current["gems"] if gems is None else max(0, gems)

    connection.execute(
        """
        UPDATE users
        SET xp = ?,
            level = ?,
            streak_days = ?,
            orbs = ?,
            gems = ?
        WHERE id = ?
        """,
        (
            new_xp,
            new_level,
            new_streak,
            new_orbs,
            new_gems,
            user_id
        )
    )

    connection.commit()

    updated_user = connection.execute(
        """
        SELECT * FROM users
        WHERE id =?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return updated_user
