from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from database import lessons_collection, progress_collection, sessions_collection, users_collection
from auth import get_current_user
from models import SubmitQuizRequest
from bson import ObjectId
from llm_generator import evaluate_quiz_via_llm

router = APIRouter(tags=["quiz"])


@router.post("/submit-quiz")
async def submit_quiz(req: SubmitQuizRequest, user=Depends(get_current_user)):
    user_id = str(user["_id"])

    # Fetch the lesson
    lesson = await lessons_collection.find_one({"_id": ObjectId(req.lesson_id)})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    quiz = lesson.get("quiz", [])
    if not quiz:
        raise HTTPException(status_code=400, detail="No quiz for this lesson")

    # Convert user answers to dict format for LLM
    answers_dicts = [{"question_index": a.question_index, "selected_option": a.selected_option} for a in req.answers]
    
    # 🧠 Hand off evaluation to LLM
    ai_eval = await evaluate_quiz_via_llm(lesson, answers_dicts)
    
    # Fallback to manual checking if LLM fails
    if ai_eval is None:
        correct = 0
        total = len(quiz)
        for answer in req.answers:
            if answer.question_index < len(quiz):
                q = quiz[answer.question_index]
                opts = q.get("options", [])
                
                # Check based on answer_index (LLM seeds) or is_correct (Mock seeds)
                if answer.selected_option < len(opts):
                    is_correct_manual = opts[answer.selected_option].get("is_correct", False)
                    is_correct_index = q.get("answer_index") == answer.selected_option
                    if is_correct_manual or is_correct_index:
                        correct += 1
                        
        score = (correct / total) * 100 if total > 0 else 0
        feedback = "👍 Good job!" if score >= 50 else "📚 Keep learning!"
    else:
        correct = ai_eval.get("total_correct", 0)
        total = ai_eval.get("total_questions", len(quiz))
        score = float(ai_eval.get("score_percentage", 0))
        feedback = ai_eval.get("feedback", "Excellent effort!")

    # XP calculation
    xp_earned = int(score * 0.5)  # Up to 50 XP per quiz
    if score >= 100:
        xp_earned += 20  # Perfect score bonus

    # Save progress
    progress_doc = {
        "user_id": user_id,
        "lesson_id": req.lesson_id,
        "score": score,
        "correct": correct,
        "total": total,
        "xp_earned": xp_earned,
        "completed_at": datetime.utcnow(),
    }
    
    # Check if already completed - update if so
    existing = await progress_collection.find_one({
        "user_id": user_id, 
        "lesson_id": req.lesson_id
    })
    if existing:
        await progress_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": progress_doc}
        )
    else:
        await progress_collection.insert_one(progress_doc)

    # Save session
    session_doc = {
        "user_id": user_id,
        "time_spent": lesson.get("duration", 5),
        "date": datetime.utcnow(),
    }
    await sessions_collection.insert_one(session_doc)

    # Update user XP
    await users_collection.update_one(
        {"_id": user["_id"] if isinstance(user["_id"], ObjectId) else ObjectId(user["_id"])},
        {"$inc": {"xp": xp_earned}}
    )

    # Update streak
    now = datetime.utcnow()
    last_active = user.get("last_active")
    current_streak = user.get("streak", 0)
    
    if last_active:
        if isinstance(last_active, str):
            last_active = datetime.fromisoformat(last_active)
        days_diff = (now.date() - last_active.date()).days
        if days_diff == 1:
            current_streak += 1
        elif days_diff > 1:
            current_streak = 1
        # If same day, keep streak
    else:
        current_streak = 1

    await users_collection.update_one(
        {"_id": user["_id"] if isinstance(user["_id"], ObjectId) else ObjectId(user["_id"])},
        {"$set": {"streak": current_streak, "last_active": now}}
    )

    return {
        "score": score,
        "correct": correct,
        "total": total,
        "xp_earned": xp_earned,
        "feedback": feedback,
        "streak": current_streak,
    }
