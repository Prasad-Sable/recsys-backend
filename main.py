from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import lessons_collection
from seed_lessons import generate_lessons
from auth import router as auth_router
from routes.lessons import router as lessons_router
from routes.recommend import router as recommend_router
from routes.quiz import router as quiz_router
from routes.dashboard import router as dashboard_router
from routes.progress import router as progress_router
from routes.gamification import router as gamification_router

app = FastAPI(title="Micro-Learning Recommender System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(lessons_router)
app.include_router(recommend_router)
app.include_router(quiz_router)
app.include_router(dashboard_router)
app.include_router(progress_router)
app.include_router(gamification_router)


@app.on_event("startup")
async def startup_event():
    # Database Indexing for Speed
    from database import users_collection, progress_collection, lessons_collection
    import motor
    
    await users_collection.create_index("email", unique=True)
    await progress_collection.create_index("user_id")
    await lessons_collection.create_index([("topic", 1), ("difficulty", 1)])
    print("🚀 Database Indexes Optimized")

    # Seed lessons if collection is empty
    count = await lessons_collection.count_documents({})
    if count == 0:
        lessons = generate_lessons()
        await lessons_collection.insert_many(lessons)
        print(f"✅ Seeded {len(lessons)} lessons into MongoDB")
    else:
        print(f"📚 Found {count} existing lessons")


@app.get("/")
async def root():
    return {"message": "Micro-Learning Recommender System API", "status": "running"}
