from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UserProfile:
    id: int
    username: str

    level: int = 1
    xp: int = 0
    streak_days: int = 0

    orbs: int = 0
    gems: int = 0

    ads_watched: int = 0
    max_ads_per_day: int = 5

    last_active_date: Optional[str] = None

    completed_lessons: List[str] = field(default_factory=list)
    completed_challenges: List[str] = field(default_factory=list)

    inventory_desks: List[str] = field(
        default_factory=lambda: ["default_desk"]
    )

    inventory_monitors: List[str] = field(
        default_factory=lambda: ["default_monitor"]
    )

    inventory_wallpapers: List[str] = field(
        default_factory=lambda: ["default_wallpaper"]
    )

    equipped_desk: str = "default_desk"
    equipped_monitor: str = "default_monitor"
    equipped_wallpaper: str = "default_wallpaper"


@dataclass
class LessonProgress:
    user_id: int
    lesson_id: str

    completed: bool = False
    score: int = 0
    attempts: int = 0

    completed_at: Optional[str] = None


@dataclass
class ChallengeProgress:
    user_id: int
    challenge_id: str

    completed: bool = False
    score: int = 0
    attempts: int = 0

    completed_at: Optional[str] = None
