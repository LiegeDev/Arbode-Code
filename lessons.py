from typing import Optional


LESSONS = [
    {
        "id": "python_variables",
        "language": "python",
        "title": "Variables",
        "description": "Learn how to store values using variables.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 1,
        "locked": False
    },
    {
        "id": "python_print",
        "language": "python",
        "title": "Print Statements",
        "description": "Learn how to display information using print().",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 2,
        "locked": False
    },
    {
        "id": "python_datatypes",
        "language": "python",
        "title": "Data Types",
        "description": "Learn about strings, integers, floats, booleans, and more.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 3,
        "locked": False
    },
    {
        "id": "python_if",
        "language": "python",
        "title": "If Statements",
        "description": "Learn how programs make decisions using conditions.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 4,
        "locked": False
    },
    {
        "id": "python_for_loops",
        "language": "python",
        "title": "For Loops",
        "description": "Learn how to repeat code using for loops.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 5,
        "locked": False
    },
    {
        "id": "luau_variables",
        "language": "luau",
        "title": "Luau Variables",
        "description": "Learn how variables work in Luau.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 1,
        "locked": False
    },
    {
        "id": "luau_functions",
        "language": "luau",
        "title": "Luau Functions",
        "description": "Learn how to create and use functions in Luau.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 2,
        "locked": False
    },
    {
        "id": "luau_if",
        "language": "luau",
        "title": "Luau If Statements",
        "description": "Learn conditional logic in Luau.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 3,
        "locked": False
    },
    {
        "id": "luau_loops",
        "language": "luau",
        "title": "Luau Loops",
        "description": "Learn how to repeat code using Luau loops.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 4,
        "locked": False
    },
    {
        "id": "luau_tables",
        "language": "luau",
        "title": "Luau Tables",
        "description": "Learn how tables store collections of values in Luau.",
        "difficulty": "Beginner",
        "xp_reward": 100,
        "orb_reward": 50,
        "order": 5,
        "locked": False
    }
]


def get_all_lessons():
    return LESSONS


def get_lesson_by_id(lesson_id: str) -> Optional[dict]:
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson

    return None


def get_lessons_by_language(language: str):
    language = language.lower()

    return [
        lesson
        for lesson in LESSONS
        if lesson["language"] == language
    ]


def get_next_lesson(lesson_id: str) -> Optional[dict]:
    current = get_lesson_by_id(lesson_id)

    if current is None:
        return None

    language_lessons = get_lessons_by_language(
        current["language"]
    )

    for lesson in language_lessons:
        if lesson["order"] == current["order"] + 1:
            return lesson

    return None
