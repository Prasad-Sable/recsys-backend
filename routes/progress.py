from fastapi import APIRouter, Depends
from datetime import datetime
from database import progress_collection, sessions_collection, lessons_collection
from auth import get_current_user
from models import ProgressRecord
from bson import ObjectId

router = APIRouter(tags=["progress"])


@router.post("/progress")
async def record_progress(req: ProgressRecord, user=Depends(get_current_user)):
    user_id = str(user["_id"])
    progress_doc = {
        "user_id": user_id,
        "lesson_id": req.lesson_id,
        "score": req.score,
        "completed_at": datetime.utcnow(),
    }
    
    existing = await progress_collection.find_one({
        "user_id": user_id,
        "lesson_id": req.lesson_id,
    })
    if existing:
        await progress_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": progress_doc}
        )
    else:
        await progress_collection.insert_one(progress_doc)

    # Record session
    session_doc = {
        "user_id": user_id,
        "time_spent": req.time_spent,
        "date": datetime.utcnow(),
    }
    await sessions_collection.insert_one(session_doc)

    return {"message": "Progress recorded"}


@router.get("/continue")
async def continue_learning(user=Depends(get_current_user)):
    user_id = str(user["_id"])
    interests = user.get("interests", [])
    level = user.get("level", "Beginner")

    # Get all completed lesson IDs
    completed_cursor = progress_collection.find({"user_id": user_id})
    completed_ids = set()
    async for p in completed_cursor:
        completed_ids.add(p["lesson_id"])

    # Find lessons matching interests and level that haven't been completed
    query = {}
    if interests:
        query["topic"] = {"$in": interests}
    query["difficulty"] = level

    cursor = lessons_collection.find(query).limit(10)
    next_lesson = None
    async for lesson in cursor:
        lid = str(lesson["_id"])
        if lid not in completed_ids:
            lesson["_id"] = lid
            next_lesson = lesson
            break

    if not next_lesson:
        # Fallback: any uncompleted lesson
        all_cursor = lessons_collection.find({}).limit(50)
        async for lesson in all_cursor:
            lid = str(lesson["_id"])
            if lid not in completed_ids:
                lesson["_id"] = lid
                next_lesson = lesson
                break

    return {"lesson": next_lesson}
