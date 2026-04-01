from fastapi import APIRouter, Depends
from database import progress_collection, sessions_collection, lessons_collection, users_collection
from auth import get_current_user
from bson import ObjectId
from routes.gamification import get_badges, get_quests

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
async def get_dashboard(user=Depends(get_current_user)):
    user_id = str(user["_id"])

    # Get all progress records
    progress_cursor = progress_collection.find({"user_id": user_id})
    progress_records = []
    async for p in progress_cursor:
        progress_records.append(p)

    # Get all sessions
    session_cursor = sessions_collection.find({"user_id": user_id})
    total_time = 0
    async for s in session_cursor:
        total_time += s.get("time_spent", 0)

    # Calculate stats
    lessons_completed = len(progress_records)
    total_score = sum(p.get("score", 0) for p in progress_records)
    accuracy = round(total_score / lessons_completed, 1) if lessons_completed > 0 else 0

    # Topic distribution and weak areas
    topic_stats = {}
    for p in progress_records:
        lesson = await lessons_collection.find_one({"_id": ObjectId(p["lesson_id"])})
        if lesson:
            topic = lesson["topic"]
            if topic not in topic_stats:
                topic_stats[topic] = {"count": 0, "total_score": 0}
            topic_stats[topic]["count"] += 1
            topic_stats[topic]["total_score"] += p.get("score", 0)

    topic_distribution = []
    weak_areas = []
    for topic, stats in topic_stats.items():
        avg = round(stats["total_score"] / stats["count"], 1) if stats["count"] > 0 else 0
        topic_distribution.append({
            "topic": topic,
            "count": stats["count"],
            "avg_score": avg,
        })
        if avg < 60:
            weak_areas.append(topic)

    # Get fresh user data for XP and streak
    fresh_user = await users_collection.find_one({"_id": user["_id"] if isinstance(user["_id"], ObjectId) else ObjectId(user["_id"])})
    streak = fresh_user.get("streak", 0) if fresh_user else 0
    xp = fresh_user.get("xp", 0) if fresh_user else 0

    return {
        "total_time": total_time,
        "lessons_completed": lessons_completed,
        "accuracy": accuracy,
        "streak": streak,
        "xp": xp,
        "topic_distribution": topic_distribution,
        "weak_areas": weak_areas,
    }


@router.get("/dashboard/all")
async def get_dashboard_all(user=Depends(get_current_user)):
    # Run dashboard, badges and quests logic concurrently
    import asyncio
    
    # We call our existing logic functions
    results = await asyncio.gather(
        get_dashboard(user),
        get_badges(user),
        get_quests(user)
    )
    
    return {
        "stats": results[0],
        "badges": results[1],
        "quests": results[2]
    }
