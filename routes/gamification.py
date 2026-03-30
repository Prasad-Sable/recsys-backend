from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from database import badges_collection, quests_collection, progress_collection, users_collection
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/gamification", tags=["gamification"])

# Badges definitions
DEFAULT_BADGES = [
    {"name": "First Steps", "description": "Complete your first lesson.", "icon": "🎓", "condition_type": "lessons_completed", "condition_value": 1},
    {"name": "Bookworm", "description": "Complete 10 lessons.", "icon": "📚", "condition_type": "lessons_completed", "condition_value": 10},
    {"name": "On Fire", "description": "Reach a 3-day streak.", "icon": "🔥", "condition_type": "streak", "condition_value": 3},
    {"name": "Perfect Score", "description": "Get 100% on a quiz.", "icon": "⭐", "condition_type": "perfect_score", "condition_value": 1},
]

# Quests definitions (these would dynamically reset in a real app)
DAILY_QUESTS = [
    {"title": "Daily Learner", "description": "Complete 2 lessons today", "target_value": 2, "xp_reward": 50, "condition_type": "lessons_today"},
    {"title": "Perfect Accuracy", "description": "Get a 100% score on a quiz today", "target_value": 1, "xp_reward": 100, "condition_type": "perfect_score_today"},
]


async def initialize_quests(user_id: str):
    now = datetime.utcnow()
    # Check if quests exist for today
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    existing_quests = await quests_collection.find({"user_id": user_id, "date": {"$gte": today_start}}).to_list(length=10)
    
    if not existing_quests:
        # Create new daily quests
        new_quests = []
        for q in DAILY_QUESTS:
            new_quest = q.copy()
            new_quest["user_id"] = user_id
            new_quest["date"] = now
            new_quest["completed"] = False
            new_quests.append(new_quest)
        if new_quests:
            await quests_collection.insert_many(new_quests)


@router.get("/badges")
async def get_badges(user=Depends(get_current_user)):
    user_id = str(user["_id"])
    
    # Get user's progress records
    progress_records = await progress_collection.find({"user_id": user_id}).to_list(length=1000)
    lessons_completed = len(progress_records)
    perfect_scores = sum(1 for p in progress_records if p.get("score", 0) == 100)
    streak = user.get("streak", 0)

    # Award badges dynamically
    earned_badges = []
    
    for badge in DEFAULT_BADGES:
        earned = False
        if badge["condition_type"] == "lessons_completed" and lessons_completed >= badge["condition_value"]:
            earned = True
        elif badge["condition_type"] == "streak" and streak >= badge["condition_value"]:
            earned = True
        elif badge["condition_type"] == "perfect_score" and perfect_scores >= badge["condition_value"]:
            earned = True
            
        badge_out = badge.copy()
        badge_out["_id"] = badge["name"].lower().replace(" ", "_")
        badge_out["earned"] = earned
        if earned:
            badge_out["earned_at"] = datetime.utcnow() # simplified for demo
        earned_badges.append(badge_out)

    return earned_badges


@router.get("/quests")
async def get_quests(user=Depends(get_current_user)):
    user_id = str(user["_id"])
    
    # Ensure daily quests exist
    await initialize_quests(user_id)
    
    # Get today's quests
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    quests_cursor = quests_collection.find({"user_id": user_id, "date": {"$gte": today_start}})
    
    quests = []
    async for q in quests_cursor:
        # Calculate current progress dynamically
        current_val = 0
        if q["condition_type"] == "lessons_today":
            # fetch progress for today
            today_progress = await progress_collection.count_documents({
                "user_id": user_id, 
                "completed_at": {"$gte": today_start}
            })
            current_val = today_progress
        elif q["condition_type"] == "perfect_score_today":
            today_perfect = await progress_collection.count_documents({
                "user_id": user_id, 
                "score": 100,
                "completed_at": {"$gte": today_start}
            })
            current_val = today_perfect
            
        completed = current_val >= q["target_value"]
        
        # Give XP if newly completed
        if completed and not q.get("completed", False):
            await quests_collection.update_one({"_id": q["_id"]}, {"$set": {"completed": True}})
            # Give XP
            await users_collection.update_one(
                {"_id": user["_id"] if isinstance(user["_id"], ObjectId) else ObjectId(user["_id"])},
                {"$inc": {"xp": q["xp_reward"]}}
            )
            q["completed"] = True
            
        q["_id"] = str(q["_id"])
        q["current_value"] = min(current_val, q["target_value"])
        quests.append(q)
        
    return quests
