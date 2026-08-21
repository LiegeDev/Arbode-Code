from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Challenge:
    id: str
    title: str
    description: str
    language: str
    difficulty: str
    xp_reward: int
    orb_reward: int
    starter_code: str = ""
    expected_output: Optional[str] = None


CHALLENGES: List[Challenge] = [
    Challenge(
        id="python-hello-world",
        title="Hello, World!",
        description="Write a Python program that prints Hello, World!",
        language="python",
        difficulty="beginner",
        xp_reward=50,
        orb_reward=10,
        starter_code="",
        expected_output="Hello, World!"
    ),

    Challenge(
        id="python-add-numbers",
        title="Add Two Numbers",
        description="Create a program that adds two numbers together.",
        language="python",
        difficulty="beginner",
        xp_reward=75,
        orb_reward=15,
        starter_code=(
            "a = 5\n"
            "b = 10\n\n"
            "# Write your code below"
        ),
        expected_output="15"
    ),

    Challenge(
        id="luau-hello-world",
        title="Hello, World!",
        description="Write a Luau program that prints Hello, World!",
        language="luau",
        difficulty="beginner",
        xp_reward=50,
        orb_reward=10,
        starter_code="-- Write your code below",
        expected_output="Hello, World!"
    )
]


def get_all_challenges():
    return [
        {
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "language": challenge.language,
            "difficulty": challenge.difficulty,
            "xp_reward": challenge.xp_reward,
            "orb_reward": challenge.orb_reward,
            "starter_code": challenge.starter_code
        }
        for challenge in CHALLENGES
    ]


def get_challenge_by_id(challenge_id: str):
    for challenge in CHALLENGES:
        if challenge.id == challenge_id:
            return {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "language": challenge.language,
                "difficulty": challenge.difficulty,
                "xp_reward": challenge.xp_reward,
                "orb_reward": challenge.orb_reward,
                "starter_code": challenge.starter_code,
                "expected_output": challenge.expected_output
            }

    return None


def get_challenges_by_language(language: str):
    language = language.lower()

    return [
        {
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "language": challenge.language,
            "difficulty": challenge.difficulty,
            "xp_reward": challenge.xp_reward,
            "orb_reward": challenge.orb_reward,
            "starter_code": challenge.starter_code
        }
        for challenge in CHALLENGES
        if challenge.language.lower() == language
    ]
