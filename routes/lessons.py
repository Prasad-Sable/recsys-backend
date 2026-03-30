from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from database import lessons_collection
from auth import get_current_user

router = APIRouter(tags=["lessons"])


@router.get("/lessons")
async def get_lessons(
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(50),
):
    query = {}
    if topic:
        query["topic"] = topic
    if difficulty:
        query["difficulty"] = difficulty

    cursor = lessons_collection.find(query).limit(limit)
    lessons = []
    async for lesson in cursor:
        lesson["_id"] = str(lesson["_id"])
        lessons.append(lesson)
    return lessons
