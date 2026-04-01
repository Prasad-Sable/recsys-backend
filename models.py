from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# ─── Auth Models ───────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OnboardingRequest(BaseModel):
    interests: List[str]
    level: str


# ─── Lesson Models ─────────────────────────────────────────
class QuizOption(BaseModel):
    text: str
    is_correct: bool

class QuizQuestion(BaseModel):
    question: str
    options: List[QuizOption]

class LessonOut(BaseModel):
    id: str = Field(alias="_id")
    title: str
    topic: str
    duration: int
    difficulty: str
    content: str
    quiz: List[QuizQuestion]

    class Config:
        populate_by_name = True


# ─── Quiz Models ───────────────────────────────────────────
class QuizAnswer(BaseModel):
    question_index: int
    selected_option: int

class SubmitQuizRequest(BaseModel):
    lesson_id: str
    answers: List[QuizAnswer]

class QuizResult(BaseModel):
    score: float
    correct: int
    total: int
    xp_earned: int
    feedback: str


# ─── Recommendation Models ─────────────────────────────────
class RecommendRequest(BaseModel):
    available_time: int
    topics: Optional[List[str]] = None
    custom_topic: Optional[str] = None


# ─── Dashboard Models ──────────────────────────────────────
class TopicStat(BaseModel):
    topic: str
    count: int
    avg_score: float

class DashboardResponse(BaseModel):
    total_time: int
    lessons_completed: int
    accuracy: float
    streak: int
    xp: int
    topic_distribution: List[TopicStat]
    weak_areas: List[str]


# ─── Progress Models ───────────────────────────────────────
class ProgressRecord(BaseModel):
    lesson_id: str
    score: float
    time_spent: int

# ─── Gamification Models ───────────────────────────────────
class BadgeOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    icon: str
    condition_type: str
    condition_value: int
    earned: bool = False
    earned_at: Optional[datetime] = None

class QuestOut(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    target_value: int
    current_value: int
    xp_reward: int
    completed: bool = False

class GamificationLevel(BaseModel):
    level: int
    xp: int
    next_level_xp: int
