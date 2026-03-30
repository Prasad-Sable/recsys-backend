from fastapi import APIRouter, Depends
from database import lessons_collection, progress_collection
from auth import get_current_user
from models import RecommendRequest
from bson import ObjectId
import random
import asyncio
from llm_generator import create_and_store_lesson

router = APIRouter(tags=["recommendation"])

DIFFICULTY_ORDER = ["Beginner", "Intermediate", "Advanced"]

@router.post("/recommend")
async def recommend_lessons(req: RecommendRequest, user=Depends(get_current_user)):
    user_id = str(user["_id"])
    
    if req.topics and len(req.topics) > 0:
        interests = req.topics
    else:
        interests = user.get("interests", ["Tech", "Fitness", "Study"])
        
    if not interests:
        interests = ["Tech", "Fitness", "Study"]
        
    level = user.get("level", "Beginner")
    available_time = req.available_time

    # Get completed lesson IDs to calculate adaptive difficulty
    completed_cursor = progress_collection.find({"user_id": user_id})
    completed_lessons = {}
    async for p in completed_cursor:
        completed_lessons[p["lesson_id"]] = p.get("score", 0)

    # Calculate average score to determine adaptive difficulty
    scores = list(completed_lessons.values())
    avg_score = sum(scores) / len(scores) if scores else 50

    # Determine target difficulty
    level_idx = DIFFICULTY_ORDER.index(level) if level in DIFFICULTY_ORDER else 0
    if avg_score < 50 and level_idx > 0:
        target_difficulty = DIFFICULTY_ORDER[level_idx - 1]
    elif avg_score >= 80 and level_idx < 2:
        target_difficulty = DIFFICULTY_ORDER[level_idx + 1]
    else:
        target_difficulty = level

    # GENERATE AI LESSONS ON THE FLY
    # Pick 2 random interests to generate lessons for
    selected_topics = random.sample(interests, min(2, len(interests)))
    
    # We will generate 2 lessons concurrently using the OpenRouter AI LLM
    tasks = [
        create_and_store_lesson(topic=topic, difficulty=target_difficulty, duration=available_time)
        for topic in selected_topics
    ]
    
    # Await all LLM generation tasks
    generated_lessons_raw = await asyncio.gather(*tasks)
    
    # Filter out any failed generation attempts
    recommended = [l for l in generated_lessons_raw if l is not None]
    
    # If API fails fully, attempt to fall back to existing database lessons
    if not recommended:
        query = {
            "duration": {"$lte": available_time},
            "topic": {"$in": interests}
        }
        cursor = lessons_collection.find(query).limit(2)
        async for lesson in cursor:
            lesson["_id"] = str(lesson["_id"])
            recommended.append(lesson)

    return {
        "recommendations": recommended,
        "adaptive_info": {
            "avg_score": round(avg_score, 1),
            "target_difficulty": target_difficulty,
            "original_level": level,
        }
    }
