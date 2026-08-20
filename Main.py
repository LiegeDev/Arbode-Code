from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapimiddlewarecors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "arbode.db"

app = FastAPI(
    title="Arbode Code API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
            completed_at TEXT,
            UNIQUE(user_id, lesson_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)


class UserResponse(BaseModel):
    id: int
    username: str
    level: int
    xp: int
    streak_days: int
    orbs: int
    gems: int
    ads_watched: int
    max_ads_per_day: int
    last_active_date: str | None


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
async def root():
    return {
        "name": "Arbode Code",
        "status": "online",
        "version": "0.1.0"
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/api/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    username = user.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty."
        )

    connection = get_connection()

    try:
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

        user_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        return dict(row)

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    finally:
        connection.close()


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return dict(row)


@app.patch("/api/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    xp: int | None = None,
    level: int | None = None,
    streak_days: int | None = None
):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if row is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    current_xp = row["xp"] if xp is None else max(0, xp)
    current_level = row["level"] if level is None else max(1, level)
    current_streak = (
        row["streak_days"]
        if streak_days is None
        else max(0, streak_days)
    )

    connection.execute(
        """
        UPDATE users
        SET xp = ?,
            level = ?,
            streak_days = ?
        WHERE id = ?
        """,
        (
            current_xp,
            current_level,
            current_streak,
            user_id
        )
    )

    connection.commit()

    updated = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    return dict(updated)


@app.post("/api/users/{user_id}/lessons/{lesson_id}/complete")
async def complete_lesson(
    user_id: int,
    lesson_id: str
):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    existing = connection.execute(
        """
        SELECT * FROM lesson_progress
        WHERE user_id = ? AND lesson_id = ?
        """,
        (user_id, lesson_id)
    ).fetchone()

    if existing and existing["completed"]:
        connection.close()

        return {
            "success": False,
            "message": "Lesson already completed."
        }

    now = datetime.now(timezone.utc).isoformat()

    if existing is None:
        connection.execute(
            """
            INSERT INTO lesson_progress (
                user_id,
                lesson_id,
                completed,
                completed_at
            )
            VALUES (?, ?, 1, ?)
            """,
            (user_id, lesson_id, now)
        )
    else:
        connection.execute(
            """
            UPDATE lesson_progress
            SET completed = 1,
                completed_at = ?
            WHERE user_id = ? AND lesson_id = ?
            """,
            (now, user_id, lesson_id)
        )

    reward_orbs = 50
    reward_xp = 100

    new_xp = user["xp"] + reward_xp
    new_orbs = user["orbs"] + reward_orbs

    xp_per_level = 1000
    new_level = max(
        1,
        (new_xp // xp_per_level) + 1
    )

    connection.execute(
        """
        UPDATE users
        SET xp = ?,
            level = ?,
            orbs = ?
        WHERE id = ?
        """,
        (
            new_xp,
            new_level,
            new_orbs,
            user_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "lesson_id": lesson_id,
        "rewards": {
            "xp": reward_xp,
            "orbs": reward_orbs
        },
        "new_xp": new_xp,
        "new_level": new_level,
        "new_orbs": new_orbs
    }
    }
